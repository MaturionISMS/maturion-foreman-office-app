# ID Strategy – Maturion ISMS

**Version**: 1.0  
**Date**: 2025-12-04  
**Status**: Active  
**Build Wave**: 1.2

---

## 1. Purpose

This document defines the **ID generation and management strategy** for all entities across the Maturion ISMS ecosystem.

The ID strategy ensures:
- Globally unique identifiers
- Time-ordered creation tracking
- Distributed system compatibility
- Performance optimization
- Security and privacy
- Compliance and auditability

---

## 2. Primary Key Strategy

### 2.1 Technology Choice

**UUID Version 7 (UUIDv7)** is the standard for all primary keys.

**Why UUIDv7?**
- ✅ Globally unique across distributed systems
- ✅ Time-ordered (sortable by creation time)
- ✅ 128-bit (highly collision-resistant)
- ✅ No central coordination required
- ✅ Database-friendly (B-tree index performance)
- ✅ Non-guessable (security)
- ✅ Embeds timestamp (auditability)

**Format**: `01234567-89ab-7def-0123-456789abcdef`
- First 48 bits: Unix timestamp (milliseconds)
- Next 12 bits: Random bits
- Next 2 bits: Version (0111 = v7)
- Next 62 bits: Random bits

### 2.2 Implementation

**PostgreSQL Extension**: `uuid-ossp` or `pgcrypto`

```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- UUIDv7 generation function (PostgreSQL 17+)
CREATE OR REPLACE FUNCTION generate_uuidv7() RETURNS UUID AS $$
DECLARE
  unix_ts_ms BIGINT;
  uuid_bytes BYTEA;
BEGIN
  unix_ts_ms := FLOOR(EXTRACT(EPOCH FROM NOW()) * 1000);
  uuid_bytes := 
    LPAD(TO_HEX(unix_ts_ms)::BYTEA, 6, '0') ||
    gen_random_bytes(10);
  -- Set version and variant bits
  uuid_bytes := SET_BYTE(uuid_bytes, 6, (GET_BYTE(uuid_bytes, 6) & 0x0F) | 0x70);
  uuid_bytes := SET_BYTE(uuid_bytes, 8, (GET_BYTE(uuid_bytes, 8) & 0x3F) | 0x80);
  RETURN ENCODE(uuid_bytes, 'hex')::UUID;
END;
$$ LANGUAGE plpgsql VOLATILE;

-- Table definition with UUIDv7
CREATE TABLE example_entity (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  -- ... other fields ...
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**For PostgreSQL < 17**: Use `gen_random_uuid()` (UUIDv4) as fallback:

```sql
id UUID PRIMARY KEY DEFAULT gen_random_uuid()
```

### 2.3 ID Column Definition

**Standard primary key column**:

```sql
id UUID PRIMARY KEY DEFAULT generate_uuidv7()
```

- **Name**: Always `id` (never `uuid`, `guid`, `entity_id`)
- **Type**: `UUID` (not `CHAR(36)` or `VARCHAR(36)`)
- **Constraint**: `PRIMARY KEY`
- **Default**: `generate_uuidv7()` or `gen_random_uuid()`

---

## 3. Foreign Key Strategy

### 3.1 Foreign Key Naming

Format: `{referenced_table}_id`

Examples:
- `organisation_id` → references `organisations(id)`
- `user_id` → references `users(id)`
- `parent_risk_id` → references `risk(id)` (self-reference)

### 3.2 Foreign Key Definition

```sql
organisation_id UUID NOT NULL REFERENCES organisations(id)
```

- **Type**: `UUID` (matches primary key)
- **NOT NULL**: Required (unless truly optional)
- **REFERENCES**: Explicit foreign key constraint
- **ON DELETE**: Specify behavior (RESTRICT, CASCADE, SET NULL)

### 3.3 Foreign Key Indexes

**ALWAYS** create indexes on foreign key columns:

```sql
CREATE INDEX idx_{table}_{fk_column} ON {table}({fk_column});
```

Example:
```sql
CREATE INDEX idx_user_organisation_id ON users(organisation_id);
```

---

## 4. Composite Keys (Avoid)

### 4.1 When to Avoid

❌ **Do NOT use composite primary keys** unless absolutely necessary:
- Reduces query complexity
- Improves join performance
- Simplifies ORM mapping
- Better for distributed systems

### 4.2 When to Use

✅ **Use composite UNIQUE constraints** instead:

```sql
CREATE TABLE personnel (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  employee_number TEXT NOT NULL,
  -- ... other fields ...
  CONSTRAINT uq_personnel_organisation_employee 
    UNIQUE (organisation_id, employee_number)
);
```

This allows:
- Simple primary key (`id`)
- Natural key uniqueness (`organisation_id + employee_number`)
- Efficient foreign key references

---

## 5. Natural Keys vs Surrogate Keys

### 5.1 Surrogate Key (UUID)

**Primary key**: Always use surrogate key (UUID).

Benefits:
- Stable (never changes)
- Globally unique
- No business logic dependency
- Safe for foreign key references

### 5.2 Natural Key

**Unique constraint**: Use for natural keys (email, employee_number, etc.).

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  email TEXT NOT NULL,
  CONSTRAINT uq_user_email UNIQUE (organisation_id, email)
);
```

Benefits:
- Enforces uniqueness at database level
- Supports efficient lookups
- Allows natural key changes without breaking references

---

## 6. Sequential IDs (When Needed)

### 6.1 Use Cases

Sequential IDs are needed for:
- Invoice numbers
- Project codes
- Ticket numbers
- Any user-visible identifier that must be sequential

### 6.2 Implementation

**Use PostgreSQL SEQUENCE**:

```sql
CREATE SEQUENCE seq_invoice_number START 1000;

CREATE TABLE invoice (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  invoice_number BIGINT NOT NULL DEFAULT nextval('seq_invoice_number'),
  -- ... other fields ...
  CONSTRAINT uq_invoice_number UNIQUE (organisation_id, invoice_number)
);
```

**Multi-Tenant Sequences**:

For tenant-specific sequential numbers:

```sql
CREATE TABLE invoice (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  invoice_number BIGINT NOT NULL,
  -- ... other fields ...
  CONSTRAINT uq_invoice_number UNIQUE (organisation_id, invoice_number)
);

-- Application logic generates next number per organisation
-- SELECT COALESCE(MAX(invoice_number), 0) + 1 
-- FROM invoice 
-- WHERE organisation_id = :org_id
-- FOR UPDATE; -- Lock to prevent race conditions
```

---

## 7. ID Encoding and Formatting

### 7.1 Internal Representation

**PostgreSQL**: Store as native `UUID` type (16 bytes).

```sql
id UUID PRIMARY KEY DEFAULT generate_uuidv7()
```

### 7.2 API Representation

**JSON/REST API**: Represent as lowercase hyphenated string.

```json
{
  "id": "01234567-89ab-7def-0123-456789abcdef",
  "organisation_id": "98765432-10ab-7cde-f012-3456789abcde"
}
```

**GraphQL**: Use `ID` scalar type.

```graphql
type User {
  id: ID!
  organisationId: ID!
}
```

### 7.3 URL Encoding

**REST URLs**: Use UUIDs directly (no encoding needed).

```
GET /api/v1/users/01234567-89ab-7def-0123-456789abcdef
```

**Short IDs**: If needed for user-facing URLs, use base62 encoding:

```
https://app.maturion.com/p/AbC123XyZ
```

Store mapping in database:
```sql
CREATE TABLE short_url (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  short_code TEXT NOT NULL UNIQUE,
  entity_type TEXT NOT NULL,
  entity_id UUID NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

## 8. ID Validation

### 8.1 Format Validation

**PostgreSQL**: Native UUID validation (automatically enforced).

**Application Layer**: Validate UUID format before queries.

```typescript
function isValidUUID(uuid: string): boolean {
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  return uuidRegex.test(uuid);
}
```

### 8.2 Existence Validation

Always validate that referenced IDs exist:

```sql
-- Foreign key constraint enforces this automatically
organisation_id UUID NOT NULL REFERENCES organisations(id)
```

### 8.3 Tenant Validation

Always validate that the ID belongs to the current tenant:

```sql
SELECT * FROM entity
WHERE id = :entity_id
  AND organisation_id = :current_organisation_id;
```

---

## 9. ID Generation Performance

### 9.1 Database-Generated UUIDs

**Pros**:
- Consistent across all inserts
- No application dependency
- Guaranteed uniqueness

**Cons**:
- Requires database round-trip for `RETURNING id`

```sql
INSERT INTO users (organisation_id, email, full_name)
VALUES (:org_id, :email, :name)
RETURNING id;
```

### 9.2 Application-Generated UUIDs

**Pros**:
- No database round-trip needed
- Can insert batches without waiting for IDs

**Cons**:
- Application must implement UUIDv7 generation
- Risk of incorrect implementation

**Recommendation**: Use database-generated UUIDs for consistency and reliability.

---

## 10. ID Security

### 10.1 Non-Guessable IDs

UUIDs are **non-sequential and non-guessable**:
- ✅ Cannot enumerate entities by incrementing ID
- ✅ Cannot infer creation order (though UUIDv7 is sortable)
- ✅ Cannot guess other tenant's IDs

### 10.2 Authorization Checks

**ALWAYS** validate tenant ownership:

```sql
-- Good: Includes organisation_id check
SELECT * FROM risk
WHERE id = :risk_id
  AND organisation_id = :current_organisation_id;

-- Bad: No tenant check (security vulnerability!)
SELECT * FROM risk
WHERE id = :risk_id;
```

### 10.3 Exposure in Logs

**Avoid logging full UUIDs** in production logs (GDPR/POPIA concern).

Log truncated UUIDs for debugging:

```typescript
logger.info(`Processing user ${userId.substring(0, 8)}...`);
// Output: Processing user 01234567...
```

---

## 11. ID Indexing

### 11.1 Primary Key Index

Automatically created as clustered B-tree index:

```sql
id UUID PRIMARY KEY DEFAULT generate_uuidv7()
-- Auto-creates: {table}_pkey index
```

### 11.2 Foreign Key Index

**ALWAYS** create index on foreign keys:

```sql
CREATE INDEX idx_user_organisation_id ON users(organisation_id);
```

### 11.3 Composite Index

For multi-column queries:

```sql
CREATE INDEX idx_risk_organisation_status 
  ON risk(organisation_id, status)
  WHERE deleted_at IS NULL;
```

---

## 12. ID Aliasing (Self-Referencing Tables)

For self-referencing tables (parent-child relationships):

```sql
CREATE TABLE risk (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  parent_risk_id UUID REFERENCES risk(id),
  -- ... other fields ...
);

CREATE INDEX idx_risk_parent_risk_id ON risk(parent_risk_id);
```

Query:
```sql
-- Get risk with its parent
SELECT r.*, p.title AS parent_title
FROM risk r
LEFT JOIN risk p ON r.parent_risk_id = p.id
WHERE r.id = :risk_id
  AND r.organisation_id = :org_id;
```

---

## 13. ID Migration Strategy

### 13.1 From Integer IDs to UUIDs

If migrating from integer IDs:

```sql
-- Step 1: Add new UUID column
ALTER TABLE legacy_table ADD COLUMN uuid_id UUID DEFAULT generate_uuidv7();

-- Step 2: Backfill UUIDs
UPDATE legacy_table SET uuid_id = generate_uuidv7() WHERE uuid_id IS NULL;

-- Step 3: Add unique constraint
ALTER TABLE legacy_table ADD CONSTRAINT uq_legacy_table_uuid_id UNIQUE (uuid_id);

-- Step 4: Update foreign keys in other tables (gradual migration)

-- Step 5: Make UUID primary key (requires downtime)
ALTER TABLE legacy_table DROP CONSTRAINT legacy_table_pkey;
ALTER TABLE legacy_table ADD PRIMARY KEY (uuid_id);
ALTER TABLE legacy_table DROP COLUMN id;
ALTER TABLE legacy_table RENAME COLUMN uuid_id TO id;
```

### 13.2 From UUIDv4 to UUIDv7

No migration needed (both are valid UUIDs).

For new records:
```sql
ALTER TABLE entity ALTER COLUMN id SET DEFAULT generate_uuidv7();
```

Existing records keep their UUIDv4 values (no impact).

---

## 14. Special Cases

### 14.1 Global Reference Tables

For read-only global reference data (countries, industries, etc.):

```sql
CREATE TABLE ref_country (
  code CHAR(2) PRIMARY KEY, -- ISO 3166-1 alpha-2
  name TEXT NOT NULL,
  is_active BOOLEAN DEFAULT TRUE
);
```

Use natural key (country code) instead of UUID.

### 14.2 Temporal Tables (Versioning)

For versioned entities:

```sql
CREATE TABLE policy_version (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  policy_id UUID NOT NULL REFERENCES policy(id),
  version_number INTEGER NOT NULL,
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  -- ... versioned fields ...
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_policy_version UNIQUE (policy_id, version_number)
);
```

- `id`: Unique ID for each version
- `policy_id`: Links to parent policy
- `version_number`: Sequential version number

---

## 15. Conclusion

The Maturion ISMS ID strategy ensures:

- ✅ Globally unique identifiers (UUIDv7)
- ✅ Time-ordered creation tracking
- ✅ Distributed system compatibility
- ✅ Database performance (B-tree friendly)
- ✅ Security (non-guessable)
- ✅ Tenant isolation enforcement
- ✅ Compliance and auditability

**All modules MUST use UUIDv7 for primary keys.**

---

**Prepared by**: Maturion Foreman  
**Build Wave**: 1.2  
**Date**: 2025-12-04
