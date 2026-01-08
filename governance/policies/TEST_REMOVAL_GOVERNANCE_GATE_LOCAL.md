# TEST_REMOVAL_GOVERNANCE_GATE_LOCAL

**Policy ID**: TEST_REMOVAL_GOVERNANCE_GATE_LOCAL  
**Version**: 1.0.0  
**Date**: 2026-01-08  
**Authority**: Governance Canon  
**Status**: ACTIVE (Local Enforcement)

---

## Purpose

This document establishes **local enforcement** of the canonical TEST_REMOVAL_GOVERNANCE_GATE policy for the Maturion Foreman Office App repository. It prevents test dodging by requiring evidence-based justification and appropriate authorization before any test removal.

---

## Canonical Reference

**Source**: APGI-cmy/maturion-foreman-governance  
**Canonical Policy**: `governance/policy/TEST_REMOVAL_GOVERNANCE_GATE.md`  
**Layered Down From**: PR #891

---

## Zero-Tolerance Policy

**Tests SHALL NOT be removed without proof that they are unmaintainable or truly redundant.**

### Core Principle

Test removal is **permanently suspicious** and requires the same rigor as:
- Governance document deletion
- Security control removal
- Architecture regression

**Default position**: Tests stay. Removal requires overwhelming evidence.

---

## Prohibited Justifications

The following justifications are **NEVER acceptable** for test removal:

### ❌ "Tests don't map to architecture"

**Why prohibited**: 
- Tests may map to behaviors, not class names
- Evidence tests validate governance artifacts
- Heartbeat tests validate platform liveness
- Governance tests validate constitutional rules

**Correct approach**: Use ARCHITECTURE_TEST_TRACEABILITY_METHOD_LOCAL.md to determine if test is truly unmapped.

### ❌ "Architecture sections not implemented yet"

**Why prohibited**:
- RED QA tests are **intentional** and **required**
- RED tests represent future requirements
- Removing RED tests = abandoning planned functionality

**Correct approach**: Leave RED tests in place. Mark with `@pytest.mark.wave{N}` for future implementation.

### ❌ "Class names not found in architecture"

**Why prohibited**:
- Class names are implementation details
- Tests validate **behaviors**, not class names
- Architecture describes **capabilities**, not class hierarchies

**Correct approach**: Map test → behavior → requirement → architecture section using correct methodology.

### ❌ "Too many tests / noise reduction"

**Why prohibited**:
- Test count is irrelevant to test value
- "Noise" is subjective and often indicates real issues
- Removing tests to make dashboards "cleaner" = test dodging

**Correct approach**: Fix root cause of noise (e.g., improve test categorization, fix flaky tests).

### ❌ "Speculative" or "Unimplemented"

**Why prohibited**:
- All RED QA tests are "unimplemented" by design
- "Speculative" tests represent planned functionality
- QA-to-Red methodology requires tests before implementation

**Correct approach**: Tests stay until explicitly deprioritized by CS2 with architecture justification.

---

## Required Evidence for Test Removal

Before ANY test removal, the following evidence MUST be provided:

### 1. Traceability Analysis

**Using correct methodology** (see ARCHITECTURE_TEST_TRACEABILITY_METHOD_LOCAL.md):

```
Test → Behavior Under Test → Requirement → Architecture Section
```

**NOT** the incorrect methodology:
```
Test → Class Name → Search Architecture (WRONG)
```

**Evidence required**:
- What behavior does this test validate?
- What requirement drives this behavior?
- What architecture section specifies this requirement?
- If none found: Why is this behavior not required? (CS2 decision needed)

### 2. Impact Assessment

- How many tests are being removed? (1-5, 6-10, 11+)
- What coverage is lost? (behavior, edge cases, error paths)
- What risks emerge from removal? (regression, compliance, security)

### 3. Alternative Coverage

- Is this behavior tested elsewhere? (provide test references)
- If yes: Why have duplicate tests? (acceptable duplication scenarios exist)
- If no: Why is this behavior no longer required? (requires architecture change)

### 4. Removal Justification

**Only acceptable justifications**:
1. **Duplicate coverage**: Same behavior tested elsewhere with better clarity
2. **Architecture change**: Requirement explicitly removed via governance process
3. **Unmaintainable**: Test cannot be made reliable despite remediation attempts (CS2 decision)

---

## Approval Requirements

Test removal requires authorization based on scope:

| Test Count | Authorization Required |
|------------|------------------------|
| 1-5 tests  | FM approval + evidence |
| 6-10 tests | FM + Governance Liaison (GA) approval |
| 11+ tests  | CS2 approval + architecture impact assessment |

**Violation of approval requirements = Immediate test restoration + Incident report**

---

## Enforcement Process

### Before Removal

1. **Stop**: Do not remove tests immediately
2. **Analyze**: Apply correct traceability methodology
3. **Document**: Create removal justification with required evidence
4. **Seek approval**: Per authorization requirements above
5. **Log**: Document in TEST_REMOVAL_LOG.md (if approved)

### If Removal Proceeds Without Authorization

1. **Immediate restoration**: Revert all test removals
2. **Incident report**: Document as test dodging incident
3. **Root cause analysis**: Why did unauthorized removal occur?
4. **Prevention update**: Update builder contracts/gates as needed

---

## Special Cases

### RED QA Tests (Intentionally Failing)

**Default**: RED tests SHALL NOT be removed.

**Acceptable actions**:
- Mark with appropriate wave markers (`@pytest.mark.wave1`, etc.)
- Document in RED_QA/README.md
- Track in build plan for future implementation

**Unacceptable actions**:
- Removing because "not implemented"
- Removing because "failing"
- Removing to make test suite pass

### Evidence Tests (Governance Artifacts)

**Default**: Evidence tests SHALL NOT be removed.

**These validate**:
- Governance artifact existence
- Governance artifact schemas
- Governance artifact traceability

**Removal only allowed if**:
- Governance artifact itself is deprecated (requires governance process)
- Alternative validation mechanism proven superior (requires CS2 approval)

### Heartbeat/Liveness Tests

**Default**: Heartbeat tests SHALL NOT be removed.

**These validate**:
- Platform basic functionality
- Critical path availability
- Stall detection

**Removal only allowed if**:
- Functionality no longer exists (requires architecture change)
- Replaced by better liveness mechanism (requires CS2 approval)

---

## TEST_REMOVAL_LOG.md

All approved test removals MUST be logged:

**Location**: `governance/incidents/TEST_REMOVAL_LOG.md`

**Required fields**:
- Date
- Test(s) removed
- Justification
- Evidence reference
- Approver
- Alternative coverage (if any)

**Purpose**: Audit trail for test removal decisions

---

## Relationship to Other Policies

This policy enforces:
- **T0-003**: Zero Test Debt Constitutional Rule
- **ZERO_WARNING_TEST_DEBT_IMMEDIATE_REMEDY_DOCTRINE.md**: Quality signal preservation
- **ARCHITECTURE_TEST_TRACEABILITY_METHOD_LOCAL.md**: Correct traceability methodology

This policy prevents:
- Test dodging (hiding quality signals)
- Coverage regression (losing validation)
- Architectural drift (removing behavioral constraints)

---

## Consequences of Violation

**Violation = Test Dodging = Work Stoppage**

1. **Immediate**: All test removals reverted
2. **Documentation**: Incident report created
3. **Prevention**: Builder contracts updated
4. **Review**: Pattern analysis for systemic issues

**Zero tolerance. No exceptions.**

---

## References

**Canonical Governance**:
- TEST_REMOVAL_GOVERNANCE_GATE.md (maturion-foreman-governance)
- PR #891: Governance layer-down for test dodging prevention

**Related Local Policies**:
- ARCHITECTURE_TEST_TRACEABILITY_METHOD_LOCAL.md
- INCIDENT-2026-01-08-WARNING-SUPPRESSION.md

**Implementation**:
- `.github/agents/ForemanApp-agent.md` (Test Removal Authorization section)
- All builder contracts (Test and Warning Governance sections)

---

**Policy Owner**: Foreman (FM)  
**Review Cycle**: Quarterly  
**Next Review**: 2026-04-08  
**Status**: ACTIVE
