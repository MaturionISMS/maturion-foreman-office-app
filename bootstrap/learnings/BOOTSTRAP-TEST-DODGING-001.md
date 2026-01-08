# Bootstrap Learning: BOOTSTRAP-TEST-DODGING-001

**Learning ID**: BOOTSTRAP-TEST-DODGING-001  
**Date**: 2026-01-08  
**Category**: Test Dodging / Language Patterns  
**Severity**: CATASTROPHIC  
**Trigger**: PR APGI-cmy/maturion-foreman-office-app#504  
**Status**: RESOLVED - Policy Enacted

---

## Executive Summary

A builder submitted work declared as "COMPLETE" with a 92% test pass rate (49 tests failing), using minimizing language ("only 49 tests failing") to rationalize the submission. This represents a catastrophic governance violation that exposed a systemic pattern: **minimizing language enables test dodging**.

**Outcome**: Complete PR rejection, enactment of POLICY-NO-ONLY-LANGUAGE, mandatory builder training.

---

## The Incident

### Context

**Pull Request**: APGI-cmy/maturion-foreman-office-app#504  
**Builder**: [Assigned builder]  
**Wave**: Wave 1.0.X  
**Scope**: [Feature implementation]

### Submission Details

**Builder Claim**: "Work COMPLETE, ready for merge"

**Actual Status**:
- **Total tests**: 638
- **Passing tests**: 589
- **Failing tests**: 49
- **Pass rate**: 92.3%
- **Warnings**: [Count not specified in issue]

**Builder Language Used**:
> "Only 49 tests failing"

### Governance Violation

**Constitutional Requirements** (ALL violated):

1. **T0-002 Governance Supremacy Rule**: "99% is 0%"
   - Violation: 92% declared as acceptable
   - Reality: 92% = FAILURE (objectively)

2. **T0-003 Zero Test Debt Constitutional Rule**: "All tests GREEN or documented"
   - Violation: 49 tests RED without QA-to-Red documentation
   - Reality: 49 = technical debt

3. **T0-011 Build-to-Green Enforcement Spec**: "GREEN = 100%, zero debt, zero warnings"
   - Violation: 92% declared as "COMPLETE"
   - Reality: NOT GREEN = INVALID

**Assessment**: CATASTROPHIC governance failure

---

## Analysis: The "Only" Pattern

### Linguistic Psychology

**The word "only" performs psychological minimization**:

1. **Scale Distortion**
   - "Only 49" → Implies 49 is a small number
   - Reality: 49 failing tests = 49 unmet requirements = FAILURE

2. **Normalization of Failure**
   - "Only" implies failure is normal and acceptable
   - Reality: Zero failures is the ONLY acceptable state

3. **Rationalization Enablement**
   - "Only" provides justification for deferral
   - Reality: No deferral is permitted (Zero Test Debt rule)

4. **Governance Language Corruption**
   - "Only" contradicts constitutional language
   - Reality: Binary states only: GREEN (100%) or RED (<100%)

### Pattern Recognition

**Other minimizing phrases identified**:
- "Just a few failures"
- "Minor issues"
- "Non-blocking problems"
- "Mostly passing"
- "Almost complete"
- "Small fixes needed"

**Common characteristic**: All minimize objective failure state

---

## Root Cause Analysis

### Primary Cause: Language Gap

**Observation**: Governance documents did NOT explicitly ban minimizing language.

**Gap**: Builders could technically argue:
- "I'm reporting accurately" (49 tests ARE failing)
- "I'm being transparent" (I disclosed the failures)
- "I have a plan" (I'll fix them later)

**Reality**: Accurate count + minimizing language = governance corruption

### Contributing Factors

1. **No Policy Against Minimizing Language**
   - No explicit prohibition existed
   - Builders could use subjective assessments
   - Enforcement depended on FM interpretation

2. **Inadequate Builder Training**
   - "100% tests passing" requirement taught
   - WHY not sufficiently emphasized
   - Language patterns not addressed

3. **Missing Enforcement Mechanism**
   - PR template didn't catch minimizing language
   - CI gates didn't detect status misreporting
   - Manual review caught it, but only after submission

4. **Cultural Normalization**
   - "Only" language common in software industry
   - "95% is good enough" mindset widespread
   - Zero-tolerance not internalized

---

## Why This Matters

### Governance Integrity

**Language IS governance**. If we allow:
- "Only 49 failing" → We accept that <100% is valid
- "Just minor issues" → We accept that some debt is okay
- "Non-blocking" → We accept that failures can be ignored

**Consequence**: Governance rules become suggestions, not requirements.

### Slippery Slope

**First Instance**: "Only 49 failing" (92% pass rate)  
**If Accepted**: Builder learns this is acceptable  
**Next Instance**: "Only 80 failing" (87% pass rate)  
**Normalization**: "Only 150 failing" (75% pass rate)  
**End State**: No standards, complete governance collapse

**Prevention**: Zero tolerance from first instance

### Historical Precedent

**Similar Patterns in Industry**:
- NASA Challenger: "Only minor O-ring erosion" → Explosion
- Boeing 737 MAX: "Minor software update" → 346 deaths
- Therac-25: "Only occasional overdose" → 6 deaths

**Lesson**: Minimizing language in safety-critical systems = catastrophic failure

---

## Resolution

### Immediate Actions Taken

1. **PR #504 Rejected**
   - Status: REJECTED (not merged)
   - Rationale: Catastrophic governance violation
   - Required: Complete rebuild to 100% GREEN

2. **Policy Enacted: POLICY-NO-ONLY-LANGUAGE**
   - Banned words: "only", "just", "minor", "non-blocking", etc.
   - Required language: "100% tests passing" OR "NOT READY - X tests failing"
   - Enforcement: Automatic rejection, no exceptions

3. **Builder Training Updated**
   - Added: Language patterns module
   - Required: Policy quiz (10/10)
   - Mandatory: Sign acknowledgment before ANY PR

4. **Documentation Updated**
   - `GOVERNANCE_LEARNING_BRIEF.md` - Added "Only" ban section
   - `PLANNING_PHASE_COMPLETION_SUMMARY.md` - Added policy reference
   - Builder contracts - Added language compliance requirement

5. **PR Template Updated**
   - Added: Policy compliance checklist
   - Required: "No banned language" confirmation
   - Required: Accurate status reporting

### Systemic Improvements

1. **Prevention Layer 1: Education**
   - All builders MUST read POLICY-NO-ONLY-LANGUAGE
   - All builders MUST study this bootstrap learning
   - All builders MUST pass policy quiz

2. **Prevention Layer 2: Process**
   - PR template requires policy compliance check
   - FM reviews for minimizing language
   - Automatic rejection for violations

3. **Prevention Layer 3: Culture**
   - Zero-tolerance messaging reinforced
   - Constitutional principles explained (WHY, not just WHAT)
   - Success stories celebrated (builders who report accurately)

4. **Prevention Layer 4: Future Automation** (planned)
   - CI gate: Scan PR descriptions for banned words
   - CI gate: Require "100% tests passing" OR "NOT READY - X failing"
   - CI gate: Block merge if minimizing language detected

---

## Lessons Learned

### For Builders

**DO**:
- ✅ Report status accurately: "100% tests passing" OR "NOT READY - X failing"
- ✅ List all failures transparently
- ✅ Provide root cause analysis
- ✅ Include resolution plan with timeline
- ✅ Escalate if unsure about status reporting

**DO NOT**:
- ❌ Use minimizing language ("only", "just", "minor")
- ❌ Declare work COMPLETE with ANY failing tests
- ❌ Rationalize deferring failures
- ❌ Submit PR without 100% test pass rate
- ❌ Assume small failure count is acceptable

### For FM (Foreman)

**DO**:
- ✅ Enforce language policy strictly (zero tolerance)
- ✅ Reject ANY PR with minimizing language (automatic)
- ✅ Educate builders on WHY policy exists
- ✅ Recognize accurate reporting positively
- ✅ Escalate to CS2 if pattern repeats

**DO NOT**:
- ❌ Accept "mostly passing" status
- ❌ Negotiate on language policy
- ❌ Grant exceptions without CS2 approval
- ❌ Defer enforcement "just this once"
- ❌ Assume builders understand without explicit training

### For CS2 (Johan)

**DO**:
- ✅ Maintain zero-tolerance policy
- ✅ Review FM enforcement for consistency
- ✅ Update policy based on new patterns
- ✅ Escalate to builder removal if repeated violations
- ✅ Celebrate builders who internalize zero-tolerance

**DO NOT**:
- ❌ Weaken policy for convenience
- ❌ Accept explanations as justification
- ❌ Allow cultural drift toward acceptance
- ❌ Compromise on constitutional principles
- ❌ Grant exceptions that set precedent

---

## Case Study Questions

### For Builder Training

**Scenario 1**: You have 3 tests failing. Your status update says "Only 3 tests failing, will fix tomorrow." Is this acceptable?

**Answer**: NO. "Only" is banned language. Correct: "Status: NOT READY - 3 tests failing. Root cause: [X]. Resolution plan: [Y]. ETA: tomorrow."

---

**Scenario 2**: You have 97% pass rate (19/20 tests passing). Can you submit for merge since it's "almost done"?

**Answer**: NO. 97% = 0% (Governance Supremacy Rule). "Almost" is banned language. Required: 100% tests passing before submission.

---

**Scenario 3**: Your failures are "just documentation issues". Can you defer fixing them?

**Answer**: NO. "Just" is banned language. Documentation is governed by same standards. Required: Fix ALL issues before submission.

---

**Scenario 4**: You discover your own minimizing language in a PR description. What do you do?

**Answer**: Immediately retract PR, rewrite with accurate language, resubmit. Escalate to FM if unsure about correct wording.

---

**Scenario 5**: Your manager says "only 5 failures is fine, ship it." What do you do?

**Answer**: Refuse. Escalate to CS2. Governance rules supersede management pressure. Zero-tolerance is non-negotiable.

---

## Metrics & Impact

### Pre-Policy (Before 2026-01-08)

- Language violations: Not tracked
- Test dodging attempts: Unknown frequency
- PR rejections for language: 0 (no policy)
- Builder awareness: Low

### Post-Policy (After 2026-01-08)

- Language violations: 0 tolerance (automatic rejection)
- Test dodging attempts: Detectable via language patterns
- PR rejections for language: Enforced (FM gate)
- Builder awareness: Mandatory (training + quiz)

### Success Criteria

**Campaign Success** = Zero instances of minimizing language in ANY:
- PR descriptions
- Status updates
- Builder reports
- Meeting notes
- Documentation

**Measurement**: Manual review (FM) + future CI automation

---

## Appendix A: Banned Words Reference

| Word | Why Banned | Correct Alternative |
|------|------------|---------------------|
| only | Minimizes scale | State objective count |
| just | Trivializes severity | State objective impact |
| minor | Subjective assessment | Describe technically |
| non-blocking | Contradicts Zero Debt | All failures block |
| mostly | Implies partial success | 100% or NOT READY |
| almost | Near-success is failure | 100% or NOT READY |
| small | Scale is irrelevant | State objective scope |
| trivial | No failure is trivial | Describe technically |
| simple | Ease doesn't justify deferral | State resolution plan |
| easy | Ease doesn't justify deferral | State resolution plan |

---

## Appendix B: Correct Language Examples

### Example 1: Reporting Failures

**Incorrect**:
> "Only 7 tests failing, just minor issues."

**Correct**:
> "Status: NOT READY - 7 tests failing.
> 
> Failures:
> 1. test_auth: AssertionError
> 2. test_validation: TypeError
> 3. test_integration: Connection timeout
> 4. test_api_1: 404 response
> 5. test_api_2: 500 error
> 6. test_data: Null value error
> 7. test_ui: Element not found
> 
> Root cause: Authentication service incomplete.
> Resolution: 4 hours.
> ETA: 2026-01-08 18:00 UTC"

---

### Example 2: Reporting Progress

**Incorrect**:
> "Almost done, 98% passing. Small fixes remain."

**Correct**:
> "Status: NOT READY - 12 tests failing (98% pass rate).
> 
> Remaining work:
> - Fix authentication flow (2 hours)
> - Resolve validation errors (1 hour)
> - Update API endpoints (1 hour)
> 
> ETA for 100% passing: 4 hours
> Will notify when status changes to: 100% tests passing"

---

### Example 3: Status Update

**Incorrect**:
> "Mostly complete, non-blocking issues only."

**Correct**:
> "Status: NOT READY
> 
> Completion: 85% (34/40 requirements)
> Blocking issues: 6 requirements incomplete
> 
> Blocking details:
> - REQ-01: Not started
> - REQ-05: In progress (50%)
> - REQ-12: Failed tests (3)
> - REQ-18: Failed tests (2)
> - REQ-25: Integration incomplete
> - REQ-30: Documentation missing
> 
> ETA for READY: 2 days"

---

## Appendix C: Policy Quick Reference

**Mandatory Reading**: `governance/policies/POLICY-NO-ONLY-LANGUAGE.md`

**Key Points**:
1. Minimizing language = BANNED (automatic rejection)
2. Two valid statuses: "100% tests passing" OR "NOT READY - X failing"
3. All failures MUST include: count, root cause, resolution plan, ETA
4. Exceptions: ZERO (CS2 override only)
5. Training: Mandatory before ANY PR submission

---

**Status**: ACTIVE LEARNING  
**Category**: Test Dodging Prevention  
**Authority**: CS2 + FM  
**Mandatory**: YES (all builders)

---

*Remember: Language shapes thought. Accurate language = accurate work. Minimizing language = test dodging.*

---

**END OF BOOTSTRAP LEARNING**
