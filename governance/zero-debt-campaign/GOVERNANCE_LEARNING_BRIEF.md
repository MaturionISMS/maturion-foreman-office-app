# ZWZDI Campaign - Governance Learning Brief

**Campaign ID**: ZWZDI-2026-001  
**Document**: Governance Learning Brief for Builders  
**Version**: 1.0  
**Last Updated**: 2026-01-08  
**Mandatory Reading**: ALL builders MUST read before cleanup execution

---

## Purpose

This document educates all builders on:
1. Why warnings are technical debt
2. Why test debt is unacceptable
3. The zero-tolerance policy
4. Common test dodging patterns
5. Correct behavior going forward

**READ THIS CAREFULLY**: This is not optional. Understanding these principles is essential for maintaining governance integrity.

---

## Core Principle: Warnings Are Debt

### What Are Warnings?

Warnings are messages from:
- Test frameworks (pytest)
- Linters (pylint, flake8, mypy)
- Build tools (TypeScript compiler, webpack)
- Runtime systems (Python interpreter, Node.js)

### Why Warnings Are Debt

**Warnings are NOT informational**. They are **deferred errors**.

#### Analogy: The Leaking Roof

Imagine your house has a small roof leak:
- "It's just a little water" ← Ignoring the warning
- "I'll fix it later" ← Deferring the debt
- **Result**: Structural damage, mold, expensive repair

**Warnings work the same way**:
- One warning → easy to fix now
- 10 warnings → harder to fix
- 365 warnings → **massive technical debt**

#### The Compound Effect

Warnings accumulate like financial debt:
1. **Warning introduced** (principal)
2. **More code built on top** (interest)
3. **Warning becomes harder to fix** (compound interest)
4. **Eventually: critical failure** (bankruptcy)

### Real-World Consequences

**Scenario 1: Ignored Deprecation Warning**
```python
# Warning: 'old_function' is deprecated, use 'new_function'
result = old_function(data)
```
**What happens**:
1. Next library version: `old_function` removed
2. Code breaks in production
3. Emergency fix required
4. Downtime, lost trust, financial impact

**Scenario 2: Suppressed Type Warning**
```python
# type: ignore
value = some_function()  # Returns int, but we treat as str
```
**What happens**:
1. Runtime type error in production
2. Data corruption possible
3. Hard to debug (warning was silenced)
4. Hours wasted finding root cause

---

## Core Principle: Test Debt Is Unacceptable

### What Is Test Debt?

Test debt occurs when:
1. **Tests remain RED** (failing) without resolution
2. **Tests are skipped** (`@pytest.mark.skip`) without proper authorization
3. **Tests are commented out** instead of fixed or removed
4. **Tests have incomplete implementations** (placeholder logic)
5. **Tests use `pass` or `NotImplementedError`** without proper QA-to-Red status

### Why Test Debt Is Catastrophic

**Tests are your safety net**. Test debt is like cutting holes in your safety net.

#### The Safety Net Analogy

Circus performers work with safety nets:
- **Every hole** = potential death
- **"We'll fix the net later"** = unacceptable
- **Net inspection before every show** = mandatory

**Your test suite is your safety net**:
- Every RED test = hole in the net
- "We'll implement it later" = unacceptable
- **100% GREEN before shipping** = mandatory

### Red vs. Debt

**Important distinction**:

| State | Status | Acceptable? |
|-------|--------|-------------|
| **QA-to-Red** | Tests RED, awaiting implementation, documented in QA_CATALOG.md | ✅ YES - This is the plan |
| **Build-to-Green** | Tests GREEN after implementation | ✅ YES - This is success |
| **Test Debt** | Tests RED without plan, or skipped/commented | ❌ NO - This is failure |

**QA-to-Red is intentional RED** (planned work)  
**Test Debt is unintentional RED** (unplanned debt)

### Real-World Consequences

**Scenario 1: Skipped Authentication Test**
```python
@pytest.mark.skip(reason="TODO: fix later")
def test_authentication():
    # Test critical security logic
    pass
```
**What happens**:
1. Authentication bug ships to production
2. Security vulnerability exposed
3. Data breach occurs
4. Legal/financial/reputational damage

**Scenario 2: Commented Out Test**
```python
# def test_data_validation():
#     # This test was failing, commenting out for now
#     assert validate_input(malicious_data) == False
```
**What happens**:
1. Data validation bypassed
2. Malicious input accepted
3. System compromise
4. Critical incident

---

## The Zero-Tolerance Policy

### What Zero-Tolerance Means

**Zero warnings = PASS**  
**One warning = FAIL**  
**365 warnings = CATASTROPHIC FAIL**

**Zero RED tests = PASS** (excluding documented QA-to-Red)  
**One debt test = FAIL**  
**151 debt tests = CATASTROPHIC FAIL**

### The 99% Is 0% Rule (Governance Supremacy Rule)

From `governance/policies/governance-supremacy-rule.md`:

> "99% is 0%. There is no partial credit. A system that passes 99% of tests but fails 1% is a FAILED system."

**Examples**:
- 99% of tests passing = FAIL
- 99% of code covered = FAIL  
- 99% of requirements met = FAIL
- 1 warning remaining = FAIL

### Why Zero Tolerance?

**Quality is binary**:
- Airplane either flies safely or it doesn't
- Bridge either holds weight or it doesn't
- Code either works correctly or it doesn't

**There is no "mostly safe airplane"**

### Enforcement

Zero-tolerance is enforced through:
1. **PR Gates**: PRs with warnings BLOCKED
2. **FM Verification**: Work with warnings REJECTED
3. **Builder Accountability**: Builders who introduce warnings IMMEDIATELY remediate
4. **Campaign like ZWZDI**: Accumulated debt ELIMINATED before new work

---

## Common Test Dodging Patterns (PROHIBITED)

### Pattern 1: "Skip for Now"

**Example**:
```python
@pytest.mark.skip(reason="Will fix later")
def test_critical_feature():
    pass
```

**Why it's wrong**:
- "Later" never comes
- Test debt accumulates
- Feature ships untested

**Correct approach**:
- If test is QA-to-Red: Document in QA_CATALOG.md, mark with proper QA ID
- If test is broken: FIX IT NOW
- If test is obsolete: REMOVE IT with traceability

---

### Pattern 2: "Comment Out to Make CI Pass"

**Example**:
```python
# def test_that_was_failing():
#     assert something_important()
```

**Why it's wrong**:
- Hidden debt
- No traceability
- Functionality untested

**Correct approach**:
- If test fails: INVESTIGATE and FIX
- If feature changed: UPDATE TEST
- If test obsolete: REMOVE with traceability document

---

### Pattern 3: "Use `pass` as Implementation"

**Example**:
```python
def test_data_integrity():
    pass  # TODO: implement this
```

**Why it's wrong**:
- Test appears to pass (GREEN) but tests nothing
- False confidence
- Bugs slip through

**Correct approach**:
- If awaiting implementation: Use `pytest.raises(NotImplementedError)` with QA ID
- If implemented: WRITE THE TEST
- If not needed: REMOVE

---

### Pattern 4: "Suppress the Warning"

**Example**:
```python
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
```

**Why it's wrong**:
- Hides the problem
- Problem gets worse over time
- Future developers don't see the issue

**Correct approach**:
- FIX the root cause of the warning
- If library-generated and unfixable: Document explicitly why suppression is necessary
- Seek approval for suppression from FM

---

### Pattern 5: "It's Just a Warning"

**Mindset**:
> "The tests pass, so the warnings don't matter."

**Why it's wrong**:
- Warnings indicate problems
- Problems become errors
- Errors cause failures

**Correct approach**:
- Treat warnings as errors
- Fix immediately upon introduction
- Never merge code with warnings

---

## Correct Behavior Going Forward

### Builder Responsibilities

As a builder, you MUST:

1. **Write Warning-Free Code**
   - Run tests locally before submitting
   - Fix warnings immediately
   - Never suppress warnings without FM approval

2. **Write Complete Tests**
   - All tests either GREEN or documented QA-to-Red
   - No skipped tests without authorization
   - No commented tests
   - No placeholder implementations

3. **Perform Code Checking**
   - Review all generated code
   - Verify logical correctness
   - Check for obvious defects
   - Include checking evidence in Builder QA Report

4. **Immediate Remedy**
   - If you discover your own warning: FIX IT IMMEDIATELY
   - If you discover your own test debt: FIX IT IMMEDIATELY
   - If you discover someone else's debt: ESCALATE TO FM

### Verification Checklist (Before Submitting Work)

Before marking your work complete, verify:

- [ ] All tests run: `pytest tests/` (or relevant subset)
- [ ] Zero warnings in output
- [ ] Zero RED tests (excluding documented QA-to-Red)
- [ ] All code reviewed for correctness
- [ ] Builder QA Report includes code checking evidence
- [ ] No skipped or commented tests
- [ ] No warning suppressions without justification

### When You Encounter Warnings

**During development**, if a warning appears:

1. **STOP immediately**
2. **READ the warning** carefully
3. **FIX the root cause** (don't suppress)
4. **VERIFY warning gone**
5. **CONTINUE work**

**Do NOT**:
- Ignore it
- Suppress it
- Defer it
- Assume "someone else will fix it"

---

## Case Study: How We Got to 365 Warnings

### Timeline

1. **Wave 0**: Clean state, zero warnings
2. **Wave 1.0**: Builder introduces 20 warnings, defers fixing
3. **Wave 1.0.1**: Builder introduces 30 more warnings, sees existing warnings and thinks "a few more won't matter"
4. **Wave 1.0.2**: 50 more warnings, now harder to find which are new
5. **Wave 1.0.3**: 80 more warnings, overwhelming, builder gives up
6. **Wave 1.0.4**: 100 more warnings, completely normalized
7. **Foundation**: 85 more warnings, "this is just how it is"
8. **Result**: 365 warnings, massive technical debt

### What Went Wrong

1. **First warning not fixed immediately** (broken window)
2. **Accumulation normalized** (boiling frog)
3. **No enforcement at PR gates** (no prevention)
4. **No builder accountability** (no consequences)
5. **No governance education** (lack of understanding)

### Lesson Learned

**Zero-tolerance from the start** prevents accumulation.

**Fix first warning immediately** prevents all subsequent warnings.

---

## Your Role in ZWZDI

### During This Campaign

You will be assigned cleanup for a specific wave. You MUST:

1. **Read this document** (you're doing it now ✓)
2. **Review your wave cleanup plan**
3. **Eliminate ALL warnings** in your wave scope
4. **Resolve ALL test debt** in your wave scope
5. **Provide completion evidence**
6. **Submit for FM verification**

### After This Campaign

You MUST:

1. **Never introduce warnings** going forward
2. **Fix warnings immediately** if they appear
3. **Write complete tests** (GREEN or documented RED)
4. **Perform code checking** before submitting
5. **Maintain zero-tolerance mindset**

---

## Summary: The Three Laws

### Law 1: Warnings Are Debt
Treat every warning as a deferred error. Fix immediately.

### Law 2: Test Debt Is Catastrophic
100% or 0%. There is no in-between. Complete or fail.

### Law 3: Zero Tolerance Is Non-Negotiable
One warning = failure. One debt test = failure. No exceptions.

---

## Acknowledgment

By proceeding with your wave cleanup, you acknowledge that you have:

✅ Read and understood this Governance Learning Brief  
✅ Understand why warnings are debt  
✅ Understand why test debt is unacceptable  
✅ Understand the zero-tolerance policy  
✅ Commit to maintaining zero warnings and zero debt going forward  

---

## Questions or Clarifications

If anything in this document is unclear:
1. **STOP** your cleanup work
2. **ESCALATE** to Foreman (FM)
3. **WAIT** for clarification
4. **THEN** proceed with full understanding

**Do NOT proceed with incomplete understanding.**

---

## NEW: The "Only" Language Ban

**Policy**: POLICY-NO-ONLY-LANGUAGE (2026-01-08)

Minimizing language is now banned when describing test failures or technical debt.

### Banned Language

❌ "Only 5 tests failing"  
❌ "Just documentation nits"  
❌ "Non-blocking failures"  
❌ "Minor issues remaining"  
❌ "Almost complete"

### Required Language

✅ Required: "100% tests passing" or "NOT READY - X tests failing"

### Why This Matters

**"Only" is the universal language of test dodging.**

When someone says "only 5 tests failing", they are:
1. Minimizing the severity of 5 complete failures
2. Normalizing the existence of test debt
3. Implying that 5 failures are acceptable
4. Preparing to skip fixing them

**Zero-tolerance means zero-tolerance language.**

If we permit "only X failing", we implicitly accept that X failures are tolerable. But zero-tolerance says X > 0 = FAIL.

### Enforcement

- **Automatic rejection**: Any PR or completion claim containing banned minimizing language
- **No exceptions**: Without explicit CS2 approval
- **Builder training**: All builders must read POLICY-NO-ONLY-LANGUAGE before assignment

### See Bootstrap Learning

**BOOTSTRAP-TEST-DODGING-001** documents the PR #504 incident that led to this policy:
- 92% pass rate was presented as "COMPLETE"
- Minimizing language hid 8% failure rate
- CS2 rejection triggered governance update

**Location**: `bootstrap/learnings/BOOTSTRAP-TEST-DODGING-001.md`

**Authority**: `governance/policies/POLICY-NO-ONLY-LANGUAGE.md`

---

**Document Status**: MANDATORY READING  
**Enforcement**: Builder must acknowledge reading before wave assignment  
**Authority**: CS2 (Johan Ras) + FM

---

*Remember: Quality is not an option. It is the foundation of everything we build.*
