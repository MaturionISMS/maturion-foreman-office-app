# FOREMAN_DATABASE_SCHEMA_v1.0.md

## Johan's Foreman Office — Database Schema Specification

**Version**: 1.0  
**Date**: 2025-12-15  
**Database**: PostgreSQL (Supabase)  
**Tenant Isolation**: organisation_id (future: multi-tenant)

---

## 1. TABLES

### 1.1 programs

```sql
CREATE TABLE programs (
    program_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    objectives JSONB NOT NULL DEFAULT '[]',
    state TEXT NOT NULL CHECK (state IN ('planned', 'in-progress', 'blocked', 'completed', 'failed')),
    progress_percentage INTEGER NOT NULL DEFAULT 0 CHECK (progress_percentage BETWEEN 0 AND 100),
    evidence_location TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by UUID,
    organisation_id UUID -- Future: enforce tenant isolation
);

CREATE INDEX idx_programs_state ON programs(state);
CREATE INDEX idx_programs_org ON programs(organisation_id);
```

### 1.2 waves

```sql
CREATE TABLE waves (
    wave_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    program_id UUID NOT NULL REFERENCES programs(program_id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    sequence_number INTEGER NOT NULL,
    dependencies JSONB NOT NULL DEFAULT '[]', -- Array of wave_ids
    state TEXT NOT NULL CHECK (state IN ('planned', 'in-progress', 'blocked', 'completed', 'failed')),
    progress_percentage INTEGER NOT NULL DEFAULT 0 CHECK (progress_percentage BETWEEN 0 AND 100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(program_id, sequence_number)
);

CREATE INDEX idx_waves_program ON waves(program_id);
CREATE INDEX idx_waves_state ON waves(state);
```

### 1.3 tasks

```sql
CREATE TABLE tasks (
    task_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    wave_id UUID NOT NULL REFERENCES waves(wave_id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    architecture_reference TEXT NOT NULL,
    qa_suite_location TEXT NOT NULL,
    acceptance_criteria TEXT NOT NULL,
    assigned_builder TEXT CHECK (assigned_builder IN ('ui-builder', 'api-builder', 'schema-builder', 'integration-builder', 'qa-builder')),
    state TEXT NOT NULL CHECK (state IN ('planned', 'assigned', 'in-progress', 'blocked', 'completed', 'failed')),
    progress_percentage INTEGER NOT NULL DEFAULT 0 CHECK (progress_percentage BETWEEN 0 AND 100),
    evidence_location TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ
);

CREATE INDEX idx_tasks_wave ON tasks(wave_id);
CREATE INDEX idx_tasks_state ON tasks(state);
CREATE INDEX idx_tasks_builder ON tasks(assigned_builder);
```

### 1.4 builders

```sql
CREATE TABLE builders (
    builder_id TEXT PRIMARY KEY CHECK (builder_id IN ('ui-builder', 'api-builder', 'schema-builder', 'integration-builder', 'qa-builder')),
    backend_type TEXT NOT NULL CHECK (backend_type IN ('local', 'hosted', 'burst')),
    current_task_id UUID REFERENCES tasks(task_id),
    state TEXT NOT NULL CHECK (state IN ('idle', 'active', 'blocked', 'failed')),
    last_heartbeat TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    provenance JSONB NOT NULL DEFAULT '{}', -- {model, escalation_rationale}
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_builders_state ON builders(state);
CREATE INDEX idx_builders_heartbeat ON builders(last_heartbeat);
```

### 1.5 blockers

```sql
CREATE TABLE blockers (
    blocker_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type TEXT NOT NULL CHECK (entity_type IN ('program', 'wave', 'task')),
    entity_id UUID NOT NULL,
    classification TEXT NOT NULL CHECK (classification IN (
        'architecture_qa_mismatch',
        'impossible_requirements',
        'protected_path',
        'repeated_failures',
        'constitutional_violation',
        'builder_stall'
    )),
    description TEXT NOT NULL,
    detected_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    resolved_at TIMESTAMPTZ,
    resolution_action TEXT
);

CREATE INDEX idx_blockers_entity ON blockers(entity_type, entity_id);
CREATE INDEX idx_blockers_unresolved ON blockers(resolved_at) WHERE resolved_at IS NULL;
```

### 1.6 heartbeats

```sql
CREATE TABLE heartbeats (
    heartbeat_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    builder_id TEXT NOT NULL REFERENCES builders(builder_id),
    task_id UUID REFERENCES tasks(task_id),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status TEXT NOT NULL CHECK (status IN ('active', 'idle', 'blocked')),
    message TEXT,
    progress_percentage INTEGER CHECK (progress_percentage BETWEEN 0 AND 100)
);

CREATE INDEX idx_heartbeats_builder ON heartbeats(builder_id, timestamp DESC);
CREATE INDEX idx_heartbeats_task ON heartbeats(task_id);
```

### 1.7 evidence_trail

```sql
CREATE TABLE evidence_trail (
    evidence_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type TEXT NOT NULL CHECK (entity_type IN ('program', 'wave', 'task', 'builder')),
    entity_id UUID NOT NULL,
    action TEXT NOT NULL,
    actor TEXT NOT NULL, -- 'foreman' or builder_id
    backend TEXT, -- 'local', 'hosted', 'burst'
    model TEXT, -- model used
    context JSONB NOT NULL DEFAULT '{}',
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_evidence_entity ON evidence_trail(entity_type, entity_id, timestamp DESC);
CREATE INDEX idx_evidence_timestamp ON evidence_trail(timestamp DESC);
```

### 1.8 governance_violations

```sql
CREATE TABLE governance_violations (
    violation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID REFERENCES tasks(task_id),
    builder_id TEXT REFERENCES builders(builder_id),
    violation_type TEXT NOT NULL,
    description TEXT NOT NULL,
    detected_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    resolution TEXT,
    resolved_at TIMESTAMPTZ
);

CREATE INDEX idx_violations_task ON governance_violations(task_id);
CREATE INDEX idx_violations_builder ON governance_violations(builder_id);
CREATE INDEX idx_violations_unresolved ON governance_violations(resolved_at) WHERE resolved_at IS NULL;
```

### 1.9 architecture_validations

```sql
CREATE TABLE architecture_validations (
    validation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID NOT NULL REFERENCES tasks(task_id),
    architecture_reference TEXT NOT NULL,
    validation_results JSONB NOT NULL, -- Checklist results
    pass_rate NUMERIC(5,2) NOT NULL CHECK (pass_rate BETWEEN 0 AND 100),
    build_readiness TEXT NOT NULL CHECK (build_readiness IN ('READY', 'NOT_READY')),
    validated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    validated_by TEXT NOT NULL DEFAULT 'foreman'
);

CREATE INDEX idx_arch_validations_task ON architecture_validations(task_id);
```

### 1.10 qa_executions

```sql
CREATE TABLE qa_executions (
    execution_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID NOT NULL REFERENCES tasks(task_id),
    qa_suite_location TEXT NOT NULL,
    total_tests INTEGER NOT NULL,
    passing_tests INTEGER NOT NULL,
    failing_tests INTEGER NOT NULL,
    skipped_tests INTEGER NOT NULL,
    test_debt_count INTEGER NOT NULL DEFAULT 0,
    qa_status TEXT NOT NULL CHECK (qa_status IN ('RED', 'PARTIAL', 'GREEN')),
    executed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    execution_time_ms INTEGER
);

CREATE INDEX idx_qa_executions_task ON qa_executions(task_id, executed_at DESC);
```

---

## 2. RELATIONSHIPS

```
programs (1) ──< (N) waves
waves (1) ──< (N) tasks
builders (1) ──< (1) tasks (current_task)
tasks (1) ──< (N) blockers
tasks (1) ──< (N) heartbeats
tasks (1) ──< (N) evidence_trail
tasks (1) ──< (N) architecture_validations
tasks (1) ──< (N) qa_executions
```

---

## 3. INDEXES

All foreign keys have indexes (listed above).

Additional indexes for performance:
- State-based queries (programs, waves, tasks, builders)
- Timestamp-based queries (evidence_trail, heartbeats)
- Unresolved blockers and violations

---

## 4. CONSTRAINTS

### 4.1 Check Constraints

- State enums enforced at database level
- Progress percentage: 0-100
- Pass rate: 0-100
- Builder types: ui, api, schema, integration, qa
- Backend types: local, hosted, burst

### 4.2 Unique Constraints

- Program names globally unique
- Wave sequence numbers unique within program

### 4.3 Foreign Key Constraints

- ON DELETE CASCADE for waves → programs
- ON DELETE CASCADE for tasks → waves
- ON DELETE RESTRICT for builders → tasks (current_task)

---

## 5. ROW LEVEL SECURITY (RLS)

**Future Implementation** (Wave 1+):

```sql
-- Enable RLS on all tables
ALTER TABLE programs ENABLE ROW LEVEL SECURITY;
ALTER TABLE waves ENABLE ROW LEVEL SECURITY;
-- ... etc for all tables

-- Policy: Users can only access their org's data
CREATE POLICY org_isolation ON programs
    USING (organisation_id = current_user_org_id());
```

**Wave 0**: RLS not enforced (single-tenant for Maturion governance)

---

## 6. TRIGGERS

### 6.1 Updated At Trigger

```sql
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER programs_updated_at BEFORE UPDATE ON programs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER waves_updated_at BEFORE UPDATE ON waves
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER tasks_updated_at BEFORE UPDATE ON tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER builders_updated_at BEFORE UPDATE ON builders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

### 6.2 Progress Calculation Trigger

```sql
CREATE OR REPLACE FUNCTION calculate_wave_progress()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE waves SET progress_percentage = (
        SELECT AVG(progress_percentage)::INTEGER
        FROM tasks
        WHERE wave_id = NEW.wave_id
    ) WHERE wave_id = NEW.wave_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER task_progress_updated AFTER UPDATE OF progress_percentage ON tasks
    FOR EACH ROW EXECUTE FUNCTION calculate_wave_progress();
```

Similar trigger for program progress calculation.

---

## 7. MIGRATIONS

**Initial Schema**: Wave 0  
**Migration Strategy**: Alembic or Supabase migrations  
**Backward Compatibility**: All schema changes in future waves must be additive (no breaking changes)

---

*Generated for Issue #2 - Architecture & QA Design (Wave 0 Completion)*
