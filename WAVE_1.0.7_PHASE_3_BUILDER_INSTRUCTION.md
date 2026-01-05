# Wave 1.0.7 Phase 3 — Core User Flows Implementation

**Wave:** 1.0.7  
**Phase:** 3 of 3 (FINAL PHASE)  
**Builder:** qa-builder  
**QA Scope:** Core User Flows (11 tests covering QA-200 to QA-210)  
**Execution Artifact:** New PR (to be created)  
**Status:** AUTHORIZED FOR EXECUTION  
**Date:** 2026-01-04  
**FM Authority:** Maturion Foreman

---

## Executive Summary

Phase 3 implements **Core User Flows** for the Foreman Office App to make **11 RED tests GREEN**.

**This is the FINAL PHASE of Wave 1.0.7.**

**Context:**
- Phase 1 (Analytics) completed: 15/15 tests GREEN ✅ MERGED
- Phase 2 (Cross-Cutting) completed: 17/17 tests GREEN ✅ MERGED
- Phase 3 covers: Intent→Build Flow, Evidence Drill-Down Flow, Escalation→Resolution Flow

**Critical Boundaries:**
- This is Phase 3 of 3-phase Wave 1.0.7 execution
- **Wave 1.0.7 COMPLETES when Phase 3 completes** (43 total tests: 15+17+11)
- Phase 3 completion = Wave 1.0.7 completion

---

## Scope Definition

### QA Components to Implement

**Total Test Count:** 11 tests  
**Test Location:** `tests/wave1_0_qa_infrastructure/flows/`

**Core User Flows:**
- **Intent → Build Execution Flow** (QA-200 to QA-204): 5 tests
  - QA-200: End-to-end intent to build completion
  - QA-201: Intent intake step
  - QA-202: Clarification step
  - QA-203: Requirement generation step
  - QA-204: Approval step

- **Evidence Drill-Down Flow** (QA-205 to QA-207): 3 tests
  - QA-205: Build initiation step
  - QA-206: Builder assignment step
  - QA-207: Build execution monitoring

- **Escalation → Resolution Flow** (QA-208 to QA-210): 3 tests
  - QA-208: QA validation step
  - QA-209: Build completion step
  - QA-210: Error handling in flow

**Note:** The 11 tests in `tests/wave1_0_qa_infrastructure/flows/` cover the core user flows (QA-200 to QA-210) per the QA-to-Red implementation strategy.

### Out of Scope

- ❌ Analytics components — Phase 1 complete, do not modify
- ❌ Cross-Cutting components — Phase 2 complete, do not modify
- ❌ Any UI, API, Schema, or Integration components — other waves, do not modify
- ❌ Extended flow QA (QA-211 to QA-242) — future waves

---

## Input Artifacts

### Architecture (Frozen)
- **FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md** (frozen 2025-12-31)
- Section: Core User Flows
- All flow contracts defined and frozen

### QA Catalog
- **QA_CATALOG.md**
- Flow-Based QA section (QA-200 to QA-210)

### Test Suite (RED)
- **Location:** `tests/wave1_0_qa_infrastructure/flows/`
- **Files:**
  - `test_core_flows.py` (11 flow tests)
- **Status:** All 11 tests RED (awaiting implementation)
- **Existing Test Infrastructure:** `conftest.py` fixtures available

---

## Task

### Primary Objective
**Implement core user flows to make all 11 RED tests GREEN.**

### Implementation Requirements

1. **Create Module Structures**
   - Create `foreman/flows/` module directory
   - Organize flows by type:
     - `intent_to_build.py` (Intent → Build flow)
     - `flow_executor.py` (Flow execution engine)
     - `evidence_drill_down.py` (Evidence drill-down flow)
     - `escalation_resolution.py` (Escalation → Resolution flow)
     - Additional supporting modules as needed

2. **Implement Flows**
   - Implement all core user flows per frozen architecture
   - Follow architecture contracts exactly
   - Ensure tenant isolation via `organisation_id`
   - Implement proper state management and transitions
   - Implement evidence trail generation
   - Use type hints throughout

3. **Achieve Build-to-Green**
   - Make all 11 tests GREEN
   - Achieve GREEN on **first attempt** (One-Time Build Correctness)
   - Zero test debt (no skips, no TODOs, no incomplete tests)

4. **Code Checking (Mandatory)**
   - Perform self-code-checking on all generated code
   - Verify logical correctness against architecture
   - Verify implementation makes RED tests GREEN correctly
   - Check for obvious defects, errors, or omissions
   - Document code checking evidence in completion report

---

## Execution Instructions

### Step 1: Review Input Artifacts
- Read frozen architecture (FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md)
  - Focus on Core User Flows section
- Review QA catalog (QA_CATALOG.md, Flow-Based QA section)
- Inspect RED test suite (`tests/wave1_0_qa_infrastructure/flows/`)
- Understand test expectations and flow contracts

### Step 2: Create Module Structure
```bash
mkdir -p foreman/flows
touch foreman/flows/__init__.py
```

### Step 3: Implement Flows
- Implement each core user flow per architecture spec
- Follow test-driven approach: let tests define expected behavior
- Ensure tenant isolation in all data operations
- Implement state transitions and evidence generation

### Step 4: Validate Tests
```bash
pytest tests/wave1_0_qa_infrastructure/flows/ -v
```

**Expected:** 11/11 tests GREEN, zero failures

### Step 5: Perform Code Checking
- Review all generated code for correctness
- Verify architecture alignment
- Check for defects and edge cases
- Document findings in completion report

### Step 6: Generate Evidence
- Generate Builder QA Report with code checking evidence
- Document completion with COMPLETE terminal state
- List all implemented flows

### Step 7: Submit for Gate Validation
- Commit all changes to new PR
- Push to PR
- Report COMPLETE state to FM
- Request FM gate validation

---

## Success Criteria

Phase 3 is complete when:

1. ✅ All 11 Core Flow tests GREEN (100% pass rate)
2. ✅ Zero test debt maintained (no skips, no TODOs, no incomplete tests)
3. ✅ Architecture alignment verified (100% from frozen spec)
4. ✅ Code checking performed and documented
5. ✅ Evidence artifacts generated
6. ✅ Builder report submitted with COMPLETE terminal state
7. ✅ FM review requested in PR

**Gate Pass:** ALL requirements satisfied  
**Gate Fail:** ANY requirement not satisfied

---

## Constraints

### MUST NOT
- ❌ Modify frozen architecture
- ❌ Modify test suite (unless correcting obvious test bugs)
- ❌ Modify governance documents
- ❌ Skip, comment out, or mark tests as TODO
- ❌ Add test debt
- ❌ Deviate from frozen architecture specifications
- ❌ Modify Phase 1 (Analytics) code - already merged
- ❌ Modify Phase 2 (Cross-Cutting) code - already merged
- ❌ Modify constitutional files (`.github/workflows/`, `BUILD_PHILOSOPHY.md`, `foreman/`, `governance/`)

### MUST
- ✅ Implement exactly as specified in frozen architecture
- ✅ Make all 11 tests GREEN
- ✅ Achieve Build-to-Green on first attempt
- ✅ Maintain zero test debt
- ✅ Follow BUILD_PHILOSOPHY.md principles
- ✅ Perform mandatory code checking with evidence
- ✅ Generate complete evidence artifacts
- ✅ Report only in BLOCKED or COMPLETE terminal states

---

## Execution State Discipline (OPOJD Requirement)

### Allowed Execution States

Under One-Time Build Law and governance learnings (BL-016, BL-018, BL-019), ONLY the following execution states are permitted:

1. **BLOCKED** — Execution cannot proceed due to:
   - Missing dependencies
   - Unresolved ambiguity in requirements
   - Platform/environment failure
   - Clarification required from FM

2. **COMPLETE** — Execution finished with:
   - 11/11 tests GREEN (100%)
   - Zero test debt
   - All evidence artifacts generated
   - Code checking performed and documented
   - Ready for FM gate review

### Prohibited Execution States

❌ **PARTIAL PROGRESS** — Not a valid state  
❌ **INCREMENTAL COMPLETION** — Not recognized  
❌ **PERCENTAGE REPORTS** — Not acceptable (e.g., "9/11 tests passing")  
❌ **ITERATIVE STATUS UPDATES** — Violates OPOJD  
❌ **WORK-IN-PROGRESS SUBMISSIONS** — Not permitted

### Reporting Requirements

**IF BLOCKED:**
- Report BLOCKED state immediately with:
  - Specific blocker description
  - Attempted resolution steps
  - FM action required
- WAIT for FM response
- DO NOT proceed without FM clearance

**IF COMPLETE:**
- Report COMPLETE state with:
  - 11/11 tests GREEN confirmation
  - Evidence artifacts location
  - Code checking evidence documented
  - Builder completion report
  - FM gate review request
- Submit ONLY when 100% complete
- NO partial submissions

**NEVER REPORT:**
- Partial pass counts (e.g., "9/11 tests passing")
- Progress percentages (e.g., "80% complete")
- Incremental status updates (e.g., "Intent flow done, working on escalation flow")
- Work-in-progress checkpoints

### Mindset Compliance

**Builder mindset compliance is a CONDITION of continued appointment.**

Builders SHALL:
- Internalize OPOJD terminal state discipline
- Report ONLY in BLOCKED or COMPLETE states
- Request clarification if execution state is ambiguous
- Reference `governance/canon/BOOTSTRAP_EXECUTION_LEARNINGS.md` for governance context

Builders SHALL NOT:
- Adopt iterative/agile progress reporting patterns
- Submit partial work for "feedback loops"
- Request "progress checks" or "interim reviews"
- Interpret FM supervision as encouragement for partial delivery

---

## Governance Reference

### Binding Documents
- **BUILD_PHILOSOPHY.md** — One-Time Build Correctness principle
- **governance/canon/BOOTSTRAP_EXECUTION_LEARNINGS.md** — BL-016 (proactive complexity management), BL-018 (platform constraints), BL-019 (test dodging prevention)
- **FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md** — Frozen architecture (immutable)
- **WAVE_1.0.7_PHASE_1_FM_GATE_APPROVAL_FINAL.md** — Phase 1 learnings
- **WAVE_1.0.7_PHASE_2_BUILDER_INSTRUCTION.md** — Phase 2 learnings

### Active Learnings from Phase 1 & 2
- ✅ **BL-019 Enforcement:** Test dodging is a governance violation (100% = 100%, no exceptions)
- ✅ **FL/CI Determinism:** Tests must pass deterministically in full CI suite
- ✅ **Code Checking Mandatory:** Builder self-checking required with documented evidence
- ✅ **Terminal State Discipline:** BLOCKED or COMPLETE only, no partial reporting
- ✅ **Minimal Changes:** Surgical, targeted implementations only

---

## Wave 1.0.7 Completion Context

### Wave 1.0.7 Overall Status

**Wave Status:** INCOMPLETE (Phase 3 execution authorized, final phase)

**Phase Breakdown:**
- Phase 1 (Analytics): ✅ COMPLETE (15/15 tests GREEN, merged to main)
- Phase 2 (Cross-Cutting): ✅ COMPLETE (17/17 tests GREEN, merged to main)
- Phase 3 (Flows): ⏳ **EXECUTION AUTHORIZED** (11 tests, this instruction)

**Wave Completion Criteria:**
- All 43 tests GREEN across all 3 phases (15+17+11)
- Phase 3 completion = Wave 1.0.7 completion
- Wave-level certification required after Phase 3

### Phase 3 Authorization

**Prerequisites (All Satisfied):**
- ✅ Phase 1 complete (15/15 GREEN, merged)
- ✅ Phase 2 complete (17/17 GREEN, merged)
- ✅ Phase 1 gate PASS
- ✅ Phase 2 gate PASS
- ✅ FM Phase 3 scope assessment complete
- ✅ FM Phase 3 instruction issued

**Phase 3 Boundaries:**
- Authorized: Core User Flows (11 tests)
- Not Authorized: Extended flows or additional waves
- FM Gate Required: Phase 3 gate review for Wave 1.0.7 completion

### Wave 1.0.7 Completion

**Upon Phase 3 COMPLETE:**
- FM conducts Phase 3 gate review
- If PASS: FM declares Wave 1.0.7 COMPLETE
- FM issues Wave 1.0.7 completion certification
- Wave-level evidence artifacts generated
- Readiness for next wave assessed

---

## Dependencies

### Prerequisite Components (All Available)
- **schema-builder:** QA-001 to QA-018 (18 QA) — ✅ MERGED
- **api-builder:** QA-058 to QA-092 (35 QA) — ✅ MERGED
- **integration-builder:** QA-093 to QA-131 (39 QA) — ✅ MERGED
- **Phase 1 (Analytics):** QA-132 to QA-146 (15 QA) — ✅ MERGED
- **Phase 2 (Cross-Cutting):** QA-147 to QA-199 subset (17 tests) — ✅ MERGED

All dependencies satisfied. No blockers.

---

## Builder Reminders

### Critical Points
1. **100% = 100%** — 10/11 = FAIL. Only 11/11 = PASS.
2. **No Test Dodging** — Flaky tests are blockers, not acceptable debt.
3. **Terminal States Only** — Report BLOCKED or COMPLETE. No percentages.
4. **Code Checking Mandatory** — Self-review required with evidence.
5. **Scope Discipline** — Core Flows ONLY. No extended flows.
6. **FINAL PHASE** — Phase 3 completion = Wave 1.0.7 completion.

### If Uncertain
- **STOP and ask FM** — Clarity is better than assumption.
- **Use BLOCKED state** — Not a failure, it's correct governance.
- **Reference governance docs** — All learnings documented and binding.

---

## FM Support

**Architecture Questions:**
- Refer to frozen architecture (FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md)
- Escalate if architecture ambiguities discovered

**Test Questions:**
- Refer to test suite (`tests/wave1_0_qa_infrastructure/flows/`)
- Tests define expected behavior precisely

**Governance Questions:**
- Refer to BUILD_PHILOSOPHY.md
- Refer to BOOTSTRAP_EXECUTION_LEARNINGS.md
- Escalate if governance clarification needed

**Execution Clarifications:**
- Use BLOCKED state to request FM guidance
- Do not proceed with assumptions

---

## Next Steps After Phase 3

**Upon Phase 3 COMPLETE Submission:**
1. FM conducts Phase 3 gate review
2. FM declares gate PASS or FAIL
3. If PASS: FM approves Phase 3 PR for merge
4. CS2 merges Phase 3 PR to main
5. **FM declares Wave 1.0.7 COMPLETE** ✅
6. FM issues Wave 1.0.7 completion certification
7. FM assesses readiness for next wave

**Wave 1.0.7 Completion:**
- Achieved when Phase 3 completes (43/43 tests GREEN: 15+17+11)
- FM issues Wave 1.0.7 completion certification
- Wave-level evidence artifacts generated
- Celebration! 🎉

---

## Deliverables

1. **Production Code**
   - `foreman/flows/intent_to_build.py`
   - `foreman/flows/flow_executor.py`
   - `foreman/flows/evidence_drill_down.py`
   - `foreman/flows/escalation_resolution.py`
   - All supporting modules

2. **Test Results**
   - All 11 tests GREEN
   - Test execution output

3. **Documentation**
   - Builder QA Report (BUILDER_QA_REPORT.md)
   - Code checking evidence statement
   - Completion summary with COMPLETE terminal state

---

## Timeline Expectation

**Phase:** Build-to-Green implementation (FINAL PHASE)  
**Estimated Duration:** ~1-2 hours (based on 11 tests, similar to Phase 2)  
**Critical Path:** Yes (required for Wave 1.0.7 completion)

---

## FM Approval

**Authorization:** Phase 3 execution **AUTHORIZED** ✅  
**Authorized By:** Maturion Foreman (FM)  
**Authorization Date:** 2026-01-04  
**Authority Source:** FM Agent Contract v3.2.0  
**Execution Vehicle:** New PR (to be created by builder)

**Next Builder Action:** Create new PR and execute Phase 3 implementation

**Wave Completion:** Phase 3 completion = Wave 1.0.7 COMPLETE 🎯

---

**END WAVE 1.0.7 PHASE 3 BUILDER INSTRUCTION**
