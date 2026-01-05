# Subwave 2.1: Enhanced Dashboard — ui-builder Build-to-Green

**Wave:** 2.0  
**Subwave:** 2.1  
**Builder:** ui-builder  
**QA Range:** QA-401 to QA-415 (15 QA components)  
**Complexity:** LOW  
**Duration Estimate:** 4-6 days  
**Dependencies:** Wave 1.0 Complete ✅  
**Status:** CORRECTED (BL-019 Emergency QA Range Correction)

---

## Executive Summary

Implement **Enhanced Dashboard** features for the Foreman Office App to make **15 RED tests GREEN**.

**Mission:** Enhance the existing Dashboard subsystem with advanced features including drill-down capabilities, filtering, and real-time updates.

**Context:**
- Builds on Wave 1.0 Dashboard foundation (QA-023 to QA-042)
- Adds drill-down navigation (5 QA)
- Adds advanced filtering (5 QA)
- Adds real-time dashboard updates (5 QA)

**Critical Boundaries:**
- This is Subwave 2.1 of Wave 2.0 (14 total subwaves)
- First subwave in Wave 2.0 execution sequence
- Must complete before Subwave 2.2 can start

---

## Scope Definition

### QA Components to Implement

**Total Test Count:** 15 tests  
**Test Location:** `tests/wave2_0_qa_infrastructure/test_enhanced_dashboard.py`

**Enhanced Dashboard Features:**
- **Drill-Down Navigation** (QA-401 to QA-405): 5 tests
  - QA-401: Navigate from RED status to root cause (verify drill-down path, evidence retrieval)
  - QA-402: Navigate from AMBER status to reason (verify reason display, supporting data)
  - QA-403: Navigate to evidence artifacts (verify retrieval, display, immutability)
  - QA-404: Multi-level drill-down (verify breadcrumb trail, back navigation, state preservation)
  - QA-405: Drill-down error handling (verify evidence not found, broken link handling)

- **Advanced Filtering** (QA-406 to QA-410): 5 tests
  - QA-406: Filter dashboard by domain (verify domain selection, display updates)
  - QA-407: Filter dashboard by status (verify GREEN/AMBER/RED filtering, multi-select)
  - QA-408: Filter dashboard by time range (verify date range selection, data reload)
  - QA-409: Filter dashboard by component (verify component selection, hierarchy filtering)
  - QA-410: Filter combination (verify multiple filters together, AND/OR logic)

- **Real-Time Dashboard Updates** (QA-411 to QA-415): 5 tests
  - QA-411: Real-time status update via WebSocket (verify push notification, UI update)
  - QA-412: Real-time domain addition (verify new domain appears, no page reload)
  - QA-413: Real-time evidence linking (verify evidence updates, notification)
  - QA-414: Real-time connection loss handling (verify fallback to polling, reconnection)
  - QA-415: Real-time update throttling (verify rate limiting, batch updates, no spam)

### Out of Scope
- ❌ Parking Station features — Subwave 2.2, do not modify
- ❌ System optimizations — Subwaves 2.3+, do not modify
- ❌ Any API, Schema, or Integration components — other builders
- ❌ Extended dashboard QA beyond QA-401 to QA-415

---

## Input Artifacts

### Architecture (Frozen)
- **Wave 2 Architecture Specification** (to be frozen before Wave 2.0 starts)
- Section: Enhanced Dashboard (expansion of Wave 1 Dashboard)
- All component contracts defined and frozen

### References
- **WAVE_2_ROLLOUT_PLAN.md** — Section II, Subwave 2.1 specification
- **WAVE_2_IMPLEMENTATION_PLAN.md** — Wave 2 scope and objectives
- **FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md** — Wave 1 Dashboard foundation

### QA Catalog
- **QA_CATALOG.md** (Updated for Wave 2 - BL-019 Corrections)
- QA-401 to QA-415 specifications

### Test Suite (RED)
- **Location:** `tests/wave2_0_qa_infrastructure/test_enhanced_dashboard.py`
- **Status:** All 15 tests RED (awaiting implementation)
- **Prerequisite:** Wave 2 QA-to-Red compilation complete ✅ (BL-019 Corrections)

---

## Task

### Primary Objective
**Implement Enhanced Dashboard features to make all 15 RED tests GREEN.**

### Implementation Requirements

1. **Enhance Dashboard Module Structure**
   - Extend existing `ui/src/components/dashboard/` structure
   - Create drill-down components
   - Create filtering components
   - Create real-time update components
   - All enhancements integrate with Wave 1 Dashboard

2. **Implement Enhanced Features**
   - Implement drill-down navigation per frozen architecture
   - Implement advanced filtering per frozen architecture
   - Implement real-time updates per frozen architecture
   - Follow architecture contracts exactly
   - Ensure tenant isolation via `organisation_id`
   - Use type hints throughout

3. **Achieve Build-to-Green**
   - Make all 15 tests GREEN
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
- Read frozen Wave 2 architecture (Enhanced Dashboard section)
- Review QA catalog (QA-361 to QA-375)
- Inspect RED test suite (`tests/wave2_0_qa_infrastructure/`)
- Understand test expectations and enhanced feature contracts

### Step 2: Enhance Dashboard Module
- Extend existing dashboard components
- Create drill-down navigation components
- Create advanced filtering components
- Create real-time update handlers

### Step 3: Implement Enhanced Features
- Implement each enhanced feature per architecture spec
- Follow test-driven approach: let tests define expected behavior
- Ensure integration with existing Wave 1 Dashboard
- Ensure tenant isolation in all data operations

### Step 4: Validate Tests
```bash
pytest tests/wave2_0_qa_infrastructure/test_dashboard_enhanced_*.py -v
```

**Expected:** 15/15 tests GREEN, zero failures

### Step 5: Checkpoint Reporting (MANDATORY at 50%)
At **7-8 QA complete**, report checkpoint status:

**Checkpoint Report Format:**
```markdown
## Checkpoint 1 (50% - 7/15 QA complete)

**Status:** ON_TRACK | BLOCKED

**Details:**
- QA completed: [list QA-361 to QA-367 or similar]
- QA remaining: [list remaining]
- Impediments: [none | list specific blockers]
- Timeline: [on track | revised estimate with reason]
```

**FM Review:** FM will review checkpoint within 24 hours

### Step 6: Perform Code Checking
- Review all generated code for correctness
- Verify architecture alignment
- Check for defects and edge cases
- Document findings in completion report

### Step 7: Generate Evidence
- Generate Builder QA Report with code checking evidence
- Document completion with COMPLETE terminal state
- List all implemented enhanced features
- Evidence artifacts:
  - `evidence/wave-2.0/ui-builder/subwave-2.1/qa_test_results.xml`
  - `evidence/wave-2.0/ui-builder/subwave-2.1/qa_evidence_summary.json`
  - `WAVE_2.1_BUILDER_COMPLETION_REPORT.md`

### Step 8: Submit for Gate Validation
- Commit all changes to new PR
- Push to PR
- Report COMPLETE state to FM
- Request FM gate validation

---

## Success Criteria

### Gate Requirements (GATE-SUBWAVE-2.1)

- ✅ All 15 QA GREEN (100% pass rate)
- ✅ Checkpoint 1 (50%) reported
- ✅ Zero test debt (no skips, no TODOs, no incomplete tests)
- ✅ Architecture alignment verified (100% from frozen spec)
- ✅ Code checking performed and documented
- ✅ Evidence artifacts complete
- ✅ Builder completion report submitted with COMPLETE terminal state
- ✅ FM gate review PASS

**Gate Pass:** ALL requirements satisfied  
**Gate Fail:** ANY requirement not satisfied

---

## Constraints

### MUST NOT
- ❌ Modify frozen Wave 2 architecture
- ❌ Modify test suite (unless correcting obvious test bugs)
- ❌ Modify governance documents
- ❌ Skip, comment out, or mark tests as TODO
- ❌ Add test debt
- ❌ Deviate from frozen architecture specifications
- ❌ Modify Wave 1 Dashboard code beyond integration points
- ❌ Modify constitutional files (`.github/workflows/`, `BUILD_PHILOSOPHY.md`, `foreman/`, `governance/`)

### MUST
- ✅ Implement exactly as specified in frozen Wave 2 architecture
- ✅ Make all 15 tests GREEN
- ✅ Achieve Build-to-Green on first attempt
- ✅ Report checkpoint at 50% (7-8 QA complete)
- ✅ Maintain zero test debt
- ✅ Follow BUILD_PHILOSOPHY.md principles
- ✅ Perform mandatory code checking with evidence
- ✅ Generate complete evidence artifacts
- ✅ Report only in BLOCKED or COMPLETE terminal states

---

## Execution State Discipline (Terminal States Only)

### Allowed Execution States

1. **BLOCKED** — Execution cannot proceed due to:
   - Missing dependencies
   - Unresolved ambiguity in requirements
   - Platform/environment failure
   - Clarification required from FM

2. **COMPLETE** — Execution finished with:
   - 15/15 tests GREEN (100%)
   - Checkpoint 1 reported
   - Zero test debt
   - All evidence artifacts generated
   - Code checking performed and documented
   - Ready for FM gate review

### Prohibited Execution States

❌ **PARTIAL PROGRESS** — Not a valid state  
❌ **INCREMENTAL COMPLETION** — Not recognized  
❌ **PERCENTAGE REPORTS** — Not acceptable (e.g., "12/15 tests passing")  
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
  - 15/15 tests GREEN confirmation
  - Checkpoint 1 report included
  - Evidence artifacts location
  - Code checking evidence documented
  - Builder completion report
  - FM gate review request
- Submit ONLY when 100% complete
- NO partial submissions

**NEVER REPORT:**
- Partial pass counts (e.g., "12/15 tests passing")
- Progress percentages (e.g., "80% complete")
- Incremental status updates (e.g., "Drill-down done, working on filtering")
- Work-in-progress checkpoints beyond mandated 50% checkpoint

---

## Builder Appointment Package

### 1. Scope Statement
- **QA Range:** QA-361 to QA-375
- **QA Count:** 15 components
- **Complexity:** LOW
- **Duration:** 4-6 days

### 2. Architecture References
- Wave 2 Architecture Specification (Enhanced Dashboard section)
- Wave 1 Dashboard subsystem (integration points)
- WebSocket connection patterns (for real-time updates)

### 3. QA-to-Red Confirmation
- All 15 QA (QA-361 to QA-375) must be in RED state before execution
- QA-to-Red traceability to architecture verified by FM
- Expected GREEN criteria: Enhanced Dashboard features functional per architecture

### 4. Execution State Discipline
- OPOJD terminal states: BLOCKED or COMPLETE only
- Checkpoint required at 50% (7-8 QA complete)
- Escalate immediately if blocked or uncertain

### 5. Evidence Requirements
- Test results: `evidence/wave-2.0/ui-builder/subwave-2.1/qa_test_results.xml`
- Evidence summary: `evidence/wave-2.0/ui-builder/subwave-2.1/qa_evidence_summary.json`
- Completion report: `WAVE_2.1_BUILDER_COMPLETION_REPORT.md`

### 6. Governance References
- **BUILD_PHILOSOPHY.md** — One-Time Build Correctness
- **governance/specs/IN_BETWEEN_WAVE_RECONCILIATION_SPEC.md** — IBWR learnings
- **.github/agents/ui-builder.md** — ui-builder contract
- **governance/canon/BOOTSTRAP_EXECUTION_LEARNINGS.md** — BL-016, BL-018, BL-019

---

## Dependencies

### Prerequisites (Blocking)
- ✅ **Wave 1.0 Complete** — 210/210 QA GREEN (SATISFIED)
- ⏳ **Wave 2 Architecture Frozen** — Pending
- ⏳ **Wave 2 QA-to-Red Complete** — Pending (QA-361 to QA-375 must be RED)
- ⏳ **Platform Readiness GREEN** — Pending verification
- ⏳ **Wave 2.0 Authorization** — CS2 (Johan) approval required

### Downstream Dependencies
- **Subwave 2.2** (Parking Station Advanced) — BLOCKED until GATE-SUBWAVE-2.1 PASS
- **Subwave 2.3** (System Optimizations Phase 1) — BLOCKED until GATE-SUBWAVE-2.1 PASS

### Parallel Execution
- **None** — Subwave 2.1 must complete before other subwaves can start

---

## Parallelism and Sequencing

### Blocking Condition
- This subwave is **BLOCKED** until:
  - Wave 2.0 authorization granted by CS2
  - Wave 2 architecture frozen
  - Wave 2 QA-to-Red complete (QA-361 to QA-375 RED)
  - Platform readiness confirmed GREEN

### Sequential Execution
- Subwave 2.1 must complete and pass gate before:
  - Subwave 2.2 can start (ui-builder)
  - Subwave 2.3 can start (api-builder)

### No Parallel Execution
- Subwave 2.1 is the entry point for Wave 2.0
- No other subwaves can execute in parallel

---

## Governance Reference

### Binding Documents
- **BUILD_PHILOSOPHY.md** — One-Time Build Correctness principle
- **governance/specs/IN_BETWEEN_WAVE_RECONCILIATION_SPEC.md** — IBWR mandatory execution
- **.github/agents/ForemanApp-agent.md v3.3.0** — FM authority and IBWR enforcement
- **.github/agents/ui-builder.md** — ui-builder contract and boundaries

### Wave 2 Hardening
- ✅ **Workload Limit:** 15 QA ≤ 20 max for ui-builder (COMPLIANT)
- ✅ **Checkpoint Required:** Yes, at 50% (>10 QA)
- ✅ **Complete Appointment Package:** All 6 elements included
- ✅ **Proactive Escalation:** Triggers defined
- ✅ **Terminal State Discipline:** BLOCKED or COMPLETE only

### Active Learnings Applied
- **BL-016:** Proactive complexity assessment (LOW complexity, within limits)
- **BL-018:** Platform constraints (workload sizing enforced)
- **BL-019:** Mandatory code checking (required with evidence)

---

## FM Support

### Architecture Questions
- Refer to frozen Wave 2 architecture (Enhanced Dashboard section)
- Escalate if architecture ambiguities discovered

### Test Questions
- Refer to test suite (`tests/wave2_0_qa_infrastructure/test_dashboard_enhanced_*.py`)
- Tests define expected behavior precisely

### Governance Questions
- Refer to BUILD_PHILOSOPHY.md
- Refer to BOOTSTRAP_EXECUTION_LEARNINGS.md
- Escalate if governance clarification needed

### Execution Clarifications
- Use BLOCKED state to request FM guidance
- Do not proceed with assumptions
- Checkpoint reporting mandatory at 50%

---

## Next Steps After Subwave 2.1

### Upon COMPLETE Submission
1. FM conducts GATE-SUBWAVE-2.1 review
2. FM declares gate PASS or FAIL
3. If PASS: FM approves Subwave 2.1 PR for merge
4. CS2 merges Subwave 2.1 PR to main
5. **FM authorizes Subwave 2.2 execution**
6. Builder receives Subwave 2.2 instruction

### Wave 2.0 Progression
- Subwave 2.1 complete → Subwave 2.2 ready
- 13 more subwaves to complete for Wave 2.0
- Wave 2.0 completes when all 14 subwaves PASS

---

## Deliverables

1. **Production Code**
   - Enhanced Dashboard components in `ui/src/components/dashboard/`
   - Drill-down navigation components
   - Advanced filtering components
   - Real-time update handlers
   - All supporting modules

2. **Test Results**
   - All 15 tests GREEN
   - Test execution output
   - Evidence artifacts

3. **Documentation**
   - Builder QA Report (`WAVE_2.1_BUILDER_COMPLETION_REPORT.md`)
   - Checkpoint 1 report (embedded in completion report)
   - Code checking evidence statement
   - Completion summary with COMPLETE terminal state

---

## Timeline Expectation

**Phase:** Build-to-Green implementation  
**Estimated Duration:** 4-6 days  
**Checkpoint:** 50% at 2-3 days  
**Critical Path:** Yes (first subwave in Wave 2.0)

---

## Builder Reminders

### Critical Points
1. **100% = 100%** — 14/15 = FAIL. Only 15/15 = PASS.
2. **Checkpoint Mandatory** — Report at 50% (7-8 QA complete).
3. **No Test Dodging** — Flaky tests are blockers, not acceptable debt.
4. **Terminal States Only** — Report BLOCKED or COMPLETE. No percentages.
5. **Code Checking Mandatory** — Self-review required with evidence.
6. **Scope Discipline** — Enhanced Dashboard ONLY (QA-361 to QA-375).
7. **First Subwave** — Sets the tone for Wave 2.0 execution.

### If Uncertain
- **STOP and ask FM** — Clarity is better than assumption.
- **Use BLOCKED state** — Not a failure, it's correct governance.
- **Reference governance docs** — All learnings documented and binding.

---

## FM Authorization

**Status:** READY FOR AUTHORIZATION (pending Wave 2.0 prerequisites)  
**Authorization Pending:**
- Wave 2.0 authorization by CS2 (Johan)
- Wave 2 architecture freeze
- Wave 2 QA-to-Red compilation
- Platform readiness GREEN

**Once Authorized:**
- FM will issue execution authorization
- Builder will create new PR and execute
- Subwave 2.1 will be first Wave 2.0 execution

**Authority:** Maturion Foreman (FM)  
**FM Agent Contract Version:** 3.3.0  
**Rollout Plan Reference:** WAVE_2_ROLLOUT_PLAN.md Section II, Subwave 2.1

---

**END SUBWAVE 2.1 BUILDER SUB-ISSUE SPECIFICATION**
