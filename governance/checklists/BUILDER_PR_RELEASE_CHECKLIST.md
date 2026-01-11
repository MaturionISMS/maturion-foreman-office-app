# Builder PR Release Checklist

**Version**: 2.0.0+  
**Authority**: Execution Bootstrap Protocol + PR Gate Requirements Canon  
**Applies To**: All Builder Agents (UI, API, Schema, Integration, QA)  
**Status**: MANDATORY  
**Compliance Deadline**: 2026-02-11

---

## Purpose

This checklist defines exactly what must be satisfied for Builder PR gates to pass. All items marked MANDATORY must be complete before PR merge.

**Key Principle**: If all checklist items are satisfied, the PR gate **MUST** pass. No additional requirements permitted.

---

## Category 0: Execution Bootstrap Protocol (MANDATORY v2.0.0+)

**Applies To**: ALL PRs that create or modify execution artifacts (workflows, scripts, gates, configs)

- [ ] **Step 1: Execution Artifacts Identified**
  - All execution artifacts documented in PREHANDOVER_PROOF
  - Complete inventory with paths
  
- [ ] **Step 2: Local Execution Complete**
  - All artifacts executed locally in agent environment
  - Complete execution logs captured
  - Execution environment documented

- [ ] **Step 3: Exit Codes Validated**
  - All exit codes = 0 (success)
  - Zero warnings detected
  - Zero errors detected
  - Validation results documented

- [ ] **Step 4: Evidence Collected**
  - Execution logs attached/linked
  - Output files documented
  - Screenshots provided (if applicable)
  - All evidence accessible in PR

- [ ] **Step 5: Failure Remediation Complete**
  - Any detected failures fixed before handover
  - Re-execution after fixes shows GREEN
  - Remediation actions documented
  - OR: No failures detected on first execution

- [ ] **Step 6: Green Attestation Provided**
  - Agent attestation: "All checks GREEN on commit [hash]"
  - All checks listed with ✅ status
  - Commit hash specified for verification

- [ ] **Step 7: Handover Authorization**
  - PREHANDOVER_PROOF document created
  - Authorization statement: "Handover authorized, all checks green"
  - Evidence linked to proof document
  - Hard rule acknowledged: "CI is confirmation, NOT diagnostic"

**Template**: `.github/agent-templates/PREHANDOVER_PROOF_TEMPLATE.md`  
**Reference**: `governance/canon/EXECUTION_BOOTSTRAP_PROTOCOL_REFERENCE.md`

**CRITICAL**: If PR does not modify execution artifacts, Category 0 may be marked N/A. Otherwise, ALL 7 steps are MANDATORY.

---

## Category 1: Architecture Conformance (MANDATORY)

- [ ] **Frozen Architecture Followed**
  - Implementation matches frozen architecture specification exactly
  - No architectural decisions made during implementation
  - Architecture reference documented

- [ ] **Scope Boundaries Respected**
  - Only in-scope items modified
  - No out-of-scope changes included
  - Scope documented in PR description

- [ ] **Design Freeze Honored**
  - No design changes during build
  - Architecture frozen before build started
  - Design Freeze acknowledged

---

## Category 2: Test Execution (MANDATORY)

- [ ] **100% Tests Passing**
  - All tests GREEN (100% pass rate)
  - Zero test debt
  - Zero skipped tests
  - Zero ignored tests

- [ ] **Zero Warnings**
  - No warnings in test output
  - No warnings in build output
  - No warnings in linter output

- [ ] **QA-to-Red Validation**
  - Tests were RED before implementation
  - Tests are now GREEN after implementation
  - Evidence of RED → GREEN transition provided

- [ ] **Test Coverage Complete**
  - All new code covered by tests
  - Coverage metrics documented
  - No coverage gaps

---

## Category 3: Agent QA Boundaries (MANDATORY)

- [ ] **Builder QA Only**
  - Builder modified only Builder QA tests/code
  - No modifications to Governance QA
  - No modifications to FM QA
  - Agent boundary respected (T0-009 Constitutional)

- [ ] **No Cross-Boundary Violations**
  - Agent stayed within assigned scope
  - No work on other agents' responsibilities
  - Boundaries documented if clarification needed

---

## Category 4: Code Quality (MANDATORY)

- [ ] **Zero Test Debt**
  - No `.skip`, `.todo`, `.only` patterns
  - No test modifications to make tests pass
  - All tests genuinely passing
  - Zero Test Debt constitutional rule honored (T0-003)

- [ ] **Code Checking Complete**
  - Builder reviewed all generated code
  - Code correctness verified
  - Logic validated against architecture

- [ ] **Linting Passed**
  - All linters GREEN
  - No linting errors
  - No linting warnings

- [ ] **Deprecation Gate Passed**
  - No deprecated APIs used (BL-026)
  - Modern Python patterns used (if applicable)
  - `ruff check --select UP` passes

---

## Category 5: Evidence & Documentation (MANDATORY)

- [ ] **Evidence Trail Complete**
  - Test execution logs included
  - Build logs included
  - Linting results included

- [ ] **Completion Report Submitted**
  - Builder completion report created
  - All sections filled out
  - Evidence linked

- [ ] **PR Description Complete**
  - What was implemented
  - Architecture reference
  - Test results summary
  - Evidence links

---

## Category 6: Governance Compliance (MANDATORY)

- [ ] **Build Philosophy Honored**
  - One-Time Build Correctness principle followed
  - Zero regression
  - Build-to-Green workflow followed

- [ ] **No Test Removal Without Authorization**
  - No tests removed
  - OR: FM authorization obtained for test removal
  - Test removal logged (if applicable)

- [ ] **Warning Handling Doctrine Followed**
  - No warnings suppressed
  - All warnings fixed
  - Immediate remedy applied

- [ ] **Constitutional Sandbox Pattern Respected**
  - Tier-1 Constitutional requirements absolute
  - Tier-2 Procedural adaptations documented (if any)
  - Judgment decisions explained

---

## Category 7: Merge Readiness (MANDATORY)

- [ ] **FM Approval Obtained**
  - FM reviewed work
  - FM confirmed gate readiness
  - FM merge authorization provided

- [ ] **No Blocking Issues**
  - No known bugs
  - No incomplete work
  - No technical debt introduced

- [ ] **Handover Complete**
  - All deliverables provided
  - All evidence linked
  - Handover authorized by builder

---

## Category 8: Builder-Specific Requirements (MANDATORY)

### For UI Builder

- [ ] Component tests passing
- [ ] Visual regression tests passing (if applicable)
- [ ] Accessibility standards met
- [ ] Responsive design validated

### For API Builder

- [ ] API route tests passing
- [ ] Integration tests passing
- [ ] Error handling validated
- [ ] API documentation updated (if applicable)

### For Schema Builder

- [ ] Schema validation passing
- [ ] Migration tests passing
- [ ] Data integrity validated
- [ ] Schema documentation updated (if applicable)

### For Integration Builder

- [ ] Integration tests passing
- [ ] External service mocks validated
- [ ] Error handling tested
- [ ] Integration documentation updated (if applicable)

### For QA Builder

- [ ] Test infrastructure validated
- [ ] Test coverage metrics documented
- [ ] QA-to-Red suite validated
- [ ] Test documentation updated (if applicable)

---

## Checklist Usage

### Before PR Creation

1. Complete all applicable categories
2. Mark N/A for non-applicable items with justification
3. Collect all evidence

### During PR Review

1. FM validates all MANDATORY categories
2. Gates enforce checklist mechanically
3. No subjective criteria permitted

### Before Merge

1. All MANDATORY items complete
2. FM authorization obtained
3. All gates GREEN

---

## Gate Enforcement

**Automated Gates**:
- Agent Boundary Gate (Category 3)
- Build-to-Green Enforcement (Category 2)
- Builder QA Gate (Category 2, 4)
- Deprecation Detection Gate (Category 4)

**Manual Review**:
- FM Architecture Gate (Category 1)
- FM Merge Approval (Category 7)

**Hard Rule**: If all checklist items satisfied, gates MUST pass. No additional requirements.

---

## References

- **Canonical Protocol**: maturion-foreman-governance/governance/canon/EXECUTION_BOOTSTRAP_PROTOCOL.md
- **PR Gate Requirements Canon**: governance/alignment/PR_GATE_REQUIREMENTS_CANON.md
- **Gate Release Checklists Reference**: governance/alignment/PR_GATE_RELEASE_CHECKLISTS_REFERENCE.md
- **Builder Contracts**: `.github/agents/[builder-name].md`

---

**Version**: 2.0.0+  
**Status**: MANDATORY  
**Authority**: Canonical Governance

---

**END OF BUILDER PR RELEASE CHECKLIST**
