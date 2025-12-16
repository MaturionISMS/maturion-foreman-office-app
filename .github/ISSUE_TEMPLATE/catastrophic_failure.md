---
name: Catastrophic Failure — FL/CI
about: Report a defect observed after Build-to-Green (Field/Live or CI/Test)
title: '[FLCI] '
labels: 'catastrophic-failure, priority-critical'
assignees: ''

---

# Catastrophic Failure Report

**Failure ID**: FLCI-YYYYMMDD-NNN (e.g., FLCI-20251216-001)  
**Reported Date**: YYYY-MM-DD  
**Severity**: <!-- catastrophic | double-catastrophic -->

---

## 1. What Failed (Objective Description)

<!-- Provide a clear, objective description of what failed -->
<!-- Focus on observable behavior, not speculation about causes -->


---

## 2. Where Observed

**Context**: <!-- Field/Live | CI/Test | Development | Staging -->

**Screen/Flow**: <!-- Specific UI screen, API endpoint, or workflow step -->


**User Impact**: <!-- Describe the impact on users if applicable -->


---

## 3. Failure Severity Classification

**Severity Level**: <!-- Select ONE -->
- [ ] **Catastrophic** — First occurrence of this defect type
- [ ] **Double-Catastrophic** — Second occurrence of a previously fixed defect type
- [ ] **Multi-Catastrophic** — Third+ occurrence (governance crisis)

**Justification**:
<!-- Explain why this severity level was chosen -->


---

## 4. Root Cause Analysis

**Primary Root Cause Bucket**: <!-- Select ONE -->
- [ ] Missing Architecture
- [ ] Missing QA Coverage
- [ ] Misaligned QA (tests don't match architecture)
- [ ] Implementation Bug (logic error, typo, etc.)
- [ ] Governance Gap (policy or process failure)
- [ ] Integration Issue (module boundary violation)
- [ ] Environmental Issue (config, deployment, infrastructure)
- [ ] Unknown (requires investigation)

**Detailed Root Cause**:
<!-- Provide detailed analysis of what went wrong and why -->


**Why Did This Escape Build-to-Green?**:
<!-- Explain how this defect passed through our QA gates -->


---

## 5. Immediate Fix

**Fix Applied**: <!-- Yes | No | In Progress -->

**Fix Description**:
<!-- Describe the immediate fix that resolves the defect -->


**Fix Validation**:
<!-- How was the fix validated? What tests were run? -->


---

## 6. Permanent Prevention (MANDATORY)

Every catastrophic failure MUST result in permanent prevention.

### 6.1 Test Coverage Updates

**New Tests Added**:
- [ ] Unit test(s) added
- [ ] Integration test(s) added
- [ ] E2E test(s) added
- [ ] Regression test(s) added

**Test Details**:
<!-- List specific tests added with file paths and test names -->


**Test Coverage Gap Analysis**:
<!-- Explain what test coverage was missing and why -->


### 6.2 Architecture Updates

**Architecture Changes Required**: <!-- Yes | No -->

**Architecture Updates**:
<!-- If Yes, describe architecture documentation or spec updates -->


### 6.3 Governance/Policy Updates

**Policy Update Required**: <!-- Yes | No -->

**Policy Changes**:
<!-- If Yes, describe governance or policy changes needed -->


### 6.4 Prevention Validation

**How This Defect Will Be Caught Forever**:
<!-- Explain the permanent mechanism that ensures this can never happen again -->


**Prevention Evidence**:
<!-- Link to tests, governance updates, architecture changes -->


---

## 7. Lesson Propagation

**Affected Modules/Repositories**:
<!-- List all modules or repos that might have similar issues -->


**Propagation Plan**:
<!-- How will this lesson be propagated to other areas? -->
- [ ] Similar code/patterns identified and fixed
- [ ] Tests added to all affected modules
- [ ] Governance documentation updated across repos
- [ ] Builder agent contracts updated (if applicable)
- [ ] Architecture patterns updated

---

## 8. Evidence Trail

**Evidence Location**: `foreman/evidence/flci/FLCI-[YYYYMMDD]-[NNN]/`

**Evidence Files Required**:
- [ ] `failure-report.json` (structured failure data)
- [ ] `root-cause-analysis.md` (detailed RCA)
- [ ] `prevention-plan.json` (prevention actions and validation)
- [ ] `test-coverage-delta.json` (before/after test coverage)
- [ ] `completion-validation.md` (final validation that prevention is permanent)

**Evidence Status**: <!-- Complete | In Progress | Not Started -->

---

## 9. Related Issues/PRs

**Related Issues**:
<!-- Link to related issues -->


**Fix PR(s)**:
<!-- Link to pull requests that fix this issue -->


**Prevention PR(s)**:
<!-- Link to pull requests that implement permanent prevention -->


---

## 10. Foreman Validation

**Validated By**: <!-- Foreman Agent | Human -->  
**Validation Date**: <!-- YYYY-MM-DD -->  
**Validation Status**: <!-- ✅ Complete | ⏳ In Progress | ❌ Incomplete -->

**Validation Notes**:
<!-- Foreman or human validation of permanent prevention -->


---

## 11. Closure Criteria

This issue can ONLY be closed when ALL of the following are met:

- [ ] Immediate fix applied and validated
- [ ] Root cause fully understood and documented
- [ ] Permanent prevention implemented (tests/architecture/policy)
- [ ] Prevention validated (defect can never escape again)
- [ ] Lessons propagated to all affected areas
- [ ] Complete evidence trail generated
- [ ] Foreman validation passed
- [ ] Human approval obtained (for double-catastrophic or higher)

**Status**: <!-- OPEN | CLOSED -->

---

## Constitutional Authority

This workflow implements:
- **BUILD_PHILOSOPHY.md** — Section XIII (Failure Learning)
- **Foreman Agent Contract** — One-Time Failure Doctrine
- **Zero Regression Guarantee** — Permanent prevention requirement

**Doctrine**: *"A failure may occur once. Upon first occurrence, implement permanent prevention. Repeat occurrence without prevention is a catastrophic failure."*

---

## Additional Context

<!-- Add any other context, screenshots, logs, or information here -->


---

**Reporter**: <!-- Your name/handle -->  
**Date**: <!-- YYYY-MM-DD -->
