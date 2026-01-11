# PR Gate Release Checklists (Canonical Reference)

**Status**: Canonical Reference  
**Authority**: Corporate Governance Canon (`maturion-foreman-governance`)  
**FM Scope**: Enforcement-Only (No Modification)  
**Protocol Version**: 2.0.0+  
**Updated**: 2026-01-11 - Added Execution Bootstrap Protocol (Category 0)

---

## Purpose

This document references the **canonical** PR Gate Release Checklists from the governance repository and ensures FM enforcement aligns with checklist-driven predictability.

**Major Update (2026-01-11)**: All checklists now include **Category 0: Execution Bootstrap Protocol (v2.0.0+)** as MANDATORY for PRs with execution artifacts.

---

## Local FM App Checklists

**Local Implementation** (maturion-foreman-office-app):

- **Builder PR Checklist**: `governance/checklists/BUILDER_PR_RELEASE_CHECKLIST.md`
  - Version: 2.0.0+
  - Includes: Category 0 (Execution Bootstrap Protocol) + Category 8 (Builder-Specific Requirements)
  - Applies to: UI Builder, API Builder, Schema Builder, Integration Builder, QA Builder

- **FM PR Checklist**: `governance/checklists/FM_PR_RELEASE_CHECKLIST.md`
  - Version: 2.0.0+
  - Includes: Category 0 (Execution Bootstrap Protocol) + Category 4 (FM Execution Quality) + FM-specific categories
  - Applies to: Foreman (FM) Agent

**Compliance Deadline**: 2026-02-11  
**First Monitoring Report**: 2026-04-14

---

## Canonical Source

**Repository**: `maturion-foreman-governance`  
**Documents**:
- `PR_GATE_RELEASE_CHECKLIST_BUILDER.md` (canonical)
- `PR_GATE_RELEASE_CHECKLIST_GOVERNANCE_ADMIN.md` (canonical)
- `PR_GATE_RELEASE_CHECKLIST_FM.md` (canonical)
- `EXECUTION_BOOTSTRAP_PROTOCOL.md` (v2.0.0+ - Category 0)
- `EXECUTION_BOOTSTRAP_PROTOCOL_MONITORING_AND_ENFORCEMENT.md`

These checklists are **authoritative** and define exactly what must be satisfied for PR gates to pass.

**Local Implementations**:
- `governance/checklists/BUILDER_PR_RELEASE_CHECKLIST.md` (this repo)
- `governance/checklists/FM_PR_RELEASE_CHECKLIST.md` (this repo)

---

## Category 0: Execution Bootstrap Protocol (NEW 2026)

**MANDATORY for all PRs with execution artifacts (workflows, scripts, gates, configs)**

All agents (FM + Builders) must complete 7-step verification before handover:

1. Identify execution artifacts
2. Execute locally
3. Validate exit codes
4. Collect evidence
5. Remediate failures
6. Attest: "All checks GREEN"
7. Authorize handover

**Hard Rule**: CI is confirmation, NOT diagnostic. No handover relying on CI to discover failures.

**Template**: `.github/agent-templates/PREHANDOVER_PROOF_TEMPLATE.md`  
**Reference**: `governance/canon/EXECUTION_BOOTSTRAP_PROTOCOL_REFERENCE.md`  
**Canonical**: maturion-foreman-governance/governance/canon/EXECUTION_BOOTSTRAP_PROTOCOL.md

**Compliance Deadline**: 2026-02-11  
**Monitoring**: Quarterly reports (first due 2026-04-14)

---

## Key Principle (Canonical)

> **Checklists define gate requirements. Gates enforce checklists. Nothing more.**

If all checklist items for the active agent role are satisfied, the PR gate **MUST** pass.

If a gate blocks compliant work, it is a governance alignment defect.

---

## Checklist Applicability

Each agent role has a specific release checklist:

| Agent Role         | Checklist Document                              | Version | Category 0 |
|--------------------|-------------------------------------------------|---------|------------|
| Builder            | `governance/checklists/BUILDER_PR_RELEASE_CHECKLIST.md` | 2.0.0+ | ✅ INCLUDED |
| Governance Admin   | `PR_GATE_RELEASE_CHECKLIST_GOVERNANCE_ADMIN.md` (canonical) | TBD | TBD |
| FM Agent           | `governance/checklists/FM_PR_RELEASE_CHECKLIST.md` | 2.0.0+ | ✅ INCLUDED |

Only the checklist for the **active agent role** applies to a given PR.

**Note**: Builder and FM checklists in this repository (maturion-foreman-office-app) include Category 0 (Execution Bootstrap Protocol v2.0.0+) as of 2026-01-11.

---

## FM Implementation Requirements

FM workflows **must**:

1. **Load the correct checklist** for the detected agent role
2. **Validate only checklist items** (no additional requirements)
3. **Pass if all items satisfied** (no subjective criteria)
4. **Fail with checklist citation** if items not satisfied

FM workflows **must not**:

- ❌ Add requirements not in the checklist
- ❌ Apply checklists from other agent roles
- ❌ Use path-based or heuristic requirements
- ❌ Block compliant work with extra validations

---

## Predictability Invariant

From canonical governance:

> **If all checklist items for the active agent role are satisfied, the PR gate MUST pass.**

This invariant is **unbreakable** and ensures deterministic gate behavior.

---

## Gate-to-Checklist Mapping

FM gates must map to checklist sections:

| FM Gate                     | Builder Checklist       | Governance Checklist    | FM Checklist            |
|-----------------------------|-------------------------|-------------------------|-------------------------|
| Agent Boundary Gate         | Section: Agent QA       | Section: Agent QA       | Section: Agent QA       |
| Builder QA Gate             | Section: Builder QA     | N/A (not applicable)    | N/A (not applicable)    |
| Build-to-Green Enforcement  | Section: Test Execution | N/A (not applicable)    | Section: Test Execution |
| FM Architecture Gate        | N/A (not applicable)    | N/A (not applicable)    | Section: Architecture   |
| Governance Artifact Gate    | N/A (not applicable)    | Section: Artifacts      | N/A (not applicable)    |

**N/A (not applicable)** means the gate must skip for that agent role.

---

## Checklist-Driven Enforcement Example

For an **FM Agent** PR:

1. **Detect role**: FM Agent
2. **Load checklist**: `PR_GATE_RELEASE_CHECKLIST_FM.md`
3. **Apply gates**:
   - ✅ Agent Boundary Gate (applicable, enforce)
   - ⏭️ Builder QA Gate (not applicable, skip)
   - ✅ Build-to-Green Enforcement (applicable, enforce)
   - ✅ FM Architecture Gate (applicable, enforce)
   - ⏭️ Governance Artifact Gate (not applicable, skip)
4. **Result**: Pass if all applicable checklist items satisfied

---

## Documentation-Only Status

The PR Gate Release Checklists are **documentation-only**:

- They define **what** must be satisfied
- They do **not** define **how** gates enforce
- Gates enforce checklists, not the reverse

This ensures:
- Checklists remain human-readable and authoritative
- Gates remain machine-executable and predictable
- Changes to checklists propagate deterministically

---

## Compliance Validation

FM must validate that:

1. Every gate declares its checklist mapping
2. Every gate respects agent role applicability
3. No gate enforces requirements outside its checklist
4. Skipped gates do not cause PR failure

---

## References

- **Canonical Checklists**: `maturion-foreman-governance/PR_GATE_RELEASE_CHECKLIST_*.md`
- **Agent Role Applicability**: `governance/alignment/AGENT_ROLE_GATE_APPLICABILITY_REFERENCE.md`
- **Two-Gatekeeper Model**: `governance/alignment/TWO_GATEKEEPER_MODEL.md`
- **PR Gate Requirements Canon**: `governance/alignment/PR_GATE_REQUIREMENTS_CANON.md`

---

**Last Updated**: 2026-01-11  
**Authority**: Corporate Governance Canon  
**FM Status**: Enforcement-Only (No Local Modification)  
**Protocol Version**: 2.0.0+ (Execution Bootstrap Protocol included)
