# ZWZDI Prevention Protocols & Checklist

**Campaign ID**: ZWZDI-2026-001  
**Phase**: Prevention  
**Document Type**: Prevention Protocols & Implementation Checklist  
**Date**: 2026-01-08  
**Author**: Foreman (FM)  
**Authority**: CS2 (Johan Ras)

---

## I. Executive Summary

This document defines the systematic prevention mechanisms implemented following the ZWZDI campaign to ensure future warning and test debt accumulation is prevented at the source.

---

## II. Prevention Gates (CI/CD Integration)

### A. Zero-Warning Merge Gate

**Purpose**: Block any PR that introduces warnings

**Implementation**:
```yaml
# .github/workflows/zero-warning-gate.yml
name: Zero Warning Gate

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  warning-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests with warning enforcement
        run: |
          pytest tests/ -v --strict-warnings
          if [ $? -ne 0 ]; then
            echo "❌ FAILED: Warnings detected - PR BLOCKED"
            exit 1
          fi
          echo "✅ PASSED: Zero warnings confirmed"
```

**Enforcement**: PRs cannot merge with ANY warnings present

### B. Test Debt Detection Gate

**Purpose**: Block any PR that introduces test debt

**Implementation**:
```yaml
# .github/workflows/test-debt-gate.yml
name: Test Debt Gate

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  debt-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Detect test debt patterns
        run: |
          # Check for skipped tests
          if grep -r "\.skip\|@pytest\.mark\.skip" tests/; then
            echo "❌ FAILED: Skipped tests detected"
            exit 1
          fi
          
          # Check for TODO/FIXME in tests
          if grep -r "TODO\|FIXME" tests/*.py; then
            echo "❌ FAILED: TODO/FIXME found in tests"
            exit 1
          fi
          
          echo "✅ PASSED: No test debt patterns found"
```

**Enforcement**: PRs cannot merge with test debt patterns

### C. Minimizing Language Linter

**Purpose**: Block PRs with banned minimizing language

**Implementation**:
```yaml
# .github/workflows/language-linter.yml
name: Minimizing Language Linter

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  language-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check for minimizing language
        run: |
          # Check PR body and commit messages
          BANNED_PATTERNS="only [0-9]+ (test|warning|failure)|just (some|a few)|minor (issue|failure|warning)|non-blocking"
          
          if echo "${{ github.event.pull_request.body }}" | grep -iE "$BANNED_PATTERNS"; then
            echo "❌ FAILED: Minimizing language detected in PR description"
            echo "Reference: POLICY-NO-ONLY-LANGUAGE"
            exit 1
          fi
          
          echo "✅ PASSED: No minimizing language detected"
```

**Enforcement**: PRs with minimizing language are automatically flagged

---

## III. Prevention Checklist (Builder Pre-Submission)

### A. Before Submitting ANY Work

Every builder MUST verify:

**Test Suite Verification**:
- [ ] All tests executed: `pytest tests/ -v`
- [ ] Zero test failures (excluding documented QA-to-Red)
- [ ] Zero warnings in test output
- [ ] Zero skipped tests (unless documented QA-to-Red)
- [ ] No TODO/FIXME in test files

**Code Quality Verification**:
- [ ] All linting passing
- [ ] No deprecation warnings in my code
- [ ] No type warnings
- [ ] No unused imports

**Language Verification**:
- [ ] No "only X failing" in any description
- [ ] No "just some warnings" language
- [ ] No "minor issues" minimizing
- [ ] Accurate status: "100% passing" OR "NOT READY - X failing"

**Documentation Verification**:
- [ ] All changes documented
- [ ] Evidence artifacts complete
- [ ] Completion report accurate

### B. Builder Self-Certification Statement

Before claiming completion, builders MUST be able to honestly state:

> "I certify that:
> 1. All tests in my scope are passing (100%)
> 2. Zero warnings exist in my scope
> 3. No test debt patterns exist in my code
> 4. I have not used minimizing language
> 5. My completion claim reflects actual state"

---

## IV. Prevention Checklist (FM Pre-Authorization)

### A. Before Authorizing Any Wave/Subwave

FM MUST verify (extends BL-018, BL-019, BL-020):

**QA Catalog Verification**:
- [ ] QA range exists in QA_CATALOG.md (BL-018)
- [ ] QA definitions semantically match subwave scope (BL-019)
- [ ] QA-to-Red test files exist in repository (BL-020)
- [ ] Test file paths in spec are accurate

**Baseline Verification**:
- [ ] Full test suite run before authorization
- [ ] Zero warnings in baseline
- [ ] Zero test debt in baseline
- [ ] All prior wave cleanup verified

**Documentation Verification**:
- [ ] Sub-issue specification complete
- [ ] Builder assignment clear
- [ ] Success criteria defined
- [ ] Evidence requirements specified

### B. FM Authorization Statement

Before authorizing work, FM MUST be able to honestly state:

> "I certify that:
> 1. QA range verified (BL-018)
> 2. Semantic alignment verified (BL-019)
> 3. Test existence verified (BL-020)
> 4. Zero warnings in baseline
> 5. Zero test debt in baseline
> 6. Builder is trained on governance"

---

## V. Prevention Checklist (Verification Phase)

### A. Before Accepting Completion Claims

FM MUST verify:

**Test Suite Validation**:
- [ ] Full test suite executed: `pytest tests/ -v --tb=short`
- [ ] Test count matches expected
- [ ] Pass count verified (excluding QA-to-Red)
- [ ] Warning count is ZERO
- [ ] No skipped tests (excluding documented QA-to-Red)

**Evidence Validation**:
- [ ] Completion report exists
- [ ] Test output evidence attached
- [ ] All claims match actual results
- [ ] No minimizing language in reports

**Language Validation**:
- [ ] No "only X failing" in any submission
- [ ] No "just" / "minor" / "non-blocking"
- [ ] Status accurately reflects test results
- [ ] "COMPLETE" only used when 100% GREEN

---

## VI. Risks and Countermeasures

### Risk 1: Warning Accumulation (Recurrence)

**Risk**: Warnings accumulate again over time

**Probability**: MEDIUM (without gates)  
**Impact**: HIGH (leads to debt crisis)

**Countermeasures**:
1. ✅ Zero-warning merge gate (CI enforcement)
2. ✅ Daily warning count audit (FM responsibility)
3. ✅ Builder self-check obligation
4. ✅ Immediate remedy doctrine (ZERO_WARNING_TEST_DEBT_IMMEDIATE_REMEDY_DOCTRINE.md)

**Residual Risk**: LOW (with countermeasures active)

### Risk 2: Test Debt Introduction

**Risk**: Test debt introduced through skips, TODOs, stubs

**Probability**: MEDIUM (common developer pattern)  
**Impact**: HIGH (undermines QA reliability)

**Countermeasures**:
1. ✅ Test debt detection gate (CI enforcement)
2. ✅ Pre-commit hooks (local enforcement)
3. ✅ Builder training on zero-test-debt-constitutional-rule.md
4. ✅ FM verification of completion claims

**Residual Risk**: LOW (with countermeasures active)

### Risk 3: Test Dodging via Language

**Risk**: Minimizing language masks failures

**Probability**: MEDIUM (natural human tendency)  
**Impact**: HIGH (enables debt hiding)

**Countermeasures**:
1. ✅ POLICY-NO-ONLY-LANGUAGE (explicit ban)
2. ✅ Language linter (automated detection)
3. ✅ Builder training on BOOTSTRAP-TEST-DODGING-001
4. ✅ FM verification of language in submissions

**Residual Risk**: LOW (with policy enforced)

### Risk 4: Incomplete Wave Planning

**Risk**: Wave authorization without proper verification

**Probability**: LOW (after BL-018, BL-019, BL-020)  
**Impact**: HIGH (causes builder blocks)

**Countermeasures**:
1. ✅ BL-018: QA range verification mandatory
2. ✅ BL-019: Semantic alignment verification mandatory
3. ✅ BL-020: Test existence verification mandatory
4. ✅ FM Pre-Authorization Checklist

**Residual Risk**: LOW (with BL learnings enforced)

### Risk 5: Governance Erosion Over Time

**Risk**: Policies weakened or ignored over time

**Probability**: LOW (strong governance culture)  
**Impact**: CRITICAL (undermines entire system)

**Countermeasures**:
1. ✅ Constitutional enforcement (non-negotiable)
2. ✅ CS2 authority for exceptions only
3. ✅ Bootstrap learning registry (permanent memory)
4. ✅ Continuous governance audits

**Residual Risk**: MINIMAL (with constitutional enforcement)

---

## VII. Ongoing Monitoring

### A. Daily Checks (FM Responsibility)

1. **Warning Count Audit**:
   - Run: `pytest tests/ -v 2>&1 | grep "warning" | wc -l`
   - Expected: 0
   - Action if > 0: IMMEDIATE STOP, investigate, remediate

2. **Test Debt Scan**:
   - Run: `grep -r "\.skip\|TODO\|FIXME" tests/`
   - Expected: No matches (excluding documented QA-to-Red)
   - Action if matches: IMMEDIATE STOP, investigate, remediate

3. **Language Review**:
   - Review all PR descriptions and completion claims
   - Flag any minimizing language
   - Action if found: REJECT, require accurate language

### B. Weekly Audits (FM Responsibility)

1. **Full Suite Validation**:
   - Run complete test suite
   - Verify zero warnings, zero debt
   - Document in weekly report

2. **Governance Compliance Review**:
   - Verify all active work follows policies
   - Check builder training status
   - Review any exception requests

3. **Trend Analysis**:
   - Compare warning/debt counts week-over-week
   - Identify any upward trends
   - Escalate concerning patterns to CS2

---

## VIII. Success Criteria

Prevention Phase is SUCCESSFUL when:

1. ✅ **Zero-warning gate** active and enforced
2. ✅ **Test debt gate** active and enforced
3. ✅ **POLICY-NO-ONLY-LANGUAGE** enacted and enforced
4. ✅ **All builders** trained and acknowledged policies
5. ✅ **Bootstrap learning** (BOOTSTRAP-TEST-DODGING-001) documented
6. ✅ **Prevention checklist** integrated into workflows
7. ✅ **Ongoing monitoring** procedures established
8. ✅ **Risk countermeasures** active and verified
9. ✅ **CS2 approval** obtained for campaign closure

---

## IX. Document References

### A. Created in Prevention Phase

1. `governance/policies/POLICY-NO-ONLY-LANGUAGE.md` - Minimizing language ban
2. `bootstrap/learnings/BOOTSTRAP-TEST-DODGING-001.md` - Test dodging case study
3. `governance/zero-debt-campaign/ZWZDI_PREVENTION_PROTOCOLS.md` - This document
4. `governance/zero-debt-campaign/ZWZDI_POSTMORTEM_REPORT.md` - Campaign postmortem

### B. Updated in Prevention Phase

1. `governance/zero-debt-campaign/GOVERNANCE_LEARNING_BRIEF.md` - Added "Only" Language Ban section
2. `governance/zero-debt-campaign/PLANNING_PHASE_COMPLETION_SUMMARY.md` - Policy integration
3. `governance/zero-debt-campaign/PROGRESS_TRACKER.md` - Prevention Phase status
4. `BOOTSTRAP_EXECUTION_LEARNINGS.md` - BL-021 entry

### C. Referenced Governance

1. `governance/policies/zero-test-debt-constitutional-rule.md` (T0-003)
2. `governance/policies/ZERO_WARNING_TEST_DEBT_IMMEDIATE_REMEDY_DOCTRINE.md`
3. `governance/policies/governance-supremacy-rule.md` (T0-002)
4. `governance/contracts/quality-integrity-contract.md`

---

## X. Authority and Approval

**Document**: ZWZDI Prevention Protocols  
**Status**: COMPLETE - Pending CS2 Approval  
**Date**: 2026-01-08  
**Author**: Foreman (FM)  
**Authority**: CS2 (Johan Ras)  
**Campaign**: ZWZDI-2026-001

**Next Step**: CS2 review and approval for campaign closure (Issue #508)

---

*END OF ZWZDI PREVENTION PROTOCOLS*
