# QA-to-Red Acceptance Checklist

**Version**: 1.0.0  
**Status**: Active  
**Authority**: BUILD_PHILOSOPHY.md Phase 2 + DP-RED Registry Specification  
**Purpose**: Ensures QA-to-Red phase completion meets all requirements before Build-to-Green progression  
**Date Created**: 2025-12-30

---

## I. Purpose and Scope

This checklist validates that the QA-to-Red phase (BUILD_PHILOSOPHY.md Phase 2) has been completed correctly and all RED tests are properly classified and traceable before progressing to Build-to-Green (Phase 3).

**Constitutional Authority**: BUILD_PHILOSOPHY.md Phase 2: RED QA (Failing Tests)

---

## II. Mandatory Test Intent Declaration

### ☐ All RED tests are explicitly classified

Every RED test MUST be classified as either:
- **INTENTIONAL_RED** - RED because underlying component/integration is not yet implemented
- **UNINTENTIONAL_RED** - RED due to defect, misconfiguration, missing artifact, or test construction error

**Validation**:
```bash
python foreman/scripts/validate-dp-red-compliance.py
```

**Success Criteria**:
- ✅ All RED tests have `intent` field in registry
- ✅ No tests with missing or invalid intent classification
- ✅ Validation script reports zero intent classification errors

---

## III. INTENTIONAL_RED Requirements

### ☐ All INTENTIONAL_RED tests are traceable to frozen architecture

Each INTENTIONAL_RED test MUST have:

1. **Valid Architecture Reference**
   - `architecture_ref` field must point to a frozen architecture component
   - Reference must be specific and verifiable
   - Cannot be "N/A", empty, or generic

2. **Documented Missing Implementation**
   - `reason` field must clearly state what implementation is missing
   - Must explicitly indicate "does not exist", "not yet implemented", or similar
   - Minimum 20 characters

3. **Future Build Task Mapping**
   - `future_build_task` field must reference a Build-to-Green task
   - Task must be identifiable and planned
   - Cannot be empty or generic

**Validation Command**:
```bash
python foreman/scripts/validate-dp-red-compliance.py --check-traceability
```

**Success Criteria**:
- ✅ All INTENTIONAL_RED tests have valid `architecture_ref`
- ✅ All INTENTIONAL_RED tests have `future_build_task` defined
- ✅ All INTENTIONAL_RED reasons clearly indicate missing implementation
- ✅ No architecture references are "N/A" or empty
- ✅ All referenced architecture components exist and are frozen

---

## IV. UNINTENTIONAL_RED Requirements

### ☐ All UNINTENTIONAL_RED tests are being actively fixed

UNINTENTIONAL_RED tests represent defects and MUST be fixed immediately.

**Age Limits**:
- ⚠️ Warning: UNINTENTIONAL_RED older than 2 days
- ❌ Error: UNINTENTIONAL_RED older than 7 days (BLOCKS progression)

**Validation**:
```bash
python foreman/scripts/validate-dp-red-compliance.py --check-unintentional
```

**Success Criteria**:
- ✅ No UNINTENTIONAL_RED tests older than 7 days
- ✅ All UNINTENTIONAL_RED tests have clear fix plans documented
- ✅ UNINTENTIONAL_RED count is decreasing or zero

---

## V. Orphaned Test Prevention

### ☐ Zero orphaned or unexplained RED tests exist

An **ORPHANED TEST** is a governance violation. A test is orphaned if:

- ❌ No declared intent (neither INTENTIONAL_RED nor UNINTENTIONAL_RED)
- ❌ Cannot be traced to frozen architecture component
- ❌ Missing implementation is not identified
- ❌ RED due to ambiguity or oversight
- ❌ INTENTIONAL_RED without `future_build_task` mapping

**Validation**:
```bash
python foreman/scripts/validate-dp-red-compliance.py --detect-orphaned
```

**Success Criteria**:
- ✅ Zero orphaned tests detected
- ✅ All RED tests have complete traceability chain:
  - Intent → Architecture → Implementation Plan
- ✅ No ambiguous or unexplained RED status
- ✅ Validation reports "No orphaned tests found"

---

## VI. Registry Integrity

### ☐ DP-RED Registry is valid and complete

**Schema Validation**:
```bash
python foreman/scripts/validate-dp-red-compliance.py --validate-schema
```

**Required Checks**:
- ✅ Registry file exists: `foreman/qa/dp-red-registry.json`
- ✅ Schema version is correct: `1.0.0`
- ✅ Phase matches current phase file: `foreman/qa/current-phase.json`
- ✅ All entries have required fields
- ✅ No duplicate test_ids
- ✅ All dates are valid ISO-8601 format
- ✅ No entries with future registration dates

---

## VII. Phase Compliance

### ☐ Current phase allows DP-RED entries

**Phase Check**:
```bash
cat foreman/qa/current-phase.json
```

**Requirements**:
- ✅ Current phase is `QA_DESIGN` if RED tests exist
- ✅ Phase transition rules are enforced
- ✅ No attempt to progress to QA_BUILD with RED tests
- ✅ Registry phase matches current-phase.json

**Block Condition**:
- ❌ If phase is QA_BUILD or later and registry has entries → HARD BLOCK

---

## VIII. Test-to-Registry Mapping

### ☐ All failing tests are registered

**Validation**:
```bash
python foreman/scripts/validate-dp-red-compliance.py --check-mapping
```

**Requirements**:
- ✅ Every RED test from test execution is in registry
- ✅ No unregistered RED tests exist
- ✅ No orphaned registry entries (in registry but not failing)

**Note**: This validation is warning-only if test execution is unavailable, but MUST pass before phase progression.

---

## IX. Build-to-Green Readiness

### ☐ QA-to-Red phase is complete and ready for Build-to-Green

**Final Validation**:
```bash
python foreman/scripts/validate-dp-red-compliance.py --full-report
```

**Completion Criteria**:

1. ✅ All RED tests classified (INTENTIONAL_RED or UNINTENTIONAL_RED)
2. ✅ All INTENTIONAL_RED tests have:
   - Valid architecture traceability
   - Future build task mapping
   - Clear reason indicating missing implementation
3. ✅ All UNINTENTIONAL_RED tests are being fixed (< 7 days old)
4. ✅ Zero orphaned tests
5. ✅ Registry integrity validated
6. ✅ Phase compliance confirmed
7. ✅ Test-to-registry mapping complete
8. ✅ No governance violations detected

**Output Artifacts**:
- `dp-red-compliance-report.json` - Full validation report
- `dp-red-summary.md` - Human-readable summary

---

## X. Governance Compliance

### ☐ Constitutional requirements satisfied

**BUILD_PHILOSOPHY.md Compliance**:
- ✅ Phase 2 (RED QA) requirements met
- ✅ Zero Test Debt confirmed (no .skip(), .todo(), stubs)
- ✅ QA status is validly RED (not accidental GREEN)
- ✅ All architecture components tested
- ✅ Test failures are clear and specific

**DP-RED Registry Specification Compliance**:
- ✅ foreman/qa/dp-red-registry-spec.md rules enforced
- ✅ Intent classification mandatory
- ✅ Traceability mandatory for INTENTIONAL_RED
- ✅ Orphaned test prevention enforced
- ✅ Build gate logic validated

---

## XI. Sign-Off Checklist

Before progressing to Build-to-Green (Phase 3):

- [ ] All sections of this checklist are complete
- [ ] All validation commands run successfully
- [ ] Zero errors in validation reports
- [ ] All warnings addressed or documented
- [ ] Evidence artifacts generated and committed
- [ ] QA-to-Red completion approved by Foreman
- [ ] No orphaned tests exist
- [ ] All INTENTIONAL_RED tests mapped to Build-to-Green tasks

**Sign-Off Authority**: Foreman (Maturion)  
**Date**: ___________________  
**Validated By**: ___________________

---

## XII. References

**Authoritative Documents**:
- BUILD_PHILOSOPHY.md Phase 2: RED QA (Failing Tests)
- foreman/qa/dp-red-registry-spec.md
- foreman/qa/DP-RED-QUICK-REFERENCE.md
- foreman/scripts/validate-dp-red-compliance.py

**Related Checklists**:
- foreman/qa/fm-execution-checklist.md
- PLATFORM_READINESS_EVIDENCE_VERIFICATION_CHECKLIST.md

---

**Last Updated**: 2025-12-30  
**Version**: 1.0.0  
**Status**: Active and Enforced

---

*No orphaned or unexplained RED tests shall progress to Build-to-Green.*
