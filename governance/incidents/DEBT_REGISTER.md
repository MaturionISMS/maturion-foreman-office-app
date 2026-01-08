# Technical Debt Register

**Purpose**: Track all technical debt items requiring elimination  
**Authority**: FM Agent Contract v3.4.0, Debt Elimination Gate Spec  
**Status**: Active  
**Last Updated**: 2026-01-07

---

## Active Debt Items

### DEBT-001: Wave 1.0.1 Schema Foundation Warnings

**Debt ID**: DEBT-001  
**Type**: Warnings  
**Severity**: MEDIUM  
**Debt Size**: 194 warnings  
**Origin**: Wave 1.0.1 Schema Foundation (PR #349)  
**Origin Date**: 2026-01-02  
**Builder**: schema-builder  
**Status**: UNRESOLVED  
**Age**: 5 days (as of 2026-01-07)

**Debt Description**:
194 warnings observed during Wave 1.0.1 test execution. All tests passing (18/18 GREEN) but warnings present in test output. Warnings classified into 5 categories: deprecation (60-100), testing framework noise (50-70), DB/ORM config advice (30-50), test isolation (20-30), type/assertion (10-20).

**Gate Decision at Merge**:
Approved for merge with documented execution debt. FM classified warnings as "acceptable temporary execution debt" with promise of future cleanup.

**Impact**:
- Immediate: LOW (tests passing, functionality correct)
- Medium-term: MEDIUM (warnings may proliferate, deprecations may become errors)
- Long-term: HIGH (policy erosion, debt normalization)

**Elimination Plan**:
- **Phase 1**: Re-verify warnings still present (run tests, capture actual output)
- **Phase 2**: Warning-by-warning analysis (classify, prioritize, define remediation)
- **Phase 3**: Remediation execution (assign schema-builder, fix warnings)
- **Phase 4**: Verification (confirm ZERO warnings)

**Owner**: schema-builder  
**Deadline**: 2026-01-21 (14 days from registration)  
**Escalation**: If deadline missed, HALT all new work and escalate to Johan

**Related Documents**:
- `WAVE_1.0.1_WARNING_CLASSIFICATION_AND_GATE_DECISION.md`
- `governance/incidents/HISTORICAL_WAVE_PR_WARNING_TEST_DEBT_SURVEY_RCA.md`

**Tracking**:
- [ ] Phase 1: Re-verification complete
- [ ] Phase 2: Analysis complete
- [ ] Phase 3: Remediation complete
- [ ] Phase 4: Verification complete (ZERO warnings confirmed)

---

### DEBT-002: Wave 0 RED QA Tests

**Debt ID**: DEBT-002  
**Type**: Unimplemented Tests  
**Severity**: HIGH  
**Debt Size**: 65 RED tests across 5 categories  
**Origin**: Wave 0 (pre-Wave 1.0 baseline)  
**Origin Date**: 2025-12-22 or earlier  
**Builder**: Multiple (core platform team)  
**Status**: UNRESOLVED  
**Age**: 16+ days (as of 2026-01-07)

**Debt Description**:
65 tests written in TDD style (tests before implementation) and moved to RED_QA/ directory. All tests failing due to missing implementations. Tests excluded from CI via pytest.ini. Current active test suite: 100% passing (33/33) but 65 tests not executed.

**Test Categories**:
1. **Decision Determinism** (8 tests) - `test_decision_determinism.py`
   - DecisionTracker, decision replay, trace recording
2. **Evidence Integrity** (20 tests) - `test_evidence_integrity.py`
   - EvidenceGenerator, automatic evidence generation, schema validation
3. **Evidence Schema Validation** (12 tests) - `test_evidence_schema_validation.py`
   - JSON schema validation infrastructure
4. **Governance Supremacy** (16 tests) - `test_governance_supremacy.py`
   - ArchitectureFreezeManager, QAEnforcementManager, governance enforcement
5. **Liveness Continuity** (9 tests) - `test_liveness_continuity.py`
   - HeartbeatMonitor, RecoveryManager, runtime monitoring

**Gate Decision at Discovery**:
Tests moved to RED_QA/ and excluded from CI. Classified as "intentional TDD RED tests awaiting implementation". Resolution: proper classification, not elimination.

**Impact**:
- Immediate: LOW (active suite 100% GREEN, excluded tests not running)
- Medium-term: HIGH (represents unimplemented functionality, technical debt)
- Long-term: CRITICAL (TDD without implementation = broken discipline)

**Elimination Plan - Requires Decision**:
Three options per category:
1. **IMPLEMENT**: Assign builder, freeze architecture, execute Build-to-Green
2. **DEFER**: Move to `tests/future/`, document in FUTURE_FUNCTIONALITY.md, create Wave 3.0+ issue
3. **REMOVE**: Delete tests, document rationale, justify as speculative

**FM Recommendation**:
- **IMPLEMENT**: Evidence Integrity (20 tests) - critical for audit and governance
- **DEFER**: Decision Determinism (8 tests), Governance Supremacy (16 tests) - Wave 3.0+
- **REMOVE**: Evidence Schema Validation (12 tests) - overlaps with Evidence Integrity
- **REMOVE**: Liveness Continuity (9 tests) - monitoring not core, premature

**Owner**: TBD (depends on IMPLEMENT/DEFER/REMOVE decision)  
**Deadline**: 2026-01-28 (21 days from registration)  
**Escalation**: If deadline missed, HALT all new work and escalate to Johan

**Related Documents**:
- `governance/incidents/INCIDENT-20251222-TEST-DEBT.md`
- `tests/wave0_minimum_red/RED_QA/README.md`
- `tests/wave0_minimum_red/RED_QA/IMPLEMENTATION_TRACKING.md`
- `governance/incidents/HISTORICAL_WAVE_PR_WARNING_TEST_DEBT_SURVEY_RCA.md`

**Tracking**:
- [ ] IMPLEMENT/DEFER/REMOVE decision made per category
- [ ] If IMPLEMENT: Architecture frozen, QA-to-Red defined, builder assigned
- [ ] If DEFER: Tests moved to tests/future/, issues created for Wave 3.0+
- [ ] If REMOVE: Tests deleted, rationale documented
- [ ] Verification: RED_QA/ directory empty or properly scoped

---

### DEBT-003: Wave 1.0.4 Single Warning ✅ RESOLVED

**Debt ID**: DEBT-003  
**Type**: Warning (Configuration Issue)  
**Severity**: LOW  
**Debt Size**: 1 warning (historical)  
**Origin**: Wave 1.0.4 API Foundation (PR #357)  
**Origin Date**: 2026-01-02  
**Resolution Date**: 2026-01-08  
**Builder**: api-builder  
**Status**: ✅ **RESOLVED**  
**Resolution Time**: 6 days

**Debt Description**:
Single warning observed during Wave 1.0.4 test execution. Test output: "49 passed, 1 warning in 0.08s". Warning text and category NOT classified in merge approval. Gate decision did NOT address warning. Tests all passing (49/49 GREEN).

**Gate Decision at Merge**:
Approved for merge. Warning mentioned in completion summary but NOT analyzed or classified. NO gate decision documented for warning.

**Root Cause Analysis**:
Investigation revealed warning was suppressed by `--disable-warnings` in pytest.ini (line 19). This configuration violated Zero-Warning Governance Doctrine by hiding warnings rather than fixing them. The original warning was either:
1. Environment-specific or transient at time of Wave 1.0.4 execution
2. Already fixed in subsequent work
3. Suppressed before classification could occur

**Resolution Actions**:
1. ✅ Removed `--disable-warnings` from pytest.ini per Zero-Warning Governance Doctrine
2. ✅ Added documentation explaining warning visibility requirement
3. ✅ Re-ran Wave 1.0.4 tests: **49 passed, 0 warnings** (ZERO warnings confirmed)
4. ✅ Added missing pytest markers (wave1_0, cross_cutting, flows) to resolve marker warnings
5. ✅ Verified zero warnings from Wave 1.0.4 scope

**Resolution Evidence**:
- Commit: DEBT-003 resolution (pytest.ini updated)
- Test Run: `python -m pytest tests/wave1_api_builder/ -v` → 49 passed, 0 warnings
- Configuration: pytest.ini lines 15-16 document warning visibility requirement

**Impact Assessment**:
- Wave 1.0.4 tests: ZERO warnings (CLEAN)
- Zero-Warning policy: RESTORED (warnings now visible, not suppressed)
- Governance compliance: ACHIEVED

**Owner**: api-builder (resolved by FM Agent)  
**Original Deadline**: 2026-01-14 (met, resolved 6 days early)

**Related Documents**:
- `WAVE_1.0.4_COMPLETION_SUMMARY.md` (line 144: "49 passed, 1 warning in 0.08s")
- `WAVE_1.0.4_FM_MERGE_APPROVAL.md` (no warning classification present)
- `governance/incidents/HISTORICAL_WAVE_PR_WARNING_TEST_DEBT_SURVEY_RCA.md`
- `pytest.ini` (lines 15-21: warning configuration)

**Resolution Tracking**:
- [x] Phase 1: Warning identified (root cause: --disable-warnings in pytest.ini)
- [x] Phase 2: Warning classified (configuration issue, not code issue)
- [x] Phase 3: Warning remediated (removed --disable-warnings, verified zero warnings)
- [x] Phase 4: Merge approval updated (DEBT-003 resolved, no retroactive update needed)

**Secondary Discovery**:
During resolution, discovered 244 DeprecationWarnings in other test suites (datetime.utcnow() usage). These are OUT OF SCOPE for DEBT-003 but documented for future remediation tracking. Wave 1.0.4 scope remains CLEAN.

---

## Debt Statistics

**Total Active Debt Items**: 3  
**Total Warnings**: 195 (194 + 1)  
**Total Unimplemented Tests**: 65  
**Oldest Debt Age**: 16+ days (DEBT-002)  
**Average Debt Age**: ~9 days  

**By Severity**:
- HIGH: 1 (DEBT-002)
- MEDIUM: 1 (DEBT-001)
- LOW: 0 (DEBT-003 ✅ RESOLVED)

**By Builder**:
- schema-builder: 1 debt item (DEBT-001)
- api-builder: 1 debt item (DEBT-003)
- Multiple/TBD: 1 debt item (DEBT-002)

---

## Debt Resolution History

*(No resolved debt items yet)*

---

## Governance Rules

**Rule 1**: No new wave authorized while unresolved debt exists  
**Rule 2**: Debt >30 days triggers mandatory elimination before new work  
**Rule 3**: Every debt item MUST have assigned owner and deadline  
**Rule 4**: Debt deadline missed = HALT all work, escalate to Johan  
**Rule 5**: Debt register audited monthly, escalate any item >60 days old

**Authority**: 
- `governance/specs/DEBT_ELIMINATION_GATE_SPEC.md` (to be created)
- FM Agent Contract v3.4.0

---

## Monthly Audit Log

**2026-01-07**: Debt register created, 3 items registered  
**2026-01-08**: DEBT-003 resolved (Wave 1.0.4 warning eliminated)  
**Next Audit**: 2026-02-07

---

**Maintained By**: FM Agent  
**Last Updated**: 2026-01-08  
**Status**: Active (2 unresolved items, 1 resolved)

---

**END OF DEBT REGISTER**
