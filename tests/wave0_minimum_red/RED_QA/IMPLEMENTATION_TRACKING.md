# RED QA Implementation Tracking

## Overview

This document tracks the implementation status of RED QA tests that were properly classified during governance incident INCIDENT-20251222-TEST-DEBT.

**Total RED QA Tests**: 65  
**Test Files**: 5  
**Status**: Awaiting Implementation  
**Priority**: TBD per roadmap

---

## Tracking Issues

### Issue 1: Implement Decision Determinism System
**File**: `tests/wave0_minimum_red/RED_QA/test_decision_determinism.py`  
**Tests**: 8  
**Priority**: High  
**Estimated Effort**: Medium  

**Scope**:
- Complete decision data structures (add `can_complete`, `name` keys)
- Implement `DecisionTraceRecorder.get_traces()` method
- Implement `GovernanceMemoryLogger.query()` method
- Add immutability enforcement to decision traces
- Add reasoning step capture

**Files to Modify**:
- `foreman/governance/decision_determinism.py`
- `foreman/governance/memory_logger.py`

**Acceptance Criteria**:
- All 8 tests pass
- Decision traces are deterministic (same input → same output)
- Decision traces are replayable
- Decision traces are stored immutably

---

### Issue 2: Implement Evidence Integrity System
**File**: `tests/wave0_minimum_red/RED_QA/test_evidence_integrity.py`  
**Tests**: 20  
**Priority**: High  
**Estimated Effort**: High  

**Scope**:
- Update `BuildStateManager.start_build()` signature (add `architecture_path` param)
- Implement `BuildStateManager.complete_build()` method
- Implement `BuildExecutor.execute_iteration()` method
- Implement `BuildExecutor.execute_build()` method
- Implement `EvidenceGenerator.generate_build_initiation()` method
- Implement `EvidenceGenerator.generate_iteration()` method
- Implement `EvidenceSchemaValidator.get_available_schemas()` method
- Complete schema validation implementation

**Files to Modify**:
- `foreman/build/state_manager.py`
- `foreman/build/executor.py`
- `foreman/governance/evidence_integrity.py`

**Acceptance Criteria**:
- All 20 tests pass
- Evidence automatically generated for all build phases
- Evidence conforms to schemas
- Evidence includes full traceability chain

---

### Issue 3: Implement Governance Supremacy Enforcement
**File**: `tests/wave0_minimum_red/RED_QA/test_governance_supremacy.py`  
**Tests**: 16  
**Priority**: Critical  
**Estimated Effort**: High  

**Scope**:
- Implement `ArchitectureFreezeManager` class
- Implement `QAEnforcementManager` class
- Implement `TaskCompletionValidator.validate_completion()` method
- Add architecture change blocking logic (CS2+ requires approval)
- Add QA bypass prevention logic
- Add test debt detection and blocking
- Add governance bypass logging

**Files to Create/Modify**:
- `foreman/governance/architecture_freeze.py`
- `foreman/governance/qa_enforcement.py`
- `foreman/build/task_completion.py`

**Acceptance Criteria**:
- All 16 tests pass
- Architecture freeze prevents unauthorized CS2+ changes
- 100% test pass rate enforced (99% = failure)
- QA validation cannot be skipped
- Test debt blocks task completion
- All bypass attempts logged to governance memory

**NOTE**: This issue directly relates to the current test debt governance requirement. Implementation of this subsystem will enforce the same governance rules that this incident addresses.

---

### Issue 4: Implement Liveness and Continuity Monitoring
**File**: `tests/wave0_minimum_red/RED_QA/test_liveness_continuity.py`  
**Tests**: 9  
**Priority**: Medium  
**Estimated Effort**: Medium  

**Scope**:
- Update `HeartbeatMonitor.__init__()` to accept parameters
- Implement heartbeat generation logic
- Implement stall detection logic
- Implement `RecoveryManager.select_strategy()` method
- Add recovery strategy selection logic
- Add recovery execution tracking

**Files to Modify**:
- `foreman/monitoring/heartbeat.py`
- `foreman/monitoring/recovery.py`

**Acceptance Criteria**:
- All 9 tests pass
- Heartbeat continuously generated during builds
- Stall detection triggers on missing heartbeats
- Recovery strategies automatically selected
- Recovery execution is tracked

---

### Issue 5: Implement Evidence Schema Validation
**File**: `tests/wave0_minimum_red/RED_QA/test_evidence_schema_validation.py`  
**Tests**: 12  
**Priority**: High  
**Estimated Effort**: Medium  

**Scope**:
- Fix JSON schema internal references (`definitions/task_id`)
- Complete schema validation data structures (add `valid` key)
- Implement `AuditReplayEngine.replay_build()` method
- Add immutability enforcement in schemas
- Add traceability verification logic
- Enable governance gate to use schema validation

**Files to Modify**:
- `foreman/governance/evidence_schema_validator.py`
- `foreman/governance/audit_replay.py`
- Evidence schema JSON files in `governance/schemas/`

**Acceptance Criteria**:
- All 12 tests pass
- Evidence schemas validate correctly with proper internal references
- Malformed evidence is rejected
- Valid evidence is accepted
- Immutability flags are enforced
- Traceability chains are verified
- Build replay from evidence is possible

---

## Implementation Priority Order

Based on criticality and dependencies:

1. **Issue 3: Governance Supremacy** (Critical) - Enforces the governance rules
2. **Issue 2: Evidence Integrity** (High) - Foundational for audit trails
3. **Issue 5: Evidence Schema Validation** (High) - Validates evidence quality
4. **Issue 1: Decision Determinism** (High) - Ensures reproducible decisions
5. **Issue 4: Liveness and Continuity** (Medium) - Operational monitoring

---

## Dependencies

- **Issue 5** depends on **Issue 2** (schemas validate evidence from evidence integrity)
- **Issue 1** may benefit from **Issue 2** (decision traces are evidence)
- **Issue 3** can proceed independently (governance enforcement)
- **Issue 4** can proceed independently (operational monitoring)

---

## Success Criteria

Implementation is complete when:
- All 65 RED QA tests pass
- All test files moved back to `tests/wave0_minimum_red/`
- RED_QA directory is empty or removed
- pytest.ini no longer needs to exclude RED_QA
- 100% pass rate maintained (now 98/98 instead of 33/33)

---

## Current Status

**Date**: 2025-12-22  
**Status**: Awaiting Roadmap Prioritization  
**Issues Created**: 0/5  
**Tests Implemented**: 0/65  
**Progress**: 0%

---

## Notes

These tests represent **intentional technical debt** that is:
- Explicitly documented
- Properly classified
- Tracked for implementation
- Excluded from CI until implemented
- Not blocking current work

This is governance-compliant technical debt management.
