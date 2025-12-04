# Global Database Architecture – Maturion ISMS

**Version**: 1.0  
**Date**: 2025-12-04  
**Status**: Active  
**Build Wave**: 1.2

---

## 1. Purpose

This document defines the **global database architecture** for the entire Maturion Integrated Security Management System (ISMS).

It establishes:
- Database technology stack
- Global design principles
- Multi-tenancy model
- Data isolation patterns
- Shared infrastructure
- Compliance foundations
- Performance strategies
- Scalability approach

All module-level schemas MUST align with this global architecture.

---

## 2. Technology Stack

### 2.1 Primary Database

**PostgreSQL 15+**

- Relational database for structured ISMS data
- JSONB support for flexible metadata
- Row-level security (RLS) for tenant isolation
- Advanced indexing (B-tree, GiST, GIN, BRIN)
- Full ACID compliance
- Mature tooling and ecosystem

### 2.2 Time-Series Extension

**TimescaleDB**

- Time-series data for logs, events, metrics
- Automatic partitioning and retention policies
- Continuous aggregates for analytics
- High-performance inserts for audit trails
- Compression for historical data

### 2.3 Search Extension

**pg_trgm + Full-Text Search**

- Trigram indexes for fuzzy search
- Full-text search for documents and policies
- Multilingual support
- Performance-optimized search queries

---

## 3. Global Design Principles

### 3.1 One-Time Build Correctness

- Schema designed right the first time
- No retroactive fixes or migrations
- Comprehensive validation before deployment

### 3.2 Zero Regression

- Backwards-compatible schema changes only
- Additive migrations, never destructive
- Versioned schema with clear upgrade paths

### 3.3 Multi-Tenant by Default

- ALL tables include `organisation_id` (tenant key)
- Row-level security (RLS) enforced at database level
- Zero cross-tenant data leakage
- Tenant data fully isolated

### 3.4 Audit-First Design

- Every table includes audit fields (created_at, updated_at, created_by, updated_by)
- Immutable audit logs for compliance
- Event sourcing for critical operations
- Full data lineage tracking

### 3.5 Soft Deletes

- Logical deletes via `deleted_at` field
- No hard deletes except for GDPR/POPIA compliance
- Deleted records remain queryable for audit
- Retention policies for permanent deletion

### 3.6 Explicit Over Implicit

- No magic defaults or conventions
- Explicit foreign keys, indexes, constraints
- Clear naming, no abbreviations
- Self-documenting schema

---

## 4. Global Tables

### 4.1 Tenant Management

```sql
-- organisations (tenant root)
CREATE TABLE organisations (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  name TEXT NOT NULL,
  legal_name TEXT,
  industry TEXT,
  country_code CHAR(2),
  timezone TEXT DEFAULT 'UTC',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at TIMESTAMPTZ NULL
);

-- organisation_settings
CREATE TABLE organisation_settings (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  setting_key TEXT NOT NULL,
  setting_value JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(organisation_id, setting_key)
);
```

### 4.2 User Management

```sql
-- users
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  email TEXT NOT NULL,
  full_name TEXT NOT NULL,
  role TEXT NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at TIMESTAMPTZ NULL,
  UNIQUE(organisation_id, email)
);

-- user_permissions
CREATE TABLE user_permissions (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  user_id UUID NOT NULL REFERENCES users(id),
  module TEXT NOT NULL,
  permission TEXT NOT NULL,
  granted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  granted_by UUID REFERENCES users(id),
  UNIQUE(user_id, module, permission)
);
```

### 4.3 Audit Logs (Immutable)

```sql
-- audit_log (TimescaleDB hypertable)
CREATE TABLE audit_log (
  id UUID NOT NULL,
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  user_id UUID REFERENCES users(id),
  module TEXT NOT NULL,
  entity_type TEXT NOT NULL,
  entity_id UUID NOT NULL,
  action TEXT NOT NULL, -- created, updated, deleted, viewed
  changes JSONB,
  ip_address INET,
  user_agent TEXT,
  
  -- Composite primary key (timestamp + id) for TimescaleDB
  PRIMARY KEY (timestamp, id)
);

-- Convert to TimescaleDB hypertable
SELECT create_hypertable('audit_log', 'timestamp');
```

### 4.4 Event Log (Cross-Module Events)

```sql
-- event_log (TimescaleDB hypertable)
CREATE TABLE event_log (
  id UUID NOT NULL,
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  event_type TEXT NOT NULL,
  source_module TEXT NOT NULL,
  source_entity_type TEXT,
  source_entity_id UUID,
  target_module TEXT,
  target_entity_type TEXT,
  target_entity_id UUID,
  payload JSONB,
  processed_at TIMESTAMPTZ,
  
  -- Composite primary key (timestamp + id) for TimescaleDB
  PRIMARY KEY (timestamp, id)
);

-- Convert to TimescaleDB hypertable
SELECT create_hypertable('event_log', 'timestamp');
```

---

## 5. Shared Schema Patterns

### 5.1 Standard Audit Fields

ALL module tables MUST include:

```sql
-- Tenant isolation
organisation_id UUID NOT NULL REFERENCES organisations(id),

-- Creation tracking
created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
created_by UUID NOT NULL REFERENCES users(id),

-- Update tracking
updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
updated_by UUID REFERENCES users(id),

-- Soft delete
deleted_at TIMESTAMPTZ NULL,
deleted_by UUID REFERENCES users(id)
```

### 5.2 Versioning Pattern

For versioned entities (policies, risk assessments, etc.):

```sql
-- Example: policy table with versioning
CREATE TABLE policies (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  version_number INTEGER NOT NULL DEFAULT 1,
  is_current_version BOOLEAN DEFAULT TRUE,
  parent_version_id UUID REFERENCES policies(id),
  -- ... entity-specific fields ...
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_by UUID NOT NULL REFERENCES users(id),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_by UUID REFERENCES users(id),
  deleted_at TIMESTAMPTZ NULL,
  UNIQUE(organisation_id, id, version_number)
);
```

### 5.3 Status Pattern

For workflow-based entities:

```sql
status TEXT NOT NULL DEFAULT 'draft',
status_changed_at TIMESTAMPTZ,
status_changed_by UUID REFERENCES users(id),

CONSTRAINT valid_status CHECK (status IN ('draft', 'pending_review', 'approved', 'rejected', 'archived'))
```

### 5.4 Retention Pattern

For data retention compliance:

```sql
retention_until TIMESTAMPTZ,
retention_reason TEXT,
is_legally_protected BOOLEAN DEFAULT FALSE
```

---

## 6. Indexing Strategy

### 6.1 Primary Indexes

- Primary key on `id` (UUID) - clustered index
- Unique index on natural keys (e.g., `organisation_id + email`)

### 6.2 Foreign Key Indexes

ALL foreign keys MUST have indexes:

```sql
CREATE INDEX idx_users_organisation_id ON users(organisation_id);
CREATE INDEX idx_user_permissions_user_id ON user_permissions(user_id);
```

### 6.3 Query Optimization Indexes

For common query patterns:

```sql
-- Multi-tenant queries
CREATE INDEX idx_entity_org_deleted ON entity(organisation_id, deleted_at);

-- Status filtering
CREATE INDEX idx_entity_status ON entity(status) WHERE deleted_at IS NULL;

-- Time-range queries
CREATE INDEX idx_entity_created_at ON entity(created_at DESC);
```

### 6.4 Full-Text Search Indexes

For text search:

```sql
CREATE INDEX idx_policy_title_trgm ON policies USING gin(title gin_trgm_ops);
CREATE INDEX idx_policy_content_fts ON policies USING gin(to_tsvector('english', content));
```

---

## 7. Multi-Tenancy Implementation

### 7.1 Row-Level Security (RLS)

Enable RLS on ALL tables:

```sql
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own org's data
CREATE POLICY tenant_isolation ON users
  USING (organisation_id = current_setting('app.current_organisation_id')::UUID);
```

### 7.2 Application-Level Enforcement

- Set `app.current_organisation_id` at connection time
- Validate organisation_id on all INSERT/UPDATE operations
- Include organisation_id in all WHERE clauses

### 7.3 Isolation Guarantees

- No queries can return data from other organisations
- No cross-tenant foreign keys
- Separate search indexes per tenant (if needed)

---

## 8. Performance & Scalability

### 8.1 Partitioning

- Partition large tables by `organisation_id` (tenant)
- Partition time-series tables by time (TimescaleDB automatic)
- Partition audit logs by month

### 8.2 Connection Pooling

- PgBouncer for connection pooling
- Max 100 connections per module
- Transaction-level pooling for read-only queries

### 8.3 Read Replicas

- Read-only replicas for reporting and analytics
- Write to primary, read from replicas
- Eventual consistency acceptable for dashboards

### 8.4 Caching

- Redis for session data and hot lookups
- Cached data includes organisation_id
- Cache invalidation on updates

---

## 9. Backup & Recovery

### 9.1 Backup Strategy

- Full backup daily at 02:00 UTC
- Incremental backups every 4 hours
- Point-in-time recovery (PITR) enabled
- 30-day retention for backups

### 9.2 Disaster Recovery

- RTO (Recovery Time Objective): 1 hour
- RPO (Recovery Point Objective): 15 minutes
- Cross-region backup replication
- Automated failover for high availability

---

## 10. Compliance & Security

### 10.1 Encryption

- Encryption at rest (AES-256)
- Encryption in transit (TLS 1.3)
- Encrypted backups
- Key rotation every 90 days

### 10.2 Data Lineage

- Full audit trail via `audit_log`
- Event sourcing for critical changes
- Immutable logs (no updates or deletes)

### 10.3 Retention & Deletion

- Soft deletes by default (`deleted_at`)
- Hard deletes for GDPR/POPIA right-to-be-forgotten
- Automated retention policy enforcement
- Legal hold support

### 10.4 Compliance Mapping

- ISO 27001: Audit logs, access control, encryption
- GDPR/POPIA: Data minimization, retention, deletion
- NIST CSF: Logging, monitoring, incident response

---

## 11. Migration & Versioning

### 11.1 Schema Versioning

- Semantic versioning for schema (MAJOR.MINOR.PATCH)
- Migrations tracked in `schema_migrations` table
- Backwards-compatible changes only (MINOR/PATCH)
- Breaking changes require MAJOR version bump

### 11.2 Migration Process

1. Write migration script (up and down)
2. Test on staging environment
3. Validate data integrity
4. Apply to production during maintenance window
5. Monitor for errors and rollback if needed

### 11.3 Zero-Downtime Migrations

- Additive changes (new columns, tables)
- Blue-green deployment for breaking changes
- Feature flags for gradual rollout

---

## 12. Integration Foundations

### 12.1 Cross-Module Relationships

- Use event log for loose coupling
- Avoid direct foreign keys across modules
- Use integration tables for many-to-many relationships

### 12.2 Event-Driven Architecture

- Publish events to `event_log` on state changes
- Subscribe to events in other modules
- Asynchronous processing for non-critical paths

---

## 13. Monitoring & Observability

### 13.1 Database Metrics

- Query performance (slow query log)
- Connection pool utilization
- Index usage statistics
- Table bloat monitoring

### 13.2 Alerting

- Slow queries > 1 second
- Connection pool exhaustion
- Replication lag > 5 seconds
- Backup failures

---

## 14. Governance

### 14.1 Schema Changes

- All schema changes require Foreman approval
- Schema changes tracked in version control
- No direct production schema changes
- All changes via migration scripts

### 14.2 Documentation

- Schema documented in `tables.md`, `fields.md`, `relationships.md`
- ERD diagrams auto-generated from schema
- API documentation auto-generated from schema

---

## 15. Conclusion

This global database architecture ensures:

- ✅ Multi-tenant isolation
- ✅ Audit-first design for compliance
- ✅ Scalability and performance
- ✅ Security and encryption
- ✅ Disaster recovery
- ✅ One-time build correctness
- ✅ Zero regression evolution

All module-level schemas MUST adhere to this global architecture.

**Next Steps**:
1. Implement module-level schemas following this architecture
2. Create global tables (organisations, users, audit_log, event_log)
3. Enable RLS on all tables
4. Deploy TimescaleDB extension
5. Set up backup and monitoring

---

**Prepared by**: Maturion Foreman  
**Build Wave**: 1.2  
**Date**: 2025-12-04
