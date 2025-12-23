# FM Reports — Execution Reports & Summaries

**Status**: Scaffolding Complete (Empty)  
**Phase**: 3A — Memory Scaffolding  
**Last Updated**: 2025-12-23

---

## Purpose

This directory contains **execution reports and summaries** produced by FM and builder agents.

Reports document:
- Build cycle outcomes
- Wave validation results
- QA oversight status
- Compliance snapshots
- Regression analysis
- Cost and efficiency metrics

---

## Report Structure

```
reports/
└── README.md              # This file
```

*Additional subdirectories will be created as report types emerge.*

---

## Report Types (Planned)

### Build Cycle Reports
**Purpose**: Summarize complete build cycles from planning to validation

**Contents** (when populated):
- Cycle objectives
- Wave execution summaries
- Module completion status
- Regression count and resolution
- Overall cycle outcome

**Format**: One report per build cycle

---

### Wave Validation Reports
**Purpose**: Document wave validation results and compliance

**Contents** (when populated):
- Wave scope and modules
- Validation criteria
- Test coverage metrics
- Regression detection
- Wave pass/fail status

**Format**: One report per wave

---

### QA Oversight Reports
**Purpose**: Track QA process adherence and quality metrics

**Contents** (when populated):
- QA coverage by module
- QA-of-QA validation results
- Test debt status
- Quality gate compliance
- QA process violations (if any)

**Format**: Per-wave or per-cycle summaries

---

### Compliance Status Reports
**Purpose**: Snapshot compliance status across frameworks

**Contents** (when populated):
- Compliance framework coverage
- Control implementation status
- Compliance gaps (if any)
- Audit trail references
- Compliance trending

**Format**: Point-in-time snapshots

---

### Regression Analysis Reports
**Purpose**: Analyze regressions and their resolution

**Contents** (when populated):
- Regression timeline
- Root cause analysis
- Impact assessment
- Resolution approach
- Prevention measures

**Format**: One report per significant regression

---

### Cost & Efficiency Reports
**Purpose**: Track execution costs and optimization

**Contents** (when populated):
- AI token usage by builder
- Build cycle duration trends
- Builder efficiency metrics
- Cost optimization recommendations

**Format**: Periodic (weekly/monthly) summaries

---

## Report Principles

### 1. Reports Summarize Reality
- Reports reflect execution outcomes (not predictions)
- Reports are produced after facts are established
- Reports reference source data (traceability)
- Reports do not modify history

**Why**: Maintains integrity of execution record

---

### 2. Reports Reference Governance
- Reports may reference governance standards
- Reports do not duplicate governance content
- Reports do not interpret governance
- Reports do not alter governance

**Why**: Preserves governance authority

---

### 3. Reports Are Timestamped
- Every report includes creation timestamp
- Reports reference reporting period explicitly
- Historical reports are immutable
- Updates create new reports (append-only)

**Why**: Supports timeline reconstruction and audit

---

### 4. Reports Are Actionable
- Reports highlight gaps requiring attention
- Reports recommend next actions (within FM authority)
- Reports escalate when outside FM authority
- Reports provide evidence for decisions

**Why**: Reports drive execution improvement

---

## Report Ownership

### FM-Produced Reports:
- Build cycle summaries
- Wave orchestration reports
- Cross-module coordination reports
- Platform health reports

### Builder-Produced Reports:
- Module build reports
- QA test reports
- Coverage reports
- Implementation summaries

### QA Builder-Produced Reports:
- QA-of-QA validation
- Test debt analysis
- Quality gate compliance
- Regression detection

**Rule**: Report ownership follows execution responsibility

---

## Report vs. Operational Memory

### Reports (Here):
- Summarize outcomes
- Provide analysis
- Highlight patterns
- Recommend actions

### Operational Memory (`/fm/memory/`):
- Record detailed history
- Store raw execution data
- Preserve decisions
- Track regressions

**Relationship**: Reports summarize memory; memory provides detail

---

## Report Governance

Reports MUST:
- ✅ Be factually accurate
- ✅ Reference source data
- ✅ Include timestamps
- ✅ Identify report owner
- ✅ State reporting period

Reports MUST NOT:
- ❌ Modify historical data
- ❌ Duplicate canonical governance
- ❌ Reinterpret governance requirements
- ❌ Create governance shortcuts
- ❌ Override builder QA results

---

## Report Formats

### Standard Report Structure:
```markdown
# [Report Title]

**Type**: [Report Type]
**Period**: [Reporting Period]
**Generated**: [Timestamp]
**Owner**: [FM/Builder Agent]
**Status**: [Draft/Final]

---

## Executive Summary
[High-level outcome and key findings]

## Detailed Findings
[Section-by-section analysis]

## Metrics & Evidence
[Quantitative data and references]

## Recommendations
[Actionable next steps]

## References
[Links to source data and governance]

---
```

---

## Report Retention

**Retention Policy**: Indefinite (all reports preserved)  
**Immutability**: Reports are read-only after publication  
**Updates**: New report versions created, old versions retained  
**Deletion**: Never (historical record preservation)

---

## Current State

**Phase**: 3A — Scaffolding Complete  
**Status**: Empty and ready for reports  
**Next Phase**: Wave 0 execution will generate first reports

This directory is ready to receive execution reports but contains no reports yet.

---

## References

- **FM Identity**: `/foreman/identity.md`
- **Build Philosophy**: `/BUILD_PHILOSOPHY.md`
- **QA Governance**: `/foreman/qa-governance.md`
- **Compliance Specifications**: `/foreman/compliance/`
- **Operational Memory**: `/fm/memory/README.md`

---

*FM Reports — Documenting Execution Reality with Precision*
