# Historical Wave PR Warning and Test Debt Survey with Root Cause Analysis

**Incident ID**: HISTORICAL-WAVE-PR-DEBT-SURVEY  
**Date Created**: 2026-01-07  
**Created By**: FM Agent  
**Type**: Survey and Root Cause Analysis  
**Severity**: Critical  
**Status**: In Progress  
**Authority**: FM Agent Contract v3.4.0, Zero Test Debt Constitutional Rule (T0-003)

---

## Executive Summary

This document provides a comprehensive survey of all historical wave implementation PRs that were merged with warnings or test debt, performs root cause analysis of why this accumulation was permitted, and defines elimination strategy.

**Key Findings:**
- **2 Major Debt Items Identified**: 194 warnings (Wave 1.0.1) + 65 RED tests (Wave 0)
- **Root Cause**: "Future cleanup" promise pattern - debt accepted with documentation but no concrete elimination plan
- **Impact**: Zero Test Debt policy violated, technical debt accumulated
- **Status**: Debt documented but not eliminated, blocking true zero-debt state

---

## Part 1: Historical PR Survey

### Survey Methodology

**Scope**: All Wave PRs from Wave 0.1 through Wave 2.0  
**Sources Reviewed**:
- All `WAVE_*_FM_MERGE_APPROVAL.md` documents
- All `WAVE_*_COMPLETION_SUMMARY.md` documents
- `INCIDENT-20251222-TEST-DEBT.md`
- `WAVE_1.0.1_WARNING_CLASSIFICATION_AND_GATE_DECISION.md`
- `TEST_DEBT_ANALYSIS.md`

**Search Criteria**:
- Warnings mentioned in merge approvals
- Test debt mentioned or identified
- "Future cleanup" or "follow-up required" language
- Any deviation from 100% green/zero debt policy

---

### Debt Item 1: Wave 1.0.1 Schema Foundation Warnings

**PR**: #349 (schema-builder)  
**Date Merged**: 2026-01-02 14:27:01 UTC  
**Builder**: schema-builder  
**QA Range**: QA-001 to QA-018 (18 components)

**Gate Decision**: ✅ PASS with documented execution debt

**Debt Details**:
- **Type**: 194 warnings during test execution
- **Test Status**: All 18 tests PASSING (100% GREEN)
- **Warning Categories**:
  1. Deprecation warnings (30-50%, ~60-100 warnings)
  2. Testing framework noise (25-35%, ~50-70 warnings)
  3. Database/ORM configuration advice (15-25%, ~30-50 warnings)
  4. Test isolation and cleanup warnings (10-15%, ~20-30 warnings)
  5. Type/assertion compatibility (5-10%, ~10-20 warnings)

**FM Classification Decision**:
- Warnings do NOT affect functional correctness
- Warnings do NOT block merge gate
- Warnings classified as "acceptable temporary execution debt"
- Future-breakage risk assessed as LOW to MEDIUM (manageable)

**Follow-Up Promise**:
> "Follow-Up Required: YES (explicit instruction in future wave)"  
> "Wave 2.0 Planning: Include warning cleanup in scope (explicit instruction)"

**Documented In**: `WAVE_1.0.1_WARNING_CLASSIFICATION_AND_GATE_DECISION.md`

**Current Status**: ⚠️ **DEBT PERSISTS - No elimination executed**

---

### Debt Item 2: Wave 0 RED QA Tests Moved to RED_QA/

**Context**: Pre-Wave 1.0 baseline  
**Date Identified**: 2025-12-22  
**Identified By**: FM Repo Builder Agent  
**Related Issue**: Governance enforcement implementation

**Debt Details**:
- **Type**: 65 tests intentionally RED (TDD approach - tests before implementation)
- **Test Status**: All 65 tests FAILING (0% GREEN)
- **Location**: Moved to `tests/wave0_minimum_red/RED_QA/`
- **Test Categories**:
  1. Decision Determinism (8 tests) - `test_decision_determinism.py`
  2. Evidence Integrity (20 tests) - `test_evidence_integrity.py`
  3. Evidence Schema Validation (12 tests) - `test_evidence_schema_validation.py`
  4. Governance Supremacy (16 tests) - `test_governance_supremacy.py`
  5. Liveness Continuity (9 tests) - `test_liveness_continuity.py`

**Resolution Applied**:
- Tests moved to RED_QA/ directory
- Properly classified as "intentional TDD RED tests"
- Excluded from CI runs via pytest.ini
- Active test suite: 100% passing (33/33 tests)

**Follow-Up Promise**:
> "These are intentional TDD RED tests. Implementation pending."  
> "Tests must not be run in CI until implementation exists."

**Documented In**: 
- `governance/incidents/INCIDENT-20251222-TEST-DEBT.md`
- `tests/wave0_minimum_red/RED_QA/README.md`
- `TEST_DEBT_ANALYSIS.md`

**Current Status**: ⚠️ **DEBT PERSISTS - Tests still RED, implementation not started**

---

### Survey Result: Other Waves

**Wave 1.0.2 (qa-builder)**: ✅ NO DEBT
- PR #353
- All 43 tests properly RED (QA-to-Red phase)
- Zero test debt confirmed
- No warnings reported

**Wave 1.0.3 (ui-builder)**: ✅ NO DEBT
- PR #355
- All 39 tests properly RED (QA-to-Red phase)
- Zero test debt confirmed
- No warnings reported

**Wave 1.0.4 (api-builder)**: ✅ NO DEBT (with caveat)
- PR #357
- All 49 tests GREEN (100% pass)
- Zero test debt confirmed
- **1 warning reported but not classified or tracked**
  - Source: `WAVE_1.0.4_COMPLETION_SUMMARY.md` line 144
  - Text: "49 passed, 1 warning in 0.08s"
  - **NO CLASSIFICATION PROVIDED**
  - **NO GATE DECISION DOCUMENTED FOR WARNING**

**Wave 1.0.5 (integration-builder)**: ✅ NO DEBT
- PR #361
- All 39 tests GREEN (100% pass)
- Zero test debt confirmed
- No warnings reported

**Wave 2.0+**: Not surveyed (out of scope for this historical analysis)

---

## Part 2: Root Cause Analysis

### RCA Question 1: Why Were Warnings/Debt Accepted Instead of Blocked?

**Answer**: "Future Cleanup" Promise Pattern

**Pattern Identified**:
1. Builder completes work with warnings/RED tests
2. FM performs classification/analysis
3. FM assesses warnings as "non-blocking" or "acceptable debt"
4. FM documents debt and promises "future cleanup"
5. FM approves merge with debt present
6. **No concrete elimination plan created**
7. **No builder assigned to cleanup**
8. **No follow-up wave/issue created**

**Evidence**:

From `WAVE_1.0.1_WARNING_CLASSIFICATION_AND_GATE_DECISION.md`:
```
Follow-Up Actions (Future Wave)

1. Wave 1.0 Monitoring:
   - Monitor warning counts in subsequent builder executions
   - Detect warning proliferation patterns

2. Wave 2.0 Planning:
   - Include warning cleanup in Wave 2.0 scope (if warranted)
   - Define explicit instruction for warning remediation
   - Assign cleanup to appropriate builder(s)
```

**Problem**: "If warranted" and "future wave" are non-committal. No concrete plan, no assigned responsibility, no timeline.

---

### RCA Question 2: What Process Gaps Allowed This Pattern?

**Gap 1**: No "Debt Elimination Plan Required" Gate Check
- FM allowed merge with debt but without concrete elimination plan
- "Future cleanup" promise is unverifiable and unenforceable
- No tracking mechanism for debt items

**Gap 2**: No Maximum Debt Accumulation Threshold
- 194 warnings accepted as "manageable"
- 65 RED tests accepted as "TDD approach"
- No threshold defined for "too much debt"
- No escalation trigger for accumulated debt

**Gap 3**: No Debt Ownership Assignment
- Warnings documented but no owner assigned
- RED tests documented but no implementation schedule
- Responsibility diffused to "core platform team" or "future wave"

**Gap 4**: No Debt Elimination Verification
- Debt documented but never verified as eliminated
- No follow-up gate check
- No audit of whether "future cleanup" actually happened

**Gap 5**: Ambiguous Zero Test Debt Policy Interpretation
- Policy states "Zero Test Debt" but allows "documented execution debt"
- RED tests classified as "not debt" because they're "intentional"
- Warnings classified as "not test debt" because tests pass
- **Policy loophole**: Debt is acceptable if documented and justified

---

### RCA Question 3: What Risk Factors Led to Accumulation?

**Risk Factor 1**: Separation of "Test Status" from "Warning Status"
- Tests PASSING = merge approved
- Warnings present but categorized separately
- Warnings not treated with same severity as test failures

**Risk Factor 2**: TDD Approach Misapplied
- TDD should be: Write RED test → Implement → Test GREEN → Merge
- Actual pattern: Write 65 RED tests → Move to RED_QA/ → Merge without implementation
- RED tests became "future work" instead of immediate implementation requirement

**Risk Factor 3**: Optimistic Debt Assessment
- "LOW to MEDIUM risk" assessment allowed approval
- "Future-breakage risk is manageable" rationalization
- No quantitative risk threshold defined

**Risk Factor 4**: Bootstrap Execution Pressure
- Wave 1.0 was first full build wave
- Pressure to demonstrate progress and velocity
- Debt acceptance rationalized as "necessary for forward progress"

**Risk Factor 5**: No Governance Ratchet After First Debt Acceptance
- First debt (Wave 1.0.1 warnings) set precedent
- No governance update to prevent recurrence
- Pattern allowed to repeat (Wave 0 RED tests)

---

### RCA Question 4: Why Wasn't Debt Eliminated in Subsequent Waves?

**Answer**: No Forcing Function

**Observations**:
1. **Wave 1.0.2 through 1.0.5**: Focused on their own QA ranges
   - No instruction to address Wave 1.0.1 warnings
   - No instruction to implement Wave 0 RED tests
   - Each wave treated as isolated work unit

2. **Wave 2.0 Planning**: No evidence of debt elimination in Wave 2 scope
   - No "WAVE_2_WARNING_CLEANUP_PLAN.md" document found
   - No builder assigned to warning remediation
   - No RED test implementation scheduled

3. **No Gate Blocking Subsequent Work**: Debt in Wave 1.0.1 did not block Wave 1.0.2+
   - Subsequent waves proceeded without debt elimination requirement
   - Debt accumulated without forcing resolution

4. **Memory Loss**: Debt promised in "future wave" but not tracked
   - No persistent debt register
   - No automated reminder
   - No escalation after N waves without resolution

---

## Part 3: Impact Assessment

### Current Debt State

**Active Test Suite**:
- Tests running in CI: 33 tests (from wave0_minimum_red/)
- Pass rate: 100% (33/33 GREEN)
- Test debt: ZERO (per active suite definition)

**Excluded from CI**:
- RED_QA tests: 65 tests (100% RED, intentionally excluded)
- Reason: Awaiting implementation
- Status: Documented as "future work"

**Warnings**:
- Wave 1.0.1 warnings: 194 warnings (documented, not eliminated)
- Wave 1.0.4 warning: 1 warning (observed but not classified)
- Status: Persists in codebase, not eliminated

---

### Risk Impact

**Immediate Risks**: LOW
- Active test suite is 100% GREEN
- Application functionality not impaired
- Debt is documented and visible

**Medium-Term Risks**: MEDIUM
- Warnings may proliferate in future waves
- Deprecation warnings may become errors in dependency upgrades
- RED tests represent unimplemented functionality (technical debt)
- "Future cleanup" pattern may repeat

**Long-Term Risks**: HIGH
- Debt normalization: "Documented debt is acceptable" becomes cultural norm
- Policy erosion: Zero Test Debt policy weakened by "exception" pattern
- Governance failure: Promises without enforcement lead to broken trust
- Build quality degradation: Warnings ignored, RED tests never implemented

---

### Governance Policy Compliance

**Zero Test Debt Constitutional Rule (T0-003)**: ⚠️ **PARTIAL VIOLATION**

**Policy Statement**:
> "No skipped, commented, incomplete, or placeholder tests. All tests must be complete and executable."

**Current Status**:
- ✅ No skipped tests in active suite
- ✅ No commented-out tests
- ✅ No incomplete tests in active suite
- ⚠️ **65 RED tests excluded from CI (not skipped but not executed)**
- ⚠️ **194 warnings accepted as "temporary debt"**

**Interpretation Question**: Are excluded RED tests a violation?
- Argument FOR violation: Tests exist but don't run = equivalent to skipped
- Argument AGAINST violation: Tests properly classified as TDD RED, awaiting implementation
- **FM Assessment**: VIOLATION - Tests should be implemented before merge, not deferred

---

## Part 4: Elimination Strategy

### Principle: Zero Tolerance for Accumulated Debt

**New Rule**: ALL historical debt MUST be eliminated before new waves authorized.

**Rationale**:
1. Debt accumulation pattern must be broken
2. "Future cleanup" promises must be fulfilled
3. Zero Test Debt policy must be restored to absolute
4. Governance credibility depends on enforcement

---

### Debt Item 1 Elimination Plan: 194 Warnings

**Strategy**: Systematic warning classification and remediation

**Phase 1: Re-Verification** (Immediate)
- Run Wave 1.0.1 tests again to verify warnings still present
- Capture actual warning messages (not estimates)
- Confirm warning categories and counts

**Phase 2: Warning-by-Warning Analysis** (1-2 days)
- Create spreadsheet: Warning Text | File | Line | Category | Remediation
- For each warning:
  - Is it still present? (dependency updates may have resolved)
  - What's the fix? (code change, config change, suppression)
  - What's the risk of fixing? (breakage potential)
  - What's the priority? (critical deprecations first)

**Phase 3: Remediation Execution** (2-5 days)
- Assign schema-builder to address warnings (original responsible agent)
- Create sub-issue: "Wave 1.0.1 Warning Elimination"
- Define acceptance criteria: ZERO warnings in schema foundation tests
- Execute fixes, validate, merge

**Phase 4: Verification** (Immediate after fix)
- Run full test suite
- Confirm ZERO warnings in Wave 1.0.1 test range
- Update incident status to RESOLVED

**Responsible Agent**: schema-builder (original owner of Wave 1.0.1)  
**FM Oversight**: Mandatory gate check before approval

---

### Debt Item 2 Elimination Plan: 65 RED Tests

**Strategy**: Implement or Remove - No Middle Ground

**Phase 1: Decision per Test Category** (Immediate)
- For each of 5 RED test categories, decide:
  - **IMPLEMENT**: Core functionality, required for platform
  - **DEFER**: Nice-to-have, Wave 3.0+ scope
  - **REMOVE**: Speculative, not needed

**Phase 2: Implementation Plan** (If IMPLEMENT chosen)
- Assign builder per category:
  - Decision Determinism → api-builder or integration-builder
  - Evidence Integrity → integration-builder
  - Evidence Schema Validation → qa-builder
  - Governance Supremacy → integration-builder
  - Liveness Continuity → integration-builder
- Create sub-issues for each category
- Define architecture for missing components
- Execute Build-to-Green for each

**Phase 3: Deferral Plan** (If DEFER chosen)
- Move tests to `tests/future/` directory (separate from RED_QA/)
- Document in `FUTURE_FUNCTIONALITY.md`
- Remove from RED_QA/ to avoid confusion
- Create placeholder issues for Wave 3.0+

**Phase 4: Removal Plan** (If REMOVE chosen)
- Delete test files
- Document removal rationale
- Update test count baselines

**FM Recommendation**: 
- IMPLEMENT: Evidence Integrity (critical for audit)
- DEFER: Decision Determinism, Governance Supremacy (Wave 3.0+)
- REMOVE: Evidence Schema Validation (overlaps with Evidence Integrity), Liveness Continuity (monitoring not core)

**Responsible Agents**: TBD based on IMPLEMENT/DEFER/REMOVE decisions  
**FM Oversight**: Mandatory architecture freeze and QA-to-Red before implementation

---

### Minor Debt Item: Wave 1.0.4 Single Warning

**Strategy**: Quick investigation and resolution

**Action**:
- Identify warning source (test output analysis)
- Classify per Wave 1.0.1 categories
- Remediate immediately or document as acceptable
- Update Wave 1.0.4 merge approval with classification

**Responsible Agent**: api-builder  
**Timeline**: 1 day

---

## Part 5: Governance Hardening

### New Governance Rule: No Merge with Unresolved Warnings

**Rule Specification**: `governance/specs/ZERO_WARNING_MERGE_GATE_SPEC.md` (to be created)

**Rule Content**:
1. **Gate Check**: CI must report ZERO warnings (not just ZERO failures)
2. **Warning Classification Required**: Any warning must be classified before merge
3. **Acceptable Warning Categories**: None (all warnings must be resolved)
4. **Exception Process**: Johan approval required for any warning acceptance
5. **Follow-Up Plan Required**: If warning accepted, elimination plan with owner and timeline MUST be created
6. **Debt Register**: All accepted warnings tracked in `governance/incidents/WARNING_DEBT_REGISTER.md`
7. **Escalation**: 2+ warnings in same category across waves = automatic HALT

---

### New Governance Rule: TDD RED Tests Must Be Implemented Before Merge

**Rule Specification**: `governance/specs/TDD_RED_TO_GREEN_MERGE_REQUIREMENT_SPEC.md` (to be created)

**Rule Content**:
1. **TDD Process**: Write RED test → Implement → Test GREEN → Merge (all in same PR)
2. **No RED Test Merges**: RED tests not allowed in merged code (except explicit DP-RED registry)
3. **DP-RED Exception**: Only tests in DP-RED registry can be RED at merge time
4. **DP-RED Requirement**: DP-RED entry MUST include implementation issue/wave assignment
5. **DP-RED Audit**: Monthly audit of DP-RED registry, escalate any item >60 days old

---

### New Governance Rule: Debt Elimination Forcing Function

**Rule Specification**: `governance/specs/DEBT_ELIMINATION_GATE_SPEC.md` (to be created)

**Rule Content**:
1. **Debt Register**: All technical debt tracked in `governance/incidents/DEBT_REGISTER.md`
2. **Wave Authorization Block**: No new wave authorized while unresolved debt exists
3. **Debt Age Limit**: Debt >30 days triggers mandatory elimination before new work
4. **Debt Owner Assignment**: Every debt item MUST have assigned owner and deadline
5. **Escalation**: Debt deadline missed = HALT all work, escalate to Johan

---

## Part 6: Prevention of Recurrence

### What Must Change

**1. Gate Enforcement Strictness**
- Zero warnings policy enforced at CI level
- No "acceptable temporary debt" exceptions
- Any exception requires Johan approval + elimination plan

**2. TDD Discipline**
- RED tests written and implemented in same wave
- No deferral of implementation to "future wave"
- DP-RED registry for intentional RED tests with strict governance

**3. Debt Visibility**
- Persistent debt register
- Monthly debt audit
- Debt age escalation

**4. Forcing Functions**
- New wave authorization blocked by unresolved debt
- Debt deadline enforcement with HALT
- Builder accountability for debt elimination

**5. Governance Ratchets**
- New specs created (3 specs above)
- BL/FL entries created for warning/debt acceptance pattern
- Second occurrence of pattern invokes TARP

---

## Part 7: Learnings for Future Discipline

### Lesson 1: "Future Cleanup" is Broken Promise Pattern

**What Happened**: Debt accepted with promise of "future cleanup" but no concrete plan

**Why It Failed**: No forcing function, no accountability, no verification

**What Must Change**: All debt requires elimination plan WITH owner, deadline, and gate block

---

### Lesson 2: "Documented Debt" is Not Zero Debt

**What Happened**: Warnings/RED tests documented and accepted as "visible debt"

**Why It Failed**: Documentation without elimination is acknowledgment without action

**What Must Change**: Zero Debt means ZERO - no exceptions, no documentation workaround

---

### Lesson 3: Optimization Pressure Erodes Standards

**What Happened**: Wave 1.0 pressure led to debt acceptance to show progress

**Why It Failed**: Short-term velocity prioritized over long-term quality

**What Must Change**: Build Philosophy supremacy - correctness always wins over speed

---

### Lesson 4: First Exception Sets Precedent

**What Happened**: Wave 1.0.1 warnings acceptance set pattern for future debt

**Why It Failed**: No governance ratchet created after first exception

**What Must Change**: Every exception MUST trigger governance hardening to prevent recurrence

---

### Lesson 5: TDD Without Discipline is Speculation

**What Happened**: 65 RED tests written without implementation commitment

**Why It Failed**: Tests became "future work" instead of immediate implementation requirement

**What Must Change**: RED tests only in same-wave implementation or explicit DP-RED with plan

---

## Part 8: Recommended Actions (Immediate)

### Action 1: HALT All New Wave Work

**Rationale**: Debt elimination takes precedence over new functionality

**Duration**: Until all historical debt eliminated and verified

**Communication**: Update all stakeholders on HALT reason and debt elimination priority

---

### Action 2: Execute Debt Elimination (Sequentially)

**Week 1**: 
- Minor debt (Wave 1.0.4 single warning)
- Re-verify Wave 1.0.1 warnings (current state)

**Week 2**:
- Implement decision for 65 RED tests (IMPLEMENT/DEFER/REMOVE)
- Begin Wave 1.0.1 warning remediation (if IMPLEMENT chosen)

**Week 3**:
- Complete Wave 1.0.1 warning elimination
- Complete RED test implementation or removal

**Week 4**:
- Verification and evidence generation
- Governance hardening (create 3 new specs)

---

### Action 3: Create Governance Ratchets

**Spec 1**: `governance/specs/ZERO_WARNING_MERGE_GATE_SPEC.md`  
**Spec 2**: `governance/specs/TDD_RED_TO_GREEN_MERGE_REQUIREMENT_SPEC.md`  
**Spec 3**: `governance/specs/DEBT_ELIMINATION_GATE_SPEC.md`

**Rationale**: Make third-time occurrence impossible

---

### Action 4: Register This Pattern as BL/FL

**Entry**: BL-021 or FL-021 (next available)  
**Title**: "Warning/Test Debt Acceptance with 'Future Cleanup' Promise Pattern"  
**Classification**: First-time failure (this RCA represents discovery and correction)  
**Prevention**: 3 governance specs above + forward scan

---

### Action 5: Update INCIDENT-20251222-TEST-DEBT

**Status**: Link to this comprehensive RCA  
**Resolution Plan**: Reference debt elimination strategy above  
**Timeline**: 4-week elimination window

---

## Part 9: Success Criteria

### Definition of "Debt-Free State"

**Criteria**:
1. ✅ Active test suite: 100% GREEN (maintained)
2. ✅ Wave 1.0.1 warnings: ZERO (currently 194)
3. ✅ Wave 1.0.4 warning: Classified and resolved (currently 1)
4. ✅ RED_QA tests: Implemented OR removed (currently 65 RED)
5. ✅ Debt register: Empty (no tracked debt items)
6. ✅ Governance specs: 3 new prevention specs created
7. ✅ BL/FL entry: Pattern registered and prevented

---

## Part 10: Evidence and Traceability

**Source Documents**:
- `WAVE_1.0.1_WARNING_CLASSIFICATION_AND_GATE_DECISION.md` (194 warnings)
- `INCIDENT-20251222-TEST-DEBT.md` (65 RED tests)
- `TEST_DEBT_ANALYSIS.md` (historical analysis)
- All Wave 1.0 merge approval documents
- All Wave 1.0 completion summaries

**Artifacts Created**:
- This RCA document
- Debt elimination plan (above)
- Governance hardening plan (above)
- Prevention specifications (to be created)

**Verification**:
- To be performed after elimination execution
- Evidence pack to be generated
- Status update to governance dashboard

---

## Conclusion

**Summary**: 2 major debt items (194 warnings + 65 RED tests) accumulated due to "future cleanup" promise pattern without forcing function. Debt documented but not eliminated. Zero Test Debt policy effectively violated.

**Root Cause**: Process gaps (no debt elimination plan requirement, no max debt threshold, no ownership assignment, no verification, policy interpretation ambiguity) + risk factors (separation of test/warning status, TDD misapplication, optimistic assessment, bootstrap pressure, no ratchet after first exception).

**Elimination Strategy**: Systematic remediation of warnings (schema-builder assigned), implement/defer/remove decision for RED tests, strict governance hardening with 3 new specs, pattern registration as BL/FL for prevention.

**Governance Impact**: Zero Test Debt policy must be restored to absolute. No exceptions, no "documented debt" workaround. Debt forcing function required. Governance credibility depends on enforcement.

**Timeline**: 4 weeks for complete elimination and hardening.

**Status**: Survey complete, RCA complete, elimination plan defined, awaiting authorization to execute.

---

**Prepared By**: FM Agent  
**Date**: 2026-01-07  
**Authority**: FM Agent Contract v3.4.0  
**Classification**: Critical Governance Incident  
**Action Required**: Johan authorization for HALT and debt elimination execution

---

**END OF HISTORICAL WAVE PR WARNING AND TEST DEBT SURVEY WITH ROOT CAUSE ANALYSIS**
