# TDD RED-to-GREEN Merge Requirement Specification

**Spec ID**: TDD-RED-TO-GREEN-MERGE-SPEC  
**Version**: 1.0.0  
**Status**: PROPOSED  
**Date**: 2026-01-07  
**Authority**: FM Agent Contract v3.4.0, BL-021 Prevention, Build-to-Green Enforcement (T0-011)  
**Purpose**: Enforce proper TDD discipline - RED tests must be implemented before merge

---

## Executive Summary

This specification enforces the correct Test-Driven Development (TDD) process: Write RED test → Implement → Test GREEN → Merge. RED tests at merge time are PROHIBITED except for tests explicitly registered in DP-RED registry with concrete implementation plans.

**Key Principle**: TDD is "Red-Green-Refactor" in a SINGLE iteration, not "Red now, Green someday".

---

## Scope

**Applies To**:
- All test code (unit, integration, E2E)
- All PR merge gates (Wave, Subwave, Governance, Hotfix)
- All builders (ui, api, schema, integration, qa)

**Does NOT Apply To**:
- DP-RED registry tests (explicitly deferred, see below)
- Tests in `tests/examples/` or `tests/prototypes/` (never run in CI)
- Development branches (pre-PR)

---

## TDD Process Requirement

### Correct TDD Process

**TDD Cycle (Single PR)**:
1. **RED**: Write failing test (captures requirement)
2. **GREEN**: Implement minimum code to make test pass
3. **REFACTOR**: Improve code while keeping test green
4. **MERGE**: Merge PR with ALL tests GREEN

**Timeline**: All steps within SAME PR/wave. No deferral between steps.

**Verification**:
- Test added in PR commit 1: FAILING (RED)
- Implementation added in PR commit 2+: Test now PASSING (GREEN)
- PR merge: Test GREEN, implementation complete

### Prohibited Pattern

**"Write RED tests, implement later" pattern**:
1. ~~Write 65 RED tests~~
2. ~~Move to RED_QA/ directory~~
3. ~~Exclude from CI~~
4. ~~Merge without implementation~~
5. ~~Promise "future implementation"~~

**Status**: PROHIBITED (BL-021 pattern)

---

## Merge Gate Rule: All Tests GREEN

### Primary Rule

**ALL tests in CI MUST be GREEN for PR to be eligible for merge.**

**PASS Criteria**:
```
Test Count: N/N passing (100%)
RED tests: 0
GREEN tests: N
Skipped: 0
Excluded: 0 (except DP-RED registry tests)
```

**FAIL Criteria**:
```
RED tests: >0 (ANY failing tests = GATE BLOCKED)
```

### Verification

**CI Check**:
- Run full test suite (pytest, jest, etc.)
- Count RED tests (failing)
- Gate BLOCKED if RED count >0

**PR Status**:
- "All Tests GREEN" check = PASS only if 0 RED tests
- Merge button disabled if RED tests present

---

## DP-RED Registry Exception

### Purpose

DP-RED (Deferred Pending RED) registry is the ONLY mechanism for intentionally RED tests at merge time.

**Use Cases**:
1. **Architecture Definition**: Tests define intended architecture before implementation wave scheduled
2. **Cross-Wave Dependencies**: Test depends on another wave's implementation (dependency blocking)
3. **Explicit Deferral**: Test represents future functionality with documented business decision to defer

**NOT Valid Use Cases**:
- "Don't have time to implement now"
- "Implementation is hard"
- "TDD exploration"

### DP-RED Entry Requirements

Every DP-RED test MUST have registry entry with ALL of the following:

**Mandatory Fields**:
```
DP-RED-<number>:
  Test File: <path to test file>
  Test Function(s): <list of test functions>
  QA Range: <QA IDs covered by test>
  Reason: <why RED at merge time - must be valid use case>
  Implementation Plan:
    Wave: <wave number or TBD>
    Builder: <assigned builder or TBD>
    Architecture: <architecture doc reference or "TBD - Wave X.Y planning">
    QA-to-Red: <QA-to-Red spec reference or "TBD - Wave X.Y planning">
  Deadline: <date or "Wave X.Y completion">
  Registered By: <FM Agent or Johan>
  Registered Date: <date>
  Status: <PENDING|IN_PROGRESS|RESOLVED>
```

**Validation**:
- Entry MUST exist before merge
- All mandatory fields MUST be populated (no "TBD" except for wave planning scenarios)
- Reason MUST match valid use case
- Implementation plan MUST be concrete (wave assigned, not just "future")

### DP-RED Audit

**Monthly Audit**:
- Review all DP-RED entries
- Check status (PENDING vs IN_PROGRESS vs RESOLVED)
- Escalate any entry >60 days old with no progress
- Remove RESOLVED entries (tests now GREEN)

**Escalation Triggers**:
- DP-RED entry >90 days old = automatic escalation to Johan
- DP-RED entry with missed deadline = escalation to FM
- DP-RED entry proliferation (>10 active entries) = HALT and review

---

## Implementation Requirements

### Builder Responsibility

**Before PR Submission**:
- [ ] All tests written MUST have implementation in same PR
- [ ] Verify all tests GREEN locally
- [ ] If test must be RED at merge, create DP-RED registry entry FIRST
- [ ] Include DP-RED entry in PR description

**PR Description Requirements**:
- List all tests added (file:function)
- Confirm all tests GREEN OR list DP-RED entries
- No RED tests without DP-RED registration

### FM Gate Enforcement

**FM Checks**:
- [ ] Run full test suite, verify 0 RED tests (excluding DP-RED)
- [ ] For any DP-RED tests, verify registry entry exists and is valid
- [ ] Verify DP-RED entry has concrete implementation plan
- [ ] Reject PR if RED tests without DP-RED entry
- [ ] Reject PR if DP-RED entry incomplete or invalid

**FM Does NOT**:
- Approve RED tests without DP-RED entry
- Approve DP-RED entry without implementation plan
- Create DP-RED entries on behalf of builders (builder responsibility)

---

## DP-RED Registry Location

**File**: `governance/qa/DP_RED_REGISTRY.md`

**Structure**:
```markdown
# DP-RED Registry

## Active DP-RED Entries

### DP-RED-001: <Test Category>
[Full entry as per template above]

### DP-RED-002: <Test Category>
[Full entry as per template above]

## Resolved DP-RED Entries

### DP-RED-XXX: <Test Category> (Resolved YYYY-MM-DD)
[Archived entry]
```

**Access Control**:
- FM Agent: Read + Write (create, update, resolve entries)
- Builders: Read only (reference for DP-RED tests)
- Johan: Read + Write + Delete (ultimate authority)

---

## Prohibited Actions

**Builders MUST NOT**:
- Submit PR with RED tests and no DP-RED entry
- Create incomplete DP-RED entry ("TBD" in required fields)
- Move RED tests to excluded directory (e.g., RED_QA/) to bypass gate
- Rationalize RED tests as "TDD exploration" or "future work" without DP-RED entry

**FM MUST NOT**:
- Approve PR with RED tests (regardless of rationalization)
- Create DP-RED entry without builder's explicit request and justification
- Accept "future implementation" promise without DP-RED entry
- Bypass DP-RED requirement for any builder

---

## Failure Mode: "Write RED Tests, Implement Later" Pattern

**Pattern Description**: Developer writes numerous RED tests, moves them to excluded directory or special category, merges without implementation, promises "future work", never implements.

**Pattern ID**: BL-021 (registered)

**Historical Example**: 65 RED tests moved to RED_QA/, excluded from CI, no implementation scheduled

**Prevention**: This specification

**Detection**:
- RED test count >0 at merge (excluding valid DP-RED)
- RED tests in excluded directory without DP-RED entry
- DP-RED entries without concrete implementation plan

**Response**:
- GATE BLOCKED
- RED tests must be implemented OR registered in DP-RED with valid plan
- No merge until 100% GREEN (or valid DP-RED)

---

## Migration Plan for Existing RED Tests

### Current State

**65 RED tests in RED_QA/** (as of 2026-01-07):
- Decision Determinism (8 tests)
- Evidence Integrity (20 tests)
- Evidence Schema Validation (12 tests)
- Governance Supremacy (16 tests)
- Liveness Continuity (9 tests)

### Required Action

**Option 1: IMPLEMENT** (Preferred for critical functionality)
- Create DP-RED entry for each category
- Schedule implementation wave
- Assign builder
- Freeze architecture
- Execute Build-to-Green
- Move tests from RED_QA/ to active suite once GREEN

**Option 2: DEFER** (For non-critical future functionality)
- Create DP-RED entry for each category
- Document as Wave 3.0+ scope
- Keep tests in RED_QA/ with DP-RED reference
- Review in Wave 3.0 planning

**Option 3: REMOVE** (For speculative or overlapping tests)
- Delete test files
- Document removal rationale
- No DP-RED entry needed (tests no longer exist)

**Timeline**: Decision required by 2026-01-28 (per DEBT-002 deadline)

---

## Success Criteria

**TDD Discipline Achieved**:
- All PRs merged: 100% GREEN tests (or valid DP-RED)
- DP-RED registry: <10 active entries at any time
- DP-RED average age: <30 days
- Zero instances of RED tests merged without DP-RED entry

**TDD Culture Maintained**:
- Builders write tests and implementations in same PR
- DP-RED used only for valid exceptions (not workaround)
- FM enforces TDD discipline consistently
- RED_QA/ directory empty (all tests in active suite or DP-RED)

---

## Rationale

### Why Prohibit RED Tests at Merge?

1. **TDD Discipline**: TDD is not "write tests someday, implement someday" - it's a tight cycle
2. **Debt Prevention**: RED tests without implementation = technical debt accumulation
3. **False Coverage**: RED tests give illusion of coverage without actual validation
4. **Maintenance Burden**: RED tests must be maintained even though they don't validate anything
5. **Broken Promises**: "Future implementation" rarely happens without forcing function

### Why DP-RED Registry Required?

1. **Explicit Deferral**: Forces conscious decision and documentation
2. **Accountability**: Assigns owner and deadline
3. **Traceability**: Tracks all intentionally RED tests
4. **Audit Trail**: Enables monitoring and escalation
5. **Prevention**: High bar discourages casual deferral

### Why Not Just Allow "TDD Exploration"?

Because:
- Exploration without implementation = speculation
- Speculation in main branch = clutter
- Clutter becomes forgotten debt
- Debt accumulates and blocks future work

**Correct Approach**: Explore in prototype branch, implement when ready, merge when GREEN.

---

## Related Documents

- `governance/qa/DP_RED_REGISTRY.md` (to be created)
- `governance/incidents/HISTORICAL_WAVE_PR_WARNING_TEST_DEBT_SURVEY_RCA.md` (pattern RCA)
- `governance/incidents/INCIDENT-20251222-TEST-DEBT.md` (65 RED tests)
- `tests/wave0_minimum_red/RED_QA/README.md` (current RED tests)
- `governance/specs/BUILD_TO_GREEN_ENFORCEMENT_SPEC.md` (T0-011)
- `governance/specs/ZERO_WARNING_MERGE_GATE_SPEC.md` (related spec)

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-07 | FM Agent | Initial specification |

---

**Status**: PROPOSED - Awaiting Johan approval  
**Authority**: FM Agent Contract v3.4.0  
**Purpose**: Enforce TDD discipline, prevent RED test accumulation

---

**END OF TDD RED-TO-GREEN MERGE REQUIREMENT SPECIFICATION**
