# Post-Job Enhancement Reflection — Agent Contract Section Template

**Version**: 1.0.0  
**Status**: CANONICAL TEMPLATE  
**Authority**: governance/canon/MANDATORY_ENHANCEMENT_CAPTURE_DOCTRINE.md  
**Date**: 2026-01-05

---

## Purpose

This template defines the canonical "Post-Job Enhancement Reflection — MANDATORY" section that MUST be present in all agent contracts (builders, FM agents, and governance liaison agents).

---

## Template Text

Copy this section verbatim (or with minor agent-specific adaptations) into all agent contracts:

```markdown
## Post-Job Enhancement Reflection — MANDATORY

After declaring a job **COMPLETE**, this agent MUST:

1. Pause and consider whether there are structural, ergonomic, or governance improvements that:
   - Would reduce future work or friction,
   - Improve observability, safety, or clarity,
   - Or close small obvious gaps that were intentionally left out-of-scope.

2. If such improvements exist and are within this agent's governance boundaries:
   - Record them explicitly under a **"Possible Future Enhancements"** heading
     in the PR body, completion report, or issue comment.
   - Each enhancement must be framed as **future work**, not silently folded
     into the current job.
   - Mark all enhancements: `PARKED — NOT AUTHORIZED FOR EXECUTION`
   - Route to appropriate authority (FM for builders, Johan for FM/governance)

3. If no meaningful enhancements are identified:
   - State this explicitly (e.g., `No material future enhancements identified beyond current scope.`).

**This section does not authorize scope creep in the current job.**  
It mandates **capturing** enhancements for future planning under OPOJD and One-Time Build discipline.

**Canonical Authority**: `governance/canon/MANDATORY_ENHANCEMENT_CAPTURE_DOCTRINE.md`
```

---

## Placement in Agent Contracts

### For Builder Agents

Place this section:
- **After**: "Gate-First Handover Protocol — MANDATORY"
- **Before**: "Ripple Boundary Acknowledgment — MANDATORY"

### For FM Agents (ForemanApp)

Place this section:
- **After**: Core execution sections (sequencing, gates, etc.)
- **Before**: "Signature" or final metadata

Suggested location: After Section XVIII (Execution Scope)

### For Governance Liaison Agents

Place this section:
- **After**: Safety Authority and enforcement sections
- **Before**: "End State" or final summary

Suggested location: After Section 2C (Agent-Scoped QA Boundary Enforcement)

---

## Agent-Specific Adaptations (Optional)

### Builder Agents

Can add builder-specific enhancement categories:
```markdown
**Enhancement Categories for Builders**:
- Architecture clarity/completeness
- QA coverage/effectiveness
- Implementation patterns/practices
- Tool/library selection
- Build ergonomics
```

### FM Agents

Can add FM-specific enhancement categories:
```markdown
**Enhancement Categories for FM**:
- Wave orchestration efficiency
- Builder coordination patterns
- Gate enforcement mechanisms
- Evidence collection/validation
- Governance enforcement tooling
```

### Governance Liaison Agents

Can add governance-specific enhancement categories:
```markdown
**Enhancement Categories for Governance**:
- Governance alignment automation
- Ripple intelligence handling
- Canon validation tooling
- Cross-repo synchronization
- Governance observability
```

---

## Validation

Agent contracts with this section MUST:
- ✅ Include the mandatory reflection requirement
- ✅ Include the output requirement (proposal or negation)
- ✅ Include the "PARKED — NOT AUTHORIZED FOR EXECUTION" marking
- ✅ Include routing to appropriate authority
- ✅ Include explicit negation format
- ✅ State that this does not authorize scope creep
- ✅ Reference the canonical doctrine

---

## Integration with BUILDER_CONTRACT_SCHEMA.md

This template is referenced in:
- `.github/agents/BUILDER_CONTRACT_SCHEMA.md` § "Mandatory Enhancement Capture" (lines 592-635)

Builders already have this section (as of Schema 2.0). This template formalizes the canonical text for FM and governance agents.

---

## Usage

1. **For new agent contracts**: Include this section verbatim
2. **For existing agent contracts**: Add this section if missing (ForemanApp, governance-liaison)
3. **For builder contracts**: Already compliant (no action needed)
4. **For agent contract updates**: Ensure this section remains present and unchanged

---

**Template Authority**: governance/canon/MANDATORY_ENHANCEMENT_CAPTURE_DOCTRINE.md  
**Template Status**: CANONICAL and ACTIVE  
**Template Version**: 1.0.0

---

*END OF POST-JOB ENHANCEMENT REFLECTION TEMPLATE*
