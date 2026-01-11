# Protocol Violations - Incident Tracking

**Status**: Active Tracking System  
**Authority**: EXECUTION_BOOTSTRAP_PROTOCOL_MONITORING_AND_ENFORCEMENT.md  
**Established**: 2026-01-11  
**First Report Due**: 2026-04-14 (Q2 2026)

---

## Purpose

This directory tracks **all violations** of the Execution Bootstrap Protocol in the maturion-foreman-office-app repository. Incident tracking is **MANDATORY** per canonical governance.

---

## What Constitutes a Violation

A protocol violation occurs when:

1. **No PREHANDOVER_PROOF provided** for PR with execution artifacts (workflows, scripts, gates)
2. **Incomplete 7-step verification** (missing steps, incomplete evidence)
3. **Handover without local execution** (relying on CI for discovery)
4. **Green attestation with failures** (false claim of "all checks green")
5. **Missing evidence** (no logs, no exit codes, no outputs)
6. **Bypassing protocol** (PR merged without proof)
7. **Incomplete remediation** (failures not fixed before handover)

---

## Incident Tracking Process

### Step 1: Detection

Violations may be detected by:
- PR gate enforcement (automated)
- FM review (manual)
- Governance Liaison audit (manual)
- CI failure analysis (post-merge)
- Quarterly monitoring review

### Step 2: Documentation

For each violation, create incident file: `VIOLATION_YYYY_MM_DD_[DESCRIPTION].md`

Use template: `TRACKING_TEMPLATE.md` (in this directory)

### Step 3: Escalation

- **Minor violation** (first occurrence, no impact): Document and monitor
- **Moderate violation** (repeat occurrence, minor impact): Escalate to FM
- **Major violation** (bypass, false attestation, production impact): Escalate to Johan (CS2)

### Step 4: Resolution

- Document root cause
- Document corrective actions
- Document preventive measures
- Update monitoring metrics

### Step 5: Quarterly Reporting

- Aggregate all violations for quarter
- Include in quarterly monitoring report
- Submit to governance repository
- Review effectiveness metrics

---

## Incident File Naming Convention

**Format**: `VIOLATION_YYYY_MM_DD_[SHORT_DESCRIPTION].md`

**Examples**:
- `VIOLATION_2026_01_15_MISSING_PREHANDOVER_PROOF_PR_123.md`
- `VIOLATION_2026_02_03_INCOMPLETE_EVIDENCE_API_BUILDER.md`
- `VIOLATION_2026_03_10_FALSE_GREEN_ATTESTATION_UI_BUILDER.md`

---

## Tracking Metrics

Each quarter, track:

1. **Total violations**: Count of all incidents
2. **Violations by type**: Breakdown by violation category
3. **Violations by agent**: Breakdown by agent role (FM, Builder, etc.)
4. **Severity distribution**: Minor, Moderate, Major counts
5. **Resolution time**: Average time from detection to resolution
6. **Repeat violations**: Incidents by same agent/pattern
7. **Impact assessment**: Production incidents, rework required
8. **Trend analysis**: Increasing, decreasing, stable

---

## Current Status

**Tracking Start Date**: 2026-01-11  
**Current Quarter**: Q1 2026 (2026-01-01 to 2026-03-31)  
**Next Quarter**: Q2 2026 (2026-04-01 to 2026-06-30)  
**First Report Due**: 2026-04-14

**Q1 2026 Status**:
- Total Violations: 0 (tracking just started)
- Incidents Documented: 0
- Severity: N/A
- Trend: Baseline establishment

**Q2 2026 Target**:
- Goal: <5 violations
- Focus: Agent onboarding compliance
- Review: Quarterly effectiveness assessment

---

## Incident Files in This Directory

**Current Incidents**: (None - tracking just started)

When incidents occur, they will be listed here with status:

```
- VIOLATION_YYYY_MM_DD_[DESCRIPTION].md - [OPEN | RESOLVED | ESCALATED]
```

---

## Quarterly Monitoring Reports

**Location**: `governance/reports/`

**Naming**: `EXECUTION_BOOTSTRAP_PROTOCOL_Q[N]_YYYY_MONITORING_REPORT.md`

**Schedule**:
- Q1 2026 (Jan-Mar): Report due 2026-04-14
- Q2 2026 (Apr-Jun): Report due 2026-07-14
- Q3 2026 (Jul-Sep): Report due 2026-10-14
- Q4 2026 (Oct-Dec): Report due 2027-01-14

**Template**: `governance/templates/EXECUTION_BOOTSTRAP_PROTOCOL_QUARTERLY_MONITORING_REPORT.md`

---

## References

- **Canonical Protocol**: maturion-foreman-governance/governance/canon/EXECUTION_BOOTSTRAP_PROTOCOL.md
- **Monitoring Spec**: maturion-foreman-governance/governance/canon/EXECUTION_BOOTSTRAP_PROTOCOL_MONITORING_AND_ENFORCEMENT.md
- **Incident Template**: `TRACKING_TEMPLATE.md` (this directory)
- **Quarterly Report Template**: `governance/templates/EXECUTION_BOOTSTRAP_PROTOCOL_QUARTERLY_MONITORING_REPORT.md`

---

## Questions & Escalation

**Report violations to**: Governance Liaison  
**Escalate major violations to**: Johan Ras (CS2)  
**Quarterly report submission to**: maturion-foreman-governance repository

---

**Status**: Active Tracking  
**Authority**: Canonical Governance  
**Compliance**: MANDATORY

---

**END OF PROTOCOL VIOLATIONS TRACKING README**
