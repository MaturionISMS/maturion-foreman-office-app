# QA-to-Red Suite Creation — Wave 1.0 Phase 2 (WAVE_1.0_TASK_QA_RED_01)

## Builder Assignment (Building on Wave 0.1)

This issue is created **on behalf of the Foreman (FM)** under bootstrap proxy authority.

**Builder Status:** qa-builder is **already recruited, validated, and ready** per Wave 0.1 completion.

**Wave 0.1 Evidence:**
- Builder recruitment: ✅ COMPLETE (CS2 approved)
- Builder validation: ✅ 19/19 checks passed
- Canonical artifact: `foreman/builder-registry-report.md`
- Readiness certification: `WAVE_0.1_READINESS_CERTIFICATION.md`

**Canonical Continuity:** This task builds directly on Wave 0.1 builder recruitment. No additional appointment or recruitment is required.

---

## Task Overview

**Task ID:** WAVE_1.0_TASK_QA_RED_01  
**Phase:** Phase 2 (QA-to-Red Suite Creation)  
**Builder:** qa-builder (recruited and validated in Wave 0.1)  
**Authority:** BUILD_PHILOSOPHY.md Section III Phase 2  
**Architecture Reference:** docs/architecture/TRUE_NORTH_FM_ARCHITECTURE.md v1.0 (FROZEN and CANONICAL)  
**Assigned At:** 2025-12-30 14:13 UTC (16:13 SAST)  
**Duration Estimate:** 3-5 days

---

## Authority & Governance

### BUILD_PHILOSOPHY.md Section III Phase 2 Requirement

> **"Before any code is written, the QA suite must exist. Before any code is written, the QA suite must have been executed. Before any code is written, the QA status must be RED."**

This task implements Phase 2 of the canonical build pipeline:
1. ✅ **ARCHITECTURE (Phase 1)** — COMPLETE & FROZEN
2. ⏳ **RED QA (Phase 2)** — THIS TASK
3. ⏸️ **BUILD TO GREEN (Phase 3)** — Blocked until Phase 2 complete
4. ⏸️ **VALIDATION (Phase 4)** — Blocked until Phase 3 complete
5. ⏸️ **MERGE (Phase 5)** — Blocked until Phase 4 complete

### Canonical Architecture (FROZEN)

**Document:** docs/architecture/TRUE_NORTH_FM_ARCHITECTURE.md v1.0  
**Status:** FROZEN and CANONICAL (CS2 approved 2025-12-30)  
**Size:** 663 lines  
**Components:** 53+ canonical components  
**Change Control:** No architectural changes without explicit governance authorization

**All QA-to-Red tests MUST validate the frozen architecture.**

---

## Mandatory Deliverables

### 1. DP-RED Registry

**File:** `foreman/qa/dp-red-registry.json`

**Purpose:** Register all RED (failing) tests with component mappings and green criteria.

**Format:** Custom DP-RED JSON format per `foreman/qa/dp-red-registry-spec.md`

**Contents Required:**
- Test ID (unique identifier)
- Component reference (architecture component being tested)
- Test category (foundation, UI, API, integration, governance, E2E)
- Test description (what is being validated)
- RED reason (why test currently fails)
- Green criteria (what must be implemented for test to pass)
- Build-to-green task dependency (which task will make this test GREEN)

**Example Entry:**
```json
{
  "testId": "DPRED-001",
  "component": "Foreman Dashboard",
  "category": "UI Component",
  "description": "Foreman Dashboard renders without errors",
  "redReason": "Dashboard component not yet implemented",
  "greenCriteria": "Dashboard component implemented per architecture Section 7.1",
  "buildToGreenTask": "TBD (assigned by FM in Phase 3)"
}
```

### 2. Test Suite (Comprehensive Coverage)

**Test Files Required:**
- Unit tests (Jest): Component-level validation
- Integration tests (Jest + React Testing Library): Cross-component validation
- E2E tests (Playwright): User workflow validation

**Test Framework Stack:**
- **Unit Testing:** Jest
- **Component Testing:** React Testing Library
- **E2E Testing:** Playwright
- **Coverage:** Jest coverage reports
- **Language:** TypeScript

**All tests MUST:**
- Be written BEFORE implementation exists
- Be intentionally RED (failing)
- Have clear, descriptive names
- Have explicit assertions
- Be independent (no inter-test dependencies)
- Be deterministic (consistent results)
- Be fast (unit <1s, integration <5s, E2E <30s)

### 3. Test Coverage Map

**File:** `foreman/qa/test-coverage-map.md`

**Purpose:** Map all architecture components to tests that validate them.

**Required Coverage:** ≥95% of frozen architecture (53+ components)

**Format:**
```markdown
# Test Coverage Map — Wave 1.0 Phase 2

## Architecture Component → Test Mapping

### Component: Foreman Dashboard (Architecture Section 7.1)
- **Tests:** DPRED-001, DPRED-002, DPRED-003, ...
- **Coverage:** 100% (all specified behaviors tested)

### Component: Builder Registry API (Architecture Section 8.1)
- **Tests:** DPRED-020, DPRED-021, DPRED-022, ...
- **Coverage:** 100% (all endpoints tested)

...

## Coverage Summary
- **Total Components:** 53+
- **Components Tested:** XX
- **Coverage Percentage:** ≥95%
- **Untested Components:** [list if any]
```

### 4. Red Gate Definitions

**File:** `foreman/qa/red-gate-definitions.md`

**Purpose:** Define clear criteria for when each test must pass.

**Contents:**
- Test execution order (dependencies between tests)
- Build-to-green task dependencies (which tasks make which tests GREEN)
- Phase 3 sequencing (task order for build-to-green)
- Pass criteria for each test category

### 5. QA-to-Red Validation Report

**File:** `WAVE_1.0_QA_TO_RED_VALIDATION_REPORT.md`

**Purpose:** Confirm all tests are RED and quality requirements met.

**Contents Required:**
- Test execution summary (total tests, all RED status confirmed)
- Zero test debt verification (no .skip(), .todo(), or stubs)
- Coverage validation (≥95% architecture coverage confirmed)
- DP-RED registry validation (all tests registered)
- Quality checklist (test quality standards met)
- Evidence chain (traceable to frozen architecture)

---

## Test Categories & Requirements

### Category 1: Foundation Tests (~15 tests)

**Purpose:** Validate project structure and build system setup.

**Test Coverage Required:**
- Project directory structure exists and matches architecture
- TypeScript configuration valid and compiles
- ESLint and Prettier configured correctly
- Package.json has correct dependencies
- Git hooks functional (pre-commit, pre-push)
- CI pipeline configured (GitHub Actions)
- Build system functional (Next.js build)
- Development server starts correctly
- Production build succeeds
- Environment variable handling
- Error boundary configuration
- Logging infrastructure
- Performance monitoring hooks
- Security headers configured
- CORS configuration

**All tests must be RED** (infrastructure not yet implemented).

### Category 2: UI Component Tests (~20 tests)

**Purpose:** Validate UI components from frozen architecture.

**Test Coverage Required:**
- Theme provider functional (Tailwind + shadcn/ui)
- Navigation component renders correctly
- Authentication context exists and functional
- Shared UI components render (Button, Card, Input, etc.)
- Layout components functional
- Foreman Dashboard component exists
- Task Assignment Panel component exists
- Builder Status Display component exists
- Evidence Viewer component exists
- QA Results Panel component exists
- Architecture Reference Panel component exists
- Build Wave Progress Tracker component exists
- Governance Compliance Dashboard component exists
- DAI Generator Interface component exists
- Task History Log component exists
- Responsive behavior validated
- Accessibility standards met
- Theme switching functional
- Component prop validation
- Component state management

**All tests must be RED** (UI components not yet implemented).

### Category 3: API & Backend Tests (~25 tests)

**Purpose:** Validate API endpoints and backend functionality.

**Test Coverage Required:**
- Builder registry API endpoints exist and respond
- PostgreSQL database schema exists
- Prisma client configured and functional
- Builder CRUD operations (Create, Read, Update, Delete)
- Builder status tracking functional
- Builder task assignment API functional
- Builder validation enforcement
- API authentication middleware functional
- API authorization checks enforced
- API input validation working
- API error handling correct
- API response format consistent
- Database migrations functional
- Database connection pooling
- Transaction handling correct
- Query performance acceptable
- Data sanitization enforced
- SQL injection prevention
- Rate limiting configured
- API versioning handled
- Health check endpoint functional
- Metrics endpoint functional
- Logging middleware functional
- Request ID tracking
- API documentation generated

**All tests must be RED** (API and backend not yet implemented).

### Category 4: Builder Registry Tests (~12 tests)

**Purpose:** Validate builder registry service functionality.

**Test Coverage Required:**
- Builder registration process functional
- Builder status updates correctly
- Builder task queue operational
- Builder assignment validation enforced
- Builder capability checks functional
- Builder heartbeat tracking
- Builder failure detection
- Builder recovery handling
- Builder metrics collection
- Builder audit logging
- Builder permission enforcement
- Builder state persistence

**All tests must be RED** (builder registry service not yet implemented).

### Category 5: Integration Tests (~18 tests)

**Purpose:** Validate cross-component integration.

**Test Coverage Required:**
- UI → API integration functional
- API → Database integration functional
- Authentication flow end-to-end
- Authorization flow end-to-end
- Evidence storage and retrieval flow
- Task assignment flow complete
- Builder status update flow
- Dashboard data loading flow
- Navigation state management
- Form submission flows
- File upload flows
- Real-time updates functional
- Error propagation correct
- Loading state handling
- Offline behavior handling
- Cache invalidation correct
- Optimistic updates working
- Rollback handling functional

**All tests must be RED** (integrations not yet implemented).

### Category 6: Governance Tests (~10 tests)

**Purpose:** Validate governance and compliance functionality.

**Test Coverage Required:**
- Governance dashboard displays compliance status
- Compliance monitoring API functional
- Authority boundary checks enforced
- DAI generator produces valid DAIs
- DAI validation enforced
- DAI submission workflow functional
- Audit logging comprehensive
- Evidence chain traceable
- Governance rule enforcement
- Policy violation detection

**All tests must be RED** (governance features not yet implemented).

### Category 7: E2E Scenarios (~12 tests)

**Purpose:** Validate complete user workflows.

**Test Coverage Required:**
- FM can view dashboard (complete flow)
- FM can assign task to builder (complete flow)
- FM can view evidence artifacts (complete flow)
- FM can generate DAI (complete flow)
- FM can track wave progress (complete flow)
- FM can monitor QA status (complete flow)
- FM can view builder status (complete flow)
- FM can manage builder registry (complete flow)
- FM can review governance compliance (complete flow)
- FM can access architecture reference (complete flow)
- FM can view task history (complete flow)
- FM can perform all workflows without errors (complete flow)

**All tests must be RED** (end-to-end functionality not yet implemented).

---

## Acceptance Criteria

**This task is COMPLETE when all 10 criteria are satisfied:**

1. ✅ **All tests compiled and executable**
   - Test suite compiles without TypeScript errors
   - Test files are executable via test runner
   - No syntax or import errors

2. ✅ **All tests registered in DP-RED registry**
   - `foreman/qa/dp-red-registry.json` exists
   - All ~112 tests registered with metadata
   - Registry format matches `foreman/qa/dp-red-registry-spec.md`

3. ✅ **All tests executed and status is RED**
   - Test suite executed successfully
   - 100% of tests failing (RED status)
   - Test execution logs preserved

4. ✅ **Test coverage ≥95% of frozen architecture**
   - All 53+ architecture components tested
   - Coverage map generated and validated
   - Coverage report shows ≥95%

5. ✅ **Zero test debt**
   - No `.skip()` in test files
   - No `.todo()` in test files
   - No stub implementations
   - No commented-out tests

6. ✅ **Test coverage map generated and validated**
   - `foreman/qa/test-coverage-map.md` exists
   - All architecture components mapped to tests
   - Coverage gaps identified (if any)

7. ✅ **Red gate definitions documented**
   - `foreman/qa/red-gate-definitions.md` exists
   - Test execution order defined
   - Build-to-green dependencies specified

8. ✅ **QA-to-Red validation report complete**
   - `WAVE_1.0_QA_TO_RED_VALIDATION_REPORT.md` exists
   - All validation checks performed
   - Report signed by qa-builder

9. ✅ **FM validates suite completeness**
   - FM reviews all deliverables
   - FM confirms acceptance criteria met
   - FM approves QA-to-Red suite

10. ✅ **CS2 approves QA-to-Red suite**
    - CS2 reviews QA-to-Red validation report
    - CS2 confirms governance compliance
    - CS2 authorizes FM to proceed to Phase 3

---

## Forbidden Actions

**qa-builder MUST NOT:**

1. ❌ **Implement any production code**
   - Only test code is authorized
   - No production implementation before Phase 3

2. ❌ **Make tests pass (all tests must be RED)**
   - Tests must remain failing
   - RED status is required acceptance criterion

3. ❌ **Skip or stub tests (zero test debt required)**
   - No `.skip()`, `.todo()`, or stub implementations
   - All tests must be complete and executable

4. ❌ **Modify frozen architecture**
   - Architecture is FROZEN and CANONICAL
   - No changes without governance authorization

5. ❌ **Create build-to-green tasks**
   - Task creation is FM authority only
   - Phase 3 planning occurs after Phase 2 approval

6. ❌ **Perform GitHub platform operations**
   - No PR creation or merging
   - CS2 acts as execution proxy

7. ❌ **Deviate from frozen architecture**
   - All tests must validate frozen architecture
   - No testing of non-architectural features

---

## Test Quality Standards

**All tests MUST meet these quality standards:**

### 1. Clear Test Names
- Test names describe what is being tested
- Use descriptive, readable names
- Follow convention: `describe('Component', () => { it('should do X when Y', ...) })`

### 2. Explicit Assertions
- No ambiguous expectations
- Clear pass/fail criteria
- Use specific matchers (e.g., `toEqual`, `toHaveBeenCalledWith`)

### 3. Independent Tests
- No inter-test dependencies
- Tests can run in any order
- No shared mutable state between tests

### 4. Deterministic Tests
- Consistent results every execution
- No flaky tests
- No reliance on timing or external state

### 5. Fast Tests
- Unit tests: <1 second each
- Integration tests: <5 seconds each
- E2E tests: <30 seconds each

### 6. Proper Setup & Teardown
- Use `beforeEach`/`afterEach` appropriately
- Clean up after tests
- Reset mocks and spies

### 7. Good Error Messages
- Assertions have clear failure messages
- Easy to diagnose failures
- Include relevant context

---

## Evidence & Handover Requirements

**Upon completion, qa-builder MUST:**

1. **Notify FM formally**
   - Post completion notification in this issue
   - Include summary of deliverables
   - Confirm all acceptance criteria met

2. **Ensure all deliverables committed**
   - All files committed to repository
   - Files accessible in expected locations
   - No uncommitted changes

3. **Maintain evidence chain**
   - All tests traceable to architecture components
   - Test IDs in DP-RED registry match test files
   - Coverage map matches reality

4. **Preserve test execution logs**
   - Test execution output saved
   - RED status confirmed for all tests
   - No errors during test execution

5. **Generate coverage reports**
   - Jest coverage report generated
   - Coverage meets ≥95% threshold
   - Coverage gaps documented

6. **Validate DP-RED registry**
   - Registry format correct
   - All tests registered
   - Component mappings accurate

---

## Governance Framework References

### Primary Authority

**BUILD_PHILOSOPHY.md Section III Phase 2**
- Canonical build pipeline authority
- QA-to-Red requirements
- Phase sequencing rules

### Supporting Specifications

**foreman/qa/dp-red-registry-spec.md**
- DP-RED registry format specification
- Registration requirements
- Metadata standards

**Platform Readiness Canon (G-PLAT-READY-01)**
- Platform readiness requirements
- Quality gates
- Assurance standards

**FM Agent Contract**
- Authority boundaries
- Builder responsibilities
- Execution constraints

### Architecture Reference

**docs/architecture/TRUE_NORTH_FM_ARCHITECTURE.md v1.0**
- FROZEN and CANONICAL architecture
- 53+ components to test
- Complete architecture specification

**WAVE_1.0_ARCHITECTURE_COMPLETENESS_REPORT.md**
- Architecture validation report
- Component inventory
- Directory structure

---

## Execution Protocol

**Task execution follows this sequence:**

1. **Builder Appointment (Governance-Scoped)**
   - Issue reviewed and accepted
   - Builder agent formally bound
   - Appointment recorded in this issue
   - **Execution authorized**

2. **Architecture Study**
   - Review TRUE_NORTH_FM_ARCHITECTURE.md v1.0
   - Understand all 53+ components
   - Map components to test categories

3. **Test Planning**
   - Plan test structure
   - Define test organization
   - Create test file structure

4. **Test Implementation**
   - Write all ~112 tests
   - Ensure all tests are RED
   - Maintain zero test debt

5. **DP-RED Registry Creation**
   - Register all tests
   - Map tests to components
   - Define green criteria

6. **Coverage Validation**
   - Generate coverage reports
   - Validate ≥95% coverage
   - Create coverage map

7. **Documentation**
   - Create red gate definitions
   - Generate QA-to-Red validation report
   - Document evidence chain

8. **FM Validation**
   - Notify FM of completion
   - FM validates deliverables
   - FM approves or requests changes

9. **CS2 Approval**
   - FM generates DAI for CS2
   - CS2 creates PR (as proxy)
   - CS2 reviews and approves
   - CS2 merges PR (as proxy)

10. **Phase 3 Authorization**
    - CS2 authorizes FM to proceed to Phase 3
    - FM begins build-to-green planning
    - Wave 1.0 continues

---

## Duration Estimate

**Estimated Time:** 3-5 days

**Breakdown:**
- **Day 1:** Architecture study + foundation tests (~15 tests) + UI component tests (~20 tests)
- **Day 2:** API & backend tests (~25 tests) + builder registry tests (~12 tests)
- **Day 3:** Integration tests (~18 tests) + governance tests (~10 tests)
- **Day 4:** E2E scenarios (~12 tests) + DP-RED registry compilation
- **Day 5:** Coverage validation + documentation + validation report

**Factors affecting duration:**
- Test complexity
- Architecture comprehension time
- DP-RED registry compilation time
- Coverage validation iterations
- FM/CS2 review cycles

---

## Technical Requirements Summary

**Test Framework Stack:**
- Jest (unit testing)
- React Testing Library (component testing)
- Playwright (E2E testing)
- TypeScript (test language)
- Jest coverage (coverage reporting)

**Test Organization:**
- `__tests__/` directories co-located with code
- `tests/integration/` for integration tests
- `tests/e2e/` for E2E tests
- Clear naming conventions

**Configuration Files:**
- `jest.config.js` (Jest configuration)
- `playwright.config.ts` (Playwright configuration)
- `.eslintrc.js` (test linting)
- `tsconfig.test.json` (test TypeScript config)

**Quality Tools:**
- ESLint (test code linting)
- Prettier (test code formatting)
- TypeScript (test type checking)
- Jest coverage (coverage reporting)

---

## Questions or Clarifications

If any aspect of this specification is unclear, **STOP and escalate to FM immediately.**

Do not proceed with uncertain requirements.

FM will clarify any ambiguity before execution continues.

---

## Metadata

**Task ID:** WAVE_1.0_TASK_QA_RED_01  
**Phase:** Phase 2 (QA-to-Red Suite Creation)  
**Builder:** qa-builder (pending formal appointment)  
**Assigned At:** 2025-12-30 13:42 UTC (15:42 SAST)  
**Duration Estimate:** 3-5 days  
**Authority:** BUILD_PHILOSOPHY.md Section III Phase 2  
**Architecture:** TRUE_NORTH_FM_ARCHITECTURE.md v1.0 (FROZEN)  
**Specification Version:** 1.0  
**Generated By:** Maturion Foreman (FM)  
**Generated At:** 2025-12-30 13:50 UTC (15:50 SAST)

---

**Maturion Foreman**  
Planning and Sequencing Authority  
Wave 1.0 Phase 2 — QA-to-Red Suite Creation
