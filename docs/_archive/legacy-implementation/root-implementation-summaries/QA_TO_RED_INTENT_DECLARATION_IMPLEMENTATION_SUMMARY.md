# QA-to-Red Test Intent Declaration - Implementation Summary

**Issue**: QA-to-Red Test Intent Declaration (FM Layer-Down)  
**Date**: 2025-12-30  
**Status**: Implementation Complete  
**Authority**: BUILD_PHILOSOPHY.md Phase 2 + DP-RED Registry Specification

---

## I. Executive Summary

This implementation adds mandatory test intent declaration to the QA-to-Red phase, ensuring all RED tests are explicitly classified and traceable. The changes prevent orphaned tests and strengthen governance without weakening QA standards.

**Core Requirement**: Every RED test MUST be explicitly declared as either INTENTIONAL_RED or UNINTENTIONAL_RED, with complete traceability for INTENTIONAL_RED tests.

---

## II. Changes Made

### 1. Extended DP-RED Registry Specification

**File**: `foreman/qa/dp-red-registry-spec.md`

**Additions**:
- New mandatory `intent` field (enum: INTENTIONAL_RED | UNINTENTIONAL_RED)
- New `future_build_task` field (required for INTENTIONAL_RED tests)
- New section III.A: "Intent Classification and Orphaned Test Prevention"
- Comprehensive validation logic for intent classification
- Orphaned test criteria and prevention rules

**Schema Changes**:
```json
{
  "intent": "INTENTIONAL_RED",  // NEW: Mandatory classification
  "future_build_task": "B2G-FM-001: Implement Feature"  // NEW: Required for INTENTIONAL_RED
}
```

**Key Requirements Added**:
- INTENTIONAL_RED tests must have valid `architecture_ref`
- INTENTIONAL_RED tests must have `future_build_task` mapping
- INTENTIONAL_RED reason must indicate missing implementation
- UNINTENTIONAL_RED tests have 7-day age limit
- Orphaned tests (no intent, no traceability) are governance violations

---

### 2. Enhanced Validation Script

**File**: `foreman/scripts/validate-dp-red-compliance.py`

**Enhancements**:
- Added `intent` field to required fields list
- Added intent classification validation logic
- Added INTENTIONAL_RED specific checks:
  - Valid architecture_ref (not "N/A", not empty)
  - future_build_task field present
  - Reason indicates missing implementation
- Added UNINTENTIONAL_RED age checks:
  - Warning at 2 days
  - Error (blocks) at 7 days
- Enhanced error messages with governance violation indicators

**Test Coverage**:
- ✅ Missing intent field → "GOVERNANCE VIOLATION" error
- ✅ Invalid intent value → validation error
- ✅ INTENTIONAL_RED without architecture_ref → error
- ✅ INTENTIONAL_RED without future_build_task → error
- ✅ UNINTENTIONAL_RED > 7 days → blocking error
- ✅ Valid entries → pass

---

### 3. New Checklists Created

#### A. QA-to-Red Acceptance Checklist

**File**: `foreman/qa/qa-to-red-acceptance-checklist.md`

**Purpose**: Validates QA-to-Red phase completion before Build-to-Green progression

**Key Sections**:
- Mandatory Test Intent Declaration
- INTENTIONAL_RED Requirements (traceability, task mapping)
- UNINTENTIONAL_RED Requirements (age limits, fix tracking)
- Orphaned Test Prevention
- Registry Integrity Validation
- Phase Compliance
- Build-to-Green Readiness

**Validation Commands Provided**:
```bash
python foreman/scripts/validate-dp-red-compliance.py
python foreman/scripts/validate-dp-red-compliance.py --check-traceability
python foreman/scripts/validate-dp-red-compliance.py --detect-orphaned
```

---

#### B. FM Execution Checklist

**File**: `foreman/qa/fm-execution-checklist.md`

**Purpose**: Permanent guardrail checklist for all Foreman-led build execution

**Key Sections**:
- Pre-Execution Validation (architecture, QA-to-Red)
- During Execution (regression, alignment, boundaries)
- Build-to-Green Progression
- Post-Execution Validation
- **Section VI: Orphaned Test Prevention (Permanent Guardrail)**
- Phase Transition Gates
- Escalation Triggers

**Permanent Guardrail**:
```
☐ No orphaned or unexplained RED tests exist

Every RED test must have:
- Declared intent (INTENTIONAL_RED or UNINTENTIONAL_RED)
- Traceability to frozen architecture
- Documented missing implementation
- Future Build-to-Green task mapping
```

---

### 4. Updated Documentation

#### A. BUILD_PHILOSOPHY.md

**Changes**:
- Enhanced Phase 2 (RED QA) with test intent declaration requirements
- Added explicit orphaned test prevention rules
- Updated DP-RED mechanism description
- Added "Test Intent Declaration (Mandatory)" subsection

**Key Addition**:
> "Every RED test MUST be classified as INTENTIONAL_RED or UNINTENTIONAL_RED. RED status alone does NOT indicate failure. Intent classification determines treatment and acceptance."

---

#### B. PLATFORM_READINESS_EVIDENCE_VERIFICATION_CHECKLIST.md

**Changes**:
- Added "Orphaned Test Prevention" item to Pre-Handover Checklist
- Added validation command and success criteria
- Linked to BUILD_PHILOSOPHY.md Phase 2 authority

**Addition**:
```markdown
☐ All RED QA tests are explicitly classified as INTENTIONAL or UNINTENTIONAL,
   with each INTENTIONAL_RED test:
   - Traced to a frozen architecture component
   - Linked to a missing implementation
   - Registered in the QA registry
   - Mapped to a future Build-to-Green task
```

---

#### C. DP-RED-QUICK-REFERENCE.md

**Changes**:
- Updated registry entry example with `intent` and `future_build_task` fields
- Added "Test Intent Classification (Mandatory)" section
- Added "Orphaned Tests (PROHIBITED)" explanation

**Key Additions**:
- Definition of INTENTIONAL_RED
- Definition of UNINTENTIONAL_RED
- Orphaned test criteria
- Examples of valid entries

---

## III. Governance Compliance

### Constitutional Authority

This implementation is authorized by and enforces:
- BUILD_PHILOSOPHY.md Phase 2: RED QA (Failing Tests)
- Governance Supremacy Rule
- Zero Test Debt Constitutional Rule
- DP-RED Registry Specification

### Orphaned Test Prevention

**Definition**: A test is ORPHANED (governance violation) if:
- ❌ No declared intent (neither INTENTIONAL_RED nor UNINTENTIONAL_RED)
- ❌ Cannot be traced to frozen architecture component
- ❌ Missing implementation is not identified
- ❌ For INTENTIONAL_RED: no future_build_task mapping
- ❌ RED due to ambiguity or oversight

**Enforcement**: Orphaned RED tests block all progression and trigger STOP + escalation.

---

## IV. Validation Testing

### Test Scenarios Validated

1. **Missing Intent Field**:
   - Input: Entry without `intent` field
   - Result: ❌ GOVERNANCE VIOLATION error
   - Exit Code: 1

2. **INTENTIONAL_RED Without future_build_task**:
   - Input: INTENTIONAL_RED entry missing `future_build_task`
   - Result: ❌ Error: "Must be mapped to a Build-to-Green task"
   - Exit Code: 1

3. **INTENTIONAL_RED Without Valid Architecture Ref**:
   - Input: INTENTIONAL_RED with `architecture_ref: "N/A"`
   - Result: ❌ Error: "Must be traceable to frozen architecture"
   - Exit Code: 1

4. **UNINTENTIONAL_RED Too Old**:
   - Input: UNINTENTIONAL_RED registered 10 days ago
   - Result: ❌ Error: "Must be fixed immediately - exceeds 7-day limit"
   - Exit Code: 1

5. **Valid INTENTIONAL_RED**:
   - Input: Complete INTENTIONAL_RED entry with all required fields
   - Result: ✅ PASS - Merge allowed
   - Exit Code: 0

6. **Empty Registry**:
   - Input: Registry with no entries
   - Result: ✅ PASS - All tests must be GREEN
   - Exit Code: 0

---

## V. Integration Points

### CI/CD Integration

The validation is integrated into the build-to-green enforcement workflow:

```
1. enforce-zero-test-debt
       ↓
2. validate-dp-red-compliance  ← Enhanced with intent validation
       ↓
3. enforce-100-percent-pass
       ↓
4. ...
```

### Checklist Integration

Three levels of checklists now enforce orphaned test prevention:

1. **QA-to-Red Acceptance Checklist**
   - Validates QA-to-Red phase completion
   - Ensures all RED tests classified before progression

2. **FM Execution Checklist**
   - Permanent guardrail for all build execution
   - Section VI dedicated to orphaned test prevention

3. **Platform Readiness Checklist**
   - Platform-level verification
   - Required for wave transitions

---

## VI. Usage Examples

### Register INTENTIONAL_RED Test

```json
{
  "test_id": "foreman.liveness.test_heartbeat",
  "test_path": "tests/wave0_minimum_red/test_liveness.py::test_heartbeat_generation",
  "phase": "QA_DESIGN",
  "intent": "INTENTIONAL_RED",
  "reason": "Implementation module foreman.runtime.liveness does not exist yet. Test validates architecture contract before build.",
  "architecture_ref": "foreman/architecture/FOREMAN_ARCHITECTURE_v1.0.md#liveness-system",
  "future_build_task": "B2G-FM-001: Implement Foreman Liveness System",
  "registered_by": "Foreman",
  "registered_date": "2025-12-30T14:00:00Z",
  "module": "foreman",
  "category": "liveness",
  "build_blocker": true
}
```

### Register UNINTENTIONAL_RED Test

```json
{
  "test_id": "foreman.api.test_connection",
  "test_path": "tests/integration/test_api.py::test_connection",
  "phase": "QA_DESIGN",
  "intent": "UNINTENTIONAL_RED",
  "reason": "Test failing due to missing environment variable API_BASE_URL. Configuration defect must be fixed.",
  "architecture_ref": "N/A - configuration defect",
  "registered_by": "QA Engineer",
  "registered_date": "2025-12-30T14:00:00Z",
  "module": "foreman",
  "category": "integration",
  "build_blocker": true
}
```

### Validate Registry

```bash
# Full validation
python foreman/scripts/validate-dp-red-compliance.py

# Detect orphaned tests
python foreman/scripts/validate-dp-red-compliance.py --detect-orphaned

# JSON output
python foreman/scripts/validate-dp-red-compliance.py --json
```

---

## VII. Success Metrics

### Implementation Completeness

- ✅ Schema extended with intent classification
- ✅ Validation script enforces intent requirements
- ✅ QA-to-Red acceptance checklist created
- ✅ FM execution checklist created
- ✅ Platform readiness checklist updated
- ✅ BUILD_PHILOSOPHY.md updated
- ✅ All documentation updated
- ✅ Validation tested with multiple scenarios
- ✅ All test scenarios pass

### Governance Enforcement

- ✅ Orphaned tests mechanically blocked
- ✅ INTENTIONAL_RED traceability enforced
- ✅ UNINTENTIONAL_RED age limits enforced
- ✅ Build-to-Green task mapping required
- ✅ Architecture references validated
- ✅ Clear error messages for violations

---

## VIII. Files Modified

### Created Files (2)
1. `foreman/qa/qa-to-red-acceptance-checklist.md` (7,742 bytes)
2. `foreman/qa/fm-execution-checklist.md` (9,580 bytes)

### Modified Files (5)
1. `foreman/qa/dp-red-registry-spec.md` - Added intent classification section
2. `foreman/scripts/validate-dp-red-compliance.py` - Enhanced validation logic
3. `BUILD_PHILOSOPHY.md` - Updated Phase 2 requirements
4. `PLATFORM_READINESS_EVIDENCE_VERIFICATION_CHECKLIST.md` - Added orphaned test prevention
5. `foreman/qa/DP-RED-QUICK-REFERENCE.md` - Added intent classification guide

### Total Changes
- **7 files changed**
- **964 insertions**
- **4 deletions**

---

## IX. Compliance Statement

This implementation satisfies all requirements from the issue:

✅ **Mandatory Rule**: Every RED test MUST be explicitly declared as INTENTIONAL_RED or UNINTENTIONAL_RED

✅ **INTENTIONAL_RED Requirements**:
- Test traceable to frozen architecture component
- Missing implementation explicitly stated
- Registered in QA registry
- Mapped to future Build-to-Green task

✅ **Orphaned Test Criteria Enforced**:
- Tests without intent → governance violation
- Cannot trace to architecture → governance violation
- Missing implementation not identified → governance violation
- No future task mapping → governance violation

✅ **Enforcement**: Orphaned RED tests trigger STOP and escalation

✅ **Permanent Guardrail**: Checklist item added to:
- FM execution checklist
- QA-to-Red acceptance checklist
- Platform readiness checklist

---

## X. References

### Authoritative Documents
- BUILD_PHILOSOPHY.md Phase 2: RED QA (Failing Tests)
- foreman/qa/dp-red-registry-spec.md Section III.A
- foreman/qa/qa-to-red-acceptance-checklist.md
- foreman/qa/fm-execution-checklist.md Section VI

### Validation Scripts
- foreman/scripts/validate-dp-red-compliance.py

### Quick Reference
- foreman/qa/DP-RED-QUICK-REFERENCE.md

---

**Implementation Date**: 2025-12-30  
**Implementation Status**: Complete  
**Validation Status**: All scenarios tested and passing  
**Ready for Handover**: Yes

---

*No orphaned or unexplained RED tests shall progress to Build-to-Green.*
