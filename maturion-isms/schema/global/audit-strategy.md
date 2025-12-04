# Audit Strategy – Maturion ISMS

**Version**: 1.0  
**Date**: 2025-12-04  
**Status**: Active  
**Build Wave**: 1.2

---

## 1. Purpose

This document defines the **audit and tracking strategy** for the entire Maturion ISMS ecosystem.

The audit strategy ensures:
- Full compliance with ISO 27001, GDPR, POPIA, NIST CSF
- Complete data lineage and change tracking
- Immutable audit logs
- Forensic investigation capabilities
- User accountability
- Security incident response support

---

## 2. Audit Principles

### 2.1 Audit-First Design

**Every table** includes mandatory audit fields:
- Who created it (`created_by`)
- When it was created (`created_at`)
- Who last updated it (`updated_by`)
- When it was last updated (`updated_at`)
- Who deleted it (`deleted_by` - soft delete only)
- When it was deleted (`deleted_at` - soft delete only)

### 2.2 Immutability

**Audit logs are immutable**:
- No UPDATE operations on audit_log table
- No DELETE operations on audit_log table
- Append-only event log
- Tamper-evident logging

### 2.3 Completeness

**All changes are logged**:
- CREATE operations
- UPDATE operations (with before/after values)
- DELETE operations (soft delete)
- VIEW operations (for sensitive data)
- EXPORT operations
- PERMISSION changes

---

## 3. Standard Audit Fields

### 3.1 Mandatory Fields (All Tables)

**Every module table MUST include these fields**:

```sql
CREATE TABLE example_entity (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  
  -- Entity-specific fields here
  
  -- MANDATORY AUDIT FIELDS
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_by UUID NOT NULL REFERENCES users(id),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_by UUID REFERENCES users(id),
  deleted_at TIMESTAMPTZ NULL,
  deleted_by UUID REFERENCES users(id)
);
```

### 3.2 Field Specifications

#### created_at
- **Type**: `TIMESTAMPTZ` (timestamp with time zone)
- **Constraint**: `NOT NULL`
- **Default**: `NOW()`
- **Purpose**: Record creation timestamp
- **Never updated**: Set once on INSERT

#### created_by
- **Type**: `UUID`
- **Constraint**: `NOT NULL`
- **References**: `users(id)`
- **Purpose**: User who created the record
- **Never updated**: Set once on INSERT

#### updated_at
- **Type**: `TIMESTAMPTZ`
- **Constraint**: `NOT NULL`
- **Default**: `NOW()`
- **Purpose**: Last modification timestamp
- **Auto-updated**: On every UPDATE via trigger

#### updated_by
- **Type**: `UUID`
- **Constraint**: `NULL` (initially NULL)
- **References**: `users(id)`
- **Purpose**: User who last modified the record
- **Auto-updated**: On every UPDATE via trigger

#### deleted_at
- **Type**: `TIMESTAMPTZ`
- **Constraint**: `NULL`
- **Purpose**: Soft delete timestamp
- **Set once**: On soft delete operation

#### deleted_by
- **Type**: `UUID`
- **Constraint**: `NULL`
- **References**: `users(id)`
- **Purpose**: User who deleted the record
- **Set once**: On soft delete operation

---

## 4. Automatic Timestamp Updates

### 4.1 Trigger Function

**Auto-update `updated_at` on every UPDATE**:

```sql
CREATE OR REPLACE FUNCTION trg_update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  NEW.updated_by = current_setting('app.current_user_id', TRUE)::UUID;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### 4.2 Apply Trigger to All Tables

```sql
CREATE TRIGGER trg_update_timestamp
  BEFORE UPDATE ON example_entity
  FOR EACH ROW
  EXECUTE FUNCTION trg_update_timestamp();
```

**This trigger MUST be applied to EVERY module table.**

---

## 5. Immutable Audit Log

### 5.1 Audit Log Table (TimescaleDB Hypertable)

```sql
CREATE TABLE audit_log (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  
  -- Timestamp (TimescaleDB partition key)
  timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  
  -- User context
  user_id UUID REFERENCES users(id),
  user_email TEXT,
  user_role TEXT,
  
  -- Module context
  module TEXT NOT NULL,
  entity_type TEXT NOT NULL,
  entity_id UUID NOT NULL,
  
  -- Action performed
  action TEXT NOT NULL, -- 'created', 'updated', 'deleted', 'viewed', 'exported'
  
  -- Change details
  changes JSONB, -- Before/after values for updates
  
  -- Request context
  ip_address INET,
  user_agent TEXT,
  request_id UUID,
  
  -- Compliance metadata
  retention_until TIMESTAMPTZ,
  is_legally_protected BOOLEAN DEFAULT FALSE
);

-- Convert to TimescaleDB hypertable (partitioned by timestamp)
SELECT create_hypertable('audit_log', 'timestamp');

-- Indexes
CREATE INDEX idx_audit_log_organisation_timestamp 
  ON audit_log(organisation_id, timestamp DESC);
CREATE INDEX idx_audit_log_entity 
  ON audit_log(entity_type, entity_id);
CREATE INDEX idx_audit_log_user 
  ON audit_log(user_id, timestamp DESC);
CREATE INDEX idx_audit_log_module_action 
  ON audit_log(module, action);
```

### 5.2 Audit Log Trigger

**Automatically log all changes to audit_log**:

```sql
CREATE OR REPLACE FUNCTION trg_audit_log()
RETURNS TRIGGER AS $$
DECLARE
  v_user_id UUID;
  v_user_email TEXT;
  v_action TEXT;
  v_changes JSONB;
BEGIN
  -- Get user context
  v_user_id := current_setting('app.current_user_id', TRUE)::UUID;
  v_user_email := current_setting('app.current_user_email', TRUE);
  
  -- Determine action
  IF TG_OP = 'INSERT' THEN
    v_action := 'created';
    v_changes := to_jsonb(NEW);
  ELSIF TG_OP = 'UPDATE' THEN
    v_action := 'updated';
    v_changes := jsonb_build_object(
      'before', to_jsonb(OLD),
      'after', to_jsonb(NEW)
    );
  ELSIF TG_OP = 'DELETE' THEN
    v_action := 'deleted';
    v_changes := to_jsonb(OLD);
  END IF;
  
  -- Insert audit log entry
  INSERT INTO audit_log (
    organisation_id,
    timestamp,
    user_id,
    user_email,
    module,
    entity_type,
    entity_id,
    action,
    changes,
    ip_address,
    user_agent
  ) VALUES (
    COALESCE(NEW.organisation_id, OLD.organisation_id),
    NOW(),
    v_user_id,
    v_user_email,
    TG_TABLE_SCHEMA,
    TG_TABLE_NAME,
    COALESCE(NEW.id, OLD.id),
    v_action,
    v_changes,
    current_setting('app.client_ip', TRUE)::INET,
    current_setting('app.user_agent', TRUE)
  );
  
  RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;
```

### 5.3 Apply Audit Trigger to Tables

```sql
CREATE TRIGGER trg_audit_log
  AFTER INSERT OR UPDATE OR DELETE ON example_entity
  FOR EACH ROW
  EXECUTE FUNCTION trg_audit_log();
```

**This trigger SHOULD be applied to all sensitive tables.**

---

## 6. Soft Delete Strategy

### 6.1 Soft Delete Pattern

**Never hard delete records** (except for GDPR/POPIA compliance).

```sql
-- Soft delete (sets deleted_at)
UPDATE entity
SET deleted_at = NOW(),
    deleted_by = :current_user_id
WHERE id = :entity_id
  AND organisation_id = :current_organisation_id
  AND deleted_at IS NULL;
```

### 6.2 Querying Active Records

**Always filter out deleted records**:

```sql
SELECT * FROM entity
WHERE organisation_id = :org_id
  AND deleted_at IS NULL;
```

### 6.3 Partial Index for Active Records

```sql
CREATE INDEX idx_entity_organisation_active
  ON entity(organisation_id)
  WHERE deleted_at IS NULL;
```

### 6.4 Hard Delete (GDPR/POPIA Right to be Forgotten)

```sql
-- Hard delete (permanent removal)
DELETE FROM entity
WHERE id = :entity_id
  AND organisation_id = :org_id
  AND deleted_at IS NOT NULL; -- Must be soft deleted first

-- Audit log entry remains (but entity data is removed)
```

---

## 7. Additional Audit Fields (Conditional)

### 7.1 Approval Workflow

For entities requiring approval:

```sql
approved_at TIMESTAMPTZ,
approved_by UUID REFERENCES users(id),
approval_notes TEXT
```

### 7.2 Review Workflow

For entities requiring periodic review:

```sql
last_reviewed_at TIMESTAMPTZ,
last_reviewed_by UUID REFERENCES users(id),
next_review_date DATE,
review_frequency_days INTEGER
```

### 7.3 Archival

For entities that can be archived:

```sql
archived_at TIMESTAMPTZ,
archived_by UUID REFERENCES users(id),
archive_reason TEXT
```

### 7.4 Publication

For entities that can be published:

```sql
published_at TIMESTAMPTZ,
published_by UUID REFERENCES users(id),
is_published BOOLEAN DEFAULT FALSE
```

---

## 8. Retention Policies

### 8.1 Retention Fields

```sql
retention_until TIMESTAMPTZ,
retention_reason TEXT,
is_legally_protected BOOLEAN DEFAULT FALSE
```

### 8.2 Retention Policy Examples

**Audit logs**:
- Default retention: 7 years
- Legal hold: Indefinite
- Automatic deletion after retention period

**Soft deleted records**:
- Retention: 90 days after deletion
- Automatic hard delete after retention period

**Archived records**:
- Retention: As per organisational policy
- No automatic deletion

### 8.3 Retention Enforcement

```sql
-- Automatic deletion of expired audit logs (TimescaleDB)
SELECT add_retention_policy('audit_log', INTERVAL '7 years');

-- Automatic hard delete of expired soft deletes
DELETE FROM entity
WHERE deleted_at IS NOT NULL
  AND deleted_at < NOW() - INTERVAL '90 days'
  AND is_legally_protected = FALSE;
```

---

## 9. Compliance Mapping

### 9.1 ISO 27001

**A.12.4.1 Event Logging**:
- ✅ Audit log captures all security events
- ✅ User login/logout, access attempts
- ✅ Data access and modification

**A.12.4.2 Protection of Log Information**:
- ✅ Immutable audit logs (no updates/deletes)
- ✅ Access control on audit_log table
- ✅ Log integrity verification

**A.12.4.3 Administrator and Operator Logs**:
- ✅ Admin actions logged to audit_log
- ✅ Privileged operations tracked

**A.12.4.4 Clock Synchronization**:
- ✅ TIMESTAMPTZ ensures time zone consistency
- ✅ NTP synchronization at server level

### 9.2 GDPR / POPIA

**Article 30: Records of Processing Activities**:
- ✅ Full data lineage via audit_log
- ✅ Who accessed what, when, and why

**Article 17: Right to Erasure**:
- ✅ Soft delete for audit purposes
- ✅ Hard delete for right-to-be-forgotten
- ✅ Audit log entry remains (metadata only)

**Article 32: Security of Processing**:
- ✅ Immutable audit trail
- ✅ Tamper-evident logging
- ✅ Forensic investigation support

### 9.3 NIST CSF

**PR.PT-1: Audit/log records**:
- ✅ Comprehensive audit log
- ✅ Timestamped, attributed, immutable

**DE.AE-3: Event data aggregated**:
- ✅ TimescaleDB for efficient log aggregation
- ✅ Continuous aggregates for analytics

**RS.AN-1: Forensic analysis**:
- ✅ Immutable audit log for forensics
- ✅ Full change history available

---

## 10. Query Patterns

### 10.1 Get Entity History

```sql
SELECT 
  al.timestamp,
  u.full_name AS user_name,
  al.action,
  al.changes
FROM audit_log al
LEFT JOIN users u ON al.user_id = u.id
WHERE al.entity_type = 'risk'
  AND al.entity_id = :risk_id
  AND al.organisation_id = :org_id
ORDER BY al.timestamp DESC;
```

### 10.2 Get User Activity

```sql
SELECT 
  al.timestamp,
  al.module,
  al.entity_type,
  al.action
FROM audit_log al
WHERE al.user_id = :user_id
  AND al.organisation_id = :org_id
  AND al.timestamp >= NOW() - INTERVAL '30 days'
ORDER BY al.timestamp DESC
LIMIT 100;
```

### 10.3 Get Recent Changes (Dashboard)

```sql
SELECT 
  al.timestamp,
  u.full_name AS user_name,
  al.entity_type,
  al.action
FROM audit_log al
LEFT JOIN users u ON al.user_id = u.id
WHERE al.organisation_id = :org_id
  AND al.timestamp >= NOW() - INTERVAL '7 days'
ORDER BY al.timestamp DESC
LIMIT 50;
```

---

## 11. Performance Considerations

### 11.1 TimescaleDB Partitioning

- Audit log partitioned by `timestamp`
- Automatic data retention policies
- Compressed older partitions (10x space savings)

### 11.2 Indexes

- Index on `(organisation_id, timestamp DESC)`
- Index on `(entity_type, entity_id)`
- Index on `(user_id, timestamp DESC)`

### 11.3 Query Optimization

- Use time-range filters to limit partitions scanned
- Avoid `SELECT *` on audit_log (JSONB can be large)
- Use continuous aggregates for dashboard queries

---

## 12. Security

### 12.1 Access Control

**Only audit administrators can query audit_log**:

```sql
GRANT SELECT ON audit_log TO audit_admin_role;
REVOKE ALL ON audit_log FROM PUBLIC;
```

### 12.2 Row-Level Security

```sql
ALTER TABLE audit_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON audit_log
  USING (organisation_id = current_setting('app.current_organisation_id')::UUID);
```

### 12.3 Immutability

**No UPDATE or DELETE on audit_log**:

```sql
REVOKE UPDATE, DELETE ON audit_log FROM ALL;
```

---

## 13. Conclusion

The Maturion ISMS audit strategy ensures:

- ✅ Full compliance with ISO 27001, GDPR, POPIA, NIST CSF
- ✅ Complete data lineage and change tracking
- ✅ Immutable audit logs
- ✅ Forensic investigation capabilities
- ✅ User accountability
- ✅ Security incident response support
- ✅ Performance-optimized with TimescaleDB

**All modules MUST implement these audit fields and patterns.**

---

**Prepared by**: Maturion Foreman  
**Build Wave**: 1.2  
**Date**: 2025-12-04
