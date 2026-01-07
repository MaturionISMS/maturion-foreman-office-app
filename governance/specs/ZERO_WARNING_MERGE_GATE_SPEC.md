# Zero Warning Merge Gate Specification

**Spec ID**: ZERO-WARNING-MERGE-GATE-SPEC  
**Version**: 1.0.0  
**Status**: PROPOSED  
**Date**: 2026-01-07  
**Authority**: FM Agent Contract v3.4.0, BL-021 Prevention  
**Purpose**: Prevent accumulation of warnings by enforcing zero-warning requirement at merge gate

---

## Executive Summary

This specification defines a strict zero-warning policy for all PR merge gates. NO warnings are acceptable at merge time. Any warning must be resolved or, in exceptional cases, approved by Johan with mandatory elimination plan.

**Key Principle**: Warnings are unresolved issues, not acceptable "noise". All warnings MUST be eliminated before merge.

---

## Scope

**Applies To**:
- All PR merge gates (Wave, Subwave, Governance, Hotfix)
- All test execution contexts (unit, integration, E2E)
- All warning types (deprecation, tooling, linting, type checking, framework)

**Does NOT Apply To**:
- Development branches (pre-PR)
- Local development environments
- Exploratory prototypes (not merged)

---

## Gate Check: Zero Warning Requirement

### Primary Rule

**CI MUST report ZERO warnings for PR to be eligible for merge.**

```
PASS Criteria: 
  - Test count: N/N passing (100%)
  - Warning count: 0 (ZERO)
  - Error count: 0 (ZERO)

FAIL Criteria:
  - Warning count: >0 (ANY warnings = GATE BLOCKED)
```

### Implementation

**CI Configuration**:
- Test runners configured to fail on warnings (e.g., `pytest --strict-warnings`, `eslint --max-warnings 0`)
- Build tools configured to treat warnings as errors
- All warning output captured and reported

**Gate Automation**:
- GitHub Actions workflow checks warning count
- PR status check: "Zero Warning Gate" = PASS only if warning count = 0
- PR merge blocked if warning count >0

---

## Warning Classification Requirement

### Mandatory Classification

Before any exception discussion, ALL warnings MUST be classified:

**Classification Template**:
```
Warning ID: W-<number>
Warning Text: <exact warning message>
Source File: <file:line>
Category: <see categories below>
Severity: <CRITICAL|HIGH|MEDIUM|LOW>
Root Cause: <why warning generated>
Fix Complexity: <TRIVIAL|SIMPLE|MODERATE|COMPLEX>
Fix Risk: <LOW|MEDIUM|HIGH>
Recommended Action: <FIX|SUPPRESS|ESCALATE>
```

**Warning Categories**:
1. **Deprecation**: Feature/API marked as deprecated by upstream
2. **Type Safety**: Type mismatch, missing type hints, coercion issues
3. **Linting**: Style violations, unused imports, formatting
4. **Framework**: Test framework internals, plugin compatibility
5. **Security**: Potential security issues (insecure randomness, SQL injection risk)
6. **Performance**: Performance degradation warnings
7. **Configuration**: Misconfigured tools or dependencies
8. **Other**: Uncategorized (requires investigation)

---

## Acceptable Warning Categories

**Zero**.

**Rationale**: All warnings represent unresolved issues. If a warning is acceptable, it should be suppressed at the source (not ignored). If it cannot be suppressed, it must be fixed.

---

## Exception Process

### When Exception May Be Considered

ONLY when ALL of the following are true:
1. Warning source is external (upstream dependency, not our code)
2. Fix requires major refactoring or dependency upgrade outside PR scope
3. Warning does NOT indicate correctness, security, or safety issue
4. Temporary suppression is not feasible or advisable
5. Risk assessment concludes warning is LOW risk in short term (<30 days)

### Exception Approval Authority

**Johan ONLY**.

FM Agent does NOT have authority to approve warning exceptions.

### Exception Requirements

If Johan grants exception, ALL of the following MUST be provided:

1. **Elimination Plan**:
   - Concrete steps to eliminate warning
   - Assigned owner (builder or team member)
   - Deadline (maximum 30 days from exception grant)
   - Verification criteria (how will ZERO state be confirmed)

2. **Tracking**:
   - Entry in `governance/incidents/DEBT_REGISTER.md`
   - Debt ID assigned
   - Weekly status updates required

3. **Gate Block**:
   - No new waves authorized until warning eliminated
   - Exception blocks all downstream work

4. **Escalation**:
   - If deadline missed, automatic HALT and escalate to Johan
   - If warning proliferates (>1 additional warning in same category), automatic HALT

---

## Debt Register Integration

### Registration

Every accepted warning (if exception granted) MUST be registered in debt register:

**Debt Entry Template**:
```
Debt ID: DEBT-<number>
Type: Warning
Severity: <from classification>
Debt Size: <warning count>
Origin: <PR number, wave, builder>
Origin Date: <merge date>
Owner: <assigned individual>
Deadline: <max 30 days from origin>
Status: UNRESOLVED
```

### Audit

- Monthly audit of debt register
- Any warning debt item >30 days triggers escalation
- Any warning debt item >60 days triggers HALT and Johan escalation

---

## Prevention Mechanisms

### Pre-Merge Validation

**PR Author Checklist**:
- [ ] Run tests locally with strict warnings enabled
- [ ] Verify zero warnings before creating PR
- [ ] If warnings present, fix or classify before PR submission

**CI Validation**:
- [ ] Zero Warning Gate check runs on every PR
- [ ] Warning count displayed in PR status
- [ ] Merge button disabled if warnings present

### Builder Contracts

**Builder Responsibility**:
- Builders MUST deliver code with zero warnings
- Builder QA reports MUST include warning count (expected: 0)
- Builders MUST NOT submit PR with warnings

**FM Enforcement**:
- FM rejects any PR with warnings (no exception authority)
- FM escalates to Johan if builder requests exception
- FM verifies elimination plan if exception granted

---

## Monitoring and Alerting

### Warning Trend Monitoring

**Metrics Tracked**:
- Warning count per PR (expected: 0)
- Warning count trend across waves
- Warning proliferation rate (warnings in category over time)
- Exception grant frequency

**Alert Thresholds**:
- Any PR with warnings = immediate alert
- 2+ exceptions granted in 30 days = escalation to Johan
- Warning proliferation detected (>3 warnings in same category) = automatic HALT

### Dashboard

**Zero Warning Dashboard** (to be created):
- Current PR warning count (real-time)
- Historical warning trend (chart)
- Active exception count (should be 0 or minimal)
- Debt register summary (warning items)

---

## Rationale

### Why Zero Warnings?

1. **Warnings are unresolved issues**: Not informational, not acceptable noise
2. **Warnings accumulate**: First warning tolerated → 10 warnings tolerated → 100 warnings ignored
3. **Warnings hide problems**: Real issues buried in warning noise
4. **Warnings erode standards**: "Some warnings OK" → "Many warnings OK" → "Warnings don't matter"
5. **Warnings block future upgrades**: Deprecation warnings become errors in new versions

### Why No "Acceptable Warning Categories"?

Because "acceptable" is subjective and leads to:
- Category expansion: "Deprecation acceptable" → "Framework acceptable" → "All acceptable"
- Warning accumulation: "This deprecation OK" → "10 deprecations OK" → "100 deprecations OK"
- Policy erosion: Zero Warning policy → "Zero critical warnings" → "Zero blocking warnings" → "Minimize warnings"

### Why Johan-Only Exception Authority?

Because:
- FM lacks authority to weaken governance
- Builder cannot self-approve exceptions
- Centralized control prevents exception proliferation
- High bar ensures exceptions are truly exceptional

---

## Failure Mode: Warning Acceptance Pattern

**Pattern Description**: Warning present at merge, classified as "acceptable temporary debt", promised "future cleanup", no concrete plan, debt persists indefinitely.

**Pattern ID**: BL-021 (registered)

**Prevention**: This specification

**Detection**: Warning count >0 at merge = pattern occurrence

**Response**: GATE BLOCKED, no merge until warning resolved or Johan exception granted with elimination plan

---

## Success Criteria

**Zero Warning State Achieved**:
- All PRs merged: warning count = 0
- Debt register: zero warning items (or <3 with active elimination)
- Exception count: 0 (or <2 per 30 days with justification)
- Warning trend: flat at zero (no proliferation)

**Zero Warning Discipline Maintained**:
- PR authors verify zero warnings before submission
- CI enforces zero warnings at gate
- FM rejects any PR with warnings
- Builders deliver zero-warning code consistently

---

## Rollout Plan

### Phase 1: Specification Approval (Week 1)
- Submit this spec for Johan review
- Obtain approval for zero-warning policy
- Communicate policy to all builders

### Phase 2: CI Implementation (Week 2)
- Update test runner configs (pytest, eslint, etc.) to fail on warnings
- Create GitHub Actions workflow for Zero Warning Gate check
- Enable gate check on all PRs

### Phase 3: Debt Elimination (Week 3-4)
- Eliminate existing warnings (DEBT-001, DEBT-003 from register)
- Verify all active PRs have zero warnings
- Achieve clean baseline

### Phase 4: Enforcement (Ongoing)
- Monitor zero-warning compliance
- Enforce gate blocks
- Audit exception grants
- Maintain zero-warning discipline

---

## Related Documents

- `governance/incidents/HISTORICAL_WAVE_PR_WARNING_TEST_DEBT_SURVEY_RCA.md` (pattern RCA)
- `governance/incidents/DEBT_REGISTER.md` (active debt tracking)
- `governance/specs/TDD_RED_TO_GREEN_MERGE_REQUIREMENT_SPEC.md` (related spec)
- `governance/specs/DEBT_ELIMINATION_GATE_SPEC.md` (related spec)
- `governance/policies/zero-test-debt-constitutional-rule.md` (T0-003)

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-07 | FM Agent | Initial specification |

---

**Status**: PROPOSED - Awaiting Johan approval  
**Authority**: FM Agent Contract v3.4.0  
**Purpose**: Prevent warning accumulation, maintain Zero Test Debt discipline

---

**END OF ZERO WARNING MERGE GATE SPECIFICATION**
