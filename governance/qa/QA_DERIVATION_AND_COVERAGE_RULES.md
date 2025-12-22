# QA Derivation and Coverage Rules

**Status**: Mandatory  
**Last Updated**: 2025-12-22  
**Authority**: Johan Ras  
**Wave**: 2.6 - FM Build Readiness

---

## I. Constitutional Authority

**QA functions as proof of architecture realization, not as a signal.**

**Every architecture element MUST have corresponding test coverage before build authorization.**

---

## II. Purpose

This document defines:
1. How architecture elements map to QA assertions
2. What constitutes acceptable test coverage
3. When RED QA is permitted (pre-build only)
4. How test debt, skips, and deferrals are prohibited
5. How unmapped architecture elements are detected and handled
6. When and how to escalate insufficient QA coverage

**Goal**: Ensure QA validates that architecture has been realized correctly, not merely that code executes.

---

## III. Core Principle: QA as Proof

### Traditional (Rejected) Model

```
Code → Tests → Coverage Report → "Good enough"
```

**Problems**:
- Tests may not validate architecture
- Coverage percentage is meaningless if tests don't prove correctness
- Tests may pass while architecture is violated

### Governance Model (Mandated)

```
Architecture → Derived QA Assertions → Tests → Coverage = Proof
```

**Benefits**:
- Every architecture element has explicit test coverage
- Tests prove architecture realization
- Coverage is meaningful (traces to architecture)
- Missing coverage = incomplete architecture realization

---

## IV. Architecture Element → QA Assertion Mapping

### Rule 1: Every Architecture Element Must Be Test-Covered

**Architecture Element Types**:
1. **Components** - Modules, classes, services, functions
2. **Interfaces** - APIs, contracts, integration points
3. **Data Models** - Schemas, entities, relationships
4. **Behaviors** - Business logic, workflows, state transitions
5. **Constraints** - Validation rules, invariants, preconditions
6. **Error Handling** - Exception paths, error recovery, fallbacks
7. **Performance** - Latency, throughput, resource usage
8. **Security** - Authentication, authorization, data protection

**Mapping Requirement**:
- Each architecture element MUST map to ≥1 QA assertion
- Each QA assertion MUST trace back to ≥1 architecture element
- No unmapped architecture elements permitted
- No orphaned QA assertions permitted

---

### Rule 2: QA Assertion Derivation Process

**Step 1: Identify Architecture Elements**
- Parse architecture specification
- Extract all components, interfaces, data models, behaviors, constraints, error handling, performance requirements, security requirements

**Step 2: Generate QA Assertions**
For each architecture element, generate assertions that prove:
- **Existence**: Element exists in implementation
- **Interface Compliance**: Element's interface matches specification
- **Behavior Compliance**: Element behaves as specified
- **Constraint Satisfaction**: Element satisfies all constraints
- **Error Handling**: Element handles errors as specified
- **Integration**: Element integrates correctly with other elements

**Step 3: Create Traceability Matrix**
- Architecture Element ID → QA Assertion IDs
- QA Assertion ID → Architecture Element ID
- Coverage Percentage per Element
- Overall Coverage Percentage

---

### Rule 3: Minimum QA Assertions per Element Type

| Architecture Element Type | Minimum QA Assertions |
|--------------------------|----------------------|
| Component | 3 (existence, interface, behavior) |
| Interface | 4 (schema, success path, error path, integration) |
| Data Model | 3 (schema validation, CRUD operations, constraints) |
| Behavior | 2 (happy path, edge cases) |
| Constraint | 2 (satisfied, violated) |
| Error Handling | 2 (error triggered, error recovered) |
| Performance | 1 (meets requirement under load) |
| Security | 3 (authenticated access, unauthorized blocked, data protected) |

**Total minimum assertions = sum across all architecture elements.**

---

## V. Acceptable Test Coverage Definition

### Coverage Metrics

1. **Architecture Element Coverage**
   - Percentage of architecture elements with ≥1 QA assertion
   - **Required Minimum**: 100%
   - **No exceptions**

2. **QA Assertion Coverage**
   - Percentage of QA assertions implemented as tests
   - **Required Minimum**: 100%
   - **No exceptions**

3. **Code Coverage** (Secondary Metric)
   - Percentage of code lines/branches executed by tests
   - **Required Minimum**: 80% (guideline)
   - **Note**: High code coverage without architecture traceability is insufficient

### Coverage Validation

**PASS Criteria**:
- ✅ Architecture Element Coverage = 100%
- ✅ QA Assertion Coverage = 100%
- ✅ All tests pass (GREEN)
- ✅ Traceability matrix complete
- ✅ No unmapped elements
- ✅ No test debt

**FAIL Criteria**:
- ❌ Architecture Element Coverage < 100%
- ❌ QA Assertion Coverage < 100%
- ❌ Any tests failing (RED)
- ❌ Traceability matrix incomplete
- ❌ Any unmapped elements
- ❌ Test debt present

---

## VI. RED QA (Pre-Build Only)

### Definition

**RED QA** = Tests that are defined but intentionally failing or not yet implemented.

### Acceptable RED QA

RED QA is ONLY acceptable during:
1. **Architecture Design Phase** - Tests defined before implementation
2. **Test-First Development** - Tests written before code
3. **RED → GREEN Cycle** - Tests RED, then implementation makes them GREEN

**Acceptable Location**: Only in development/feature branches, never in main/release branches.

---

### Unacceptable RED QA

RED QA is NEVER acceptable:
1. **At Build Authorization Time** - All tests must be GREEN before build
2. **In Main Branch** - Main branch must always be GREEN
3. **In Release Branches** - Release branches must always be GREEN
4. **Post-Merge** - Merged code must have all tests GREEN

---

### RED QA Handling

**During Development**:
1. RED tests are tracked in `qa/design_phase/DP_RED_REGISTRY.json`
2. Each RED test must have:
   - Test ID
   - Architecture element it validates
   - Reason for RED
   - Target GREEN date
   - Owner

**Before Build Authorization**:
1. All RED tests must be GREEN
2. DP-RED registry must be empty or archived
3. QA validation report must show 0 RED tests

**If RED tests exist at build authorization time**:
- Build authorization BLOCKED
- Escalate to build owner
- Implement missing functionality or remove tests
- Re-validate coverage = 100% and all GREEN

---

## VII. Test Debt Prohibition

### Prohibited Patterns

The following patterns are **ABSOLUTELY FORBIDDEN**:

1. **Test Skipping**
   ```python
   @pytest.skip("Will fix later")
   @unittest.skip("Not working yet")
   it.skip("Broken test")
   ```

2. **Conditional Skipping (without governance approval)**
   ```python
   if condition: skip_test()
   ```

3. **Test Disabling**
   ```python
   # def test_feature():  # Commented out
   ```

4. **False Positive Tests**
   ```python
   def test_feature():
       pass  # No assertions
       
   def test_feature():
       assert True  # Always passes
   ```

5. **Deferred Testing**
   ```python
   # TODO: Add tests later
   # FIXME: Tests missing
   ```

---

### Detection and Enforcement

**Pre-Commit Detection**:
- Scan for forbidden patterns in test files
- Block commit if patterns detected
- Require removal or governance approval

**PR Gate Detection**:
- Build-to-Green workflow scans for test debt patterns
- PR blocked if test debt detected
- Escalation required for approval

**Exception Process**:
- Extremely rare
- Requires Johan Ras authorization
- Must be time-bounded and tracked
- Requires DP-RED registry entry

---

## VIII. Unmapped Architecture Element Detection

### Detection Process

**Step 1: Parse Architecture**
- Extract all architecture elements from frozen architecture artifacts
- Generate list of required QA assertions

**Step 2: Parse QA Implementation**
- Extract all implemented tests
- Extract traceability metadata

**Step 3: Compare**
- Identify architecture elements without QA assertions
- Identify QA assertions without architecture elements
- Generate unmapped element report

---

### Unmapped Element Handling

**If unmapped architecture elements detected**:

1. **BLOCK build authorization**
2. **Generate gap report**:
   - List of unmapped elements
   - Architecture element IDs
   - Severity (critical, high, medium)
3. **Escalate to QA owner**
4. **Derive missing QA assertions**
5. **Implement missing tests**
6. **Re-validate coverage = 100%**
7. **Log failure**: `FAILURE_TYPE: UNMAPPED_ARCHITECTURE_ELEMENTS`

**If unmapped QA assertions detected**:

1. **Investigate**: Why do these tests exist?
2. **Options**:
   - A. Tests validate implicit architecture (update architecture)
   - B. Tests are orphaned (remove tests)
   - C. Tests are mislabeled (fix traceability metadata)
3. **Update traceability matrix**
4. **Re-validate no unmapped assertions**

---

## IX. Insufficient QA Coverage Escalation

### Escalation Triggers

Escalate to Johan Ras if:
1. Architecture element coverage < 100%
2. QA assertion coverage < 100%
3. Unmapped elements cannot be resolved
4. Tests cannot be implemented (architectural issue)
5. Coverage validation fails repeatedly (>2 attempts)

### Escalation Content

Must include:
- Current coverage metrics
- List of unmapped elements
- Gap analysis
- Blocker description
- Proposed resolution (if known)
- Impact on build timeline

### Escalation Response

Johan Ras will:
- Authorize scope reduction (remove unmapped elements from architecture), OR
- Authorize deadline extension (allow time for test implementation), OR
- Authorize architecture revision (fix architectural issues), OR
- Provide clarification, OR
- Declare build blocked pending resolution

---

## X. QA Derivation Process (Detailed)

### Phase 1: Architecture Element Extraction

**Input**: Frozen architecture artifacts (`architecture/builds/<build-id>/`)

**Process**:
1. Parse `compilation.md` for component list
2. Parse `interfaces/` for API definitions
3. Parse `models/` for data model definitions
4. Parse requirements for behavior specifications
5. Extract constraints, error handling, performance, security requirements

**Output**: Architecture Element Inventory

---

### Phase 2: QA Assertion Generation

**Input**: Architecture Element Inventory

**Process**:
For each architecture element:
1. Generate existence assertions
2. Generate interface compliance assertions
3. Generate behavior compliance assertions
4. Generate constraint satisfaction assertions
5. Generate error handling assertions
6. Generate integration assertions

**Output**: Derived QA Assertion Catalog

---

### Phase 3: Test Implementation Planning

**Input**: Derived QA Assertion Catalog

**Process**:
1. Group assertions by test suite
2. Identify shared test fixtures/data
3. Determine test execution order
4. Estimate test implementation effort
5. Assign test owners

**Output**: QA Implementation Plan

---

### Phase 4: Test Implementation

**Input**: QA Implementation Plan

**Process**:
1. Implement test fixtures
2. Implement test data generators
3. Implement test assertions
4. Link tests to architecture elements (traceability metadata)
5. Validate tests execute correctly

**Output**: Implemented Test Suite

---

### Phase 5: Coverage Validation

**Input**: Implemented Test Suite

**Process**:
1. Execute all tests
2. Generate coverage report
3. Validate architecture element coverage = 100%
4. Validate QA assertion coverage = 100%
5. Validate all tests GREEN
6. Generate traceability matrix

**Output**: QA Coverage Validation Report

**Status**: PASS or FAIL

---

## XI. Traceability Requirements

### Traceability Metadata

Each test MUST include metadata:

```python
@test(architecture_element="USER_AUTHENTICATION_SERVICE")
@test(qa_assertion="AUTH_001: Service authenticates valid credentials")
def test_valid_user_authentication():
    # Test implementation
```

```javascript
describe('User Authentication Service', () => {
  // @architecture_element: USER_AUTHENTICATION_SERVICE
  // @qa_assertion: AUTH_001: Service authenticates valid credentials
  it('should authenticate valid user credentials', () => {
    // Test implementation
  });
});
```

---

### Traceability Matrix Format

```json
{
  "architecture_element_id": "USER_AUTHENTICATION_SERVICE",
  "architecture_element_type": "component",
  "qa_assertions": [
    {
      "assertion_id": "AUTH_001",
      "assertion_text": "Service authenticates valid credentials",
      "test_ids": ["test_valid_user_authentication"],
      "status": "GREEN"
    },
    {
      "assertion_id": "AUTH_002",
      "assertion_text": "Service rejects invalid credentials",
      "test_ids": ["test_invalid_user_authentication"],
      "status": "GREEN"
    }
  ],
  "coverage": "100%"
}
```

---

## XII. Build Authorization Precondition

**QA Derivation & Coverage Rules is a mandatory precondition for build authorization.**

Build Authorization Gate requires:
- Architecture Compilation Contract: **PASS**
- QA Derivation & Coverage Rules: **PASS**
- Scope Freeze: **CONFIRMED**

**If QA Coverage != 100% or any tests RED, build authorization CANNOT proceed.**

---

## XIII. Evidence Requirements

### Required Evidence

For each build:
1. Architecture Element Inventory
2. Derived QA Assertion Catalog
3. QA Implementation Plan
4. Implemented Test Suite (code)
5. Test Execution Report (all GREEN)
6. Coverage Report (100% architecture element coverage)
7. Traceability Matrix (complete)

### Evidence Storage

- Location: `architecture/builds/<build-id>/qa-evidence/`
- Retention: Indefinite
- Access: Organization-wide

---

## XIV. Machine Decidability

**These rules are designed to be mechanically enforceable.**

Future FM Agent will:
- Auto-extract architecture elements
- Auto-generate QA assertions
- Auto-detect unmapped elements
- Auto-validate coverage = 100%
- Auto-block build authorization on FAIL

---

## XV. Success Criteria

QA derivation and coverage is successful when:
1. ✅ All architecture elements have QA assertions
2. ✅ All QA assertions implemented as tests
3. ✅ All tests GREEN
4. ✅ Coverage = 100%
5. ✅ Traceability matrix complete
6. ✅ No test debt
7. ✅ Build authorization possible

---

## XVI. References

- **Corporate Governance Canon**: https://github.com/MaturionISMS/maturion-foreman-governance
- **Architecture Compilation Contract**: `governance/architecture/ARCHITECTURE_COMPILATION_CONTRACT.md`
- **Build Authorization Gate**: `governance/build/BUILD_AUTHORIZATION_GATE.md`
- **QA Governance**: `governance/specs/qa-governance.md`
- **QA-of-QA**: `governance/specs/qa-of-qa.md`
- **Zero Test Debt Constitutional Rule**: `governance/policies/zero-test-debt-constitutional-rule.md`

---

*QA as Proof - Not as Signal*
