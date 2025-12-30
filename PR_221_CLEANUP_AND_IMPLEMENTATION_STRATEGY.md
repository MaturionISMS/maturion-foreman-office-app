# PR #221 Cleanup & Implementation Strategy

**Date:** 2025-12-30  
**Status:** Execution Instruction from CS2  
**Purpose:** Clean PR #221 and establish forward implementation strategy  
**Authority:** CS2 Directive (comment 3699537877)

---

## Executive Summary

This document provides:
1. **File Inventory & Categorization** — All PR #221 files categorized (KEEP/MOVE/REMOVE/REPLACE)
2. **Cleanup Execution Plan** — Safe removal strategy
3. **Forward Implementation Strategy** — Clean baseline for Architecture → QA-to-Red → Build-to-Green
4. **Workflow Updates** — Correct workflows for build readiness

---

## A. File Inventory & Categorization

### Files Added/Modified in PR #221 (18 commits)

Total files: 18 (17 added, 1 modified)

---

### Category 1: KEEP (Canonical / Required / Still Relevant)

**13 files — Represent canonical Wave 0 completion and Wave 1.0 progress**

#### Wave 0.1: Builder Recruitment (KEEP — Canonical)
1. ✅ **WAVE_0.1_BUILDER_RECRUITMENT_REPORT.md** — Builder recruitment results (19/19 checks passed)
2. ✅ **WAVE_0.1_BUILDER_RECRUITMENT_SPEC.md** — Builder recruitment scope and plan
3. ✅ **WAVE_0.1_DELIVERABLES_README.md** — Navigation guide for Wave 0.1 artifacts
4. ✅ **WAVE_0.1_PREHANDOVER_PROOF.md** — CS2 handover proof
5. ✅ **WAVE_0.1_QUICK_SUMMARY.md** — Executive summary (2-min read)
6. ✅ **WAVE_0.1_READINESS_CERTIFICATION.md** — CS2 approval documented

**Reason to KEEP:** Wave 0.1 is canonical, CS2-approved, and referenced by Wave 1.0 continuity correction. These are evidence artifacts proving builder readiness.

---

#### Wave 0.2: Task Assignment Validation (KEEP — Canonical)
7. ✅ **WAVE_0.2_COMPLETION_SUMMARY.md** — Wave 0.2 objectives satisfied
8. ✅ **WAVE_0.2_QUICK_SUMMARY.md** — Executive summary
9. ✅ **WAVE_0.2_TASK_ASSIGNMENT_DRY_RUN_SPEC.md** — Task assignment spec

**Reason to KEEP:** Wave 0.2 validated execution mechanics (CS2-approved). Required evidence for governance continuity.

---

#### Wave 1.0 Canonical Artifacts (KEEP — Active)
10. ✅ **WAVE_1.0_ARCHITECTURE_COMPLETENESS_REPORT.md** — Architecture validation (CS2 approved freeze)
11. ✅ **WAVE_1.0_SELF_AUDIT_GAP_ANALYSIS.md** — Governance continuity error detection (CS2 verified)
12. ✅ **WAVE_1.0_TASK_QA_RED_01_BUILDER_ISSUE_SPEC.md** — QA-to-Red builder issue specification (CORRECTED)

**Reason to KEEP:** Active Wave 1.0 Phase 2 artifacts, CS2-approved architecture freeze, corrected builder issue spec ready for proxy execution.

---

#### Supporting Evidence (KEEP — Referenced)
13. ✅ **foreman/builder-registry-report.md** — Modified (5/5 builders validated, 19/19 checks passed)

**Reason to KEEP:** PRE-EXISTING file modified with Wave 0.1 validation results. Canonical evidence of builder readiness.

---

### Category 2: REMOVE (Clutter / Superseded / Bootstrap-Only)

**4 files — Wave 0.2 bootstrap artifacts no longer needed**

#### Wave 0.2 Bootstrap Execution Artifacts (REMOVE — Bootstrap-only)
1. ❌ **WAVE_0.2_DAI_TASK_UI_01.md** — DAI for CS2 proxy (bootstrap simulation, completed)
2. ❌ **WAVE_0.2_EXECUTION_STATUS_TRACKER.md** — Execution tracker (bootstrap visibility, completed)
3. ❌ **WAVE_0.2_TASK_UI_01_ASSIGNMENT.md** — Task UI-01 assignment (bootstrap simulation, completed)

**Reason to REMOVE:**
- Bootstrap-only artifacts for Wave 0.2 validation
- Purpose: Validate execution mechanics (✅ COMPLETE)
- Not needed for Wave 1.0 forward execution
- Evidence captured in WAVE_0.2_COMPLETION_SUMMARY.md (KEEP)
- Safe to remove: Not referenced by governance or active plans

**Dependency Impact:** None — evidence preserved in summary document

---

#### Invalid Execution Plan (REMOVE — Superseded)
4. ❌ **WAVE_1.0_EXECUTION_PLAN.md** — Invalid plan (skipped architecture freeze, withdrawn per CS2)

**Reason to REMOVE:**
- Withdrawn per CS2 instruction (governance sequencing drift)
- Violated BUILD_PHILOSOPHY.md canonical pipeline
- Superseded by corrected Wave 1.0 approach (architecture freeze → QA-to-Red → build-to-green)
- No longer referenced or valid

**Dependency Impact:** None — plan was withdrawn, never executed

---

### Category 3: KEEP but Consider Relocation

**1 file — Deliverable, but location may need review**

1. 🔄 **docs/ui/FOREMAN_UI_COMPONENT_INVENTORY.md** — UI component inventory (Wave 0.2 deliverable)

**Current Status:** KEEP (it's a deliverable)  
**Location Review Needed:** Yes — determine if docs/ui/ is correct long-term location or if should move to docs/planning/ or foreman/planning/

**Reason to KEEP:** Legitimate planning artifact (10 UI components documented), even though generated via bootstrap simulation.

**Action:** KEEP for now, flag for future location review when planning artifacts are organized.

---

## B. Cleanup Execution Plan

### Step B1: Safety Validation (Pre-Removal Checks)

Before removing any files, validate:
1. ✅ File is not referenced in BUILD_PHILOSOPHY.md
2. ✅ File is not referenced in canonical architecture (TRUE_NORTH_FM_ARCHITECTURE.md)
3. ✅ File is not referenced in APP_DESCRIPTION.md
4. ✅ File is not referenced in governance/agents/*.agent.contract.md
5. ✅ File purpose is captured in retained evidence (WAVE_0.2_COMPLETION_SUMMARY.md)

**All 4 files marked for removal satisfy all safety criteria.**

---

### Step B2: Removal Sequence

**Files to Remove (in any order, no dependencies):**
1. WAVE_0.2_DAI_TASK_UI_01.md
2. WAVE_0.2_EXECUTION_STATUS_TRACKER.md
3. WAVE_0.2_TASK_UI_01_ASSIGNMENT.md
4. WAVE_1.0_EXECUTION_PLAN.md

**Command:**
```bash
git rm WAVE_0.2_DAI_TASK_UI_01.md \
       WAVE_0.2_EXECUTION_STATUS_TRACKER.md \
       WAVE_0.2_TASK_UI_01_ASSIGNMENT.md \
       WAVE_1.0_EXECUTION_PLAN.md
```

---

### Step B3: Post-Cleanup Verification

After removal, verify:
1. All canonical Wave 0 artifacts remain (Wave 0.1 + Wave 0.2 summaries)
2. All active Wave 1.0 artifacts remain (architecture completeness, self-audit, builder issue spec)
3. No broken references in WAVE_0.2_COMPLETION_SUMMARY.md
4. PR #221 contains only canonical artifacts

---

## C. Forward Implementation Strategy (Clean Baseline)

### C1. Canonical Build Pipeline (BUILD_PHILOSOPHY.md)

**5-Phase Pipeline (Non-Negotiable):**

```
Phase 1: ARCHITECTURE (Freeze)           ✅ COMPLETE (CS2 approved)
    ↓
Phase 2: RED QA (QA-to-Red)              ⏳ READY (builder issue spec generated)
    ↓
Phase 3: BUILD TO GREEN (Implementation) ⏸️ BLOCKED (awaits Phase 2)
    ↓
Phase 4: VALIDATION (QA-to-Green)        ⏸️ BLOCKED (awaits Phase 3)
    ↓
Phase 5: MERGE (Integration)             ⏸️ BLOCKED (awaits Phase 4)
```

---

### C2. Wave 1.0 Current Status (Clean Baseline)

#### Phase 1: Architecture Freeze ✅ COMPLETE
- **Architecture:** TRUE_NORTH_FM_ARCHITECTURE.md v1.0 (FROZEN)
- **Validation:** WAVE_1.0_ARCHITECTURE_COMPLETENESS_REPORT.md (26 KB)
- **CS2 Approval:** Obtained (2025-12-30)
- **Status:** Locked, no changes without governance authorization

#### Phase 2: QA-to-Red ⏳ READY FOR CS2 PROXY
- **Builder:** qa-builder (recruited and validated in Wave 0.1)
- **Task Spec:** WAVE_1.0_TASK_QA_RED_01_BUILDER_ISSUE_SPEC.md (CORRECTED)
- **Canonical Continuity:** Established (references Wave 0.1 evidence)
- **Status:** Awaiting CS2 proxy issue creation

**CS2 Proxy Actions Required:**
1. Create GitHub issue per WAVE_1.0_TASK_QA_RED_01_BUILDER_ISSUE_SPEC.md
2. Title: "QA-to-Red Suite Creation — Wave 1.0 Phase 2 (WAVE_1.0_TASK_QA_RED_01)"
3. Assign: qa-builder (already recruited in Wave 0.1)
4. Labels: wave-1.0, phase-2, qa-to-red, qa-builder
5. Execute: qa-builder compiles QA-to-Red suite per specification

**Phase 2 Deliverables (qa-builder):**
- DP-RED Registry (`foreman/qa/dp-red-registry.json`)
- Test Suite (Unit, Integration, E2E) — all RED
- Test Coverage Map (≥95% architecture coverage)
- Red Gate Definitions
- QA-to-Red Validation Report

#### Phase 3: Build-to-Green ⏸️ BLOCKED
- **Status:** Awaits Phase 2 QA-to-Red completion
- **Requirements:** QA suite exists, executed, all tests RED
- **Planning:** Will derive from QA-to-Red results (not before)

#### Phase 4-5: Validation & Merge ⏸️ BLOCKED
- **Status:** Awaits Phase 3 implementation completion

---

### C3. Implementation Sequencing (No Deviation)

**Canonical Sequence (BUILD_PHILOSOPHY.md Section III):**

1. ✅ **App Description** — APP_DESCRIPTION.md v1.1 (validated)
2. ✅ **Functional Requirements** — FM_FUNCTIONAL_SPEC.md v1.1.0 (validated)
3. ✅ **Architecture** — TRUE_NORTH_FM_ARCHITECTURE.md v1.0 (FROZEN)
4. ⏳ **QA-to-Red** — WAVE_1.0_TASK_QA_RED_01 (in progress via CS2 proxy)
5. ⏸️ **Build-to-Green** — Awaits QA-to-Red completion
6. ⏸️ **Validation** — Awaits build completion
7. ⏸️ **Merge** — Awaits validation

**No steps may be skipped, reordered, or executed in parallel.**

---

### C4. Builder Status (Canonical Continuity)

**Builders Recruited (Wave 0.1 — CS2 Approved):**
- ui-builder — Ready
- api-builder — Ready
- schema-builder — Ready
- integration-builder — Ready
- qa-builder — Assigned to Phase 2

**Validation:** 19/19 checks passed (foreman/builder-registry-report.md)

**No additional recruitment or appointment required.**

---

## D. Workflow Updates (Build Readiness & Implementation)

### D1. Current CI/CD Status

**Existing Workflows (Pre-PR #221):**
- Located in `.github/workflows/`
- Need review to ensure Phase 2+ support

**Required for Phase 2:**
- CI workflow that runs tests (Jest, Playwright)
- PR gate enforcement (per BL-0008)
- Branch protection configured

**Required for Phase 3+:**
- All 9 PR merge gates (per builder issue spec):
  1. All unit tests pass
  2. All integration tests for modified code pass
  3. No new DP-RED entries (unless authorized)
  4. Code coverage ≥80% for changed code
  5. ESLint/Prettier pass
  6. TypeScript compilation pass
  7. No security vulnerabilities
  8. FM validation approval
  9. At least one previously RED test now GREEN

---

### D2. Workflow Validation Plan

**Step D2.1:** Review existing `.github/workflows/*.yml`
**Step D2.2:** Validate test execution support (Jest, Playwright)
**Step D2.3:** Validate PR gate enforcement capability
**Step D2.4:** Update workflows if gaps found
**Step D2.5:** Document workflow configuration in evidence

**Note:** Workflow updates should be separate commit/PR from cleanup to maintain governance traceability.

---

## E. Governance Compliance

### E1. BUILD_PHILOSOPHY.md Adherence ✅

**5-Phase Pipeline:** Followed exactly  
**One-Time Build Correctness:** Architecture frozen before QA-to-Red  
**Zero Regression:** Not applicable yet (no code implemented)  
**Full Architectural Alignment:** All artifacts reference TRUE_NORTH v1.0  
**Zero Loss of Context:** Wave 0 evidence preserved, continuity established  
**Zero Ambiguity:** All specs explicit, acceptance criteria clear

---

### E2. Platform Readiness Prerequisites ✅

**G-PLAT-READY-01 Compliance:**
- ✅ Platform Readiness Assurance (GREEN) — CS2 confirmed
- ✅ Governance layer-down complete — Enforced
- ✅ Branch protection verified — Active
- ✅ Architecture completeness satisfied — CS2 approved

---

### E3. PR Gate Layer-Down (BL-0008) ✅

**All 5 PR gates defined:**
1. ✅ Test execution gate
2. ✅ Code quality gate
3. ✅ Coverage gate
4. ✅ Security gate
5. ✅ FM approval gate

**Status:** Defined in builder issue spec, will be enforced in Phase 3+

---

### E4. Canonical Continuity ✅

**Wave 0 → Wave 1 Continuity:**
- Wave 0.1: Builder recruitment (CS2 approved)
- Wave 0.2: Task assignment mechanics validated (CS2 approved)
- Wave 1.0 Phase 1: Architecture frozen (CS2 approved)
- Wave 1.0 Phase 2: QA-to-Red ready (awaits CS2 proxy)

**Governance Continuity Error:** Detected via self-audit (WAVE_1.0_SELF_AUDIT_GAP_ANALYSIS.md), corrected per CS2 instruction

---

## F. Cleanup Execution Summary

### Files to KEEP (13 files)
```
WAVE_0.1_BUILDER_RECRUITMENT_REPORT.md
WAVE_0.1_BUILDER_RECRUITMENT_SPEC.md
WAVE_0.1_DELIVERABLES_README.md
WAVE_0.1_PREHANDOVER_PROOF.md
WAVE_0.1_QUICK_SUMMARY.md
WAVE_0.1_READINESS_CERTIFICATION.md
WAVE_0.2_COMPLETION_SUMMARY.md
WAVE_0.2_QUICK_SUMMARY.md
WAVE_0.2_TASK_ASSIGNMENT_DRY_RUN_SPEC.md
WAVE_1.0_ARCHITECTURE_COMPLETENESS_REPORT.md
WAVE_1.0_SELF_AUDIT_GAP_ANALYSIS.md
WAVE_1.0_TASK_QA_RED_01_BUILDER_ISSUE_SPEC.md
foreman/builder-registry-report.md
```

Plus 1 file flagged for location review:
```
docs/ui/FOREMAN_UI_COMPONENT_INVENTORY.md
```

---

### Files to REMOVE (4 files)
```
WAVE_0.2_DAI_TASK_UI_01.md
WAVE_0.2_EXECUTION_STATUS_TRACKER.md
WAVE_0.2_TASK_UI_01_ASSIGNMENT.md
WAVE_1.0_EXECUTION_PLAN.md
```

---

### Post-Cleanup PR #221 Contents

**Total files after cleanup:** 14 files (13 canonical + 1 flagged for review)

**Categories:**
- Wave 0.1 canonical artifacts: 6 files
- Wave 0.2 canonical artifacts: 3 files
- Wave 1.0 active artifacts: 3 files
- Builder registry evidence: 1 file
- UI planning artifact: 1 file

**Status:** Clean baseline for forward implementation

---

## G. Forward Execution (Post-Cleanup)

### G1. Immediate Next Steps (CS2 Actions)

**Step G1.1:** Review and approve this cleanup strategy  
**Step G1.2:** Execute cleanup (remove 4 files)  
**Step G1.3:** Create GitHub issue per WAVE_1.0_TASK_QA_RED_01_BUILDER_ISSUE_SPEC.md  
**Step G1.4:** Assign qa-builder to Phase 2 QA-to-Red task  
**Step G1.5:** Phase 2 execution begins (bootstrap proxy rules)

---

### G2. Phase 2 Execution Flow

**qa-builder receives task:**
1. Reads frozen architecture (TRUE_NORTH_FM_ARCHITECTURE.md v1.0)
2. Compiles QA-to-Red test suite (~112 tests across 7 categories)
3. Executes tests (all intentionally RED)
4. Registers tests in DP-RED registry
5. Generates coverage map (≥95% architecture coverage)
6. Generates QA-to-Red validation report
7. Notifies FM of completion

**FM validates deliverables:**
1. All acceptance criteria met (10 criteria)
2. No forbidden actions violated (7 restrictions)
3. Zero test debt confirmed
4. Coverage ≥95% verified
5. Generates DAI for CS2 proxy PR creation

**CS2 proxy execution:**
1. Creates PR per DAI
2. Reviews and merges PR (bootstrap proxy rules)
3. Notifies FM of Phase 2 completion

**Phase 3 initiation:**
1. FM derives build-to-green tasks from QA-to-Red results
2. FM assigns builders per task
3. Build-to-green execution begins (9 PR merge gates enforced)

---

### G3. Success Criteria (Forward Implementation)

**Phase 2 Complete When:**
- ✅ All QA-to-Red deliverables produced
- ✅ All tests RED (100% failing)
- ✅ Coverage ≥95% of architecture
- ✅ Zero test debt
- ✅ FM validates completeness
- ✅ CS2 approves QA-to-Red suite

**Phase 3+ Success:**
- Derived from Phase 2 results (not pre-planned)

---

## H. Governance Traceability

### H1. Authority Chain

```
CS2 (Human Authority)
    ↓ authorized
BUILD_PHILOSOPHY.md (Constitutional Authority)
    ↓ governs
Wave 1.0 Execution (FM Planning Authority)
    ↓ sequences
Phase 2: QA-to-Red (qa-builder Execution)
    ↓ enables
Phase 3: Build-to-Green (builders Execution)
```

---

### H2. Evidence Chain

```
Platform Readiness (G-PLAT-READY-01) ✅ CS2 confirmed
    ↓
Wave 0.1 Completion ✅ CS2 approved
    ↓
Wave 0.2 Completion ✅ CS2 approved
    ↓
Phase 1: Architecture Freeze ✅ CS2 approved
    ↓
Phase 2: QA-to-Red ⏳ CS2 proxy executing
    ↓
Phase 3: Build-to-Green ⏸️ Blocked (awaits Phase 2)
```

---

## I. Risk Assessment

### I1. Cleanup Risks

**Risk:** Accidental removal of canonical artifacts  
**Mitigation:** Safety validation checks (Section B1), categorization explicit  
**Status:** LOW RISK (all removal targets validated)

**Risk:** Broken references after cleanup  
**Mitigation:** Post-cleanup verification (Section B3), reference audit  
**Status:** LOW RISK (removed files not referenced)

---

### I2. Forward Implementation Risks

**Risk:** Phase 2 execution delay  
**Mitigation:** Clear builder issue spec, bootstrap proxy rules validated (Wave 0.2)  
**Status:** MEDIUM RISK (depends on CS2 proxy availability)

**Risk:** QA-to-Red incompleteness  
**Mitigation:** 10 explicit acceptance criteria, FM validation gate  
**Status:** LOW RISK (builder spec comprehensive)

**Risk:** Build-to-green planning premature  
**Mitigation:** BUILD_PHILOSOPHY.md enforcement, no planning before QA-to-Red  
**Status:** LOW RISK (governance clear, self-audit performed)

---

## J. Approval & Execution

### J1. Approval Required From CS2

**This strategy requires CS2 approval before execution.**

**Approval Criteria:**
- ✅ Cleanup plan is safe (no canonical artifacts removed)
- ✅ Forward strategy aligns with BUILD_PHILOSOPHY.md
- ✅ Governance compliance maintained
- ✅ Canonical continuity preserved

---

### J2. Execution Sequence (After Approval)

**Step J2.1:** Execute cleanup (remove 4 files) — FM authority  
**Step J2.2:** Commit cleanup with clear message — CS2 proxy  
**Step J2.3:** Update PR #221 description with clean baseline — CS2 proxy  
**Step J2.4:** Create Phase 2 builder issue — CS2 proxy  
**Step J2.5:** Phase 2 execution begins — qa-builder + FM validation + CS2 proxy

---

## K. Document Status

**Status:** READY FOR CS2 REVIEW  
**Completeness:** 100% (all sections complete)  
**Governance Alignment:** ✅ VERIFIED  
**Authority:** FM Planning (CS2 execution proxy required)

---

**Maturion Foreman**  
PR #221 Cleanup & Implementation Strategy  
Generated per CS2 Instruction (comment 3699537877)  
2025-12-30 14:36 UTC (16:36 SAST)
