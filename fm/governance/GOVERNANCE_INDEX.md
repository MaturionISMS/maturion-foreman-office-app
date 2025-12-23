# FM Governance Index — Canonical Governance References

**Status**: Active  
**Phase**: 3A — Memory Scaffolding  
**Last Updated**: 2025-12-23

---

## Purpose

This document provides **read-only references** to canonical governance that FM consumes and executes.

**Critical Rule**: FM does NOT duplicate, modify, or redefine governance. This index links to authoritative sources only.

---

## Canonical Governance Repository

**Authority**: Maturion ISMS Governance Canon  
**Location**: https://github.com/MaturionISMS/maturion-foreman-governance  
**Status**: Authoritative and Final

All governance rules, principles, standards, and specifications are defined in the canonical governance repository.

---

## Core Governance Documents

### Vision & Principles

**Build Philosophy**  
**Location**: `/BUILD_PHILOSOPHY.md` (FM App Repository)  
**Status**: Canonical  
**Purpose**: Defines One-Time Build Correctness, Zero Regression, and core execution principles

**FM Identity**  
**Location**: `/foreman/identity.md` (FM App Repository)  
**Purpose**: Defines who FM is and FM's role in the ecosystem

**FM Roles & Duties**  
**Location**: `/foreman/roles-and-duties.md` (FM App Repository)  
**Purpose**: Defines FM's responsibilities and boundaries

---

## Architecture Governance

**Minimum Architecture Template**  
**Location**: `/foreman/minimum-architecture-template.md` (FM App Repository)  
**Purpose**: Defines mandatory architecture artifact structure

**Architecture Validation Checklist**  
**Location**: `/foreman/architecture-validation-checklist.md` (FM App Repository)  
**Purpose**: Defines validation criteria for architecture compliance

**Architecture Naming Conventions**  
**Location**: `/foreman/architecture-naming-conventions.md` (FM App Repository)  
**Purpose**: Defines naming standards for architecture artifacts

**Architecture Folder Structure**  
**Location**: `/foreman/architecture-folder-structure.md` (FM App Repository)  
**Purpose**: Defines directory structure for architecture documentation

**Versioning Rules**  
**Location**: `/foreman/versioning-rules.md` (FM App Repository)  
**Purpose**: Defines version numbering and compatibility rules

---

## QA Governance

**QA Governance**  
**Location**: `/foreman/qa-governance.md` (FM App Repository)  
**Purpose**: Defines QA standards, requirements, and responsibilities

**QA Minimum Coverage Requirements**  
**Location**: `/foreman/qa-minimum-coverage-requirements.md` (FM App Repository)  
**Purpose**: Defines minimum test coverage thresholds

**QA-of-QA Specification**  
**Location**: `/foreman/qa-of-qa.md` (FM App Repository)  
**Purpose**: Defines how QA itself is validated

**Zero Test Debt Constitutional Rule**  
**Location**: `/governance/policies/zero-test-debt-constitutional-rule.md` (FM App Repository)  
**Purpose**: Defines zero test debt as unbreakable law

---

## Compliance Governance

**Compliance Reference Map**  
**Location**: `/foreman/compliance/compliance-reference-map.md` (FM App Repository)  
**Purpose**: Maps compliance frameworks to ISMS modules

**Compliance Control Library**  
**Location**: `/foreman/compliance/compliance-control-library.json` (FM App Repository)  
**Purpose**: Defines compliance controls and their requirements

**Compliance QA Specification**  
**Location**: `/foreman/compliance/compliance-qa-spec.md` (FM App Repository)  
**Purpose**: Defines how compliance is validated

**Compliance Watchdog Specification**  
**Location**: `/foreman/compliance/compliance-watchdog-spec.md` (FM App Repository)  
**Purpose**: Defines continuous compliance monitoring

---

## Builder Governance

**Builder Capability Map**  
**Location**: `/foreman/builder/builder-capability-map.json` (FM App Repository)  
**Purpose**: Defines what each builder agent can do

**Builder Permission Policy**  
**Location**: `/foreman/builder/builder-permission-policy.json` (FM App Repository)  
**Purpose**: Defines builder permissions and restrictions

**Builder Collaboration Rules**  
**Location**: `/foreman/builder/builder-collaboration-rules.md` (FM App Repository)  
**Purpose**: Defines how builders work together

**UI Builder Specification**  
**Location**: `/foreman/builder/ui-builder-spec.md` (FM App Repository)

**API Builder Specification**  
**Location**: `/foreman/builder/api-builder-spec.md` (FM App Repository)

**Schema Builder Specification**  
**Location**: `/foreman/builder/schema-builder-spec.md` (FM App Repository)

**Integration Builder Specification**  
**Location**: `/foreman/builder/integration-builder-spec.md` (FM App Repository)

**QA Builder Specification**  
**Location**: `/foreman/builder/qa-builder-spec.md` (FM App Repository)

---

## Privacy & Security Governance

**Memory Model**  
**Location**: `/governance/policies/memory-model.md` (FM App Repository)  
**Purpose**: Defines memory isolation and tenant boundaries

**Privacy Guardrails**  
**Location**: `/governance/policies/privacy-guardrails.md` (FM App Repository)  
**Purpose**: Defines privacy protections and data isolation rules

**Security Escalation Policy**  
**Location**: `/governance/policies/security-escalation-policy.md` (FM App Repository)  
**Purpose**: Defines security incident handling

---

## Change Management Governance

**Design Freeze Rule**  
**Location**: `/governance/policies/design-freeze-rule.md` (FM App Repository)  
**Purpose**: Defines when designs are frozen and immutable

**Change Policy**  
**Location**: `/governance/policies/change-policy.md` (FM App Repository)  
**Purpose**: Defines how changes are proposed, reviewed, and approved

**Governance Supremacy Rule**  
**Location**: `/governance/policies/governance-supremacy-rule.md` (FM App Repository)  
**Purpose**: Defines governance authority hierarchy

---

## Platform Governance

**Platform Awareness**  
**Location**: `/foreman/platform-awareness.md` (FM App Repository)  
**Purpose**: Defines platform responsibilities and boundaries

**Runtime Agent Plan**  
**Location**: `/foreman/runtime-agent-plan.md` (FM App Repository)  
**Purpose**: Defines future runtime agent capabilities

**QA Dashboard Specification**  
**Location**: `/foreman/platform/qa-dashboard-spec.md` (FM App Repository)

**Governance QA Dashboard Specification**  
**Location**: `/foreman/platform/governance-qa-dashboard-spec.md` (FM App Repository)

**Compliance Dashboard Specification**  
**Location**: `/foreman/compliance/compliance-dashboard-spec.md` (FM App Repository)

---

## Execution Doctrine

**Command Grammar**  
**Location**: `/foreman/command-grammar.md` (FM App Repository)  
**Purpose**: Defines how Johan and agents communicate

**Task Distribution Rules**  
**Location**: `/foreman/task-distribution-rules.md` (FM App Repository)  
**Purpose**: Defines how tasks are assigned to builders

**Context Awareness**  
**Location**: `/foreman/context-awareness.md` (FM App Repository)  
**Purpose**: Defines how FM maintains execution context

---

## Governance Consumption Rules

### FM MUST:
1. **Reference governance via links** — Never duplicate canonical content
2. **Treat governance as read-only** — Never modify governance documents
3. **Consume governance as authoritative** — Never reinterpret governance intent
4. **Defer to governance for law** — All rules come from governance
5. **Execute governance precisely** — Build to canonical specifications

### FM MUST NOT:
1. ❌ **Copy governance content into FM directories**
2. ❌ **Rewrite or summarize governance documents**
3. ❌ **Modify governance standards or requirements**
4. ❌ **Create alternative governance interpretations**
5. ❌ **Store canonical specifications in operational memory**

---

## Authority Flow

```
Canonical Governance (maturion-foreman-governance)
            ↓
    Governance Index (this document)
            ↓
   FM Execution Logic (FM orchestration)
            ↓
  Builder Execution (builder agents)
            ↓
    Validation (QA builder)
            ↓
 Operational Memory (FM memory)
```

**Rule**: Authority flows downward only. Execution never overrides governance.

---

## Governance Alignment Statement

**Declaration**: FM consumes governance; FM does not create governance.

FM's relationship to governance is:
- **Consumer** (not creator)
- **Executor** (not interpreter)
- **Enforcer** (not definer)
- **Reporter** (not judge)

All governance authority resides in canonical governance documents. FM implements governance-defined requirements with precision and fidelity.

---

## Governance Update Protocol

When canonical governance changes:

1. **FM detects change** (via governance liaison role)
2. **FM reviews impact** (what execution logic is affected)
3. **FM updates references** (this index, if needed)
4. **FM adapts execution** (implementation follows governance)
5. **FM validates alignment** (governance QA dashboard)

**FM never questions governance changes** — FM adapts execution to match.

---

## References

- **Canonical Governance Repository**: https://github.com/MaturionISMS/maturion-foreman-governance
- **Governance Adoption Policy**: `/governance/policies/FM_GOVERNANCE_ADOPTION_POLICY.md`
- **Governance Alignment Overview**: `/governance/alignment/GOVERNANCE_ALIGNMENT_OVERVIEW.md`
- **Two-Gatekeeper Model**: `/governance/alignment/TWO_GATEKEEPER_MODEL.md`

---

*FM Governance Index — Read-Only Consumption of Canonical Authority*
