# Complete Warning Inventory - ZWZDI Campaign

**Campaign ID**: ZWZDI-2026-001  
**Issue**: Incomplete Campaign Planning - Wave 1.0.5 Remediation  
**Date**: 2026-01-08  
**Author**: Foreman (FM)  
**Status**: COMPLETE

---

## Executive Summary

This document provides a complete inventory of all 477 warnings found during ZWZDI campaign verification phase. The warnings were not addressed in the original wave plans (Waves 1.0 through Foundation), necessitating Wave 1.0.5 remediation.

**Total Warnings**: 477 occurrences (122 unique locations)
- **DeprecationWarning**: 470 occurrences (115 unique file:line locations)
- **PytestReturnNotNoneWarning**: 7 occurrences (1 file, 7 test functions)

**Why 477 ≠ 122**: Each unique warning location is triggered multiple times during full test suite execution (average 3.9 triggers per location).

---

## Warning Count Reconciliation

### Original Baseline (Planning Phase)
- **Date**: 2026-01-08
- **Count**: 365 warnings
- **Method**: `pytest tests/ -v --tb=short`
- **Status**: INCOMPLETE (did not account for all occurrences)

### Verification Phase Measurement
- **Date**: 2026-01-08 (after waves 1.0-1.0.4)
- **Count**: 477 warnings
- **Method**: `pytest tests/ -v --tb=short`
- **Status**: COMPLETE (full test suite execution)

### Reconciliation
- **Gap**: 477 - 365 = 112 warnings
- **Explanation**: Original baseline did not fully measure all warning occurrences in full suite
- **Unique Locations**: 115 (DeprecationWarning) + 1 (PytestReturnNotNoneWarning) = 116 warning sources

---

## Warning Type 1: DeprecationWarning (470 occurrences, 115 locations)

### Description
Python 3.12 deprecated `datetime.utcnow()` in favor of timezone-aware `datetime.now(datetime.UTC)`.

### Message
```
datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. 
Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
```

### Fix Pattern
```python
# BEFORE (deprecated):
from datetime import datetime
timestamp = datetime.utcnow()

# AFTER (correct):
from datetime import datetime, UTC
timestamp = datetime.now(UTC)
```

### Distribution by Directory

| Directory | Unique Locations | Occurrences | Builder Owner | Priority |
|-----------|------------------|-------------|---------------|----------|
| **foreman/** | 54 | ~211 | API Builder | HIGH |
| **runtime/** | 26 | ~102 | API Builder | HIGH |
| **tests/** | 26 | ~102 | QA Builder | MEDIUM |
| **fm/** | 4 | ~16 | API Builder | HIGH |
| **ui/** | 4 | ~16 | UI Builder | MEDIUM |
| **python_agent/** | 1 | ~4 | API Builder | LOW |
| **TOTAL** | **115** | **~451** | - | - |

**Note**: Occurrence estimates based on average 3.9 triggers per location. Actual count after fix may vary.

---

## Warning Locations: foreman/ (54 locations)

**Owner**: API Builder  
**Reason**: API Builder owns runtime/foreman subsystems per Wave 1.0.3 scope

| File | Line | Context |
|------|------|---------|
| `foreman/analytics/cost_tracker.py` | 77 | `timestamp = datetime.utcnow()` |
| `foreman/analytics/metrics_engine.py` | 84 | `timestamp = datetime.utcnow()` |
| `foreman/analytics/storage.py` | 27 | `cutoff = datetime.utcnow() - timedelta(days=days)` |
| `foreman/analytics/storage.py` | 34 | `h.get("timestamp", datetime.utcnow()) >= cutoff` |
| `foreman/analytics/usage_analyzer.py` | 75 | `"timestamp": datetime.utcnow()` |
| `foreman/analytics/usage_analyzer.py` | 91 | `"timestamp": datetime.utcnow()` |
| `foreman/analytics/usage_analyzer.py` | 107 | `"timestamp": datetime.utcnow()` |
| `foreman/cross_cutting/audit_logger.py` | 34 | (timestamp usage) |
| `foreman/cross_cutting/evidence_store.py` | 38 | (timestamp usage) |
| `foreman/cross_cutting/evidence_store.py` | 39 | (timestamp usage) |
| `foreman/cross_cutting/memory_manager.py` | 57 | `"created_at": datetime.utcnow().isoformat()` |
| `foreman/cross_cutting/memory_manager.py` | 78 | `"timestamp": datetime.utcnow()` |
| `foreman/cross_cutting/memory_manager.py` | 189 | `"timestamp": datetime.utcnow()` |
| `foreman/cross_cutting/memory_proposal.py` | 20 | `self.created_at = datetime.utcnow()` |
| `foreman/cross_cutting/notification_dispatcher.py` | 37 | (timestamp usage) |
| `foreman/cross_cutting/notification_dispatcher.py` | 93 | (timestamp usage) |
| `foreman/cross_cutting/system_health_watchdog.py` | 51 | (timestamp usage) |
| `foreman/cross_cutting/system_health_watchdog.py` | 63 | (timestamp usage) |
| `foreman/cross_cutting/system_health_watchdog.py` | 69 | (timestamp usage) |
| `foreman/cross_cutting/system_health_watchdog.py` | 103 | (timestamp usage) |
| `foreman/cross_cutting/system_health_watchdog.py` | 136 | (timestamp usage) |
| `foreman/cross_cutting/system_health_watchdog.py` | 192 | (timestamp usage) |
| `foreman/cross_cutting/system_health_watchdog.py` | 216 | (timestamp usage) |
| `foreman/cross_cutting/system_health_watchdog.py` | 230 | (timestamp usage) |
| `foreman/cross_cutting/system_health_watchdog.py` | 238 | (timestamp usage) |
| `foreman/cross_cutting/system_health_watchdog.py` | 243 | (timestamp usage) |
| `foreman/domain/blocker.py` | 67 | `self.created_at = datetime.utcnow()` |
| `foreman/domain/blocker.py` | 68 | `self.updated_at = datetime.utcnow()` |
| `foreman/domain/program.py` | 58 | `self.created_at = datetime.utcnow()` |
| `foreman/domain/program.py` | 59 | `self.updated_at = datetime.utcnow()` |
| `foreman/domain/task.py` | 76 | `self.created_at = datetime.utcnow()` |
| `foreman/domain/task.py` | 77 | `self.updated_at = datetime.utcnow()` |
| `foreman/domain/wave.py` | 61 | `self.created_at = datetime.utcnow()` |
| `foreman/domain/wave.py` | 62 | `self.updated_at = datetime.utcnow()` |
| `foreman/flows/flow_executor.py` | 18 | (timestamp usage) |
| `foreman/flows/flow_executor.py` | 19 | (timestamp usage) |
| `foreman/flows/flow_executor.py` | 20 | (timestamp usage) |
| `foreman/flows/flow_executor.py` | 21 | (timestamp usage) |
| `foreman/flows/flow_executor.py` | 22 | (timestamp usage) |
| `foreman/flows/flow_executor.py` | 23 | (timestamp usage) |
| `foreman/flows/flow_executor.py` | 24 | (timestamp usage) |
| `foreman/flows/flow_executor.py` | 25 | (timestamp usage) |
| `foreman/intent/approval_manager.py` | 66 | (timestamp usage) |
| `foreman/intent/approval_manager.py` | 80 | (timestamp usage) |
| `foreman/intent/intake_handler.py` | 31 | (timestamp usage) |
| `foreman/runtime/task_manager.py` | 104 | `task.updated_at = datetime.utcnow()` |
| `foreman/runtime/task_manager.py` | 135 | `task.started_at = datetime.utcnow()` |
| `foreman/runtime/task_manager.py` | 136 | `task.updated_at = datetime.utcnow()` |
| `foreman/runtime/task_manager.py` | 168 | `task.completed_at = datetime.utcnow()` |
| `foreman/runtime/task_manager.py` | 169 | `task.updated_at = datetime.utcnow()` |
| `foreman/runtime/task_manager.py` | 203 | `task.failed_at = datetime.utcnow()` |
| `foreman/runtime/task_manager.py` | 204 | `task.updated_at = datetime.utcnow()` |
| `foreman/runtime/task_manager.py` | 230 | `'timestamp': datetime.utcnow().isoformat()` |
| `foreman/runtime/task_manager.py` | 271 | `'timestamp': datetime.utcnow().isoformat()` |

---

## Warning Locations: runtime/ (26 locations)

**Owner**: API Builder  
**Reason**: API Builder owns runtime subsystem per Wave 1.0.3 scope

| File | Line | Context |
|------|------|---------|
| `runtime/cascading_failure_handler.py` | 45 | (timestamp usage) |
| `runtime/cascading_failure_handler.py` | 83 | (timestamp usage) |
| `runtime/cascading_failure_handler.py` | 124 | (timestamp usage) |
| `runtime/cascading_failure_handler.py` | 131 | (timestamp usage) |
| `runtime/cascading_failure_handler.py` | 181 | (timestamp usage) |
| `runtime/cascading_failure_handler.py` | 200 | (timestamp usage) |
| `runtime/data_consistency_manager.py` | 70 | (timestamp usage) |
| `runtime/data_consistency_manager.py` | 150 | (timestamp usage) |
| `runtime/data_consistency_manager.py` | 190 | (timestamp usage) |
| `runtime/data_consistency_manager.py` | 196 | (timestamp usage) |
| `runtime/deadlock_detector.py` | 57 | (timestamp usage) |
| `runtime/deadlock_detector.py` | 67 | (timestamp usage) |
| `runtime/deadlock_detector.py` | 98 | (timestamp usage) |
| `runtime/deadlock_detector.py` | 110 | (timestamp usage) |
| `runtime/deadlock_detector.py` | 165 | (timestamp usage) |
| `runtime/deadlock_detector.py` | 272 | (timestamp usage) |
| `runtime/deadlock_detector.py` | 275 | (timestamp usage) |
| `runtime/race_condition_handler.py` | 150 | (timestamp usage) |
| `runtime/race_condition_handler.py` | 156 | (timestamp usage) |
| `runtime/race_condition_handler.py` | 214 | (timestamp usage) |
| `runtime/system_failure_handler.py` | 42 | (timestamp usage) |
| `runtime/system_failure_handler.py` | 99 | (timestamp usage) |
| `runtime/system_failure_handler.py` | 202 | (timestamp usage) |
| `runtime/system_failure_handler.py` | 206 | (timestamp usage) |
| `runtime/system_failure_handler.py` | 250 | (timestamp usage) |
| `runtime/system_failure_handler.py` | 257 | (timestamp usage) |

---

## Warning Locations: fm/ (4 locations)

**Owner**: API Builder  
**Reason**: API Builder owns fm/orchestration subsystem

| File | Line | Context |
|------|------|---------|
| `fm/orchestration/build_authorization_gate.py` | 145 | `timestamp=datetime.utcnow().isoformat() + 'Z'` |
| `fm/runtime/watchdog/alert_reader.py` | 206 | `'generated_at': datetime.utcnow().isoformat()` |
| `fm/runtime/watchdog/escalation_reporter.py` | 106 | `'generated_at': datetime.utcnow().isoformat()` |
| `fm/runtime/watchdog/escalation_reporter.py` | 215 | `'generated_at': datetime.utcnow().isoformat()` |

---

## Warning Locations: python_agent/ (1 location)

**Owner**: API Builder  
**Reason**: API Builder owns python_agent subsystem

| File | Line | Context |
|------|------|---------|
| `python_agent/memory_proposal_client.py` | 107 | `timestamp = datetime.utcnow().isoformat() + 'Z'` |

---

## Warning Locations: tests/ (26 locations)

**Owner**: QA Builder  
**Reason**: QA Builder owns test files

| File | Line | Context |
|------|------|---------|
| `tests/test_build_authorization_gate.py` | 164 | `(evidence_dir / "freeze-timestamp.txt").write_text(datetime.utcnow().isoformat())` |
| `tests/test_build_authorization_gate.py` | 232 | `(evidence_dir / "freeze-timestamp.txt").write_text(datetime.utcnow().isoformat())` |
| `tests/wave1_0_qa_infrastructure/analytics/test_cost_tracker.py` | 44 | `data_source.add_metric("builds_completed", 10, timestamp=datetime.utcnow())` |
| `tests/wave1_0_qa_infrastructure/analytics/test_cost_tracker.py` | 45 | `data_source.add_metric("builds_failed", 2, timestamp=datetime.utcnow())` |
| `tests/wave1_0_qa_infrastructure/analytics/test_cost_tracker.py` | 46 | `data_source.add_metric("qa_components_passed", 500, timestamp=datetime.utcnow())` |
| `tests/wave1_0_qa_infrastructure/analytics/test_cost_tracker.py` | 71 | `start_time = datetime.utcnow()` |
| `tests/wave1_0_qa_infrastructure/analytics/test_cost_tracker.py` | 73 | `first_call_duration = (datetime.utcnow() - start_time).total_seconds()` |
| `tests/wave1_0_qa_infrastructure/analytics/test_cost_tracker.py` | 76 | `start_time = datetime.utcnow()` |
| `tests/wave1_0_qa_infrastructure/analytics/test_cost_tracker.py` | 78 | `second_call_duration = (datetime.utcnow() - start_time).total_seconds()` |
| `tests/wave1_0_qa_infrastructure/analytics/test_cost_tracker.py` | 114 | `base_time = datetime.utcnow()` |
| `tests/wave1_0_qa_infrastructure/analytics/test_cost_tracker.py` | 138 | `start_time = datetime.utcnow()` |
| `tests/wave1_0_qa_infrastructure/analytics/test_cost_tracker.py` | 140 | `retrieval_duration = (datetime.utcnow() - start_time).total_seconds()` |
| `tests/wave1_0_qa_infrastructure/analytics/test_cost_tracker.py` | 619 | `base_time = datetime.utcnow()` |
| `tests/wave1_0_qa_infrastructure/cross_cutting/test_other_components.py` | 223 | (timestamp usage) |
| `tests/wave2_0_qa_infrastructure/conftest.py` | 88 | (timestamp usage) |
| `tests/wave2_0_qa_infrastructure/test_governance_advanced_integration.py` | 87 | (timestamp usage) |
| `tests/wave2_0_qa_infrastructure/test_governance_advanced_integration.py` | 89 | (timestamp usage) |
| `tests/wave2_0_qa_infrastructure/test_governance_advanced_integration.py` | 136 | (timestamp usage) |
| `tests/wave2_0_qa_infrastructure/test_governance_advanced_integration.py` | 179 | (timestamp usage) |
| `tests/wave2_0_qa_infrastructure/test_governance_advanced_integration.py` | 224 | (timestamp usage) |
| `tests/wave2_0_qa_infrastructure/test_governance_advanced_integration.py` | 273 | (timestamp usage) |
| `tests/wave2_0_qa_infrastructure/test_governance_advanced_security.py` | 70 | (timestamp usage) |
| `tests/wave2_0_qa_infrastructure/test_governance_advanced_security.py` | 116 | (timestamp usage) |
| `tests/wave2_0_qa_infrastructure/test_governance_advanced_security.py` | 173 | (timestamp usage) |
| `tests/wave2_0_qa_infrastructure/test_governance_advanced_security.py` | 215 | (timestamp usage) |
| `tests/wave2_0_qa_infrastructure/test_governance_advanced_security.py` | 259 | (timestamp usage) |

---

## Warning Locations: ui/ (4 locations)

**Owner**: UI Builder  
**Reason**: UI Builder owns ui/ subsystem per Wave 1.0 scope

| File | Line | Context |
|------|------|---------|
| `ui/dashboard/enhanced_dashboard.py` | 132 | (timestamp usage) |
| `ui/dashboard/enhanced_drilldown.py` | 247 | (timestamp usage) |
| `ui/dashboard/enhanced_notifications.py` | 77 | (timestamp usage) |
| `ui/dashboard/enhanced_realtime.py` | 135 | (timestamp usage) |

---

## Warning Type 2: PytestReturnNotNoneWarning (7 occurrences, 1 file)

### Description
Pytest requires test functions to return `None`. Seven test functions in `tests/test_agent_boundary_validation.py` incorrectly return `bool` values.

### Message
```
Test functions should return None, but tests/test_agent_boundary_validation.py::<function_name> returned <class 'bool'>.
```

### Fix Pattern
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

### Locations

**File**: `tests/test_agent_boundary_validation.py`  
**Owner**: QA Builder  
**Lines**: Multiple (7 test functions)

| Test Function | Current Behavior | Required Fix |
|---------------|------------------|--------------|
| `test_valid_builder_qa` | `return <bool>` | `assert <bool>` |
| `test_valid_fm_qa` | `return <bool>` | `assert <bool>` |
| `test_valid_governance_qa` | `return <bool>` | `assert <bool>` |
| `test_cross_agent_violation_builder_to_governance` | `return <bool>` | `assert <bool>` |
| `test_cross_agent_violation_fm_to_builder` | `return <bool>` | `assert <bool>` |
| `test_missing_metadata` | `return <bool>` | `assert <bool>` |
| `test_no_reports` | `return <bool>` | `assert <bool>` |

---

## Builder Ownership Summary

| Builder | Warning Count | Files | Effort Estimate |
|---------|---------------|-------|-----------------|
| **API Builder** | ~345 occurrences | 85 files (foreman/, runtime/, fm/, python_agent/) | **1 day** |
| **QA Builder** | ~125 occurrences + 7 return warnings | 26 files + 1 file | **0.5 day** |
| **UI Builder** | ~16 occurrences | 4 files (ui/) | **0.25 day** |
| **TOTAL** | **477 warnings** | **116 files** | **1.75 days** |

### Ownership Rationale

**API Builder** owns majority (72%) because:
- Owns `foreman/` subsystem (runtime orchestration)
- Owns `runtime/` subsystem (failure handlers)
- Owns `fm/orchestration` and `fm/runtime`
- Owns `python_agent/` integration
- Wave 1.0.3 scope included API routes and runtime

**QA Builder** owns test warnings (26%) because:
- Owns all test files
- Responsible for test code quality
- Wave 1.0.4 scope included QA infrastructure

**UI Builder** owns UI warnings (2%) because:
- Owns `ui/` subsystem
- Wave 1.0 scope included dashboard components

---

## Effort Estimates

### API Builder (1 day)
- **Task**: Replace 85 instances of `datetime.utcnow()` with `datetime.now(UTC)`
- **Files**: 85 files across foreman/, runtime/, fm/, python_agent/
- **Pattern**: Search-and-replace with import updates
- **Verification**: Run tests for each file after change
- **Risk**: LOW (mechanical transformation)
- **Timeline**: 6-8 hours

### QA Builder (0.5 day)
- **Task 1**: Replace 26 instances of `datetime.utcnow()` in test files
  - Effort: 2 hours
- **Task 2**: Fix 7 test functions returning bool in `test_agent_boundary_validation.py`
  - Effort: 1 hour (change `return` to `assert`)
- **Verification**: Run full test suite
- **Risk**: LOW (mechanical transformation)
- **Timeline**: 3-4 hours

### UI Builder (0.25 day)
- **Task**: Replace 4 instances of `datetime.utcnow()` in ui/ files
- **Files**: 4 files in ui/dashboard/
- **Pattern**: Search-and-replace with import updates
- **Verification**: Run UI tests
- **Risk**: LOW (mechanical transformation)
- **Timeline**: 2 hours

---

## Priority Classification

### High Priority (API Builder warnings)
- **Reason**: Core runtime and orchestration code
- **Impact**: Affects all subsystems
- **Count**: 345 occurrences (72%)
- **Must complete first**: Yes

### Medium Priority (QA Builder warnings)
- **Reason**: Test code quality
- **Impact**: Warning visibility but not functionality
- **Count**: 125 + 7 occurrences (28%)
- **Can parallelize**: After API Builder 50% complete

### Low Priority (UI Builder warnings)
- **Reason**: UI dashboard components only
- **Impact**: Minimal (4 files)
- **Count**: 16 occurrences (3%)
- **Can parallelize**: After API Builder 50% complete

---

## Verification Methodology

### Per-File Verification (During Implementation)
```bash
# After fixing file X:
pytest tests/ -k "test_*X*" --tb=short -W all
# Expected: 0 warnings related to file X
```

### Full Suite Verification (After Wave 1.0.5 Complete)
```bash
# Run full suite:
pytest tests/ -v --tb=short

# Expected output:
# ====== X passed in Y seconds ======
# (NO "warnings summary" section)

# Or with strict warnings:
pytest tests/ --strict-warnings
# Expected: All tests pass, no warnings
```

### Evidence Requirements
Each builder must provide:
1. **Before Count**: `pytest tests/ --tb=no 2>&1 | grep -c "DeprecationWarning"` (before changes)
2. **After Count**: Same command (after changes) - must show 0
3. **File Diffs**: Git diff showing all `datetime.utcnow()` → `datetime.now(UTC)` changes
4. **Test Pass Proof**: Full test suite output showing 628 passed, 0 warnings

---

## Wave 1.0.5 Scope Assignment

Based on this inventory, Wave 1.0.5 cleanup is assigned to:

**Primary**: API Builder (345 warnings, 1 day)
**Secondary**: QA Builder (132 warnings, 0.5 day)
**Tertiary**: UI Builder (16 warnings, 0.25 day)

**Execution Strategy**:
- **Day 1**: API Builder completes foreman/, runtime/, fm/, python_agent/ cleanup
- **Day 1 (parallel after 4 hours)**: QA Builder starts test file cleanup
- **Day 1 (parallel after 6 hours)**: UI Builder starts ui/ cleanup
- **Day 2 (morning)**: All builders verify, provide evidence, FM confirms 0 warnings

**Total Timeline**: 1.5 days (with parallelization)

---

**Document**: Complete Warning Inventory  
**Status**: COMPLETE  
**Date**: 2026-01-08  
**Author**: Foreman (FM)  
**Authority**: CS2 (Johan Ras)
