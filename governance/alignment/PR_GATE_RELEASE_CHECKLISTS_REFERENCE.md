# PR Gate Release Checklists (Canonical Reference)

**Status**: Canonical Reference  
**Authority**: Corporate Governance Canon (`maturion-foreman-governance`)  
**FM Scope**: Enforcement-Only (No Modification)

---

## Purpose

This document references the **canonical** PR Gate Release Checklists from the governance repository and ensures FM enforcement aligns with checklist-driven predictability.

---

## Canonical Source

**Repository**: `maturion-foreman-governance`  
**Documents**:
- `PR_GATE_RELEASE_CHECKLIST_BUILDER.md`
- `PR_GATE_RELEASE_CHECKLIST_GOVERNANCE_ADMIN.md`
- `PR_GATE_RELEASE_CHECKLIST_FM.md`

These checklists are **authoritative** and define exactly what must be satisfied for PR gates to pass.

---

## Key Principle (Canonical)

> **Checklists define gate requirements. Gates enforce checklists. Nothing more.**

If all checklist items for the active agent role are satisfied, the PR gate **MUST** pass.

If a gate blocks compliant work, it is a governance alignment defect.

---

## Checklist Applicability

Each agent role has a specific release checklist:

| Agent Role         | Checklist Document                              |
|--------------------|-------------------------------------------------|
| Builder            | `PR_GATE_RELEASE_CHECKLIST_BUILDER.md`          |
| Governance Admin   | `PR_GATE_RELEASE_CHECKLIST_GOVERNANCE_ADMIN.md` |
| FM Agent           | `PR_GATE_RELEASE_CHECKLIST_FM.md`               |

Only the checklist for the **active agent role** applies to a given PR.

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

**Last Updated**: 2025-12-22  
**Authority**: Corporate Governance Canon  
**FM Status**: Enforcement-Only (No Local Modification)
