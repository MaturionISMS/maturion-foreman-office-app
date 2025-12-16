# Catastrophic Failure Completion Validation

**Failure ID**: FLCI-YYYYMMDD-NNN  
**Validation Date**: YYYY-MM-DD  
**Validated By**: <Validator Name (Foreman | Human)>

---

## Closure Criteria Checklist

### 1. Immediate Fix
- [ ] Fix applied and validated
- [ ] Fix PR merged: <Link to PR>
- [ ] Production deployment completed
- [ ] Users notified (if applicable)

### 2. Root Cause Understanding
- [ ] Root cause fully documented
- [ ] Root cause analysis completed: `root-cause-analysis.md`
- [ ] Contributing factors identified
- [ ] Escape analysis completed (why it escaped B2G)

### 3. Permanent Prevention Implemented
- [ ] Tests added (minimum 1 required)
- [ ] Architecture updated (if required)
- [ ] Governance/policy updated (if required)
- [ ] Prevention mechanism documented

### 4. Prevention Validated
- [ ] New tests passing
- [ ] CI/CD updated with new tests
- [ ] Prevention mechanism tested
- [ ] Cannot reproduce original failure

### 5. Lessons Propagated
- [ ] Similar code/patterns identified
- [ ] Tests added to affected modules
- [ ] Documentation updated across repos
- [ ] Builder contracts updated (if applicable)
- [ ] Architecture patterns updated (if applicable)

### 6. Evidence Trail Complete
- [ ] `failure-report.json` - Complete
- [ ] `root-cause-analysis.md` - Complete
- [ ] `prevention-plan.json` - Complete
- [ ] `test-coverage-delta.json` - Complete
- [ ] `completion-validation.md` (this file) - Complete

### 7. Foreman Validation
- [ ] All criteria met
- [ ] Evidence trail complete
- [ ] Prevention permanent
- [ ] No outstanding issues

### 8. Human Approval
- [ ] Human review completed (required for double-catastrophic+)
- [ ] Human approval obtained
- [ ] Approval documented

---

## Evidence Summary

### Failure Report
**Location**: `foreman/evidence/flci/FLCI-YYYYMMDD-NNN/failure-report.json`  
**Status**: ✅ Complete  
**Severity**: <catastrophic | double-catastrophic | multi-catastrophic>  
**Root Cause**: <primary_bucket>

### Prevention Actions

#### Tests Added
| Type | File | Test Name | Purpose |
|------|------|-----------|---------|
| \<type\> | \<file\> | \<name\> | \<purpose\> |

**Total Tests Added**: N

#### Architecture Updates
<List architecture updates, or "None required">

#### Governance Updates
<List governance updates, or "None required">

### Test Coverage Delta
**Before**: X% coverage (N tests)  
**After**: Y% coverage (M tests)  
**Improvement**: +Z% (+K tests)

---

## Prevention Mechanism Validation

### How This Will Be Caught Forever

<Detailed explanation of the permanent mechanism>

### Validation Evidence

1. <Link to test run showing new tests pass>
2. <Link to CI passing with new tests>
3. <Link to coverage report showing improvement>

### Attempted Reproduction

**Attempt Date**: YYYY-MM-DD  
**Result**: <Failure cannot be reproduced | Caught by new tests | Other>  
**Notes**: <Validation notes>

---

## Lesson Propagation Status

### Affected Areas Identified
1. <Module/Repository 1>
2. <Module/Repository 2>

### Propagation Actions Taken
1. <Action 1>
2. <Action 2>

### Propagation Evidence
- <Link to PR 1>
- <Link to PR 2>

---

## Final Assessment

### Overall Status
**Status**: <✅ COMPLETE | ⏳ IN PROGRESS | ❌ INCOMPLETE>

### Blocking Issues
<List any blocking issues, or "None">

### Completion Notes
<Any final notes about completion>

---

## Doctrine Compliance

This catastrophic failure resolution complies with:

- ✅ **One-Time Failure Doctrine** - Permanent prevention implemented
- ✅ **Zero Regression Guarantee** - Tests prevent repeat
- ✅ **Build Philosophy** - Learning from failure
- ✅ **Evidence Requirements** - Complete trail documented

---

## Approval

**Foreman Validation**: <✅ APPROVED | ❌ REJECTED>  
**Foreman Notes**: <Validation notes>  
**Foreman Timestamp**: YYYY-MM-DDTHH:MM:SS.sssZ

**Human Approval**: <✅ APPROVED | ❌ REJECTED | N/A>  
**Human Approver**: <Name>  
**Human Notes**: <Approval notes>  
**Human Timestamp**: YYYY-MM-DD

---

## Issue Closure

**Issue Number**: <GitHub Issue #>  
**Closure Date**: YYYY-MM-DD  
**Closed By**: <Person>

**Status**: <CLOSED | OPEN>

---

*This validation confirms that the catastrophic failure has been permanently prevented and all lessons have been captured and propagated.*
