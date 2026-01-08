# POLICY-NO-ONLY-LANGUAGE

**Policy ID**: POLICY-NO-ONLY-LANGUAGE  
**Status**: ACTIVE  
**Enacted**: 2026-01-08  
**Authority**: CS2 Decision  
**Source**: PR APGI-cmy/maturion-foreman-office-app#901  
**Precedent**: PR APGI-cmy/maturion-foreman-office-app#504 (92% pass rate declared "COMPLETE")

---

## Summary

Minimizing language is banned when describing test failures, technical debt, or system status. All status reporting must be accurate and binary: either "100% tests passing" or "NOT READY - X tests failing".

---

## Problem Statement

### The "Only" Pattern

In PR APGI-cmy/maturion-foreman-office-app#504, a builder submitted work with:
- **92% pass rate** (589/638 tests passing)
- **49 tests failing**
- **Status declared**: "COMPLETE"
- **Language used**: "Only 49 tests failing"

This language pattern creates a psychological minimization of technical debt:
- "Only 5 tests failing" → Implies 5 is acceptable
- "Just documentation nits" → Implies documentation quality doesn't matter
- "Non-blocking failures" → Implies failures can be ignored

### Why This Is Dangerous

**Constitutional Violation**: The Governance Supremacy Rule (T0-002) states:
> "99% is 0%. There is no partial credit. A system that passes 99% of tests but fails 1% is a FAILED system."

**Build Philosophy Violation**: One-Time Build Correctness requires:
> "Builders MUST build-to-green exactly once. Non-green = INVALID, restart required."

**Reality**: 
- 92% pass rate = 8% failure rate
- 49 failing tests = 49 unmet requirements
- "COMPLETE" = FALSE (objectively incorrect)

---

## Banned Language

### Absolutely Prohibited

When describing test failures, build status, or technical debt, the following words are **BANNED**:

❌ **"only"** - Minimizes scale of failure  
❌ **"just"** - Trivializes technical debt  
❌ **"minor"** - Subjective assessment of objective failure  
❌ **"non-blocking"** - All failures block (Zero Test Debt rule)  
❌ **"mostly"** - Implies partial success is acceptable  
❌ **"almost"** - Near-success is still failure  
❌ **"small"** - Scale is irrelevant, failure is binary  
❌ **"trivial"** - No failure is trivial  
❌ **"simple"** - Complexity is irrelevant, fix is required  
❌ **"easy"** - Ease of fix doesn't justify deferral  

### Context Examples

**Prohibited Patterns**:
```
❌ "Only 5 tests failing"
❌ "Just some documentation issues"
❌ "Minor type errors"
❌ "Non-blocking linting warnings"
❌ "Mostly passing (95%)"
❌ "Almost done (98% complete)"
❌ "Small refactoring needed"
❌ "Trivial fixes required"
❌ "Simple updates pending"
❌ "Easy to fix later"
```

**Why They're Prohibited**:
- They create false confidence
- They normalize technical debt
- They violate zero-tolerance policy
- They enable test dodging
- They corrupt governance language

---

## Required Language

### Accurate Status Reporting

**Only two valid status declarations**:

✅ **"100% tests passing"** - Objective, verifiable, GREEN  
✅ **"NOT READY - X tests failing"** - Objective, verifiable, RED  

### Detailed Failure Reporting

When reporting failures, use:

✅ **"X tests failing"** - Objective count  
✅ **"Test suite status: RED"** - Clear binary state  
✅ **"Work incomplete: X issues remain"** - Accurate assessment  
✅ **"Failures identified: [list]"** - Transparent enumeration  
✅ **"Root cause: [description]"** - Technical analysis  
✅ **"Resolution plan: [steps]"** - Action plan  

### Example: Correct Reporting

**Before (Prohibited)**:
> "Build is mostly complete. Only 5 tests failing, just minor issues. Non-blocking."

**After (Required)**:
> "Build status: NOT READY - 5 tests failing.
> 
> Failing tests:
> - test_authentication: AssertionError on line 42
> - test_validation: TypeError - expected str, got int
> - test_integration: Connection timeout
> - test_api_endpoint: 404 response (expected 200)
> - test_data_integrity: Null value in required field
> 
> Root cause: Authentication service not fully implemented.
> 
> Resolution plan:
> 1. Implement authentication service (2 hours)
> 2. Fix validation type mismatch (30 minutes)
> 3. Configure integration test environment (1 hour)
> 4. Update API endpoint routing (1 hour)
> 5. Add null checks to data layer (30 minutes)
> 
> Estimated completion: 5 hours
> Status: NOT READY until 100% tests passing."

---

## Enforcement

### Automatic Rejection

Any PR, report, or status update containing banned language will be:

1. **AUTOMATICALLY REJECTED** (no review, no discussion)
2. **RETURNED TO SENDER** with this policy reference
3. **REQUIRED RE-SUBMISSION** with accurate language

### No Exceptions

**There are ZERO exceptions to this policy**, including:
- Urgent work
- Minor changes
- Documentation updates
- Experimental features
- Proof-of-concept code
- Internal testing

### CS2 Override Only

**Only CS2 (Johan Ras)** can approve an exception, and ONLY with:
- Written justification
- Risk assessment
- Time-bound constraint
- Explicit governance waiver

---

## Rationale

### Linguistic Integrity

**Language shapes thought**. Minimizing language:
- Corrupts accurate assessment
- Normalizes failure acceptance
- Enables rationalization
- Weakens governance enforcement

### Constitutional Alignment

**T0-002 Governance Supremacy**: 99% is 0%  
**T0-003 Zero Test Debt**: All tests GREEN or documented  
**T0-011 Build-to-Green**: 100% pass = GREEN, <100% = INVALID  

### Historical Evidence

**PR APGI-cmy/maturion-foreman-office-app#504**:
- Builder used "only 49 failing" language
- Declared work "COMPLETE"
- Submitted for merge approval
- 92% pass rate (objectively RED)
- **Result**: Catastrophic governance violation, required full rejection

**Lesson**: Minimizing language directly enables test dodging.

---

## Training & Acknowledgment

### Builder Requirements

Before ANY PR submission, builders MUST:

1. **Read this policy** in full
2. **Study BOOTSTRAP-TEST-DODGING-001** case study
3. **Pass policy quiz** (10/10 required)
4. **Sign acknowledgment** of banned language policy

### Quiz Sample Questions

1. **Q**: Can you say "only 3 tests failing" if you plan to fix them soon?  
   **A**: NO - banned language regardless of intent

2. **Q**: Is 99% pass rate acceptable?  
   **A**: NO - 99% is 0% (Governance Supremacy Rule)

3. **Q**: What are the only two valid status declarations?  
   **A**: "100% tests passing" OR "NOT READY - X tests failing"

4. **Q**: Can you use "minor issues" if the fixes are simple?  
   **A**: NO - "minor" is banned, simplicity doesn't justify deferral

5. **Q**: Who can approve exceptions to this policy?  
   **A**: Only CS2 (Johan Ras) with written justification

---

## Cross-References

**Related Policies**:
- `governance/policies/zero-test-debt-constitutional-rule.md` - Zero Test Debt requirement
- `governance/policies/governance-supremacy-rule.md` - 99% is 0% principle
- `governance/policies/ZERO_WARNING_TEST_DEBT_IMMEDIATE_REMEDY_DOCTRINE.md` - Warning governance

**Related Documents**:
- `BUILD_PHILOSOPHY.md` - One-Time Build Correctness
- `governance/zero-debt-campaign/GOVERNANCE_LEARNING_BRIEF.md` - Builder education
- `bootstrap/learnings/BOOTSTRAP-TEST-DODGING-001.md` - PR #504 case study

**Governance Canon**:
- T0-002: Governance Supremacy Rule
- T0-003: Zero Test Debt Constitutional Rule
- T0-011: Build-to-Green Enforcement Spec

---

## Implementation Checklist

For repository adoption:

- [ ] Copy this policy to `governance/policies/POLICY-NO-ONLY-LANGUAGE.md`
- [ ] Copy bootstrap learning to `bootstrap/learnings/BOOTSTRAP-TEST-DODGING-001.md`
- [ ] Update `GOVERNANCE_LEARNING_BRIEF.md` with policy reference
- [ ] Update builder training checklist
- [ ] Add to PR template compliance section
- [ ] Train all builders on policy
- [ ] Enforce in code review process
- [ ] Integrate into CI/CD gates (future)

---

## Revision History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-01-08 | CS2 (Johan Ras) | Initial policy enactment |

---

**Status**: ACTIVE  
**Authority**: CS2 Decision 2026-01-08  
**Enforcement**: MANDATORY, IMMEDIATE, AUTOMATIC  
**Exceptions**: ZERO (CS2 override only)

---

*END OF POLICY*
