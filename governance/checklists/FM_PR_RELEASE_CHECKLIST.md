# FM PR Release Checklist

**Version**: 2.0.0+  
**Authority**: Execution Bootstrap Protocol + PR Gate Requirements Canon  
**Applies To**: Foreman (FM) Agent PRs  
**Status**: MANDATORY  
**Compliance Deadline**: 2026-02-11

---

## Purpose

This checklist defines exactly what must be satisfied for FM PR gates to pass. All items marked MANDATORY must be complete before PR merge.

**Key Principle**: If all checklist items are satisfied, the PR gate **MUST** pass. No additional requirements permitted.

---

## Category 0: Execution Bootstrap Protocol (MANDATORY v2.0.0+)

**Applies To**: ALL PRs that create or modify execution artifacts (workflows, scripts, gates, configs, orchestration tools)

- [ ] **Step 1: Execution Artifacts Identified**
  - All execution artifacts documented in PREHANDOVER_PROOF
  - Complete inventory with paths
  - Includes: workflows, scripts, gates, orchestration tools, automation
  
- [ ] **Step 2: Local Execution Complete**
  - All artifacts executed locally in agent environment
  - Complete execution logs captured
  - Execution environment documented
  - Special attention to orchestration and gate artifacts

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
  - FM attestation: "All checks GREEN on commit [hash]"
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

## Category 1: Architecture Governance (MANDATORY)

- [ ] **Architecture Completeness Validated**
  - Architecture compilation passes
  - All modules have frozen architecture
  - Architecture indexing up to date
  - No architecture gaps exist

- [ ] **Architecture Gate Logic Correct**
  - Gate enforcement aligns with architecture requirements
  - No gate logic errors
  - Gates test correctly

- [ ] **Architecture Traceability Maintained**
  - Architecture traceability matrix current
  - All components mapped
  - Traceability validated

---

## Category 2: Builder Orchestration (MANDATORY)

- [ ] **Builder Appointment Protocol Followed**
  - Builder appointments use canonical template
  - All appointment sections complete
  - Scope boundaries explicit
  - Ripple Intelligence alignment confirmed

- [ ] **Builder Task Specifications Complete**
  - Task specs follow canonical format
  - Architecture references correct
  - QA references correct
  - Success criteria explicit

- [ ] **Builder Coordination Validated**
  - Builder handoff logic correct
  - Builder sequencing validated
  - Builder dependencies documented

---

## Category 3: Agent QA Boundaries (MANDATORY)

- [ ] **FM QA Only**
  - FM modified only FM QA tests/code
  - No modifications to Builder QA
  - No modifications to Governance QA
  - Agent boundary respected (T0-009 Constitutional)

- [ ] **No Cross-Boundary Violations**
  - FM stayed within orchestration/governance scope
  - No builder implementation work
  - Boundaries documented if clarification needed

---

## Category 4: FM Execution Quality (MANDATORY)

- [ ] **100% Tests Passing**
  - All FM tests GREEN (100% pass rate)
  - Zero test debt
  - Zero skipped tests
  - Zero ignored tests

- [ ] **Zero Warnings**
  - No warnings in test output
  - No warnings in execution logs
  - No warnings in validation output

- [ ] **Orchestration Logic Validated**
  - Wave planning logic correct
  - Builder sequencing correct
  - Gate management logic correct
  - Evidence collection logic correct

- [ ] **Code Quality Standards Met**
  - Linting passed
  - Code review complete
  - Deprecation gate passed (BL-026)
  - No technical debt introduced

---

## Category 5: Gate & Workflow Management (MANDATORY)

- [ ] **Gate Configuration Validated**
  - All gates configured correctly
  - Gate applicability logic correct
  - Gate enforcement logic validated
  - No gate bypass logic

- [ ] **Workflow Definitions Correct**
  - Workflow syntax valid
  - Workflow logic correct
  - Workflow tested locally
  - Evidence of workflow execution provided

- [ ] **Gate-to-Checklist Alignment**
  - Gates enforce checklist requirements
  - No additional gate requirements
  - Gates respect agent role applicability
  - Predictability invariant maintained

---

## Category 6: Governance Compliance (MANDATORY)

- [ ] **Tier-0 Canon Compliance**
  - All Tier-0 documents honored
  - Constitutional requirements absolute
  - No Tier-0 violations

- [ ] **Build Philosophy Honored**
  - One-Time Build Correctness principle followed
  - Zero regression
  - FM orchestration aligns with philosophy

- [ ] **No Test Removal Without Authorization**
  - No tests removed
  - OR: Johan authorization obtained for test removal
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

## Category 7: Ripple Intelligence (MANDATORY)

- [ ] **Ripple Effects Identified**
  - All ripple effects documented
  - Ripple scope complete
  - Ripple validation planned

- [ ] **Ripple Execution Complete**
  - All ripple changes implemented
  - Ripple consistency validated
  - Validators executed

- [ ] **Ripple Evidence Provided**
  - Ripple manifest created/updated
  - All affected files listed
  - Validation results documented

---

## Category 8: Evidence & Documentation (MANDATORY)

- [ ] **Evidence Trail Complete**
  - Execution logs included
  - Validation results included
  - Test results included

- [ ] **FM Completion Report Submitted**
  - Completion report created
  - All sections filled out
  - Evidence linked

- [ ] **PR Description Complete**
  - What was changed
  - Why it was changed
  - Governance alignment confirmed
  - Evidence links provided

- [ ] **Governance Visibility Created**
  - Visibility event created (if governance change affects builders)
  - Visibility content clear
  - Grace period specified (if applicable)

---

## Category 9: Merge Readiness (MANDATORY)

- [ ] **Self-Review Complete**
  - FM reviewed own work
  - All checklist items validated
  - Evidence complete

- [ ] **Governance Liaison Review** (if applicable)
  - Governance Liaison reviewed governance changes
  - Governance alignment confirmed
  - Cross-repo boundaries respected

- [ ] **No Blocking Issues**
  - No known bugs
  - No incomplete work
  - No technical debt introduced

- [ ] **Handover Complete**
  - All deliverables provided
  - All evidence linked
  - Handover authorized by FM

---

## Category 10: Platform Actions (MANDATORY - FM Specific)

**Note**: FM cannot execute platform actions directly. Platform execution proxy required.

- [ ] **Platform Action Requirements Documented**
  - All required platform actions listed
  - Platform action specifications complete
  - Proxy execution requirements clear

- [ ] **Platform Action Validation**
  - Platform actions tested (via proxy in Wave 0)
  - Platform action logic validated
  - Platform action evidence provided

- [ ] **DAI/DAR Coordination** (if applicable)
  - DAI/DAR handoff specified
  - Platform action instructions clear
  - Execution verification planned

---

## Category 11: Builder Impact Assessment (MANDATORY - FM Specific)

- [ ] **Builder Impact Assessed**
  - Impact on all builders documented
  - Breaking changes identified
  - Migration path specified (if needed)

- [ ] **Builder Coordination Complete**
  - Builders notified of changes
  - Builder training updated (if needed)
  - Builder contracts updated (if needed)

- [ ] **Governance Transition Managed**
  - Transition plan documented
  - Grace period specified (if needed)
  - Enforcement timeline clear

---

## Checklist Usage

### Before PR Creation

1. Complete all applicable categories
2. Mark N/A for non-applicable items with justification
3. Collect all evidence
4. Create PREHANDOVER_PROOF (if execution artifacts modified)

### During PR Review

1. FM self-validates all MANDATORY categories
2. Governance Liaison validates governance changes (if applicable)
3. Gates enforce checklist mechanically

### Before Merge

1. All MANDATORY items complete
2. All gates GREEN
3. Evidence trail complete

---

## Gate Enforcement

**Automated Gates**:
- Agent Boundary Gate (Category 3)
- Build-to-Green Enforcement (Category 4)
- FM Architecture Gate (Category 1)
- Tier-0 Activation Gate (Category 6)
- Deprecation Detection Gate (Category 4)

**Manual Review**:
- FM Self-Review (Category 9)
- Governance Liaison Review (Category 9, if applicable)

**Hard Rule**: If all checklist items satisfied, gates MUST pass. No additional requirements.

---

## References

- **Canonical Protocol**: maturion-foreman-governance/governance/canon/EXECUTION_BOOTSTRAP_PROTOCOL.md
- **PR Gate Requirements Canon**: governance/alignment/PR_GATE_REQUIREMENTS_CANON.md
- **Gate Release Checklists Reference**: governance/alignment/PR_GATE_RELEASE_CHECKLISTS_REFERENCE.md
- **FM Contract**: `.github/agents/ForemanApp-agent.md`
- **FM Execution Mandate**: governance/contracts/FM_EXECUTION_MANDATE.md
- **FM Merge Gate Management Canon**: governance/alignment/FM_MERGE_GATE_MANAGEMENT_CANON.md

---

**Version**: 2.0.0+  
**Status**: MANDATORY  
**Authority**: Canonical Governance

---

**END OF FM PR RELEASE CHECKLIST**
