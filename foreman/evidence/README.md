# Evidence Directory

**Purpose**: Store complete evidence trails for all build tasks  
**Status**: Mandatory for all builds  
**Authority**: BUILD_PHILOSOPHY.md Section XII (Evidence Requirements)

---

## Overview

This directory contains **structured evidence** for every build task executed in the Maturion ecosystem.

**Evidence is mandatory** and serves multiple purposes:
- Audit trail for governance compliance
- Learning from past builds
- Troubleshooting and debugging
- Quality assurance
- Continuous improvement

---

## Directory Structure

```
foreman/evidence/
├── README.md (this file)
├── templates/
│   ├── build-initiation.template.json
│   ├── validation-results.template.json
│   ├── iteration.template.json
│   └── completion-report.template.md
└── builds/
    ├── <task-id-001>/
    │   ├── build-initiation.json
    │   ├── validation-results.json
    │   ├── iterations/
    │   │   ├── iteration-001.json
    │   │   ├── iteration-002.json
    │   │   └── ...
    │   ├── final-validation.json
    │   ├── qa-results.json
    │   └── completion-report.md
    ├── <task-id-002>/
    │   └── ...
    └── ...
```

---

## Evidence Components

### 1. Build Initiation Evidence

**File**: `build-initiation.json`  
**Template**: `templates/build-initiation.template.json`

**Contains**:
- Task ID and metadata
- Instruction received (exact format)
- Architecture reference
- QA suite location and status
- Builder assigned
- Expected deliverables
- Timestamp started

**When Created**: At the start of every build task

---

### 2. Validation Results Evidence

**File**: `validation-results.json`  
**Template**: `templates/validation-results.template.json`

**Contains**:
- Instruction format validation results
- Architecture validation results
- QA suite validation results
- Acceptance criteria validation results
- Overall validation status
- Decision (PROCEED | REJECT)
- Action required if rejected

**When Created**: After pre-build validation (before build starts)

---

### 3. Iteration Evidence

**Files**: `iterations/iteration-NNN.json`  
**Template**: `templates/iteration.template.json`

**Contains**:
- Iteration number
- QA status before and after
- Target test information
- Implementation details (files modified, approach)
- Result and progress
- Next action
- Escalation info (if needed)

**When Created**: After each build iteration

**Note**: There will be one iteration file per iteration (iteration-001, iteration-002, etc.)

---

### 4. Completion Report

**File**: `completion-report.md`  
**Template**: `templates/completion-report.template.md`

**Contains**:
- Build summary (status, duration, iterations)
- Final QA results (100% pass required)
- Build quality validation
- Iteration summary table
- Evidence trail checklist
- Deliverables status
- Architecture conformance
- Governance compliance
- Issues and resolutions
- Lessons learned
- Foreman validation
- Human approval status

**When Created**: At build completion (or failure)

---

### 5. Additional Evidence Files

**Files**:
- `final-validation.json` - Final validation before reporting green
- `qa-results.json` - Complete QA test results
- `escalation-report.md` - If escalation occurred
- `incident-report.md` - If governance violation detected

**When Created**: As needed during build process

---

## Evidence Requirements

### Mandatory for ALL Builds

Every build MUST have:
- ✅ `build-initiation.json`
- ✅ `validation-results.json`
- ✅ At least one `iterations/iteration-*.json`
- ✅ `completion-report.md`

**If ANY missing** → Evidence trail is incomplete → Build cannot be approved

### Optional (Situational)

- `final-validation.json` - Recommended for all successful builds
- `qa-results.json` - Recommended for detailed QA records
- `escalation-report.md` - Required if escalation occurred
- `incident-report.md` - Required if violation detected

---

## Evidence Usage

### By Foreman

**Before Build**:
- Review past evidence from similar builds
- Learn from previous issues and solutions
- Improve task sequencing

**During Build**:
- Monitor progress through iteration evidence
- Detect patterns of issues
- Identify when to escalate

**After Build**:
- Validate completeness
- Extract lessons learned
- Update governance memory

### By Builders

**Before Build**:
- Review evidence from similar past builds
- Understand common pitfalls
- Plan approach

**During Build**:
- Document each iteration
- Capture decision rationale
- Log issues immediately

**After Build**:
- Complete evidence trail
- Document lessons learned
- Suggest improvements

### By Humans (Johan, Developers)

**Review and Audit**:
- Understand what was built and how
- Validate governance compliance
- Learn from build patterns
- Identify process improvements

**Troubleshooting**:
- Diagnose build failures
- Understand decisions made
- Trace root causes

---

## Evidence Templates

### Using Templates

1. **Copy** template from `templates/` directory
2. **Fill in** all fields with actual data
3. **Save** to appropriate build directory
4. **Validate** completeness

### Template Fields

**JSON Templates** (`.json`):
- Replace `<placeholders>` with actual values
- Update counts and status fields
- Add arrays and objects as needed
- Maintain valid JSON structure

**Markdown Templates** (`.md`):
- Replace `<placeholders>` with actual content
- Update checklists (✅ or ❌)
- Fill in all sections
- Keep structure intact

---

## Evidence Validation

### Checklist for Complete Evidence

```
Build Evidence Completeness Checklist:
□ build-initiation.json exists and is valid
□ validation-results.json exists and is valid
□ At least one iteration file exists
□ All iteration files are sequential (001, 002, ...)
□ completion-report.md exists and is complete
□ All required sections filled in
□ No <placeholder> text remaining
□ All timestamps are ISO 8601 format
□ All file paths are absolute and correct
□ All JSON files are valid JSON
```

**If ANY unchecked** → Evidence is incomplete

---

## Evidence Retention

### Retention Policy

- **All evidence is permanent** (never deleted)
- Stored in version control (git)
- Survives chat resets and model upgrades
- Available for future reference

### Storage Considerations

- Evidence files are text-based (JSON and Markdown)
- Minimal storage footprint
- Easily searchable and parseable
- Human-readable

---

## Evidence and Governance

### Governance Requirements

Evidence is **mandatory** under:
- BUILD_PHILOSOPHY.md Section XII (Evidence Requirements)
- Foreman Agent Contract Section VIII (Evidence and Audit Trail)
- Build to Green Rule Section VI (Evidence Requirements)

**Evidence is part of governance compliance.**

### Audit Trail

Evidence provides:
- Complete audit trail for all builds
- Traceability of decisions
- Compliance validation
- Quality assurance
- Continuous improvement data

---

## Example Evidence

### Example Build Task

**Task ID**: `task-user-profile-001`  
**Module**: User Profile Management  
**Builder**: UI Builder

**Evidence Files**:
```
foreman/evidence/builds/task-user-profile-001/
├── build-initiation.json (task details)
├── validation-results.json (all validations passed)
├── iterations/
│   ├── iteration-001.json (ProfileView component)
│   ├── iteration-002.json (ProfileEdit component)
│   ├── iteration-003.json (UserService)
│   └── iteration-004.json (validation logic)
├── final-validation.json (100% pass confirmed)
├── qa-results.json (12/12 tests passing)
└── completion-report.md (build successful)
```

**Result**: Complete evidence trail, build approved, merged successfully

---

## Quick Reference

### For Foreman

**Creating Evidence**:
1. Use templates from `templates/`
2. Create `builds/<task-id>/` directory
3. Copy and fill templates
4. Validate completeness
5. Reference in completion report

### For Builders

**Documenting Work**:
1. Start with `build-initiation.json`
2. Create `iterations/` directory
3. Log each iteration immediately
4. Complete `completion-report.md`
5. Verify all evidence present

### For Humans

**Reviewing Evidence**:
1. Navigate to `builds/<task-id>/`
2. Read `completion-report.md` first
3. Review validation results
4. Check iteration details if needed
5. Verify completeness

---

## Version and Status

**Version**: 1.0.0  
**Status**: Active  
**Last Updated**: 2025-12-15  
**Owner**: Johan (MaturionISMS)  
**Maintainer**: Maturion Foreman

---

## Summary

Evidence is:
- ✅ **Mandatory** - Required for all builds
- ✅ **Structured** - Templates and standards
- ✅ **Complete** - All phases documented
- ✅ **Permanent** - Never deleted
- ✅ **Auditable** - Full traceability
- ✅ **Valuable** - Learning and improvement

**Perfect software requires perfect documentation.**

---

*END OF EVIDENCE DIRECTORY README*
