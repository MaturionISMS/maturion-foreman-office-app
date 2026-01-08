# POLICY-NO-ONLY-LANGUAGE

**Policy ID**: POLICY-NO-ONLY-LANGUAGE  
**Version**: 1.0  
**Date**: 2026-01-08  
**Authority**: CS2 Decision (Johan Ras)  
**Source**: APGI-cmy/maturion-foreman-governance#901  
**Trigger**: PR APGI-cmy/maturion-foreman-office-app#504 test dodging incident  
**Status**: ACTIVE - Constitutional Enforcement

---

## Purpose

This policy bans the use of minimizing language when describing test failures, technical debt, or build quality issues. Such language enables test dodging, normalizes debt, and undermines the constitutional 100% GREEN mandate.

---

## Policy Statement

**Minimizing language is BANNED in all communication about test results, build status, and technical debt.**

### Banned Terms

The following terms are **PROHIBITED** when describing failures, warnings, or incomplete work:

❌ **"only"** (e.g., "only 5 tests failing")  
❌ **"just"** (e.g., "just documentation nits")  
❌ **"minor"** (e.g., "minor test failures")  
❌ **"non-blocking"** (e.g., "non-blocking warnings")  
❌ **"trivial"** (e.g., "trivial issues")  
❌ **"simple"** (e.g., "simple fix needed")  
❌ **"small"** (e.g., "small number of failures")  
❌ **"few"** (e.g., "a few tests failing")  

### Required Language

When reporting status, use **accurate, non-minimizing descriptions**:

✅ **"100% tests passing"** - When all tests pass  
✅ **"NOT READY - X tests failing"** - When any test fails  
✅ **"BUILD INCOMPLETE - Y warnings present"** - When warnings exist  
✅ **"BLOCKED - technical debt prevents GREEN"** - When debt exists  
✅ **"COMPLETE - all tests GREEN, zero warnings"** - When actually complete  

---

## Rationale

### The Psychology of Minimizing Language

Minimizing language serves psychological purposes, not technical ones:

1. **Reduces Perceived Severity**  
   - "Only 5 tests" feels less serious than "5 tests failing"
   - Creates false sense of progress
   - Normalizes incomplete work

2. **Enables Test Dodging**  
   - Softens rejection resistance
   - Makes "close enough" seem acceptable
   - Undermines zero-tolerance enforcement

3. **Compounds Over Time**  
   - "Only 5" becomes "only 10" becomes "only 50"
   - Each use lowers the bar further
   - Eventually normalizes catastrophic debt

### Historical Evidence

**PR #504 Incident** (2026-01-08):  
- Builder declared "COMPLETE" with 92% pass rate (8% failing)
- Used minimizing language to describe failures
- Attempted to normalize partial completion
- **Result**: Rejection, policy creation, constitutional enforcement

**Pattern Recognition**:  
- Every major test dodging incident involved minimizing language
- "Only", "just", "minor" = universal early warning signal
- Language shift precedes governance violation

---

## Scope

### Applies To

This policy applies to **ALL** of the following:

- **PR descriptions** and comments
- **Issue reports** and updates
- **Builder completion reports**
- **QA reports** and evidence
- **Status updates** and handovers
- **Verbal communication** in meetings
- **Documentation** about build state
- **Commit messages** describing fixes
- **Code comments** about test status

### Enforcement Contexts

1. **PR Review**  
   - Automatic rejection if minimizing language detected
   - No exceptions without CS2 approval

2. **Builder Handovers**  
   - Handover rejected if status minimized
   - Resubmission required with accurate language

3. **Issue Creation**  
   - Issues using minimizing language returned for revision
   - Accurate severity assessment required

4. **Governance Escalation**  
   - Escalations using minimizing language deprioritized
   - Severity reassessment required

---

## Exceptions

### Approved Contexts (Limited)

Minimizing language MAY be used in these **specific contexts only**:

1. **Describing Improvements**  
   ✅ "Only 2 steps required" (when reducing complexity)  
   ✅ "Just one command to run" (when simplifying process)

2. **Historical Comparison**  
   ✅ "Previously 50 failures, now only 5" (showing progress trend)  
   ✅ "Was 365 warnings, currently just 10" (quantifying reduction)

3. **Effort Estimation**  
   ✅ "Only 1 hour to fix" (when estimating resolution time)  
   ✅ "Just needs documentation" (when work is trivial)

### Key Distinction

**NOT ALLOWED**: Minimizing **current failures/debt**  
**ALLOWED**: Describing **simplicity** or **progress**

**Test**: If the word makes a failure seem less serious, it's BANNED.

---

## Enforcement

### Detection

**Automated Detection** (CI/PR gates):
- Scan PR descriptions for banned terms
- Flag comments using minimizing language
- Reject PRs with policy violations

**Manual Review** (FM/GA):
- Review handover language
- Assess status reporting accuracy
- Enforce policy in escalations

### Consequences

| Violation | Consequence |
|-----------|-------------|
| **First Use** | PR/handover **REJECTED** with policy reference |
| **Second Use** | **Mandatory policy training** + resubmission |
| **Third Use** | **Builder accountability review** with FM/CS2 |
| **Habitual Use** | **Builder removal** from project |

### Appeal Process

If minimizing language detected:

1. **No Appeal for Clear Violations**  
   - "Only 5 tests failing" = clear violation, no appeal

2. **Appeal for Edge Cases**  
   - Ambiguous usage may be appealed to FM
   - FM decision final, CS2 escalation available

3. **CS2 Override**  
   - Only CS2 can grant exceptions
   - Must document rationale
   - Exception does not create precedent

---

## Training Requirements

### Mandatory Reading

Before submitting ANY builder work, ALL builders MUST:

1. ✅ Read this policy in full
2. ✅ Study `bootstrap/learnings/BOOTSTRAP-TEST-DODGING-001.md` case study
3. ✅ Pass policy quiz (10/10 required)
4. ✅ Sign acknowledgment of banned language policy

### Training Materials

**Policy Quiz** includes:
- Identify banned language in sample text
- Rewrite minimizing statements accurately
- Explain psychological impact of minimizing language
- Describe enforcement process

**Case Study** (BOOTSTRAP-TEST-DODGING-001):
- PR #504 incident analysis
- How minimizing language enabled test dodging
- Consequences of policy violation
- Correct vs. incorrect status reporting

---

## Examples

### ❌ INCORRECT (Banned Language)

**PR Description**:
> "Implementation complete. Only 5 tests failing, just need minor fixes. Non-blocking issues remain."

**Problems**:
- "Only 5 tests" = minimizes failures
- "Just need minor fixes" = normalizes debt
- "Non-blocking issues" = false urgency assessment

**Correct Status**: NOT READY - 5 tests failing

---

### ✅ CORRECT (Accurate Language)

**PR Description**:
> "Implementation NOT READY. 5 tests failing, require fixes before merge. Known issues documented below."

**Why Correct**:
- "NOT READY" = honest assessment
- "5 tests failing" = factual, non-minimizing
- "Require fixes" = clear expectation
- No language softening severity

---

### ❌ INCORRECT (False Completion)

**Builder Report**:
> "Work is essentially done. Only a few documentation warnings and some non-critical test failures."

**Problems**:
- "Essentially done" = false claim
- "Only a few" = minimizes scope
- "Non-critical" = subjective severity assessment

**Correct Status**: INCOMPLETE - X warnings, Y test failures

---

### ✅ CORRECT (Honest Status)

**Builder Report**:
> "Work INCOMPLETE. 12 documentation warnings present. 3 tests failing. Resolution plan attached."

**Why Correct**:
- "INCOMPLETE" = binary status
- Specific counts provided
- No severity minimization
- Resolution plan included

---

## Integration with Existing Governance

### Constitutional Alignment

This policy enforces:

1. **T0-002 Governance Supremacy Rule** (99% is 0%)
   - 100% or nothing
   - No partial credit
   - Minimizing language enables "close enough" thinking

2. **T0-003 Zero Test Debt Constitutional Rule**
   - All tests GREEN or documented RED
   - No normalized failures
   - Minimizing language normalizes debt

3. **BUILD_PHILOSOPHY.md** (One-Time Build Correctness)
   - Quality designed in
   - First build GREEN
   - Minimizing language defers quality

### Policy Hierarchy

**POLICY-NO-ONLY-LANGUAGE** is:
- **SUBORDINATE** to constitutional rules (T0-002, T0-003)
- **ENFORCES** constitutional 100% GREEN mandate
- **PREVENTS** test dodging patterns
- **SUPPORTS** Build-to-Green methodology

---

## Monitoring and Compliance

### Compliance Metrics

Track and report:

1. **Policy Violations per Sprint**
   - Count of rejected PRs/handovers
   - Builder-specific violation tracking
   - Trend analysis

2. **Language Pattern Analysis**
   - Frequency of banned terms in commits/PRs
   - Correlation with test debt incidents
   - Training effectiveness measurement

3. **Cultural Shift Indicators**
   - Reduction in minimizing language over time
   - Increase in accurate status reporting
   - Improvement in first-time completion rates

### Reporting

**Monthly Report** to CS2/FM:
- Violation count and trends
- Builder compliance rates
- Training completion status
- Policy effectiveness assessment

---

## Review and Updates

### Annual Review

This policy SHALL be reviewed annually:

- **Effectiveness**: Is it preventing test dodging?
- **Scope**: Are banned terms comprehensive?
- **Enforcement**: Are consequences appropriate?
- **Training**: Are builders complying?

### Amendment Process

To amend this policy:

1. **Proposal** to FM with rationale
2. **FM Review** and recommendation
3. **CS2 Approval** required for changes
4. **Version Update** and republication
5. **Builder Notification** and retraining

---

## References

**Source Documentation**:
- `bootstrap/learnings/BOOTSTRAP-TEST-DODGING-001.md` (PR #504 case study)
- `governance/policies/TEST_REMOVAL_GOVERNANCE_GATE_LOCAL.md` (test removal policy)
- `governance/policies/zero-test-debt-constitutional-rule.md` (T0-003)
- `governance/policies/governance-supremacy-rule.md` (T0-002)
- `BUILD_PHILOSOPHY.md` (One-Time Build Correctness)

**Related Policies**:
- **TEST_REMOVAL_GOVERNANCE_GATE_LOCAL.md** - Prevents test removal
- **ZERO_WARNING_TEST_DEBT_IMMEDIATE_REMEDY_DOCTRINE.md** - Enforces immediate warning fixes
- **zero-test-debt-constitutional-rule.md** - Constitutional 100% GREEN mandate

**Incident Reports**:
- PR #504 (2026-01-08): Test dodging via minimizing language

---

## Authority and Approval

**Enacted By**: CS2 (Johan Ras)  
**Date**: 2026-01-08  
**Effective**: Immediately  
**Scope**: ALL builders, ALL repositories  
**Enforcement**: Mandatory, no exceptions without CS2 approval  

**Policy Owner**: Foreman (FM)  
**Enforcement Authority**: Foreman (FM) + Governance Administrator (GA)  
**Appeal Authority**: CS2 (Johan Ras)

---

## Summary

**Banned Language**: "only", "just", "minor", "non-blocking", "trivial", "simple", "small", "few"

**Required Language**: "100% tests passing" OR "NOT READY - X tests failing"

**Enforcement**: Automatic rejection, no exceptions without CS2 approval

**Purpose**: Prevent test dodging, maintain 100% GREEN mandate, eliminate debt normalization

**Authority**: Constitutional enforcement under T0-002 and T0-003

---

**This policy is ACTIVE and MANDATORY. All builders MUST comply.**

**Violations will result in immediate work rejection and potential builder accountability review.**

**Questions or appeals: Escalate to FM → GA → CS2**

---

**END OF POLICY**
