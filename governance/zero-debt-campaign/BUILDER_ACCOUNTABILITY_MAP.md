# ZWZDI Campaign - Builder Accountability Map

**Campaign ID**: ZWZDI-2026-001  
**Document**: Builder Accountability and Ownership Mapping  
**Version**: 1.0  
**Last Updated**: 2026-01-08

---

## Purpose

This document maps warnings and test debt to the original builders responsible for introducing them. **Builders fix their own debt.**

**Core Principle**: **Accountability drives learning and prevents recurrence.**

---

## Accountability Philosophy

### Why Builder Accountability Matters

1. **Learning**: Fixing your own mistakes reinforces correct behavior
2. **Ownership**: You own what you build, including its quality
3. **Prevention**: Understanding your patterns prevents future debt
4. **Fairness**: Those who created debt resolve it

### No Delegation

- Builders do NOT delegate cleanup to others
- Builders do NOT say "someone else will fix it"
- Builders do NOT pass debt to future developers

---

## Wave Ownership Mapping

### Wave 1.0: Initial UI and Dashboard

**Builder**: UI Builder  
**Original Work**: Initial UI components, dashboard, commissioning wizard  
**Test Directories**:
- `tests/wave1_ui/`
- `tests/test_commissioning_wizard_spec.py`
- `tests/test_commissioning_controller.py`
- Wave 1.0 related tests in `tests/wave1_0_qa_infrastructure/`

**Accountability Scope**:
- All warnings from UI component tests
- All warnings from dashboard tests
- All warnings from commissioning tests
- Test debt in UI-related tests
- Any RED tests in wave1_ui scope

**Estimated Debt**: TBD (to be inventoried during planning)

---

### Wave 1.0.1: Schema Foundation

**Builder**: Schema Builder  
**Original Work**: Database schema, models, migrations  
**Test Directories**:
- `tests/wave1_schema_foundation/`
- Schema-related tests in `tests/wave1_0_qa_infrastructure/`

**Accountability Scope**:
- All warnings from schema tests
- All warnings from model tests
- All warnings from migration tests (if applicable)
- Test debt in schema-related tests
- Any RED tests in schema foundation scope

**Estimated Debt**: TBD (to be inventoried during planning)

---

### Wave 1.0.2: Integration Subsystem

**Builder**: Integration Builder  
**Original Work**: Integration layer, escalation subsystem, event handling  
**Test Directories**:
- `tests/wave1_integration_builder/`
- Integration-related tests in `tests/wave1_0_qa_infrastructure/`

**Accountability Scope**:
- All warnings from integration tests
- All warnings from escalation subsystem tests
- Test debt in integration tests
- **Known Issues**:
  - AttributeError in escalation tests (7 tests)
  - `test_qa_097_create_escalation_with_5_elements`
  - `test_qa_098_route_escalation_to_johan`
  - `test_qa_099_present_escalation_in_ui`
  - `test_qa_100_handle_escalation_decision`
  - `test_qa_101_track_escalation_lifecycle`
  - `test_qa_102_escalation_priority_handling`
  - `test_qa_103_escalation_context_linking`

**Estimated Debt**: 7 failing tests + warnings TBD

---

### Wave 1.0.3: API Routes and Endpoints

**Builder**: API Builder  
**Original Work**: API implementation, routes, endpoints  
**Test Directories**:
- `tests/wave1_api_builder/`
- API-related tests in `tests/wave1_0_qa_infrastructure/`
- `tests/test_build_control_api.py`

**Accountability Scope**:
- All warnings from API tests
- All warnings from endpoint tests
- Test debt in API tests
- Any RED tests in API scope

**Estimated Debt**: TBD (to be inventoried during planning)

---

### Wave 1.0.4: Additional API Features

**Builder**: API Builder  
**Original Work**: Extended API functionality, additional endpoints  
**Test Directories**:
- Additional tests in `tests/wave1_api_builder/`
- Feature-specific tests in `tests/wave1_0_qa_infrastructure/`

**Accountability Scope**:
- All warnings from Wave 1.0.4 API work
- Test debt from Wave 1.0.4 scope
- Any RED tests from Wave 1.0.4 features

**Estimated Debt**: TBD (to be inventoried during planning)

---

### Foundation: Cross-Cutting Infrastructure

**Builders**: Schema Builder + API Builder (joint ownership)  
**Original Work**: Foundation layer spanning multiple waves, shared infrastructure  
**Test Directories**:
- `tests/test_startup_requirement_loader.py`
- `tests/test_startup_guard_spec.py`
- `tests/test_build_intervention.py`
- `tests/test_build_node_inspector.py`
- Cross-cutting tests in `tests/wave1_0_qa_infrastructure/`

**Accountability Scope**:
- Warnings from foundation/infrastructure tests
- **Known Issues**:
  - Missing startup requirements files (14 tests):
    - `lib/startup/startup-requirements.json` (not found)
    - `lib/startup/RequirementLoader.ts` (not found)
    - `lib/startup/README.md` (not found)
- Test debt in cross-cutting tests
- Shared infrastructure issues

**Estimated Debt**: 14 failing tests + warnings TBD

---

## Wave 2.0: Future Work (NOT in ZWZDI Scope)

**Status**: QA-to-Red (properly documented)  
**Test Directories**: `tests/wave2_0_qa_infrastructure/`

**Tests in Wave 2.0**:
- ~130 NotImplementedError tests
- Properly documented with QA IDs
- Assigned to specific builders
- NOT considered test debt

**Action**: NO ACTION REQUIRED during ZWZDI campaign

**Rationale**: These are intentional RED tests awaiting future implementation.

---

## Wave 0: Foundation Tests

**Status**: Excluded from ZWZDI cleanup (marked with `@pytest.mark.wave0`)  
**Test Directories**: `tests/wave0_minimum_red/`

**Action**: NO ACTION REQUIRED during ZWZDI campaign

**Rationale**: These are foundational tests outside current cleanup scope.

---

## Detailed Accountability Breakdown

### Current State Summary

| Wave | Builder | Test Dir | Passing | Failing | Warnings | Status |
|------|---------|----------|---------|---------|----------|--------|
| Wave 1.0 | UI Builder | wave1_ui/ | TBD | TBD | TBD | PENDING INVENTORY |
| Wave 1.0.1 | Schema Builder | wave1_schema_foundation/ | TBD | TBD | TBD | PENDING INVENTORY |
| Wave 1.0.2 | Integration Builder | wave1_integration_builder/ | TBD | 7 | TBD | PENDING INVENTORY |
| Wave 1.0.3 | API Builder | wave1_api_builder/ | TBD | TBD | TBD | PENDING INVENTORY |
| Wave 1.0.4 | API Builder | wave1_api_builder/ | TBD | TBD | TBD | PENDING INVENTORY |
| Foundation | Schema + API | various | TBD | 14 | TBD | PENDING INVENTORY |
| Wave 2.0 | QA Builder | wave2_0_qa_infrastructure/ | 0 | 130 | 0 | EXCLUDED (QA-to-Red) |

**Total Known Failing**: 21 tests (7 + 14)  
**Total Known Warnings**: 365 warnings (to be categorized by wave)

---

## Warning Categorization (To Be Completed)

During campaign planning, FM will categorize all 365 warnings by:

### Category 1: Deprecation Warnings
- Library deprecations
- Function deprecations
- API deprecations

**Action**: Update to new API or suppress with documentation

---

### Category 2: Import Warnings
- Unused imports
- Wildcard imports
- Circular imports

**Action**: Remove unused imports, make imports explicit

---

### Category 3: Type Warnings
- Type mismatches
- Missing type hints
- Type casting issues

**Action**: Fix type annotations, add missing hints

---

### Category 4: Test Framework Warnings
- Pytest warnings
- Fixture warnings
- Assertion warnings

**Action**: Update test patterns, fix assertions

---

### Category 5: Runtime Warnings
- Resource warnings (unclosed files)
- Performance warnings
- Security warnings

**Action**: Fix resource leaks, address performance issues

---

## Builder Assignment Process

### How Builders Are Assigned

1. **FM inventories warnings** by test file/directory
2. **FM maps test files** to original waves
3. **FM identifies builder** who implemented wave
4. **FM creates cleanup issue** for that builder
5. **Builder assigned** with wave-specific cleanup plan

### Assignment Criteria

**Builder is accountable for warnings if**:
- They implemented the wave containing the warning
- They wrote the test file containing the warning
- They introduced the code causing the warning

**Exceptions**:
- If original builder unavailable: CS2 designates replacement
- If responsibility disputed: FM determines based on git history, CS2 arbitrates if needed

---

## Cleanup Issue Assignment

For each wave, FM will create a builder cleanup issue containing:

1. **Wave identification**
2. **Builder assignment**
3. **Scope definition** (specific test files and warnings)
4. **Current state** (baseline warnings/failures)
5. **Target state** (zero warnings, zero failures)
6. **Completion criteria**
7. **Evidence requirements**
8. **Link to wave cleanup plan**

**Template**: See `ISSUE_TEMPLATE_BUILDER_CLEANUP.md`

---

## Accountability Enforcement

### During Cleanup

- Builder reads GOVERNANCE_LEARNING_BRIEF.md
- Builder reviews wave cleanup plan
- Builder eliminates ALL warnings in scope
- Builder resolves ALL test debt in scope
- Builder provides completion evidence
- FM verifies (PASS/FAIL)

### If Incomplete

- FM REJECTS cleanup attempt
- Builder must continue until 100% complete
- Next wave BLOCKED until current wave COMPLETE

### If Resistance

- Escalate to CS2
- CS2 enforces accountability mandate
- Builder participation non-optional (ZWZDI has CS2 authority)

---

## Success Metrics Per Builder

Each builder's success is measured by:

✅ **Zero warnings** in their wave scope  
✅ **Zero test debt** in their wave scope  
✅ **Completion evidence** provided  
✅ **FM verification PASS**  
✅ **Timeline adherence** (or justified delay with updated estimate)  

---

## Post-Campaign Learning

After campaign completion, each builder will:

1. **Reflect** on patterns in their warnings/debt
2. **Document** lessons learned
3. **Commit** to zero-tolerance going forward
4. **Apply** learning to future waves

**Goal**: Never repeat ZWZDI. Prevention > Cure.

---

## Accountability Summary

| Builder | Waves Owned | Estimated Cleanup Effort | Status |
|---------|-------------|-------------------------|--------|
| **UI Builder** | Wave 1.0 | 2 days | PENDING |
| **Schema Builder** | Wave 1.0.1, Foundation (joint) | 2 + 1 days | PENDING |
| **Integration Builder** | Wave 1.0.2 | 1 day | PENDING |
| **API Builder** | Wave 1.0.3, Wave 1.0.4, Foundation (joint) | 1 + 1 + 1 days | PENDING |
| **QA Builder** | Wave 2.0 | N/A | EXCLUDED |

**Total Builder Effort**: 10 days across 4 builders

---

## Next Steps

1. **FM**: Complete warning inventory by wave
2. **FM**: Update this document with detailed warning counts
3. **FM**: Create per-wave cleanup plans
4. **FM**: Create builder cleanup issues
5. **Builders**: Acknowledge accountability and prepare for cleanup

---

**Document Status**: IN PROGRESS (pending warning inventory)  
**Next Update**: After warning categorization complete  
**Owner**: Foreman (FM)
