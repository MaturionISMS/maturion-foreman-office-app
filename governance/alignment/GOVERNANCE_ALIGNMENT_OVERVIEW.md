# FM Governance Alignment Overview

**Status**: Foundation  
**Last Updated**: 2025-12-22  
**Authority**: Johan Ras

---

## I. Constitutional Statement

**The FM repository adopts, executes, and enforces corporate governance canon.**

**The FM repository does NOT:**
- Create governance
- Redefine governance
- Reinterpret governance
- Weaken governance

**All governance authority flows from the corporate governance canon**, maintained in the `maturion-foreman-governance` repository.

---

## II. Governance Source of Truth

### Corporate Governance Canon Location

**Repository**: `maturion-foreman-governance`  
**URL**: https://github.com/MaturionISMS/maturion-foreman-governance

### What Lives There

1. **Constitutional Rules**
   - Governance Supremacy Rule (GSR)
   - Zero Test Debt Constitutional Rule
   - Design Freeze Rule
   - DP-RED Policy

2. **Architecture Standards**
   - Minimum Architecture Template
   - Architecture Validation Checklist
   - Architecture Naming Conventions
   - Architecture Folder Structure
   - Versioning Rules

3. **QA Governance**
   - QA Governance Specification
   - QA-of-QA Requirements
   - QA Minimum Coverage Requirements
   - Quality Integrity Contract

4. **Compliance**
   - Compliance Reference Map
   - Compliance Control Library
   - Compliance QA Specification
   - Compliance Watchdog Specification

5. **Build Enforcement**
   - Build-to-Green Enforcement Specification
   - Foreman Execution State Model
   - Task Distribution Rules

6. **All Other Governance Artifacts**
   - Innovation specs, survey specs, admin specs
   - Platform specs, runtime specs, test specs
   - Dashboard specs, contracts, templates

---

## III. FM Repository Role

### What FM Repository Contains

1. **Governance Adoption Framework** (this directory)
   - How FM adopts corporate governance
   - How governance rules become execution constraints
   - Agent role definitions
   - Scope discipline

2. **Governance Enforcement Mechanisms**
   - PR gate workflows (GitHub Actions)
   - Build-to-green enforcement
   - Architecture validation gates
   - Agent state validation

3. **Builder Specifications**
   - FM Builder agent spec (executes builds)
   - Governance Liaison spec (monitors governance)
   - Future FM Agent spec (mechanizes enforcement)

4. **Execution Artifacts**
   - Builder orchestration scripts
   - Validation tools
   - Evidence collection
   - FM Office automation (future)

---

## IV. Agent Roles

### 1. Governance Liaison (FM-Scoped)

**Role**: Monitor and translate corporate governance into FM execution requirements

**Responsibilities**:
- Watch for changes in `maturion-foreman-governance` repository
- Translate new or updated governance into FM execution constraints
- Update PR gates to reflect governance changes
- Ensure FM execution remains aligned with governance canon
- Escalate governance ambiguities to Johan Ras

**Boundaries**:
- ❌ Does NOT create governance
- ❌ Does NOT modify governance meaning
- ❌ Does NOT override governance
- ✅ DOES translate governance into actionable execution constraints
- ✅ DOES ensure FM remains aligned

**Authority**: Read-only on governance canon, write access to FM execution configuration

---

### 2. FM Builder

**Role**: Execute build tasks within FM repository under governance constraints

**Responsibilities**:
- Build FM repository components and features
- Comply with all governance constraints from corporate canon
- Build-to-green (no handover until all PR gates are green)
- Provide evidence of governance compliance
- Escalate when governance constraints cannot be met

**Boundaries**:
- ❌ Does NOT modify governance
- ❌ Does NOT disable PR gates
- ❌ Does NOT request temporary overrides
- ❌ Does NOT hand over until green
- ✅ DOES build within governance constraints
- ✅ DOES escalate blockers with proposed solutions

**Authority**: Write access to FM repository code, zero authority over governance

---

### 3. FM Agent (Future Execution Authority)

**Role**: Real-time governance enforcement and FM Office automation

**Status**: Not yet implemented (placeholder for future)

**Planned Responsibilities**:
- Mechanize governance enforcement in real-time
- Provide instant governance feedback during development
- Power FM Office dashboard with live governance state
- Generate audible alerts for governance violations
- Automate evidence collection and compliance reporting

**Planned Boundaries**:
- ❌ Does NOT modify governance canon
- ❌ Does NOT override governance rules
- ✅ DOES enforce governance mechanically
- ✅ DOES provide real-time feedback
- ✅ DOES collect and present evidence

**Authority**: Enforcement and visibility only, zero authority to modify governance

---

## V. Governance Change Flow

### How Governance Changes Propagate

```
1. Corporate Governance Change
   ↓ (in maturion-foreman-governance repo)
   
2. Governance Liaison Detects Change
   ↓ (monitoring upstream)
   
3. Translate to FM Execution Constraints
   ↓ (no interpretation, direct translation)
   
4. Update PR Gates / Enforcement Mechanisms
   ↓ (GitHub Actions, validation scripts)
   
5. FM Builder Operates Under New Constraints
   ↓ (builds to green under updated rules)
   
6. Future: FM Agent Mechanizes New Rule
   ↓ (real-time enforcement in development)
```

### Critical Invariants

1. **Changes originate upstream** - FM never initiates governance changes
2. **No interpretation** - Governance Liaison translates, does not interpret
3. **No weakening** - Translation cannot reduce governance requirements
4. **No delay** - Governance changes apply immediately once translated
5. **No exceptions** - All agents operate under governance without override

---

## VI. Governance Enforcement Layers

### Layer 1: PR Gates (Current Authority)

**Mechanism**: GitHub Actions workflows  
**Status**: Active and authoritative  
**Scope**: All PRs in FM repository

**Gates**:
- Build-to-green enforcement
- FM Architecture Gate (completeness + agent state)
- Test coverage validation (future)
- Compliance validation (future)

**Unbreakable Rule**: No PR merge until all gates are green

---

### Layer 2: Builder Constraints (Current)

**Mechanism**: FM Builder agent contract  
**Status**: Active  
**Scope**: All FM Builder operations

**Constraints**:
- Must build-to-green before handover
- Must provide pre-handover proof (all checks green)
- Must escalate when blocked (no silent stops)
- Must comply with all governance policies

**Unbreakable Rule**: Handover forbidden until CI checks are green

---

### Layer 3: FM Agent Mechanization (Future)

**Mechanism**: Real-time governance enforcement in FM Office  
**Status**: Not yet implemented  
**Scope**: Live development, CI/CD, and runtime

**Planned Capabilities**:
- Instant governance feedback in IDE/editor
- Real-time compliance checking
- Automatic evidence collection
- Dashboard visualization
- Audible alerts for violations

**Goal**: Make governance violations impossible, not just detectable

---

## VII. Scope Discipline Alignment

### Corporate Governance Scope Discipline

Defined in: `maturion-foreman-governance/policies/change-policy.md`

**Rules**:
- One responsibility domain per PR
- Explicit scope declaration required
- No mixed concerns
- Governance changes separate from execution changes

### FM Adoption

FM repository PRs MUST:
1. Declare scope explicitly (see `governance/scope/README.md`)
2. Limit to one responsibility domain
3. Separate governance alignment from execution logic
4. Never mix governance changes with application code

**Enforcement**: PR gate checks for scope declaration and single-domain constraint

---

## VIII. Explicit Prohibitions

FM repository agents and processes are **explicitly forbidden** from:

1. ❌ Creating new governance rules
2. ❌ Modifying governance canon
3. ❌ Reinterpreting governance requirements
4. ❌ Weakening governance constraints
5. ❌ Disabling PR gates
6. ❌ Requesting temporary overrides
7. ❌ Handing over before green
8. ❌ Mixing governance and execution in same PR
9. ❌ Writing to `maturion-foreman-governance` repository

---

## IX. Escalation Paths

### When Governance Blocks FM Work

If FM Builder cannot meet governance constraints:

1. **Document the blocker**
   - What governance constraint blocks progress?
   - What is the root cause?
   - What is the impact?

2. **Propose solutions** (in order of preference)
   - A. Meet governance constraint through different approach
   - B. Request governance clarification (if ambiguous)
   - C. Request bounded temporary override (time-limited)
   - D. Request governance change (upstream, in governance repo)

3. **Escalate to Johan Ras**
   - Provide problem statement
   - Provide solution options
   - Wait for authority decision
   - Do NOT proceed without approval

**Never**: Disable gates, weaken constraints, or hand over in blocked state

---

## X. Success Criteria

FM governance alignment is successful when:

1. ✅ Corporate governance canon is authoritative and unchangeable by FM
2. ✅ Governance changes flow cleanly from upstream to FM execution
3. ✅ PR gates mechanically enforce governance without human interpretation
4. ✅ FM Builder always builds to green before handover
5. ✅ No governance violations occur (prevented, not just detected)
6. ✅ Governance state is visible and auditable at all times
7. ✅ Future FM Agent mechanizes enforcement seamlessly

---

## XI. Future State Vision

### FM Office Integration

When FM Agent is implemented:

- **Real-time governance feedback** in development environment
- **Live compliance dashboard** showing governance state
- **Audible alerts** for governance violations or drift
- **Automatic evidence collection** for audits
- **Predictive governance** (warn before violation occurs)

### Governance Mechanization

Goal: Make incorrect builds **impossible**, not just detectable

- IDE integration prevents non-compliant code
- CI/CD blocks non-compliant changes before commit
- Runtime monitors governance state continuously
- Evidence is collected automatically, not manually

---

## XII. References

- **Corporate Governance Canon**: https://github.com/MaturionISMS/maturion-foreman-governance
- **Build Philosophy**: `/BUILD_PHILOSOPHY.md`
- **FM Builder Contract**: `.github/agents/FMRepoBuilder.yaml`
- **PR Gates**: `.github/workflows/`

---

*FM Governance Alignment - Adoption, Not Creation*
