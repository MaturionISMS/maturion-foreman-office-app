# RED QA Tests Directory

## Purpose

This directory contains **intentional TDD RED tests** that were written before their corresponding implementations exist.

## Governance Classification

**Status**: RED QA (Test-Driven Development)  
**Authority**: Governance Policy on Test Debt  
**Date Classified**: 2025-12-22  
**Classified By**: FM Repo Builder Agent  
**Approved By**: [Awaiting Johan Ras approval]

## Why These Tests Are Here

These tests represent **future functionality** that has been specified but not yet implemented. They are:

1. **Intentionally failing** - This is expected TDD behavior
2. **Not technical debt** - They are properly classified and tracked
3. **Not run in CI** - Excluded from standard test runs
4. **Tracked for implementation** - Each has a corresponding tracking issue

## Test Categories

### 1. Decision Determinism (8 tests)
**File**: `test_decision_determinism.py`  
**Tests**: 8 failing  
**Subsystem**: Decision recording and replay  
**Tracking**: [Issue TBD]

**What's Missing**:
- Complete decision data structures (missing keys like `can_complete`, `name`)
- `get_traces()` method (only `get_trace()` exists)
- `GovernanceMemoryLogger.query()` method
- Immutability enforcement

**Implementation Needed In**:
- `foreman/governance/decision_determinism.py`

---

### 2. Evidence Integrity (20 tests)
**File**: `test_evidence_integrity.py`  
**Tests**: 20 failing  
**Subsystem**: Build evidence generation and validation  
**Tracking**: [Issue TBD]

**What's Missing**:
- `BuildStateManager.start_build()` signature (`architecture_path` param)
- `BuildStateManager.complete_build()` method
- `BuildExecutor.execute_iteration()` method
- `BuildExecutor.execute_build()` method
- `EvidenceGenerator.generate_build_initiation()` method
- `EvidenceGenerator.generate_iteration()` method
- `EvidenceSchemaValidator.get_available_schemas()` method
- Schema validation implementation

**Implementation Needed In**:
- `foreman/build/state_manager.py`
- `foreman/build/executor.py`
- `foreman/governance/evidence_integrity.py`

---

### 3. Governance Supremacy (16 tests)
**File**: `test_governance_supremacy.py`  
**Tests**: 16 failing  
**Subsystem**: Governance enforcement and QA gating  
**Tracking**: [Issue TBD]

**What's Missing**:
- `ArchitectureFreezeManager` class
- `QAEnforcementManager` class
- `TaskCompletionValidator.validate_completion()` method
- Architecture change blocking logic
- QA bypass prevention logic
- Test debt detection and blocking

**Implementation Needed In**:
- `foreman/governance/architecture_freeze.py`
- `foreman/governance/qa_enforcement.py`
- `foreman/build/task_completion.py`

---

### 4. Liveness Continuity (9 tests)
**File**: `test_liveness_continuity.py`  
**Tests**: 9 failing  
**Subsystem**: Heartbeat monitoring and stall recovery  
**Tracking**: [Issue TBD]

**What's Missing**:
- `HeartbeatMonitor.__init__()` signature (expects parameters)
- `RecoveryManager.select_strategy()` method
- Stall detection logic
- Recovery strategy selection
- Recovery execution tracking

**Implementation Needed In**:
- `foreman/monitoring/heartbeat.py`
- `foreman/monitoring/recovery.py`

---

### 5. Evidence Schema Validation (12 tests)
**File**: `test_evidence_schema_validation.py`  
**Tests**: 12 failing  
**Subsystem**: Evidence schema validation and audit replay  
**Tracking**: [Issue TBD]

**What's Missing**:
- JSON schema internal references (`definitions/task_id`)
- Schema validation returns incomplete data (missing `valid` key)
- `AuditReplayEngine.replay_build()` method
- Immutability enforcement in schemas
- Traceability verification logic

**Implementation Needed In**:
- `foreman/governance/evidence_schema_validator.py`
- `foreman/governance/audit_replay.py`
- Evidence schema JSON files

---

## How to Use These Tests

### During Development
1. Choose a subsystem to implement (e.g., Decision Determinism)
2. Review the RED QA tests for that subsystem
3. Implement the missing functionality
4. Run the specific test file to verify
5. Once ALL tests in a file pass, move it back to `tests/wave0_minimum_red/`

### For CI/CD
These tests are **excluded** from CI runs via pytest configuration.

### For Tracking
Each category has a tracking issue that links to:
- The RED QA test file
- The implementation files needed
- Acceptance criteria
- Priority

---

## Governance Compliance

This classification maintains governance compliance by:

1. **Making technical debt explicit** - Not hidden, clearly documented
2. **Preventing false positives** - Tests won't fail CI unexpectedly
3. **Maintaining 100% pass rate** - Only implemented tests run in CI
4. **Enabling TDD workflow** - Tests written before implementation
5. **Ensuring traceability** - Each test linked to tracking issue

---

## Moving Tests Out of RED QA

**Criteria for Moving a Test File**:
1. ALL tests in the file must pass
2. Implementation must be complete and reviewed
3. Tests must be integrated into CI
4. Evidence of pass must be documented

**Process**:
1. Implement the missing functionality
2. Run: `python -m pytest tests/wave0_minimum_red/RED_QA/test_<name>.py -v`
3. Verify 100% pass rate for that file
4. Move file back: `mv tests/wave0_minimum_red/RED_QA/test_<name>.py tests/wave0_minimum_red/`
5. Run full test suite to ensure no regressions
6. Update this README to remove the category
7. Close the tracking issue

---

## Current Status

**Total RED QA Tests**: 65 (53 + 12)  
**RED QA Test Files**: 5  
**Pass Rate**: 0% (expected - these are RED tests)  
**Active Test Suite**: 33 tests (100% passing)  
**Target Date**: TBD per implementation roadmap  
**Blocker**: None - properly classified

---

## Approval Chain

**Classified By**: FM Repo Builder Agent  
**Date**: 2025-12-22T17:00:00Z  
**Governance Incident**: INCIDENT-20251222-TEST-DEBT  
**Approved By**: [Awaiting Johan Ras]  
**Approval Date**: [Pending]

---

## References

- Governance Incident: `governance/incidents/INCIDENT-20251222-TEST-DEBT.md`
- Test Debt Policy: [Link to governance policy]
- TDD Workflow: [Link to development workflow]
