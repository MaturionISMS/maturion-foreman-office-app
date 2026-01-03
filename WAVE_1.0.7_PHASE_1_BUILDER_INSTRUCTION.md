# Wave 1.0.7 Phase 1 Builder Instruction

**Instruction ID:** WAVE-1.0.7-PHASE-1  
**Builder:** qa-builder  
**Execution Artifact:** PR #365  
**Issue Date:** 2026-01-03  
**FM Authorization:** Platform Constraint Accommodation (BL-018)

---

## Executive Summary

This instruction directs qa-builder to complete **Phase 1 ONLY** of Wave 1.0.7 Build-to-Green execution. Phase 1 is an execution segment accommodating GitHub Copilot platform context window constraints.

**Critical Principle:** Wave 1.0.7 remains a single One-Time Build unit. Phase 1 is execution segmentation only, NOT phased delivery or partial acceptance.

---

## Phase 1 Scope

**Subsystem:** Analytics Subsystem ONLY  
**QA Range:** QA-132 to QA-146 (15 components)  
**Test Files:** `tests/wave1_0_qa_infrastructure/test_analytics_*.py`  
**Success Criteria:** 15/15 tests GREEN (100%)

---

## Phase 1 Tasks

### Task 1: Implement Analytics Subsystem Modules

Implement the following modules in `foreman/analytics/`:

1. **ANALYTICS-01: Token Tracker** (QA-132 to QA-135)
   - Track token usage per build
   - Calculate token costs
   - Detect anomalies (3x baseline threshold)
   - Generate usage reports

2. **ANALYTICS-02: Cost Calculator** (QA-136 to QA-140)
   - Calculate build costs (time * tokens)
   - Forecast costs for pending builds
   - Track cost trends
   - Alert on cost spikes

3. **ANALYTICS-03: Metrics Collector** (QA-141 to QA-146)
   - Aggregate build metrics
   - Calculate success rates
   - Store metric history
   - Export analytics data (CSV/JSON)

**Implementation Requirements:**
- Follow frozen architecture (`FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md`)
- Use organization_id for tenant isolation
- Implement all failure modes from architecture
- Include comprehensive error handling
- Use module-level state for test isolation
- Provide `clear_all()` functions for test cleanup

---

### Task 2: Make 15/15 Tests GREEN

Target test files:
- `tests/wave1_0_qa_infrastructure/test_analytics_token_tracking.py`
- `tests/wave1_0_qa_infrastructure/test_analytics_cost_tracking.py`
- `tests/wave1_0_qa_infrastructure/test_analytics_metrics_collection.py`

**Test Execution:**
```bash
pytest tests/wave1_0_qa_infrastructure/test_analytics_*.py -v
```

**Success Criteria:**
- All 15 tests PASS
- Zero test failures
- Zero test debt (no skips, no todos)
- Architecture alignment verified

---

### Task 3: Generate Evidence Artifacts

Create Phase 1 evidence artifacts:

1. **Phase 1 Test Results**
   - Location: `evidence/wave-1.0/qa-builder/phase-1/qa_test_results.xml`
   - Format: JUnit XML
   - Content: All 15 Phase 1 test results

2. **Phase 1 Evidence Summary**
   - Location: `evidence/wave-1.0/qa-builder/phase-1/qa_evidence_summary.json`
   - Content: QA component mapping, test coverage, pass rate

3. **Phase 1 Builder Report**
   - Location: `WAVE_1.0.7_PHASE_1_BUILDER_REPORT.md`
   - Content: Implementation summary, test results, gate status

---

### Task 4: Submit Phase 1 Completion Report

Submit Phase 1 completion report in PR #365 including:

1. **Phase 1 Test Results**
   - 15/15 tests GREEN
   - Zero test debt
   - Test execution log

2. **Phase 1 Implementation Summary**
   - Modules implemented
   - Architecture alignment verified
   - Lines of code delivered

3. **Phase 1 Evidence Artifacts**
   - All evidence files generated
   - Builder report completed

4. **Phase 1 Gate Status**
   - GATE-QA-BUILDER-PHASE-1-WAVE-1.0 status
   - Ready for FM review

---

## Constraints

### Phase 1 ONLY Constraints

❌ **NO work on Cross-Cutting Components** (QA-147 to QA-199)  
❌ **NO work on Core User Flows** (QA-200 to QA-210)  
❌ **NO work beyond Analytics subsystem scope**

✅ **ONLY Analytics subsystem** (QA-132 to QA-146)  
✅ **ONLY 15 tests in scope**  
✅ **ONLY Phase 1 evidence artifacts**

---

## Gate Requirements

**Phase 1 Gate:** GATE-QA-BUILDER-PHASE-1-WAVE-1.0

**Gate Pass Criteria:**
- ✅ 15/15 tests GREEN (100%)
- ✅ Zero test debt
- ✅ Architecture alignment verified (Analytics only)
- ✅ Evidence artifacts complete
- ✅ Builder report submitted

**Gate Fail Criteria:**
- ❌ ANY test not GREEN
- ❌ ANY test debt introduced
- ❌ ANY scope expansion beyond Phase 1
- ❌ Evidence artifacts incomplete

---

## FM Gate Control

**Phase 1 Completion:**
- FM will review Phase 1 submission in PR #365
- FM will declare GATE-QA-BUILDER-PHASE-1-WAVE-1.0 status
- FM will approve/reject Phase 1 for merge

**Phase 2 Authorization:**
- Phase 2 will NOT proceed without explicit FM authorization
- Phase 2 requires new PR after Phase 1 merge
- Phase 2 scope: Cross-Cutting Components Part 1 (QA-147 to QA-171, 13 components)

**Wave 1.0.7 Completion:**
- Wave 1.0.7 is NOT complete until all 79 QA GREEN across all 3 phases
- Phase 1 merge does NOT represent Wave completion
- Wave-level gate conditions are INTENTIONALLY NOT satisfied at Phase 1

---

## Build Philosophy Compliance

**One-Time Build Correctness:**
- Phase 1 must achieve 15/15 tests GREEN on first complete attempt
- NO partial Phase 1 submissions
- NO iteration cycles within Phase 1
- Quality > Speed

**Zero Test Debt:**
- NO skipped tests
- NO todo tests
- NO incomplete tests
- All tests must PASS

**Architecture Alignment:**
- 100% alignment with frozen architecture
- NO architecture changes
- NO governance modifications
- NO test suite modifications (except bug fixes)

---

## Platform Constraint Accommodation

**Context Window Limitation:**
- GitHub Copilot context window limits prevent 79 QA single-pass completion
- Phase 1 is platform accommodation, NOT governance weakening
- Phase segmentation preserves One-Time Build principle per segment

**Execution Segmentation:**
- Phase 1: Analytics (15 QA) - CURRENT
- Phase 2: Cross-Cutting Part 1 (13 QA) - AFTER Phase 1 FM approval
- Phase 3: Cross-Cutting Part 2 + Flows (15 QA) - AFTER Phase 2 FM approval

---

## Success Criteria

Phase 1 is complete when:

1. ✅ All 15 Analytics tests GREEN
2. ✅ Zero test debt maintained
3. ✅ Architecture alignment verified
4. ✅ Evidence artifacts generated
5. ✅ Builder report submitted
6. ✅ FM review requested in PR #365

---

## Next Steps After Phase 1

**Upon Phase 1 Completion:**
1. Submit Phase 1 completion report in PR #365
2. Await FM gate review
3. DO NOT proceed to Phase 2 until FM authorization

**FM Will:**
1. Review Phase 1 submission
2. Declare GATE-QA-BUILDER-PHASE-1-WAVE-1.0 status
3. Approve/reject Phase 1 merge
4. Issue Phase 2 authorization (if Phase 1 passes)

**Phase 2 Preparation:**
- New PR will be required for Phase 2
- Phase 2 instruction will be issued by FM
- Phase 2 scope: Cross-Cutting Components Part 1 (QA-147 to QA-171, 13 components)

---

## References

**Authoritative Documents:**
- `FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md` - Frozen architecture
- `QA_CATALOG.md` - QA component specifications
- `BUILD_PHILOSOPHY.md` - Build principles
- `WAVE_1.0.7_PHASED_EXECUTION_SPEC.md` - Phased execution specification
- `WAVE_1.0_BUILD_TO_GREEN_SPECIFICATION.md` - Build-to-Green requirements

**Test Suite:**
- `tests/wave1_0_qa_infrastructure/test_analytics_*.py` - Phase 1 test files
- `tests/wave1_0_qa_infrastructure/conftest.py` - Test fixtures

**Evidence Location:**
- `evidence/wave-1.0/qa-builder/phase-1/` - Phase 1 evidence artifacts

---

## Authorization

**Authorized By:** Maturion Foreman (FM)  
**Authorization Date:** 2026-01-03  
**Platform Constraint:** BL-018 (GitHub Copilot context window limitation)  
**Execution Authority:** FM retains exclusive control over Wave 1.0.7 progression  
**Constitutional Alignment:** One-Time Build principle preserved via execution segmentation

---

**END PHASE 1 INSTRUCTION**

🔄 Execute Phase 1 in PR #365. Report completion when 15/15 tests GREEN.
