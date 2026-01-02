# FM Repository Governance

**Status**: Hardened  
**Last Updated**: 2025-12-29  
**Batch 1 Governance Hardening**: Complete (Issues #123, #78, #86)

---

## Purpose

This directory contains FM repository governance scaffolding that establishes how the FM repository adopts and executes corporate governance canon.

**Critical Distinction**:
- **Corporate governance canon** lives in `maturion-foreman-governance` repository
- **FM governance scaffolding** (this directory) defines how FM adopts and executes that canon

This is **adoption and execution framing**, not governance creation.

---

## Master Authority Reference

**START HERE**: [GOVERNANCE_AUTHORITY_MATRIX.md](GOVERNANCE_AUTHORITY_MATRIX.md)

**This is the definitive answer to**:
- Who can stop a build, and why?
- Who owns governance decisions?
- Who enforces governance rules?
- Who can override governance?
- What is the escalation chain?

**Use this document to resolve all governance authority questions.**

---

## Directory Structure

```
governance/
├── README.md                                        # This file
├── GOVERNANCE_AUTHORITY_MATRIX.md                   # **Master authority reference**
├── alignment/                                       # Governance alignment documentation
│   ├── GOVERNANCE_ALIGNMENT_OVERVIEW.md             # How FM adopts corporate governance
│   ├── TWO_GATEKEEPER_MODEL.md                      # Dual gatekeeper authority
│   ├── PR_GATE_REQUIREMENTS_CANON.md                # Canonical PR gate requirements
│   ├── PR_GATE_FAILURE_HANDLING_PROTOCOL.md         # Canonical failure handling
│   └── ... (other alignment docs)
├── policies/                                        # FM-specific execution policies
│   ├── FM_GOVERNANCE_ADOPTION_POLICY.md             # How governance becomes execution
│   ├── RED_GATE_AUTHORITY_AND_OWNERSHIP.md          # **Red gate ownership rules**
│   ├── governance-supremacy-rule.md                 # Constitutional governance
│   ├── zero-test-debt-constitutional-rule.md        # Test debt prohibition
│   └── ... (other policies)
├── workflows/                                       # Governance workflows
│   ├── GOVERNANCE_POLICY_SYNC_SPECIFICATION.md      # **Policy sync mechanism**
│   └── ... (other workflow specs)
├── build/                                           # Build governance
│   └── BUILD_AUTHORIZATION_GATE.md                  # Build preconditions
├── events/                                          # FM Office visibility placeholders
├── scope/                                           # Scope discipline documentation
├── agents/                                          # Agent specifications
├── contracts/                                       # Contracts and templates
├── dashboards/                                      # Dashboard specifications
├── specs/                                           # Technical specifications
├── qa/                                              # QA governance
├── architecture/                                    # Architecture governance
├── reports/                                         # Governance reports
└── CROSS_REPOSITORY_AUTHORITY_AND_ESCALATION_POLICY.md
```

---

## Batch 1 Governance Hardening (Complete)

**Issues Addressed**: #123 (FM Governance Hardening), #78 (Governance Policy Sync), #86 (Red Gate Ownership)

**New Documents Created**:

1. **[GOVERNANCE_AUTHORITY_MATRIX.md](GOVERNANCE_AUTHORITY_MATRIX.md)**
   - Master authority reference
   - Answers: "Who can stop a build, and why?"
   - Defines all governance authority boundaries
   - Establishes escalation chains
   - Clarifies override authority

2. **[policies/RED_GATE_AUTHORITY_AND_OWNERSHIP.md](policies/RED_GATE_AUTHORITY_AND_OWNERSHIP.md)**
   - Explicit red gate ownership rules
   - Gate declaration authority matrix
   - Build stop authority clarification
   - FM behavior requirements for red gates
   - Addresses Issue #86

3. **[workflows/GOVERNANCE_POLICY_SYNC_SPECIFICATION.md](workflows/GOVERNANCE_POLICY_SYNC_SPECIFICATION.md)**
   - Governance policy synchronization mechanism
   - Canon-to-FM translation workflow
   - Drift detection and prevention
   - Upward ripple (FM lessons to canon)
   - Addresses Issue #78

**Result**: Zero governance ambiguity. Clear stop/go authority. Explicit policy sync mechanism.

---

## Key Documents

### Master Authority Reference

**[GOVERNANCE_AUTHORITY_MATRIX.md](GOVERNANCE_AUTHORITY_MATRIX.md)** ⭐
- **Definitive answer**: Who can stop a build, and why?
- Authority ownership for all governance decisions
- Gate declaration authority matrix
- Enforcement authority assignments
- Escalation chains
- Override authority (Johan only)
- **Use this document first for any authority question**

### FM Execution Mandate

**[contracts/FM_EXECUTION_MANDATE.md](contracts/FM_EXECUTION_MANDATE.md)** ⭐
- **FM's constitutional execution authority declaration**
- Autonomous role declaration (Build Manager, Orchestrator, Enforcement Authority)
- POLC execution model (Planning, Organizing, Leading, Controlling)
- Autonomous capabilities vs. bootstrap constraints
- Bootstrap proxy model (CS2 as mechanical proxy, authority remains with FM)
- STOP and escalation semantics
- Completion and handover definition
- **Pre-Build Gate — Required before any build execution**

**[contracts/FM_EXECUTION_MANDATE_ADDENDUM_001.md](contracts/FM_EXECUTION_MANDATE_ADDENDUM_001.md)** ⭐
- **Bootstrap authorship vs. mechanical execution clarification**
- Reaffirms base mandate remains active and binding
- Explicit: FM authors all content, proxy executes mechanically only
- Ripple Intelligence responsibilities confirmed for FM execution planning
- Zero contradictions verified between mandate, agent contract, and bootstrap loop
- **Addendum is as binding as base mandate**

### Red Gate Ownership

**[policies/RED_GATE_AUTHORITY_AND_OWNERSHIP.md](policies/RED_GATE_AUTHORITY_AND_OWNERSHIP.md)**
- Red gate declarant authority by gate type
- Red gate ownership responsibilities
- Build stop authority clarification
- Red gate resolution procedures
- FM behavior requirements (FM-BEHAV-1)
- Prohibition enforcement

### Governance Policy Sync

**[workflows/GOVERNANCE_POLICY_SYNC_SPECIFICATION.md](workflows/GOVERNANCE_POLICY_SYNC_SPECIFICATION.md)**
- Canonical governance source of truth
- Synchronization workflow (manual + future automated)
- Sync artifact types (mirrors, adoption docs, enforcement, agent contracts)
- Drift detection and prevention
- Escalation for canon conflicts
- Upward ripple (FM lessons to canon)

### Governance Alignment (Canonical References)

**NEW - [alignment/AGENT_ROLE_GATE_APPLICABILITY_REFERENCE.md](alignment/AGENT_ROLE_GATE_APPLICABILITY_REFERENCE.md)**
- **Canonical Reference** to `maturion-foreman-governance/AGENT_ROLE_GATE_APPLICABILITY.md`
- Defines agent-role-based gate applicability (not path-based)
- Ensures FM workflows respect agent role as sole determinant
- Implements predictability invariant

**NEW - [alignment/PR_GATE_RELEASE_CHECKLISTS_REFERENCE.md](alignment/PR_GATE_RELEASE_CHECKLISTS_REFERENCE.md)**
- **Canonical Reference** to PR Gate Release Checklists
- Ensures FM gates enforce checklists only (no additional requirements)
- Implements: "If all checklist items satisfied, gate MUST pass"

**[alignment/TWO_GATEKEEPER_MODEL.md](alignment/TWO_GATEKEEPER_MODEL.md)**
- Defines dual gatekeeper authority structure
- Gatekeeper 1: Governance Administrator
- Gatekeeper 2: FM Builder
- Both defer to canonical governance

**[alignment/AGENT_SCOPED_QA_BOUNDARIES.md](alignment/AGENT_SCOPED_QA_BOUNDARIES.md)**
- Enforces strict agent QA separation
- Builder QA by builders only
- Governance QA by governance agents only
- FM QA by FM agents only

**[alignment/PR_GATE_REQUIREMENTS_CANON.md](alignment/PR_GATE_REQUIREMENTS_CANON.md)**
- Canonical gate semantics
- READY/NOT_READY declarations
- Enforcement-only validation

**[alignment/PR_GATE_FAILURE_HANDLING_PROTOCOL.md](alignment/PR_GATE_FAILURE_HANDLING_PROTOCOL.md)**
- Canonical failure classifications
- Escalation semantics
- Emergency authorization constraints

**[alignment/GOVERNANCE_RIPPLE_COMPATIBILITY.md](alignment/GOVERNANCE_RIPPLE_COMPATIBILITY.md)**
- Downward ripple: Canon → FM
- Upward ripple: FM lessons → Canon
- Evolution without hard-coded assumptions

**[alignment/FM_REPOSITORY_QA_CLARIFICATION.md](alignment/FM_REPOSITORY_QA_CLARIFICATION.md)**
- FM tests orchestration/enforcement/monitoring
- Not ISMS module implementation

**[alignment/GOVERNANCE_ALIGNMENT_SUMMARY.md](alignment/GOVERNANCE_ALIGNMENT_SUMMARY.md)**
- Complete alignment status
- Evidence of canonical principle implementation
- Update log

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

## Two-Gatekeeper Model (Canonical Alignment)

**Status**: Active and Enforced  
**Authority**: Corporate Governance Canon  
**Last Updated**: 2025-12-22

FM governance operates under a **dual gatekeeper model** where:

### Gatekeeper 1: Governance Administrator (Agent-Level)
- **Role**: Validate governance artifacts and schemas
- **Scope**: Governance compliance, canonical alignment, drift detection
- **Authority**: Read-only on Builder QA results
- **Prohibitions**: NO Builder QA execution, NO implementation defect discovery

### Gatekeeper 2: Foreman App Builder (FM Runtime Layer)
- **Role**: Orchestrate enforcement workflows
- **Scope**: Aggregate governance signals, enforce merge eligibility
- **Authority**: Enforcement only, no override
- **Prohibitions**: NO governance rule interpretation, NO canonical gate weakening

**Neither gatekeeper may override the other.**  
**Both defer to canonical governance.**

See: [Two-Gatekeeper Model](alignment/TWO_GATEKEEPER_MODEL.md)

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

## Canonical Governance Alignment (Critical)

**Status**: Active and Enforced  
**Date Aligned**: 2025-12-22  
**Authority**: Corporate Governance Canon

FM governance has been aligned with the finalized and **GREEN** governance canon. The following canonical specifications define FM enforcement behavior:

### Core Alignment Specifications

1. **[PR Gate Requirements (Canonical Mirror)](alignment/PR_GATE_REQUIREMENTS_CANON.md)**
   - Builder QA Reports as sole source of truth
   - PR gates as enforcement-only (no CI-discovery)
   - Canonical failure classifications
   - Gate semantics and requirements

2. **[Agent-Scoped QA Boundaries](alignment/AGENT_SCOPED_QA_BOUNDARIES.md)**
   - Builder QA by Builder agents only
   - Governance QA by Governance agents only
   - FM QA by FM agents only
   - Cross-agent QA = catastrophic violation

3. **[Two-Gatekeeper Model](alignment/TWO_GATEKEEPER_MODEL.md)**
   - Gatekeeper 1: Governance Administrator (governance artifacts)
   - Gatekeeper 2: FM Builder (Builder QA enforcement)
   - Neither overrides the other
   - Both defer to canonical governance

4. **[PR Gate Failure Handling Protocol](alignment/PR_GATE_FAILURE_HANDLING_PROTOCOL.md)**
   - Canonical failure categories
   - Failure classification semantics
   - Escalation protocols
   - Emergency override rules

5. **[Governance Ripple Compatibility](alignment/GOVERNANCE_RIPPLE_COMPATIBILITY.md)**
   - Downward ripple: Canon → FM (automatic propagation)
   - Upward ripple: FM → Canon (lesson learned promotion)
   - No hard-coded assumptions
   - Version compatibility support

### Explicit Prohibitions

FM governance enforcement MUST NOT:
- ❌ Reintroduce CI-discovery logic
- ❌ Duplicate PR gate enforcement
- ❌ Reinterpret governance intent
- ❌ Perform Builder QA
- ❌ Act as alternative authority

Any such behavior is a governance violation.

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
