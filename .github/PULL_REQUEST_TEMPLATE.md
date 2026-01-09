# Pull Request

## Description

<!-- Provide a clear and concise description of what this PR does -->

## Type of Change

<!-- Mark relevant items with an 'x' -->

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Governance/policy update
- [ ] Test improvement
- [ ] Refactoring (no functional changes)

## Changes Made

<!-- List the key changes made in this PR -->

-
-
-

## Testing

<!-- Describe the testing you've performed -->

### Test Results

- [ ] All tests passing (100% GREEN)
- [ ] Zero warnings in test output
- [ ] Zero RED tests (excluding documented QA-to-Red)
- [ ] No skipped or commented tests
- [ ] Code checking performed (logical correctness verified)

**Test Command**: `pytest tests/` (or specify subset)

**Test Output Summary**:
```
<!-- Paste relevant test output here -->
Tests passing: X/X (100%)
Warnings: 0
```

## Policy Compliance

<!-- MANDATORY: All items must be checked before submission -->

### Language Policy (POLICY-NO-ONLY-LANGUAGE)

- [ ] No banned minimizing language used ("only", "just", "minor", "non-blocking")
- [ ] Status is accurate: "100% tests passing" OR "NOT READY - X tests failing"
- [ ] All test failures justified with root cause + resolution plan
- [ ] If < 100% pass rate, CS2 approval obtained before submission

**Reference**: POLICY-NO-ONLY-LANGUAGE (`governance/policies/POLICY-NO-ONLY-LANGUAGE.md`)

### Quality Standards

- [ ] Zero-tolerance compliance: No warnings, no debt tests
- [ ] Build-to-Green: Work is complete and verified GREEN
- [ ] Code review: All generated code reviewed for correctness
- [ ] No test removal without proper governance authorization
- [ ] No warning suppression without FM approval
- [ ] Constitutional compliance: All Tier-1 requirements preserved (BL-024)
- [ ] If procedural guidance adapted: Documented with justification (BL-024)

### Documentation

- [ ] Documentation updated (if applicable)
- [ ] Architecture documentation updated (if applicable)
- [ ] QA catalog updated (if applicable)
- [ ] Changes reflected in relevant governance docs (if applicable)

## Breaking Changes

<!-- If this PR introduces breaking changes, describe them here -->

**Breaking Changes**: None / [Describe]

**Migration Path**: [Describe how to migrate if applicable]

## Dependencies

<!-- List any dependencies required for this PR -->

**Dependencies**: None / [List]

**Blocks**: [List any issues this PR blocks]

**Blocked By**: [List any issues blocking this PR]

## Checklist

<!-- ALL items must be checked before requesting review -->

- [ ] My code follows the project's coding standards
- [ ] I have performed a self-review of my code
- [ ] I have commented my code where necessary
- [ ] I have made corresponding changes to documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] All tests pass locally (100% GREEN)
- [ ] I have read POLICY-NO-ONLY-LANGUAGE and comply
- [ ] I have not used minimizing language in this PR
- [ ] I acknowledge the 100% GREEN mandate (99% = 0%)
- [ ] I understand Constitutional Sandbox Pattern (BL-024): Tier-1 vs Tier-2
- [ ] If I adapted procedural guidance: I documented my judgment with rationale

## Status Declaration

<!-- Choose ONE status -->

**Current Status**: 
- [ ] ✅ **COMPLETE** - 100% tests passing, zero warnings, ready for merge
- [ ] ❌ **NOT READY** - [Specify number] tests failing, [Specify number] warnings

<!-- If NOT READY, explain below -->

**Issues Preventing GREEN**:
-
-

**Resolution Plan**:
-
-

**Estimated Time to GREEN**: [X hours/days]

## Additional Notes

<!-- Any additional information that reviewers should know -->

---

## For Reviewers

### Review Checklist

- [ ] Code follows project standards
- [ ] Tests are comprehensive and passing
- [ ] No warnings present
- [ ] No minimizing language used
- [ ] Documentation is adequate
- [ ] Changes align with architecture
- [ ] No governance violations detected
- [ ] No test dodging patterns observed
- [ ] Constitutional compliance verified (BL-024): Tier-1 requirements preserved
- [ ] If procedural adaptations made: Justification is documented

### Approval Criteria

**PR can be approved ONLY if:**

1. ✅ 100% tests passing (no exceptions)
2. ✅ Zero warnings in output
3. ✅ No minimizing language used
4. ✅ All policy compliance items checked
5. ✅ Status accurately declared
6. ✅ Documentation complete

**If any criteria not met**: Request changes, do NOT approve.

---

## References

**Governance Policies**:
- [Constitutional Sandbox Pattern (BL-024)](https://github.com/APGI-cmy/maturion-foreman-governance/blob/main/governance/canon/CONSTITUTIONAL_SANDBOX_PATTERN.md)
- [POLICY-NO-ONLY-LANGUAGE](governance/policies/POLICY-NO-ONLY-LANGUAGE.md)
- [Zero Test Debt Rule](governance/policies/zero-test-debt-constitutional-rule.md)
- [Governance Supremacy Rule](governance/policies/governance-supremacy-rule.md)
- [BUILD_PHILOSOPHY.md](BUILD_PHILOSOPHY.md)

**Bootstrap Learnings**:
- [BOOTSTRAP-TEST-DODGING-001](bootstrap/learnings/BOOTSTRAP-TEST-DODGING-001.md)

**Training**:
- [Builder Training Checklist](governance/BUILDER_TRAINING_CHECKLIST.md)

---

**By submitting this PR, I acknowledge:**

I have read and comply with POLICY-NO-ONLY-LANGUAGE and Constitutional Sandbox Pattern (BL-024). I understand that use of minimizing language or submission of work with warnings/debt will result in immediate PR rejection. I acknowledge the 100% GREEN mandate is non-negotiable. I understand Tier-1 constitutional requirements are immutable, and any Tier-2 procedural adaptations are documented with justification.

**Builder Signature**: @[username]  
**Date**: [YYYY-MM-DD]
