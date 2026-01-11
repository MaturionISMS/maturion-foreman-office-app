# Protocol Violation Incident Report

**Incident ID**: VIOLATION_YYYY_MM_DD_[SHORT_DESCRIPTION]  
**Date Detected**: YYYY-MM-DD  
**Detected By**: [Agent Name or Role]  
**Status**: [OPEN | INVESTIGATING | RESOLVED | ESCALATED]

---

## Incident Summary

**Violation Type**: [Select from list below]
- [ ] No PREHANDOVER_PROOF provided
- [ ] Incomplete 7-step verification
- [ ] Handover without local execution
- [ ] Green attestation with failures
- [ ] Missing evidence
- [ ] Bypassing protocol
- [ ] Incomplete remediation
- [ ] Other: [Describe]

**Severity**: [Select one]
- [ ] MINOR - First occurrence, no impact, good faith error
- [ ] MODERATE - Repeat occurrence or minor impact
- [ ] MAJOR - Bypass, false attestation, or production impact

**PR Number**: #[NUMBER]  
**Branch**: [branch-name]  
**Agent Involved**: [Agent Name/Role]  
**Commit Hash**: [commit-hash]

---

## Violation Details

### What Happened

[Detailed description of the violation]

**Expected Behavior**:
- [What should have happened according to protocol]

**Actual Behavior**:
- [What actually happened]

**Evidence of Violation**:
- [Links to PR, commits, comments, logs showing violation]

---

## Impact Assessment

**Production Impact**: [YES | NO]  
**Description**: [If yes, describe impact]

**Rework Required**: [YES | NO]  
**Effort**: [If yes, estimate effort]

**Downstream Dependencies Affected**: [YES | NO]  
**Description**: [If yes, describe affected systems/agents]

**CI/CD Pipeline Impact**: [YES | NO]  
**Description**: [If yes, describe impact]

---

## Root Cause Analysis

### Contributing Factors

1. **Primary Cause**: [What directly caused the violation]

2. **Contributing Factors**: [What made the violation more likely]
   - [Factor 1]
   - [Factor 2]
   - [Factor 3]

3. **Systemic Issues**: [Any deeper systemic problems identified]

### Why It Happened

[Detailed explanation of why the violation occurred]

**Agent Understanding**: [Did agent understand protocol? YES/NO]  
**Training Gap**: [Was this a training issue? YES/NO]  
**Process Gap**: [Was this a process/tooling issue? YES/NO]  
**Time Pressure**: [Was deadline pressure a factor? YES/NO]

---

## Resolution

### Immediate Actions Taken

- [ ] Violation documented in this file
- [ ] PR blocked/reverted (if not merged)
- [ ] Agent notified
- [ ] FM notified
- [ ] Other: [Describe]

### Corrective Actions

**Short-term** (fix this specific violation):
1. [Action 1]
2. [Action 2]
3. [Action 3]

**Status**: [COMPLETE | IN_PROGRESS | PLANNED]  
**Completion Date**: [YYYY-MM-DD or N/A]

### Preventive Measures

**Long-term** (prevent recurrence):
1. [Measure 1]
2. [Measure 2]
3. [Measure 3]

**Responsible**: [Agent/Role]  
**Target Date**: [YYYY-MM-DD]  
**Status**: [PLANNED | IN_PROGRESS | COMPLETE]

---

## Agent Accountability

**Agent Involved**: [Agent Name/Role]  
**Violation Count**: [1st | 2nd | 3rd | 4th+]  
**Accountability Action**: [Select one]
- [ ] DOCUMENTATION - First violation, documented only
- [ ] RETRAINING - Required protocol retraining
- [ ] REVIEW - FM accountability review
- [ ] ESCALATION - Escalated to Johan (CS2)
- [ ] Other: [Describe]

**Retraining Status**: [COMPLETE | SCHEDULED | N/A]  
**Retraining Date**: [YYYY-MM-DD or N/A]

---

## Timeline

| Date | Event | Actor | Notes |
|------|-------|-------|-------|
| YYYY-MM-DD | Violation occurred | [Agent] | [Details] |
| YYYY-MM-DD | Violation detected | [Detector] | [How detected] |
| YYYY-MM-DD | Incident documented | [Documenter] | This file created |
| YYYY-MM-DD | Escalation (if any) | [Who] | [To whom] |
| YYYY-MM-DD | Resolution started | [Agent] | [Actions] |
| YYYY-MM-DD | Resolution complete | [Agent] | [Outcome] |

---

## Lessons Learned

### What Went Well

- [Positive aspect 1]
- [Positive aspect 2]

### What Needs Improvement

- [Improvement area 1]
- [Improvement area 2]

### Recommendations

1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]

---

## Related Documentation

**Related Incidents**: [List any related violations or incidents]

**Related PRs**: [List any related PRs]

**Related Issues**: [List any related GitHub issues]

**Canonical References**:
- EXECUTION_BOOTSTRAP_PROTOCOL.md
- EXECUTION_BOOTSTRAP_PROTOCOL_MONITORING_AND_ENFORCEMENT.md
- PREHANDOVER_PROOF_TEMPLATE.md

---

## Escalation Path

**Escalated**: [YES | NO]  
**Escalated To**: [FM | Johan (CS2) | N/A]  
**Escalation Date**: [YYYY-MM-DD or N/A]  
**Escalation Reason**: [Describe or N/A]  
**Escalation Response**: [Describe or N/A]

---

## Closure

**Incident Status**: [OPEN | RESOLVED | ESCALATED]  
**Closed By**: [Name/Role]  
**Closed Date**: [YYYY-MM-DD or N/A]  
**Resolution Summary**: [Brief summary of resolution]

**Verification**:
- [ ] Root cause documented
- [ ] Corrective actions complete
- [ ] Preventive measures planned
- [ ] Agent accountability addressed
- [ ] Lessons learned captured
- [ ] Ready for quarterly report inclusion

---

## Quarterly Report Metrics

**Quarter**: Q[N] YYYY  
**Included in Report**: [YES | NO | PENDING]  
**Report Date**: [YYYY-MM-DD or N/A]

---

## Document Control

**Created By**: [Name/Role]  
**Created Date**: YYYY-MM-DD  
**Last Updated**: YYYY-MM-DD  
**Version**: 1.0

---

**END OF INCIDENT REPORT TEMPLATE**
