# Agent Onboarding

**Status**: Active  
**Authority**: CS2 (Agent Contract Minimalism Framework)  
**Date**: 2026-01-11  
**Updated**: Added BL-026 Automated Deprecation Detection Gate reference

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

## Automated Deprecation Detection Gate (BL-026)

**MANDATORY for all agents writing Python code**:

The **Automated Deprecation Detection Gate** (BL-026) enforces:
- Modern Python 3.12+ API patterns
- Zero deprecated API usage
- Forward compatibility with future Python versions
- Automated pre-commit and CI/CD enforcement

**Key Requirements**:
- Use `datetime.now(timezone.utc)` instead of `datetime.utcnow()`
- Use built-in generics (`dict`, `list`) instead of `typing.Dict`, `typing.List` (Python 3.9+)
- All violations block commit and merge
- Exceptions require FM approval with quarterly review

**Reference**: `governance/policies/AUTOMATED_DEPRECATION_DETECTION_GATE.md`

**Auto-Fix**: Run `ruff check --select UP --fix .` to auto-fix most violations

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
