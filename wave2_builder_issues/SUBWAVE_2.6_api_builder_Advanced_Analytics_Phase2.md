# Subwave 2.6: Advanced Analytics Phase2 — api-builder Build-to-Green

**Wave:** 2.0  
**Subwave:** 2.6  
**Builder:** api-builder  
**QA Range:** QA-446 to QA-460 (15 QA components)  
**Complexity:** HIGH  
**Duration Estimate:** 5-7 days  
**Dependencies:** GATE-SUBWAVE-2.5 PASS  
**Status:** CORRECTED (BL-019 Emergency QA Range Correction)

---

## Executive Summary

Implement **Advanced Analytics Phase2** features to make **15 RED tests GREEN**.

**Mission:** Per WAVE_2_ROLLOUT_PLAN.md Section II, Subwave 2.6.

---

## Scope Definition

### QA Components
**Total:** 15 tests  
**Location:** `tests/wave2_0_qa_infrastructure/test_advanced_analytics_phase2.py`  
**Range:** QA-446 to QA-460

**Test Categories:**
- **Trend Analysis** (QA-446 to QA-450): 5 tests
- **Predictive Analytics** (QA-451 to QA-455): 5 tests
- **Custom Report Generation** (QA-456 to QA-460): 5 tests

### Out of Scope
- Other subwave QA ranges

---

## Builder Appointment Package

1. **Scope Statement**
   - QA Range: QA-446 to QA-460
   - QA Count: 15 components
   - Complexity: HIGH
   - Duration: 5-7 days

2. **Architecture References**
   - Wave 2 Architecture Specification (Advanced Analytics Phase2 section)
   - Integration points per rollout plan

3. **QA-to-Red Confirmation**
   - All 15 QA in RED state before execution

4. **Execution State Discipline**
   - Terminal states: BLOCKED or COMPLETE only
   - **Checkpoint Required:** At 50% (7 QA complete)

5. **Evidence Requirements**
   - Test results: `evidence/wave-2.0/api-builder/subwave-2.6/qa_test_results.xml`
   - Evidence summary: `evidence/wave-2.0/api-builder/subwave-2.6/qa_evidence_summary.json`
   - Completion report: `WAVE_2.6_BUILDER_COMPLETION_REPORT.md`

6. **Governance References**
   - BUILD_PHILOSOPHY.md — One-Time Build Correctness
   - .github/agents/api-builder.md — Builder contract
   - BL-016, BL-018, BL-019 learnings

---

## Success Criteria

### Gate Requirements (GATE-SUBWAVE-2.6)

- ✅ All 15 QA GREEN (100%)
- ✅ Checkpoint at 50% reported
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
2. **COMPLETE** — 15/15 GREEN, all artifacts ready

### Prohibited States
❌ Partial progress reports  
❌ Percentage updates  
❌ Incremental submissions

---

## Dependencies

### Prerequisites (Blocking)
- ⏳ **GATE-SUBWAVE-2.5 PASS** — BLOCKING

### Downstream Dependencies
- Later subwaves BLOCKED until GATE-SUBWAVE-2.6 PASS

---

## Parallelism and Sequencing

### Blocking Condition
- **BLOCKED** until GATE-SUBWAVE-2.5 PASS

### Sequential Execution
- Must complete before later dependent subwaves

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
   - 15/15 tests GREEN on first attempt
   - Zero test debt

4. **Code Checking (Mandatory)**
   - Self-review all generated code
   - Document evidence

---

## Validation

```bash
pytest tests/wave2_0_qa_infrastructure/test_advanced_analytics_phase2_*.py -v
```

**Expected:** 15/15 GREEN, zero failures

---

## Deliverables

1. **Production Code**
   - Implementation modules per architecture
   - All supporting code

2. **Test Results**
   - All 15 tests GREEN
   - Evidence artifacts

3. **Documentation**
   - Builder QA Report (`WAVE_2.6_BUILDER_COMPLETION_REPORT.md`)
   - Checkpoint report (at 50%)
   - Code checking evidence
   - COMPLETE terminal state declaration

---

## Timeline Expectation

**Duration:** 5-7 days
**Checkpoint:** 50% at 2 days

---

## Constraints

### MUST NOT
- ❌ Modify frozen architecture
- ❌ Modify test suite
- ❌ Skip tests or add test debt
- ❌ Modify constitutional files

### MUST
- ✅ Implement per frozen architecture
- ✅ 15/15 tests GREEN
- ✅ Build-to-Green on first attempt
- ✅ Report checkpoint at 50%
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
**Rollout Plan Reference:** WAVE_2_ROLLOUT_PLAN.md Section II, Subwave 2.6

---

**END SUBWAVE 2.6 BUILDER SUB-ISSUE SPECIFICATION**
