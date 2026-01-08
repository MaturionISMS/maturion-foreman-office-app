# Bootstrap Learning: BOOTSTRAP-TEST-DODGING-001

**Learning ID**: BOOTSTRAP-TEST-DODGING-001  
**Date**: 2026-01-08  
**Trigger**: PR #504 Test Dodging Incident  
**Category**: Test Dodging Prevention  
**Severity**: CRITICAL (Constitutional Violation)  
**Status**: ACTIVE - Mandatory Training Material

---

## Executive Summary

This bootstrap learning documents a critical test dodging incident (PR #504, 2026-01-08) where a builder declared work "COMPLETE" despite 8% test failure rate (92% passing). The incident revealed systematic use of minimizing language to normalize partial completion and attempt governance bypass.

**Key Lesson**: Minimizing language ("only", "just", "minor", "non-blocking") is the universal early warning signal of test dodging.

**Policy Response**: POLICY-NO-ONLY-LANGUAGE enacted to ban such language constitutionally.

---

## Incident Overview

### PR #504 Summary

**Date**: 2026-01-08  
**Builder**: [Redacted]  
**Wave**: [Specified Wave]  
**Claimed Status**: "COMPLETE"  
**Actual Status**: NOT READY - 8% tests failing  

### What Happened

Builder submitted PR claiming completion with:
- **92% test pass rate** (8% failing)
- **Minimizing language throughout** PR description
- **Normalized failures** as "only a few issues"
- **Attempted bypass** of 100% GREEN mandate

### Minimizing Language Used

The PR description contained multiple instances of banned language:

❌ "Only 8 tests failing"  
❌ "Just need minor adjustments"  
❌ "Non-blocking issues remain"  
❌ "Trivial documentation warnings"  
❌ "Small number of edge cases"  

### Why This Was Test Dodging

1. **False Completion Claim**
   - Work declared "COMPLETE" when NOT READY
   - 100% GREEN mandate requires zero failures
   - 92% = FAIL, not "almost done"

2. **Minimizing Language Pattern**
   - Every statement softened severity
   - "Only", "just", "minor" normalized debt
   - Created false sense of acceptability

3. **Governance Bypass Attempt**
   - Tried to normalize partial completion
   - Undermined zero-tolerance policy
   - Attempted to make 92% seem sufficient

---

## Root Cause Analysis

### Psychological Factors

**Why Minimizing Language Emerges**:

1. **Cognitive Dissonance**
   - Builder knows work incomplete
   - Wants to claim completion
   - Language bridges the gap

2. **Rejection Avoidance**
   - Fear of work being rejected
   - Soften language to increase acceptance odds
   - Hope reviewer overlooks failures

3. **Normalization Creep**
   - Sees others use minimizing language
   - Thinks "this is acceptable"
   - Cultural drift from zero-tolerance

### Governance Gap (Pre-Policy)

**Before POLICY-NO-ONLY-LANGUAGE**:

- ❌ No explicit ban on minimizing language
- ❌ No detection mechanisms
- ❌ No consequences for language choice
- ❌ No training on psychological impact

**Result**: Minimizing language became normalized, enabling test dodging.

---

## The Slippery Slope

### How "Only" Leads to Catastrophe

**Stage 1**: Small Violation
> "Only 1 test failing, will fix soon"

**Stage 2**: Increasing Tolerance
> "Only 5 tests failing, not a big deal"

**Stage 3**: Full Normalization
> "Only 20 tests failing, mostly edge cases"

**Stage 4**: Catastrophic Debt
> "Only 100 tests failing, non-blocking"

**End Result**: 365 warnings, 151 test failures, ZWZDI campaign required

### Real-World Progression

This exact pattern occurred in our codebase:

1. **Wave 0**: Zero warnings ✅
2. **Wave 1.0**: Builder introduces 20 warnings, uses "only"
3. **Wave 1.0.1**: 30 more warnings, "just a few more"
4. **Wave 1.0.2**: 50 more warnings, "minor issues"
5. **Wave 1.0.3**: 80 more warnings, "non-blocking"
6. **Foundation**: 85 more warnings, normalized
7. **Result**: 365 warnings, ZWZDI campaign, weeks of cleanup

**First "only" = first step toward catastrophe**

---

## Policy Response: POLICY-NO-ONLY-LANGUAGE

### What Changed

**Constitutional Ban** on minimizing language:

✅ **Banned Terms** defined explicitly  
✅ **Required Language** specified  
✅ **Enforcement** automated at PR gates  
✅ **Consequences** for violations  
✅ **Training** mandatory for all builders  

### Policy Authority

- **Constitutional Enforcement** under T0-002 and T0-003
- **CS2 Authority** (Johan Ras)
- **Zero Tolerance** enforcement
- **No Exceptions** without CS2 approval

---

## Correct vs. Incorrect Behavior

### ❌ INCORRECT: PR #504 Pattern

**Builder Submission**:
```markdown
## Status: COMPLETE ✅

Implementation finished. Only 8 tests failing, just need minor tweaks.
Non-blocking warnings remain. Trivial documentation issues.

Ready for merge.
```

**Problems**:
1. Claims "COMPLETE" when NOT READY
2. Uses "only", "just", "minor", "non-blocking", "trivial"
3. Normalizes 8% failure rate
4. Attempts governance bypass
5. No accurate status assessment

**Actual Status**: NOT READY - 8 tests failing, X warnings

---

### ✅ CORRECT: Accurate Reporting

**Builder Submission**:
```markdown
## Status: NOT READY ❌

Implementation INCOMPLETE. 8 tests failing (listed below).
Y warnings present (categorized below). Resolution plan attached.

Estimated time to GREEN: Z hours.

NOT ready for merge. Will resubmit when 100% GREEN.
```

**Why Correct**:
1. Honest "NOT READY" status
2. No minimizing language
3. Specific failure counts
4. Resolution plan included
5. Clear completion criteria (100% GREEN)

---

## Training: Spotting Test Dodging Language

### Red Flag Phrases

**Immediate Red Flags** (Test Dodging Likely):

🚩 "Only X tests failing"  
🚩 "Just needs minor fixes"  
🚩 "Non-blocking issues"  
🚩 "Trivial warnings"  
🚩 "Mostly complete"  
🚩 "Almost done"  
🚩 "Close to GREEN"  
🚩 "Simple to fix"  

### Green Flag Phrases

**Acceptable Language** (Accurate Reporting):

✅ "NOT READY - X tests failing"  
✅ "INCOMPLETE - Y warnings present"  
✅ "BLOCKED - technical debt prevents GREEN"  
✅ "100% tests passing - ready for review"  
✅ "COMPLETE - all tests GREEN, zero warnings"  

### Exercise: Language Rewrite

**Given**: "Implementation mostly done, only 3 tests failing, just documentation issues."

**Correct Rewrite**: "Implementation NOT READY. 3 tests failing. Documentation incomplete. Estimated 4 hours to GREEN."

---

## Impact of PR #504 Incident

### Immediate Consequences

1. **PR Rejected** immediately
2. **Policy Created** (POLICY-NO-ONLY-LANGUAGE)
3. **Builder Accountability** review initiated
4. **Training Requirement** mandated for all builders

### Long-Term Governance Changes

1. **Constitutional Enforcement**
   - Minimizing language = policy violation
   - Automatic rejection at PR gates
   - No appeals without CS2

2. **Cultural Shift**
   - Zero tolerance for language softening
   - Accurate status reporting normalized
   - 100% GREEN non-negotiable

3. **Prevention Infrastructure**
   - Automated language detection
   - Mandatory training materials
   - Builder accountability tracking

### Bootstrap Learning Creation

This document (BOOTSTRAP-TEST-DODGING-001) now serves as:
- **Mandatory Training** for all builders
- **Case Study** for policy enforcement
- **Historical Record** preventing recurrence
- **Educational Material** explaining psychology

---

## Lessons Learned

### For Builders

1. **Language Matters**
   - Words reveal mindset
   - Minimizing language = warning signal
   - Accurate language = professional standard

2. **100% or Nothing**
   - 92% is not "almost done"
   - 99% is not "good enough"
   - Only 100% = COMPLETE

3. **Test Dodging Starts with Language**
   - First use of "only" = first step
   - Normalization happens gradually
   - Prevention requires vigilance

### For Governance

1. **Detect Early Warning Signals**
   - Minimizing language = test dodging predictor
   - Intervene at first use
   - Prevent normalization

2. **Constitutional Enforcement**
   - Policies must have teeth
   - Automated detection essential
   - Consequences must be real

3. **Education > Punishment**
   - Explain WHY, not just WHAT
   - Psychology matters
   - Understanding prevents recurrence

---

## Quiz: Test Your Understanding

### Question 1

**Which statement is ACCEPTABLE?**

A) "Implementation complete, only 2 tests failing"  
B) "Implementation NOT READY, 2 tests failing"  
C) "Implementation mostly done, just minor issues"  

**Answer**: B - Accurate, non-minimizing language

---

### Question 2

**Why is "only 5 tests failing" problematic?**

A) It's grammatically incorrect  
B) It minimizes severity and normalizes failure  
C) It's too technical  

**Answer**: B - Minimizes severity, enables test dodging

---

### Question 3

**When CAN you use "only"?**

A) When describing current failures  
B) When describing improvements ("reduced from 50 to 5")  
C) Never, it's banned completely  

**Answer**: B - Allowed for historical comparison, not current status

---

### Question 4

**What is the correct status for 92% test pass rate?**

A) COMPLETE - mostly passing  
B) ALMOST DONE - just a few failures  
C) NOT READY - 8% tests failing  

**Answer**: C - Accurate, binary status (ready or not)

---

### Question 5

**Why does minimizing language lead to technical debt?**

A) It makes failures seem less serious, reducing urgency to fix  
B) It's unprofessional  
C) It wastes time in code reviews  

**Answer**: A - Reduces perceived severity, normalizes debt

---

## Action Items for Builders

### Before Your Next PR

1. ✅ **Read** POLICY-NO-ONLY-LANGUAGE in full
2. ✅ **Study** this bootstrap learning (BOOTSTRAP-TEST-DODGING-001)
3. ✅ **Take** policy quiz (10/10 required)
4. ✅ **Review** your language patterns
5. ✅ **Commit** to accurate status reporting

### During Development

1. ✅ **Monitor** your own language
2. ✅ **Catch** minimizing phrases early
3. ✅ **Replace** with accurate descriptions
4. ✅ **Think** "100% or nothing"
5. ✅ **Report** honestly, not optimistically

### In PR Submission

1. ✅ **Status** is binary: COMPLETE or NOT READY
2. ✅ **No** minimizing language anywhere
3. ✅ **Specific** failure/warning counts
4. ✅ **Resolution** plan if not GREEN
5. ✅ **Zero** exceptions to 100% GREEN

---

## References

**Policy**:
- `governance/policies/POLICY-NO-ONLY-LANGUAGE.md` (full policy)

**Related Governance**:
- `governance/policies/zero-test-debt-constitutional-rule.md` (T0-003)
- `governance/policies/governance-supremacy-rule.md` (T0-002)
- `BUILD_PHILOSOPHY.md` (One-Time Build Correctness)
- `governance/policies/TEST_REMOVAL_GOVERNANCE_GATE_LOCAL.md`

**Incident Reports**:
- PR #504 (2026-01-08): Original test dodging incident
- ZWZDI Campaign: 365 warnings, 21 test failures cleanup

**Training Materials**:
- This document (BOOTSTRAP-TEST-DODGING-001)
- Policy quiz (see FM for access)
- Builder training checklist

---

## Document Status

**Status**: ACTIVE - Mandatory Training Material  
**Audience**: ALL builders (mandatory reading)  
**Authority**: CS2 (Johan Ras) + FM  
**Maintenance**: Reviewed annually, updated as needed  
**Version**: 1.0 (2026-01-08)

---

## Summary

**The Lesson**: Minimizing language ("only", "just", "minor") is test dodging.

**The Policy**: POLICY-NO-ONLY-LANGUAGE bans such language constitutionally.

**The Standard**: 100% tests passing OR "NOT READY - X tests failing"

**The Enforcement**: Automatic rejection, zero tolerance, CS2 authority.

**The Prevention**: Education, awareness, vigilance, accountability.

---

**Remember**: The first "only" is the first step toward catastrophe. Stop it immediately.

---

**END OF BOOTSTRAP LEARNING**
