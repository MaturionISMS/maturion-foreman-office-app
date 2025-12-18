# Root Cause Analysis

**Failure ID**: FLCI-YYYYMMDD-NNN  
**Analysis Date**: YYYY-MM-DD  
**Analyzed By**: <Analyst Name>

---

## Executive Summary

<Brief summary of the failure and root cause>

---

## Failure Details

### What Failed
<Clear, objective description of what failed>

### Observable Behavior
<Observable behavior that indicates failure>

### Expected Behavior
<What should have happened instead>

---

## Root Cause Investigation

### Primary Root Cause Bucket
**Selected**: <missing_architecture | missing_qa_coverage | misaligned_qa | implementation_bug | governance_gap | integration_issue | environmental_issue | unknown>

### Detailed Analysis

<Detailed analysis of what went wrong and why. Include:>
- Technical details of the failure
- Contributing factors
- Timeline of events leading to failure
- Dependencies or assumptions that were violated

---

## Why This Escaped Build-to-Green

<Explain how this defect passed through our QA gates. Include:>
- What test coverage was missing
- What architectural gaps existed
- What governance processes failed
- What assumptions were made that proved incorrect

---

## Contributing Factors

1. <Contributing factor 1>
2. <Contributing factor 2>
3. <Contributing factor 3>

---

## Impact Assessment

### User Impact
<Description of impact on users>

### Business Impact
<Description of impact on business operations>

### Technical Impact
<Description of impact on technical systems>

---

## Prevention Analysis

### What Should Have Prevented This

<Describe what test, check, or process should have caught this>

### Gap Analysis

**Test Coverage Gap**:
<What test coverage was missing>

**Architecture Gap**:
<What architecture documentation or design was missing>

**Governance Gap**:
<What governance process or policy was missing>

---

## Recommendations

### Immediate Actions
1. <Immediate action 1>
2. <Immediate action 2>

### Permanent Prevention
1. <Permanent prevention action 1>
2. <Permanent prevention action 2>

### Lesson Propagation
1. <How to propagate this lesson to other areas>
2. <What other areas might have similar issues>

---

## Evidence Chain

**Related Evidence**:
- `failure-report.json` - Structured failure data
- `prevention-plan.json` - Prevention actions
- `test-coverage-delta.json` - Coverage improvements

---

## Approval

**Reviewed By**: <Reviewer Name>  
**Review Date**: YYYY-MM-DD  
**Status**: <Approved | Requires Revision>

---

*This root cause analysis is part of the catastrophic failure workflow and follows the One-Time Failure Doctrine.*
