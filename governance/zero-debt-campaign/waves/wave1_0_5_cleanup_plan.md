# Wave 1.0.5 Cleanup Plan - Final Warning Elimination

**Campaign**: ZWZDI-2026-001  
**Wave**: 1.0.5  
**Type**: REMEDIATION (addresses incomplete planning from original waves)  
**Builders**: API Builder (primary), QA Builder (secondary), UI Builder (tertiary)  
**Status**: PLANNING COMPLETE - AWAITING FM AUTHORIZATION  
**Created**: 2026-01-08

---

## Wave Purpose

Wave 1.0.5 is a **remediation wave** created to address the 477 warnings that were not included in the original campaign wave plans (Waves 1.0 through Foundation).

**Root Cause**: FM incomplete planning (warning inventory not completed before wave scoping)  
**Accountability**: FM (acknowledged in FM_ACCOUNTABILITY_REPORT.md)  
**Impact**: Campaign incomplete despite 6 waves completed

---

## Current State (Baseline)

**Measurement Date**: 2026-01-08 (after Waves 1.0 through Foundation)  
**Command**: `pytest tests/ -v --tb=short`

### Warning Count
- **Total**: 477 warnings
- **DeprecationWarning**: 470 occurrences (115 unique file:line locations)
- **PytestReturnNotNoneWarning**: 7 occurrences (1 file, 7 test functions)

### Test Status
- **Total Tests**: 678 collected
- **Passing**: 628 tests
- **Failing**: 125 tests (NotImplementedError - QA-to-Red, properly documented)
- **QA-to-Red Excluded**: 125 tests (Wave 2.0 future work)
- **Actual Pass Rate**: 628/628 = 100% (excluding QA-to-Red)

### Zero Test Debt Status
✅ **ACHIEVED** - All 21 actual failing tests resolved in previous waves  
❌ **WARNING DEBT** - 477 warnings remain

---

## Target State (Wave 1.0.5 Complete)

**Warnings**: **0 (ZERO)**  
**Test Pass Rate**: 100% (maintained)  
**Test Debt**: 0 (maintained)

### Success Criteria
- [ ] Zero DeprecationWarning occurrences
- [ ] Zero PytestReturnNotNoneWarning occurrences
- [ ] All 628 tests still passing
- [ ] No regression (no new warnings or failures introduced)
- [ ] Evidence package provided by each builder

---

## Cleanup Scope by Warning Type

### Scope 1: DeprecationWarning (470 occurrences, 115 locations)

**Issue**: Python 3.12 deprecated `datetime.utcnow()` in favor of timezone-aware `datetime.now(datetime.UTC)`

**Message**:
```
datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. 
Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
```

**Fix Pattern**:
```python
# BEFORE (deprecated):
from datetime import datetime
timestamp = datetime.utcnow()

# AFTER (correct):
from datetime import datetime, UTC
timestamp = datetime.now(UTC)
```

**Distribution**:
- foreman/ - 54 locations → API Builder
- runtime/ - 26 locations → API Builder
- tests/ - 26 locations → QA Builder
- fm/ - 4 locations → API Builder
- ui/ - 4 locations → UI Builder
- python_agent/ - 1 location → API Builder

---

### Scope 2: PytestReturnNotNoneWarning (7 occurrences, 1 file)

**Issue**: Test functions returning `bool` instead of `None`

**Message**:
```
Test functions should return None, but tests/test_agent_boundary_validation.py::<function> returned <class 'bool'>.
```

**Fix Pattern**:
```python
# BEFORE (incorrect):
def test_example():
    result = validate_something()
    return result  # ❌ WRONG

# AFTER (correct):
def test_example():
    result = validate_something()
    assert result  # ✅ CORRECT
```

**Location**: `tests/test_agent_boundary_validation.py` (7 test functions) → QA Builder

---

## Builder Assignments

### API Builder (Primary) - 345 warnings, 85 files

**Scope**:
- foreman/ (54 files)
- runtime/ (26 files)
- fm/ (4 files)
- python_agent/ (1 file)

**Effort**: 1 day (6-8 hours)

**Files**:
```
foreman/analytics/cost_tracker.py
foreman/analytics/metrics_engine.py
foreman/analytics/storage.py (2 locations)
foreman/analytics/usage_analyzer.py (3 locations)
foreman/cross_cutting/audit_logger.py
foreman/cross_cutting/evidence_store.py (2 locations)
foreman/cross_cutting/memory_manager.py (3 locations)
foreman/cross_cutting/memory_proposal.py
foreman/cross_cutting/notification_dispatcher.py (2 locations)
foreman/cross_cutting/system_health_watchdog.py (11 locations)
foreman/domain/blocker.py (2 locations)
foreman/domain/program.py (2 locations)
foreman/domain/task.py (2 locations)
foreman/domain/wave.py (2 locations)
foreman/flows/flow_executor.py (8 locations)
foreman/intent/approval_manager.py (2 locations)
foreman/intent/intake_handler.py
foreman/runtime/task_manager.py (9 locations)
runtime/cascading_failure_handler.py (6 locations)
runtime/data_consistency_manager.py (4 locations)
runtime/deadlock_detector.py (7 locations)
runtime/race_condition_handler.py (3 locations)
runtime/system_failure_handler.py (6 locations)
fm/orchestration/build_authorization_gate.py
fm/runtime/watchdog/alert_reader.py
fm/runtime/watchdog/escalation_reporter.py (2 locations)
python_agent/memory_proposal_client.py
```

**Task**:
1. For each file:
   - Add `from datetime import UTC` to imports (if not present)
   - Replace all `datetime.utcnow()` with `datetime.now(UTC)`
   - Verify file syntax
   - Run related tests

2. After all files complete:
   - Run full test suite
   - Verify 0 DeprecationWarnings in scope
   - Provide evidence package

---

### QA Builder (Secondary) - 132 warnings, 27 files

**Scope**:
- tests/ (26 files with datetime warnings)
- tests/test_agent_boundary_validation.py (7 return warnings)

**Effort**: 0.5 day (3-4 hours)

**Datetime Files**:
```
tests/test_build_authorization_gate.py (2 locations)
tests/wave1_0_qa_infrastructure/analytics/test_cost_tracker.py (13 locations)
tests/wave1_0_qa_infrastructure/cross_cutting/test_other_components.py
tests/wave2_0_qa_infrastructure/conftest.py
tests/wave2_0_qa_infrastructure/test_governance_advanced_integration.py (6 locations)
tests/wave2_0_qa_infrastructure/test_governance_advanced_security.py (5 locations)
```

**Return Warning File**:
```
tests/test_agent_boundary_validation.py (7 test functions)
```

**Task 1** (Datetime):
1. For each test file:
   - Add `from datetime import UTC` to imports
   - Replace all `datetime.utcnow()` with `datetime.now(UTC)`
   - Run test file to verify
   
**Task 2** (Return):
1. Open `tests/test_agent_boundary_validation.py`
2. Find 7 test functions with `return <bool>` statements:
   - test_valid_builder_qa
   - test_valid_fm_qa
   - test_valid_governance_qa
   - test_cross_agent_violation_builder_to_governance
   - test_cross_agent_violation_fm_to_builder
   - test_missing_metadata
   - test_no_reports
3. Replace each `return <expr>` with `assert <expr>`
4. Run file tests to verify

**Task 3** (Verification):
1. Run full test suite
2. Verify 0 warnings in test scope
3. Provide evidence package

---

### UI Builder (Tertiary) - 16 warnings, 4 files

**Scope**:
- ui/dashboard/ (4 files)

**Effort**: 0.25 day (2 hours)

**Files**:
```
ui/dashboard/enhanced_dashboard.py
ui/dashboard/enhanced_drilldown.py
ui/dashboard/enhanced_notifications.py
ui/dashboard/enhanced_realtime.py
```

**Task**:
1. For each file:
   - Add `from datetime import UTC` to imports
   - Replace `datetime.utcnow()` with `datetime.now(UTC)`
   - Run UI tests to verify

2. After all files complete:
   - Run full test suite
   - Verify 0 DeprecationWarnings in UI scope
   - Provide evidence package

---

## Execution Strategy

### Timeline: 1.5 days (with parallelization)

#### Day 1 (Morning - Hours 0-4)
- **API Builder**: Start cleanup (foreman/, runtime/, fm/, python_agent/)
  - Focus on high-volume files first
  - Verify after each subsystem complete
- **QA Builder**: WAIT (blocked on API Builder 50% complete)
- **UI Builder**: WAIT (blocked on API Builder 50% complete)

#### Day 1 (Afternoon - Hours 4-8)
- **API Builder**: Continue cleanup, reach 75% complete
- **QA Builder**: Start datetime cleanup in test files (can parallelize)
- **UI Builder**: Start ui/ cleanup (can parallelize)

#### Day 2 (Morning - Hours 0-4)
- **API Builder**: Complete remaining files, run full verification
- **QA Builder**: Complete datetime + return fixes, run full verification
- **UI Builder**: Complete ui/ files, run full verification
- **FM**: Verify 0 warnings, collect evidence from all builders

---

## Verification Methodology

### Per-Builder Verification (During Implementation)

**API Builder**:
```bash
# After fixing foreman/ subsystem:
pytest tests/ -k "foreman" --tb=short -W all

# After fixing runtime/ subsystem:
pytest tests/ -k "runtime" --tb=short -W all

# After all API Builder work:
pytest tests/ --tb=short -W all | grep -c "DeprecationWarning"
# Expected: Count significantly reduced
```

**QA Builder**:
```bash
# After fixing test files:
pytest tests/test_build_authorization_gate.py --tb=short -W all
pytest tests/wave1_0_qa_infrastructure/ --tb=short -W all
pytest tests/wave2_0_qa_infrastructure/ --tb=short -W all

# After fixing return warnings:
pytest tests/test_agent_boundary_validation.py -W all
# Expected: 0 PytestReturnNotNoneWarning
```

**UI Builder**:
```bash
# After fixing ui/ files:
pytest tests/ -k "ui or dashboard" --tb=short -W all
# Expected: 0 DeprecationWarning in UI scope
```

---

### Full Suite Verification (After Wave 1.0.5 Complete)

**Command**:
```bash
pytest tests/ -v --tb=short
```

**Expected Output**:
```
====== 628 passed, 125 failed (QA-to-Red) in X seconds ======
(NO "warnings summary" section)
```

**Strict Warnings Check**:
```bash
pytest tests/ --strict-warnings -k "not test_qa"
```

**Expected**: All non-QA-to-Red tests pass with zero warnings

---

## Evidence Requirements

### Each Builder Must Provide

#### 1. Before State Evidence
- **Command**: `pytest tests/ --tb=no -W all 2>&1 | grep "<WarningType>" | wc -l`
- **Screenshot**: Terminal output showing warning count BEFORE cleanup
- **File**: `WAVE_1_0_5_<builder>_BEFORE.txt`

#### 2. Work Evidence
- **Git Diff**: All files modified with datetime.utcnow() replacements
- **File List**: List of all files changed
- **Commit**: Single commit with message "Wave 1.0.5: Eliminate DeprecationWarnings in <scope>"

#### 3. After State Evidence
- **Command**: Same as before, showing 0 warnings
- **Screenshot**: Terminal output showing warning count AFTER cleanup
- **File**: `WAVE_1_0_5_<builder>_AFTER.txt`

#### 4. Test Pass Evidence
- **Command**: `pytest tests/ -v --tb=short`
- **Screenshot**: Terminal output showing all tests passing
- **Regression Check**: No new failures introduced

#### 5. Completion Summary
- **File**: `WAVE_1_0_5_<builder>_COMPLETION_SUMMARY.md`
- **Contents**:
  - Warning count before/after
  - Files modified (count and list)
  - Test results (before/after)
  - Effort actual vs. estimate
  - Issues encountered (if any)

---

## Success Criteria Checklist

### API Builder Success
- [ ] All 85 files in scope modified
- [ ] All datetime.utcnow() replaced with datetime.now(UTC)
- [ ] UTC imported in all modified files
- [ ] No syntax errors introduced
- [ ] All related tests passing
- [ ] DeprecationWarning count in scope: 0
- [ ] Evidence package complete

### QA Builder Success
- [ ] All 26 test files modified (datetime)
- [ ] 7 test functions fixed (return → assert)
- [ ] All datetime.utcnow() replaced
- [ ] All return statements replaced with assertions
- [ ] PytestReturnNotNoneWarning count: 0
- [ ] DeprecationWarning count in test scope: 0
- [ ] All tests passing (no regression)
- [ ] Evidence package complete

### UI Builder Success
- [ ] All 4 ui/dashboard/ files modified
- [ ] All datetime.utcnow() replaced
- [ ] UTC imported in all modified files
- [ ] UI tests passing
- [ ] DeprecationWarning count in UI scope: 0
- [ ] Evidence package complete

### FM Verification Success
- [ ] All builder evidence packages received
- [ ] Full suite runs with 0 warnings: `pytest tests/ -v --tb=short`
- [ ] Test pass rate maintained: 628 passing
- [ ] No regression: 0 new failures
- [ ] Strict warnings passes: `pytest tests/ --strict-warnings -k "not test_qa"`

---

## Wave 1.0.5 Completion Gate

**FM MUST verify ALL before accepting wave completion**:

1. **Warning Count Verification**:
   - [ ] Run: `pytest tests/ --tb=no -W all 2>&1 | tee wave1_0_5_final_check.txt`
   - [ ] Check: `grep -c "DeprecationWarning" wave1_0_5_final_check.txt` → Expected: 0
   - [ ] Check: `grep -c "PytestReturnNotNoneWarning" wave1_0_5_final_check.txt` → Expected: 0
   - [ ] Total warning count: **ZERO**

2. **Test Pass Verification**:
   - [ ] Run: `pytest tests/ -v --tb=short`
   - [ ] Check: 628 passed (maintained)
   - [ ] Check: 0 new failures
   - [ ] Check: No test regression

3. **Evidence Collection**:
   - [ ] API Builder evidence package received
   - [ ] QA Builder evidence package received
   - [ ] UI Builder evidence package received
   - [ ] All before/after counts documented
   - [ ] All file diffs provided

4. **Governance Compliance**:
   - [ ] COMPLETE_WARNING_INVENTORY.md updated with "RESOLVED" status
   - [ ] FM_ACCOUNTABILITY_REPORT.md marked complete
   - [ ] Wave 1.0.5 execution logged in PROGRESS_TRACKER.md
   - [ ] Zero-warning baseline documented for future reference

**Gate Decision**:
- **PASS**: ALL checks green → Wave 1.0.5 COMPLETE, campaign proceeds to Prevention Phase
- **FAIL**: ANY check red → Wave 1.0.5 INCOMPLETE, assigned builders must remediate

---

## Risk Mitigation

### Risk 1: Regression Introduced by Datetime Changes

**Likelihood**: LOW  
**Impact**: MEDIUM  
**Mitigation**:
- Mechanical transformation (search-and-replace)
- UTC behavior identical to utcnow() for naive datetime
- Comprehensive test coverage exists
- Per-file verification after each change

**Contingency**: If regression found, revert specific file and investigate

---

### Risk 2: Builder Unavailability

**Likelihood**: LOW  
**Impact**: HIGH  
**Mitigation**:
- API Builder owns 72% of work (critical path)
- QA and UI Builders can start after API Builder 50% complete
- Work is parallelizable after critical path clear

**Contingency**: CS2 can reassign work to available builder if unavailability confirmed

---

### Risk 3: Unexpected Warning Types

**Likelihood**: VERY LOW  
**Impact**: LOW  
**Mitigation**:
- Complete inventory performed (122 unique locations catalogued)
- Only 2 warning types found (DeprecationWarning, PytestReturnNotNoneWarning)
- Both types well-understood with known fixes

**Contingency**: If new warning type discovered, HALT and escalate to FM

---

### Risk 4: Test Suite Too Slow for Iteration

**Likelihood**: MEDIUM  
**Impact**: LOW  
**Mitigation**:
- Builders can run subset tests during development
- Use `pytest tests/ -k "keyword"` for targeted testing
- Full suite run only at end of builder's work

**Contingency**: Accept longer verification time, prioritize correctness over speed

---

## Dependencies and Blockers

### Dependencies
- **API Builder must complete first** (owns 72% of warnings)
- **QA and UI Builders** can start after API Builder 50% complete
- **FM verification** requires all three builders complete

### Blockers
- None identified (work is independent, no external dependencies)

---

## Post-Wave Actions

After Wave 1.0.5 complete and FM-verified:

1. **Update PROGRESS_TRACKER.md**:
   - Mark Wave 1.0.5 complete
   - Document final warning count: 0
   - Document final test pass rate: 100%

2. **Create Baseline Documentation**:
   - Document zero-warning state as new baseline
   - Store evidence for future audits
   - Reference in governance policies

3. **Proceed to Prevention Phase** (Issue #507):
   - Update governance policies
   - Establish CI zero-warning gate
   - Update builder contracts
   - Create bootstrap learning entry

---

## Lessons for Future Waves

### What We Learned from This Remediation

1. **Complete Inventory BEFORE Planning**:
   - Never defer categorization to execution phase
   - Always complete warning inventory during planning
   - Verify sum of wave counts equals baseline

2. **Verification Must Include Warning Checks**:
   - Test passage is necessary but not sufficient
   - Warning elimination must be verified explicitly
   - Evidence must include before/after warning counts

3. **Daily Audits Prevent Surprises**:
   - Daily warning count tracking catches regressions early
   - Trend analysis identifies problems before completion
   - Real-time visibility enables corrective action

4. **Evidence-Based Verification**:
   - Self-certification without evidence is unreliable
   - Quantitative proof (counts, logs, screenshots) required
   - FM verification cannot rely on builder confirmation alone

---

**Document**: Wave 1.0.5 Cleanup Plan  
**Status**: COMPLETE (planning), AWAITING AUTHORIZATION (execution)  
**Created**: 2026-01-08  
**Author**: Foreman (FM)  
**Authority**: CS2 (Johan Ras)
