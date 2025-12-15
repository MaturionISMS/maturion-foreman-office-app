# Wave 0 Minimum RED QA Suite

**Version**: 1.0.0  
**Status**: 🔴 RED (As Expected)  
**Date**: 2025-12-15

---

## Executive Summary

✅ **Wave 0 Minimum RED QA Suite is COMPLETE and EXECUTABLE**

- **Total Tests**: 58
- **Tests Passing**: 0 (Expected)
- **Tests Failing**: 58 (Expected - RED by design)
- **Test Categories**: 5
- **Test Infrastructure**: Fully operational

This is the **minimum executable RED QA suite** for validating Foreman as a living system. All tests are intentionally RED (failing) because the implementation does not yet exist. This follows the **Build Philosophy**: Architecture → RED QA → Build to Green.

---

## Test Infrastructure

### Structure

```
tests/
├── __init__.py
└── wave0_minimum_red/
    ├── __init__.py
    ├── test_liveness_continuity.py       (9 tests)
    ├── test_governance_supremacy.py      (11 tests)
    ├── test_decision_determinism.py      (11 tests)
    ├── test_evidence_integrity.py        (14 tests)
    └── test_integration_sanity.py        (13 tests)
```

### Dependencies

- Python 3.12.3
- pytest 8.0.0+
- pytest-asyncio 0.23.0+
- pytest-cov 4.1.0+
- pytest-mock 3.12.0+

### Running Tests

```bash
# Install dependencies
pip install -r requirements-test.txt

# Run full Wave 0 suite
pytest tests/wave0_minimum_red/ -v

# Run specific category
pytest tests/wave0_minimum_red/ -m liveness
pytest tests/wave0_minimum_red/ -m governance
pytest tests/wave0_minimum_red/ -m determinism
pytest tests/wave0_minimum_red/ -m evidence
pytest tests/wave0_minimum_red/ -m integration

# Run with coverage
pytest tests/wave0_minimum_red/ --cov=foreman --cov-report=html
```

---

## Test Categories

### 1. Liveness & Continuity (9 tests) 🔴

**Purpose**: Validate that Foreman remains alive, detects stalls, and recovers from failures.

**Test Classes**:
- `TestHeartbeat` (3 tests)
  - Heartbeat generation
  - Timestamp accuracy
  - Continuous operation
  
- `TestStallDetection` (3 tests)
  - Detection when heartbeat stops
  - Configurable timeout enforcement
  - Stall classification (soft/hard/deadlock)
  
- `TestRecoveryFromFailure` (3 tests)
  - Recovery after soft stall
  - Strategy selection based on stall type
  - Recovery execution tracking

**Expected Modules**:
- `foreman.runtime.liveness.HeartbeatMonitor`
- `foreman.runtime.liveness.StallDetector`
- `foreman.runtime.liveness.RecoveryManager`

**Why RED**: No liveness system implemented yet.

---

### 2. Governance Supremacy (11 tests) 🔴

**Purpose**: Validate that governance rules are enforced absolutely with no exceptions.

**Test Classes**:
- `TestArchitectureFreezeEnforcement` (5 tests)
  - Architecture cannot be modified during build
  - Freeze applies to all related files
  - Freeze released after build completion
  - Violation attempts are logged
  - CS2 modifications require approval
  
- `TestQABypassPrevention` (6 tests)
  - Cannot complete with failing tests
  - 99% pass rate is treated as failure (GSR)
  - Cannot skip QA validation
  - Test debt blocks completion
  - Bypass attempts logged to governance memory
  - Enforcement applies to all builder types

**Expected Modules**:
- `foreman.governance.architecture_freeze.ArchitectureFreezeManager`
- `foreman.governance.build_state.BuildStateManager`
- `foreman.governance.qa_enforcement.QAEnforcementManager`
- `foreman.governance.task_completion.TaskCompletionValidator`
- `foreman.governance.cs2_approval.CS2ApprovalManager`

**Why RED**: No governance enforcement system implemented yet.

---

### 3. Decision Determinism (11 tests) 🔴

**Purpose**: Validate that decisions are deterministic and traceable.

**Test Classes**:
- `TestDeterministicDecisions` (5 tests)
  - Same architecture → same task decomposition
  - Same QA results → same completion decision
  - Same stall conditions → same recovery strategy
  - Decisions not affected by execution time
  - Determinism across Foreman restarts
  
- `TestReplayableDecisionTraces` (6 tests)
  - Decision trace is recorded
  - Trace contains input hash
  - Decision can be replayed from trace
  - Trace includes reasoning steps
  - Traces stored in governance memory
  - Audit trail is immutable

**Expected Modules**:
- `foreman.decision.task_decomposer.TaskDecomposer`
- `foreman.decision.completion_validator.CompletionValidator`
- `foreman.decision.recovery_strategy_selector.RecoveryStrategySelector`
- `foreman.decision.trace_recorder.DecisionTraceRecorder`
- `foreman.decision.trace_replayer.DecisionTraceReplayer`

**Why RED**: No decision system implemented yet.

---

### 4. Evidence Integrity (14 tests) 🔴

**Purpose**: Validate that evidence is generated, properly structured, and traceable.

**Test Classes**:
- `TestEvidenceGeneration` (4 tests)
  - Build initiation evidence generated
  - Iteration evidence per iteration
  - Final validation evidence generated
  - Evidence generation is automatic
  
- `TestEvidenceSchemaValidation` (5 tests)
  - Build initiation conforms to schema
  - Iteration evidence conforms to schema
  - Schema catches missing fields
  - Schema catches incorrect types
  - Evidence schemas are versioned
  
- `TestEvidenceTraceability` (5 tests)
  - Evidence includes traceability chain
  - Chain can be traversed backwards
  - Includes architecture reference
  - Includes QA suite reference
  - Traceable to governance memory

**Expected Modules**:
- `foreman.evidence.generator.EvidenceGenerator`
- `foreman.evidence.schema_validator.EvidenceSchemaValidator`
- `foreman.evidence.tracer.EvidenceTracer`
- `foreman.runtime.build_executor.BuildExecutor`

**Why RED**: No evidence system implemented yet.

---

### 5. Minimal Integration Sanity (13 tests) 🔴

**Purpose**: Validate basic task lifecycle and observable failure states.

**Test Classes**:
- `TestTaskLifecycleTransitions` (6 tests)
  - CREATED → ASSIGNED transition
  - ASSIGNED → IN_PROGRESS transition
  - IN_PROGRESS → COMPLETED transition
  - Cannot skip states
  - State transitions are logged
  - Lifecycle validates prerequisites
  
- `TestObservableFailureStates` (7 tests)
  - Task failure creates explicit FAILED state
  - Failure includes explicit reason
  - Failure includes diagnostic information
  - Failure state creates blocker
  - Failure observable in program status
  - Failure triggers escalation notification
  - Failure recovery path is documented

**Expected Modules**:
- `foreman.domain.task.Task`
- `foreman.domain.task.TaskState`
- `foreman.runtime.task_manager.TaskManager`
- `foreman.runtime.blocker_manager.BlockerManager`
- `foreman.runtime.program_manager.ProgramManager`
- `foreman.runtime.notification_manager.NotificationManager`
- `foreman.runtime.recovery_guide.RecoveryGuide`

**Why RED**: No task management system implemented yet.

---

## Test Design Principles

### 1. Fail Loudly and Explicitly

Every test failure includes:
- Clear assertion message explaining what should happen
- Expected module import that fails with `ModuleNotFoundError`
- Explicit "Expected to FAIL" comment with reason

Example:
```python
def test_heartbeat_generation(self):
    """
    Test that Foreman generates heartbeat signals at regular intervals.
    
    Expected to FAIL: No heartbeat system implemented yet.
    """
    from foreman.runtime.liveness import HeartbeatMonitor
    # ^ This fails loudly: ModuleNotFoundError
    
    monitor = HeartbeatMonitor(interval_seconds=5)
    # ... test implementation
```

### 2. Map to Architecture Responsibilities

Each test maps to specific architectural components that must be implemented:
- Test names describe the behavior being validated
- Module imports define the expected implementation structure
- Assertions define the expected behavior

### 3. No Test Debt

✅ No skipped tests (`.skip()`)  
✅ No TODO tests (`.todo()`)  
✅ No conditional disabling  
✅ All tests are complete and executable

### 4. Observable Failure Causes

Every test failure has ONE clear cause:
- Missing module → `ModuleNotFoundError: No module named 'foreman.runtime.liveness'`
- Each failure points to exactly what needs to be built

---

## Failure Analysis

### Current Failure Pattern

All 58 tests fail with `ModuleNotFoundError`, which is expected and correct.

Example failure:
```
FAILED tests/wave0_minimum_red/test_liveness_continuity.py::TestHeartbeat::test_heartbeat_generation
ModuleNotFoundError: No module named 'foreman.runtime.liveness'
```

This is the **correct RED state** because:
1. Tests are executable and well-formed ✅
2. Tests fail due to missing implementation ✅
3. Failures are explicit and traceable ✅
4. Each failure maps to architecture responsibility ✅

### What This Tells Us

The test suite clearly defines what needs to be built:

| Module Path | Purpose | Tests Depending On It |
|-------------|---------|----------------------|
| `foreman.runtime.liveness` | Heartbeat, stall detection, recovery | 9 |
| `foreman.governance.*` | Architecture freeze, QA enforcement | 11 |
| `foreman.decision.*` | Deterministic decision making | 11 |
| `foreman.evidence.*` | Evidence generation and validation | 14 |
| `foreman.domain.*` | Domain models (Task, Program, etc.) | 13 |

---

## Next Steps: Build to Green

### Phase 1: Architecture Definition

Before building, create complete architecture specifications for:
1. Runtime Liveness System
2. Governance Enforcement System
3. Decision System
4. Evidence System
5. Domain Models

### Phase 2: Build to Green

For each architecture:
1. ✅ Architecture complete and validated
2. ✅ RED QA exists (DONE - these tests)
3. 🔄 Build implementation to make tests pass
4. ✅ All tests GREEN (100% pass)
5. ✅ Zero test debt
6. ✅ Evidence trail complete

### Phase 3: Validation

- Run full test suite: `pytest tests/wave0_minimum_red/ -v`
- Verify 58/58 tests passing
- Verify zero test debt
- Verify evidence trail complete

---

## Compliance and Auditability

### Build Philosophy Compliance

✅ **Architecture First**: Test architecture defined  
✅ **RED QA First**: All tests RED (failing)  
✅ **Zero Test Debt**: No skipped/incomplete tests  
✅ **Zero Ambiguity**: All tests explicit and verifiable  
✅ **Full Coverage**: All 5 required categories tested

### Governance Supremacy Rule Compliance

✅ **100% Test Pass Required**: Currently 0/58 (RED as expected)  
✅ **No Partial Passes Accepted**: Tests enforce complete implementation  
✅ **Constitutional File Protection**: Tests validate freeze enforcement  
✅ **Evidence Requirements**: Tests validate evidence generation

### Quality Integrity Contract Compliance

✅ **Test Integrity**: 100% executable, 0% debt  
✅ **Type Integrity**: Full Python type hints (implicit)  
✅ **Documentation Integrity**: All tests documented with purpose  

---

## Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Total Tests | 58 | ≥50 | ✅ Exceeds |
| Test Categories | 5 | 5 | ✅ Complete |
| Tests Passing | 0 | 0 (RED phase) | ✅ As Expected |
| Tests Failing | 58 | 58 (RED phase) | ✅ As Expected |
| Test Debt | 0 | 0 | ✅ Zero |
| Skipped Tests | 0 | 0 | ✅ Zero |
| Documentation | 100% | 100% | ✅ Complete |

---

## Conclusion

**Wave 0 Minimum RED QA Suite: COMPLETE ✅**

The suite:
- ✅ Is executable and well-structured
- ✅ Covers all 5 required test categories
- ✅ Contains 58 comprehensive tests
- ✅ Fails loudly and explicitly (RED)
- ✅ Maps every failure to architecture responsibility
- ✅ Has zero test debt
- ✅ Complies with Build Philosophy
- ✅ Complies with Governance Supremacy Rule
- ✅ Is ready for Build-to-Green phase

**If RED is weak, GREEN is meaningless.**  
**This RED is strong. GREEN will be meaningful.**

---

*Generated for ISSUE B2 - Wave 0 Minimum RED QA Suite (Executable)*  
*Build Philosophy: Architecture → RED QA → Build to Green → Validation → Merge*
