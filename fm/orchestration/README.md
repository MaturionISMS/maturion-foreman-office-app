# FM Orchestration — Build Coordination & Execution

**Status**: Scaffolding Complete (Empty)  
**Phase**: 3A — Memory Scaffolding  
**Last Updated**: 2025-12-23

---

## Purpose

This directory manages **build orchestration and coordination** for Maturion Foreman (FM).

This is where FM coordinates:
- Wave-based execution plans
- Builder agent task assignments
- QA oversight and validation
- Cross-module dependencies
- Build sequencing and parallelization

---

## Orchestration Structure

```
orchestration/
├── README.md                  # This file
├── wave-plans/               # Wave-based execution plans
├── builder-assignments/      # Builder agent task assignments
└── qa-oversight/             # QA oversight and validation tracking
```

---

## Orchestration Components

### Wave Plans (`wave-plans/`)
**Purpose**: Define and track wave-based build execution

**Contents** (when populated):
- Wave definitions and scope
- Module dependencies per wave
- Builder allocation per wave
- Wave success criteria
- Wave validation plans

**Wave Model**:
- Each wave is a logical grouping of related modules
- Modules within a wave can build in parallel where dependencies allow
- Wave completion requires all modules to reach green
- Wave validation ensures no cross-module regressions

**Relationship to One-Time Build Law**:
- Waves enforce dependency ordering (build correctness)
- Wave validation prevents regressions (zero regression)
- Wave plans are pre-validated (first-time correctness)

---

### Builder Assignments (`builder-assignments/`)
**Purpose**: Track which builder agents are working on what

**Contents** (when populated):
- Current builder assignments
- Builder task queues
- Builder capacity and availability
- Task completion records
- Builder handover documentation

**Builder Agents**:
- `ui-builder` — UI components and frontend
- `api-builder` — API routes and backend logic
- `schema-builder` — Database schema and models
- `integration-builder` — Inter-module and external integrations
- `qa-builder` — Tests, coverage, and QA-of-QA

**Assignment Principles**:
- One builder per module per phase (clear ownership)
- Builders collaborate via handover (no simultaneous edits)
- QA builder validates after implementation builders complete
- Foreman coordinates, builders execute

---

### QA Oversight (`qa-oversight/`)
**Purpose**: Track QA validation and oversight across builds

**Contents** (when populated):
- QA validation checkpoints
- Coverage reports per module
- QA-of-QA results
- Regression detection records
- Quality gate status

**QA Oversight Model**:
- FM ensures QA is performed, not performing QA itself
- Builder agents produce QA artifacts
- QA builder validates those artifacts
- FM monitors that QA process is followed
- QA oversight ≠ QA execution

**Relationship to QA Governance**:
- FM enforces that builders follow QA governance
- FM validates that minimum coverage is met
- FM does not define QA standards (that's governance)
- FM does not execute module tests (that's builders)

---

## Orchestration Principles

### 1. Wave-Based Execution
**Concept**: Build in logical waves, validate each wave before proceeding

**Benefits**:
- Clear dependency management
- Parallelization where possible
- Isolated regression detection
- Incremental validation

**Constraints**:
- Wave N cannot start until Wave N-1 is green
- All modules in a wave must complete before wave closes
- Wave validation is mandatory

---

### 2. Builder Coordination
**Concept**: FM coordinates builders, builders execute tasks

**FM Responsibilities**:
- Assign tasks to appropriate builders
- Ensure builder handover is clean
- Monitor builder progress
- Detect builder conflicts or blocks

**Builder Responsibilities**:
- Execute assigned tasks to green
- Produce QA artifacts
- Document decisions
- Hand over cleanly to next builder

**Anti-Pattern**: FM becoming a builder itself

---

### 3. QA Oversight (Not Execution)
**Concept**: FM monitors that QA happens, not doing QA itself

**FM QA Oversight**:
- Verify QA artifacts exist
- Check coverage meets minimums
- Validate QA-of-QA is performed
- Track regressions and fixes

**FM Does NOT**:
- Execute module unit tests
- Write module test cases
- Debug module test failures
- Perform module QA

**Boundary**: FM tests orchestration logic, not module implementation

---

### 4. Dependency Awareness
**Concept**: FM understands module dependencies and enforces build order

**Dependency Types**:
- Schema dependencies (e.g., User → Role)
- API dependencies (e.g., Integration → API)
- UI dependencies (e.g., Dashboard → Components)

**Enforcement**:
- Waves are ordered by dependency layers
- Intra-wave parallelization respects dependencies
- Circular dependencies are prohibited

---

## Current State

**Phase**: 3A — Scaffolding Complete  
**Status**: Empty and ready for orchestration  
**Next Phase**: Wave 0 execution will populate orchestration state

All subdirectories exist but contain no orchestration plans yet.

---

## Orchestration vs. Governance

### FM Orchestration (Here)
- Coordinates builder execution
- Tracks task assignments
- Monitors QA process
- Manages wave execution

### Governance (Canonical)
- Defines what must be built (architecture)
- Defines how to validate (QA standards)
- Defines success criteria (compliance)
- Defines constraints (rules and principles)

**Relationship**: FM orchestration executes governance-defined requirements

---

## Orchestration Authority

FM orchestration:
- Decides task order (within governance constraints)
- Assigns tasks to builders (following capability map)
- Validates execution completeness (not correctness)
- Coordinates handovers (following protocols)

FM orchestration does NOT:
- Define what "correct" means (that's governance)
- Override builder QA results (that's governance)
- Skip QA requirements (that's governance)
- Modify architecture standards (that's governance)

**Authority**: FM has orchestration authority, not governance authority

---

## References

- **Build Philosophy**: `/BUILD_PHILOSOPHY.md`
- **One-Time Build Law**: `/BUILD_PHILOSOPHY.md` (Principle 1)
- **FM Roles & Duties**: `/foreman/roles-and-duties.md`
- **Builder Specifications**: `/foreman/builder/`
- **QA Governance**: `/governance/policies/qa-governance.md`
- **Builder Collaboration Rules**: `/foreman/builder/builder-collaboration-rules.md`

---

*FM Orchestration — Coordinating Build Execution with Precision*
