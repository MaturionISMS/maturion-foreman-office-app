# Wave 1.0.7 Phase 2 — Cross-Cutting Components Implementation

**Wave:** 1.0.7  
**Phase:** 2 of 3  
**Builder:** qa-builder  
**QA Scope:** Cross-Cutting Components (17 tests covering QA-147 to QA-199 subset)  
**Execution Artifact:** New PR (to be created)  
**Status:** AUTHORIZED FOR EXECUTION  
**Date:** 2026-01-04  
**FM Authority:** Maturion Foreman

---

## Executive Summary

Phase 2 implements **Cross-Cutting Components** for the Foreman Office App to make **17 RED tests GREEN**.

**Context:**
- Phase 1 (Analytics) completed successfully: 15/15 tests GREEN ✅
- Phase 1 PR #365 merged to main ✅
- Phase 2 covers: Memory Manager, Authority Engine, Notification Service, Evidence Store, Audit Logger, Watchdog

**Critical Boundaries:**
- This is Phase 2 of 3-phase Wave 1.0.7 execution
- Wave 1.0.7 is NOT complete until all 3 phases complete (79 total QA)
- Phase 2 completion does NOT represent Wave-level completion

---

## Scope Definition

### QA Components to Implement

**Total Test Count:** 17 tests  
**Test Location:** `tests/wave1_0_qa_infrastructure/cross_cutting/`

**Cross-Cutting Components:**
- **Memory Manager** (CROSS-01): QA-147 to QA-152 subset
- **Authority Engine** (CROSS-02): QA-153 to QA-158 subset
- **Notification Service** (CROSS-03): QA-159 to QA-164 subset
- **Evidence Store** (CROSS-04): QA-165 to QA-170 subset
- **Audit Logger** (CROSS-05): QA-171 to QA-176 subset
- **Watchdog Observer** (CROSS-06): QA-177 to QA-182 subset
- **Additional Components**: QA-183 to QA-199 subset

**Note:** The 17 tests in `tests/wave1_0_qa_infrastructure/cross_cutting/` cover a representative subset of the full QA-147 to QA-199 range per the QA-to-Red implementation strategy.

### Out of Scope (Reserved for Phase 3)

- ❌ Core User Flows (QA-200 to QA-210) — Phase 3 only
- ❌ Any Analytics components — Phase 1 complete, do not modify
- ❌ Any UI, API, Schema, or Integration components — other waves, do not modify

---

## Input Artifacts

### Architecture (Frozen)
- **FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md** (frozen 2025-12-31)
- Section: Cross-Cutting Components
- All component contracts defined and frozen

### QA Catalog
- **QA_CATALOG.md**
- Cross-Cutting Components section (QA-147 to QA-199)

### Test Suite (RED)
- **Location:** `tests/wave1_0_qa_infrastructure/cross_cutting/`
- **Files:**
  - `test_memory_manager.py` (Memory Manager tests)
  - `test_other_components.py` (Authority, Notification, Evidence, Audit, Watchdog, Additional)
- **Status:** All 17 tests RED (awaiting implementation)
- **Existing Test Infrastructure:** `conftest.py` fixtures available

---

## Task

### Primary Objective
**Implement cross-cutting components to make all 17 RED tests GREEN.**

### Implementation Requirements

1. **Create Module Structures**
   - Create `foreman/cross_cutting/` module directory
   - Organize components by subsystem:
     - `memory_manager.py`
     - `memory_schema.py` (if needed for validation)
     - `authority_engine.py`
     - `notification_service.py`
     - `evidence_store.py`
     - `audit_logger.py`
     - `watchdog.py`
     - Additional supporting modules as needed

2. **Implement Components**
   - Implement all cross-cutting components per frozen architecture
   - Follow architecture contracts exactly
   - Ensure tenant isolation via `organisation_id`
   - Implement proper error handling per architecture
   - Use type hints throughout

3. **Achieve Build-to-Green**
   - Make all 17 tests GREEN
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
  - Focus on Cross-Cutting Components section
- Review QA catalog (QA_CATALOG.md, Cross-Cutting section)
- Inspect RED test suite (`tests/wave1_0_qa_infrastructure/cross_cutting/`)
- Understand test expectations and component contracts

### Step 2: Create Module Structure
```bash
mkdir -p foreman/cross_cutting
touch foreman/cross_cutting/__init__.py
```

### Step 3: Implement Components
- Implement each cross-cutting component per architecture spec
- Follow test-driven approach: let tests define expected behavior
- Ensure tenant isolation in all data operations
- Implement failure modes and error handling

### Step 4: Validate Tests
```bash
pytest tests/wave1_0_qa_infrastructure/cross_cutting/ -v
```

**Expected:** 17/17 tests GREEN, zero failures

### Step 5: Perform Code Checking
- Review all generated code for correctness
- Verify architecture alignment
- Check for defects and edge cases
- Document findings in completion report

### Step 6: Generate Evidence
- Generate Builder QA Report with code checking evidence
- Document completion with COMPLETE terminal state
- List all implemented components

### Step 7: Submit for Gate Validation
- Commit all changes to new PR
- Push to PR
- Report COMPLETE state to FM
- Request FM gate validation

---

## Success Criteria

Phase 2 is complete when:

1. ✅ All 17 Cross-Cutting tests GREEN (100% pass rate)
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
- ❌ Implement Phase 3 (Flows) - not authorized yet
- ❌ Modify constitutional files (`.github/workflows/`, `BUILD_PHILOSOPHY.md`, `foreman/`, `governance/`)

### MUST
- ✅ Implement exactly as specified in frozen architecture
- ✅ Make all 17 tests GREEN
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
   - 17/17 tests GREEN (100%)
   - Zero test debt
   - All evidence artifacts generated
   - Code checking performed and documented
   - Ready for FM gate review

### Prohibited Execution States

❌ **PARTIAL PROGRESS** — Not a valid state  
❌ **INCREMENTAL COMPLETION** — Not recognized  
❌ **PERCENTAGE REPORTS** — Not acceptable (e.g., "14/17 tests passing")  
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
  - 17/17 tests GREEN confirmation
  - Evidence artifacts location
  - Code checking evidence documented
  - Builder completion report
  - FM gate review request
- Submit ONLY when 100% complete
- NO partial submissions

**NEVER REPORT:**
- Partial pass counts (e.g., "14/17 tests passing")
- Progress percentages (e.g., "80% complete")
- Incremental status updates (e.g., "Memory manager done, working on audit logger")
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
- **WAVE_1.0.7_PHASE_1_FM_GATE_APPROVAL_FINAL.md** — Phase 1 learnings and expectations

### Active Learnings from Phase 1
- ✅ **BL-019 Enforcement:** Test dodging is a governance violation (100% = 100%, no exceptions)
- ✅ **FL/CI Determinism:** Tests must pass deterministically in full CI suite
- ✅ **Code Checking Mandatory:** Builder self-checking required with documented evidence
- ✅ **Terminal State Discipline:** BLOCKED or COMPLETE only, no partial reporting

---

## Wave 1.0.7 Phased Execution Context

### Wave 1.0.7 Overall Status

**Wave Status:** INCOMPLETE (Phase 2 of 3 in progress)

**Phase Breakdown:**
- Phase 1 (Analytics): ✅ COMPLETE (15/15 tests GREEN, merged to main)
- Phase 2 (Cross-Cutting): ⏳ **EXECUTION AUTHORIZED** (17 tests, this instruction)
- Phase 3 (Flows): ⏳ PENDING (11 tests, awaiting Phase 2 completion)

**Wave Completion Criteria:**
- All 79 QA components GREEN across all 3 phases
- Phase 2 merge does NOT represent Wave completion
- Phase 3 must complete for Wave 1.0.7 closure

### Phase 2 Authorization

**Prerequisites (All Satisfied):**
- ✅ Phase 1 complete (15/15 GREEN)
- ✅ Phase 1 gate PASS
- ✅ Phase 1 merged to main
- ✅ FM Phase 2 scope assessment complete
- ✅ FM Phase 2 instruction issued

**Phase 2 Boundaries:**
- Authorized: Cross-Cutting Components (17 tests)
- Not Authorized: Core Flows (Phase 3)
- FM Gate Required: Phase 2 gate review before Phase 3 authorization

### Phase 3 Progression

**Phase 3 Authorization:**
- Phase 3 will NOT proceed without explicit FM authorization
- Phase 3 requires Phase 2 COMPLETE and FM gate PASS
- Phase 3 instruction will be issued ONLY after Phase 2 approval
- New PR required for Phase 3 after Phase 2 merge

---

## Dependencies

### Prerequisite Components (All Available)
- **schema-builder:** QA-001 to QA-018 (18 QA) — ✅ MERGED
- **api-builder:** QA-058 to QA-092 (35 QA) — ✅ MERGED
- **integration-builder:** QA-093 to QA-131 (39 QA) — ✅ MERGED
- **Phase 1 (Analytics):** QA-132 to QA-146 (15 QA) — ✅ MERGED

All dependencies satisfied. No blockers.

---

## Builder Reminders

### Critical Points
1. **100% = 100%** — 16/17 = FAIL. Only 17/17 = PASS.
2. **No Test Dodging** — Flaky tests are blockers, not acceptable debt.
3. **Terminal States Only** — Report BLOCKED or COMPLETE. No percentages.
4. **Code Checking Mandatory** — Self-review required with evidence.
5. **Scope Discipline** — Cross-Cutting ONLY. No flows yet.

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
- Refer to test suite (`tests/wave1_0_qa_infrastructure/cross_cutting/`)
- Tests define expected behavior precisely

**Governance Questions:**
- Refer to BUILD_PHILOSOPHY.md
- Refer to BOOTSTRAP_EXECUTION_LEARNINGS.md
- Escalate if governance clarification needed

**Execution Clarifications:**
- Use BLOCKED state to request FM guidance
- Do not proceed with assumptions

---

## Next Steps After Phase 2

**Upon Phase 2 COMPLETE Submission:**
1. FM conducts Phase 2 gate review
2. FM declares gate PASS or FAIL
3. If PASS: FM approves Phase 2 PR for merge
4. CS2 merges Phase 2 PR to main
5. FM issues Phase 3 authorization (Core Flows, 11 tests)
6. Builder executes Phase 3 in new PR

**Wave 1.0.7 Completion:**
- Achieved when all 3 phases complete (79/79 QA GREEN)
- FM issues Wave 1.0.7 completion certification
- Wave-level evidence artifacts generated

---

## Deliverables

1. **Production Code**
   - `foreman/cross_cutting/memory_manager.py`
   - `foreman/cross_cutting/memory_schema.py`
   - `foreman/cross_cutting/authority_engine.py`
   - `foreman/cross_cutting/notification_service.py`
   - `foreman/cross_cutting/evidence_store.py`
   - `foreman/cross_cutting/audit_logger.py`
   - `foreman/cross_cutting/watchdog.py`
   - All supporting modules

2. **Test Results**
   - All 17 tests GREEN
   - Test execution output

3. **Documentation**
   - Builder QA Report (BUILDER_QA_REPORT.md)
   - Code checking evidence statement
   - Completion summary with COMPLETE terminal state

---

## Timeline Expectation

**Phase:** Build-to-Green implementation  
**Estimated Duration:** ~1-2 hours (based on 17 tests, similar complexity to Phase 1's 15 tests)  
**Critical Path:** Yes (required for Wave 1.0.7 Phase 3 authorization)

---

## FM Approval

**Authorization:** Phase 2 execution **AUTHORIZED** ✅  
**Authorized By:** Maturion Foreman (FM)  
**Authorization Date:** 2026-01-04  
**Authority Source:** FM Agent Contract v3.2.0  
**Execution Vehicle:** New PR (to be created by builder)

**Next Builder Action:** Create new PR and execute Phase 2 implementation

---

**END WAVE 1.0.7 PHASE 2 BUILDER INSTRUCTION**
