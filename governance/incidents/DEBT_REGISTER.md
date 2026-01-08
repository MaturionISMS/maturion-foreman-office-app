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

### DEBT-002: Wave 0 RED QA Tests — RESTORED

**Debt ID**: DEBT-002  
**Type**: Unimplemented Tests  
**Severity**: HIGH  
**Debt Size**: 60 RED tests across 5 categories  
**Origin**: Wave 0 (pre-Wave 1.0 baseline)  
**Origin Date**: 2025-12-22 or earlier  
**Builder**: Multiple (core platform team)  
**Status**: IMPLEMENTATION APPROVED (CS2 Decision 2026-01-08)  
**Age**: 17+ days (as of 2026-01-08)

**Debt Description**:
60 tests written in TDD style (tests before implementation) and moved to RED_QA/ directory. All tests failing due to missing implementations. Tests excluded from CI via pytest.ini. Current active test suite: 100% passing but 60 tests not executed.

**CRITICAL UPDATE (2026-01-08)**: Tests were incorrectly removed in PR #470 as "speculative features never part of Wave 0 requirements." RCA analysis (governance/rca/RCA_WAVE_0_60_TESTS_WITHOUT_ARCHITECTURAL_REQUIREMENT.md) proved ALL 60 tests ARE architecturally grounded and validate specified requirements. Tests restored via PR #479 (revert of PR #470).

**Test Categories**:
1. **Decision Determinism** (11 tests) - `test_decision_determinism.py`
   - DecisionTracker, decision replay, trace recording
2. **Evidence Integrity** (14 tests) - `test_evidence_integrity.py`
   - EvidenceGenerator, automatic evidence generation, schema validation
3. **Evidence Schema Validation** (15 tests) - `test_evidence_schema_validation.py`
   - JSON schema validation infrastructure
4. **Governance Supremacy** (11 tests) - `test_governance_supremacy.py`
   - ArchitectureFreezeManager, QAEnforcementManager, governance enforcement
5. **Liveness Continuity** (9 tests) - `test_liveness_continuity.py`
   - HeartbeatMonitor, RecoveryManager, runtime monitoring

**Total**: 60 tests (11 + 14 + 15 + 11 + 9)

**Gate Decision at Discovery**:
Tests moved to RED_QA/ and excluded from CI. Classified as "intentional TDD RED tests awaiting implementation". 

**PR #470 Incident**: Tests incorrectly removed as "speculative" based on wrong traceability methodology (looked for class names instead of architectural requirements). RCA proved tests ARE architecturally valid.

**Restoration**: All 60 tests restored via revert of PR #470 (2026-01-08).

**Impact**:
- Immediate: LOW (active suite 100% GREEN, excluded tests not running)
- Medium-term: HIGH (represents unimplemented functionality, technical debt)
- Long-term: CRITICAL (TDD without implementation = broken discipline)

**CS2 Decision Record**:

**Date**: 2026-01-08  
**Decision Maker**: Johan Ras (CS2)  
**Decision**: IMPLEMENT ALL 60 FEATURES (100% BUILD)

**Decision Statement**:
> "Implement all 60 features. That is 100% build. Nothing else is acceptable."

**Options Considered**: 
1. Option A: Implement All → **SELECTED**
2. Option B: Re-scope Architecture → REJECTED
3. Option C: Phased Implementation → REJECTED

**Justification**:
- All 60 tests validate architecturally-specified requirements (per RCA)
- Architecture specifies these features → features must be implemented
- Zero-tolerance policy: No scope reduction, no deferral, no exceptions

**Implications**:
- 60 additional tests must turn GREEN
- 5 architectural subsystems must be fully implemented
- Final test suite: 93 tests total (33 current + 60 to be implemented)

**Blocking**: No new wave authorized until all 60 features implemented

---

**Implementation Approach**:
1. Phase 1: Architecture Freeze - Freeze architecture for all 5 feature categories
2. Phase 2: QA Verification - Verify all 60 tests correctly validate requirements
3. Phase 3: Builder Assignment - Assign builders per feature category
4. Phase 4: Build-to-Green Execution - Implement features until all 60 tests pass
5. Phase 5: Final Verification - Confirm 100% pass rate (93 tests total)

**Feature Implementation Priority**: 
1. Governance Supremacy (11 tests) - CRITICAL
2. Evidence Integrity (14 tests) - HIGH
3. Evidence Schema Validation (15 tests) - HIGH
4. Decision Determinism (11 tests) - HIGH
5. Liveness Continuity (9 tests) - MEDIUM

**Success Criteria**: 
- All 60 tests GREEN (100% pass rate)
- All features implemented per architecture specifications
- Zero test debt remaining
- Tests moved from RED_QA/ to active suite
- Final test count: 93 tests passing

**Owner**: FM (orchestrator) + assigned builders per category  
**Next Step**: Create implementation wave plan

**Related Documents**:
- `governance/incidents/INCIDENT-20251222-TEST-DEBT.md`
- `tests/wave0_minimum_red/RED_QA/README.md`
- `tests/wave0_minimum_red/RED_QA/IMPLEMENTATION_TRACKING.md`
- `governance/rca/RCA_WAVE_0_60_TESTS_WITHOUT_ARCHITECTURAL_REQUIREMENT.md` (proves tests ARE valid)
- `governance/incidents/HISTORICAL_WAVE_PR_WARNING_TEST_DEBT_SURVEY_RCA.md`

**Tracking**:
- [x] Tests restored (PR #479, revert of PR #470)
- [x] RCA completed proving tests are architecturally valid
- [x] RED_QA directory restored with all 60 tests
- [x] pytest.ini exclusion confirmed in place
- [x] CS2 DECISION MADE: IMPLEMENT ALL 60 FEATURES (2026-01-08)
- [ ] Create implementation wave plan (Wave 1.5 or Wave 2.0)
- [ ] Architecture freeze executed for all 5 feature categories
- [ ] Builders assigned per category
- [ ] Build-to-Green execution in progress
- [ ] All 60 tests GREEN (final verification)
- [ ] Tests moved to active suite, RED_QA directory removed

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

### DEBT-004: Warning Baseline Remediation (Pytest Markers)

**Debt ID**: DEBT-004  
**Type**: Warnings (Configuration/Registration)  
**Severity**: LOW to MEDIUM  
**Debt Size**: 64 warnings (PytestUnknownMarkWarning)  
**Origin**: Test dodging prevention governance (INCIDENT-2026-01-08-WARNING-SUPPRESSION)  
**Origin Date**: 2026-01-08  
**Builder**: qa-builder  
**Status**: UNRESOLVED  
**Age**: 0 days (as of 2026-01-08)

**Debt Description**:
64 `PytestUnknownMarkWarning` warnings revealed after removing `--disable-warnings` from pytest.ini. Warnings indicate custom pytest markers used in tests but not registered in pytest.ini. Eight unregistered markers identified: chp, commissioning, governance_sync, guard, lifecycle, memory, startup, ui.

**Discovery Context**:
Warnings were hidden by `--disable-warnings` in pytest.ini (test dodging violation). After emergency remediation removing warning suppression, established warning baseline documenting all exposed warnings.

**Root Cause**:
- Custom pytest markers added to tests without registering in pytest.ini
- No marker registration process established
- Tests written before governance enforcement of marker registration

**Affected Markers**:
1. `chp` (7 occurrences) - CHP memory integration tests
2. `commissioning` (5 occurrences) - Commissioning controller tests
3. `governance_sync` (12 occurrences) - Governance memory sync tests
4. `guard` (count unknown) - Guard/validation tests
5. `lifecycle` (9 occurrences) - Memory lifecycle tests
6. `memory` (multiple) - Memory subsystem tests
7. `startup` (count unknown) - Startup/initialization tests
8. `ui` (9 occurrences) - UI component/wizard tests

**Impact**:
- Immediate: LOW (tests run correctly, functional impact zero)
- Medium-term: LOW-MEDIUM (noise in test output, potential typo masking)
- Long-term: MEDIUM (reduces test categorization reliability)

**Remediation Options**:
1. **Register markers** (recommended): Add all 8 markers to pytest.ini with descriptions
2. **Remove markers**: Delete marker decorators, use existing markers
3. **Consolidate markers**: Map to existing markers where overlap exists

**Elimination Plan**:
- **Phase 1**: Analyze marker usage patterns and test categorization strategy
- **Phase 2**: Decide registration vs. consolidation for each marker
- **Phase 3**: Update pytest.ini or remove/replace markers in tests
- **Phase 4**: Verification (confirm ZERO PytestUnknownMarkWarning)

**Owner**: qa-builder  
**Deadline**: 2026-01-22 (14 days from registration)  
**Escalation**: If deadline missed, document reason and extend deadline (non-blocking debt)

**Related Documents**:
- `governance/warning-baseline.md` (detailed inventory)
- `governance/incidents/INCIDENT-2026-01-08-WARNING-SUPPRESSION.md`
- `governance/policies/ZERO_WARNING_TEST_DEBT_IMMEDIATE_REMEDY_DOCTRINE.md`

**Tracking**:
- [x] Warning baseline documented
- [ ] Phase 1: Usage analysis complete
- [ ] Phase 2: Remediation strategy defined
- [ ] Phase 3: Implementation complete
- [ ] Phase 4: Verification complete (ZERO marker warnings)

---

## Debt Statistics

**Total Active Debt Items**: 3  
**Total Resolved Debt Items**: 1 (DEBT-003)  
**Total Warnings**: 258 (DEBT-001: 194, DEBT-004: 64)  
**Total Unimplemented Tests**: 60 (DEBT-002 - RESTORED)  
**Oldest Debt Age**: 17+ days (DEBT-002)  
**Average Debt Age**: ~8 days  

**By Severity (Active)**:
- HIGH: 1 (DEBT-002)
- MEDIUM: 1 (DEBT-001)
- LOW-MEDIUM: 1 (DEBT-004)

**By Builder**:
- schema-builder: 1 debt item (DEBT-001)
- qa-builder: 1 debt item (DEBT-004)
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
**2026-01-08**: DEBT-002 tests incorrectly removed in PR #470, then restored via revert PR #478  
**2026-01-08**: DEBT-004 registered (64 pytest marker warnings revealed after warning suppression removed)  
**Next Audit**: 2026-02-07

---

**Maintained By**: FM Agent  
**Last Updated**: 2026-01-08  
**Status**: Active (3 unresolved items, 1 resolved)  
**Latest Update**: DEBT-004 registered after warning baseline established

---

**END OF DEBT REGISTER**
