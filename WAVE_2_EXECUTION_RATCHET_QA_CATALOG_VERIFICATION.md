# Wave 2 Execution Ratchet — QA Catalog Verification Checklist

**Version:** 1.0.0  
**Date:** 2026-01-05  
**Authority:** FM Execution Mandate (T0-013), Bootstrap Learning BL-018  
**Status:** MANDATORY — Activated for Wave 2 and All Future Waves  
**Purpose:** Prevent QA-to-Red precondition gaps in wave planning

---

## Purpose

This document defines **mandatory QA Catalog verification requirements** for all wave planning and subwave assignment activities. It implements the structural ratchet from Bootstrap Learning BL-018 (Wave 2.2 QA Catalog Misalignment).

**Constitutional Authority:** FM Agent Contract Section XIV (Mandatory Sequencing)

**Rationale:** Wave 2.2 (Parking Station Advanced) was planned with QA-376 to QA-385 as the assigned QA range, but these QA IDs were already allocated to Network and Resource Failure Modes. This catastrophic planning failure blocked Wave 2 execution and required complete structural correction.

---

## Mandatory Verification Checklist

### Before Creating ANY Subwave Sub-Issue File

FM (or delegated planning authority) MUST complete this checklist before generating subwave sub-issue files or creating GitHub issues:

```
SUBWAVE PLANNING VERIFICATION CHECKLIST
Subwave: ______  Wave: ______  Date: ______

ARCHITECTURE VERIFICATION:
- [ ] Architecture section for this subwave exists in TRUE_NORTH_FM_ARCHITECTURE.md
- [ ] Architecture section is complete and frozen (no TBD/TODO items)
- [ ] All component contracts, data flows, and integration points are defined
- [ ] Architecture version and freeze date recorded: __________

QA CATALOG VERIFICATION:
- [ ] QA range assigned to this subwave: QA-___ to QA-___
- [ ] All QA IDs in range VERIFIED to exist in QA_CATALOG.md
- [ ] All QA definitions VERIFIED to match subwave intent
- [ ] NO QA ID collisions detected with existing allocations
- [ ] QA_CATALOG.md version verified: __________

QA DEFINITION ALIGNMENT:
- [ ] Each QA component description matches intended feature scope
- [ ] QA component counts match subwave scope (e.g., 10 QA for 10 features)
- [ ] QA components are correctly categorized (component/flow/state/failure)
- [ ] QA traceability to architecture confirmed

QA-TO-RED PRECONDITION:
- [ ] QA-to-Red test files exist in tests/wave<N>_qa_infrastructure/
- [ ] Test file naming matches QA range (e.g., test_parking_station_advanced_*.py)
- [ ] All tests are RED (verified by test run)
- [ ] Test RED status is "not implemented" (not broken/invalid)
- [ ] Test execution command documented: __________

BUILDER APPOINTMENT VALIDATION:
- [ ] Builder assigned to subwave has capability for feature type
- [ ] Builder contract scope includes subwave features
- [ ] Workload limits observed (max 20 QA, qa-builder max 15)
- [ ] Checkpoint requirements determined (>10 QA = checkpoint at 50%)

DEPENDENCY VERIFICATION:
- [ ] All prerequisite subwaves identified
- [ ] All prerequisite subwave QA ranges verified
- [ ] Dependency chain validated against Wave Rollout Plan
- [ ] No circular dependencies detected

GOVERNANCE ALIGNMENT:
- [ ] BUILD_PHILOSOPHY.md principles observed
- [ ] FM Agent Contract Section XIV sequencing followed
- [ ] Bootstrap Learnings (BL-016, BL-017, BL-018) applied
- [ ] Governance canon requirements layered down

DOCUMENTATION COMPLETENESS:
- [ ] Subwave sub-issue file contains all 6 mandatory elements:
      1. Scope Statement
      2. Architecture References
      3. QA-to-Red Confirmation
      4. Execution State Discipline
      5. Evidence Requirements
      6. Governance References
- [ ] Sub-issue file references correct Wave Plan and Implementation Plan
- [ ] Sub-issue file contains correct QA range and definitions

APPROVAL:
- [ ] Verification completed by: __________
- [ ] Verification date: __________
- [ ] Approved by FM: [ ] YES  [ ] PENDING
```

---

## Verification Process

### Step 1: Architecture Completeness Check

**Before assigning QA ranges:**
1. Review TRUE_NORTH_FM_ARCHITECTURE.md for the feature set
2. Confirm architecture section is complete and frozen
3. If architecture gap exists, STOP and extend architecture first
4. Record architecture version and freeze date

### Step 2: QA Catalog Range Selection

**Before assigning QA IDs:**
1. Review QA_CATALOG.md to identify next available QA range
2. Verify QA IDs are NOT already allocated
3. Verify QA count matches feature count (e.g., 10 features = 10 QA)
4. Reserve QA range and record in planning document

### Step 3: QA Catalog Extension (If Needed)

**If QA components do not exist for subwave features:**
1. Extend TRUE_NORTH_FM_ARCHITECTURE.md with feature definitions (if not already complete)
2. Extend QA_CATALOG.md with new QA components:
   - Assign sequential QA IDs (next available from catalog)
   - Write QA component descriptions matching architecture
   - Categorize QA components correctly (component/flow/state/failure)
   - Update QA_CATALOG.md version and date
3. Commit QA_CATALOG.md update before proceeding

### Step 4: QA-to-Red Test Creation

**Before builder assignment:**
1. Create test files in tests/wave<N>_qa_infrastructure/
2. Implement RED tests for all assigned QA components
3. Verify tests are RED with "not implemented" status
4. Run tests and confirm expected RED state
5. Commit tests before sub-issue creation

### Step 5: QA Range Verification

**Before generating sub-issue file:**
1. Cross-reference assigned QA range with QA_CATALOG.md
2. Verify each QA ID exists and matches subwave intent
3. Verify no QA ID collisions
4. Document verification results in checklist

### Step 6: Sub-Issue Generation

**Only after Steps 1-5 complete:**
1. Generate subwave sub-issue file with verified QA range
2. Include correct QA definitions from QA_CATALOG.md
3. Reference correct test file locations
4. Complete all 6 mandatory builder appointment elements

### Step 7: Final Validation

**Before GitHub issue creation:**
1. Review completed verification checklist
2. Confirm ALL checklist items are satisfied
3. Obtain FM approval
4. Create GitHub issue with verified sub-issue content

---

## Enforcement Mechanism

### Validation Gate

This checklist is a **mandatory gate** in the wave planning process. No subwave sub-issue file may be created without completing this checklist.

**Gate Owner:** Maturion Foreman (FM)

**Gate Status:**
- **PASS:** All checklist items satisfied, FM approval obtained
- **FAIL:** Any checklist item unsatisfied, sub-issue creation blocked

### Automated Validation (Future)

**Recommended Automation:**
1. Script to validate QA ranges against QA_CATALOG.md
2. Test existence verification for assigned QA ranges
3. Test RED status verification before builder assignment
4. Checklist completion validation before issue creation

### Audit Trail

**Required Documentation:**
1. Completed verification checklist for each subwave
2. QA_CATALOG.md version reference for each subwave
3. Architecture freeze date reference for each subwave
4. Test execution logs showing RED status
5. FM approval signature for each subwave

---

## Application to Wave 2

### Immediate Actions (Wave 2 Remaining Subwaves)

**Before authorizing any remaining Wave 2 subwaves (2.3 to 2.14):**

1. **Audit All Subwave QA Ranges:**
   - Verify QA-341 to QA-400 allocations in QA_CATALOG.md
   - Confirm QA definitions match subwave intents
   - Identify any additional QA misalignments

2. **Correct Any Misalignments:**
   - Update sub-issue files with correct QA ranges
   - Extend QA_CATALOG.md if needed
   - Create missing QA-to-Red tests
   - Regenerate affected sub-issue files

3. **Complete Verification Checklists:**
   - One checklist per subwave (2.3 to 2.14)
   - Archive completed checklists in evidence/wave-2.0/planning/
   - Obtain FM approval for each subwave

4. **Update Wave 2 Plans:**
   - Update WAVE_2_ROLLOUT_PLAN.md with verified QA ranges
   - Update WAVE_2_IMPLEMENTATION_PLAN.md with corrected scope
   - Update WAVE_2_BUILDER_SUB_ISSUES_COMPLETION_REPORT.md

### Subwave 2.2 Specific Actions

**Pending FM Decision (Option A, B, or C):**

**If Option A (Parking Station Advanced IS Wave 2 Scope):**
1. Extend TRUE_NORTH_FM_ARCHITECTURE.md with parking advanced section
2. Extend QA_CATALOG.md with QA-401 to QA-410 (parking advanced components)
3. Implement QA-to-Red tests for QA-401 to QA-410
4. Complete verification checklist for Subwave 2.2 (revised)
5. Regenerate SUBWAVE_2.2_UI_BUILDER_PARKING_STATION_ADVANCED.md with QA-401 to QA-410
6. Update issue #398 with corrected scope
7. Obtain FM approval
8. Authorize builder to proceed

**If Option B or C (Remove/Defer Subwave 2.2):**
1. Remove Subwave 2.2 from WAVE_2_ROLLOUT_PLAN.md
2. Close issue #398 with rationale
3. Update Wave 2 sequencing (Subwave 2.3 depends on 2.1, not 2.2)
4. Proceed with remaining subwaves (2.3 to 2.14)

---

## Application to Future Waves (Wave 3+)

### Wave Planning Process (Constitutional Order)

**Mandatory Sequence:**
```
1. Architecture Definition
   - Define all Wave N features in TRUE_NORTH_FM_ARCHITECTURE.md
   - Freeze architecture before QA Catalog extension

2. QA Catalog Extension
   - Extend QA_CATALOG.md with QA components for Wave N features
   - Assign sequential QA IDs (next available)
   - Categorize QA components correctly

3. QA-to-Red Compilation
   - Implement RED tests for all Wave N QA components
   - Verify tests are RED with "not implemented" status
   - Commit tests before wave planning

4. Wave Planning and Subwave Assignment
   - Assign QA ranges to subwaves based on QA_CATALOG.md
   - Complete verification checklist for each subwave
   - Generate sub-issue files with verified QA ranges

5. Builder Appointment and Execution
   - Create GitHub issues with verified sub-issue content
   - Assign builders with complete appointment packages
   - Authorize execution only after all preconditions satisfied
```

**PROHIBITED:** Skipping any step or proceeding out of order.

### Continuous Improvement

**After Each Wave:**
1. Review verification checklist effectiveness
2. Identify additional verification items if needed
3. Update checklist based on learnings
4. Automate verification steps where possible

---

## Related Documents

- **ROOT_CAUSE_ANALYSIS_WAVE_2_2_BLOCK.md** — Detailed RCA for Wave 2.2 failure
- **BOOTSTRAP_EXECUTION_LEARNINGS.md** — BL-018 learning entry
- **FLCI_REGISTRY_UPDATE_BL_018.md** — FL/CI registry entry
- **FM Agent Contract Section XIV** — Mandatory sequencing requirements
- **BUILD_PHILOSOPHY.md** — One-Time Build and QA-to-Red principles
- **QA_CATALOG.md** — Canonical QA component index
- **TRUE_NORTH_FM_ARCHITECTURE.md** — Frozen architecture baseline

---

## Status

**Checklist Status:** ✅ ACTIVE — Mandatory for Wave 2 and All Future Waves  
**Enforcement:** ✅ Immediate — Applies to all remaining Wave 2 subwaves (2.3 to 2.14)  
**Authority:** FM Execution Mandate (T0-013), Bootstrap Learning BL-018  
**Version:** 1.0.0  
**Last Updated:** 2026-01-05  
**Maintained By:** Maturion Foreman (FM)

---

**END WAVE 2 EXECUTION RATCHET — QA CATALOG VERIFICATION CHECKLIST**
