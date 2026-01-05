# QA Catalog Alignment Gate Specification (FM Repository)

**Version:** 1.0.0  
**Date:** 2026-01-05  
**Status:** ACTIVE (Mandatory)  
**Authority:** Derived from Governance PR #877 (maturion-foreman-governance)  
**Canonical Source:** `maturion-foreman-governance` Repository  
**FM Implementation:** This Document

---

## I. Purpose and Authority

### Canonical Grounding

This specification implements the **QA-Catalog-Alignment Gate Canon** from the governance repository (PR #877) within the FM repository context.

**Upstream Governance Authority:**
- Governance PR #877: "Canonize BL-018/BL-019: QA Catalog Alignment, BL Forward-Scan, and Second-Time Failure Prohibition"
- Source Document: `QA_CATALOG_ALIGNMENT_GATE_CANON.md` (governance repo)
- Architecture Completeness Requirements §3.14 (QA Catalog Alignment)

**This document translates canonical governance into FM-specific execution requirements.**

### Purpose

The QA-Catalog-Alignment Gate ensures that:

1. **Architecture → QA Catalog → QA-to-Red → Planning** sequence is enforced
2. All wave/subwave QA range assignments are **semantically valid**
3. QA ranges are **verified to exist** in `QA_CATALOG.md` before authorization
4. QA catalog entries **match the intended scope** of the work
5. **QA-to-Red tests exist** for all assigned QA ranges before builder appointment

This gate is **MANDATORY** and **BLOCKING**. FM MUST NOT authorize wave/subwave execution without passing this gate.

---

## II. Gate Trigger Points (When This Gate Runs)

FM MUST execute the QA-Catalog-Alignment Gate at the following decision points:

### A. Wave Planning Authorization
- **Trigger:** Before finalizing wave rollout plan
- **Scope:** All subwaves in the wave
- **Output:** PASS/FAIL for wave authorization

### B. Subwave Authorization
- **Trigger:** Before creating builder sub-issue or appointing builder
- **Scope:** Single subwave QA range
- **Output:** PASS/FAIL for subwave authorization

### C. QA Range Allocation
- **Trigger:** During wave planning when assigning QA ranges to subwaves
- **Scope:** Each QA range assignment
- **Output:** PASS/FAIL for QA range validity

### D. Post-BL Forward-Scan
- **Trigger:** After any BL/FL/CI that affects QA Catalog alignment
- **Scope:** All in-scope work (current and planned)
- **Output:** Identification of affected subwaves requiring correction

---

## III. Gate Checks (MANDATORY)

The QA-Catalog-Alignment Gate consists of the following checks:

### Check 1: QA Range Existence
**Question:** Does the QA range exist in `QA_CATALOG.md`?

**Procedure:**
1. Identify the QA range for the subwave (e.g., QA-043 to QA-057)
2. Open `QA_CATALOG.md`
3. Verify EVERY QA ID in the range is defined in the catalog
4. Verify no gaps in the range

**Pass Criteria:**
- ✅ All QA IDs in range are defined in `QA_CATALOG.md`
- ✅ No gaps in the sequence

**Fail Criteria:**
- ❌ Any QA ID in range is NOT defined in `QA_CATALOG.md`
- ❌ Gaps exist in the QA range

**On Failure:** BLOCK subwave authorization, escalate to FM for architecture/QA catalog extension

---

### Check 2: Semantic Alignment
**Question:** Do the QA catalog entries semantically match the subwave scope?

**Procedure:**
1. Read subwave description and intended scope (e.g., "Parking Station Advanced - Prioritization and Bulk Operations")
2. Read QA catalog entries for the assigned QA range
3. Verify semantic match between:
   - Subwave feature description
   - QA component descriptions
   - Architectural element being tested

**Pass Criteria:**
- ✅ QA catalog entries describe the same features as the subwave scope
- ✅ No semantic disconnect between subwave intent and QA descriptions

**Fail Criteria:**
- ❌ QA catalog entries describe different features (e.g., subwave is "Parking Advanced", QA range is "Network Failure Modes")
- ❌ Semantic mismatch between subwave and QA catalog

**On Failure:** BLOCK subwave authorization, escalate to FM for QA range reassignment or architecture correction

---

### Check 3: QA-to-Red Test Existence
**Question:** Do RED tests exist for all QA IDs in the range?

**Procedure:**
1. For each QA ID in the range:
   - Identify expected test file location per `QA_TO_RED_SUITE_SPEC.md`
   - Verify test file exists on disk
   - Verify test file contains test for this QA ID
2. Record test file locations

**Pass Criteria:**
- ✅ Test files exist for ALL QA IDs in range
- ✅ Test file locations are consistent with QA-to-Red spec
- ✅ Tests are RED (not yet implemented) per QA-to-Red semantics

**Fail Criteria:**
- ❌ ANY test file missing for QA IDs in range
- ❌ Test files exist but don't contain QA ID tests
- ❌ Tests are not in expected locations

**On Failure:** BLOCK subwave authorization, escalate to FM for QA-to-Red foundation completion

---

### Check 4: No QA ID Collisions
**Question:** Is the QA range allocated to only one subwave?

**Procedure:**
1. Review all subwave specifications in current wave
2. Identify all QA range assignments
3. Check for overlapping QA ranges

**Pass Criteria:**
- ✅ No QA ID is assigned to multiple subwaves
- ✅ No overlapping ranges

**Fail Criteria:**
- ❌ Same QA ID assigned to multiple subwaves
- ❌ Overlapping QA ranges

**On Failure:** BLOCK wave authorization, escalate to FM for QA range de-confliction

---

### Check 5: Architecture Alignment
**Question:** Does the architecture define the features covered by this QA range?

**Procedure:**
1. Identify architectural sections referenced by QA catalog entries
2. Verify architecture document (e.g., `TRUE_NORTH_FM_ARCHITECTURE.md`) contains:
   - Component definitions
   - Flow definitions
   - State definitions
   - Failure mode definitions
3. Verify architecture is FROZEN (not in draft)

**Pass Criteria:**
- ✅ Architecture document contains all referenced components/flows/states
- ✅ Architecture is marked FROZEN
- ✅ No architecture placeholders or TODOs in referenced sections

**Fail Criteria:**
- ❌ Architecture missing definitions for QA catalog entries
- ❌ Architecture is not frozen
- ❌ Architecture sections contain placeholders

**On Failure:** BLOCK subwave authorization, escalate to FM for architecture completion/freeze

---

## IV. Gate Outcomes

### Outcome: PASS
All checks pass. FM may proceed with:
- Finalizing subwave specification
- Creating builder sub-issue
- Appointing builder
- Authorizing Build-to-Green execution

**Evidence Required:**
- Gate execution checklist (all checks ✅)
- QA catalog verification log
- Test file existence verification
- Semantic alignment verification

---

### Outcome: FAIL
Any check fails. FM MUST:
1. **BLOCK** the subwave authorization
2. **STOP** wave progression at this point
3. **ESCALATE** to appropriate correction pathway:
   - Check 1 Failure → Extend QA Catalog
   - Check 2 Failure → Reassign QA range or correct architecture
   - Check 3 Failure → Complete QA-to-Red foundation
   - Check 4 Failure → De-conflict QA ranges
   - Check 5 Failure → Complete/freeze architecture
4. **REGISTER FL/CI** entry documenting the failure
5. **CORRECT** the structural gap before retry
6. **RE-RUN** the gate after correction

**FM MUST NOT:**
- Proceed with appointment despite gate failure
- Delegate structural gap correction to builders
- Assume builders will "figure it out"
- Create issues with invalid foundational assumptions

---

## V. FM Responsibilities

### Before Wave Planning
1. Verify architecture is complete and frozen
2. Verify QA Catalog is extended (if new features added)
3. Verify QA-to-Red tests exist for all catalog entries

### During Wave Planning
1. Execute QA-Catalog-Alignment Gate for each subwave QA range assignment
2. Document gate execution results
3. BLOCK wave finalization if any subwave fails gate

### Before Builder Appointment
1. Re-verify QA-Catalog-Alignment Gate for assigned subwave
2. Include gate verification evidence in appointment
3. STOP if gate no longer passes

### After BL/FL/CI Discovery
1. Execute forward-scan to identify all affected subwaves
2. Re-run QA-Catalog-Alignment Gate for affected subwaves
3. BLOCK execution of affected subwaves until corrections complete

---

## VI. Builder Expectations

Builders MUST expect that FM has passed the QA-Catalog-Alignment Gate before appointment.

**Builders MUST:**
- Verify gate evidence is included in appointment
- Verify QA range exists and matches subwave scope
- Verify QA-to-Red tests exist before starting Build-to-Green
- Declare BLOCKED if gate preconditions are not met

**Builders MUST NOT:**
- Proceed without gate verification
- "Invent" missing QA components
- "Assume" QA catalog alignment
- Implement without QA-to-Red foundation

**On Discovery of Gate Failure:**
Builders must immediately:
1. STOP work
2. Declare BLOCKED in the issue
3. Escalate to FM with evidence
4. Wait for FM structural correction

---

## VII. Relationship to BL-018 and BL-019

This gate was created in response to:

- **BL-018:** Wave 2.2 QA Catalog Misalignment (first-time failure)
- **BL-019:** Wave 2.3+ QA Catalog Semantic Misalignment (second-time failure - CATASTROPHIC)

**Lessons Learned:**
1. Wave planning MUST verify QA catalog alignment before authorization
2. QA range assignment without verification leads to structural blocks
3. Builders correctly STOP when preconditions are not met
4. FM must execute forward-scan after BL discovery to find all affected work

**Prevention:**
This gate, when executed correctly, prevents:
- Invalid QA range assignments
- Semantic mismatches between subwave intent and QA catalog
- Missing QA-to-Red foundations
- Builder appointments with invalid preconditions

---

## VIII. Enforcement and Compliance

### Constitutional Status
This gate is **MANDATORY** per:
- T0-001: BUILD_PHILOSOPHY.md (Architecture → QA-to-Red → Planning sequence)
- T0-013: FM_EXECUTION_MANDATE.md (FM planning authority and sequencing)
- Governance PR #877: QA-Catalog-Alignment Gate Canon

### Enforcement Mechanism
- FM Agent Contract (Section XIV - Mandatory Sequencing) requires gate execution
- Builder Agent Contracts require gate verification before accepting appointment
- PR gates MAY verify gate execution evidence in builder sub-issues

### Non-Compliance
Failure to execute this gate is a **constitutional violation** and will result in:
- BL/FL/CI entry documenting the failure
- Governance ratchet creation
- Potential Wave execution halt
- Emergency corrective action if repeated

---

## IX. Automation and Tooling

### Current State (Manual)
Gate execution is currently MANUAL:
- FM manually verifies QA catalog entries
- FM manually checks test file existence
- FM manually verifies semantic alignment

### Future State (Automated)
Potential automation:
1. **QA Range Validator Script:** Verify QA range exists in QA_CATALOG.md
2. **Semantic Alignment Checker:** AI-powered semantic match verification
3. **Test Existence Verifier:** Automated test file location and content check
4. **Gate Execution Dashboard:** Real-time gate status for all subwaves

Automation MUST NOT:
- Replace FM judgment on semantic alignment
- Bypass gate execution
- Auto-pass gate without verification

---

## X. References

### Upstream Governance
- **Governance PR #877:** Canonization of BL-018/BL-019 learnings
- **QA_CATALOG_ALIGNMENT_GATE_CANON.md:** Canonical gate definition (governance repo)
- **ARCHITECTURE_COMPLETENESS_REQUIREMENTS.md §3.14:** QA Catalog Alignment requirement
- **BUILD_PHILOSOPHY.md:** Architecture → QA-to-Red → Planning sequence

### FM Repository Documents
- **QA_CATALOG.md:** Authoritative QA component index
- **QA_TO_RED_SUITE_SPEC.md:** RED/GREEN semantics and test locations
- **TRUE_NORTH_FM_ARCHITECTURE.md:** Frozen architecture specification
- **BL_FORWARD_SCAN_OBLIGATION_SPEC.md:** Forward-scan execution protocol
- **SECOND_TIME_FAILURE_PROHIBITION_SPEC.md:** Second-time failure handling

### Related Learnings
- **BL-018:** Wave 2.2 QA Catalog Misalignment (first-time failure)
- **BL-019:** Wave 2.3+ QA Catalog Semantic Misalignment (second-time failure)
- **BL-020:** Missing Test Suite in Subwave Assignment (similar pattern)

---

## XI. Version History

**v1.0.0 (2026-01-05):**
- Initial creation
- Layered down from governance PR #877
- Addresses BL-018 and BL-019 learnings
- Mandatory gate for all wave/subwave planning

---

**Document Owner:** Maturion Foreman (FM)  
**Maintenance:** Governance updates from canonical source  
**Status:** ACTIVE — All wave planning MUST execute this gate
