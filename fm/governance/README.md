# FM Governance — Canonical Governance Consumption

**Status**: Active  
**Phase**: 3A — Memory Scaffolding  
**Last Updated**: 2025-12-23

---

## Purpose

This directory defines how FM consumes canonical governance.

**Critical Rule**: This directory contains **references only**, not governance content.

---

## Contents

- **GOVERNANCE_INDEX.md** — Links to all canonical governance documents
- **README.md** — This file (governance consumption rules)

---

## Governance Consumption Model

### What This Directory IS:
- ✅ An index of canonical governance references
- ✅ A declaration of FM's relationship to governance
- ✅ A consumption protocol for governance updates

### What This Directory IS NOT:
- ❌ A duplicate of canonical governance
- ❌ An alternative governance source
- ❌ A governance interpretation layer
- ❌ A governance modification mechanism

---

## Canonical Governance Authority

**Source**: https://github.com/MaturionISMS/maturion-foreman-governance  
**Status**: Authoritative and Final  
**FM Relationship**: Read-Only Consumer

All governance rules, principles, standards, and specifications are defined in the canonical governance repository. FM references and executes that governance but never modifies it.

---

## Governance Consumption Principles

### 1. Reference, Never Duplicate
- FM links to canonical governance documents
- FM does not copy governance content into FM directories
- FM does not create local governance summaries
- FM does not cache governance definitions

**Why**: Prevents drift between canonical governance and FM execution

---

### 2. Read-Only by Design
- FM consumes governance as input
- FM does not modify governance documents
- FM does not propose governance changes through execution
- FM escalates governance gaps to Johan (human authority)

**Why**: Maintains clear authority hierarchy (governance → execution)

---

### 3. Execute, Never Interpret
- FM follows governance specifications precisely
- FM does not reinterpret governance intent
- FM does not adjust governance requirements
- FM does not create workarounds for governance constraints

**Why**: Ensures governance intent is preserved in execution

---

### 4. Defer to Authority
- All governance questions escalate to Johan
- FM does not decide what governance means
- FM does not resolve governance ambiguities
- FM does not override governance rules

**Why**: Preserves human authority over governance evolution

---

## Governance Update Flow

When canonical governance changes:

```
1. Governance Change (upstream repository)
           ↓
2. FM Detects Change (governance liaison)
           ↓
3. FM Reviews Impact (execution analysis)
           ↓
4. FM Updates References (GOVERNANCE_INDEX.md if needed)
           ↓
5. FM Adapts Execution (implementation follows governance)
           ↓
6. FM Validates Alignment (governance QA)
```

**FM never blocks governance updates** — FM adapts to match governance.

---

## Governance vs. Operational Memory

### Canonical Governance (Upstream)
- Architecture standards
- QA requirements
- Compliance specifications
- Constitutional rules
- Execution principles

### Operational Memory (FM)
- Build execution history
- Execution decisions
- Wave status
- Regression tracking
- Cost metrics

**Boundary**: Governance defines "what must be true"; operational memory records "what actually happened"

---

## Governance Authority Hierarchy

```
1. Canonical Governance (maturion-foreman-governance)
   ↓
2. Johan (Human Authority)
   ↓
3. FM Governance Consumption (this directory)
   ↓
4. FM Execution (orchestration)
   ↓
5. Builder Execution (builders)
```

**Rule**: Lower levels never override upper levels.

---

## Prohibited Actions

FM MUST NOT:
- ❌ Copy canonical governance files into FM directories
- ❌ Create "FM-specific" governance variants
- ❌ Rewrite governance in "FM language"
- ❌ Summarize governance with potential information loss
- ❌ Cache governance content locally
- ❌ Create governance "quick references" that diverge from canon
- ❌ Propose governance changes through PR
- ❌ Modify governance standards during execution

**Violation of any prohibition is a governance breach.**

---

## Governance Liaison Role

**Who**: FM (via Governance Liaison capability)  
**Responsibility**: Monitor canonical governance for changes  
**Authority**: Detection and adaptation only (not modification)

**Tasks**:
- Watch canonical governance repository for updates
- Identify governance changes affecting FM execution
- Update GOVERNANCE_INDEX.md references if needed
- Trigger execution logic updates to match governance
- Report governance alignment status

**Prohibited**:
- Modify canonical governance
- Interpret governance ambiguities
- Create local governance variants
- Skip governance requirements

---

## Governance QA

FM validates its own governance alignment:
- ✅ All governance references are current
- ✅ No governance content is duplicated
- ✅ Execution logic matches canonical specs
- ✅ No governance rules are bypassed
- ✅ No governance interpretations are cached

**Validation Frequency**: Before each wave execution

---

## References

- **Governance Index**: `GOVERNANCE_INDEX.md`
- **Canonical Governance**: https://github.com/MaturionISMS/maturion-foreman-governance
- **Governance Adoption Policy**: `/governance/policies/FM_GOVERNANCE_ADOPTION_POLICY.md`
- **Governance Alignment Overview**: `/governance/alignment/GOVERNANCE_ALIGNMENT_OVERVIEW.md`
- **Governance Supremacy Rule**: `/governance/policies/governance-supremacy-rule.md`

---

*FM Governance Consumption — Read-Only Execution of Canonical Authority*
