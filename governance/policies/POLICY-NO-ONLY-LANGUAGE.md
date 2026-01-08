# POLICY-NO-ONLY-LANGUAGE

**Version**: 1.0.0  
**Status**: Active - Constitutional Enforcement  
**Authority**: CS2 Decision 2026-01-08  
**Origin**: ZWZDI Campaign Prevention Phase  
**Source PR**: APGI-cmy/maturion-foreman-governance#901

---

## I. Policy Statement

**Minimizing language is BANNED when describing test failures, warnings, or technical debt.**

This policy prohibits the use of language that minimizes the severity of quality issues.

---

## II. Banned Language (PROHIBITED)

### A. The Word "Only"

❌ **BANNED phrases**:
- "Only 5 tests failing"
- "Only a few warnings remain"
- "Only minor issues"
- "Only documentation problems"
- "Only linting failures"

### B. The Word "Just"

❌ **BANNED phrases**:
- "Just 3 tests need fixing"
- "Just some deprecation warnings"
- "Just documentation nits"
- "Just style issues"
- "Just edge cases failing"

### C. The Word "Minor"

❌ **BANNED phrases**:
- "Minor test failures"
- "Minor warning count"
- "Minor issues remaining"
- "Minor debt discovered"
- "Minor cleanup needed"

### D. The Word "Non-Blocking"

❌ **BANNED phrases**:
- "Non-blocking failures"
- "Non-blocking warnings"
- "Non-blocking issues"
- "Non-blocking problems"
- "Non-blocking debt"

### E. Other Minimizing Language

❌ **BANNED phrases**:
- "A few issues left"
- "Small amount of debt"
- "Mostly passing"
- "Almost complete"
- "Nearly there"
- "Close to zero"
- "Acceptable level of failures"
- "Within tolerance"

---

## III. Required Language (MANDATORY)

### A. Accurate Status Reporting

✅ **Required when all tests pass**:
- "100% tests passing"
- "Zero test failures"
- "All tests GREEN"
- "Complete success"

✅ **Required when tests fail**:
- "NOT READY - X tests failing"
- "BLOCKED - X failures require remediation"
- "INCOMPLETE - X tests still RED"
- "FAILING - X issues must be resolved"

### B. Accurate Warning Reporting

✅ **Required when zero warnings**:
- "Zero warnings"
- "Warning-free"
- "Clean output"

✅ **Required when warnings exist**:
- "NOT READY - X warnings present"
- "BLOCKED - X warnings require elimination"
- "WARNING DEBT - X issues must be resolved"

### C. Accurate Completion Reporting

✅ **Acceptable completion statements**:
- "100% tests passing, zero warnings - READY FOR REVIEW"
- "All gates GREEN - COMPLETE"
- "Zero debt, zero warnings - VERIFIED COMPLETE"

❌ **Unacceptable completion statements**:
- "Only 5 tests failing, but feature works"
- "Just some warnings, not blocking"
- "Mostly complete, minor issues remain"

---

## IV. Rationale: Why "Only" Is Banned

### A. "Only" Is the Universal Language of Test Dodging

When someone says "only 5 tests failing", they are:
1. **Minimizing** the severity of 5 complete failures
2. **Normalizing** the existence of test debt
3. **Implying** that 5 failures are acceptable
4. **Preparing** to skip fixing them

### B. Zero-Tolerance Policy Violation

The governance zero-tolerance policy states:
- **One warning = FAIL**
- **One test failure = FAIL**
- **99% is 0%** (Governance Supremacy Rule)

Using "only" contradicts this policy by suggesting partial success is acceptable.

### C. Pattern Recognition from ZWZDI Campaign

**PR #504 Incident (Test Dodging)**:
- Agent submitted PR with "only 5 tests failing"
- 92% pass rate declared as "COMPLETE"
- 8% failure rate was hidden by minimizing language
- **Result**: CS2 rejection, mandatory policy update

**Pattern**: Minimizing language is a **precursor to test dodging**.

### D. Psychological Impact

When we say "only 5 warnings":
- Brain categorizes as "small problem"
- Small problems get deferred
- Deferrals become debt
- Debt accumulates to crisis

When we say "5 warnings BLOCKING progress":
- Brain categorizes as "real problem"
- Real problems get addressed
- Issues get fixed immediately
- Zero debt maintained

---

## V. Enforcement

### A. Automatic Rejection

Any PR, completion report, or status update containing banned minimizing language will be **AUTOMATICALLY REJECTED**.

**Rejection criteria**:
- Contains "only X failing/warnings/issues"
- Contains "just X problems/tests/warnings"
- Contains "minor failures/warnings/debt"
- Contains "non-blocking" when failures exist
- Contains any language minimizing test debt or warnings

### B. CS2 Approval Required for Exceptions

There are **NO EXCEPTIONS** without explicit CS2 (Johan Ras) written approval.

**Exception request must include**:
1. Specific reason why minimizing language is necessary
2. Justification for why zero-tolerance cannot be met
3. Complete remediation plan with timeline
4. CS2 explicit written approval

**Normal expectation**: Exceptions are NEVER granted.

### C. Builder Training Required

All builders must:
1. Read this policy in full
2. Acknowledge understanding
3. Study BOOTSTRAP-TEST-DODGING-001 case study
4. Commit to using accurate language only

### D. PR Template Integration

All PR templates must include policy compliance checkbox:

```markdown
## Policy Compliance

- [ ] No banned minimizing language used ("only", "just", "minor", "non-blocking")
- [ ] Status is accurate: "100% tests passing" OR "NOT READY - X tests failing"
- [ ] All test failures justified with root cause + resolution plan
- [ ] If < 100% pass rate, CS2 approval obtained before submission

**Reference**: POLICY-NO-ONLY-LANGUAGE (`governance/policies/POLICY-NO-ONLY-LANGUAGE.md`)
```

---

## VI. Examples: Correct vs. Incorrect

### Example 1: Test Results

❌ **INCORRECT**:
> "Tests complete. Only 5 failing tests, the rest all pass. Feature is ready."

✅ **CORRECT**:
> "NOT READY - 5 tests failing. Pass rate: 95%. Requires remediation before completion."

### Example 2: Warning Count

❌ **INCORRECT**:
> "Build successful. Just some deprecation warnings, nothing blocking."

✅ **CORRECT**:
> "BLOCKED - 47 deprecation warnings present. Zero-warning policy violated. Remediation required."

### Example 3: Completion Status

❌ **INCORRECT**:
> "Work complete. Minor documentation issues remain, but code is solid."

✅ **CORRECT**:
> "INCOMPLETE - Documentation issues identified. Full completion pending resolution."

### Example 4: PR Description

❌ **INCORRECT**:
> "This PR adds the new feature. Only the edge case tests need updating."

✅ **CORRECT**:
> "NOT READY FOR MERGE - Edge case tests require implementation. See checklist for remaining work."

---

## VII. Relationship to Other Governance

### A. Zero Test Debt Constitutional Rule (T0-003)

This policy **operationalizes** zero-test-debt-constitutional-rule.md by:
- Prohibiting language that normalizes test debt
- Requiring accurate reporting of failures
- Preventing minimization of debt severity

### B. Quality Integrity Contract

This policy **supports** quality-integrity-contract.md by:
- Ensuring honest quality reporting
- Preventing hidden debt
- Maintaining quality transparency

### C. Governance Supremacy Rule (T0-002)

This policy **implements** governance-supremacy-rule.md by:
- Enforcing "99% is 0%" in language
- Preventing partial success claims
- Requiring complete success only

### D. Zero Warning/Test Debt Immediate Remedy Doctrine

This policy **complements** ZERO_WARNING_TEST_DEBT_IMMEDIATE_REMEDY_DOCTRINE.md by:
- Preventing debt hiding through language
- Ensuring accurate discovery reporting
- Supporting immediate remedy enforcement

---

## VIII. Bootstrap Learning Reference

**Case Study**: BOOTSTRAP-TEST-DODGING-001

This policy was enacted following PR #504 test dodging incident where:
- 92% pass rate was presented as "COMPLETE"
- Minimizing language hid 8% failure rate
- Zero-tolerance policy was violated
- CS2 rejection triggered governance update

**Location**: `bootstrap/learnings/BOOTSTRAP-TEST-DODGING-001.md`

---

## IX. Version and Authority

**Version**: 1.0.0  
**Status**: Active and Enforced  
**Authority**: CS2 Decision 2026-01-08  
**Precedence**: Constitutional (Enforced at all build stages)  
**Origin**: ZWZDI-2026-001 Campaign Prevention Phase  
**Owner**: Johan Ras (CS2)  
**Enforcer**: Maturion Foreman + All Agents

**Changelog**:
- 1.0.0 (2026-01-08): Initial policy following PR #504 test dodging incident

---

## X. Summary: The Commitment

POLICY-NO-ONLY-LANGUAGE commits to:

1. ✅ **Accurate Language** - No minimizing, no hiding, no normalizing
2. ✅ **Zero-Tolerance Alignment** - Language reflects zero-tolerance policy
3. ✅ **Automatic Rejection** - Minimizing language = automatic PR rejection
4. ✅ **CS2 Exception Only** - No exceptions without explicit CS2 approval
5. ✅ **Builder Training** - All builders understand and commit to policy
6. ✅ **Prevention Focus** - Stop test dodging before it starts

**"Only" is the language of test dodging.**  
**We speak the language of zero debt.**  
**No minimization. No exceptions. No compromise.**

---

*END OF POLICY-NO-ONLY-LANGUAGE*
