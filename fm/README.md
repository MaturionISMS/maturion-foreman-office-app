# FM (Foreman) — Operational Memory & Orchestration

**Status**: Scaffolding Complete (Empty)  
**Phase**: 3A — Memory Scaffolding  
**Last Updated**: 2025-12-23

---

## Purpose

This directory contains the **operational memory and orchestration structures** for Maturion Foreman (FM), the permanent AI Foreman and Platform Agent for the Maturion ISMS ecosystem.

**Critical Distinction**:
- **Governance canon** lives in the `maturion-foreman-governance` repository (read-only, authoritative)
- **FM operational memory** (this directory) stores execution decisions, build history, and orchestration state
- **FM does NOT redefine or duplicate governance** — it consumes and executes it

---

## Directory Structure

```
fm/
├── README.md                       # This file
├── memory/                         # Operational memory (build history, decisions, regressions)
│   ├── build-history/             # Historical build execution records
│   ├── wave-status/               # Wave execution status and outcomes
│   ├── regressions/               # Regression tracking and resolution
│   ├── decisions/                 # Execution decisions and rationales
│   ├── cost-efficiency/           # Cost and efficiency metrics
│   └── README.md                  # Memory structure explanation
├── orchestration/                 # Build orchestration and coordination
│   ├── wave-plans/                # Wave-based execution plans
│   ├── builder-assignments/       # Builder agent task assignments
│   ├── qa-oversight/              # QA oversight and validation tracking
│   └── README.md                  # Orchestration explanation
├── governance/                    # Governance consumption (references only)
│   ├── GOVERNANCE_INDEX.md        # Links to canonical governance
│   └── README.md                  # Governance consumption rules
└── reports/                       # Execution reports and summaries
    └── README.md                  # Report structure and purpose
```

---

## What Lives Here

### Operational Memory (`memory/`)
- Build execution history
- Wave completion status
- Regression tracking and fixes
- Execution decisions and context
- Cost and efficiency data

### Orchestration State (`orchestration/`)
- Active wave plans
- Builder agent assignments
- Task distribution records
- QA oversight status

### Governance References (`governance/`)
- Links to canonical governance documents
- No duplicated governance content
- Read-only consumption model

### Execution Reports (`reports/`)
- Build cycle summaries
- Wave validation reports
- QA oversight reports
- Compliance status snapshots

---

## What Does NOT Live Here

This directory MUST NOT contain:
- ❌ Canonical governance definitions (those live in `maturion-foreman-governance`)
- ❌ Module implementation code (those live in module repositories)
- ❌ Builder agent specifications (those live in `/foreman/builder/`)
- ❌ Historical backlog content (will be selectively migrated in Phase 3B)

---

## Memory Principles

### 1. Append-Only Memory
- Memory is added, never rewritten
- Historical context is preserved
- Decisions are recorded with rationale

### 2. Operational vs. Canonical
- **Canonical memory** = Governance rules, architecture standards, compliance specs (upstream)
- **Operational memory** = Build history, execution decisions, wave status (here)

### 3. Governance Supremacy
- FM consumes governance as read-only
- FM never modifies or redefines governance
- All governance authority flows from canonical sources

### 4. Zero Loss of Context
- Execution context is preserved
- Decisions include rationale
- Regressions are tracked to resolution

---

## Current State

**Phase 3A Complete**: Structure is scaffolded and empty  
**Next Phase**: Phase 3B — Controlled Memory Migration & Backlog Ingestion

This structure is ready to receive operational memory but contains no historical content yet.

---

## Relationship to Other Directories

### `/foreman/` Directory
- Contains builder specifications, identity, and roles
- Defines FM's governance and execution responsibilities
- Lives alongside FM operational memory

### `/governance/` Directory (Repository Root)
- Contains FM-specific governance adoption scaffolding
- Explains how FM adopts canonical governance
- Does not duplicate canonical governance

### `/memory/` Directory (Repository Root)
- Contains legacy memory structures from previous phases
- Being superseded by this FM memory structure
- May be consolidated in future phases

---

## Authority Flow

```
Canonical Governance (maturion-foreman-governance)
            ↓
    FM Governance Index (fm/governance/)
            ↓
FM Execution Decisions (fm/memory/decisions/)
            ↓
   Build Orchestration (fm/orchestration/)
            ↓
  Execution Outcomes (fm/memory/build-history/)
```

---

## References

- **Canonical Governance**: https://github.com/MaturionISMS/maturion-foreman-governance
- **FM Identity**: `/foreman/identity.md`
- **FM Roles & Duties**: `/foreman/roles-and-duties.md`
- **Build Philosophy**: `/BUILD_PHILOSOPHY.md`
- **Governance Adoption**: `/governance/policies/FM_GOVERNANCE_ADOPTION_POLICY.md`

---

*FM Operational Memory & Orchestration — Foundation for Execution Reality*
