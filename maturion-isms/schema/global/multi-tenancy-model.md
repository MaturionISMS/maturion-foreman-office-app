# Multi-Tenancy Model – Maturion ISMS

**Version**: 1.0  
**Date**: 2025-12-04  
**Status**: Active  
**Build Wave**: 1.2

---

## 1. Purpose

This document defines the **multi-tenancy architecture** for the Maturion ISMS platform.

The multi-tenancy model ensures:
- **Zero cross-tenant data leakage**
- Complete data isolation between organisations
- Scalability to thousands of tenants
- Performance optimization per tenant
- Compliance with GDPR, POPIA, ISO 27001
- Simplified tenant onboarding and offboarding

---

## 2. Multi-Tenancy Strategy

### 2.1 Approach

**Shared Database, Row-Level Isolation**

- Single PostgreSQL database
- All tables include `organisation_id` column
- Row-Level Security (RLS) enforced at database level
- Application-level enforcement as additional layer

**Why this approach?**
- ✅ Cost-effective (shared infrastructure)
- ✅ Easy maintenance (single database to manage)
- ✅ Performance optimization (shared connection pool)
- ✅ Simplified backups and disaster recovery
- ✅ Database-level isolation guarantees

**Alternatives considered**:
- ❌ Separate database per tenant (too expensive, hard to maintain)
- ❌ Separate schema per tenant (PostgreSQL schema limits, complex migrations)

---

## 3. Organisation Model

### 3.1 Organisations Table

```sql
CREATE TABLE organisations (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  
  -- Organisation identity
  name TEXT NOT NULL,
  legal_name TEXT,
  slug TEXT NOT NULL UNIQUE, -- URL-safe identifier
  
  -- Industry classification
  industry TEXT,
  sub_industry TEXT,
  
  -- Location
  country_code CHAR(2), -- ISO 3166-1 alpha-2
  timezone TEXT DEFAULT 'UTC',
  locale TEXT DEFAULT 'en-ZA',
  currency_code CHAR(3) DEFAULT 'ZAR', -- ISO 4217
  
  -- Subscription
  subscription_tier TEXT NOT NULL DEFAULT 'trial', -- trial, basic, professional, enterprise
  subscription_status TEXT NOT NULL DEFAULT 'active', -- active, suspended, cancelled
  subscription_start_date DATE,
  subscription_end_date DATE,
  
  -- Contact
  primary_contact_email TEXT,
  primary_contact_phone TEXT,
  
  -- Audit
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_by UUID, -- System user for initial creation
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_by UUID,
  deleted_at TIMESTAMPTZ NULL,
  deleted_by UUID,
  
  CONSTRAINT chk_subscription_tier CHECK (
    subscription_tier IN ('trial', 'basic', 'professional', 'enterprise')
  ),
  CONSTRAINT chk_subscription_status CHECK (
    subscription_status IN ('active', 'suspended', 'cancelled')
  )
);

-- Indexes
CREATE INDEX idx_organisations_slug ON organisations(slug);
CREATE INDEX idx_organisations_subscription ON organisations(subscription_status, subscription_tier);
CREATE INDEX idx_organisations_deleted ON organisations(deleted_at) WHERE deleted_at IS NULL;
```

### 3.2 Organisation Settings

```sql
CREATE TABLE organisation_settings (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  
  -- Setting key-value
  setting_key TEXT NOT NULL,
  setting_value JSONB NOT NULL,
  setting_type TEXT NOT NULL, -- 'system', 'user_configurable'
  
  -- Metadata
  description TEXT,
  last_modified_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  last_modified_by UUID REFERENCES users(id),
  
  UNIQUE(organisation_id, setting_key)
);

CREATE INDEX idx_organisation_settings_organisation ON organisation_settings(organisation_id);
```

---

## 4. Tenant Isolation Pattern

### 4.1 Standard Table Structure

**ALL module tables MUST include `organisation_id`**:

```sql
CREATE TABLE example_entity (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  
  -- MANDATORY: Tenant isolation
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  
  -- Entity-specific fields
  title TEXT NOT NULL,
  description TEXT,
  status TEXT NOT NULL DEFAULT 'draft',
  
  -- Standard audit fields
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_by UUID NOT NULL REFERENCES users(id),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_by UUID REFERENCES users(id),
  deleted_at TIMESTAMPTZ NULL,
  deleted_by UUID REFERENCES users(id)
);

-- MANDATORY: Index on organisation_id
CREATE INDEX idx_example_entity_organisation ON example_entity(organisation_id);

-- RECOMMENDED: Composite index for common queries
CREATE INDEX idx_example_entity_org_status 
  ON example_entity(organisation_id, status)
  WHERE deleted_at IS NULL;
```

---

## 5. Row-Level Security (RLS)

### 5.1 Enable RLS on All Tables

```sql
-- Enable Row-Level Security
ALTER TABLE example_entity ENABLE ROW LEVEL SECURITY;

-- Policy: Tenant isolation
CREATE POLICY tenant_isolation ON example_entity
  USING (organisation_id = current_setting('app.current_organisation_id', TRUE)::UUID);

-- Policy: Allow INSERT only for current tenant
CREATE POLICY tenant_insert ON example_entity
  FOR INSERT
  WITH CHECK (organisation_id = current_setting('app.current_organisation_id', TRUE)::UUID);

-- Policy: Allow UPDATE only for current tenant
CREATE POLICY tenant_update ON example_entity
  FOR UPDATE
  USING (organisation_id = current_setting('app.current_organisation_id', TRUE)::UUID);

-- Policy: Allow DELETE only for current tenant (soft delete)
CREATE POLICY tenant_delete ON example_entity
  FOR DELETE
  USING (organisation_id = current_setting('app.current_organisation_id', TRUE)::UUID);
```

### 5.2 Set Current Organisation

**At connection or request start**:

```sql
-- Set current organisation context
SET app.current_organisation_id = '01234567-89ab-7def-0123-456789abcdef';
```

**Application layer** (example in Node.js with PostgreSQL):

```typescript
// Set tenant context for this connection/transaction
await client.query(
  'SET app.current_organisation_id = $1',
  [currentOrganisationId]
);

// All subsequent queries are automatically filtered by RLS
const result = await client.query('SELECT * FROM example_entity');
// Only returns rows where organisation_id = currentOrganisationId
```

---

## 6. Application-Level Enforcement

### 6.1 Defensive Programming

**ALWAYS include `organisation_id` in WHERE clauses** (defense in depth):

```sql
-- Good: Explicit organisation_id check
SELECT * FROM entity
WHERE id = :entity_id
  AND organisation_id = :current_organisation_id;

-- Also good: RLS will enforce this, but explicit is better
SELECT * FROM entity
WHERE organisation_id = :current_organisation_id
  AND status = 'active'
  AND deleted_at IS NULL;
```

### 6.2 INSERT Validation

**ALWAYS set `organisation_id` on INSERT**:

```sql
INSERT INTO entity (organisation_id, title, description, created_by)
VALUES (:current_organisation_id, :title, :description, :current_user_id);
```

### 6.3 UPDATE Validation

**ALWAYS include `organisation_id` in UPDATE WHERE clause**:

```sql
UPDATE entity
SET title = :new_title,
    updated_at = NOW(),
    updated_by = :current_user_id
WHERE id = :entity_id
  AND organisation_id = :current_organisation_id;
```

### 6.4 Cross-Tenant Queries (Forbidden)

**NEVER query across tenants** (except for system administrators with special permissions):

```sql
-- ❌ FORBIDDEN: Cross-tenant query
SELECT COUNT(*) FROM entity; -- Returns all tenants' data

-- ✅ CORRECT: Single-tenant query
SELECT COUNT(*) FROM entity
WHERE organisation_id = :current_organisation_id;
```

---

## 7. User Management

### 7.1 Users Table

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  
  -- Tenant association
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  
  -- Identity
  email TEXT NOT NULL,
  full_name TEXT NOT NULL,
  job_title TEXT,
  department TEXT,
  
  -- Authentication (managed by Supabase Auth)
  auth_user_id UUID, -- Supabase auth.users.id
  
  -- Authorization
  role TEXT NOT NULL DEFAULT 'user', -- user, admin, super_admin
  is_active BOOLEAN DEFAULT TRUE,
  
  -- Preferences
  timezone TEXT DEFAULT 'UTC',
  locale TEXT DEFAULT 'en-ZA',
  
  -- Audit
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_by UUID, -- Can be NULL for initial system user
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_by UUID REFERENCES users(id),
  deleted_at TIMESTAMPTZ NULL,
  deleted_by UUID REFERENCES users(id),
  last_login_at TIMESTAMPTZ,
  
  -- Unique constraint: Email per organisation
  CONSTRAINT uq_user_email UNIQUE (organisation_id, email),
  
  -- Valid roles
  CONSTRAINT chk_user_role CHECK (role IN ('user', 'admin', 'super_admin'))
);

-- Indexes
CREATE INDEX idx_users_organisation ON users(organisation_id);
CREATE INDEX idx_users_auth_user ON users(auth_user_id);
CREATE INDEX idx_users_email ON users(email);

-- RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON users
  USING (organisation_id = current_setting('app.current_organisation_id', TRUE)::UUID);
```

### 7.2 User Permissions

```sql
CREATE TABLE user_permissions (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  user_id UUID NOT NULL REFERENCES users(id),
  
  -- Permission
  module TEXT NOT NULL, -- 'pit', 'erm', 'risk_assessment', etc.
  permission TEXT NOT NULL, -- 'view', 'create', 'update', 'delete', 'admin'
  
  -- Grant context
  granted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  granted_by UUID REFERENCES users(id),
  expires_at TIMESTAMPTZ,
  
  UNIQUE(user_id, module, permission)
);

CREATE INDEX idx_user_permissions_user ON user_permissions(user_id);
CREATE INDEX idx_user_permissions_organisation ON user_permissions(organisation_id);

-- RLS
ALTER TABLE user_permissions ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON user_permissions
  USING (organisation_id = current_setting('app.current_organisation_id', TRUE)::UUID);
```

---

## 8. Tenant Onboarding

### 8.1 Create Organisation

```sql
-- Step 1: Create organisation
INSERT INTO organisations (name, legal_name, slug, industry, country_code)
VALUES (
  'ACME Corporation',
  'ACME Corporation (Pty) Ltd',
  'acme-corp',
  'Technology',
  'ZA'
) RETURNING id;

-- Step 2: Create initial admin user
INSERT INTO users (organisation_id, email, full_name, role)
VALUES (
  :new_organisation_id,
  'admin@acme.com',
  'Admin User',
  'admin'
) RETURNING id;

-- Step 3: Grant initial permissions
INSERT INTO user_permissions (organisation_id, user_id, module, permission, granted_by)
VALUES
  (:new_organisation_id, :new_user_id, 'all', 'admin', :new_user_id);

-- Step 4: Create default settings
INSERT INTO organisation_settings (organisation_id, setting_key, setting_value, setting_type)
VALUES
  (:new_organisation_id, 'risk_matrix_size', '"5x5"', 'user_configurable'),
  (:new_organisation_id, 'default_language', '"en-ZA"', 'user_configurable'),
  (:new_organisation_id, 'date_format', '"YYYY-MM-DD"', 'user_configurable');
```

### 8.2 Onboarding Workflow

1. User signs up on platform
2. Create organisation record
3. Create initial admin user
4. Send verification email
5. User verifies email
6. User completes onboarding wizard
7. User invites team members
8. Set up modules (PIT, ERM, etc.)

---

## 9. Tenant Offboarding

### 9.1 Soft Delete Organisation

```sql
-- Soft delete organisation
UPDATE organisations
SET deleted_at = NOW(),
    deleted_by = :admin_user_id,
    subscription_status = 'cancelled'
WHERE id = :organisation_id;

-- Soft delete all users in organisation
UPDATE users
SET deleted_at = NOW(),
    deleted_by = :admin_user_id,
    is_active = FALSE
WHERE organisation_id = :organisation_id;

-- NOTE: Data remains in database for retention period (e.g., 90 days)
```

### 9.2 Hard Delete Organisation (GDPR/POPIA)

```sql
-- After retention period, hard delete all data
DELETE FROM user_permissions WHERE organisation_id = :organisation_id;
DELETE FROM users WHERE organisation_id = :organisation_id;
DELETE FROM organisation_settings WHERE organisation_id = :organisation_id;

-- Delete all module data (PIT, ERM, Risk, etc.)
DELETE FROM project WHERE organisation_id = :organisation_id;
DELETE FROM risk WHERE organisation_id = :organisation_id;
-- ... repeat for all module tables ...

-- Delete organisation
DELETE FROM organisations WHERE id = :organisation_id;

-- Audit log entries remain (metadata only, no sensitive data)
```

---

## 10. Performance Optimization

### 10.1 Partitioning by Tenant

For very large deployments, partition tables by `organisation_id`:

```sql
CREATE TABLE entity_partitioned (
  id UUID NOT NULL,
  organisation_id UUID NOT NULL,
  -- ... other fields ...
  PRIMARY KEY (organisation_id, id)
) PARTITION BY LIST (organisation_id);

-- Create partition per tenant (or per tenant group)
CREATE TABLE entity_org_01234567 PARTITION OF entity_partitioned
  FOR VALUES IN ('01234567-89ab-7def-0123-456789abcdef');
```

**Pros**:
- Better query performance (scan only tenant partition)
- Easier data archival/deletion

**Cons**:
- Complexity (partition management)
- Limits on number of partitions

**Recommendation**: Only use for very large multi-tenant deployments (1000+ tenants).

### 10.2 Tenant-Specific Indexes

For performance-critical queries:

```sql
CREATE INDEX idx_entity_org_status_active
  ON entity(organisation_id, status)
  WHERE deleted_at IS NULL AND status = 'active';
```

---

## 11. Security Best Practices

### 11.1 Isolation Guarantees

- ✅ RLS enforced at database level
- ✅ Application-level validation as additional layer
- ✅ All foreign keys include organisation_id check
- ✅ No cross-tenant foreign keys

### 11.2 Validation Checklist

For every query:
1. ✅ Does it include `organisation_id` filter?
2. ✅ Is RLS enabled on the table?
3. ✅ Is `app.current_organisation_id` set correctly?
4. ✅ Are there any joins that could leak data?

### 11.3 Testing

**Test for cross-tenant leakage**:

```typescript
// Test 1: Query should return only current tenant's data
const org1Data = await queryAsOrg('org-1-uuid');
const org2Data = await queryAsOrg('org-2-uuid');
expect(org1Data).not.toContain(org2Data[0]); // No overlap

// Test 2: Cannot access other tenant's data by ID
const org1EntityId = org1Data[0].id;
const org2Query = await queryEntityAsOrg(org1EntityId, 'org-2-uuid');
expect(org2Query).toBeNull(); // RLS blocks access

// Test 3: Cannot update other tenant's data
const updateResult = await updateEntityAsOrg(org1EntityId, 'org-2-uuid', {title: 'Hacked!'});
expect(updateResult.rowCount).toBe(0); // RLS blocks update
```

---

## 12. Compliance

### 12.1 ISO 27001

**A.9.4.1 Information Access Restriction**:
- ✅ RLS enforces tenant isolation
- ✅ No cross-tenant data access

**A.9.4.2 Secure Log-on Procedures**:
- ✅ Organisation context set at login
- ✅ Session tied to specific tenant

### 12.2 GDPR / POPIA

**Article 32: Security of Processing**:
- ✅ Technical measures to prevent cross-tenant access
- ✅ Database-level isolation guarantees

**Article 17: Right to Erasure**:
- ✅ Soft delete with retention period
- ✅ Hard delete on request
- ✅ Complete data removal per organisation

---

## 13. Monitoring

### 13.1 Metrics to Track

- Tenant count (active, suspended, cancelled)
- Data growth per tenant
- Query performance per tenant
- Cross-tenant query attempts (should be zero!)
- Failed RLS policy checks

### 13.2 Alerts

- Alert on cross-tenant query attempts
- Alert on RLS policy violations
- Alert on orphaned data (organisation_id not found)

---

## 14. Conclusion

The Maturion ISMS multi-tenancy model ensures:

- ✅ Zero cross-tenant data leakage
- ✅ Database-level isolation (RLS)
- ✅ Application-level enforcement (defense in depth)
- ✅ Scalability to thousands of tenants
- ✅ Performance optimization
- ✅ GDPR/POPIA compliance
- ✅ ISO 27001 compliance

**All modules MUST follow this multi-tenancy pattern.**

---

**Prepared by**: Maturion Foreman  
**Build Wave**: 1.2  
**Date**: 2025-12-04
