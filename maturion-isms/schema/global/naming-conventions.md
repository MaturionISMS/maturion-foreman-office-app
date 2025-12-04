# Database Naming Conventions – Maturion ISMS

**Version**: 1.0  
**Date**: 2025-12-04  
**Status**: Active  
**Build Wave**: 1.2

---

## 1. Purpose

This document defines **mandatory naming conventions** for all database objects across the Maturion ISMS ecosystem.

Consistency in naming ensures:
- Code readability and maintainability
- Reduced cognitive load for developers
- Predictable query patterns
- Automated tooling compatibility
- Cross-module consistency

**ALL** schemas, tables, columns, indexes, constraints, and functions MUST follow these conventions.

---

## 2. General Principles

### 2.1 Case Convention

**snake_case** for all identifiers:
- Lowercase letters only
- Words separated by underscores
- No camelCase, PascalCase, or UPPERCASE

✅ **Correct**: `user_permissions`, `created_at`, `organisation_id`  
❌ **Incorrect**: `UserPermissions`, `createdAt`, `OrganisationID`

### 2.2 Singular vs Plural

**Singular nouns** for table names:
- `user` not `users`
- `project` not `projects`
- `risk_assessment` not `risk_assessments`

Exception: Junction/link tables use both entity names in singular:
- `user_role` (links user and role)
- `project_personnel` (links project and personnel)

### 2.3 Abbreviations

**Avoid abbreviations** unless universally understood:

✅ **Allowed**: `id`, `uuid`, `url`, `iso`, `gdpr`, `api`  
❌ **Avoid**: `usr`, `prj`, `org`, `desc`, `addr`

Use full words:
- `description` not `desc`
- `address` not `addr`
- `organisation` not `org`
- `maximum` not `max`

### 2.4 Reserved Words

**Avoid PostgreSQL reserved words** as identifiers:
- `user` → Use `app_user` or `system_user`
- `order` → Use `purchase_order` or `work_order`
- `group` → Use `user_group` or `permission_group`

If unavoidable, quote the identifier: `"user"` (but strongly discouraged).

---

## 3. Table Naming

### 3.1 Standard Tables

Format: `{entity_name}`

Examples:
- `personnel`
- `risk_assessment`
- `threat`
- `vulnerability`
- `policy`
- `project`
- `task`

### 3.2 Junction Tables

Format: `{entity1}_{entity2}`

Examples:
- `project_personnel` (many-to-many: projects and personnel)
- `policy_control` (many-to-many: policies and controls)
- `risk_threat` (many-to-many: risks and threats)

### 3.3 Versioned Tables

Format: `{entity_name}_version`

Examples:
- `policy_version`
- `risk_assessment_version`
- `procedure_version`

### 3.4 Audit/Log Tables

Format: `{entity_name}_audit` or `{entity_name}_log`

Examples:
- `audit_log` (global audit log)
- `event_log` (global event log)
- `risk_change_log`
- `policy_approval_log`

### 3.5 Lookup/Reference Tables

Format: `{entity_name}_lookup` or `ref_{entity_name}`

Examples:
- `status_lookup`
- `ref_country`
- `ref_industry`
- `severity_level_lookup`

---

## 4. Column Naming

### 4.1 Primary Key

**Always** use `id` as the primary key column name:

```sql
id UUID PRIMARY KEY DEFAULT generate_uuidv7()
```

- Type: UUID (preferred) or BIGSERIAL
- Never use composite primary keys unless absolutely necessary
- Never use natural keys as primary keys

### 4.2 Foreign Keys

Format: `{referenced_table}_id`

Examples:
- `organisation_id` → references `organisations(id)`
- `user_id` → references `users(id)`
- `project_id` → references `project(id)`
- `parent_risk_id` → references `risk(id)` (self-reference)

### 4.3 Timestamps

**Mandatory audit timestamps**:

```sql
created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
deleted_at TIMESTAMPTZ NULL  -- soft delete
```

**Other timestamp columns**:
- `{action}_at`: `approved_at`, `submitted_at`, `completed_at`, `archived_at`
- `{event}_timestamp`: `login_timestamp`, `access_timestamp`

Always use `TIMESTAMPTZ` (timestamp with time zone), never `TIMESTAMP`.

### 4.4 User References

**Mandatory audit user references**:

```sql
created_by UUID NOT NULL REFERENCES users(id)
updated_by UUID REFERENCES users(id)
deleted_by UUID REFERENCES users(id)  -- soft delete
```

**Other user references**:
- `{action}_by`: `approved_by`, `submitted_by`, `assigned_to`, `reviewed_by`

### 4.5 Boolean Flags

Format: `is_{condition}` or `has_{condition}`

Examples:
- `is_active`
- `is_deleted`
- `is_approved`
- `has_attachments`
- `has_children`

Default: `DEFAULT FALSE` unless otherwise specified.

### 4.6 Status Fields

Format: `{entity}_status` or just `status`

Examples:
- `status` (when context is clear)
- `approval_status`
- `review_status`

Use ENUM types for status values:
```sql
status risk_status_enum NOT NULL DEFAULT 'draft'
```

### 4.7 Numeric Fields

- **Integers**: `{name}_count`, `{name}_number`
  - `employee_count`, `version_number`, `retry_count`
  
- **Decimals**: `{name}_amount`, `{name}_value`, `{name}_rate`
  - `budget_amount NUMERIC(12,2)`
  - `completion_percentage NUMERIC(5,2)`
  - `risk_score NUMERIC(10,2)`

- **Currency**: Always use `NUMERIC(12,2)` for monetary values
  - `total_amount`, `budget_allocated`, `cost_estimate`

### 4.8 Text Fields

- **Short text**: `{name}` (VARCHAR or TEXT)
  - `title`, `name`, `description`, `notes`
  
- **Long text**: `{name}_text` or `{name}_content`
  - `policy_text`, `procedure_content`, `review_notes`

- **URLs**: `{name}_url`
  - `website_url`, `documentation_url`

- **Codes**: `{name}_code`
  - `country_code`, `currency_code`, `iso_code`

### 4.9 JSONB Fields

Format: `{name}_metadata` or `{name}_data` or `{name}_config`

Examples:
- `custom_fields` (flexible metadata)
- `configuration_data`
- `settings_metadata`
- `integration_config`

Use JSONB (not JSON) for better performance.

### 4.10 Array Fields

Format: `{name}_list` or `{name}s` (plural)

Examples:
- `tags TEXT[]`
- `email_addresses TEXT[]`
- `attachment_ids UUID[]`

Prefer junction tables over arrays for relational data.

---

## 5. Index Naming

### 5.1 Primary Key Index

Automatically created, use default name: `{table_name}_pkey`

### 5.2 Foreign Key Index

Format: `idx_{table}_{column}`

Examples:
- `idx_user_organisation_id`
- `idx_project_created_by`
- `idx_risk_parent_risk_id`

### 5.3 Unique Index

Format: `uq_{table}_{column(s)}`

Examples:
- `uq_user_email` (single column unique)
- `uq_personnel_organisation_employee_number` (multi-column unique)

### 5.4 Composite Index

Format: `idx_{table}_{column1}_{column2}[_{columnN}]`

Examples:
- `idx_risk_organisation_status`
- `idx_audit_log_organisation_timestamp`
- `idx_project_organisation_deleted_created`

### 5.5 Partial Index

Format: `idx_{table}_{column}_where_{condition}`

Examples:
- `idx_user_email_where_active`
- `idx_risk_status_where_not_deleted`

### 5.6 Full-Text Search Index

Format: `idx_{table}_{column}_fts`

Examples:
- `idx_policy_title_fts`
- `idx_procedure_content_fts`

### 5.7 Trigram Index

Format: `idx_{table}_{column}_trgm`

Examples:
- `idx_personnel_name_trgm`
- `idx_project_title_trgm`

---

## 6. Constraint Naming

### 6.1 Primary Key Constraint

Format: `pk_{table}`

Example:
```sql
CONSTRAINT pk_user PRIMARY KEY (id)
```

PostgreSQL default: `{table}_pkey` (acceptable).

### 6.2 Foreign Key Constraint

Format: `fk_{table}_{referenced_table}`

Examples:
- `fk_user_organisation`
- `fk_project_created_by`
- `fk_risk_parent_risk`

```sql
CONSTRAINT fk_user_organisation FOREIGN KEY (organisation_id) REFERENCES organisations(id)
```

### 6.3 Unique Constraint

Format: `uq_{table}_{column(s)}`

Examples:
- `uq_user_email`
- `uq_personnel_organisation_employee_number`

```sql
CONSTRAINT uq_user_email UNIQUE (organisation_id, email)
```

### 6.4 Check Constraint

Format: `chk_{table}_{column}_{condition}`

Examples:
- `chk_risk_score_range`
- `chk_percentage_valid`
- `chk_status_valid`

```sql
CONSTRAINT chk_risk_score_range CHECK (risk_score BETWEEN 0 AND 100)
CONSTRAINT chk_status_valid CHECK (status IN ('draft', 'approved', 'archived'))
```

---

## 7. ENUM Type Naming

Format: `{entity}_{field}_enum`

Examples:
- `risk_status_enum`
- `approval_status_enum`
- `severity_level_enum`
- `priority_level_enum`

```sql
CREATE TYPE risk_status_enum AS ENUM ('draft', 'pending_review', 'approved', 'archived');
```

---

## 8. Function Naming

### 8.1 General Functions

Format: `{verb}_{entity}[_{detail}]`

Examples:
- `calculate_risk_score()`
- `update_project_status()`
- `validate_email_format()`
- `generate_report_summary()`

### 8.2 Trigger Functions

Format: `trg_{action}_{table}_{event}`

Examples:
- `trg_update_timestamp_on_update()`
- `trg_audit_log_on_change()`
- `trg_validate_status_on_insert()`

```sql
CREATE TRIGGER trg_update_timestamp
  BEFORE UPDATE ON users
  FOR EACH ROW
  EXECUTE FUNCTION trg_update_timestamp_on_update();
```

---

## 9. View Naming

Format: `v_{purpose}` or `vw_{purpose}`

Examples:
- `v_active_users`
- `v_open_risks`
- `vw_project_summary`
- `vw_compliance_dashboard`

Materialized views: `mv_{purpose}`

Examples:
- `mv_risk_analytics`
- `mv_project_metrics`

---

## 10. Schema Naming

Format: `{module_name}` (lowercase)

Examples:
- `public` (global tables: organisations, users, audit_log)
- `pit` (Project Implementation Tracker)
- `erm` (Enterprise Risk Management)
- `threat` (Threat Management)
- `vulnerability` (Vulnerability Management)

**Note**: Single-tenant deployment uses `public` schema with `organisation_id` filtering.  
Multi-tenant deployment may use separate schemas per tenant: `tenant_{uuid}`.

---

## 11. Sequence Naming

Format: `seq_{table}_{column}`

Examples:
- `seq_invoice_number`
- `seq_project_code`

```sql
CREATE SEQUENCE seq_invoice_number START 1000;
```

---

## 12. Module-Specific Conventions

### 12.1 PIT (Project Implementation Tracker)

- `project`, `phase`, `work_package`, `task`, `subtask`
- `project_personnel`, `project_milestone`
- Prefixes: None (PIT is implicit in module schema)

### 12.2 ERM (Enterprise Risk Management)

- `risk`, `risk_category`, `risk_assessment`
- `risk_control`, `risk_owner`
- Prefixes: None

### 12.3 Threat Management

- `threat`, `threat_category`, `threat_source`
- `threat_vulnerability` (junction table)
- Prefixes: None

### 12.4 Vulnerability Management

- `vulnerability`, `vulnerability_category`, `vulnerability_assessment`
- `vulnerability_fix`, `vulnerability_patch`
- Prefixes: None

---

## 13. Anti-Patterns (DO NOT USE)

❌ **Avoid**:
- Hungarian notation: `tblUser`, `strName`, `intCount`
- Mixed case: `UserPermissions`, `ProjectID`
- Abbreviations: `usr`, `prj`, `org`
- Reserved words: `user`, `order`, `group`
- Plural table names: `users`, `projects`
- Generic names: `data`, `info`, `temp`
- Prefixes: `tb_`, `tbl_`, `idx_` (except for indexes/constraints)

✅ **Use instead**:
- Clean snake_case: `user_permission`, `project_id`
- Full words: `user`, `project`, `organisation`
- Descriptive names: `project_metadata`, `risk_assessment_data`

---

## 14. Validation Rules

All naming must pass these checks:

1. ✅ snake_case only (lowercase + underscores)
2. ✅ No abbreviations (except allowed list)
3. ✅ Singular table names
4. ✅ Descriptive and self-documenting
5. ✅ Foreign keys end with `_id`
6. ✅ Timestamps end with `_at`
7. ✅ Booleans start with `is_` or `has_`
8. ✅ No reserved words without quoting

Automated validation tool: `validate-schema-naming.py`

---

## 15. Examples

### ✅ Good Naming

```sql
CREATE TABLE risk_assessment (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  title TEXT NOT NULL,
  description TEXT,
  risk_score NUMERIC(10,2),
  status risk_status_enum NOT NULL DEFAULT 'draft',
  is_approved BOOLEAN DEFAULT FALSE,
  approved_at TIMESTAMPTZ,
  approved_by UUID REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_by UUID NOT NULL REFERENCES users(id),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_by UUID REFERENCES users(id),
  deleted_at TIMESTAMPTZ NULL,
  CONSTRAINT chk_risk_score_range CHECK (risk_score BETWEEN 0 AND 100)
);

CREATE INDEX idx_risk_assessment_organisation_id ON risk_assessment(organisation_id);
CREATE INDEX idx_risk_assessment_status ON risk_assessment(status) WHERE deleted_at IS NULL;
```

### ❌ Bad Naming

```sql
-- DON'T DO THIS!
CREATE TABLE RiskAssessments (
  ID INT PRIMARY KEY,
  OrgID INT NOT NULL REFERENCES Orgs(ID),
  RiskTitle VARCHAR(255),
  Desc TEXT,
  Score DECIMAL(10,2),
  Stat VARCHAR(50),
  IsApproved BIT,
  ApprovedDate DATETIME,
  ApprovedByUserID INT,
  CreatedDate DATETIME,
  CreatedByUserID INT
);
```

---

## 16. Enforcement

- Schema changes reviewed by Foreman
- Automated linting before PR approval
- CI/CD checks for naming compliance
- Documentation auto-generated from schema

**All naming violations MUST be fixed before merge.**

---

## 17. Conclusion

Consistent naming is **non-negotiable** in the Maturion ISMS ecosystem.

Follow these conventions to ensure:
- ✅ Code clarity
- ✅ Cross-module consistency
- ✅ Automated tooling compatibility
- ✅ Developer productivity
- ✅ Long-term maintainability

**When in doubt, ask Foreman.**

---

**Prepared by**: Maturion Foreman  
**Build Wave**: 1.2  
**Date**: 2025-12-04
