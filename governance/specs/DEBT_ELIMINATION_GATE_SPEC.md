# Debt Elimination Gate Specification

**Spec ID**: DEBT-ELIMINATION-GATE-SPEC  
**Version**: 1.0.0  
**Status**: PROPOSED  
**Date**: 2026-01-07  
**Authority**: FM Agent Contract v3.4.0, BL-021 Prevention  
**Purpose**: Prevent new work authorization while unresolved technical debt exists

---

## Executive Summary

This specification establishes a "Debt Elimination Gate" that blocks authorization of new waves, subwaves, or significant work items when unresolved technical debt exists. Debt MUST be eliminated before new work begins.

**Key Principle**: Fix old problems before creating new ones. Debt elimination takes precedence over new functionality.

---

## Scope

**Applies To**:
- Wave/subwave authorization
- New feature development
- Architecture expansions
- Significant refactoring work

**Does NOT Apply To**:
- Debt elimination work itself (not blocked by debt)
- Critical hotfixes (security, data loss, system down)
- Governance hardening (improvements to prevent debt)

---

## Technical Debt Definition

### What is Technical Debt?

Technical debt is any code, test, or configuration issue that:
1. Is known and documented
2. Requires remediation
3. Has potential future negative impact
4. Is not immediately critical but cannot be ignored indefinitely

### Debt Categories

**Category 1: Test Debt**
- RED tests in active suite (failing tests)
- Skipped tests (`.skip()` decorator)
- Commented-out tests
- Incomplete test stubs
- Tests with `# TODO` or `# FIXME`
- Tests excluded from CI without valid DP-RED entry

**Category 2: Warning Debt**
- Deprecation warnings in test output
- Linting warnings
- Type checking warnings
- Framework compatibility warnings
- Security warnings (non-critical)

**Category 3: Code Debt**
- `TODO` or `FIXME` comments in production code
- Temporary workarounds or hacks
- Disabled linting rules (e.g., `# pylint: disable`)
- Dead code or unused imports
- Commented-out code blocks

**Category 4: Architecture Debt**
- Incomplete architecture sections (marked "TBD")
- Architecture-code misalignment
- Missing architectural components
- Temporary architecture decisions marked for review

**Category 5: Documentation Debt**
- Incomplete API documentation
- Outdated documentation (mismatches code)
- Missing architecture documentation
- Placeholder content in critical docs

---

## Debt Register

### Debt Tracking Mechanism

**File**: `governance/incidents/DEBT_REGISTER.md`

**Purpose**: Centralized tracking of all technical debt items

**Entry Requirements**:
Every debt item MUST have:
- **Debt ID**: Unique identifier (DEBT-<number>)
- **Type**: Category (Test, Warning, Code, Architecture, Documentation)
- **Severity**: Impact level (LOW, MEDIUM, HIGH, CRITICAL)
- **Debt Size**: Quantification (number of warnings, test count, LOC, etc.)
- **Origin**: Where/when debt was introduced (PR, wave, builder)
- **Owner**: Individual/team responsible for elimination
- **Deadline**: Date by which debt must be eliminated
- **Status**: Current state (UNRESOLVED, IN_PROGRESS, RESOLVED)
- **Elimination Plan**: Concrete steps to eliminate debt

---

## Debt Elimination Gate

### Gate Rule 1: No New Wave Authorization with Unresolved Debt

**Rule**: FM MUST NOT authorize new wave/subwave while debt register contains unresolved items.

**Enforcement**:
- Before wave/subwave authorization, FM checks debt register
- If unresolved debt exists (status = UNRESOLVED), authorization BLOCKED
- FM communicates block to Johan with debt summary
- Wave/subwave authorization requires debt elimination first

**Exception**: Johan may override block with explicit authorization and elevated monitoring

### Gate Rule 2: Debt Age Limit

**Rule**: Debt >30 days old triggers mandatory elimination before new work.

**Enforcement**:
- Monthly debt register audit
- Any debt item with age >30 days flagged for escalation
- FM notifies debt owner and Johan
- New work blocked until debt eliminated or deadline extended by Johan

**Rationale**: Debt should not accumulate indefinitely. 30 days is sufficient for most debt elimination.

### Gate Rule 3: Debt Ownership Requirement

**Rule**: Every debt item MUST have assigned owner.

**Enforcement**:
- Debt entry cannot be created without owner field
- Owner is accountable for elimination
- Owner provides weekly status updates (for debt >14 days old)
- Owner cannot reassign without Johan approval

**Accountability**:
- Builder who introduced debt = default owner
- Builder may request reassignment if debt is external or out of scope
- FM arbitrates reassignment disputes
- Johan has final authority on ownership

### Gate Rule 4: Debt Deadline Enforcement

**Rule**: Debt deadline missed triggers automatic HALT.

**Enforcement**:
- Daily debt register check for overdue items
- If deadline passed and status ≠ RESOLVED:
  - HALT all new work (no new PRs, no new waves)
  - Escalate to Johan immediately
  - Debt owner required to provide updated elimination plan
  - Work resumption requires Johan authorization

**Rationale**: Deadlines without consequences are meaningless. Missed deadline = broken commitment = stop and fix.

---

## Debt Registration Process

### When to Register Debt

**Immediate Registration Required**:
- Any warning at merge time (if exception granted by Johan)
- Any RED test merged with DP-RED entry
- Any `TODO`/`FIXME` in production code at merge
- Any known architecture gap at wave completion
- Any incomplete documentation at handover

**Process**:
1. Identify debt (discovery during build, review, or audit)
2. Classify debt (category, severity, size)
3. Determine owner (builder, team, or escalate to FM/Johan)
4. Set deadline (based on severity and complexity)
5. Create elimination plan (concrete steps, not "future work")
6. Register in debt register (add entry with all fields)
7. Track status (weekly updates for debt >14 days)

### Registration Authority

**Who Can Register Debt**:
- FM Agent (primary)
- Johan (ultimate authority)
- Builders (may propose debt registration during PR, FM approves)

**Who Cannot Register Debt**:
- Builders cannot register debt without FM approval (prevents self-authorization of debt)

---

## Debt Elimination Priority

### Severity-Based Priority

**CRITICAL** (Eliminate within 7 days):
- Security warnings
- Data loss risk
- System instability
- Blocking other work

**HIGH** (Eliminate within 14 days):
- Failing tests (RED)
- Deprecation warnings (near-term breakage)
- Architecture gaps (blocking future waves)

**MEDIUM** (Eliminate within 30 days):
- Non-critical warnings
- Code debt (TODO/FIXME)
- Documentation gaps

**LOW** (Eliminate within 60 days):
- Minor linting issues
- Stylistic improvements
- Nice-to-have documentation

### Debt Elimination Order

**Priority Order**:
1. CRITICAL debt (oldest first)
2. HIGH debt (oldest first)
3. MEDIUM debt (oldest first)
4. LOW debt (oldest first)

**Rationale**: Age + severity determines priority. Old debt compounds, fresh debt can wait (within reason).

---

## Debt Prevention

### Pre-Merge Checks

**PR Author Responsibilities**:
- [ ] No warnings in test output
- [ ] No RED tests (or DP-RED entry exists)
- [ ] No `TODO`/`FIXME` in production code (or debt registered)
- [ ] No commented-out code
- [ ] All architecture complete (or gaps documented)
- [ ] All documentation complete (or debt registered)

**FM Gate Checks**:
- [ ] Zero warning gate (per ZERO_WARNING_MERGE_GATE_SPEC)
- [ ] All tests GREEN gate (per TDD_RED_TO_GREEN_MERGE_REQUIREMENT_SPEC)
- [ ] Code quality check (no TODOs, FIXMEs, commented code)
- [ ] Architecture completeness check
- [ ] Documentation completeness check

### Builder Accountability

**Debt Introduced by Builder**:
- Builder is default owner
- Builder must eliminate within deadline
- Builder cannot approve own debt registration (FM approves)
- Builder performance tracked (debt introduction frequency)

**Repeated Debt Introduction**:
- If builder introduces debt 3+ times in 60 days:
  - FM escalates to Johan for pattern review
  - Builder may receive additional training or coaching
  - Builder may be restricted from certain work types

---

## Debt Audit

### Monthly Audit Process

**Audit Checklist**:
- [ ] Review all debt register entries
- [ ] Verify status accuracy (UNRESOLVED vs IN_PROGRESS vs RESOLVED)
- [ ] Check ages (flag any >30 days)
- [ ] Check deadlines (flag any overdue)
- [ ] Verify owner assignments (all debt has owner)
- [ ] Verify elimination plans (all concrete, not "TBD")
- [ ] Remove RESOLVED entries (archive in "Resolved" section)

**Audit Report**:
- Total debt count (by category)
- Average debt age
- Oldest debt item
- Overdue debt count
- Debt trend (increasing/decreasing/stable)

**Audit Date**: First day of each month

**Audit Authority**: FM Agent

### Escalation Triggers

**Automatic Escalation to Johan**:
- Any debt >60 days old
- Any debt with missed deadline
- Debt register size >10 items
- Debt trend increasing for 2+ months
- Critical debt not eliminated within 7 days

---

## Dashboard and Visibility

### Debt Register Dashboard (To Be Created)

**Metrics Displayed**:
- Total active debt count
- Debt by category (pie chart)
- Debt by severity (bar chart)
- Debt age distribution (histogram)
- Overdue debt count (red alert)
- Debt trend (line chart over time)

**Location**: `governance/dashboards/debt-register-dashboard.md`

**Update Frequency**: Real-time (updated on debt registration/resolution)

---

## Failure Modes

### Failure Mode 1: "Future Cleanup" Promise Without Deadline

**Pattern**: Debt documented, owner assigned, but deadline = "TBD" or "next wave"

**Prevention**: This spec (deadline required, no TBD allowed)

**Detection**: Debt entry with deadline = "TBD" or vague future reference

**Response**: FM rejects debt entry, requires concrete deadline

### Failure Mode 2: Debt Accumulation Without Elimination

**Pattern**: Debt registered, deadlines set, but never eliminated, new debt keeps adding

**Prevention**: Debt age limit (30 days) + HALT on missed deadline

**Detection**: Debt register size increasing, average age increasing

**Response**: HALT new work, focus on debt elimination

### Failure Mode 3: Debt Registry Gaming

**Pattern**: Debt "resolved" in register but not actually eliminated (marking RESOLVED without fixing)

**Prevention**: Verification requirement (FM must verify RESOLVED status)

**Detection**: Spot checks, audit cross-reference

**Response**: Re-open debt entry, extend deadline, accountability action against owner

---

## Success Criteria

**Debt-Free State**:
- Debt register: 0-3 items (minimal, temporary, with active elimination)
- Average debt age: <14 days
- Overdue debt: 0
- Debt trend: stable or decreasing
- New wave authorization: not blocked by debt

**Debt Discipline**:
- Debt registration: all debt tracked, no hidden debt
- Debt elimination: deadlines met consistently
- Debt prevention: pre-merge checks effective, debt introduction rare
- Debt visibility: dashboard current, team aware of debt status

---

## Rollout Plan

### Phase 1: Debt Register Activation (Week 1)
- ✅ Create `governance/incidents/DEBT_REGISTER.md` (already exists)
- ✅ Register existing debt (DEBT-001, DEBT-002, DEBT-003 already registered)
- [ ] Communicate debt register to all builders
- [ ] Train builders on debt registration process

### Phase 2: Gate Activation (Week 2)
- [ ] Activate Debt Elimination Gate (FM enforces no new wave with debt)
- [ ] Communicate gate rule to Johan and builders
- [ ] Begin monthly audit cycle

### Phase 3: Debt Elimination (Week 3-4)
- [ ] Execute elimination of existing debt (per DEBT-001, DEBT-002, DEBT-003 plans)
- [ ] Verify RESOLVED status
- [ ] Achieve debt-free baseline (0-3 items)

### Phase 4: Ongoing Enforcement (Continuous)
- [ ] FM enforces gate on every wave authorization
- [ ] Monthly audits conducted
- [ ] Dashboard updated
- [ ] Escalations handled

---

## Related Documents

- `governance/incidents/DEBT_REGISTER.md` (active debt tracking)
- `governance/incidents/HISTORICAL_WAVE_PR_WARNING_TEST_DEBT_SURVEY_RCA.md` (pattern RCA)
- `governance/specs/ZERO_WARNING_MERGE_GATE_SPEC.md` (warning debt prevention)
- `governance/specs/TDD_RED_TO_GREEN_MERGE_REQUIREMENT_SPEC.md` (test debt prevention)
- `governance/policies/zero-test-debt-constitutional-rule.md` (T0-003)

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-07 | FM Agent | Initial specification |

---

**Status**: PROPOSED - Awaiting Johan approval  
**Authority**: FM Agent Contract v3.4.0  
**Purpose**: Prevent debt accumulation, enforce debt elimination discipline

---

**END OF DEBT ELIMINATION GATE SPECIFICATION**
