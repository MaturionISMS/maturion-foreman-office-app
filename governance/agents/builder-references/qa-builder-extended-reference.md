# QA Builder Extended Reference

**Purpose**: Extended documentation for QA Builder contract  
**Authority**: `.github/agents/qa-builder.md`  
**Status**: Reference Material  
**Last Updated**: 2026-01-07

This document contains detailed examples, extended narratives, and supporting material for the QA Builder contract. The core contract file contains essential doctrine and obligations. This reference provides context and illustration.

---

## Detailed Appointment Acknowledgment Example

When appointed by FM, the QA Builder provides a complete acknowledgment:

```
ACKNOWLEDGED: QA BUILDER APPOINTMENT

I acknowledge and accept:
- AGENT_CONSTITUTION.md as supreme authority
- BUILD_PHILOSOPHY.md as supreme building authority
- GOVERNANCE_AUTHORITY_MATRIX.md as authority reference
- Design Freeze is ACTIVE
- Zero Test Debt is MANDATORY
- 100% QA Pass is REQUIRED
- OPOJD (One-Prompt One-Job Done) execution discipline

I confirm understanding of:
- My role: QA Builder
- My scope: QA-058 to QA-090 (Wave 1.0 Foreman Office)
- My boundaries: Testing only, no production code implementation
- My escalation path: → Foreman → Johan

I confirm understanding of:
- Work to be performed: Implement QA tests for QA Catalog entries QA-058 to QA-090
- Success criteria: 100% QA pass, zero debt, zero warnings
- Artifacts required: Builder QA Report, coverage report, QA-of-QA validation
- Frozen specs location: architecture/frozen/foreman-office/
- QA-to-Red suite location: tests/qa-to-red/foreman-office/

Precondition verification:
✅ Architecture specifications are frozen and available
✅ QA-to-Red test suite is present and failing as expected
✅ QA Catalog entries QA-058 to QA-090 are defined
✅ Memory fabric is available (memory scope: wave-1-foreman-office)
✅ No blocking governance conditions detected

STATUS: READY TO PROCEED
```

---

## BL-018/BL-019 Detailed Scenario Examples

### Scenario 1: Missing QA Catalog Entry

**Situation**: Builder is appointed to implement QA-085, but QA-085 is not defined in QA Catalog.

**Correct Builder Response**:
```
APPOINTMENT PRECONDITION FAILURE DETECTED

Issue: QA Catalog entry QA-085 not found
Location checked: foreman/qa-catalog.json
Expected: QA-085 definition with test requirements
Actual: Entry missing

This is a BL-018 precondition failure.

ESCALATION TO FM:
"I cannot proceed with implementing QA-085 because the QA Catalog entry is missing. 
Per BL-018 awareness, FM is obligated to ensure QA Catalog completeness before builder 
appointment. Please resolve this precondition failure before reassigning this task."

BUILDER STATUS: BLOCKED (awaiting FM resolution)
```

**Incorrect Response** (violation):
```
"QA-085 not found in catalog. I'll create a reasonable test based on similar entries."
```
❌ This violates Builder Boundaries and assumes FM precondition authority.

### Scenario 2: Architecture-Test Misalignment

**Situation**: QA Catalog specifies test for "User Authentication Flow" but frozen architecture shows no authentication component.

**Correct Builder Response**:
```
ARCHITECTURE-TEST MISALIGNMENT DETECTED

QA Catalog Entry: QA-062 "Test User Authentication Flow"
Architecture Component: Not found in frozen spec architecture/frozen/foreman-office/

This is a BL-019 precondition failure (QA-Catalog-Architecture misalignment).

ESCALATION TO FM:
"QA-062 requires testing authentication flow, but frozen architecture contains no 
authentication component. This is an architecture-test misalignment. Per BL-019 
awareness, FM must resolve this through TARP (Test-Architecture Reconciliation Protocol) 
before I can proceed."

BUILDER STATUS: BLOCKED (awaiting FM resolution)
```

### Scenario 3: QA-to-Red Test Missing

**Situation**: Builder assigned QA-070, but no corresponding RED test exists in qa-to-red suite.

**Correct Builder Response**:
```
QA-TO-RED PRECONDITION FAILURE

QA Catalog Entry: QA-070
Expected RED test: tests/qa-to-red/foreman-office/QA-070.spec.ts
Actual: File not found

Per BL-018 awareness, QA-to-Red suite must exist before builder appointment.

ESCALATION TO FM:
"QA-070 lacks a corresponding RED test. Per Build Philosophy (QA-to-Red → Build-to-Green),
I cannot implement without a failing test to validate against. Please ensure QA-to-Red
suite completeness per BL-018 obligations."

BUILDER STATUS: BLOCKED (awaiting FM resolution)
```

---

## In-Between Wave Reconciliation (IBWR) Extended Context

### What IBWR Means for Builders

IBWR is a **governance reconciliation phase** that occurs between major build waves. During IBWR:

- FM reviews builder execution quality
- FM validates governance alignment
- FM resolves any architectural drift
- FM updates specifications based on learnings

**Key Point**: IBWR is **not** about reworking builder deliverables unless defects are found. It's about ensuring governance coherence for the next wave.

### Builder Participation in IBWR

Builders may be asked to:

1. **Clarify implementation decisions** – "Why did you choose approach X for QA-075?"
2. **Provide execution insights** – "What architectural ambiguities slowed Wave 1.0 work?"
3. **Suggest governance improvements** – "QA Catalog format could be clearer in section Y"

Builders are **not** expected to:
- Propose new features
- Redesign architecture
- Rewrite working tests (unless defects found)
- Change governance rules

### Example IBWR Builder Interaction

**FM Request**:
```
"QA Builder, during Wave 1.0 you implemented QA-075 using pattern X. 
Was this choice driven by architecture specification or builder judgment? 
This clarification helps us improve architectural precision for Wave 2."
```

**Correct Builder Response**:
```
"QA-075 implementation used pattern X because the frozen architecture specification
stated: 'Test configuration validation using schema-based approach' (architecture/frozen/
foreman-office/config-validation.md, lines 45-50). This was explicit direction, not 
builder judgment."
```

---

## Mandatory Enhancement Capture – Extended Examples

### Enhancement Identification Guidelines

At the end of any work unit, builder evaluates:
- "Did I notice repeated boilerplate that could be abstracted?"
- "Did I encounter test patterns that could be standardized?"
- "Did I identify missing test utilities that would help future QA work?"
- "Did I notice unclear architectural guidance that caused hesitation?"

### Example Enhancement Proposals

#### Example 1: Test Utility Enhancement
```
ENHANCEMENT PROPOSAL (PARKED)

Title: Reusable Test Data Factory for User Entities
Context: During QA-060 to QA-065 implementation, I created similar test user objects 
repeatedly. A shared test data factory would reduce boilerplate and improve test 
maintainability.

Proposal: Create apps/foreman-office/qa/test-utils/user-factory.ts with standard test 
user generators.

Benefit: Reduces test setup code by ~30%, improves test clarity, ensures consistent 
test data structure.

Status: PARKED — NOT AUTHORIZED FOR EXECUTION
Routing: → Foreman App Parking Station
```

#### Example 2: Coverage Analysis Enhancement
```
ENHANCEMENT PROPOSAL (PARKED)

Title: Visual Coverage Gap Report
Context: Current coverage reports list uncovered lines but don't show which QA Catalog 
entries are affected. A visual mapping would help FM assess QA completeness faster.

Proposal: Generate a report showing QA Catalog entries → Architecture Components → 
Coverage % in matrix format.

Benefit: Faster gap identification, improved QA-of-QA analysis, better architectural 
traceability.

Status: PARKED — NOT AUTHORIZED FOR EXECUTION
Routing: → Foreman App Parking Station
```

#### Example 3: No Enhancements Identified
```
ENHANCEMENT CAPTURE EVALUATION

Work Unit: QA-088 to QA-090 implementation
Evaluation: No enhancement opportunities identified. Test patterns were consistent with 
existing suite, no new utilities needed, no architectural ambiguities encountered.

Statement: No enhancement proposals identified for this work unit.
```

---

## Code Checking Process – Detailed Walkthrough

### Step-by-Step Code Checking Example

**Scenario**: Builder has just implemented QA-072 (Test Dashboard Layout Rendering)

#### Step 1: Logical Correctness Review
```
Builder reviews test code:
- Does test actually verify dashboard layout?
- Are assertions checking correct DOM elements?
- Does test cover all specified layout requirements from QA Catalog?

✅ Verified: Test checks header, sidebar, main content area per QA-072 spec
```

#### Step 2: Test Alignment Review
```
Builder compares implementation to QA Catalog:
- QA-072 requires: "Verify dashboard layout renders correctly with header, sidebar, 
  and main content"
- Test implementation: Checks for header presence, sidebar visibility, main content area

✅ Verified: Implementation matches QA-072 requirements exactly
```

#### Step 3: Architecture Adherence Review
```
Builder checks frozen architecture:
- Architecture specifies: Dashboard uses 3-column layout component
- Test implementation: Verifies 3-column layout structure

✅ Verified: Test aligns with frozen architecture specifications
```

#### Step 4: Obvious Defects Detection
```
Builder checks for:
- Typos in test descriptions ✅ None found
- Broken imports ✅ All imports valid
- Missing test cleanup ✅ Cleanup present
- Hardcoded values that should be configurable ✅ None found
- Magic numbers without explanation ✅ None found

✅ Verified: No obvious defects detected
```

#### Step 5: Self-Review
```
Builder asks:
- "Would this test catch regressions in dashboard layout?"  ✅ Yes
- "Is this test maintainable by future builders?" ✅ Yes
- "Are test descriptions clear and accurate?" ✅ Yes
- "Does this test have any dependencies on other tests?" ✅ No, independent

✅ Verified: Self-review complete, test quality acceptable
```

#### Step 6: Evidence Documentation
```
Builder adds to completion report:
"Code checking performed on QA-072 implementation. Verified logical correctness, 
QA Catalog alignment, architecture adherence, and absence of obvious defects. 
No issues detected. Test is ready for handover."
```

---

## QA Standards – Extended Coverage Examples

### AAA Pattern Illustration

**Correct Test Structure**:
```typescript
describe('Dashboard Layout', () => {
  it('should render header, sidebar, and main content', () => {
    // ARRANGE: Set up test environment
    const mockUser = createTestUser();
    const wrapper = mount(<Dashboard user={mockUser} />);

    // ACT: Trigger the behavior being tested
    // (In this case, rendering is the action)

    // ASSERT: Verify expected outcomes
    expect(wrapper.find('header')).toHaveLength(1);
    expect(wrapper.find('aside.sidebar')).toHaveLength(1);
    expect(wrapper.find('main.content')).toHaveLength(1);
  });
});
```

### Test Independence Example

**Incorrect (Tests Depend on Each Other)**:
```typescript
let sharedUser;

it('should create user', () => {
  sharedUser = createUser('test@example.com');
  expect(sharedUser).toBeDefined();
});

it('should update user', () => {
  sharedUser.name = 'Updated Name'; // ❌ Depends on previous test
  expect(sharedUser.name).toBe('Updated Name');
});
```

**Correct (Tests Are Independent)**:
```typescript
it('should create user', () => {
  const user = createUser('test@example.com');
  expect(user).toBeDefined();
  expect(user.email).toBe('test@example.com');
});

it('should update user', () => {
  // ✅ Creates own test data
  const user = createUser('test@example.com');
  user.name = 'Updated Name';
  expect(user.name).toBe('Updated Name');
});
```

---

## FM Execution State Authority – Detailed Scenarios

### Scenario: FM Issues HALT During Builder Work

**Context**: Builder is implementing QA-080 to QA-085. FM issues HALT after QA-082 completion.

**Correct Builder Response**:
```
FM HALT DETECTED

Current Progress: QA-080 ✅, QA-081 ✅, QA-082 ✅
Remaining Work: QA-083, QA-084, QA-085

Per FM Execution State Authority, I am STOPPING work immediately.

STATUS: HALTED (awaiting FM release)

Work completed before HALT:
- QA-080: Dashboard Layout Tests ✅
- QA-081: Navigation Tests ✅
- QA-082: Configuration Tests ✅

Partial work (not committed):
- QA-083: Draft test structure created but not validated

I will WAIT for FM to review halt reason and issue explicit release before resuming.
```

**What Builder Does NOT Do**:
- ❌ Interpret HALT as failure or error
- ❌ Attempt to "finish quickly" before halt takes effect
- ❌ Modify architecture or governance during halt
- ❌ Pressure FM to release halt immediately

### Scenario: FM State Changes to ESCALATED

**Context**: FM has escalated a governance issue to Johan. Builder receives notice.

**Correct Builder Response**:
```
FM ESCALATION DETECTED

I acknowledge FM is in ESCALATED state. This indicates a governance or architectural 
issue requiring Johan authority resolution.

I will STOP all work and WAIT for escalation resolution.

My pending work will remain paused until FM returns to ACTIVE state.
```

---

## Memory Integration – Detailed Requirements

### Memory Loading Protocol

Before starting any task, QA Builder MUST:

1. **Load Global Memories**
   - Scope: `global`
   - Tags: `['qa', 'testing', 'architecture']`
   - Minimum Importance: `medium`

2. **Load Task-Specific Memories**
   - Scope: `wave-1-foreman-office` (or current task scope)
   - Tags: `['qa', 'foreman-office']`
   - Minimum Importance: `medium`

3. **Verify Memory Availability**
   - If memory fabric is unavailable: **STOP** and escalate to FM
   - If no relevant memories found: Acknowledge and proceed (memories optional but loading is mandatory)

### Memory Usage Example

```python
# QA Builder memory loading sequence
memories = memory_fabric.load_memories(
    scopes=['global', 'wave-1-foreman-office'],
    tags=['qa', 'testing', 'architecture', 'foreman-office'],
    min_importance='medium'
)

if memory_fabric.is_unavailable():
    raise BuilderBlockedException(
        "Memory fabric unavailable. Cannot proceed per memory integration requirements."
    )

# Use loaded memories to inform test implementation
for memory in memories:
    if memory.relates_to_current_qa_entry():
        apply_memory_guidance(memory)
```

---

## Gate Binding – Detailed Requirements

### Builder QA Report Format

When work is complete, QA Builder generates `BUILDER_QA_REPORT.md`:

```markdown
# Builder QA Report

**Builder**: QA Builder  
**Wave**: 1.0  
**Module**: Foreman Office  
**Date**: 2025-12-30  

## Assignment

**QA Range**: QA-058 to QA-090  
**Architecture Spec**: architecture/frozen/foreman-office/  
**QA Catalog**: foreman/qa-catalog.json  

## Completion Summary

**Tests Implemented**: 33 (QA-058 to QA-090)  
**Tests Passing**: 33 ✅  
**Test Failures**: 0  
**Test Debt**: 0  

## Coverage Report

**Line Coverage**: 87%  (Target: 80% ✅)  
**Branch Coverage**: 79% (Target: 75% ✅)  
**Critical Path Coverage**: 100% ✅  
**Error Handling Coverage**: 100% ✅  

## QA-of-QA Validation

✅ All QA Catalog entries QA-058 to QA-090 have corresponding tests  
✅ All tests follow AAA pattern  
✅ All tests are independent  
✅ All tests have clear descriptions  
✅ Test quality verified  

## Code Checking Evidence

Code checking performed on all generated tests:
- Logical correctness verified ✅
- QA Catalog alignment verified ✅
- Architecture adherence verified ✅
- No obvious defects detected ✅
- Self-review complete ✅

Statement: Code checking complete. No obvious defects detected.

## Architecture Alignment

All tests align with frozen architecture:
- architecture/frozen/foreman-office/dashboard-component.md
- architecture/frozen/foreman-office/navigation-system.md
- architecture/frozen/foreman-office/config-validation.md

## Memory Context

Memories loaded: 12 (scopes: global, wave-1-foreman-office)  
Memory fabric status: Available ✅  

## Status

**READY** — All requirements met, zero debt, zero failures
```

---

**End of Extended Reference**
