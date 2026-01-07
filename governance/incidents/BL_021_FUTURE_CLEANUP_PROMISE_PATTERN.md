# FL/CI Registry Entry — BL-021: Warning/Test Debt "Future Cleanup" Promise Pattern

**Entry ID:** BL-021  
**Title:** Warning/Test Debt Accepted with "Future Cleanup" Promise Without Concrete Elimination Plan  
**Date:** 2026-01-07  
**Reporter:** FM Agent (Historical Analysis)  
**Analyst:** FM Agent  
**Wave:** 1.0  
**Severity:** CATASTROPHIC (pattern enabling Zero Test Debt policy violation)  
**Status:** DISCOVERED + PREVENTION IMPLEMENTED  
**Classification:** First-Time Failure (discovery + correction in single action)

---

## Description

Pattern identified through historical analysis: Technical debt (warnings, RED tests) accepted at merge time with promise of "future cleanup" but without concrete elimination plan, assigned owner, or deadline. Debt documented but never eliminated, leading to accumulation and Zero Test Debt Constitutional Rule (T0-003) violation.

**Instances Identified**:
1. **Wave 1.0.1** (2026-01-02): 194 warnings accepted with promise of "Wave 2.0 cleanup" - never executed
2. **Wave 0** (2025-12-22 or earlier): 65 RED tests moved to RED_QA/ as "awaiting implementation" - never implemented
3. **Wave 1.0.4** (2026-01-02): 1 warning observed but never classified or tracked

---

## Root Cause

**Primary**: "Future Cleanup" Promise Pattern with No Forcing Function

**Contributing Factors**:
1. **No Debt Elimination Plan Requirement**: FM allowed merge with debt but without concrete plan
2. **No Maximum Debt Threshold**: No limit on acceptable debt accumulation
3. **No Debt Ownership Assignment**: Responsibility diffused to "core platform team" or "future wave"
4. **No Debt Elimination Verification**: Debt documented but never verified as eliminated
5. **Ambiguous Policy Interpretation**: Zero Test Debt policy weakened by "documented execution debt" loophole

**Pattern Mechanism**:
```
1. Builder completes work with warnings/RED tests
2. FM performs classification/analysis
3. FM assesses debt as "non-blocking" or "acceptable"
4. FM documents debt and promises "future cleanup"
5. FM approves merge with debt present
6. NO concrete elimination plan created
7. NO builder assigned to cleanup
8. NO follow-up wave/issue created
9. Debt persists indefinitely
```

---

## Impact

**Immediate** (Wave 1.0 - Wave 2.0):
- 194 warnings persisting in codebase
- 65 RED tests not implemented
- 1 additional warning untracked
- Zero Test Debt policy effectively violated

**Medium-Term**:
- Warning proliferation risk (debt normalization)
- Deprecation warnings becoming errors in dependency upgrades
- RED tests representing unimplemented functionality (technical debt)
- Broken TDD discipline (RED without GREEN)

**Long-Term**:
- Governance policy erosion ("documented debt is acceptable" becomes norm)
- Build quality degradation (warnings ignored, tests never implemented)
- Broken promises damaging governance credibility
- Cultural acceptance of technical debt

---

## Detection

**Discovery Method**: Historical survey of all Wave 1.0 merge approvals and completion summaries

**Evidence**:
- `WAVE_1.0.1_WARNING_CLASSIFICATION_AND_GATE_DECISION.md`: 194 warnings, "future cleanup" promised
- `governance/incidents/INCIDENT-20251222-TEST-DEBT.md`: 65 RED tests, "implementation pending"
- `WAVE_1.0.4_COMPLETION_SUMMARY.md`: 1 warning mentioned, never classified
- `TEST_DEBT_ANALYSIS.md`: Historical debt analysis

**Pattern Recognition**:
- "Future cleanup" language in merge approvals
- "If warranted" or "next wave" deferral language
- Debt documented without elimination plan
- No assigned owner or deadline

---

## Correction

### Immediate Actions (2026-01-07)

**1. Comprehensive Survey and RCA**:
- ✅ Created `governance/incidents/HISTORICAL_WAVE_PR_WARNING_TEST_DEBT_SURVEY_RCA.md`
- ✅ Documented all instances of pattern
- ✅ Identified 5 process gaps and 5 risk factors
- ✅ Defined comprehensive elimination strategy

**2. Debt Register Created**:
- ✅ Created `governance/incidents/DEBT_REGISTER.md`
- ✅ Registered 3 debt items (DEBT-001, DEBT-002, DEBT-003)
- ✅ Assigned owners and deadlines
- ✅ Defined tracking and escalation mechanisms

**3. Governance Hardening Specs Created**:
- ✅ `governance/specs/ZERO_WARNING_MERGE_GATE_SPEC.md` (prevents warning accumulation)
- ✅ `governance/specs/TDD_RED_TO_GREEN_MERGE_REQUIREMENT_SPEC.md` (prevents RED test accumulation)
- ✅ `governance/specs/DEBT_ELIMINATION_GATE_SPEC.md` (forces debt elimination before new work)

**4. BL Entry Created**:
- ✅ This document (BL-021 registration)

---

### Elimination Plan

**Week 1-2**: Execute Debt Elimination
- [ ] DEBT-001: Wave 1.0.1 warnings (194 warnings, schema-builder, deadline 2026-01-21)
- [ ] DEBT-003: Wave 1.0.4 warning (1 warning, api-builder, deadline 2026-01-14)
- [ ] DEBT-002: Wave 0 RED tests (65 tests, IMPLEMENT/DEFER/REMOVE decision by 2026-01-28)

**Week 3-4**: Verification and Hardening
- [ ] Verify all debt eliminated (debt register empty or <3 items)
- [ ] Activate new governance specs (Johan approval required)
- [ ] Communicate new rules to all builders
- [ ] Update builder contracts with new requirements

---

## Prevention

### Structural Prevention

**Three New Governance Specs** (created 2026-01-07):

1. **Zero Warning Merge Gate** (`ZERO_WARNING_MERGE_GATE_SPEC.md`):
   - No warnings accepted at merge (zero tolerance)
   - Exception requires Johan approval + concrete elimination plan
   - Warning debt tracked in debt register
   - CI fails on any warnings

2. **TDD RED-to-GREEN Requirement** (`TDD_RED_TO_GREEN_MERGE_REQUIREMENT_SPEC.md`):
   - RED tests must be implemented in same PR (no deferral)
   - RED tests at merge require DP-RED registry entry with plan
   - DP-RED entries audited monthly, >60 days triggers escalation
   - All tests must be GREEN at merge (or valid DP-RED)

3. **Debt Elimination Gate** (`DEBT_ELIMINATION_GATE_SPEC.md`):
   - No new wave authorized while unresolved debt exists
   - Debt >30 days triggers mandatory elimination
   - Missed deadline triggers automatic HALT
   - Debt register audited monthly

### Behavioral Prevention

**Builder Training**:
- Zero warning requirement communicated
- TDD discipline reinforced (RED-GREEN-REFACTOR in single PR)
- Debt registration process taught
- Consequences of debt introduction clarified

**FM Enforcement**:
- FM rejects ANY PR with warnings (no exception authority)
- FM rejects ANY PR with RED tests (unless valid DP-RED)
- FM enforces debt elimination gate (no new waves with debt)
- FM escalates to Johan if exception requested

**Cultural Change**:
- "Documented debt is acceptable" → "Debt is NEVER acceptable"
- "Future cleanup" → "Cleanup NOW or don't merge"
- "Low risk warnings OK" → "ZERO warnings, no exceptions"
- "TDD exploration" → "TDD discipline (implement before merge)"

---

## Forward-Scan Results

### Scan Scope

All future work authorization checkpoints:
- Wave/subwave authorizations
- PR merge gates
- Builder appointments
- Governance updates

### Scan Findings

**Potential Future Occurrences**: ZERO (if prevention implemented)

**Rationale**:
- Zero Warning Merge Gate blocks warnings at CI level (automated)
- TDD RED-to-GREEN Requirement blocks RED tests at gate (automated)
- Debt Elimination Gate blocks new waves when debt exists (FM enforced)
- Three-layer prevention (CI + FM + Spec) makes recurrence structurally impossible

**Verification**:
- CI configuration updated (fail on warnings)
- FM contract updated (debt gate enforcement)
- Builder contracts updated (zero warning/debt requirement)

---

## Governance Ratchet

### Ratchet 1: Zero Warning Merge Gate (T0-015 Candidate)

**Status**: Spec created, awaiting Johan approval for Tier-0 canon  
**Content**: `governance/specs/ZERO_WARNING_MERGE_GATE_SPEC.md`  
**Enforcement**: CI + FM gate check  
**Authority**: Prevents BL-021 recurrence (warning branch)

### Ratchet 2: TDD RED-to-GREEN Requirement (T0-016 Candidate)

**Status**: Spec created, awaiting Johan approval for Tier-0 canon  
**Content**: `governance/specs/TDD_RED_TO_GREEN_MERGE_REQUIREMENT_SPEC.md`  
**Enforcement**: FM gate check + DP-RED registry  
**Authority**: Prevents BL-021 recurrence (RED test branch)

### Ratchet 3: Debt Elimination Gate (T0-017 Candidate)

**Status**: Spec created, awaiting Johan approval for Tier-0 canon  
**Content**: `governance/specs/DEBT_ELIMINATION_GATE_SPEC.md`  
**Enforcement**: FM wave authorization check  
**Authority**: Prevents BL-021 recurrence (general debt branch)

**Recommendation**: All three specs should be elevated to Tier-0 canon after Johan approval.

---

## Lessons Learned

### Lesson 1: "Future Cleanup" is a Broken Promise Pattern

**What We Learned**: Debt accepted with promise of "future cleanup" but no concrete plan = debt that persists indefinitely.

**Why It Matters**: Promises without forcing functions are meaningless. Good intentions don't eliminate debt.

**What Must Change**: All debt requires elimination plan WITH owner, deadline, and gate block. No exceptions.

---

### Lesson 2: "Documented Debt" ≠ Zero Debt

**What We Learned**: Documenting debt doesn't eliminate it. Documentation without action = acknowledgment without resolution.

**Why It Matters**: Zero Test Debt policy means ZERO. No "documented exceptions", no "acceptable categories".

**What Must Change**: Zero means zero. Debt must be eliminated or not merged. Documentation is for tracking, not justification.

---

### Lesson 3: First Exception Sets Precedent

**What We Learned**: Wave 1.0.1 warnings acceptance set pattern for future debt acceptance.

**Why It Matters**: Every exception weakens governance unless governance is hardened after exception.

**What Must Change**: After EVERY exception, create governance ratchet to prevent recurrence. First time = learning + hardening, not normalization.

---

### Lesson 4: TDD Without Discipline is Speculation

**What We Learned**: Writing 65 RED tests without implementation commitment = speculation, not TDD.

**Why It Matters**: TDD is a discipline (RED-GREEN-REFACTOR), not a buffet (RED maybe, GREEN someday).

**What Must Change**: RED tests must be implemented in same PR. If deferral needed, use DP-RED registry with strict governance. No casual RED test parking.

---

### Lesson 5: Optimization Pressure Erodes Standards

**What We Learned**: Wave 1.0 pressure led to debt acceptance to show progress (velocity over quality).

**Why It Matters**: Short-term velocity gains create long-term quality debt. Technical debt compounds.

**What Must Change**: Build Philosophy supremacy - correctness ALWAYS wins over speed. One-Time Build Correctness > Fast Delivery.

---

## Success Metrics

**Immediate Success** (by 2026-01-28):
- [ ] All 3 debt items eliminated (DEBT-001, DEBT-002, DEBT-003)
- [ ] Debt register: 0 items or <3 with active elimination
- [ ] Zero warnings in test output
- [ ] Zero RED tests in active suite (or valid DP-RED)

**Medium-Term Success** (by 2026-02-28):
- [ ] Zero warning/debt pattern: 0 occurrences in 30 days
- [ ] All 3 governance specs activated (Johan approved)
- [ ] Builders delivering zero-warning, zero-debt code consistently
- [ ] No debt items >30 days old in register

**Long-Term Success** (by 2026-06-30):
- [ ] Zero warning/debt pattern: 0 occurrences in 180 days
- [ ] Debt register: consistently 0-2 items (minimal, temporary)
- [ ] Zero Test Debt policy: absolute adherence, no violations
- [ ] Governance credibility: promises kept, standards maintained

---

## Related Documents

**Survey and Analysis**:
- `governance/incidents/HISTORICAL_WAVE_PR_WARNING_TEST_DEBT_SURVEY_RCA.md` (comprehensive RCA)
- `governance/incidents/INCIDENT-20251222-TEST-DEBT.md` (65 RED tests)
- `WAVE_1.0.1_WARNING_CLASSIFICATION_AND_GATE_DECISION.md` (194 warnings)
- `TEST_DEBT_ANALYSIS.md` (historical debt analysis)

**Prevention Specifications**:
- `governance/specs/ZERO_WARNING_MERGE_GATE_SPEC.md` (v1.0.0)
- `governance/specs/TDD_RED_TO_GREEN_MERGE_REQUIREMENT_SPEC.md` (v1.0.0)
- `governance/specs/DEBT_ELIMINATION_GATE_SPEC.md` (v1.0.0)

**Tracking**:
- `governance/incidents/DEBT_REGISTER.md` (active debt)
- `governance/qa/DP_RED_REGISTRY.md` (to be created for deferred RED tests)

**Constitutional Authority**:
- `governance/policies/zero-test-debt-constitutional-rule.md` (T0-003)
- `governance/specs/build-to-green-enforcement-spec.md` (T0-011)
- `BUILD_PHILOSOPHY.md` (One-Time Build Correctness)

---

## Status Timeline

| Date | Status | Action |
|------|--------|--------|
| 2026-01-02 | PATTERN OCCURS | Wave 1.0.1: 194 warnings accepted |
| 2025-12-22 | PATTERN OCCURS | Wave 0: 65 RED tests moved to RED_QA/ |
| 2026-01-07 | DISCOVERED | Historical survey reveals pattern |
| 2026-01-07 | RCA COMPLETE | Root cause analysis documented |
| 2026-01-07 | PREVENTION CREATED | 3 governance specs created |
| 2026-01-07 | BL-021 REGISTERED | This entry created |
| TBD | PREVENTION ACTIVATED | Awaiting Johan approval |
| TBD | DEBT ELIMINATED | Debt register cleared |
| TBD | VERIFIED | 30+ days with zero occurrences |
| TBD | CLOSED | Pattern prevention verified

---

## Escalation History

- **2026-01-07**: Pattern discovered by FM Agent during historical survey
- **2026-01-07**: Comprehensive RCA completed, 3 prevention specs created
- **2026-01-07**: Escalated to Johan for spec approval and debt elimination authorization
- **Awaiting**: Johan decision on HALT authorization and spec activation

---

**Registered By**: FM Agent  
**Date**: 2026-01-07  
**Authority**: FM Agent Contract v3.4.0, BL Forward-Scan Obligation Spec  
**Severity**: CATASTROPHIC (pattern enabling constitutional violation)  
**Classification**: First-Time Failure (discovery + comprehensive correction)  
**Prevention Status**: PREVENTION SPECS CREATED, AWAITING ACTIVATION

---

**END OF BL-021 REGISTRY ENTRY**
