# Build-to-Green Enforcement Specification

**Version**: 1.0.0  
**Status**: Active and Enforced  
**Constitutional Authority**: BUILD_PHILOSOPHY.md + Governance Supremacy Rule  
**Last Updated**: 2025-12-16

---

## I. Purpose and Authority

### Purpose

This specification defines the **enforcement mechanisms** for true Build-to-Green semantics in the Maturion ecosystem.

**Objective**: Make it **impossible** to cheat green status.

### Constitutional Authority

This enforcement is mandated by:
- **BUILD_PHILOSOPHY.md** (Supreme Constitutional Authority)
- **Governance Supremacy Rule** (GSR Pillar 1: 100% QA Passing is ABSOLUTE)
- **Zero Test Debt Constitutional Rule** (Zero test debt is mandatory)
- **Build to Green Rule** (Builders only accept "Build to Green" instructions)

### Core Principle

**Green means GREEN.**

- Not "mostly green"
- Not "green except for..."
- Not "functionally green"
- **GREEN** = 100% compliance, zero exceptions

---

## II. What Build-to-Green Enforcement Prevents

### 1. Skipped Tests

**BLOCKED**:
- `.skip()` - Tests marked as skipped
- `.todo()` - Tests marked as TODO
- `.only()` - Focused tests (other tests don't run)
- `@pytest.mark.skip` - Python skipped tests
- `@pytest.mark.xfail` - Expected failure tests
- Commented out tests

**Why**: If a test exists, it must run and pass. No exceptions.

### 2. Suppressed Failures

**BLOCKED**:
- Tests that pass but don't actually test anything
- Stub tests with no assertions
- Tests with suppressed errors
- Tests with `expect(true).toBe(true)` (meaningless assertions)
- Test infrastructure that isn't implemented

**Why**: Tests must verify actual behavior, not just exist.

### 3. Partial Passes

**BLOCKED**:
- 99% passing = FAILURE
- 301/303 tests passing = FAILURE
- ANY test failure = BUILD BLOCKED

**Why**: 100% means 100%. Not 99.9%. Not "close enough".

### 4. Hidden Test Debt

**BLOCKED**:
- Tests excluded from test runs
- Test files in .gitignore
- Tests in jest.config exclude list
- TODO/FIXME markers in test code

**Why**: Test debt must be visible and fixed, not hidden.

---

## III. Enforcement Mechanisms

### Level 1: Pre-Commit Hooks (Local)

**Location**: `.githooks/pre-commit`

**Checks**:
- Scan for `.skip()`, `.todo()`, `.only()` patterns
- Scan for TODO/FIXME in test files
- Scan for commented out test blocks
- Block commit if violations found

**Action**: Prevent commit with violations

**Bypass**: NOT ALLOWED (constitutional rule)

### Level 2: CI/CD Workflow (Automated)

**Location**: `.github/workflows/build-to-green-enforcement.yml`

**Jobs**:

1. **enforce-zero-test-debt**
   - Runs `foreman/scripts/detect-test-debt.py`
   - Scans all test files for debt
   - BLOCKS build if debt detected

2. **enforce-100-percent-pass**
   - Runs `foreman/scripts/validate-qa-green.py`
   - Validates 100% pass requirement
   - BLOCKS build if not 100% green

3. **enforce-no-suppressed-failures**
   - Runs tests with strict mode
   - Checks for xfail/xpass markers
   - Checks for .only() focused tests
   - BLOCKS build if suppressions found

4. **enforce-constitutional-compliance**
   - Verifies constitutional files not modified
   - Generates enforcement summary
   - Reports compliance status

**Action**: Hard fail CI if any check fails

**Bypass**: NOT ALLOWED (constitutional rule)

### Level 3: Foreman Review (Orchestration)

**When**: Before merge approval

**Checks**:
- Review CI enforcement results
- Verify evidence trail complete
- Validate architectural compliance
- Confirm zero governance violations

**Action**: Reject merge if any violations

**Override**: Only by Johan (Owner Override)

### Level 4: Human Review (Final Gate)

**When**: Final merge approval

**Checks**:
- Verify all automated checks passed
- Review enforcement summary
- Confirm business requirements met

**Action**: Final approval or rejection

---

## IV. Violation Types and Remediation

### Violation Type 1: Skipped Tests

**Detection**:
```bash
python foreman/scripts/detect-test-debt.py
```

**Example Violations**:
- `it.skip('should validate email', ...)`
- `@pytest.mark.skip(reason="not implemented")`
- `// it('should handle errors', ...)`

**Remediation**:
1. Remove `.skip()` or `.todo()`
2. Implement the test fully
3. Ensure test passes
4. Re-run enforcement checks

**NOT Allowed**:
- ❌ Remove test entirely to avoid debt
- ❌ Comment out test instead of fixing
- ❌ Change test to meaningless assertion

**Required**: Complete test implementation

### Violation Type 2: Partial Pass

**Detection**:
```bash
python foreman/scripts/validate-qa-green.py
```

**Example Violations**:
- `73 passed, 1 failed` → BLOCKED
- `301 passed, 2 failed` → BLOCKED
- `99% passing` → BLOCKED

**Remediation**:
1. Identify failing tests
2. Fix ALL failures
3. Achieve 100% pass
4. Re-run validation

**NOT Allowed**:
- ❌ Skip failing tests
- ❌ Comment out failing tests
- ❌ Mark tests as xfail

**Required**: All tests must pass

### Violation Type 3: Stub Tests

**Detection**:
```bash
python foreman/scripts/detect-test-debt.py
```

**Example Violations**:
```python
def test_process_payment():
    # TODO: implement this
    pass
```

```javascript
it('should validate email', () => {
  expect(true).toBe(true)  // Meaningless
})
```

**Remediation**:
1. Implement actual test logic
2. Add meaningful assertions
3. Verify test actually tests something
4. Re-run enforcement checks

**NOT Allowed**:
- ❌ Keep stub and mark as TODO
- ❌ Add meaningless assertion to pass
- ❌ Remove test entirely

**Required**: Complete test implementation with real assertions

### Violation Type 4: Suppressed Failures

**Detection**:
```bash
CI checks for xfail/xpass markers
```

**Example Violations**:
- `@pytest.mark.xfail` - Expected to fail
- Tests that silently catch and ignore errors
- Tests in exclude lists

**Remediation**:
1. Remove suppression markers
2. Fix underlying issue
3. Make test pass cleanly
4. Re-run validation

**NOT Allowed**:
- ❌ Keep xfail marker
- ❌ Suppress errors in test
- ❌ Exclude from test run

**Required**: Test must pass without suppression

---

## V. Enforcement Scripts

### Script 1: detect-test-debt.py

**Purpose**: Detect all forms of test debt

**Usage**:
```bash
python foreman/scripts/detect-test-debt.py --test-dir tests
python foreman/scripts/detect-test-debt.py --test-dir tests --json
```

**Detects**:
- Skipped tests (`.skip()`, `.todo()`, `.only()`)
- Commented out tests
- Stub tests (no assertions)
- TODO/FIXME markers
- Incomplete test infrastructure

**Output**:
- Human-readable report (default)
- JSON report (--json flag)

**Exit Codes**:
- 0 = No test debt (PASS)
- 1 = Test debt detected (FAIL)

### Script 2: validate-qa-green.py

**Purpose**: Validate 100% pass requirement

**Usage**:
```bash
python foreman/scripts/validate-qa-green.py --test-dir tests
python foreman/scripts/validate-qa-green.py --test-dir tests --json
```

**Validates**:
- 100% tests passing (not 99%)
- Zero test failures
- Zero skipped tests
- Zero errors
- Zero warnings

**Output**:
- Human-readable report (default)
- JSON report (--json flag)

**Exit Codes**:
- 0 = QA is GREEN (PASS)
- 1 = QA is not GREEN (FAIL)

---

## VI. CI/CD Workflow Integration

### Workflow File

**Location**: `.github/workflows/build-to-green-enforcement.yml`

### Trigger Events

- `pull_request` to main or develop
- `push` to main or develop
- `workflow_dispatch` (manual trigger)

### Job Sequence

```
enforce-zero-test-debt
    ↓
enforce-100-percent-pass
    ↓
enforce-no-suppressed-failures
    ↓
enforce-constitutional-compliance
    ↓
report-enforcement-status
```

**Sequential**: Each job depends on previous job passing

**Fail-Fast**: If any job fails, workflow stops and build is BLOCKED

### Artifacts

Generated artifacts:
- `test-debt-report.json` - Test debt detection results
- `qa-green-report.json` - QA validation results
- `enforcement-summary.md` - Overall enforcement summary

**Retention**: 30 days

---

## VII. Audit Trail Requirements

### Evidence Required

For every build, enforcement generates:

1. **Test Debt Report**
   - Timestamp
   - Violations detected (if any)
   - Files and line numbers
   - Severity levels

2. **QA Green Report**
   - Test counts (total, passed, failed, skipped)
   - Pass percentage
   - Violations (if any)
   - Green/Red status

3. **Enforcement Summary**
   - All checks performed
   - Results of each check
   - Final approval/block decision
   - Constitutional references

### Storage

- Artifacts stored in GitHub Actions
- Reports available for download
- Audit trail preserved for compliance

---

## VIII. Bypass and Override

### Bypass: NOT ALLOWED

**NO bypass mechanisms exist for:**
- Test debt detection
- 100% pass requirement
- Suppressed failure detection

**Reason**: These are constitutional requirements, not guidelines.

### Owner Override

**Johan (Owner) may temporarily override** for:
- Emergency production fixes
- Critical security patches

**Override Characteristics**:
- Temporary (specific instance only)
- Explicit (clearly documented)
- Followed by mandatory cleanup

**Process**:
1. Johan states override explicitly
2. Override logged in evidence trail
3. Build proceeds with violations
4. Tracking issue created for cleanup
5. Cleanup completed within 48 hours
6. Normal enforcement resumes

---

## IX. Integration with Build Philosophy

### Implements Build Philosophy Principles

**Principle 1: One-Time Build Correctness**
- Enforcement ensures QA is complete before build
- No incomplete tests allowed

**Principle 2: Zero Regression**
- 100% pass requirement prevents regressions
- All tests must pass, always

**Principle 4: Governance Supremacy**
- Enforcement is absolute, not negotiable
- Rules override all other considerations

**Principle 5: Zero Ambiguity**
- Green/Red status is unambiguous
- No subjective interpretation

### Integration Points

```
BUILD_PHILOSOPHY.md
    ↓
Governance Supremacy Rule
    ↓
Build-to-Green Enforcement (This Spec)
    ↓
Enforcement Scripts + CI/CD Workflow
```

---

## X. Success Metrics

### Enforcement Effectiveness

**Target Metrics**:
- ✅ 100% of builds pass enforcement (or are blocked)
- ✅ Zero test debt in merged code
- ✅ 100% test pass rate in merged code
- ✅ Zero false positives (correct violations only)
- ✅ < 1 minute enforcement execution time

**Monitoring**:
- Track enforcement failures per week
- Track violation types and frequencies
- Track remediation time per violation
- Track override frequency (should be near zero)

### Quality Impact

**Expected Outcomes**:
- Zero ambiguity about green status
- Complete audit trail for compliance
- Impossible to merge with test debt
- Impossible to merge with partial passes
- Constitutional compliance guaranteed

---

## XI. Troubleshooting

### Issue: "CI keeps failing with test debt detected"

**Solution**:
1. Run `python foreman/scripts/detect-test-debt.py` locally
2. Fix all detected violations
3. Re-run script to verify zero debt
4. Commit and push

### Issue: "99% passing but CI blocks merge"

**Solution**:
1. This is correct behavior (GSR: 100% required)
2. Fix failing test(s)
3. Achieve 100% pass
4. CI will approve

**NOT a Solution**: Skip failing test (will be detected)

### Issue: "Test is flaky, can I skip it temporarily?"

**Solution**:
1. NO - skipping not allowed
2. Fix the flakiness
3. Make test reliable
4. Then merge

**NOT a Solution**: Skip until later (test debt prohibited)

---

## XII. Version and Authority

**Version**: 1.0.0  
**Status**: Active and Enforced  
**Authority**: Constitutional Authority (Build Philosophy Implementation)  
**Precedence**: Enforceable at CI/CD level (automatic blocking)  
**Last Updated**: 2025-12-16  
**Owner**: Johan (MaturionISMS)  
**Enforcer**: CI/CD + Foreman + Human Review

**Changelog**:
- 1.0.0 (2025-12-16): Initial Build-to-Green Enforcement Specification

---

## XIII. Summary: The Commitment

Build-to-Green Enforcement commits to:

1. ✅ **Zero Test Debt** - No skipped, commented, or stub tests
2. ✅ **100% Pass Rate** - Not 99%, not 301/303, exactly 100%
3. ✅ **No Suppression** - No hidden failures, no cheating
4. ✅ **Full Auditability** - Complete evidence trail
5. ✅ **Constitutional Enforcement** - Automatic and absolute

**Green means GREEN.**  
**No exceptions. No compromises. No cheating.**

---

*END OF BUILD-TO-GREEN ENFORCEMENT SPECIFICATION*
