# Subwave 2.8: Full Watchdog Coverage — integration-builder Build-to-Green

**Wave:** 2.0  
**Subwave:** 2.8  
**Builder:** integration-builder  
**QA Range:** QA-396 to QA-400 (5 QA components)  
**Complexity:** LOW  
**Duration Estimate:** 2-3 days  
**Dependencies:** GATE-SUBWAVE-2.4 PASS  
**Status:** READY FOR AUTHORIZATION

---

## Executive Summary

Implement **Full Watchdog Coverage** features to make **5 RED tests GREEN**.

**Mission:** Per WAVE_2_ROLLOUT_PLAN.md Section II, Subwave 2.8.

---

## Scope Definition

### QA Components
**Total:** 5 tests  
**Location:** `tests/wave2_0_qa_infrastructure/test_full_watchdog_coverage_*.py`  
**Range:** QA-396 to QA-400

### Out of Scope
- Other subwave QA ranges

---

## Builder Appointment Package

1. **Scope Statement**
   - QA Range: QA-396 to QA-400
   - QA Count: 5 components
   - Complexity: LOW
   - Duration: 2-3 days

2. **Architecture References**
   - Wave 2 Architecture Specification (Full Watchdog Coverage section)
   - Integration points per rollout plan

3. **QA-to-Red Confirmation**
   - All 5 QA in RED state before execution

4. **Execution State Discipline**
   - Terminal states: BLOCKED or COMPLETE only
   - No checkpoint required (≤10 QA)

5. **Evidence Requirements**
   - Test results: `evidence/wave-2.0/integration-builder/subwave-2.8/qa_test_results.xml`
   - Evidence summary: `evidence/wave-2.0/integration-builder/subwave-2.8/qa_evidence_summary.json`
   - Completion report: `WAVE_2.8_BUILDER_COMPLETION_REPORT.md`

6. **Governance References**
   - BUILD_PHILOSOPHY.md — One-Time Build Correctness
   - .github/agents/integration-builder.md — Builder contract
   - BL-016, BL-018, BL-019 learnings

---

## Success Criteria

### Gate Requirements (GATE-SUBWAVE-2.8)

- ✅ All 5 QA GREEN (100%)
- ✅ Zero test debt
- ✅ Architecture alignment verified
- ✅ Code checking performed and documented
- ✅ Evidence artifacts complete
- ✅ Builder completion report with COMPLETE terminal state
- ✅ FM gate review PASS

**Gate Pass:** ALL requirements satisfied  
**Gate Fail:** ANY requirement not satisfied

---

## Execution State Discipline

### Allowed States
1. **BLOCKED** — Cannot proceed due to impediment
2. **COMPLETE** — 5/5 GREEN, all artifacts ready

### Prohibited States
❌ Partial progress reports  
❌ Percentage updates  
❌ Incremental submissions

---

## Dependencies

### Prerequisites (Blocking)
- ⏳ **GATE-SUBWAVE-2.4 PASS** — BLOCKING

### Downstream Dependencies
- Later subwaves BLOCKED until GATE-SUBWAVE-2.8 PASS

---

## Parallelism and Sequencing

### Blocking Condition
- **BLOCKED** until GATE-SUBWAVE-2.4 PASS

### Sequential Execution
- Must complete before later dependent subwaves

### Parallel Execution Possible
- Can execute in parallel with other subwaves after 2.4 (2.5, 2.7, 2.8)

---

## Implementation Requirements

1. **Module Structure**
   - Per frozen architecture specification
   - Organized by functional area

2. **Implementation**
   - Follow architecture contracts exactly
   - Tenant isolation via `organisation_id`
   - Type hints throughout

3. **Build-to-Green**
   - 5/5 tests GREEN on first attempt
   - Zero test debt

4. **Code Checking (Mandatory)**
   - Self-review all generated code
   - Document evidence

---

## Validation

```bash
pytest tests/wave2_0_qa_infrastructure/test_full_watchdog_coverage_*.py -v
```

**Expected:** 5/5 GREEN, zero failures

---

## Deliverables

1. **Production Code**
   - Implementation modules per architecture
   - All supporting code

2. **Test Results**
   - All 5 tests GREEN
   - Evidence artifacts

3. **Documentation**
   - Builder QA Report (`WAVE_2.8_BUILDER_COMPLETION_REPORT.md`)
   - Code checking evidence
   - COMPLETE terminal state declaration

---

## Timeline Expectation

**Duration:** 2-3 days

---

## Constraints

### MUST NOT
- ❌ Modify frozen architecture
- ❌ Modify test suite
- ❌ Skip tests or add test debt
- ❌ Modify constitutional files

### MUST
- ✅ Implement per frozen architecture
- ✅ 5/5 tests GREEN
- ✅ Build-to-Green on first attempt
- ✅ Terminal states only (BLOCKED or COMPLETE)

---

## FM Support

- **Architecture:** Refer to frozen Wave 2 architecture
- **Tests:** Test suite defines behavior
- **Governance:** BUILD_PHILOSOPHY.md, learnings docs
- **Clarifications:** Use BLOCKED state, don't assume

---

## FM Authorization

**Status:** READY FOR AUTHORIZATION (pending dependencies)  
**Authority:** Maturion Foreman (FM)  
**FM Agent Contract Version:** 3.3.0  
**Rollout Plan Reference:** WAVE_2_ROLLOUT_PLAN.md Section II, Subwave 2.8

---

**END SUBWAVE 2.8 BUILDER SUB-ISSUE SPECIFICATION**
