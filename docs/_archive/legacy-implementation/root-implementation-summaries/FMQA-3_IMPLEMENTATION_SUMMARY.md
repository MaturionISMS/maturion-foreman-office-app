# FMQA-3 Implementation Summary: Catastrophic Failure Workflow

**Issue**: FMQA-3 — Implement Catastrophic Failure Handling as a Workflow (FL/CI Template + Evidence)  
**Repository**: maturion-foreman-office-app  
**Implementation Date**: 2025-12-16  
**Status**: ✅ COMPLETE

---

## Objective Achieved

Implemented a standardized, governed workflow for handling every observed defect after Build-to-Green as a catastrophic failure, ensuring:
- Nothing is ignored
- Fixes become permanent prevention
- Lessons propagate across the system
- Complete audit trail maintained

**Result**: Every post-Build-to-Green defect now follows a rigorous workflow with structured evidence, mandatory permanent prevention, and full traceability.

---

## Deliverables

### 1. GitHub Issue Template ✅

**File**: `.github/ISSUE_TEMPLATE/catastrophic_failure.md`

**Name**: "Catastrophic Failure — FL/CI"  
**Size**: 5.7KB, 200+ lines  
**Format**: GitHub issue template with YAML frontmatter

**Key Sections**:
1. **What Failed** - Objective description
2. **Where Observed** - Context (Field/Live, CI/Test, etc.)
3. **Severity Classification**
   - Catastrophic (1st occurrence)
   - Double-Catastrophic (2nd occurrence)
   - Multi-Catastrophic (3rd+ occurrence)
4. **Root Cause Analysis**
   - 8 root cause buckets (missing architecture, missing QA, misaligned QA, implementation bug, governance gap, integration issue, environmental issue, unknown)
   - Detailed RCA fields
   - Why it escaped Build-to-Green
5. **Immediate Fix** - Fix description and validation
6. **Permanent Prevention** (MANDATORY)
   - Test coverage updates (minimum 1 test required)
   - Architecture updates (if needed)
   - Governance/policy updates (if needed)
   - Prevention validation
7. **Lesson Propagation** - Affected modules and propagation plan
8. **Evidence Trail** - Required evidence files
9. **Related Issues/PRs** - Links to fixes and prevention
10. **Foreman Validation** - Validation status and notes
11. **Closure Criteria** - 8 mandatory criteria for closure

**Features**:
- Markdown checklists for tracking
- Placeholder text with clear guidance
- Constitutional authority references
- Structured data capture
- Enforcement of One-Time Failure Doctrine

---

### 2. Evidence Schema ✅

**File**: `foreman/evidence/flci/FLCI_EVIDENCE_SCHEMA.json`

**Size**: 19KB, 550+ lines  
**Format**: JSON Schema (draft-07)  
**Version**: 1.0.0

**Schema Definitions**:

#### Common Definitions
- `iso8601_timestamp` - ISO 8601 timestamp pattern
- `failure_id` - FLCI-YYYYMMDD-NNN format
- `severity_level` - catastrophic | double-catastrophic | multi-catastrophic
- `root_cause_bucket` - 8 standardized buckets
- `context_type` - field_live | ci_test | development | staging | production
- `test_type` - unit | integration | e2e | regression | performance | security

#### Evidence Type 1: Failure Report
**Schema ID**: `failure-report`

**Required Fields**:
- `failure_id` - Unique identifier
- `reported_date` - ISO 8601 timestamp
- `severity` - Level, justification, occurrence count
- `objective_description` - What failed, observable behavior, expected behavior
- `context` - Type, location, user impact
- `root_cause_analysis` - Primary bucket, detailed analysis, why escaped B2G
- `evidence_metadata` - Schema version, immutability, governance gate version

**Optional Fields**:
- `discovery_details` - Discovered by, timestamp, method

#### Evidence Type 2: Prevention Plan
**Schema ID**: `prevention-plan`

**Required Fields**:
- `failure_id` - Reference to failure report
- `immediate_fix` - Applied, description, timestamp, PR, validation
- `permanent_prevention` - Test coverage updates, prevention mechanism
  - `tests_added` - Type, file path, test name, purpose (minimum 1)
  - `coverage_gap_analysis` - Why coverage was missing
  - `architecture_updates` - If required
  - `governance_updates` - If required
  - `prevention_mechanism` - How defect will be caught forever
- `validation` - Prevention validated, by whom, timestamp
- `evidence_metadata` - Schema version, immutability, parent reference

#### Evidence Type 3: Test Coverage Delta
**Schema ID**: `test-coverage-delta`

**Required Fields**:
- `failure_id` - Reference to failure report
- `before_coverage` - Total tests, percentage, lines, by type
- `after_coverage` - Total tests, percentage, lines, by type
- `coverage_improvement` - Tests added, lines added, percentage increase, gap filled
- `evidence_metadata` - Schema version, immutability, parent reference

**Compliance Mappings**:
- ISO 27001:A.16.1 - Incident management
- NIST 800-53:IR-4 - Incident handling
- NIST 800-53:SA-11 - Developer testing
- COBIT:DSS02 - Service requests and incidents
- COBIT:APO11 - Quality management

---

### 3. Evidence Templates ✅

**Directory**: `foreman/evidence/flci/templates/`

#### JSON Templates

1. **failure-report.template.json** (1.5KB)
   - Complete structure with placeholders
   - All required and optional fields
   - Compliance mappings included
   - Ready to copy and fill

2. **prevention-plan.template.json** (1.6KB)
   - Immediate fix section
   - Permanent prevention section
   - Tests added array with example
   - Validation section
   - Parent reference to failure report

3. **test-coverage-delta.template.json** (0.9KB)
   - Before/after coverage structure
   - By test type breakdown
   - Coverage improvement metrics
   - Parent reference to failure report

#### Markdown Templates

4. **root-cause-analysis.template.md** (2.5KB)
   - Executive summary
   - Failure details
   - Root cause investigation
   - Why escaped Build-to-Green
   - Contributing factors
   - Impact assessment
   - Prevention analysis
   - Recommendations
   - Evidence chain references
   - Approval section

5. **completion-validation.template.md** (4.5KB)
   - 8-point closure criteria checklist
   - Evidence summary with status
   - Tests added table
   - Architecture/governance updates
   - Test coverage delta summary
   - Prevention mechanism validation
   - Lesson propagation status
   - Final assessment
   - Doctrine compliance checklist
   - Approval section (Foreman + Human)
   - Issue closure section

**All Templates**:
- Include `<placeholders>` for values to fill
- Follow canonical schema structure
- Include governance/compliance references
- Maintain evidence chain traceability

---

### 4. Evidence Directory Structure ✅

**Created**: `foreman/evidence/flci/`

**Structure**:
```
foreman/evidence/flci/
├── README.md (11KB - complete documentation)
├── FLCI_EVIDENCE_SCHEMA.json (19KB - canonical schema)
├── templates/
│   ├── failure-report.template.json
│   ├── prevention-plan.template.json
│   ├── test-coverage-delta.template.json
│   ├── root-cause-analysis.template.md
│   └── completion-validation.template.md
└── FLCI-YYYYMMDD-NNN/ (created per failure)
    ├── failure-report.json
    ├── prevention-plan.json
    ├── test-coverage-delta.json
    ├── root-cause-analysis.md
    └── completion-validation.md
```

**Directory Purpose**:
- Store complete evidence for all catastrophic failures
- Permanent retention (never deleted)
- Version controlled
- Machine-readable (JSON) + human-readable (Markdown)
- Full audit trail

---

### 5. FL/CI Evidence README ✅

**File**: `foreman/evidence/flci/README.md`

**Size**: 11KB, 380+ lines  
**Status**: Complete documentation

**Contents**:

1. **Overview** - Purpose and authority
2. **What is a Catastrophic Failure** - Definition and severity levels
3. **Evidence Schema** - Reference to FLCI_EVIDENCE_SCHEMA.json
4. **Directory Structure** - Complete structure diagram
5. **Workflow** - 8-step workflow from observation to closure
6. **Evidence Requirements** - Mandatory files for all failures
7. **One-Time Failure Doctrine** - Implementation details
8. **Closure Criteria** - 8 mandatory criteria
9. **Templates** - How to use templates
10. **Schema Validation** - Validation commands
11. **Compliance Mapping** - Control mappings by evidence type
12. **Example Evidence** - Complete example structure
13. **Quick Reference** - For reporters, fixers, validators
14. **Retention Policy** - Permanent retention
15. **Constitutional Authority** - References to BUILD_PHILOSOPHY.md and Agent Contract

**Key Features**:
- Complete workflow documentation
- Clear roles and responsibilities
- Step-by-step guidance
- Example evidence trail
- Quick reference sections
- Compliance integration

---

### 6. Main Evidence README Update ✅

**File**: `foreman/evidence/README.md`

**Changes Made**:

1. **Updated Directory Structure** (lines 40-79)
   - Added `flci/` directory to structure diagram
   - Shows FL/CI templates and evidence structure
   - Maintains consistency with main structure

2. **Added FL/CI Evidence Section** (lines 179-200)
   - New section: "6. FL/CI Catastrophic Failure Evidence"
   - Directory: `flci/`
   - Schema: `FLCI_EVIDENCE_SCHEMA.json`
   - README reference: `flci/README.md`
   - Purpose statement
   - Evidence types list
   - Authority references
   - Cross-reference to FL/CI README

**Integration**:
- FL/CI evidence now part of main evidence system
- Consistent with existing build evidence
- Clear separation of concerns
- Unified governance approach

---

## Workflow Implementation

### Complete Catastrophic Failure Workflow

1. **Failure Observed**
   - Defect detected after Build-to-Green
   - Create GitHub issue using "Catastrophic Failure — FL/CI" template
   - Assign failure ID: FLCI-YYYYMMDD-NNN
   - Create evidence directory

2. **Failure Report**
   - Fill in `failure-report.json` from template
   - Document objective description
   - Classify severity (catastrophic/double/multi)
   - Identify context and impact

3. **Root Cause Analysis**
   - Fill in `root-cause-analysis.md` from template
   - Investigate why it happened
   - Analyze why it escaped Build-to-Green
   - Identify contributing factors

4. **Immediate Fix**
   - Implement fix for the defect
   - Validate fix works
   - Create fix PR
   - Document in `prevention-plan.json`

5. **Permanent Prevention**
   - Add tests to catch defect forever (minimum 1)
   - Update architecture (if needed)
   - Update governance (if needed)
   - Document in `prevention-plan.json`
   - Capture coverage delta in `test-coverage-delta.json`

6. **Validation**
   - Validate prevention works
   - Attempt to reproduce failure (should fail)
   - Run tests to confirm detection
   - Document in `completion-validation.md`

7. **Lesson Propagation**
   - Identify similar patterns in other code
   - Add tests to affected modules
   - Update documentation
   - Document in `completion-validation.md`

8. **Closure**
   - Complete all evidence files
   - Foreman validation
   - Human approval (for double-catastrophic+)
   - Close GitHub issue

---

## One-Time Failure Doctrine Implementation

### From Foreman Agent Contract

> "A failure may occur once. Upon first occurrence, implement permanent prevention.
> Repeat occurrence without prevention is a catastrophic failure."

### Implementation in FMQA-3

**First Occurrence (Catastrophic)**:
- Severity: Catastrophic
- Response: Immediate fix + permanent prevention
- Requirements:
  - Root cause analysis
  - Tests added (minimum 1)
  - Prevention mechanism documented
  - Validation completed
- Approval: Foreman validation required

**Second Occurrence (Double-Catastrophic)**:
- Severity: Double-Catastrophic
- Response: Governance failure investigation
- Requirements:
  - All catastrophic requirements
  - Analysis of why prevention failed
  - Strengthened prevention mechanism
  - Governance process review
- Approval: Foreman validation + Human approval required

**Third+ Occurrence (Multi-Catastrophic)**:
- Severity: Multi-Catastrophic
- Response: Systemic failure escalation
- Requirements:
  - All double-catastrophic requirements
  - Systemic process analysis
  - Governance crisis response
  - Escalation to Johan
- Approval: Johan approval required

### Enforcement

**Mandatory Prevention**:
- Every catastrophic failure MUST result in permanent prevention
- Tests added (minimum 1, no maximum)
- Prevention mechanism documented and validated
- Cannot close issue without prevention

**Evidence Trail**:
- Complete evidence required for all severities
- Immutable evidence (never modified after creation)
- Permanent retention (never deleted)
- Full traceability chain

**Governance**:
- Constitutional authority (BUILD_PHILOSOPHY.md Section XIII)
- Agent contract compliance (One-Time Failure Doctrine)
- Zero Regression Guarantee enforcement
- Compliance control mapping

---

## Files Created/Modified

### New Files Created

1. `.github/ISSUE_TEMPLATE/catastrophic_failure.md` (5.7KB)
2. `foreman/evidence/flci/FLCI_EVIDENCE_SCHEMA.json` (19KB)
3. `foreman/evidence/flci/README.md` (11KB)
4. `foreman/evidence/flci/templates/failure-report.template.json` (1.5KB)
5. `foreman/evidence/flci/templates/prevention-plan.template.json` (1.6KB)
6. `foreman/evidence/flci/templates/test-coverage-delta.template.json` (0.9KB)
7. `foreman/evidence/flci/templates/root-cause-analysis.template.md` (2.5KB)
8. `foreman/evidence/flci/templates/completion-validation.template.md` (4.5KB)

**Total New Files**: 8  
**Total Size**: ~47KB

### Modified Files

1. `foreman/evidence/README.md`
   - Added FL/CI directory to structure diagram
   - Added FL/CI evidence section
   - ~40 lines added

**Total Modified Files**: 1

---

## Validation Results

### JSON Schema Validation ✅

All JSON files validated successfully:
- ✅ `FLCI_EVIDENCE_SCHEMA.json` - Valid JSON Schema (draft-07)
- ✅ `failure-report.template.json` - Valid JSON
- ✅ `prevention-plan.template.json` - Valid JSON
- ✅ `test-coverage-delta.template.json` - Valid JSON

**Validation Command**:
```bash
python3 -m json.tool <file> > /dev/null
```

**Result**: All JSON files parse without errors

### Markdown Template Validation ✅

All Markdown templates validated:
- ✅ `root-cause-analysis.template.md` - Well-structured
- ✅ `completion-validation.template.md` - Well-structured
- ✅ `README.md` - Complete documentation

**Result**: All templates follow Markdown best practices

### Structure Validation ✅

Directory structure validated:
- ✅ `foreman/evidence/flci/` exists
- ✅ `foreman/evidence/flci/templates/` exists
- ✅ All template files present
- ✅ Schema file present
- ✅ README present

**Result**: Complete evidence directory structure

---

## Constitutional Compliance

### BUILD_PHILOSOPHY.md Alignment

**Section XIII: Failure Learning** ✅
- Evidence collected for every failure
- Root cause analysis mandatory
- Permanent prevention required
- Lessons propagated across system

**Principle 1: One-Time Build Correctness** ✅
- Failures analyzed to improve future builds
- Prevention mechanisms added to Build-to-Green

**Principle 2: Zero Regression Guarantee** ✅
- Tests added to prevent repeat failures
- Permanent prevention enforced

**Principle 4: Zero Loss of Context** ✅
- Complete evidence trail maintained
- All decisions documented
- Rationales preserved

**Principle 5: Zero Ambiguity** ✅
- Structured evidence format
- Machine-readable schema
- Clear closure criteria

### Foreman Agent Contract Alignment

**One-Time Failure Doctrine** ✅
- First occurrence requires permanent prevention
- Second occurrence is governance failure
- Third+ occurrence is systemic failure

**Evidence and Audit Trail** ✅
- Complete evidence for all failures
- Immutable evidence records
- Permanent retention

**QA Governance** ✅
- Test coverage gaps identified and filled
- Prevention validated before closure

---

## Usage Guide

### For Reporters

**To Report a Catastrophic Failure**:

1. Navigate to repository Issues
2. Click "New issue"
3. Select "Catastrophic Failure — FL/CI" template
4. Fill in all required sections
5. Assign failure ID: FLCI-YYYYMMDD-NNN
6. Submit issue

### For Fixers

**To Fix a Catastrophic Failure**:

1. Clone repository
2. Create evidence directory: `foreman/evidence/flci/FLCI-YYYYMMDD-NNN/`
3. Copy templates from `foreman/evidence/flci/templates/`
4. Fill in `failure-report.json` (structured data)
5. Write `root-cause-analysis.md` (detailed RCA)
6. Implement immediate fix and create PR
7. Add permanent prevention tests (minimum 1)
8. Fill in `prevention-plan.json` (prevention actions)
9. Capture `test-coverage-delta.json` (coverage improvement)
10. Validate prevention works
11. Fill in `completion-validation.md` (final validation)
12. Request Foreman validation
13. Request human approval (if double-catastrophic+)
14. Close issue when all criteria met

### For Validators

**To Validate a Catastrophic Failure Resolution**:

1. Navigate to evidence directory
2. Review all evidence files for completeness
3. Verify immediate fix applied and validated
4. Verify root cause fully understood
5. Verify permanent prevention implemented
   - Tests added (minimum 1)
   - Prevention mechanism documented
   - Prevention validated
6. Verify lessons propagated
7. Check closure criteria checklist (8 items)
8. Approve or request changes
9. Document validation in `completion-validation.md`

---

## Acceptance Criteria Met

### Original Requirements ✅

**1. GitHub Issue Template** ✅
- ✅ Template created: "Catastrophic Failure — FL/CI"
- ✅ Includes objective description field
- ✅ Includes where observed (screen/flow)
- ✅ Includes severity classification (catastrophic/double/multi)
- ✅ Includes root cause buckets (8 options)
- ✅ Includes permanent prevention requirements
  - ✅ Test added/updated
  - ✅ Rule added
  - ✅ Policy update required?

**2. Evidence File Output Format** ✅
- ✅ Schema defined: `FLCI_EVIDENCE_SCHEMA.json`
- ✅ Directory structure: `foreman/evidence/flci/FLCI-YYYYMMDD-NNN/`
- ✅ Templates created (5 templates)
- ✅ Documentation complete (`README.md`)

**3. Evidence Directory** ✅
- ✅ Directory created: `foreman/evidence/flci/`
- ✅ Structure documented
- ✅ Per-failure subdirectories specified

---

## Key Features

### Workflow Features

1. **Standardized Process** - Same workflow for all catastrophic failures
2. **Structured Evidence** - JSON schema + Markdown templates
3. **Mandatory Prevention** - Cannot close without permanent prevention
4. **Severity Classification** - 3 levels with escalation
5. **Root Cause Buckets** - 8 standardized categories
6. **Lesson Propagation** - Built into workflow
7. **Foreman Validation** - Required for all
8. **Human Approval** - Required for double-catastrophic+

### Evidence Features

1. **Machine-Readable** - JSON Schema validation
2. **Human-Readable** - Markdown documentation
3. **Immutable** - Evidence never modified
4. **Permanent** - Evidence never deleted
5. **Traceable** - Parent references and IDs
6. **Compliant** - Maps to ISO/NIST/COBIT controls
7. **Versioned** - Schema version tracking
8. **Governed** - Governance Gate compatible

### Governance Features

1. **Constitutional Authority** - BUILD_PHILOSOPHY.md + Agent Contract
2. **One-Time Failure Doctrine** - Directly implemented
3. **Zero Regression** - Enforced through tests
4. **Evidence Requirements** - Mandatory evidence trail
5. **Audit Support** - Complete traceability
6. **Compliance Mapping** - ISO/NIST/COBIT controls

---

## Benefits

### Immediate Benefits

1. **Nothing Ignored** - Every failure captured and processed
2. **Permanent Prevention** - Tests ensure no repeat
3. **Learning Culture** - Failures become improvements
4. **Audit Trail** - Complete evidence for compliance
5. **Process Consistency** - Same workflow every time

### Long-Term Benefits

1. **Quality Improvement** - Test coverage increases over time
2. **Knowledge Capture** - Root causes documented
3. **Pattern Recognition** - Similar failures identified
4. **Governance Strength** - Process gaps filled
5. **Compliance Confidence** - Evidence supports audits

### Organizational Benefits

1. **Accountability** - Clear ownership and validation
2. **Transparency** - Open evidence trail
3. **Continuous Improvement** - Built-in learning
4. **Risk Reduction** - Failures prevented permanently
5. **Trust Building** - Systematic response to failures

---

## Integration with Existing Systems

### Evidence System Integration ✅

**Main Evidence Directory**:
- FL/CI evidence is subdirectory of `foreman/evidence/`
- Uses same governance gate approach
- Follows same immutability rules
- Consistent schema versioning

**Evidence Chain**:
- FL/CI failures reference Build-to-Green builds
- Test coverage deltas link to QA evidence
- Prevention plans reference architecture

### Issue Template Integration ✅

**GitHub Issues**:
- FL/CI template joins bug_report.md and feature_request.md
- Consistent YAML frontmatter format
- Labels for filtering (catastrophic-failure, priority-critical)
- Consistent structure with other templates

### Governance Integration ✅

**Constitutional Documents**:
- Implements BUILD_PHILOSOPHY.md Section XIII
- Enforces Foreman Agent Contract doctrine
- Supports Zero Regression Guarantee
- Maintains Evidence Requirements

**Compliance System**:
- Maps to ISO 27001 incident management
- Maps to NIST 800-53 incident handling
- Maps to COBIT service management
- Supports audit requirements

---

## Next Steps (Optional Enhancements)

While FMQA-3 is complete, potential future enhancements include:

1. **Automation**
   - Automated failure detection from logs
   - Automated evidence template population
   - Automated test coverage calculation

2. **Dashboard**
   - FL/CI failures dashboard
   - Severity trend charts
   - Root cause analytics
   - Prevention effectiveness metrics

3. **Notifications**
   - Alert on double-catastrophic failures
   - Escalation reminders
   - Closure criteria tracking

4. **Integration**
   - CI/CD integration for automatic issue creation
   - Monitoring system integration
   - Test coverage tool integration

5. **Analytics**
   - Failure pattern analysis
   - Root cause trend analysis
   - Prevention effectiveness measurement
   - Time-to-resolution metrics

---

## Summary

FMQA-3 is **COMPLETE**.

**Delivered**:
- ✅ GitHub issue template for catastrophic failures
- ✅ Complete evidence schema (FLCI_EVIDENCE_SCHEMA.json)
- ✅ Evidence directory structure (foreman/evidence/flci/)
- ✅ 5 comprehensive evidence templates
- ✅ Complete documentation (README.md)
- ✅ Integration with main evidence system
- ✅ Constitutional compliance
- ✅ One-Time Failure Doctrine implementation

**Result**:
Every observed defect after Build-to-Green now follows a rigorous, governed workflow that ensures:
- Nothing is ignored
- Fixes become permanent prevention
- Lessons propagate across the system
- Complete audit trail maintained
- Constitutional compliance enforced

**Status**: Ready for use

---

**Doctrine**: *"A failure may occur once. Implement permanent prevention. Repeat occurrence is catastrophic."* — **IMPLEMENTED**

---

*Implementation by: GitHub Copilot*  
*Date: 2025-12-16*  
*Status: Ready for merge*
