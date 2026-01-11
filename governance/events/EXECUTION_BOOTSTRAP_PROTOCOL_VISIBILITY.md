# Execution Bootstrap Protocol - Visibility Event

**Event Type**: Governance Protocol Layer-Down  
**Date**: 2026-01-11  
**Effective Date**: 2026-02-11 (Compliance Deadline)  
**Protocol Version**: 2.0.0+  
**Affects**: ALL Agents (FM + All Builders)  
**Authority**: maturion-foreman-governance/governance/canon/EXECUTION_BOOTSTRAP_PROTOCOL.md

---

## Purpose

This visibility event notifies ALL agents (Foreman and Builders) of the **Execution Bootstrap Protocol (v2.0.0+)** requirements that are now MANDATORY in the FM App repository.

**Key Message**: Starting 2026-02-11, ALL PRs that create or modify execution artifacts (workflows, scripts, gates, configs) MUST include a PREHANDOVER_PROOF document demonstrating completion of the 7-step verification protocol.

---

## What Changed

### NEW MANDATORY REQUIREMENT (2026-02-11)

**Execution Bootstrap Protocol (v2.0.0+)** is now required for:
- ALL agents: Foreman (FM) + All Builders
- ALL PRs with execution artifacts
- Execution artifacts include: workflows, scripts, gates, configs, automation tools

**7-Step Verification Process**:
1. Identify execution artifacts
2. Execute locally
3. Validate exit codes
4. Collect evidence
5. Remediate failures
6. Attest: "All checks GREEN"
7. Authorize handover

**Hard Rule**: CI is confirmation, NOT diagnostic. No handover relying on CI to discover failures.

---

## Who Is Affected

**ALL Agents**:
- ✅ Foreman (FM) - AFFECTED
- ✅ UI Builder - AFFECTED
- ✅ API Builder - AFFECTED
- ✅ Schema Builder - AFFECTED
- ✅ Integration Builder - AFFECTED
- ✅ QA Builder - AFFECTED
- ✅ Governance Liaison - AFFECTED (enforcement role)

**No Exceptions**: This protocol applies to ALL agents creating or modifying execution artifacts.

---

## What You Need to Do

### Immediate Actions (By 2026-02-11)

1. **Read Protocol Documentation**
   - Read: `governance/canon/EXECUTION_BOOTSTRAP_PROTOCOL_REFERENCE.md`
   - Review: `.github/agent-templates/PREHANDOVER_PROOF_TEMPLATE.md`
   - Understand: 7-step verification process

2. **Complete Training**
   - Protocol training is now in `governance/BUILDER_TRAINING_CHECKLIST.md`
   - Protocol training is now in `governance/AGENT_ONBOARDING.md`
   - Acknowledge understanding of protocol requirements

3. **Update Your Workflow**
   - Identify when you create/modify execution artifacts
   - Plan for local execution before handover
   - Prepare evidence collection process

4. **Use PREHANDOVER_PROOF Template**
   - Template location: `.github/agent-templates/PREHANDOVER_PROOF_TEMPLATE.md`
   - Include in PR for ALL execution-related work
   - Complete ALL 7 steps (no skipping permitted)

### For Each Future PR with Execution Artifacts

1. **Before Starting Work**
   - Understand what execution artifacts will be created/modified
   - Plan local execution environment
   - Review PREHANDOVER_PROOF template

2. **During Work**
   - Track all execution artifacts
   - Prepare evidence collection
   - Document execution approach

3. **Before Handover**
   - Execute ALL artifacts locally
   - Validate ALL exit codes = 0
   - Collect complete evidence
   - Fix any failures
   - Create PREHANDOVER_PROOF document

4. **At Handover**
   - Include PREHANDOVER_PROOF in PR
   - Attest: "All checks GREEN"
   - Authorize handover with evidence

---

## Grace Period & Enforcement

**Grace Period**: 2026-01-11 to 2026-02-11 (31 days)

During grace period:
- Protocol is recommended but not enforced
- Agents should practice protocol
- Training must be completed
- Questions may be asked

**Enforcement Begins**: 2026-02-11

After grace period:
- Protocol is MANDATORY
- PRs without PREHANDOVER_PROOF will be rejected
- Violations tracked in `governance/incidents/protocol-violations/`
- Quarterly monitoring reports required

---

## Key Concepts

### What Are "Execution Artifacts"?

Execution artifacts are files that are executed or interpreted by systems:

**YES - Execution Artifacts** (protocol applies):
- GitHub Actions workflows (`.github/workflows/*.yml`)
- Python scripts (`.py` files in `governance/scripts/`, `foreman/scripts/`)
- Shell scripts (`.sh` files)
- Gate configurations
- CI/CD configurations
- Automation tools

**NO - Not Execution Artifacts** (protocol does NOT apply):
- Documentation files (`.md`)
- Architecture specifications
- Test files (covered by different gates)
- UI components
- API routes
- Schema definitions

**When in Doubt**: Ask in PR if protocol applies. Better to include PREHANDOVER_PROOF unnecessarily than to omit it when required.

### Hard Rule: CI is Confirmation, NOT Diagnostic

**OLD (Prohibited) Workflow**:
1. Make changes
2. Push to PR
3. Wait for CI to fail
4. Fix based on CI failures
5. Repeat

**NEW (Required) Workflow**:
1. Make changes
2. Execute locally BEFORE push
3. Fix all failures locally
4. Document green execution in PREHANDOVER_PROOF
5. Push with proof
6. CI confirms (should never fail)

**Why This Matters**:
- Prevents CI thrashing (multiple push attempts)
- Reduces build queue load
- Ensures quality before handover
- Demonstrates agent competence
- Reduces rework and delays

---

## Where to Find Information

**Protocol Documentation**:
- Reference: `governance/canon/EXECUTION_BOOTSTRAP_PROTOCOL_REFERENCE.md`
- Template: `.github/agent-templates/PREHANDOVER_PROOF_TEMPLATE.md`
- Validation: `governance/scripts/validate_prehandover_proof.py`

**PR Checklists**:
- Builders: `governance/checklists/BUILDER_PR_RELEASE_CHECKLIST.md`
- FM: `governance/checklists/FM_PR_RELEASE_CHECKLIST.md`

**Training Materials**:
- Onboarding: `governance/AGENT_ONBOARDING.md`
- Training Checklist: `governance/BUILDER_TRAINING_CHECKLIST.md`

**Agent Contracts** (updated with protocol binding):
- ForemanApp: `.github/agents/ForemanApp-agent.md`
- All Builders: `.github/agents/[builder-name].md`
- Governance Liaison: `.github/agents/governance-liaison.md`

**Monitoring**:
- Incident Tracking: `governance/incidents/protocol-violations/`
- Quarterly Reports: `governance/templates/EXECUTION_BOOTSTRAP_PROTOCOL_QUARTERLY_MONITORING_REPORT.md`

---

## Common Questions

### Q: When do I need PREHANDOVER_PROOF?

**A**: When your PR creates or modifies execution artifacts (workflows, scripts, gates, configs). If unsure, ask in PR comments or include proof anyway.

### Q: What if I don't modify execution artifacts?

**A**: Mark Category 0 as "N/A" in your PR checklist. Protocol does not apply to documentation, architecture, UI, API, schema, or test implementations.

### Q: Can I skip local execution if I'm confident?

**A**: NO. Local execution is MANDATORY. Confidence does not waive requirements. CI failure without local execution proof is a protocol violation.

### Q: What if local execution fails?

**A**: FIX failures BEFORE handover. Re-execute after fixes. Document remediation in PREHANDOVER_PROOF. NEVER hand over with failures.

### Q: What if I can't execute locally?

**A**: Escalate to FM immediately. Provide technical details. FM will help resolve. DO NOT hand over without local execution.

### Q: How detailed should evidence be?

**A**: Complete execution logs, exit codes, outputs. Evidence must be sufficient to verify GREEN status. See template for examples.

### Q: Will this slow me down?

**A**: Initially yes (learning curve). Long-term: FASTER (no CI thrashing, no rework, higher quality, fewer blockers).

---

## Escalation & Support

**Questions about protocol**: Governance Liaison  
**Technical execution issues**: FM (ForemanApp-agent)  
**Training questions**: FM  
**Violations or incidents**: Governance Liaison  
**Constitutional matters**: Johan Ras (CS2)

---

## Monitoring & Compliance

**Quarterly Monitoring**:
- First report: 2026-04-14 (Q1 2026)
- All violations logged and reviewed
- Effectiveness assessed quarterly
- Process improvements proposed

**Violation Consequences**:
1. **First violation**: Documentation + retraining
2. **Second violation**: FM accountability review
3. **Third violation**: Escalation to Johan (CS2)
4. **Major violation** (bypass, false attestation): Immediate escalation

---

## Summary

**What**: Execution Bootstrap Protocol (v2.0.0+) mandatory for all execution-related PRs

**Who**: ALL agents (FM + Builders)

**When**: Enforcement begins 2026-02-11 (31-day grace period)

**Why**: Ensure quality before handover, eliminate CI thrashing, reduce rework

**How**: 7-step verification + PREHANDOVER_PROOF document

**Where**: Template in `.github/agent-templates/PREHANDOVER_PROOF_TEMPLATE.md`

---

## Acknowledgment

**I have read and understood this visibility event**:
- [ ] I understand the Execution Bootstrap Protocol requirements
- [ ] I know when PREHANDOVER_PROOF is required
- [ ] I know where to find the template and documentation
- [ ] I understand the hard rule: "CI is confirmation, NOT diagnostic"
- [ ] I understand enforcement begins 2026-02-11
- [ ] I will complete protocol training before creating PRs after 2026-02-11

**Agent Name**: ________________  
**Date**: ________________  
**Role**: ________________

---

**Event Status**: ACTIVE  
**Visibility**: ALL AGENTS  
**Compliance Deadline**: 2026-02-11  
**Authority**: Canonical Governance

---

**END OF VISIBILITY EVENT**
