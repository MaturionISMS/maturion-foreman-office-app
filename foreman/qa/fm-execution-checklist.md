# Foreman (FM) Execution Checklist

**Version**: 1.0.0  
**Status**: Active  
**Authority**: BUILD_PHILOSOPHY.md + Foreman Governance  
**Purpose**: Permanent guardrail checklist for Foreman-led build execution  
**Date Created**: 2025-12-30

---

## I. Purpose and Scope

This checklist provides permanent guardrails for all Foreman-led build execution activities. It ensures constitutional compliance, prevents governance violations, and enforces the Build Philosophy throughout the execution lifecycle.

**Constitutional Authority**:
- BUILD_PHILOSOPHY.md (all sections)
- Foreman Governance Canon
- QA Governance Requirements

---

## II. Pre-Execution Validation

### ☐ Architecture is frozen and validated

**Requirements**:
- ✅ Architecture document exists and is complete
- ✅ Architecture validation checklist passed
- ✅ No TBD, TODO, or placeholder sections
- ✅ All components, interfaces, and data models defined
- ✅ Architecture is frozen (no changes allowed during build)

**Validation**:
```bash
python validate-repository.py --check architecture
```

---

### ☐ QA-to-Red phase is complete

**Requirements**:
- ✅ QA suite exists and has been executed
- ✅ QA status is validly RED (at least 1 test failing)
- ✅ All RED tests are intentionally RED (design phase validation)
- ✅ No test debt exists (no .skip(), .todo(), stubs)
- ✅ QA-to-Red acceptance checklist completed

**Validation**:
```bash
# Check QA-to-Red completion
python foreman/scripts/validate-qa-green.py --phase red

# Verify test intent classification
python foreman/scripts/validate-dp-red-compliance.py
```

**See**: `foreman/qa/qa-to-red-acceptance-checklist.md`

---

### ☐ All RED tests are classified and traceable

**CRITICAL REQUIREMENT**: No orphaned tests allowed

Every RED test MUST be explicitly classified as:
- **INTENTIONAL_RED** - Implementation not yet exists, traceable to architecture
- **UNINTENTIONAL_RED** - Defect/misconfiguration, must be fixed immediately

**Validation**:
```bash
python foreman/scripts/validate-dp-red-compliance.py --detect-orphaned
```

**Success Criteria**:
- ✅ All RED tests have declared intent (INTENTIONAL_RED or UNINTENTIONAL_RED)
- ✅ All INTENTIONAL_RED tests traceable to frozen architecture component
- ✅ All INTENTIONAL_RED tests have documented missing implementation
- ✅ All INTENTIONAL_RED tests registered in QA registry
- ✅ All INTENTIONAL_RED tests mapped to future Build-to-Green tasks
- ✅ **Zero orphaned or unexplained RED tests exist**

**Orphaned Test Definition** (PROHIBITED):
- ❌ RED test without declared intent
- ❌ Cannot trace to frozen architecture
- ❌ Missing implementation not identified  
- ❌ RED due to ambiguity or oversight

**Enforcement**: Orphaned RED tests constitute a governance violation and trigger STOP + escalation.

---

### ☐ Build plan is complete and sequenced

**Requirements**:
- ✅ Build tasks derived from QA-to-Red suite
- ✅ Builder assignments are clear
- ✅ Task dependencies identified
- ✅ Build sequence validated
- ✅ No tasks without QA validation

---

## III. During Execution

### ☐ Zero Regression enforcement active

**Requirements**:
- ✅ All existing tests continue to pass
- ✅ No breaking changes without approval
- ✅ Integration points remain compatible
- ✅ Regression test suite runs on every change

**Validation**:
```bash
# Run regression suite
python -m pytest tests/ --regression-only
```

---

### ☐ Architectural alignment maintained

**Requirements**:
- ✅ All builds reference frozen architecture
- ✅ No architectural drift
- ✅ Module boundaries not violated
- ✅ Integration contracts honored

**Validation**:
```bash
python validate-repository.py --check drift
```

---

### ☐ Builder boundaries respected

**Requirements**:
- ✅ Builders operate within assigned domains
- ✅ No cross-builder boundary violations
- ✅ Builder collaboration rules followed
- ✅ Builder permissions enforced

---

### ☐ Context preservation active

**Requirements**:
- ✅ All decisions documented with rationale
- ✅ Change records maintained
- ✅ Memory fabric updated
- ✅ No loss of architectural context

---

## IV. Build-to-Green Progression

### ☐ Tests transitioning from RED to GREEN

**Requirements**:
- ✅ Implementation makes tests pass
- ✅ No test modifications to force pass
- ✅ No skipped or disabled tests
- ✅ Each GREEN test removes corresponding DP-RED entry

**Validation**:
```bash
# Check DP-RED registry cleanup
python foreman/scripts/validate-dp-red-compliance.py --check-cleanup
```

---

### ☐ 100% pass requirement maintained

**ABSOLUTE REQUIREMENT**: 
- ✅ 100% of tests passing (no exceptions)
- ❌ 99% passing = TOTAL FAILURE
- ❌ 301/303 tests = TOTAL FAILURE  
- ❌ ANY test failure = BUILD BLOCKED

**Governance Supremacy Rule**: No "good enough" compromises allowed.

**Validation**:
```bash
python -m pytest tests/ --strict
```

---

### ☐ Zero test debt maintained

**Requirements**:
- ✅ No skipped tests (.skip(), .todo())
- ✅ No incomplete tests (stubs, no assertions)
- ✅ No failing tests carried forward
- ✅ No "will fix later" deferrals

**Validation**:
```bash
python foreman/scripts/detect-test-debt.py
```

**Enforcement**: Any test debt = STOP → FIX → RE-RUN → VERIFY

---

## V. Post-Execution Validation

### ☐ All validation gates passed

**Requirements**:
- ✅ All tests GREEN (100%)
- ✅ TypeScript compilation passes
- ✅ Linting passes (zero errors, zero warnings)
- ✅ Build succeeds
- ✅ No console errors
- ✅ Interface integrity validated

**Validation**:
```bash
# Full validation suite
npm run validate:all
python foreman/scripts/validate-qa-green.py --full
```

---

### ☐ DP-RED registry cleared (if transitioning to QA_BUILD)

**Requirements**:
- ✅ All INTENTIONAL_RED tests now GREEN
- ✅ Registry entries removed for GREEN tests
- ✅ Registry is empty OR only unimplemented features remain
- ✅ Phase transition validated

**Validation**:
```bash
python foreman/scripts/validate-dp-red-compliance.py --check-build-gate
```

---

### ☐ Evidence trail complete

**Requirements**:
- ✅ Build outcomes documented
- ✅ Test results captured
- ✅ Change records committed
- ✅ Memory fabric updated
- ✅ Compliance evidence generated

---

## VI. Orphaned Test Prevention (Permanent Guardrail)

### ☐ No orphaned or unexplained RED tests exist

**CRITICAL GOVERNANCE REQUIREMENT**:

This checklist item ensures that all RED QA tests are explicitly classified, with each INTENTIONAL_RED test:
- ✅ Traced to a frozen architecture component
- ✅ Linked to a missing implementation  
- ✅ Registered in the QA registry
- ✅ Mapped to a future Build-to-Green task

**Orphaned Test Criteria** (MUST NOT EXIST):
- ❌ RED test without declared intent (neither INTENTIONAL nor UNINTENTIONAL)
- ❌ Cannot be traced to frozen architecture component
- ❌ Missing implementation not identified
- ❌ INTENTIONAL_RED without future_build_task mapping
- ❌ RED due to ambiguity or oversight

**Validation**:
```bash
python foreman/scripts/validate-dp-red-compliance.py --full-report
```

**Enforcement**:
- Orphaned RED tests are a **governance violation**
- Block all progression until classified and traceable
- Escalate to Foreman if unresolvable

**Success Criteria**:
- ✅ Zero orphaned tests detected
- ✅ All RED tests have complete traceability: Intent → Architecture → Implementation Plan
- ✅ Validation reports: "No orphaned tests found"

**Authority**: BUILD_PHILOSOPHY.md Phase 2 + DP-RED Registry Specification

---

## VII. Phase Transition Gates

### ☐ QA_DESIGN → QA_BUILD transition requirements

**Preconditions**:
- ✅ Architecture frozen and validated
- ✅ All DP-RED entries documented
- ✅ Build plan created
- ✅ No orphaned tests

**Block Conditions**:
- ❌ Any RED tests without classification
- ❌ Any orphaned tests
- ❌ Architecture not frozen
- ❌ Build plan incomplete

---

### ☐ QA_BUILD → QA_GREEN transition requirements

**Preconditions**:
- ✅ DP-RED registry empty (all tests GREEN)
- ✅ 100% test pass rate
- ✅ Zero test debt
- ✅ All validations passing

**HARD BLOCK**:
- ❌ If any DP-RED entries exist
- ❌ If any tests RED
- ❌ If any test debt detected

---

## VIII. Escalation Triggers

### Immediate STOP and escalation required if:

- ❌ Orphaned RED tests detected
- ❌ Architecture frozen but changed during build
- ❌ Test debt introduced
- ❌ Regression detected
- ❌ 100% pass requirement violated
- ❌ Governance rule cannot be satisfied
- ❌ Builder boundary violation
- ❌ Context loss detected

**Escalation Path**: Foreman → Johan (Owner)

---

## IX. Sign-Off Requirements

### Final Execution Sign-Off

Before completing any build wave or phase:

- [ ] All checklist items validated and passing
- [ ] No governance violations detected
- [ ] No orphaned tests exist
- [ ] 100% test pass achieved
- [ ] Evidence trail complete
- [ ] Build Philosophy respected throughout
- [ ] Constitutional compliance confirmed

**Sign-Off Authority**: Foreman (Maturion)  
**Date**: ___________________  
**Validated By**: ___________________

---

## X. References

**Constitutional Documents**:
- BUILD_PHILOSOPHY.md
- foreman/qa/dp-red-registry-spec.md
- foreman/qa/qa-to-red-acceptance-checklist.md

**Validation Scripts**:
- foreman/scripts/validate-dp-red-compliance.py
- foreman/scripts/validate-qa-green.py
- foreman/scripts/detect-test-debt.py
- validate-repository.py

**Related Checklists**:
- foreman/qa/qa-to-red-acceptance-checklist.md
- PLATFORM_READINESS_EVIDENCE_VERIFICATION_CHECKLIST.md

---

**Last Updated**: 2025-12-30  
**Version**: 1.0.0  
**Status**: Active and Enforced

---

*Execution without orphaned tests. Progression with full traceability.*
