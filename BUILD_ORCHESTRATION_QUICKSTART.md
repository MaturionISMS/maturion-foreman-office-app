# Build Orchestration System - Quick Start Guide

**Version**: 1.0  
**Last Updated**: 2025-12-04  
**Status**: Operational (Validated in Build Wave 0)

---

## Overview

The Build Orchestration System coordinates the construction of ISMS modules through automated planning, task generation, and cycle summary. It was successfully validated in Build Wave 0 for the PIT module.

---

## Quick Start

### Execute a Build Wave

```bash
# Step 1: Plan the build
python3 plan-build.py <MODULE_NAME>

# Step 2: Generate tasks
python3 create-build-tasks.py

# Step 3: Summarize results
python3 summarize-build-cycle.py
```

### Example: PIT Module

```bash
# Full Build Wave 0 execution
python3 plan-build.py PIT
python3 create-build-tasks.py
python3 summarize-build-cycle.py
```

---

## The Three Scripts

### 1. plan-build.py

**Purpose**: Analyzes module readiness and generates a build plan

**Inputs**:
- Module readiness reports (`MODULE_READINESS_REPORTS/`)
- Standardisation results (`standardisation_results.json`)
- Builder manifest (`foreman/builder-manifest.json`)
- Builder capabilities (`foreman/builder/builder-capability-map.json`)

**Outputs**:
- `build-plan.json` - Complete build plan with phases and readiness assessment

**Usage**:
```bash
python3 plan-build.py <MODULE_NAME>
# Example: python3 plan-build.py PIT
```

**What it does**:
1. Loads module readiness report
2. Identifies missing architecture components
3. Assesses build readiness
4. Creates 5-phase build plan
5. Assigns builders to phases
6. Identifies blockers

### 2. create-build-tasks.py

**Purpose**: Generates detailed tasks for each builder agent

**Inputs**:
- `build-plan.json` (from plan-build.py)

**Outputs**:
- `build-tasks.json` - Detailed task definitions for all builders

**Usage**:
```bash
python3 create-build-tasks.py
# Or with custom plan:
python3 create-build-tasks.py --plan custom-build-plan.json
```

**What it does**:
1. Loads build plan
2. Generates tasks for each phase
3. Creates task IDs
4. Defines acceptance criteria
5. Sets QA gates
6. Tracks dependencies
7. Adds governance checks

### 3. summarize-build-cycle.py

**Purpose**: Analyzes the build cycle and generates summary with lessons learned

**Inputs**:
- `build-plan.json`
- `build-tasks.json`
- `build-status.json` (optional)

**Outputs**:
- `BUILD_ORCHESTRATION_SUMMARY.md` - Human-readable summary
- `build-cycle-summary.json` - Machine-readable summary

**Usage**:
```bash
python3 summarize-build-cycle.py
# Or with custom files:
python3 summarize-build-cycle.py --plan custom-plan.json --tasks custom-tasks.json
```

**What it does**:
1. Analyzes what worked
2. Identifies failures
3. Extracts lessons learned
4. Generates recommendations
5. Provides Go/No-Go assessment

---

## Build Phases

Every build follows these 5 phases:

```
Phase 1: Schema Foundation (schema-builder)
  ↓
Phase 2: API Implementation (api-builder)
  ↓
Phase 3: Integration Layer (integration-builder) ←┐
  ↓                                                 ├→ Parallel
Phase 4: UI Components (ui-builder) ←──────────────┘
  ↓
Phase 5: QA & Validation (qa-builder)
```

**Why this order?**
- Schema is the foundation - nothing works without it
- API needs models from schema
- Integration and UI both depend on API, can run in parallel
- QA validates everything after implementation

---

## Output Files

### Core Build Artifacts

| File | Description | Format | Size |
|------|-------------|--------|------|
| `build-plan.json` | Build plan with phases and readiness | JSON | ~3 KB |
| `build-tasks.json` | Detailed tasks for builders | JSON | ~14 KB |
| `build-status.json` | Status snapshot | JSON | ~2 KB |
| `build-cycle-summary.json` | Machine-readable summary | JSON | ~5 KB |

### Documentation

| File | Description | Format | Size |
|------|-------------|--------|------|
| `BUILD_ORCHESTRATION_READINESS.md` | Readiness assessment | Markdown | ~13 KB |
| `BUILD_ORCHESTRATION_SUMMARY.md` | Build cycle summary | Markdown | Varies |
| `BUILD_WAVE_0_FINAL_VALIDATION.md` | Validation report | Markdown | ~14 KB |

---

## Module Readiness Requirements

Before running a build:

### Minimum Requirements
- [ ] Module readiness report exists in `MODULE_READINESS_REPORTS/`
- [ ] Module architecture completeness >= 80%
- [ ] Module status is `READY` (not `NOT_READY`)
- [ ] Critical components exist:
  - TRUE_NORTH
  - INTEGRATION_SPEC
  - DATABASE_SCHEMA
  - EDGE_FUNCTIONS (if backend module)

### Recommended
- [ ] Architecture completeness >= 90%
- [ ] All conditional components exist
- [ ] QA implementation plan complete
- [ ] Integration specifications validated

### Example: PIT Module in Build Wave 0
- Completeness: 15.4% ❌ (requires 80%)
- Status: NOT_READY ❌
- Missing: 11 of 13 components ❌
- **Result**: Build blocked (correct behavior)

---

## Build Tasks Structure

Each task includes:

```json
{
  "task_id": "PIT-SCHEMA-BUILDER-P1-T001-SCHEMA",
  "title": "PIT - Database Schema Design and Implementation",
  "builder": "schema-builder",
  "phase": 1,
  "priority": "HIGH",
  "status": "NOT_STARTED",
  "description": "Design and implement the complete database schema...",
  "acceptance_criteria": [
    "All tables and relationships defined",
    "Schema follows naming conventions",
    "..."
  ],
  "dependencies": [],
  "deliverables": [
    "Database schema DDL",
    "Schema diagram",
    "..."
  ],
  "qa_gates": [
    "Schema validation passes",
    "No circular dependencies",
    "..."
  ],
  "governance_checks": [
    "Must not access other module schemas",
    "Must respect privacy guardrails",
    "..."
  ],
  "estimated_effort": "MEDIUM"
}
```

---

## Builder Assignment

Tasks are distributed across 5 builder agents:

| Builder | Responsibilities | Typical Tasks |
|---------|------------------|---------------|
| `schema-builder` | Database schema, models, migrations | 3 per module |
| `api-builder` | API routes, edge functions, logic | 3 per module |
| `integration-builder` | Inter-module integrations, events | 2 per module |
| `ui-builder` | UI components, layouts, pages | 3 per module |
| `qa-builder` | E2E tests, QA-of-QA, compliance | 3 per module |

**Total**: ~14 tasks per module

---

## Validation Checklist

Before considering a build wave complete:

### Scripts
- [ ] plan-build.py runs without errors
- [ ] create-build-tasks.py runs without errors
- [ ] summarize-build-cycle.py runs without errors

### JSON Files
- [ ] All JSON files valid (use `python3 -m json.tool <file>`)
- [ ] build-plan.json complete
- [ ] build-tasks.json complete
- [ ] build-status.json complete

### Governance
- [ ] No builder boundary violations
- [ ] All tasks within builder capabilities
- [ ] Governance checks included where needed
- [ ] Privacy guardrails enforced

### Dependencies
- [ ] Dependencies properly tracked
- [ ] No circular dependencies
- [ ] Dependency chain valid
- [ ] No orphaned tasks

### QA
- [ ] All tasks have acceptance criteria
- [ ] All tasks have QA gates
- [ ] Coverage requirements specified
- [ ] QA-of-QA included

---

## Troubleshooting

### "Module readiness report not found"

**Problem**: Module readiness report doesn't exist

**Solution**:
```bash
# Run standardisation first
python3 standardise-architecture.py
# This generates readiness reports for all modules
```

### "Module status is NOT_READY"

**Problem**: Module architecture incomplete

**Solution**:
1. Check `MODULE_READINESS_REPORTS/<MODULE>_READINESS_REPORT.md`
2. Identify missing components
3. Complete architecture components
4. Re-run standardisation
5. Try build planning again

### "Build plan not found"

**Problem**: Trying to generate tasks before planning

**Solution**:
```bash
# Always run plan-build.py first
python3 plan-build.py <MODULE_NAME>
# Then generate tasks
python3 create-build-tasks.py
```

---

## Integration Points

### Change Management
- Architecture gaps trigger change records
- QA gaps trigger change records
- Compliance violations trigger change records
- See: `foreman/change-management/`

### ai-memory
- Historical issues captured
- Reasoning patterns recorded
- Upgrade insights documented
- See: `foreman/ai-memory/`

### Runtime System
- Runtime insights inform builds
- Build outputs feed runtime
- Continuous feedback loop
- See: `foreman/runtime/`

---

## Build Wave Progression

### Build Wave 0 (Completed)
- **Purpose**: Validate orchestration
- **Approach**: Dry-run, no code generation
- **Module**: PIT
- **Result**: ✅ Orchestration validated

### Build Wave 1 (Next)
- **Purpose**: First real module build
- **Approach**: Full code generation
- **Prerequisites**:
  - Complete PIT architecture (11 components)
  - Set up test environment
  - Configure CI/CD pipeline
  - Achieve 80%+ completeness

### Build Wave 2+
- **Purpose**: Iterative module builds
- **Approach**: Apply lessons from Wave 1
- **Focus**: Optimization and refinement

---

## Best Practices

1. **Always run scripts in order**: plan → tasks → summarize
2. **Validate JSON after generation**: Use `python3 -m json.tool`
3. **Review readiness reports first**: Don't plan unready modules
4. **Use Build Wave 0 approach**: For new features or major changes
5. **Check governance boundaries**: Ensure builders stay in lanes
6. **Track lessons learned**: Update ai-memory after each wave
7. **Create change records**: For all gaps and issues found

---

## Statistics (Build Wave 0)

- **Scripts Created**: 3
- **Build Phases**: 5
- **Tasks Generated**: 14
- **Builders Involved**: 5
- **Dependencies Tracked**: 13
- **QA Gates Defined**: 14
- **JSON Files**: 7
- **Markdown Reports**: 6
- **Validation Passes**: 100%
- **Governance Violations**: 0
- **Privacy Violations**: 0

---

## Support & Documentation

- **Full Readiness Report**: `BUILD_ORCHESTRATION_READINESS.md`
- **Build Summary**: `BUILD_ORCHESTRATION_SUMMARY.md`
- **Final Validation**: `BUILD_WAVE_0_FINAL_VALIDATION.md`
- **Change Records**: `foreman/change-management/CR-BW0-001-*.json`
- **ai-memory**: `foreman/ai-memory/build-wave-0-*.{json,md}`

---

## Contact

For questions or issues:
- **Foreman**: Maturion Foreman (AI Agent)
- **Human Review**: Johan
- **Repository**: MaturionISMS/maturion-ai-foreman

---

*Last validated: Build Wave 0 - 2025-12-04*  
*Status: Operational and ready for production use*
