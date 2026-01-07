# Future Functionality Roadmap

**Purpose**: Document functionality deferred to future waves  
**Authority**: FM Agent Contract v3.4.0, DEBT-002 Resolution  
**Status**: Active  
**Last Updated**: 2026-01-07

---

## Overview

This document tracks functionality that has been planned, documented, and test-specified but deferred to future implementation waves. All items listed here have:

- ✅ Complete test specifications
- ✅ Documented requirements
- ✅ Wave assignments
- ✅ Priority classifications
- ✅ Governance approval

---

## Wave 3.0: Evidence & Governance Systems

### Wave 3.1: Evidence System Implementation

**Scope**: Comprehensive evidence generation and validation infrastructure

**Components**:
1. **Evidence Integrity System** (14 tests)
   - Automatic evidence generation for all build phases
   - Evidence schema conformance
   - Full traceability chains
   - Architecture reference linking
   - QA suite reference linking

2. **Evidence Schema Validation** (15 tests)
   - JSON schema validation framework
   - Evidence malformation detection
   - Immutability enforcement
   - Traceability verification
   - Audit replay capability

**Priority**: HIGH  
**Estimated Effort**: 4-6 weeks  
**Dependencies**: None  
**Test Count**: 29 tests  
**Test Location**: `tests/future/wave3/test_evidence_integrity.py`, `test_evidence_schema_validation.py`

**Implementation Files Required**:
- `foreman/evidence/generator.py` (complete implementation)
- `foreman/evidence/schema_validator.py` (complete implementation)
- `foreman/governance/audit_replay.py` (new)
- `foreman/governance/build_state.py` (extend)
- `foreman/build/executor.py` (extend)
- Evidence schema JSON files (define)

**Success Criteria**:
- All 29 tests pass (100% GREEN)
- Evidence automatically generated for all builds
- Evidence can be validated and replayed
- Integration with existing governance system

---

### Wave 3.2: Decision Determinism System

**Scope**: Deterministic decision making and replay capability

**Components**:
1. **Decision Determinism** (11 tests)
   - Deterministic task decomposition
   - Deterministic completion decisions
   - Deterministic recovery strategies
   - Decision trace recording
   - Decision replay from traces
   - Decision audit trail

**Priority**: HIGH  
**Estimated Effort**: 2-3 weeks  
**Dependencies**: Wave 3.1 (Evidence System)  
**Test Count**: 11 tests  
**Test Location**: `tests/future/wave3/test_decision_determinism.py`

**Implementation Files Required**:
- `foreman/decision/task_decomposer.py` (extend)
- `foreman/decision/trace_recorder.py` (extend)
- `foreman/decision/trace_replayer.py` (implement)
- `foreman/governance/memory_logger.py` (extend)

**Success Criteria**:
- All 11 tests pass (100% GREEN)
- Same inputs produce same outputs
- Decisions can be replayed from traces
- Decision audit trail immutable

---

### Wave 3.3: Governance Automation

**Scope**: Automated governance enforcement mechanisms

**Components**:
1. **Governance Supremacy Enforcement** (11 tests)
   - Architecture freeze automation
   - QA enforcement automation
   - Test debt detection and blocking
   - Governance violation logging
   - CS2+ approval workflow automation

**Priority**: CRITICAL  
**Estimated Effort**: 3-4 weeks  
**Dependencies**: Wave 3.1, 3.2  
**Test Count**: 11 tests  
**Test Location**: `tests/future/wave3/test_governance_supremacy.py`

**Implementation Files Required**:
- `foreman/governance/architecture_freeze.py` (complete)
- `foreman/governance/qa_enforcement.py` (extend)
- `foreman/governance/task_completion.py` (extend)
- `foreman/governance/cs2_approval.py` (extend)

**Success Criteria**:
- All 11 tests pass (100% GREEN)
- Architecture changes blocked during builds
- QA validation cannot be bypassed
- Test debt blocks task completion
- All violations logged

---

## Wave 4.0: Operational Excellence

### Wave 4.1: Liveness & Continuity Monitoring

**Scope**: Runtime monitoring and recovery management

**Components**:
1. **Liveness Continuity System** (9 tests)
   - Heartbeat generation during builds
   - Stall detection when heartbeats stop
   - Recovery strategy selection
   - Recovery execution tracking
   - Continuous operation monitoring

**Priority**: MEDIUM  
**Estimated Effort**: 2-3 weeks  
**Dependencies**: Wave 3.3 (stable governance system)  
**Test Count**: 9 tests  
**Test Location**: `tests/future/wave4/test_liveness_continuity.py`

**Implementation Files Required**:
- `foreman/monitoring/heartbeat.py` (implement)
- `foreman/monitoring/recovery.py` (implement)
- `foreman/monitoring/stall_detector.py` (new)

**Success Criteria**:
- All 9 tests pass (100% GREEN)
- Heartbeats continuously generated
- Stalls detected accurately
- Recovery strategies automatically selected
- Recovery execution tracked

**Rationale for Wave 4.0+**:
- Operational concern, not core functionality
- Current system operates without monitoring
- Can be layered on stable system
- Lower priority than evidence and governance

---

## Summary Statistics

**Total Deferred Functionality**: 60 tests across 5 systems

**By Wave**:
- Wave 3.1: 29 tests (Evidence System)
- Wave 3.2: 11 tests (Decision Determinism)
- Wave 3.3: 11 tests (Governance Automation)
- Wave 4.1: 9 tests (Liveness & Continuity)

**By Priority**:
- CRITICAL: 11 tests (Governance Automation)
- HIGH: 40 tests (Evidence System + Decision Determinism)
- MEDIUM: 9 tests (Liveness & Continuity)

**Estimated Total Effort**: 11-16 weeks across 4 subwaves

---

## Implementation Sequencing

**Correct Order**:
1. Wave 3.1 first (Evidence System) - provides foundation
2. Wave 3.2 second (Decision Determinism) - uses evidence system
3. Wave 3.3 third (Governance Automation) - uses both evidence and decisions
4. Wave 4.1 fourth (Liveness & Continuity) - operational layer on stable system

**Rationale**:
- Evidence System is foundational for audit and compliance
- Decision Determinism depends on evidence infrastructure
- Governance Automation uses both evidence and decisions
- Liveness Monitoring is independent but lower priority

---

## Wave Planning Checklist

When planning each wave, FM must:

- [ ] Review test specifications from `tests/future/waveN/`
- [ ] Freeze architecture for the functionality
- [ ] Create QA-to-Red (tests already exist, may need updates)
- [ ] Validate test specifications still accurate
- [ ] Recruit/assign appropriate builder
- [ ] Execute Build-to-Green from frozen architecture
- [ ] Verify all tests pass (100% GREEN)
- [ ] Move tests to active suite
- [ ] Update this document to mark wave complete

---

## Governance Compliance

This roadmap complies with:

✅ **Zero Test Debt** - No tests deleted, all properly tracked  
✅ **One-Time Build Correctness** - Each wave built correctly once  
✅ **Architecture Freeze** - Architecture frozen before each wave  
✅ **QA-to-Red First** - Tests already exist (may need review/update)  
✅ **Build-to-Green** - Builders implement to make tests GREEN

---

## References

- **Resolution Decision**: `governance/decisions/DEBT_002_RESOLUTION_DECISION.md`
- **Test Directory**: `tests/future/`
- **Debt Register**: `governance/incidents/DEBT_REGISTER.md` (DEBT-002)
- **Original Tests**: Moved from `tests/wave0_minimum_red/RED_QA/`

---

## History

**2026-01-07**: Initial roadmap created
- 60 tests deferred from DEBT-002 cleanup
- Organized into Wave 3 (51 tests) and Wave 4 (9 tests)
- Priority and sequencing established

**Next Update**: When Wave 3.0 planning begins

---

**Maintained By**: FM Agent  
**Last Updated**: 2026-01-07  
**Status**: Active

---

**END OF FUTURE FUNCTIONALITY ROADMAP**
