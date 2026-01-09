# BL-024 Constitutional Sandbox Pattern — Layer Down Event

**Event Type**: Governance Canon Layer Down  
**Date**: 2026-01-09  
**Status**: Visibility Pending → Active  
**Authority**: Governance Liaison (on behalf of Johan/Governance Administrator)  
**Canonical Reference**: [CONSTITUTIONAL_SANDBOX_PATTERN.md](https://github.com/APGI-cmy/maturion-foreman-governance/blob/main/governance/canon/CONSTITUTIONAL_SANDBOX_PATTERN.md)

---

## Purpose

This event notifies FM and all builders that **BL-024 Constitutional Sandbox Pattern** has been layered down from governance canon into FM App repository contracts, onboarding, and process documentation.

**No immediate action required by FM or builders currently executing work.**

---

## What Changed

### Canonical Source (Governance Repo)
- **BL-024**: Constitutional Sandbox Pattern canonized in maturion-foreman-governance
- **Distinction**: Tier-1 Constitutional (immutable) vs Tier-2 Procedural (adaptable with justification)
- **Bootstrap Entry**: [BL-024 in BOOTSTRAP_EXECUTION_LEARNINGS.md](https://github.com/APGI-cmy/maturion-foreman-governance/blob/main/governance/canon/BOOTSTRAP_EXECUTION_LEARNINGS.md)
- **Rollout Guidance**: [CONSTITUTIONAL_SANDBOX_ROLLOUT_GUIDANCE.md](https://github.com/APGI-cmy/maturion-foreman-governance/blob/main/governance/canon/CONSTITUTIONAL_SANDBOX_ROLLOUT_GUIDANCE.md)

### FM App Repository Updates
1. **FM Agent Contract** (`.github/agents/ForemanApp-agent.md`)
   - Added BL-024 to governance bindings
   - Added Constitutional Sandbox Pattern section
   - Defined FM responsibilities: validate constitutional compliance, support builder judgment, document adaptations, escalate ambiguity

2. **Builder Contracts** (api-builder, integration-builder, qa-builder, ui-builder, schema-builder)
   - Added BL-024 to governance bindings
   - Added Constitutional Sandbox Pattern section
   - Clarified builder judgment authority within constitutional boundaries
   - Added requirement to document judgment/optimization decisions

3. **Onboarding** (`governance/AGENT_ONBOARDING.md`)
   - Added BL-024 reference and Tier-1 vs Tier-2 distinction

4. **Training** (`governance/BUILDER_TRAINING_CHECKLIST.md`)
   - Added mandatory BL-024 training requirement
   - Added Constitutional Sandbox awareness to acknowledgment
   - Updated training completion checklist

5. **Templates** (`.github/PULL_REQUEST_TEMPLATE.md`, `.github/agent-templates/PREHANDOVER_PROOF_TEMPLATE.md`)
   - Added constitutional compliance verification checkboxes
   - Added procedural adaptation documentation requirements

---

## What This Means

### For FM (ForemanApp-agent)
- **New Responsibility**: Validate that builders preserve Tier-1 constitutional requirements
- **New Enablement**: Communicate to builders that they have judgment authority within Tier-2 procedural boundaries
- **New Documentation**: When builders adapt process guidance, ensure justification is captured
- **New Escalation Path**: If unclear whether requirement is Tier-1 or Tier-2, escalate to Johan

### For Builders (All)
- **New Authority**: May exercise judgment on Tier-2 procedural guidance (process steps, tooling choices, optimization approaches)
- **Immutable Requirements**: Tier-1 constitutional requirements remain absolute (Zero Test Debt, 100% GREEN, One-Time Build, BUILD_PHILOSOPHY, Design Freeze, Architecture Conformance)
- **New Obligation**: MUST document all judgment/optimization decisions and rationale
- **Example**: May choose different implementation pattern (procedural), CANNOT skip tests (constitutional)

---

## Grace Period

**None required** — This is a **clarification and enablement**, not a new restriction.

- Builders already operate under constitutional requirements (Tier-1)
- BL-024 **permits** flexibility in procedural guidance (Tier-2) that may not have been explicitly understood before
- No existing practices are prohibited by this change

**Future Impact**: Builders may adapt procedural guidance more confidently, provided constitutional requirements are preserved and adaptations are documented.

---

## Enforcement

### Immediate (2026-01-09 onward)
- **Training**: New builders MUST complete BL-024 training before assignment
- **PR Template**: Constitutional compliance checkboxes now present in PR template
- **Prehandover Proof**: Constitutional compliance attestation now required

### No Retroactive Changes
- Builders currently executing work: No immediate change required
- Builders completing work: Use new PR template and prehandover proof format
- Builders starting new subwaves: Complete BL-024 training as part of onboarding refresh

---

## Ripple Scope

### Files Modified in This Layer Down
- `.github/agents/ForemanApp-agent.md`
- `.github/agents/api-builder.md`
- `.github/agents/integration-builder.md`
- `.github/agents/qa-builder.md`
- `.github/agents/ui-builder.md`
- `.github/agents/schema-builder.md`
- `governance/AGENT_ONBOARDING.md`
- `governance/BUILDER_TRAINING_CHECKLIST.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/agent-templates/PREHANDOVER_PROOF_TEMPLATE.md`
- `governance/events/bl-024-constitutional-sandbox-pattern-layer-down.md` (this file)

### Governance Alignment
- **No Tier-0 changes**: BL-024 does not modify Tier-0 constitutional documents
- **Consistent with BUILD_PHILOSOPHY.md**: Clarifies existing constitutional vs procedural distinction
- **Enhances builder enablement**: Provides framework for judgment within boundaries

---

## Questions & Escalation

### Common Questions

**Q: What if I'm unsure whether a requirement is Tier-1 or Tier-2?**  
**A**: Escalate to FM. If FM is unsure, FM escalates to Johan. Default assumption: Treat as Tier-1 (immutable) until clarified.

**Q: Can I adapt Zero Test Debt or 100% GREEN requirements?**  
**A**: **NO.** These are Tier-1 constitutional requirements and are NEVER negotiable.

**Q: Can I choose a different test framework or implementation pattern?**  
**A**: Yes, provided: (1) Constitutional requirements are preserved, (2) You document your decision and rationale, (3) You verify with FM if uncertain.

**Q: Do I need to document every small implementation choice?**  
**A**: Document significant judgment/optimization decisions that deviate from explicit procedural guidance. Use your judgment on what constitutes "significant."

### Escalation Path
1. **Builder uncertainty** → Escalate to FM
2. **FM uncertainty** → Escalate to Johan (Governance Administrator)
3. **Ambiguous Tier-1 vs Tier-2** → Johan decides, may update canonical guidance

---

## Related References

**Canonical Governance** (maturion-foreman-governance repository):
- [CONSTITUTIONAL_SANDBOX_PATTERN.md](https://github.com/APGI-cmy/maturion-foreman-governance/blob/main/governance/canon/CONSTITUTIONAL_SANDBOX_PATTERN.md)
- [BL-024 in BOOTSTRAP_EXECUTION_LEARNINGS.md](https://github.com/APGI-cmy/maturion-foreman-governance/blob/main/governance/canon/BOOTSTRAP_EXECUTION_LEARNINGS.md)
- [CONSTITUTIONAL_SANDBOX_ROLLOUT_GUIDANCE.md](https://github.com/APGI-cmy/maturion-foreman-governance/blob/main/governance/canon/CONSTITUTIONAL_SANDBOX_ROLLOUT_GUIDANCE.md)

**FM App Repository**:
- Agent contracts: `.github/agents/`
- Onboarding: `governance/AGENT_ONBOARDING.md`
- Training: `governance/BUILDER_TRAINING_CHECKLIST.md`
- Templates: `.github/PULL_REQUEST_TEMPLATE.md`, `.github/agent-templates/PREHANDOVER_PROOF_TEMPLATE.md`

**Change PR**: [foreman-governance#910](https://github.com/APGI-cmy/maturion-foreman-governance/pull/910)

---

## Visibility Acknowledgment

**FM**: Read and acknowledged (date: _____)  
**Builders**: Notified via onboarding and training updates

**Status**: Visibility event created. Active for all new onboarding and PRs as of 2026-01-09.

---

*END OF VISIBILITY EVENT*
