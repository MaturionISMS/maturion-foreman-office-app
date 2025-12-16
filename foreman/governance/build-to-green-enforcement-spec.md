# Build-to-Green Enforcement Specification

**Version**: 1.0.0  
**Status**: Active and Enforced  
**Authority**: Build Philosophy + Governance Supremacy Rule + Zero Test Debt Constitutional Rule  
**Last Updated**: 2025-12-16

---

## I. Constitutional Authority

### Hierarchy

```
BUILD_PHILOSOPHY.md (Supreme Authority)
    ↓
Principle #3: Build to Green
    ↓
Governance Supremacy Rule (GSR)
    ↓
Zero Test Debt Constitutional Rule
    ↓
Build-to-Green Rule
    ↓
Build-to-Green Enforcement Specification (This Document)
```

### Enforcement Level

**BLOCKING**: This specification implements blocking enforcement at all levels:
- Local (pre-commit hooks)
- CI/CD (automated workflows)
- Oversight (Foreman QA-of-QA)

**No bypasses without Owner override.**

---

## II. Core Requirements

### Requirement 1: Zero Test Debt (ABSOLUTE)

**Definition**: Test debt is any form of incomplete, skipped, or deferred testing.

**Forbidden Forms**:
1. Skipped tests: `.skip()`, `.todo()`, `.only()`, `@pytest.mark.skip`
2. Commented out tests
3. Stub tests with no assertions
4. `TODO`/`FIXME` markers in test files
5. Incomplete test infrastructure (stub helpers, broken mocks)
6. Suppressed errors in tests
7. Excluded tests in configuration

**Enforcement**:
- Pre-commit hook scans and blocks
- CI/CD detects and hard-fails
- QA-of-QA validates compliance

**Exit on Detection**: Build BLOCKED until all debt removed

### Requirement 2: 100% Pass Rate (ABSOLUTE)

**Definition**: ALL tests must pass. No exceptions.

**Pass Criteria**:
- Total tests = Passed tests
- Failed tests = 0
- Errors = 0
- Skipped tests = 0
- Warnings = 0
- Exit code = 0

**Rejection Criteria** (any trigger BLOCKS build):
- 99% pass rate = FAILURE
- 301/303 tests = FAILURE
- Any test failure = BLOCKED
- Any test error = BLOCKED
- Any skipped test = BLOCKED
- Any warning = BLOCKED
- Non-zero exit code = BLOCKED

**Enforcement**:
- CI/CD validates and hard-fails
- No partial pass acceptance
- GSR Pillar 1 absolute enforcement

### Requirement 3: Constitutional File Protection

**Definition**: Protected files cannot be modified without CS2 approval.

**Protected Paths**:
```
BUILD_PHILOSOPHY.md
foreman/constitution/
foreman/governance/governance-supremacy-rule.md
foreman/governance/zero-test-debt-constitutional-rule.md
foreman/builder-specs/build-to-green-rule.md
.github/workflows/build-to-green-enforcement.yml
```

**Enforcement**:
- Pre-commit warns and prompts for authorization
- CI/CD detects and warns
- Requires Owner (Johan) review

---

## III. Detection Mechanisms

### A. Test Debt Detection (`detect-test-debt.py`)

**Purpose**: Scan test files for patterns indicating test debt

**Patterns Detected**:

#### Skip Markers
- `.skip(` - JavaScript/TypeScript skip
- `describe.skip` - Suite skip
- `it.skip` - Test skip
- `test.skip` - Jest skip
- `@pytest.mark.skip` - Pytest skip decorator

#### TODO Markers
- `.todo(` - JavaScript/TypeScript todo
- `test.todo` - Jest todo
- `it.todo` - Mocha todo
- `@pytest.mark.xfail` - Pytest expected fail

#### Only Markers (should not be committed)
- `.only(` - Focused test (bad in commits)
- `fdescribe` - Focused describe
- `fit(` - Focused it

#### TODO Comments
- `# TODO` - Python TODO
- `# FIXME` - Python FIXME
- `// TODO` - JS/TS TODO
- `// FIXME` - JS/TS FIXME

#### Commented Tests
- `# def test_` - Commented Python test
- `# it(` - Commented JS test
- `// it(` - Commented JS test
- `// test(` - Commented test

#### Stub Tests (Python)
- Test functions with no assertions
- Test functions with only `pass`
- Test functions with placeholder assertions

**Algorithm**:
1. Find all test files (`.py`, `.js`, `.ts`, `.jsx`, `.tsx`)
2. Read file content
3. Apply regex patterns for each category
4. For Python: Parse test functions and check for assertions
5. Record violations with file, line, category, content
6. Generate JSON report

**Output Format**:
```json
{
  "success": false,
  "message": "❌ TEST DEBT DETECTED: 5 violations found",
  "timestamp": "2025-12-16T06:30:00Z",
  "test_directory": "tests/",
  "files_scanned": 12,
  "violations_count": 5,
  "violations": [
    {
      "file": "tests/module/test_feature.py",
      "line": 42,
      "category": "skip_markers",
      "pattern": "@pytest\\.mark\\.skip",
      "content": "@pytest.mark.skip('TODO: fix this')"
    }
  ],
  "constitutional_authority": "Zero Test Debt Constitutional Rule",
  "enforcement_level": "BLOCKING"
}
```

**Exit Codes**:
- `0`: Zero debt (success)
- `1`: Debt detected (failure)
- `2`: Scan error

### B. QA Green Validation (`validate-qa-green.py`)

**Purpose**: Validate 100% pass requirement

**Validation Steps**:
1. Detect test framework (pytest or jest)
2. Run test suite with appropriate command
3. Parse results (total, passed, failed, skipped, errors, warnings)
4. Check violations against GSR requirements
5. Generate JSON report

**Test Framework Support**:

#### Pytest
```bash
python -m pytest tests/ -v --tb=short --color=no -W error
```
- Parse output for test counts
- Warnings treated as errors (`-W error`)
- Capture exit code

#### Jest
```bash
jest --json --testPathPattern tests/
```
- Parse JSON output
- Extract test counts
- Capture exit code

**Violation Checks**:
1. **Failed Tests**: `test_result['failed'] > 0` → CRITICAL violation
2. **Test Errors**: `test_result['errors'] > 0` → CRITICAL violation
3. **Skipped Tests**: `test_result['skipped'] > 0` → CRITICAL violation (Zero Test Debt)
4. **Warnings**: `test_result['warnings'] > 0` → HIGH violation
5. **Exit Code**: `test_result['exit_code'] != 0` → CRITICAL violation
6. **Partial Pass**: `0 < pass_rate < 100` → CRITICAL violation (no 99%)

**Output Format**:
```json
{
  "success": false,
  "message": "❌ QA NOT GREEN: 3 violations detected",
  "timestamp": "2025-12-16T06:30:00Z",
  "test_directory": "tests/",
  "constitutional_authority": "Governance Supremacy Rule (GSR)",
  "enforcement_level": "BLOCKING",
  "test_result": {
    "total": 10,
    "passed": 8,
    "failed": 2,
    "skipped": 0,
    "errors": 0,
    "warnings": 0,
    "exit_code": 1,
    "output": "..."
  },
  "violations": [
    {
      "rule": "GSR Pillar 1: 100% Pass Required",
      "violation": "2 test(s) failed",
      "severity": "CRITICAL",
      "blocking": true,
      "message": "❌ 2 tests FAILED. GSR requires 100% pass. No exceptions."
    }
  ],
  "violations_count": 1,
  "blocking_reason": "GOVERNANCE_SUPREMACY_RULE_VIOLATION"
}
```

**Exit Codes**:
- `0`: QA green (100% pass)
- `1`: QA not green (violations)
- `2`: Validation error

---

## IV. CI/CD Enforcement Workflow

### Workflow File: `.github/workflows/build-to-green-enforcement.yml`

**Triggers**:
- `pull_request`: opened, synchronize, reopened
- `push`: main branch

**Permissions** (FIX for #73 403 error):
```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
```

**Jobs**: 5 sequential stages + 2 conditional reports

### Stage 1: test-debt-detection

**Purpose**: Detect and block test debt

**Steps**:
1. Checkout code
2. Set up Python 3.12
3. Install dependencies (pytest, pytest-asyncio, pytest-cov, pytest-mock)
4. Run `detect-test-debt.py --test-dir tests --json > test-debt-report.json`
5. Check exit code → fail if non-zero
6. Upload `test-debt-report.json` artifact

**On Failure**: Build BLOCKED, workflow stops

### Stage 2: qa-green-validation

**Purpose**: Validate 100% pass requirement

**Dependencies**: `needs: test-debt-detection`

**Steps**:
1. Checkout code
2. Set up Python 3.12
3. Install dependencies
4. Run `validate-qa-green.py --test-dir tests --json > qa-green-report.json`
5. Check exit code → fail if non-zero
6. Upload `qa-green-report.json` artifact

**On Failure**: Build BLOCKED, workflow stops

### Stage 3: suppression-check

**Purpose**: Detect suppressed failures

**Dependencies**: `needs: qa-green-validation`

**Steps**:
1. Checkout code
2. Set up Python 3.12
3. Install dependencies
4. Run `pytest tests/ -v --strict-markers --strict-config -W error`
5. Check exit code → fail if non-zero
6. Upload `suppression-check.log` artifact

**On Failure**: Build BLOCKED, workflow stops

### Stage 4: constitutional-compliance

**Purpose**: Verify constitutional file integrity

**Dependencies**: `needs: suppression-check`

**Steps**:
1. Checkout code
2. Check if constitutional files modified (git diff)
3. Warn if modifications detected
4. Create compliance report JSON
5. Upload `constitutional-compliance.json` artifact

**On Warning**: Continue, but flags for Owner review

### Stage 5: enforcement-report (success path)

**Purpose**: Report success and approve build

**Dependencies**: `needs: [test-debt-detection, qa-green-validation, suppression-check, constitutional-compliance]`

**Condition**: `if: always()` (runs even if others skipped)

**Steps**:
1. Download all artifacts
2. Generate enforcement report markdown
3. Post success comment to PR (if PR context)

**Comment Content**:
```
✅ **Build-to-Green Enforcement: PASSED**

All constitutional requirements met:
- Zero test debt
- 100% pass rate
- No suppressed failures
- Full compliance

**Build approved for merge.**
```

### Stage 6: enforcement-failure (failure path)

**Purpose**: Report failure and provide remediation

**Dependencies**: `needs: [test-debt-detection, qa-green-validation, suppression-check, constitutional-compliance]`

**Condition**: `if: failure()`

**Steps**:
1. Download all artifacts (continue-on-error)
2. Generate failure report markdown
3. Include violation details from artifacts
4. Post failure comment to PR (if PR context)

**Comment Content**:
```
❌ **Build-to-Green Enforcement: FAILED**

**Build BLOCKED by Governance Supremacy Rule**

Violations detected. Please:
1. Check the workflow logs for details
2. Fix all failing tests
3. Remove any test debt (skip, todo, only)
4. Ensure 100% pass rate
5. Re-run the workflow

Download artifacts for detailed reports.
```

**On Failure**: Merge blocked until fixed

---

## V. Local Enforcement (Pre-Commit Hook)

### Hook File: `.githooks/pre-commit`

**Purpose**: Prevent commits with test debt or unauthorized constitutional changes

**Installation**:
```bash
git config core.hooksPath .githooks
```

**Checks**:

#### Check 1: Test Debt Detection
1. Run `detect-test-debt.py --test-dir tests`
2. If exit code != 0:
   - Print violation details
   - Print constitutional authority
   - Block commit
3. If exit code == 0:
   - Print success
   - Continue

#### Check 2: Constitutional File Protection
1. Get list of protected files:
   ```
   BUILD_PHILOSOPHY.md
   foreman/constitution/
   foreman/governance/*.md
   foreman/builder-specs/build-to-green-rule.md
   .github/workflows/
   ```
2. Check staged files: `git diff --cached --name-only`
3. If protected file modified:
   - Warn about constitutional protection
   - Prompt: "Do you have authorization? (yes/no)"
   - If "no" → Block commit
   - If "yes" → Allow with warning

**Output**: Colored terminal output with clear pass/fail

**Exit Codes**:
- `0`: Checks passed, commit allowed
- `1`: Checks failed, commit blocked

---

## VI. Audit and Compliance

### Artifacts Generated

All workflow runs generate artifacts for audit:

1. **test-debt-report.json**
   - Test debt scan results
   - Violations list
   - Files scanned

2. **qa-green-report.json**
   - Test execution results
   - Pass/fail counts
   - Violations list

3. **suppression-check.log**
   - Strict test execution log
   - Suppression detection results

4. **constitutional-compliance.json**
   - Protected file check results
   - Modification warnings

**Retention**: GitHub default (90 days), configurable

### Audit Trail

Every enforcement action creates an audit trail:
- Timestamp (ISO 8601)
- Constitutional authority cited
- Violations detected
- Actions taken
- Blocking status

### Compliance Reporting

Reports generated include:
- Enforcement success/failure
- Violation details
- Remediation steps
- Trend analysis (future)

---

## VII. Error Handling

### Script Errors

If scripts fail to execute:
- Exit code 2 returned
- Error logged to stderr
- CI/CD marks as error (not success)
- Remediation required before retry

### Workflow Errors

If workflow encounters errors:
- Job fails
- PR comment posted (if possible)
- Artifacts uploaded (if available)
- Manual intervention may be required

### Pre-Commit Errors

If hook encounters errors:
- Warning printed
- Commit may be allowed (fail-open for usability)
- CI/CD will catch issues

---

## VIII. Owner Override

### When Allowed

Owner (Johan) may temporarily override for:
- Emergency production fixes
- Critical security patches
- Time-critical situations

### Override Process

1. Owner explicitly states override
2. Override documented in commit message
3. Override logged in evidence trail
4. Follow-up issue created for cleanup
5. Cleanup must occur within 48 hours

### Post-Override

- Rules return to full enforcement
- Technical debt created must be resolved
- Standard governance resumes

---

## IX. Version and Authority

**Version**: 1.0.0  
**Status**: Active and Enforced  
**Authority**: Constitutional (Build Philosophy + GSR + Zero Test Debt Rule)  
**Precedence**: Blocking enforcement at all levels  
**Last Updated**: 2025-12-16  
**Owner**: Johan (MaturionISMS)  
**Enforcer**: Maturion Foreman + CI/CD

**Changelog**:
- 1.0.0 (2025-12-16): Initial Build-to-Green Enforcement Specification

---

## X. Summary

Build-to-Green Enforcement provides **3-layer blocking enforcement** of quality standards:

1. **Local (Pre-Commit)**
   - Prevents test debt commits
   - Warns on constitutional changes
   - Fail-fast at development time

2. **CI/CD (Automated)**
   - 5 sequential validation stages
   - Hard-fails on violations
   - No bypass mechanism
   - Automatic PR comments

3. **Oversight (Foreman QA-of-QA)**
   - Validates enforcement compliance
   - Audit trail maintenance
   - Governance oversight

**No exceptions. No bypasses. 100% or blocked.**

---

*END OF BUILD-TO-GREEN ENFORCEMENT SPECIFICATION*
