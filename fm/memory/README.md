# FM Memory — Operational Execution Memory

**Status**: Scaffolding Complete (Empty)  
**Phase**: 3A — Memory Scaffolding  
**Last Updated**: 2025-12-23

---

## Purpose

This directory stores **operational execution memory** for Maturion Foreman (FM).

This is where FM records:
- What was built and when
- What decisions were made and why
- What regressions occurred and how they were resolved
- What waves were executed and their outcomes
- What costs were incurred and efficiency metrics

---

## Memory Structure

```
memory/
├── README.md              # This file
├── build-history/         # Historical build execution records
├── wave-status/           # Wave execution status and outcomes
├── regressions/           # Regression tracking and resolution
├── decisions/             # Execution decisions and rationales
└── cost-efficiency/       # Cost and efficiency metrics
```

---

## Memory Types

### Build History (`build-history/`)
**Purpose**: Record what was built, when, and by whom

**Contents** (when populated):
- Build execution logs
- Module build records
- Builder agent activity logs
- Build cycle summaries

**Format**: Append-only, timestamped records

---

### Wave Status (`wave-status/`)
**Purpose**: Track wave-based execution progress and outcomes

**Contents** (when populated):
- Wave plans and actual execution
- Wave validation results
- Wave completion status
- Cross-wave dependencies

**Format**: One record per wave, updated through lifecycle

---

### Regressions (`regressions/`)
**Purpose**: Track when things break and how they're fixed

**Contents** (when populated):
- Regression reports
- Root cause analysis
- Fix implementation records
- Prevention measures

**Format**: One record per regression, closed when resolved

---

### Decisions (`decisions/`)
**Purpose**: Record execution decisions and their rationale

**Contents** (when populated):
- Architectural decisions (execution-level)
- Builder selection rationale
- Task prioritization decisions
- Exception handling decisions

**Format**: Decision records with context, options, and rationale

---

### Cost Efficiency (`cost-efficiency/`)
**Purpose**: Track execution costs and efficiency metrics

**Contents** (when populated):
- AI token usage
- Build cycle durations
- Builder efficiency metrics
- Cost optimization decisions

**Format**: Timestamped metrics and analysis

---

## Critical Distinctions

### Operational Memory vs. Canonical Memory

**Operational Memory (Here)**:
- Build execution history
- Execution decisions
- Wave status
- Regressions and fixes
- Cost metrics

**Canonical Memory (Governance Repository)**:
- Governance rules and principles
- Architecture standards
- QA requirements
- Compliance specifications
- Constitutional rules

**Rule**: FM operational memory references canonical memory but never duplicates it.

---

## Memory Principles

### 1. Append-Only by Design
- Memory is added over time, never rewritten
- Historical records are immutable once closed
- Updates append new context, don't replace old

**Why**: Preserves execution history and prevents loss of context

---

### 2. Started Empty by Design
- This directory starts completely empty
- No historical content is migrated in Phase 3A
- Memory will be populated incrementally in Phase 3B

**Why**: Prevents uncontrolled memory migration and preserves governance authority

---

### 3. Context Preservation
- Every memory entry includes timestamp
- Decisions include rationale and alternatives considered
- Regressions include root cause and resolution
- Build records include builder and inputs

**Why**: Supports Zero Loss of Context principle (Build Philosophy)

---

### 4. Operational Only
- This memory does not define governance
- This memory does not create architecture standards
- This memory does not set QA requirements
- This memory records execution reality

**Why**: Maintains separation between governance (upstream) and execution (here)

---

## Future Memory Ingestion (Phase 3B)

When operational memory is migrated from backlog and archives:

**Sources**:
- Historical build cycle summaries
- Wave validation reports
- Regression tracking from issues
- Execution decisions from PR comments
- Cost metrics from build logs

**Process**:
- Selective extraction (relevant context only)
- Structured formatting (consistent schema)
- Timestamped entries (preserve timeline)
- Cross-referenced records (maintain relationships)

**Prohibited**:
- Bulk copying of unstructured content
- Duplication of canonical governance
- Rewriting of historical decisions
- Loss of original context

---

## Current State

**Phase**: 3A — Scaffolding Complete  
**Status**: Empty and ready to receive memory  
**Next Phase**: 3B — Controlled Memory Migration

All subdirectories exist but contain no files yet.

---

## Memory Authority

FM operational memory:
- Records execution reality (what happened)
- Documents decisions made (why it happened)
- Tracks outcomes (what resulted)

FM operational memory does NOT:
- Define governance rules
- Set architecture standards
- Create QA requirements
- Override canonical specifications

**Authority flows from governance to execution, never reverse.**

---

## References

- **Build Philosophy**: `/BUILD_PHILOSOPHY.md`
- **FM Identity**: `/foreman/identity.md`
- **Governance Index**: `/fm/governance/GOVERNANCE_INDEX.md`
- **Memory Model**: `/governance/policies/memory-model.md`

---

*FM Operational Memory — Recording Execution Reality*
