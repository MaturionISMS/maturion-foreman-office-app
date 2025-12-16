# FL/CI Catastrophic Failure Evidence Directory

**Purpose**: Store complete evidence trails for all catastrophic failures observed after Build-to-Green  
**Status**: Mandatory for all catastrophic failures  
**Authority**: BUILD_PHILOSOPHY.md Section XIII + Foreman Agent Contract (One-Time Failure Doctrine)  
**Schema Version**: 1.0.0

---

## Overview

This directory contains **structured evidence** for every catastrophic failure observed in Field/Live (FL) or CI/Test environments after successful Build-to-Green completion.

**Every observed defect after Build-to-Green is treated as a catastrophic failure.**

### Purpose of FL/CI Evidence

1. **Permanent Prevention** - Ensure the defect can never happen again
2. **Root Cause Learning** - Understand why it escaped Build-to-Green
3. **Process Improvement** - Strengthen QA, architecture, and governance
4. **Compliance** - Meet incident management requirements
5. **Audit Trail** - Complete traceability of failure response

---

## What is a Catastrophic Failure?

### Definition

A **catastrophic failure** is any defect observed after successful Build-to-Green completion that:
- Affects functionality
- Impacts users or systems
- Should have been caught by existing QA

### Severity Levels

**Catastrophic** - First occurrence of this defect type
- Requires immediate fix + permanent prevention
- Root cause analysis mandatory
- Test coverage gaps must be filled

**Double-Catastrophic** - Second occurrence of a previously fixed defect type
- Indicates prevention mechanism failed
- Requires human review and approval
- Governance process review required

**Multi-Catastrophic** - Third+ occurrence
- Governance crisis
- Escalation to Johan mandatory
- Systemic process failure

---

## Evidence Schema

All evidence MUST conform to: **`FLCI_EVIDENCE_SCHEMA.json`**

This schema defines three evidence types:

### 1. Failure Report (`failure-report.json`)
Structured data about the failure:
- Failure ID (FLCI-YYYYMMDD-NNN)
- Severity classification
- Objective description
- Context (where/when observed)
- Root cause analysis
- Discovery details

### 2. Prevention Plan (`prevention-plan.json`)
Permanent prevention actions:
- Immediate fix details
- Test coverage updates
- Architecture updates (if needed)
- Governance updates (if needed)
- Prevention mechanism
- Validation evidence

### 3. Test Coverage Delta (`test-coverage-delta.json`)
Before/after test coverage:
- Coverage before fix
- Coverage after fix
- Tests added by type
- Coverage improvement metrics

---

## Directory Structure

```
foreman/evidence/flci/
├── README.md (this file)
├── FLCI_EVIDENCE_SCHEMA.json (canonical schema)
├── templates/
│   ├── failure-report.template.json
│   ├── prevention-plan.template.json
│   ├── test-coverage-delta.template.json
│   ├── root-cause-analysis.template.md
│   └── completion-validation.template.md
└── FLCI-YYYYMMDD-NNN/
    ├── failure-report.json
    ├── prevention-plan.json
    ├── test-coverage-delta.json
    ├── root-cause-analysis.md
    └── completion-validation.md
```

---

## Workflow

### 1. Failure Observed
- Create GitHub issue using "Catastrophic Failure — FL/CI" template
- Assign failure ID: FLCI-YYYYMMDD-NNN
- Create evidence directory: `foreman/evidence/flci/FLCI-YYYYMMDD-NNN/`

### 2. Failure Report
- Fill in `failure-report.json` from template
- Document objective description
- Classify severity
- Identify context (where/when observed)

### 3. Root Cause Analysis
- Fill in `root-cause-analysis.md` from template
- Investigate why it happened
- Analyze why it escaped Build-to-Green
- Identify contributing factors

### 4. Immediate Fix
- Implement fix for the defect
- Validate fix works
- Document in `prevention-plan.json`

### 5. Permanent Prevention
- Add tests to catch this defect forever
- Update architecture (if needed)
- Update governance (if needed)
- Document in `prevention-plan.json`
- Capture coverage delta in `test-coverage-delta.json`

### 6. Validation
- Validate prevention works
- Attempt to reproduce failure (should fail)
- Document in `completion-validation.md`

### 7. Lesson Propagation
- Identify similar patterns in other code
- Add tests to affected modules
- Update documentation
- Document in `completion-validation.md`

### 8. Closure
- Complete all evidence files
- Foreman validation
- Human approval (for double-catastrophic+)
- Close GitHub issue

---

## Evidence Requirements

### Mandatory for ALL Catastrophic Failures

Every catastrophic failure MUST have:
- ✅ `failure-report.json` - Structured failure data
- ✅ `prevention-plan.json` - Prevention actions
- ✅ `test-coverage-delta.json` - Coverage improvements
- ✅ `root-cause-analysis.md` - Detailed RCA
- ✅ `completion-validation.md` - Final validation

**If ANY missing** → Evidence trail is incomplete → Issue cannot be closed

---

## One-Time Failure Doctrine

From Foreman Agent Contract:

> "A failure may occur once. Upon first occurrence, implement permanent prevention. 
> Repeat occurrence without prevention is a catastrophic failure."

### What This Means

1. **First Occurrence** - Acceptable but requires permanent prevention
2. **Second Occurrence** - Governance failure, prevention mechanism failed
3. **Third+ Occurrence** - Systemic failure, escalation required

### Permanent Prevention Requirements

Every catastrophic failure MUST result in:
- ✅ Tests added (minimum 1)
- ✅ Prevention mechanism documented
- ✅ Validation that defect cannot recur
- ✅ Lessons propagated to similar code

**No exceptions. No deferrals.**

---

## Closure Criteria

A catastrophic failure issue can ONLY be closed when ALL of the following are met:

- [ ] Immediate fix applied and validated
- [ ] Root cause fully understood and documented
- [ ] Permanent prevention implemented (tests/architecture/policy)
- [ ] Prevention validated (defect can never escape again)
- [ ] Lessons propagated to all affected areas
- [ ] Complete evidence trail generated
- [ ] Foreman validation passed
- [ ] Human approval obtained (for double-catastrophic or higher)

---

## Templates

All templates are in `foreman/evidence/flci/templates/`:

### JSON Templates
- `failure-report.template.json`
- `prevention-plan.template.json`
- `test-coverage-delta.template.json`

### Markdown Templates
- `root-cause-analysis.template.md`
- `completion-validation.template.md`

### Using Templates

1. Copy template to failure directory
2. Rename to remove `.template`
3. Fill in all `<placeholders>`
4. Validate against schema

---

## Schema Validation

All JSON files MUST conform to `FLCI_EVIDENCE_SCHEMA.json`.

**Required Fields**:
- failure_id (format: FLCI-YYYYMMDD-NNN)
- ISO 8601 timestamps
- evidence_metadata.immutable = true
- evidence_metadata.schema_version = "1.0.0"

**Validation**:
```bash
# Validate against schema
python foreman/evidence/schema_validator.py \
  --schema foreman/evidence/flci/FLCI_EVIDENCE_SCHEMA.json \
  --evidence foreman/evidence/flci/FLCI-YYYYMMDD-NNN/failure-report.json
```

---

## Compliance Mapping

FL/CI failure evidence maps to these compliance controls:

### Failure Report
- ISO 27001:A.16.1 - Management of information security incidents
- NIST 800-53:IR-4 - Incident Handling
- COBIT:DSS02 - Manage Service Requests and Incidents

### Prevention Plan
- ISO 27001:A.16.1.6 - Learning from information security incidents
- NIST 800-53:SA-11 - Developer Testing and Evaluation
- COBIT:APO11 - Manage Quality

### Test Coverage Delta
- ISO 27001:A.14.2.9 - System acceptance testing
- NIST 800-53:SA-11 - Developer Testing
- COBIT:BAI03.10 - Maintain systems

---

## Example Evidence

### Example Structure

```
foreman/evidence/flci/FLCI-20251216-001/
├── failure-report.json
│   └── Failure ID: FLCI-20251216-001
│       Severity: catastrophic
│       Root Cause: missing_qa_coverage
│       Context: User Profile Edit Screen
├── root-cause-analysis.md
│   └── Detailed RCA showing validation logic gap
├── prevention-plan.json
│   └── Added 3 unit tests for validation
│       Updated validation architecture doc
├── test-coverage-delta.json
│   └── Before: 85% coverage (120 tests)
│       After: 87% coverage (123 tests)
│       Improvement: +2% (+3 tests)
└── completion-validation.md
    └── All criteria met
        Prevention validated
        Foreman approved
```

---

## Quick Reference

### For Reporters

**Reporting a Failure**:
1. Create GitHub issue with "Catastrophic Failure — FL/CI" template
2. Assign failure ID
3. Fill in objective description
4. Classify severity
5. Create evidence directory

### For Fixers

**Fixing a Failure**:
1. Implement immediate fix
2. Add tests for permanent prevention
3. Fill in all evidence files
4. Validate prevention works
5. Propagate lessons

### For Validators

**Validating Completion**:
1. Review all evidence files
2. Verify prevention mechanism
3. Check test coverage improvement
4. Validate closure criteria met
5. Approve or request changes

---

## Retention Policy

- **All evidence is permanent** (never deleted)
- Stored in version control (git)
- Available for future reference and learning
- Supports audit and compliance requirements

---

## Constitutional Authority

This evidence system implements:

- **BUILD_PHILOSOPHY.md** Section XIII (Failure Learning)
- **Foreman Agent Contract** One-Time Failure Doctrine
- **Zero Regression Guarantee** Permanent prevention requirement

**Doctrine**: *"A failure may occur once. Implement permanent prevention. Repeat occurrence is catastrophic."*

---

## Version and Status

**Version**: 1.0.0  
**Status**: Active  
**Last Updated**: 2025-12-16  
**Owner**: Johan (MaturionISMS)  
**Maintainer**: Maturion Foreman

---

## Summary

FL/CI evidence is:
- ✅ **Mandatory** - Required for all catastrophic failures
- ✅ **Structured** - Schema-based with templates
- ✅ **Complete** - All phases documented
- ✅ **Permanent** - Never deleted
- ✅ **Actionable** - Drives permanent prevention
- ✅ **Auditable** - Full traceability

**Perfect software requires learning from every failure—permanently.**

---

*END OF FL/CI EVIDENCE DIRECTORY README*
