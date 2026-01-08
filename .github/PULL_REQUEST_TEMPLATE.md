# Pull Request

## Description

<!-- Provide a clear and concise description of the changes -->

## Issue Reference

<!-- Link to the issue this PR addresses -->
Fixes #

## Type of Change

<!-- Mark the relevant option with an 'x' -->

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Governance update
- [ ] Test addition/update
- [ ] Refactoring (no functional changes)

## Changes Made

<!-- List the specific changes made in this PR -->

-
-
-

## Testing

<!-- Describe the tests you ran to verify your changes -->

### Test Results

- **Test suite run**: YES / NO
- **All tests passing**: YES / NO
- **Test count**: ___ passing / ___ total
- **Pass rate**: ___%

### Test Status Declaration

<!-- REQUIRED: Choose ONE of the two valid status declarations -->

**Status**: [Select one]
- [ ] **100% tests passing** (all tests GREEN, zero failures, zero debt)
- [ ] **NOT READY - X tests failing** (specify count and details below)

### Failure Details (if NOT READY)

<!-- If NOT 100% passing, provide details below -->

**Failing tests**:
-
-

**Root cause**:


**Resolution plan**:


**ETA for 100% passing**:


## Policy Compliance

### POLICY-NO-ONLY-LANGUAGE Compliance

**Reference**: `governance/policies/POLICY-NO-ONLY-LANGUAGE.md`

- [ ] No banned minimizing language used ("only", "just", "minor", "non-blocking", "mostly", "almost", "small", "trivial", "simple", "easy")
- [ ] Status is accurate: "100% tests passing" OR "NOT READY - X tests failing"
- [ ] All test failures justified with root cause + resolution plan
- [ ] If < 100% pass rate, CS2 approval obtained before submission
- [ ] Acknowledgment: I have read and understand POLICY-NO-ONLY-LANGUAGE

### Zero-Tolerance Compliance

- [ ] Zero warnings in test output
- [ ] Zero test debt (no skipped, commented, or incomplete tests)
- [ ] Zero deprecated API usage
- [ ] All code has been checked for correctness
- [ ] Builder QA Report includes code checking evidence

### Governance Compliance

- [ ] Changes align with architecture specifications
- [ ] No modifications to protected governance paths (`governance/`, `.github/workflows/`)
- [ ] Design frozen before implementation (if applicable)
- [ ] QA-to-Red tests documented in QA_CATALOG.md (if applicable)
- [ ] Test removal governance followed (if tests removed)
- [ ] Warning handling policy followed (no suppressions without justification)

## Builder Checklist

- [ ] I have read the Builder Training Checklist (`governance/checklists/BUILDER_TRAINING_CHECKLIST.md`)
- [ ] I have passed the POLICY-NO-ONLY-LANGUAGE quiz (10/10)
- [ ] I understand constitutional requirements (T0-002, T0-003, T0-011)
- [ ] I have performed code checking on all generated/modified code
- [ ] I have run the test suite locally
- [ ] I have verified zero warnings
- [ ] I have verified 100% test pass rate (or documented NOT READY status)
- [ ] I have reviewed the changes for quality and correctness
- [ ] I am prepared to address FM review feedback immediately

## Documentation

- [ ] Documentation updated (if applicable)
- [ ] Architecture specs updated (if applicable)
- [ ] QA_CATALOG.md updated (if applicable)
- [ ] CHANGELOG updated (if applicable)
- [ ] README updated (if applicable)

## Breaking Changes

<!-- If this PR introduces breaking changes, describe them here -->

**Breaking changes**: YES / NO

**If YES, describe**:


## Additional Context

<!-- Add any other context about the PR here -->


---

## Builder Acknowledgment

By submitting this PR, I acknowledge that:

✅ I have completed all items in this checklist  
✅ I have read and complied with POLICY-NO-ONLY-LANGUAGE  
✅ My status reporting is accurate (no minimizing language)  
✅ I understand automatic rejection for policy violations  
✅ I commit to immediate remedy if issues are discovered  

**Builder**: @<!-- your-github-username -->  
**Date**: <!-- YYYY-MM-DD -->

---

## For Reviewers

### FM Review Checklist

- [ ] Language policy compliance verified (no banned words)
- [ ] Status declaration accurate (100% passing OR NOT READY with details)
- [ ] Test results verified
- [ ] Warning count verified (must be zero)
- [ ] Code checking evidence present
- [ ] Governance compliance verified
- [ ] Architecture alignment verified
- [ ] QA catalog alignment verified (if applicable)

### Review Outcome

- [ ] APPROVED for merge
- [ ] CHANGES REQUESTED
- [ ] REJECTED (policy violation)

**Reviewer**: @<!-- reviewer-github-username -->  
**Date**: <!-- YYYY-MM-DD -->

---

**END OF PR TEMPLATE**
