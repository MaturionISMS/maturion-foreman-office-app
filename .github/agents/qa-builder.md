# Cross-Repository Context Block

Maturion Governance and Builder Agents operate in a tightly coupled, multi-repository ecosystem. For this agent to function correctly, the following cross-repo context must always be consulted:

- The canonical Maturion governance rules live in the `maturion-foreman-governance` repository. All major agent contracts, policies, schemas, and core canonical references are anchored there.
- All downstream application repositories (such as `maturion-foreman-office-app`) must reference governance canon and agent contract requirements upstream.
- Agent files (such as this one) are only valid if they reference, comply with, and surface ripple-up and ripple-down effects throughout the ecosystem.
- Update and enhancement proposals MUST consider:
    - Alignment with `.github/agents/governance-repo-administrator.agent.md` in `maturion-foreman-governance`
    - Updates to and from policies, doctrine, or MANDATORY sections defined in the governance repo
    - Explicit notes about breakage or impact in sibling app repos

**All agents operating in `maturion-foreman-office-app` are expected to escalate ambiguity and ripple cases upward, and to consult the Governance Repository Administrator for canonical intent.**

---

[original file content preserved below]
