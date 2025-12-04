# Global Database Schema – Maturion ISMS

**Version**: 1.0  
**Date**: 2025-12-04  
**Build Wave**: 1.2

---

## Purpose

This directory contains **global database architecture specifications** that apply to ALL modules in the Maturion ISMS ecosystem.

Every module MUST adhere to these global standards.

---

## Documentation

### 1. Database Architecture (`database-architecture.md`)

Defines the overall database technology stack, design principles, and global infrastructure:
- PostgreSQL 15+ as primary database
- TimescaleDB for time-series data
- Multi-tenancy model (row-level isolation)
- Global tables (organisations, users, audit_log, event_log)
- Performance and scalability strategies
- Backup and recovery approach
- Compliance and security foundations

**Key Decisions**:
- Shared database with row-level security
- UUID v7 for primary keys
- Soft deletes by default
- Audit-first design

---

### 2. Naming Conventions (`naming-conventions.md`)

Mandatory naming standards for all database objects:
- `snake_case` for all identifiers
- Singular table names
- Standard foreign key naming (`{table}_id`)
- Standard timestamp fields (`created_at`, `updated_at`, `deleted_at`)
- Boolean fields start with `is_` or `has_`
- Index naming patterns
- ENUM type naming
- Function and trigger naming

**Non-Negotiable**: All schema changes MUST follow these conventions.

---

### 3. ID Strategy (`id-strategy.md`)

UUID Version 7 strategy for all primary keys:
- Time-ordered UUIDs (sortable by creation time)
- Globally unique across distributed systems
- Database-friendly (B-tree index performance)
- Non-guessable (security)
- Implementation with PostgreSQL `generate_uuidv7()`
- Foreign key patterns
- Natural key vs surrogate key guidance
- Sequential IDs when needed (invoice numbers, etc.)

**Standard Primary Key**: `id UUID PRIMARY KEY DEFAULT generate_uuidv7()`

---

### 4. Audit Strategy (`audit-strategy.md`)

Comprehensive audit and tracking strategy:
- Mandatory audit fields (created_at, created_by, updated_at, updated_by)
- Soft delete pattern (deleted_at, deleted_by)
- Immutable audit log (TimescaleDB hypertable)
- Full change tracking (before/after values)
- Automatic timestamp updates via triggers
- Retention policies (7 years for audit logs)
- Compliance with ISO 27001, GDPR, POPIA, NIST CSF

**Mandatory Fields**: Every table MUST include audit fields.

---

### 5. Multi-Tenancy Model (`multi-tenancy-model.md`)

Row-level tenant isolation strategy:
- `organisation_id` in ALL tables
- Row-Level Security (RLS) enforced at database level
- Application-level enforcement (defense in depth)
- Zero cross-tenant data leakage
- Organisation and user management
- Tenant onboarding and offboarding
- Security best practices

**Mandatory Field**: Every table MUST include `organisation_id UUID NOT NULL REFERENCES organisations(id)`

---

### 6. TimescaleDB Strategy (`timescale-strategy.md`)

Time-series data management with TimescaleDB:
- Hypertables for audit_log and event_log
- Automatic time-based partitioning
- Data retention policies (automatic cleanup)
- Compression (90% storage savings)
- Continuous aggregates (pre-computed analytics)
- Performance optimization for time-range queries
- Backup and recovery

**Use TimescaleDB For**: audit_log, event_log, metrics, any time-series data

---

### 7. Cross-Module Relationships (`relationships-guide.md`)

Integration patterns for cross-module references:
- Loose coupling (no direct FKs across modules)
- Event-driven integration via event_log
- Integration tables for many-to-many relationships
- Denormalization patterns (store frequently accessed fields)
- Eventual consistency strategy
- Application-level referential integrity
- Specific patterns for PIT ↔ WRAC, Threat ↔ Vulnerability, ERM ↔ Risk Assessment, etc.

**Key Pattern**: Use integration tables + event log instead of direct foreign keys.

---

## Global Tables

### Organisations

```sql
CREATE TABLE organisations (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  name TEXT NOT NULL,
  legal_name TEXT,
  slug TEXT NOT NULL UNIQUE,
  industry TEXT,
  country_code CHAR(2),
  timezone TEXT DEFAULT 'UTC',
  subscription_tier TEXT NOT NULL DEFAULT 'trial',
  subscription_status TEXT NOT NULL DEFAULT 'active',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at TIMESTAMPTZ NULL
);
```

### Users

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  email TEXT NOT NULL,
  full_name TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'user',
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at TIMESTAMPTZ NULL,
  CONSTRAINT uq_user_email UNIQUE (organisation_id, email)
);
```

### Audit Log (TimescaleDB Hypertable)

```sql
CREATE TABLE audit_log (
  id UUID NOT NULL,
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  user_id UUID REFERENCES users(id),
  module TEXT NOT NULL,
  entity_type TEXT NOT NULL,
  entity_id UUID NOT NULL,
  action TEXT NOT NULL,
  changes JSONB,
  ip_address INET,
  user_agent TEXT,
  PRIMARY KEY (timestamp, id)
);

SELECT create_hypertable('audit_log', 'timestamp');
```

### Event Log (TimescaleDB Hypertable)

```sql
CREATE TABLE event_log (
  id UUID NOT NULL,
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  event_type TEXT NOT NULL,
  source_module TEXT NOT NULL,
  source_entity_id UUID,
  target_module TEXT,
  target_entity_id UUID,
  payload JSONB,
  processed_at TIMESTAMPTZ,
  PRIMARY KEY (timestamp, id)
);

SELECT create_hypertable('event_log', 'timestamp');
```

---

## Module Schema Requirements

Every module MUST:

1. ✅ Include `organisation_id` in all tables
2. ✅ Include standard audit fields (created_at, created_by, updated_at, updated_by, deleted_at, deleted_by)
3. ✅ Use UUID v7 for primary keys
4. ✅ Follow naming conventions (snake_case, singular tables, etc.)
5. ✅ Enable Row-Level Security (RLS) on all tables
6. ✅ Create index on `organisation_id` for all tables
7. ✅ Use soft deletes (deleted_at) instead of hard deletes
8. ✅ Log all changes to audit_log (via trigger)
9. ✅ Publish cross-module events to event_log
10. ✅ Use integration tables for cross-module relationships

---

## Validation

Run automated validation before deploying any schema:

```bash
# Validate schema naming conventions
python3 tools/validate-schema-naming.py

# Validate audit fields presence
python3 tools/validate-audit-fields.py

# Validate RLS policies
python3 tools/validate-rls-policies.py

# Validate indexes
python3 tools/validate-indexes.py
```

---

## Examples

### Standard Module Table

```sql
CREATE TABLE example_entity (
  -- Primary key (UUID v7)
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  
  -- Tenant isolation (MANDATORY)
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  
  -- Entity fields
  title TEXT NOT NULL,
  description TEXT,
  status TEXT NOT NULL DEFAULT 'draft',
  
  -- Audit fields (MANDATORY)
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_by UUID NOT NULL REFERENCES users(id),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_by UUID REFERENCES users(id),
  deleted_at TIMESTAMPTZ NULL,
  deleted_by UUID REFERENCES users(id)
);

-- Indexes (MANDATORY)
CREATE INDEX idx_example_entity_organisation ON example_entity(organisation_id);
CREATE INDEX idx_example_entity_org_status ON example_entity(organisation_id, status)
  WHERE deleted_at IS NULL;

-- Row-Level Security (MANDATORY)
ALTER TABLE example_entity ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON example_entity
  USING (organisation_id = current_setting('app.current_organisation_id', TRUE)::UUID);

-- Timestamp update trigger (MANDATORY)
CREATE TRIGGER trg_update_timestamp
  BEFORE UPDATE ON example_entity
  FOR EACH ROW
  EXECUTE FUNCTION trg_update_timestamp();

-- Audit log trigger (RECOMMENDED for sensitive tables)
CREATE TRIGGER trg_audit_log
  AFTER INSERT OR UPDATE OR DELETE ON example_entity
  FOR EACH ROW
  EXECUTE FUNCTION trg_audit_log();
```

---

## Governance

- All schema changes require Foreman approval
- Schema documented in module-specific `tables.md`, `fields.md`, `relationships.md`
- ERD diagrams auto-generated from schema
- Migration scripts for all schema changes
- No direct production schema changes (migrations only)

---

## Next Steps

1. Review all global architecture documents
2. Understand mandatory patterns and conventions
3. Design module-specific schemas
4. Validate against global standards
5. Implement migration scripts
6. Deploy and monitor

---

**Prepared by**: Maturion Foreman  
**Build Wave**: 1.2  
**Date**: 2025-12-04
