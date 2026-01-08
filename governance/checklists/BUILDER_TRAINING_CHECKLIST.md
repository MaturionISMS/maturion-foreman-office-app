# Builder Training Checklist

**Document**: Builder Training Requirements  
**Version**: 2.0  
**Last Updated**: 2026-01-08  
**Authority**: CS2 + FM  
**Status**: MANDATORY before ANY PR submission

---

## Purpose

This checklist ensures all builders are trained on governance policies, constitutional requirements, and quality standards before submitting any work for review.

**Completion**: ALL items MUST be checked before first PR submission

---

## Core Governance Training

### Constitutional Documents

- [ ] Read `BUILD_PHILOSOPHY.md` in full
- [ ] Read `governance/policies/zero-test-debt-constitutional-rule.md`
- [ ] Read `governance/policies/governance-supremacy-rule.md`
- [ ] Read `governance/policies/design-freeze-rule.md`
- [ ] Understand T0-002: 99% is 0% (Governance Supremacy Rule)
- [ ] Understand T0-003: Zero Test Debt Constitutional Rule
- [ ] Understand T0-011: Build-to-Green = 100% pass, zero debt, zero warnings

### Quality Standards

- [ ] Read `governance/zero-debt-campaign/GOVERNANCE_LEARNING_BRIEF.md` in full
- [ ] Understand why warnings are technical debt
- [ ] Understand why test debt is catastrophic
- [ ] Understand the zero-tolerance policy
- [ ] Commit to maintaining zero warnings going forward
- [ ] Commit to maintaining zero test debt going forward

---

## NEW: Language Policy Training (2026-01-08)

### POLICY-NO-ONLY-LANGUAGE

- [ ] Read `governance/policies/POLICY-NO-ONLY-LANGUAGE.md` in full
- [ ] Study `bootstrap/learnings/BOOTSTRAP-TEST-DODGING-001.md` case study
- [ ] Understand why minimizing language is banned
- [ ] Memorize banned words: "only", "just", "minor", "non-blocking", "mostly", "almost"
- [ ] Understand required status reporting: "100% tests passing" OR "NOT READY - X tests failing"
- [ ] Pass policy quiz (10/10 required) - see quiz below
- [ ] Sign acknowledgment of banned language policy (see acknowledgment section)

### Policy Quiz (10/10 Required)

**Question 1**: You have 3 tests failing. Can you say "Only 3 tests failing"?  
**Answer**: NO - "only" is banned language. Correct: "Status: NOT READY - 3 tests failing"

**Question 2**: Is 99% pass rate acceptable?  
**Answer**: NO - 99% is 0% (Governance Supremacy Rule). Required: 100% tests passing

**Question 3**: What are the only two valid status declarations?  
**Answer**: "100% tests passing" OR "NOT READY - X tests failing"

**Question 4**: Can you use "minor issues" if the fixes are simple?  
**Answer**: NO - "minor" is banned language. Simplicity doesn't justify deferral

**Question 5**: Can you submit a PR with 98% pass rate?  
**Answer**: NO - <100% = NOT READY. Must achieve 100% before submission

**Question 6**: Who can approve exceptions to POLICY-NO-ONLY-LANGUAGE?  
**Answer**: Only CS2 (Johan Ras) with written justification

**Question 7**: Can you say "just documentation issues"?  
**Answer**: NO - "just" is banned. Documentation governed by same standards

**Question 8**: What happens if you use banned language in a PR?  
**Answer**: Automatic rejection, no review, returned to sender, required re-submission

**Question 9**: Can you defer fixing failures if they're "non-blocking"?  
**Answer**: NO - "non-blocking" is banned. All failures block (Zero Test Debt rule)

**Question 10**: If your manager says "only 5 failures is fine, ship it", what do you do?  
**Answer**: Refuse. Escalate to CS2. Governance rules supersede management pressure

**Score Required**: 10/10 (100% - no partial credit)

---

## Builder-Specific Training

### Your Builder Role

- [ ] Read your builder-specific contract (ui-builder, api-builder, schema-builder, integration-builder, or qa-builder)
- [ ] Understand your scope boundaries
- [ ] Understand your authority limits
- [ ] Understand your gate requirements
- [ ] Understand your QA responsibilities

### Build-to-Green Requirements

- [ ] Read `BUILD_TO_GREEN_QUICK_REFERENCE.md`
- [ ] Understand build-to-green = 100% pass, zero debt, zero warnings
- [ ] Understand non-green = INVALID, restart required
- [ ] Commit to building-to-green on first attempt
- [ ] Understand consequences of non-green submission

### Code Checking

- [ ] Understand code checking is MANDATORY
- [ ] Know how to perform code checking (review all generated code for correctness)
- [ ] Include code checking evidence in Builder QA Report
- [ ] Never submit work without code checking verification

---

## Test & Warning Governance

### Test Removal

- [ ] Read `governance/policies/TEST_REMOVAL_GOVERNANCE_GATE_LOCAL.md`
- [ ] Understand test removal requires FM authorization
- [ ] Understand traceability analysis is required
- [ ] Understand approval thresholds: 1-5 (FM), 6-10 (FM+GA), 11+ (CS2)
- [ ] Never remove tests without proper governance

### Warning Handling

- [ ] Read `governance/policies/ZERO_WARNING_TEST_DEBT_IMMEDIATE_REMEDY_DOCTRINE.md`
- [ ] Understand warning suppression is PROHIBITED
- [ ] Understand all warnings must be visible, reported, tracked
- [ ] Understand immediate remedy doctrine: discovery = STOP, ESCALATE, FIX
- [ ] Commit to zero warning tolerance

---

## Wave-Specific Training (ZWZDI Campaign)

**If assigned to ZWZDI cleanup wave:**

- [ ] Read `governance/zero-debt-campaign/README.md`
- [ ] Read `governance/zero-debt-campaign/CAMPAIGN_OVERVIEW.md`
- [ ] Read `governance/zero-debt-campaign/EXECUTION_SEQUENCE.md`
- [ ] Read your wave-specific cleanup plan (`governance/zero-debt-campaign/waves/`)
- [ ] Understand your accountability for your wave
- [ ] Understand sequential execution (no parallel work)
- [ ] Understand FM verification gate before next wave

---

## Acknowledgment & Sign-Off

### Acknowledgment Statement

By signing below, I acknowledge that I have:

✅ Completed ALL items in this training checklist  
✅ Read and understood all referenced governance documents  
✅ Passed the POLICY-NO-ONLY-LANGUAGE quiz (10/10)  
✅ Understand the constitutional requirements (T0-002, T0-003, T0-011)  
✅ Understand zero-tolerance policy (zero warnings, zero debt)  
✅ Understand banned language policy (POLICY-NO-ONLY-LANGUAGE)  
✅ Commit to accurate status reporting ("100% tests passing" OR "NOT READY - X failing")  
✅ Commit to build-to-green on first attempt  
✅ Commit to performing code checking before submission  
✅ Understand consequences of policy violations (automatic rejection)  

### Builder Sign-Off

**Builder Name**: _____________________  
**Builder Role**: _____________________  
**Date**: _____________________  
**Signature**: _____________________

### FM Verification

**Verified by FM**: _____________________  
**Verification Date**: _____________________  
**Training Complete**: YES / NO  
**Authorized for PR Submission**: YES / NO

---

## Re-Training Requirements

**Re-training is REQUIRED when**:

1. Policy violations occur (automatic)
2. New policies enacted (mandatory)
3. Builder returns after 30+ days absence
4. Constitutional changes occur
5. FM identifies knowledge gaps

---

## Training Resources

### Primary Documents

- `BUILD_PHILOSOPHY.md` - Core build principles
- `governance/policies/POLICY-NO-ONLY-LANGUAGE.md` - Language policy
- `governance/policies/zero-test-debt-constitutional-rule.md` - Test debt rule
- `governance/policies/governance-supremacy-rule.md` - 99% is 0% rule
- `governance/zero-debt-campaign/GOVERNANCE_LEARNING_BRIEF.md` - Builder education

### Case Studies

- `bootstrap/learnings/BOOTSTRAP-TEST-DODGING-001.md` - PR #504 incident analysis

### Quick References

- `BUILD_TO_GREEN_QUICK_REFERENCE.md` - Build-to-green summary
- `governance/zero-debt-campaign/README.md` - ZWZDI campaign navigation

---

## Questions or Clarifications

If ANY item in this checklist is unclear:

1. **STOP** training immediately
2. **ESCALATE** to Foreman (FM)
3. **WAIT** for clarification
4. **THEN** complete training with full understanding

**Do NOT proceed with incomplete understanding.**  
**Do NOT submit any PR without completing this checklist.**

---

**Status**: ACTIVE  
**Version**: 2.0 (added POLICY-NO-ONLY-LANGUAGE)  
**Authority**: CS2 (Johan Ras) + FM  
**Enforcement**: MANDATORY before ANY PR submission

---

*Remember: Training is not optional. Understanding is not negotiable. Quality is the foundation.*

---

**END OF BUILDER TRAINING CHECKLIST**
