# Execution Bootstrap Protocol - Canonical Reference

**Status**: Active Reference  
**Authority**: maturion-foreman-governance (Canonical Source)  
**Version**: 2.0.0+  
**Last Updated**: 2026-01-11  
**Compliance Deadline**: 2026-02-11

---

## Purpose

This document provides a reference to the **Execution Bootstrap Protocol** from the canonical governance repository and ensures FM App repository compliance with all protocol requirements for 2026.

---

## Canonical Source Documents

**Repository**: `APGI-cmy/maturion-foreman-governance`  
**Location**: `governance/canon/`

### Primary Protocol Documents

1. **EXECUTION_BOOTSTRAP_PROTOCOL.md**
   - Path: `governance/canon/EXECUTION_BOOTSTRAP_PROTOCOL.md`
   - Role: Primary protocol specification
   - Summary: 7-step verification protocol before handover
   - Status: MANDATORY for all agents (FM + Builders)

2. **EXECUTION_BOOTSTRAP_PROTOCOL_MONITORING_AND_ENFORCEMENT.md**
   - Path: `governance/canon/EXECUTION_BOOTSTRAP_PROTOCOL_MONITORING_AND_ENFORCEMENT.md`
   - Role: Monitoring and compliance tracking specification
   - Summary: Incident tracking, quarterly reporting, effectiveness monitoring
   - Status: MANDATORY for governance compliance

### Supporting Templates

3. **PREHANDOVER_PROOF_TEMPLATE.md**
   - Path: `governance/templates/PREHANDOVER_PROOF_TEMPLATE.md`
   - Role: Standard template for prehandover proof documentation
   - Summary: Evidence format, execution logs, attestation requirements
   - Status: MANDATORY for all execution-related PRs

4. **EXECUTION_BOOTSTRAP_PROTOCOL_QUARTERLY_MONITORING_REPORT.template.md**
   - Path: `governance/templates/EXECUTION_BOOTSTRAP_PROTOCOL_QUARTERLY_MONITORING_REPORT.template.md`
   - Role: Quarterly compliance and effectiveness reporting template
   - Summary: Metrics, violations, effectiveness assessment
   - Status: MANDATORY quarterly (Q2 2026 first report due 2026-04-14)

5. **EXECUTION_BOOTSTRAP_PROTOCOL_REFERENCE_IMPLEMENTATION.md**
   - Path: `governance/templates/EXECUTION_BOOTSTRAP_PROTOCOL_REFERENCE_IMPLEMENTATION.md`
   - Role: Reference implementation examples
   - Summary: Concrete examples of protocol execution
   - Status: GUIDANCE for implementation

---

## Protocol Summary: 7-Step Verification

All agents (FM and Builders) **MUST** execute this 7-step verification before handover:

### Category 0: Execution Bootstrap Protocol (MANDATORY v2.0.0+)

1. **Step 1: Identify Execution Artifacts**
   - Identify all execution artifacts created/modified (workflows, scripts, gates, configs)
   - Document artifact inventory in PREHANDOVER_PROOF

2. **Step 2: Local Execution**
   - Execute ALL artifacts locally in agent environment
   - Capture complete execution logs
   - Document success/failure for each artifact

3. **Step 3: Validate Exit Codes**
   - Verify all exit codes are 0 (success)
   - No warnings or errors permitted
   - Document validation results

4. **Step 4: Evidence Collection**
   - Collect execution logs, exit codes, outputs
   - Format evidence according to PREHANDOVER_PROOF_TEMPLATE
   - Link to all execution evidence

5. **Step 5: Failure Remediation**
   - If failures detected: FIX before handover
   - Re-execute after fixes
   - Document remediation actions

6. **Step 6: Green Attestation**
   - Agent attestation: "All checks GREEN on latest commit"
   - List all checks with ✅ status
   - Provide commit hash for verification

7. **Step 7: Handover Authorization**
   - Create PREHANDOVER_PROOF document
   - Include: "Handover authorized, all checks green"
   - Link to evidence and execution logs

**HARD RULE**: CI is confirmation, NOT diagnostic. No handover relying on CI to discover failures.

---

## FM App Implementation Requirements

### Requirement 1: All Agent Contracts Updated

**Status**: ALL agent contracts must reference the protocol

- `.github/agents/ForemanApp-agent.md` ✅ (to be updated)
- `.github/agents/governance-liaison.md` ✅ (to be updated)
- `.github/agents/ui-builder.md` ✅ (to be updated)
- `.github/agents/api-builder.md` ✅ (to be updated)
- `.github/agents/schema-builder.md` ✅ (to be updated)
- `.github/agents/integration-builder.md` ✅ (to be updated)
- `.github/agents/qa-builder.md` ✅ (to be updated)

**Implementation**: Add protocol reference to governance bindings section with version v2.0.0+

### Requirement 2: All Onboarding Updated

**Status**: Onboarding must include protocol training

- `governance/AGENT_ONBOARDING.md` ✅ (to be updated)
- `governance/BUILDER_TRAINING_CHECKLIST.md` ✅ (to be updated)
- Agent-specific onboarding guides ✅ (to be updated)

**Implementation**: Add 7-step protocol training requirement with acknowledgment

### Requirement 3: PR Release Checklists Updated

**Status**: All PR checklists must include Category 0 (v2.0.0+)

- Builder PR Checklist with Category 0 + Category 8 ✅ (to be created)
- FM PR Checklist with Category 0 + Category 4 ✅ (to be created)
- PREHANDOVER_PROOF requirement for execution PRs ✅ (existing template to be updated)

**Implementation**: Create comprehensive checklists with mandatory categories

### Requirement 4: Incident Tracking Infrastructure

**Status**: Local incident tracking must be operational

- `governance/incidents/protocol-violations/` directory ✅ (to be created)
- Tracking template ✅ (to be created)
- Violation reporting process ✅ (to be documented)

**Implementation**: Set up complete incident tracking structure

### Requirement 5: Monitoring & Reporting

**Status**: Quarterly monitoring must be scheduled

- First report due: 2026-04-14 (Q2 2026)
- Monitoring template ✅ (to be created locally)
- Compliance tracking ✅ (to be documented)

**Implementation**: Prepare monitoring infrastructure and schedule

---

## Governance Alignment Entry

This protocol is documented in `GOVERNANCE_ALIGNMENT.md` as:

- **Protocol Name**: Execution Bootstrap Protocol
- **Version**: 2.0.0+
- **Source**: maturion-foreman-governance/governance/canon/
- **Status**: MANDATORY
- **Compliance Deadline**: 2026-02-11
- **First Monitoring Report**: 2026-04-14

---

## Enforcement & Compliance

### Enforcement Mechanisms

1. **Agent Contracts**: All agents bound to protocol through governance bindings
2. **PR Gates**: PREHANDOVER_PROOF required for workflow/artifact PRs
3. **Training**: Mandatory protocol training in onboarding checklist
4. **Monitoring**: Quarterly compliance reporting
5. **Incident Tracking**: All violations logged and reviewed

### Compliance Validation

**Pre-Compliance Deadline (2026-02-11)**:
- [ ] All agent contracts reference protocol v2.0.0+
- [ ] All onboarding materials include protocol training
- [ ] All PR checklists include Category 0
- [ ] Incident tracking infrastructure operational
- [ ] First monitoring report scheduled

**Post-Compliance Deadline**:
- All new PRs must comply with protocol
- All violations trigger incident tracking
- Quarterly monitoring reports required

---

## Questions & Escalation

**For protocol questions**: Governance Liaison  
**For compliance issues**: FM (ForemanApp-agent)  
**For constitutional matters**: Johan Ras (CS2)  
**For canonical updates**: Governance Administrator (governance repo)

---

## References

- **Canonical Protocol**: maturion-foreman-governance/governance/canon/EXECUTION_BOOTSTRAP_PROTOCOL.md
- **Monitoring Spec**: maturion-foreman-governance/governance/canon/EXECUTION_BOOTSTRAP_PROTOCOL_MONITORING_AND_ENFORCEMENT.md
- **Template**: maturion-foreman-governance/governance/templates/PREHANDOVER_PROOF_TEMPLATE.md
- **Governance Alignment**: GOVERNANCE_ALIGNMENT.md (this repository)
- **Issue Tracking**: GitHub Issue #[NUMBER] - Layer Down: Full Execution Bootstrap Protocol Governance Rollout (2026)

---

**Status**: Active Reference  
**Compliance**: Required by 2026-02-11  
**Authority**: Canonical Governance (maturion-foreman-governance)

---

**END OF EXECUTION BOOTSTRAP PROTOCOL REFERENCE**
