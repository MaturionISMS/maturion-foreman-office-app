# Mandatory Enhancement Capture — Layer-Down Plan

**Version**: 1.0.0  
**Date**: 2026-01-05  
**Authority**: governance/canon/MANDATORY_ENHANCEMENT_CAPTURE_DOCTRINE.md  
**Status**: ACTIVE

---

## Purpose

This document outlines the layer-down plan for implementing the Mandatory Enhancement Capture doctrine across all Maturion ISMS repositories and agent contracts.

---

## I. FM Repository (maturion-foreman-office-app) — COMPLETE

### A. Status Summary

| Agent Type | Agent ID | Status | Action Required |
|------------|----------|--------|-----------------|
| Builder | ui-builder | ✅ COMPLETE | Already has section (Schema 2.0) |
| Builder | api-builder | ✅ COMPLETE | Already has section (Schema 2.0) |
| Builder | schema-builder | ✅ COMPLETE | Already has section (Schema 2.0) |
| Builder | integration-builder | ✅ COMPLETE | Already has section (Schema 2.0) |
| Builder | qa-builder | ✅ COMPLETE | Already has section (Schema 2.0) |
| FM Agent | ForemanApp | ✅ COMPLETE | Section added 2026-01-05 |
| Governance | governance-liaison | ✅ COMPLETE | Section added 2026-01-05 (one-time authorized) |

### B. Implementation Details

**Builders (ui, api, schema, integration, qa)**:
- Already compliant via BUILDER_CONTRACT_SCHEMA.md v2.0
- Section present at lines 592-635 in schema
- Section implemented in all active builder contracts
- No action required

**ForemanApp Agent**:
- Section added: 2026-01-05
- Location: Section XIX (Post-Job Enhancement Reflection)
- Version updated: 3.3.0 → 3.4.0
- Enhancement categories: Wave orchestration, builder coordination, gates, evidence, tooling, ripple

**Governance Liaison FM**:
- Section added: 2026-01-05
- Location: Section 5B (Post-Job Enhancement Reflection)
- Special authorization documented (one-time self-update)
- Enhancement categories: Governance automation, ripple, canon validation, cross-repo sync, observability

### C. Governance Artifacts Created

1. **Canonical Doctrine**: `governance/canon/MANDATORY_ENHANCEMENT_CAPTURE_DOCTRINE.md`
2. **Section Template**: `governance/templates/POST_JOB_ENHANCEMENT_REFLECTION_TEMPLATE.md`
3. **Layer-Down Plan**: `governance/alignment/MANDATORY_ENHANCEMENT_CAPTURE_LAYERDOWN_PLAN.md` (this document)

### D. Completion Evidence

- ✅ All 7 agent contracts have the mandatory section
- ✅ Canonical doctrine established
- ✅ Template documented
- ✅ One-time governance agent self-update authorized and documented
- ✅ All changes committed and validated

---

## II. Other FM-Related Repositories

### A. Applicable Repositories

If any of these repositories use `.agent` contracts for AI agents:
- `MaturionISMS/maturion-isms-core` (if exists)
- `MaturionISMS/maturion-compliance-engine` (if exists)
- `MaturionISMS/maturion-isms-modules` (if exists)

### B. Action Required (Future)

For each repository with agent contracts:

1. **Identify agent contracts**: List all `.agent` files in `.github/agents/` or equivalent
2. **Create follow-up issue**: Open issue in target repo referencing this doctrine
3. **Apply canonical section**: Add the section from `POST_JOB_ENHANCEMENT_REFLECTION_TEMPLATE.md`
4. **Validate consistency**: Ensure section matches canonical template
5. **Update agent versions**: Increment version numbers after adding section
6. **Document in PR**: Reference this layer-down plan and canonical doctrine

### C. Issue Template (Future Use)

```markdown
# Add Mandatory Enhancement Capture Section to Agent Contracts

## Context

Corporate governance has canonized "Mandatory Enhancement Capture" as a behavioral doctrine for all agents.

**Canonical Doctrine**: `maturion-foreman-office-app/governance/canon/MANDATORY_ENHANCEMENT_CAPTURE_DOCTRINE.md`  
**Section Template**: `maturion-foreman-office-app/governance/templates/POST_JOB_ENHANCEMENT_REFLECTION_TEMPLATE.md`  
**Layer-Down Plan**: `maturion-foreman-office-app/governance/alignment/MANDATORY_ENHANCEMENT_CAPTURE_LAYERDOWN_PLAN.md`

## Scope

Add the "Post-Job Enhancement Reflection — MANDATORY" section to all agent contracts in this repository:

- [ ] Agent 1: [name]
- [ ] Agent 2: [name]
- [ ] Agent N: [name]

## Deliverables

- [ ] Section added to all agent contracts
- [ ] Section matches canonical template
- [ ] Agent versions incremented
- [ ] All changes validated
- [ ] PR merged

## Authority

Johan Ras (CS2), via Mandatory Enhancement Capture Doctrine
```

---

## III. Governance Repository (maturion-foreman-governance)

### A. Status

**PENDING** — Requires separate issue in governance repository

### B. Action Required

1. **Mirror canonical doctrine**: Copy `MANDATORY_ENHANCEMENT_CAPTURE_DOCTRINE.md` to governance repo
2. **Update any governance agent contracts**: If governance repo has agent contracts, apply section
3. **Cross-repo alignment verification**: Ensure FM repo and governance repo are synchronized
4. **Update governance index**: Add doctrine to governance catalog/manifest

### C. Authority

- Governance Administrator (governance repo)
- Johan Ras (CS2) approval required

### D. Timeline

- **Target**: Within 2 weeks of FM repo completion
- **Blocker**: None (FM repo is complete and can proceed independently)

---

## IV. Cross-Repo Synchronization Protocol

### A. Source of Truth

**Primary Authority**: `maturion-foreman-office-app/governance/canon/MANDATORY_ENHANCEMENT_CAPTURE_DOCTRINE.md`

Until mirrored to governance repo, this is the canonical source.

### B. Synchronization Requirements

When propagating to other repositories:

1. **Copy canonical text**: Use exact section from template (or close variant)
2. **Reference canonical authority**: Always reference the doctrine document
3. **Document authorization**: Note that this is corporate governance requirement
4. **Maintain consistency**: Ensure section semantics remain consistent across repos

### C. Version Control

- **Doctrine version**: 1.0.0 (current)
- **Template version**: 1.0.0 (current)
- **Agent contract versions**: Increment on section addition

Future doctrine updates require:
- Update in source repo (FM repo or governance repo, whichever is canonical)
- Ripple to all implementing repositories
- Version increment across all affected contracts

---

## V. Validation and Enforcement

### A. Validation Criteria

An agent contract is compliant when:

- ✅ Contains "Post-Job Enhancement Reflection — MANDATORY" section
- ✅ Section includes mandatory reflection requirement
- ✅ Section includes output requirement (proposal or negation)
- ✅ Section includes "PARKED — NOT AUTHORIZED FOR EXECUTION" marking
- ✅ Section includes routing to appropriate authority
- ✅ Section states this does not authorize scope creep
- ✅ Section references canonical doctrine

### B. Enforcement Mechanisms

1. **Schema validation**: BUILDER_CONTRACT_SCHEMA.md already enforces for builders
2. **PR reviews**: Human reviewers check for section presence
3. **Automated checks**: Future CI validation (if implemented)
4. **Completion reports**: Agents must demonstrate enhancement capture or negation

### C. Non-Compliance Response

If an agent contract lacks this section:
- 🔴 Contract is non-compliant with governance
- 🔴 Agent cannot be appointed/recruited
- 🔴 Existing agents must be updated before next assignment
- 🔴 Escalate to Johan for resolution

---

## VI. Timeline and Milestones

### Completed

- ✅ 2026-01-05: Canonical doctrine created
- ✅ 2026-01-05: Section template documented
- ✅ 2026-01-05: ForemanApp agent updated
- ✅ 2026-01-05: Governance liaison agent updated (one-time authorized)
- ✅ 2026-01-05: Layer-down plan documented
- ✅ 2026-01-05: All FM repo agent contracts compliant

### Pending

- ⬜ TBD: Mirror doctrine to governance repository
- ⬜ TBD: Update any other repository agent contracts (as needed)
- ⬜ TBD: Cross-repo consistency validation

---

## VII. Special Cases and Exceptions

### A. One-Time Governance Agent Self-Update

**Authorization**: Documented in doctrine § XIII

**Scope**: ONLY for adding the "Post-Job Enhancement Reflection — MANDATORY" section

**Constraints**:
- No other self-modifications permitted
- Must document this exception in PR
- Requires Johan approval
- One-time only (expires after this issue)

**Evidence**: Section 5B of `governance-liaison.md` includes explicit authorization notice

### B. Future Agent Contracts

All new agent contracts (builders, FM, governance) MUST include this section from inception.

**Schema enforcement**: Already present in BUILDER_CONTRACT_SCHEMA.md v2.0

---

## VIII. Governance Alignment Verification

### A. Alignment with Existing Doctrine

This doctrine aligns with:
- ✅ BUILD_PHILOSOPHY.md (One-Time Build, OPOJD, Continuous Improvement)
- ✅ governance/policies/governance-supremacy-rule.md (Governance defines scope)
- ✅ governance/policies/design-freeze-rule.md (No mid-execution scope expansion)
- ✅ .github/agents/BUILDER_CONTRACT_SCHEMA.md (Already includes section for builders)

### B. No Conflicts Detected

- ✅ Does not weaken existing governance
- ✅ Does not authorize scope creep
- ✅ Does not bypass gates
- ✅ Does not conflict with OPOJD
- ✅ Compatible with One-Time Build

---

## IX. Success Criteria

This layer-down plan is SUCCESSFUL when:

- ✅ All FM repo agent contracts compliant (COMPLETE)
- ✅ Canonical doctrine established (COMPLETE)
- ✅ Section template documented (COMPLETE)
- ✅ One-time governance agent self-update authorized and completed (COMPLETE)
- ⬜ Governance repository mirrored doctrine (PENDING — separate issue)
- ⬜ Other repositories updated as needed (PENDING — as needed)

**Current Status**: FM repository layer-down is **COMPLETE**

---

## X. Contact and Escalation

### For Questions

- **Doctrine interpretation**: Escalate to Johan Ras (CS2)
- **Cross-repo synchronization**: Escalate to Governance Administrator
- **Agent contract updates**: Contact repository governance liaison agent

### For Issues

- **Non-compliance**: Escalate to Johan Ras (CS2)
- **Conflicts with existing doctrine**: Escalate to Johan Ras (CS2)
- **Implementation blockers**: Escalate to repository owner

---

## XI. Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2026-01-05 | Initial layer-down plan | Governance Liaison (FM repo) |

---

**Layer-Down Plan Status**: ACTIVE  
**FM Repository Status**: COMPLETE  
**Next Actions**: Mirror to governance repository (separate issue)

---

*END OF MANDATORY ENHANCEMENT CAPTURE LAYER-DOWN PLAN*
