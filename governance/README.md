# FM Repository Governance

**Status**: Initialized  
**Last Updated**: 2025-12-22

---

## Purpose

This directory contains FM repository governance scaffolding that establishes how the FM repository adopts and executes corporate governance canon.

**Critical Distinction**:
- **Corporate governance canon** lives in `maturion-foreman-governance` repository
- **FM governance scaffolding** (this directory) defines how FM adopts and executes that canon

This is **adoption and execution framing**, not governance creation.

---

## Directory Structure

```
governance/
├── README.md                              # This file
├── alignment/                             # Governance alignment documentation
│   └── GOVERNANCE_ALIGNMENT_OVERVIEW.md   # How FM adopts corporate governance
├── policies/                              # FM-specific execution policies
│   └── FM_GOVERNANCE_ADOPTION_POLICY.md   # How governance becomes execution
├── events/                                # FM Office visibility placeholders
│   └── README.md                          # Event structure for future dashboard
├── scope/                                 # Scope discipline documentation
│   └── README.md                          # Scope declaration requirements
├── agents/                                # Agent specifications (existing)
├── contracts/                             # Contracts and templates (existing)
├── dashboards/                            # Dashboard specifications (existing)
├── specs/                                 # Technical specifications (existing)
└── CROSS_REPOSITORY_AUTHORITY_AND_ESCALATION_POLICY.md (existing)
```

---

## Key Documents

### Governance Alignment

**[alignment/GOVERNANCE_ALIGNMENT_OVERVIEW.md](alignment/GOVERNANCE_ALIGNMENT_OVERVIEW.md)**
- Defines relationship with corporate governance canon
- Defines agent roles (Governance Liaison, FM Builder, FM Agent)
- Establishes that governance changes originate upstream
- Documents adoption model

### Governance Adoption

**[policies/FM_GOVERNANCE_ADOPTION_POLICY.md](policies/FM_GOVERNANCE_ADOPTION_POLICY.md)**
- Defines how governance rules become FM execution constraints
- Establishes PR gates as governance enforcement
- Requires build-to-green before handover
- Documents future FM app mechanization plan

### FM Office Visibility

**[events/README.md](events/README.md)**
- Placeholder structure for FM Office dashboard events
- Forward compatibility for future automation
- Event-driven governance visibility model

### Scope Discipline

**[scope/README.md](scope/README.md)**
- Scope declaration requirements
- One-domain-per-PR rule
- Alignment with corporate scope discipline

---

## Agent Roles

### Governance Liaison (FM-Scoped)
- Monitors corporate governance canon changes
- Translates governance into FM execution requirements
- Ensures FM remains aligned with upstream governance
- Does NOT create or modify governance

### FM Builder
- Executes build tasks within FM repository
- Must build-to-green (no handover until CI is green)
- Operates under governance constraints
- Follows PR gate enforcement

### FM Agent (Future)
- Will mechanize governance enforcement
- Will provide real-time governance feedback
- Will power FM Office dashboard
- Not yet implemented

---

## Governance Flow

```
Corporate Governance Canon (upstream)
           ↓
   Governance Liaison
           ↓
FM Execution Constraints (this repo)
           ↓
    PR Gates (GitHub Actions)
           ↓
   FM Builder (builds to green)
           ↓
  Future: FM Agent (mechanizes enforcement)
```

---

## Relationship to Corporate Governance

### What Lives Upstream (maturion-foreman-governance)
- Constitutional rules (GSR, Zero Test Debt, Design Freeze, etc.)
- Architecture standards and validation checklists
- QA governance and minimum coverage requirements
- Compliance specifications and control libraries
- All canonical governance definitions

### What Lives Here (FM Repository)
- How FM adopts upstream governance
- How governance rules become execution constraints
- PR gate configurations (enforcement mechanisms)
- Builder specifications (execution agents)
- Future FM app automation (mechanization)

### Unbreakable Rules
1. **No governance creation** - FM does not define governance
2. **No governance reinterpretation** - FM does not modify governance meaning
3. **No governance weakening** - FM does not reduce governance requirements
4. **Adoption only** - FM adopts and executes governance as defined upstream

---

## Evolution Path

### Current State (Initialization)
- Governance scaffolding established
- Directory structure in place
- Alignment and adoption documented
- No execution automation

### Near Future (FM Builder Era)
- FM Builder operates under governance constraints
- PR gates enforce governance mechanically
- Build-to-green is mandatory before handover
- Governance Liaison monitors upstream changes

### Future State (FM Agent Era)
- FM Agent mechanizes governance enforcement
- Real-time governance feedback in development
- FM Office dashboard shows governance state
- Audible alerts for governance violations

---

## Notes

- This scaffolding is **foundational** - it establishes structure before automation
- No execution logic exists yet - this is alignment documentation only
- All governance authority flows from upstream canon
- PR gates are currently the authoritative governance enforcement mechanism

---

## References

- **Corporate Governance Canon**: https://github.com/MaturionISMS/maturion-foreman-governance
- **Build Philosophy**: `/BUILD_PHILOSOPHY.md`
- **Governance Relocation Summary**: `/GOVERNANCE_RELOCATION_SUMMARY.md`

---

*FM Repository Governance Scaffolding - Foundation for Governance-Aligned Execution*
