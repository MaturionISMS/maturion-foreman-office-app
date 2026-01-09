# Agent Onboarding

**Status**: Active  
**Authority**: CS2 (Agent Contract Minimalism Framework)  
**Date**: 2026-01-09  
**Updated**: Added BL-024 Constitutional Sandbox Pattern reference

---

## Quick Start

**All agents start here**:

Read **AGENT_ONBOARDING_QUICKSTART.md** in the governance repository:  
https://github.com/APGI-cmy/maturion-foreman-governance/blob/main/governance/canon/AGENT_ONBOARDING_QUICKSTART.md

This provides:
- Your role and authority boundaries
- Essential canonical governance references
- 3-step operational protocol
- Escalation rules
- Mandatory compliance requirements

---

## Constitutional Sandbox Pattern (BL-024)

**All agents must understand**:

The **Constitutional Sandbox Pattern** (BL-024) distinguishes between:
- **Tier-1 Constitutional** (immutable): Zero Test Debt, 100% GREEN, One-Time Build Correctness, BUILD_PHILOSOPHY, Design Freeze, Architecture Conformance
- **Tier-2 Procedural** (adaptable with justification): Process steps, tooling choices, optimization approaches, implementation patterns

**Key Principle**: Constitutional requirements are absolute. Procedural guidance may be adapted when justified, with documentation.

**Reference**: [CONSTITUTIONAL_SANDBOX_PATTERN.md](https://github.com/APGI-cmy/maturion-foreman-governance/blob/main/governance/canon/CONSTITUTIONAL_SANDBOX_PATTERN.md)

---

## Then Read Your Contract

After reading the quickstart, read your `.agent` contract in `.github/agents/[your-agent].md`

Your contract is minimal (150-300 lines) and references canonical governance via `governance.bindings`.

---

## Questions?

**For operational questions**: Escalate to FM (ForemanApp-agent)  
**For governance questions**: Escalate to Governance Liaison  
**For constitutional questions**: Escalate to CS2 (Johan Ras)

---

## Canonical Governance Location

All canonical governance lives in the **maturion-foreman-governance** repository:
- Repository: https://github.com/APGI-cmy/maturion-foreman-governance
- Path: `/governance/canon/`
- Reference Branch: `main`

Your agent contract `governance.bindings` section specifies which canonical documents apply to your role.

---

*END OF AGENT ONBOARDING*
