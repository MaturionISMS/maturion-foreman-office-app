# FM Pre-Authorization Checklist Specification

**Version:** 1.0.0  
**Date:** 2026-01-07  
**Status:** ACTIVE (Mandatory)  
**Authority:** Derived from Governance PR #879 (maturion-foreman-governance)  
**Canonical Source:** `FM_PREAUTH_CHECKLIST_CANON.md` (maturion-foreman-governance)  
**FM Implementation:** This Document

---

## I. Purpose and Authority

### Canonical Grounding

This specification implements the **FM Pre-Authorization Checklist Canon** from the governance repository (PR #879) within the FM repository context.

**Upstream Governance Authority:**
- Governance PR #879: "Canonize FM Pre-Authorization Checklist (BL-020 structural fix)"
- Source Document: `FM_PREAUTH_CHECKLIST_CANON.md` (governance repo)
- Build Philosophy v1.3 – No Second-Time Failures
- BL-018/BL-019/BL-020 Failure Pattern Prevention

**This document translates canonical governance into FM-specific execution requirements.**

### Purpose

The FM Pre-Authorization Checklist ensures that FM does **NOT authorize wave/subwave execution or builder appointments without verifying mandatory prerequisites**.

**Root Cause Addressed:**
- BL-018: FM verified specs but not QA Catalog
- BL-019: FM verified QA Catalog IDs but not semantics  
- BL-020: FM verified QA Catalog but not actual test files
- **Pattern:** FM planning operated on documentation without verifying repository artifacts

**Prevention Strategy:**
Before ANY authorization, FM MUST verify:
1. Documentation (specs, plans, QA Catalog) exists AND
2. Repository artifacts (test files, architecture specs) exist AND
3. Semantic alignment between intent and reality

---

## II. When FM Must Execute This Checklist

FM **MUST** execute this checklist at the following decision points:

### A. Wave Authorization
- **Trigger:** Before marking a wave as "READY FOR AUTHORIZATION"
- **Scope:** All subwaves in the wave
- **Output:** PASS/FAIL for entire wave

### B. Subwave Authorization
- **Trigger:** Before marking a subwave as "READY FOR AUTHORIZATION"
- **Scope:** Single subwave
- **Output:** PASS/FAIL for subwave authorization

### C. Builder Appointment
- **Trigger:** Before creating or issuing ANY builder sub-issue (qa-builder, ui-builder, api-builder, schema-builder, integration-builder)
- **Scope:** The specific subwave being assigned to builder
- **Output:** PASS/FAIL for builder appointment

### D. Re-Authorization After BL/FL-CI Correction
- **Trigger:** After any BL/FL-CI issue that blocks work has been resolved
- **Scope:** The work that was previously blocked
- **Output:** PASS/FAIL for re-authorization

### E. Post-Ratchet Verification
- **Trigger:** After applying any governance ratchet (BL-018/019/020 style)
- **Scope:** All in-scope work that might be affected by the ratchet
- **Output:** Identification of work requiring correction before authorization

---

## III. The Five Mandatory Checks

FM **MUST** execute ALL five checks. Each check has explicit PASS/FAIL semantics.

### Check 1: QA Catalog Alignment

**Question:** Are the QA range assignments semantically valid and properly defined in QA_CATALOG.md?

**What FM Must Verify:**

1. **QA Range Existence:**
   - Open `QA_CATALOG.md`
   - Verify EVERY QA ID in the subwave's assigned range (e.g., QA-211 to QA-225) is defined in the catalog
   - Verify no gaps in the range

2. **Semantic Alignment:**
   - Read subwave description and intended scope (e.g., "Advanced Flow Scenarios")
   - Read QA catalog entries for the assigned QA range
   - Verify semantic match between:
     - Subwave feature description
     - QA component descriptions in catalog
     - Architectural element being tested

3. **No QA ID Collisions:**
   - Verify the QA range is NOT assigned to any other subwave
   - Verify no overlap with previously completed or in-flight work

**PASS Criteria:**
- ✅ All QA IDs in range exist in `QA_CATALOG.md`
- ✅ No gaps in the sequence
- ✅ Semantic alignment verified (subwave name/scope matches QA definitions)
- ✅ No QA ID collisions with other subwaves

**FAIL Criteria:**
- ❌ Any QA ID in range is NOT defined in `QA_CATALOG.md`
- ❌ Gaps exist in the QA range
- ❌ Semantic mismatch (e.g., subwave called "Analytics" but QA IDs describe "Flow Scenarios")
- ❌ QA ID collision detected

**On FAIL:**
- FM MUST STOP authorization
- FM MUST correct QA_CATALOG.md or subwave scope definition
- FM MUST re-execute checklist after correction

**Example (BL-020 Prevention):**
```
Subwave: "Advanced Flow Scenarios"
QA Range: QA-211 to QA-225

Check 1.1 — QA Range Existence: PASS (all IDs exist in QA_CATALOG.md)
Check 1.2 — Semantic Alignment: 
  - Subwave scope: "User Intent → Build Execution Flow Advanced"
  - QA-211 definition: "User Intent → Build Execution Flow Advanced (Happy Path)"
  - QA-212 definition: "User Intent → Build Execution Flow Advanced (Error Handling)"
  - Result: PASS (semantic match verified)
Check 1.3 — No Collisions: PASS (QA-211-225 not assigned elsewhere)

Result: PASS
```

---

### Check 2: QA-to-Red Foundation

**Question:** Do the actual test files exist in the repository for the assigned QA range?

**What FM Must Verify:**

1. **Test File Existence:**
   - Identify the expected test file location (e.g., `tests/wave2_0_qa_infrastructure/test_advanced_flow_scenarios.py`)
   - Verify the file EXISTS in the repository (not just in documentation)
   - Verify the file is readable and contains Python test code

2. **Test Function Existence:**
   - Open the test file
   - Verify a test function exists for EVERY QA ID in the range
   - Verify test function names match QA IDs (e.g., `test_qa_211`, `test_qa_212`, etc.)

3. **RED State Verification:**
   - Verify each test function is implemented (not just a placeholder comment)
   - Verify each test raises `NotImplementedError` or similar (RED state)
   - Verify tests are NOT skipped, marked as TODO, or commented out

**PASS Criteria:**
- ✅ Test file exists at expected location
- ✅ All QA IDs have corresponding test functions
- ✅ All tests are in RED state (NotImplementedError or equivalent)
- ✅ Zero test debt (no skipped/commented/incomplete tests)

**FAIL Criteria:**
- ❌ Test file does NOT exist
- ❌ Test file exists but missing test functions for some QA IDs
- ❌ Tests are not in RED state (already GREEN or broken)
- ❌ Test debt detected (skipped, commented, incomplete tests)

**On FAIL:**
- FM MUST STOP authorization
- FM MUST create missing test files/functions
- FM MUST correct test debt
- FM MUST re-execute checklist after correction

**Example (BL-020 Direct Prevention):**
```
Subwave: "Advanced Flow Scenarios"
QA Range: QA-211 to QA-225
Expected File: tests/wave2_0_qa_infrastructure/test_advanced_flow_scenarios.py

Check 2.1 — File Existence: 
  $ ls tests/wave2_0_qa_infrastructure/test_advanced_flow_scenarios.py
  tests/wave2_0_qa_infrastructure/test_advanced_flow_scenarios.py
  Result: PASS (file exists)

Check 2.2 — Test Function Existence:
  $ grep "def test_qa_" tests/wave2_0_qa_infrastructure/test_advanced_flow_scenarios.py | wc -l
  15
  Result: PASS (15 test functions for 15 QA IDs)

Check 2.3 — RED State Verification:
  $ pytest tests/wave2_0_qa_infrastructure/test_advanced_flow_scenarios.py -v --tb=no
  FAILED test_qa_211 - NotImplementedError
  FAILED test_qa_212 - NotImplementedError
  ...
  FAILED test_qa_225 - NotImplementedError
  Result: PASS (all tests RED with NotImplementedError)

Result: PASS
```

---

### Check 3: Architecture Alignment

**Question:** Is the architecture for this wave/subwave frozen, complete, and accessible?

**What FM Must Verify:**

1. **Architecture Document Existence:**
   - Identify the architecture document for the wave (e.g., `FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md`)
   - Verify the document EXISTS
   - Verify the document is marked as FROZEN or COMPLETE

2. **Subwave Scope Coverage:**
   - Verify the architecture document covers the subwave scope
   - Verify component specifications exist for all features in the subwave
   - Verify integration points are documented

3. **Architecture-QA Traceability:**
   - Verify QA Catalog entries reference architecture components
   - Verify architecture components have corresponding QA coverage
   - Verify no orphaned QA IDs or architecture components

**PASS Criteria:**
- ✅ Architecture document exists and is frozen
- ✅ Subwave scope fully covered in architecture
- ✅ Architecture-QA traceability verified
- ✅ No orphaned components or QA IDs

**FAIL Criteria:**
- ❌ Architecture document does NOT exist or is incomplete
- ❌ Architecture not frozen (still in draft/planning state)
- ❌ Subwave scope not covered in architecture
- ❌ Traceability gaps detected

**On FAIL:**
- FM MUST STOP authorization
- FM MUST complete/freeze architecture
- FM MUST correct traceability gaps
- FM MUST re-execute checklist after correction

**Example:**
```
Wave: 2.0
Subwave: "Advanced Flow Scenarios"
Architecture Doc: FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md

Check 3.1 — Document Existence: PASS (document exists and marked COMPLETE)
Check 3.2 — Scope Coverage: 
  - Subwave features: Flow Scenarios Advanced (Intent → Build → Evidence → Handover)
  - Architecture sections: §5.3 "User Intent Flow", §5.4 "Build Execution Flow"
  - Result: PASS (scope covered)
Check 3.3 — Traceability:
  - QA-211: Maps to §5.3.1 "User Intent Submission"
  - QA-212: Maps to §5.3.2 "Intent Validation"
  - Result: PASS (all QA IDs traceable)

Result: PASS
```

---

### Check 4: BL/FL-CI Ratchet Status

**Question:** Are all applicable BL/FL-CI ratchets applied to this work?

**What FM Must Verify:**

1. **Active Ratchet Identification:**
   - Review `BOOTSTRAP_EXECUTION_LEARNINGS.md` for all active BL entries
   - Review FL/CI registry for active FL/CI entries
   - Identify ratchets applicable to current wave/subwave

2. **Ratchet Application Verification:**
   - For each applicable ratchet (e.g., BL-018, BL-019, BL-020):
     - Verify the ratchet requirement is implemented
     - Verify evidence of compliance exists
     - Verify no regression of the ratchet

3. **Pattern Scan Completion:**
   - If any BL/FL-CI required forward-scan:
     - Verify scan was executed
     - Verify all instances corrected
     - Verify evidence recorded

**PASS Criteria:**
- ✅ All applicable ratchets identified
- ✅ All ratchets applied and verified
- ✅ Pattern scans complete where required
- ✅ Evidence of compliance exists

**FAIL Criteria:**
- ❌ Applicable ratchet NOT applied
- ❌ Ratchet regression detected
- ❌ Pattern scan incomplete or missing
- ❌ No evidence of compliance

**On FAIL:**
- FM MUST STOP authorization
- FM MUST apply missing ratchets
- FM MUST complete pattern scans
- FM MUST re-execute checklist after correction

**Example:**
```
Subwave: "Advanced Flow Scenarios" (Subwave 2.5)
Active Ratchets: BL-018, BL-019, BL-020

Check 4.1 — BL-018 (QA Range Existence):
  - Requirement: Verify QA range exists in QA_CATALOG.md
  - Evidence: Check 1 above (QA Catalog Alignment)
  - Result: PASS (applied via Check 1)

Check 4.2 — BL-019 (Semantic Alignment):
  - Requirement: Verify QA definitions match subwave scope
  - Evidence: Check 1.2 above (Semantic Alignment)
  - Result: PASS (applied via Check 1)

Check 4.3 — BL-020 (Test File Existence):
  - Requirement: Verify test files exist in repository
  - Evidence: Check 2 above (QA-to-Red Foundation)
  - Result: PASS (applied via Check 2)

Result: PASS
```

---

### Check 5: Dependency Gates

**Question:** Are all prerequisite subwaves/gates passed for this work?

**What FM Must Verify:**

1. **Dependency Identification:**
   - Identify all dependency gates for the subwave (e.g., GATE-SUBWAVE-2.3, GATE-SUBWAVE-2.4)
   - Verify dependencies are documented in Wave rollout plan

2. **Gate Status Verification:**
   - For each dependency gate:
     - Verify the gate has been executed
     - Verify the gate status is PASS
     - Verify gate evidence exists

3. **Sequence Enforcement:**
   - Verify correct build sequence (no parallel execution where sequential required)
   - Verify no circular dependencies

**PASS Criteria:**
- ✅ All dependencies identified
- ✅ All dependency gates PASS
- ✅ Gate evidence exists
- ✅ Correct sequence enforced

**FAIL Criteria:**
- ❌ Dependency gate NOT executed
- ❌ Dependency gate status is FAIL or PENDING
- ❌ Missing gate evidence
- ❌ Sequence violation detected

**On FAIL:**
- FM MUST STOP authorization
- FM MUST wait for dependency gates to PASS
- FM MUST NOT authorize until dependencies satisfied

**Example:**
```
Subwave: 2.5 "Advanced Flow Scenarios"
Dependencies: GATE-SUBWAVE-2.3 (System Optimizations Phase 1), GATE-SUBWAVE-2.4 (System Optimizations Phase 2)

Check 5.1 — GATE-SUBWAVE-2.3:
  - Status: PASS (verified in WAVE_2.3_BUILDER_COMPLETION_REPORT.md)
  - Evidence: evidence/wave-2.0/api-builder/subwave-2.3/qa_test_results.xml (10/10 GREEN)
  - Date: 2026-01-04
  - Result: PASS

Check 5.2 — GATE-SUBWAVE-2.4:
  - Status: PASS (verified in WAVE_2.4_BUILDER_QA_REPORT.md)
  - Evidence: evidence/wave-2.0/integration-builder/subwave-2.4/qa_test_results.xml (10/10 GREEN)
  - Date: 2026-01-05
  - Result: PASS

Result: PASS
```

---

## IV. Checklist Outcome Rules

### PASS Outcome

**Condition:** ALL five checks PASS

**FM Authorization:**
- ✅ FM **MAY** proceed with authorization
- ✅ FM **MAY** mark wave/subwave as "READY FOR AUTHORIZATION"
- ✅ FM **MAY** create/issue builder sub-issue
- ✅ FM **MAY** appoint builder

**FM Obligation:**
- FM MUST record checklist execution (see Section V)
- FM MUST include checklist evidence in authorization decision

### FAIL Outcome

**Condition:** ANY check FAILS

**FM Authorization:**
- ❌ FM **MUST NOT** proceed with authorization
- ❌ FM **MUST NOT** mark wave/subwave as "READY FOR AUTHORIZATION"
- ❌ FM **MUST NOT** create/issue builder sub-issue
- ❌ FM **MUST NOT** appoint builder

**FM Obligation:**
- FM MUST STOP authorization immediately
- FM MUST treat work as BLOCKED
- FM MUST open or update an FM/BL/FL-CI issue documenting:
  - Which check(s) failed
  - Root cause
  - Corrective action required
  - Timeline for correction
- FM MUST correct foundations (architecture, QA Catalog, test files, etc.)
- FM MUST re-execute complete checklist after correction
- FM MUST NOT skip failed checks or proceed with "partial PASS"

### BLOCKED State Semantics

When checklist FAILS:
- Work enters BLOCKED state
- Builder appointment is PROHIBITED
- Authorization is PROHIBITED
- Resolution MUST be via FM governance/architecture/QA correction
- No builder-side workarounds permitted

---

## V. Evidence Recording Convention

### Purpose

FM MUST create evidence of checklist execution to:
- Demonstrate governance compliance
- Enable audit and retrospective analysis
- Prevent future authorization gaps
- Support BL/FL-CI prevention

### Evidence Format

For each wave/subwave authorization, FM SHOULD create:

**Option 1: Standalone Report File**
- Location: `governance/reports/waves/FM_PREAUTH_CHECKLIST_WAVE_X_SUBWAVE_Y.md`
- Format: Markdown checklist

**Option 2: Section in Wave Document**
- Location: Within relevant WAVE_X_ROLLOUT_PLAN.md or SUBWAVE_X.Y_SPEC.md
- Format: Markdown section with checklist

### Evidence Content (Minimum Required)

```markdown
## FM Pre-Authorization Checklist — [Wave X] [Subwave Y] [Subwave Name]

**Date:** YYYY-MM-DD  
**FM Executor:** [Agent name or role]  
**Authorization Decision:** PASS / FAIL

### Check 1: QA Catalog Alignment
- [x] 1.1 QA Range Existence: PASS / FAIL
- [x] 1.2 Semantic Alignment: PASS / FAIL
- [x] 1.3 No QA ID Collisions: PASS / FAIL
- **Result:** PASS / FAIL

### Check 2: QA-to-Red Foundation
- [x] 2.1 Test File Existence: PASS / FAIL
- [x] 2.2 Test Function Existence: PASS / FAIL
- [x] 2.3 RED State Verification: PASS / FAIL
- **Result:** PASS / FAIL

### Check 3: Architecture Alignment
- [x] 3.1 Document Existence: PASS / FAIL
- [x] 3.2 Scope Coverage: PASS / FAIL
- [x] 3.3 Traceability: PASS / FAIL
- **Result:** PASS / FAIL

### Check 4: BL/FL-CI Ratchet Status
- [x] 4.1 Active Ratchet Identification: PASS / FAIL
- [x] 4.2 Ratchet Application Verification: PASS / FAIL
- [x] 4.3 Pattern Scan Completion: PASS / FAIL
- **Result:** PASS / FAIL

### Check 5: Dependency Gates
- [x] 5.1 Dependency Identification: PASS / FAIL
- [x] 5.2 Gate Status Verification: PASS / FAIL
- [x] 5.3 Sequence Enforcement: PASS / FAIL
- **Result:** PASS / FAIL

---

**Overall Checklist Result:** PASS / FAIL

**Authorization Decision:**
- [If PASS] Subwave X.Y authorized for [builder] appointment.
- [If FAIL] Authorization BLOCKED until [specific issue] is resolved.

**Evidence References:**
- QA Catalog: `QA_CATALOG.md` (lines X-Y)
- Test Files: `tests/wave2_0_qa_infrastructure/test_*.py`
- Architecture: `FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md` (§Z)
- Dependency Gates: `WAVE_X.Y_BUILDER_COMPLETION_REPORT.md`
```

### Evidence Timing

- **Created:** BEFORE authorization decision is made
- **Reviewed:** As part of authorization decision process
- **Persisted:** Committed to repository
- **Referenced:** In builder sub-issue or wave documentation

---

## VI. Enforcement and Compliance

### Mandatory Execution

This checklist is **MANDATORY** and **NON-OPTIONAL**.

FM **MUST NOT**:
- Skip checklist execution
- Assume checklist items are satisfied based on documentation alone
- Authorize work with "partial PASS" (e.g., 4 out of 5 checks passed)
- Bypass checklist for "urgent" or "low-risk" work
- Delegate checklist execution to builders

FM **MUST**:
- Execute checklist for EVERY authorization decision
- Verify repository artifacts, not just documentation
- Record checklist evidence
- STOP on FAIL and correct foundations

### Integration with FM Agent Contract

This checklist is bound into the FM agent contract via:
- `.github/agents/ForemanApp-agent.md` — FM Pre-Authorization Checklist Binding section

FM agent contract makes this checklist **constitutionally binding**.

### Integration with BL/FL-CI Prevention

This checklist implements prevention for:
- **BL-018:** QA Range Existence (Check 1.1)
- **BL-019:** Semantic Alignment (Check 1.2)
- **BL-020:** Test File Existence (Check 2)

This checklist is the **governance ratchet** preventing recurrence of these patterns.

### Audit and Verification

- FM governance reviews may audit checklist execution
- Missing checklist evidence = governance violation
- Incomplete checklist execution = governance violation
- Authorization without checklist = constitutional violation

---

## VII. Relationship to Other Governance

### Relationship to QA Catalog Alignment Gate

The **QA Catalog Alignment Gate** (governance/specs/QA_CATALOG_ALIGNMENT_GATE_SPEC.md) is a **subset** of this checklist.

- QA Catalog Alignment Gate = Check 1 (QA Catalog Alignment) in this checklist
- This checklist extends QA Catalog Alignment Gate with 4 additional checks

### Relationship to IBWR

The **In-Between Wave Reconciliation (IBWR)** process occurs AFTER wave completion.

This Pre-Authorization Checklist occurs BEFORE wave/subwave authorization.

Both are mandatory. They are complementary, not overlapping.

### Relationship to Builder Recruitment

Builder recruitment/appointment is **downstream** of this checklist.

Sequence:
1. FM executes Pre-Authorization Checklist → PASS
2. FM marks subwave "READY FOR AUTHORIZATION"
3. FM recruits/appoints builder
4. Builder executes build-to-green

If checklist FAILS at step 1, steps 2-4 are BLOCKED.

---

## VIII. Version History

| Version | Date | Changes | Authority |
|---------|------|---------|-----------|
| 1.0.0 | 2026-01-07 | Initial FM repository implementation | Governance PR #879 layer-down |

---

**END OF FM PRE-AUTHORIZATION CHECKLIST SPECIFICATION**
