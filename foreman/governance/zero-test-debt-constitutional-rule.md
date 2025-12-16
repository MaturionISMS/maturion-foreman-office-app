# Zero Test Debt Constitutional Rule

**Version**: 1.0.0  
**Status**: Constitutional Authority  
**Authority**: Build Philosophy + Governance Supremacy Rule  
**Last Updated**: 2025-12-15

---

## I. Constitutional Authority

This rule is a **constitutional requirement** of the Maturion Build Philosophy.

**No test debt is permitted. Ever.**

This rule is absolute, non-negotiable, and enforceable at all levels.

---

## II. Definition of Test Debt

### What is Test Debt?

**Test debt** is any form of incomplete, skipped, or deferred testing that represents work not done.

### All Forms of Test Debt (FORBIDDEN)

#### 1. Skipped Tests
```javascript
// ❌ FORBIDDEN
it.skip('should validate user input', () => { ... })
describe.skip('User authentication', () => { ... })
test.todo('implement password validation')
fit('should save user', () => { ... }) // .only() left in code
```

#### 2. Commented Out Tests
```javascript
// ❌ FORBIDDEN
// it('should handle errors', () => {
//   expect(result).toBe(error)
// })
```

#### 3. Incomplete Tests (Stubs with No Assertions)
```javascript
// ❌ FORBIDDEN
it('should process payment', () => {
  // TODO: implement this test
})

it('should validate email', () => {
  const user = createUser()
  // Missing: actual validation and assertions
})

it('should handle edge case', () => {
  expect(true).toBe(true) // Meaningless placeholder
})
```

#### 4. Tests Marked TODO or FIXME
```javascript
// ❌ FORBIDDEN
it('should encrypt data', () => {
  // FIXME: This test doesn't actually test encryption
  expect(encrypt('test')).toBeDefined()
})

// TODO: Add test for concurrent access
```

#### 5. Incomplete Test Infrastructure
```javascript
// ❌ FORBIDDEN - Stub helper functions
export const mockUserService = {
  getUser: () => { throw new Error('Not implemented') }
}

// ❌ FORBIDDEN - Broken mocks
jest.mock('./api', () => ({
  // TODO: implement proper mocks
}))
```

#### 6. Hidden Test Debt

```javascript
// ❌ FORBIDDEN - Suppressed errors
it('should validate', () => {
  try {
    validate(input)
  } catch (e) {
    // Silently swallowing errors
  }
})

// ❌ FORBIDDEN - Excluded tests
// tests/critical-feature.test.ts listed in .gitignore
// tests/ directory in jest.config exclude list
```

```bash
# ❌ FORBIDDEN - Command-line suppression (hiding failures)
pytest tests/ || true              # Exit code suppression
npm test 2>/dev/null               # Stderr suppression
./run-tests.sh 2>&1 | true         # Combined suppression
jest --passWithNoTests             # Pass without running tests
```

#### 7. Failing Tests Carried Forward
```bash
# ❌ FORBIDDEN
Tests: 295 passed, 8 failed, 303 total
# "We'll fix the 8 failures later"
```

---

## III. The Zero Test Debt Enforcement Protocol

### Detection Phase

**When Test Debt is Detected → IMMEDIATE ACTION REQUIRED**

```
TEST DEBT DETECTED
    ↓
STOP EXECUTION IMMEDIATELY
    ↓
FIX ALL DEBT
    ↓
RE-RUN QA
    ↓
VERIFY ZERO DEBT
    ↓
CONTINUE (only if zero debt confirmed)
```

### Fixing Phase

**Required Actions**:

1. **Identify All Test Debt**
   - Scan for `.skip()`, `.todo()`, `.only()`
   - Search for commented out tests
   - Find stub tests with no assertions
   - Locate TODO/FIXME comments in tests
   - Check for incomplete mocks and helpers
   - Verify all tests in suite are running

2. **Fix Each Instance**
   - Remove `.skip()` → Implement the test properly
   - Remove `.todo()` → Write the complete test
   - Remove `.only()` → Run all tests
   - Uncomment tests → Fix and enable them
   - Complete stub tests → Add proper assertions
   - Remove TODO/FIXME → Implement what's needed
   - Fix broken infrastructure → Complete mocks and helpers

3. **Verify Zero Debt**
   - Run full test suite
   - Verify 100% pass (no skips, no failures)
   - Verify no excluded tests
   - Verify all infrastructure complete
   - Verify no suppressed errors

4. **Document Resolution**
   - Log what debt was found
   - Log how it was fixed
   - Log verification results
   - Update evidence trail

### Verification Phase

**Before Continuing, Verify**:
- ✅ Zero skipped tests
- ✅ Zero .todo() tests
- ✅ Zero .only() tests
- ✅ Zero commented out tests
- ✅ Zero stub tests
- ✅ Zero TODO/FIXME in tests
- ✅ All test infrastructure complete
- ✅ All tests running and passing
- ✅ No suppressed errors
- ✅ No excluded tests

**If ANY item not checked → Test debt still exists → Continue fixing**

---

## IV. Prevention Strategies

### Pre-Commit Hooks

**Install hooks to prevent test debt from entering codebase**:

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Check for test debt patterns
if grep -r "\.skip\|\.todo\|\.only" tests/; then
  echo "ERROR: Test debt detected (.skip, .todo, .only)"
  exit 1
fi

if grep -r "TODO\|FIXME" tests/*.test.*; then
  echo "ERROR: TODO/FIXME found in tests"
  exit 1
fi

echo "✅ No test debt detected"
```

### CI/CD Validation

**Automated checks in CI/CD pipeline**:

```yaml
# .github/workflows/build-to-green-enforcement.yml
- name: Detect Test Debt
  run: |
    # Use comprehensive detection script that checks:
    # - .skip, .todo, .only patterns
    # - TODO/FIXME markers in tests
    # - Stub tests with no assertions
    # - Command-line suppression (|| true, 2>/dev/null, etc.)
    # - Suppression in CI/workflow files
    python foreman/scripts/detect-test-debt.py --test-dir tests
    
    # Script exits with code 1 if any debt detected
    # Provides actionable error messages with:
    # - File path and line number
    # - Matched pattern
    # - Issue description
    # - Remedy (including Enhancement Parking Lot reference)
```

**See**: `.github/workflows/build-to-green-enforcement.yml` for full implementation

### Foreman Pre-Build Validation

**Before accepting any build task**:

```
1. Scan QA suite for test debt
2. If test debt found → REJECT task
3. Request Foreman to fix QA suite first
4. Wait for zero test debt confirmation
5. THEN accept build task
```

### Builder Mid-Build Monitoring

**During build execution**:

```
1. After each code change → Run QA
2. Scan test results for debt patterns
3. If test debt introduced → STOP
4. Fix debt immediately
5. Re-run QA
6. Verify zero debt
7. Continue
```

---

## V. Common Objections and Responses

### Objection 1: "The test is flaky, we need to skip it temporarily"

**Response**: ❌ REJECTED

**Correct Action**:
1. Do NOT skip the test
2. Fix the flakiness
3. Make the test reliable
4. THEN continue

**Flaky tests are a quality problem, not a reason to skip.**

### Objection 2: "This test is hard to write, let's add TODO and finish later"

**Response**: ❌ REJECTED

**Correct Action**:
1. Do NOT add TODO
2. If test is hard → Architecture may be wrong
3. Escalate to Foreman
4. Get architecture clarification
5. Write complete test
6. THEN continue

**"Hard to test" means "needs architectural attention", not "defer testing".**

### Objection 3: "We'll fix these 5 failing tests in the next sprint"

**Response**: ❌ REJECTED

**Correct Action**:
1. Do NOT defer failures
2. Fix all 5 tests NOW
3. Verify 100% pass
4. THEN proceed to next work

**There is no "next sprint" for failures. Fix now.**

### Objection 4: "The feature works fine, the test is just incomplete"

**Response**: ❌ REJECTED

**Correct Action**:
1. Complete the test
2. If test reveals bugs → Fix bugs
3. If test is wrong → Fix test
4. Achieve 100% pass
5. THEN claim feature works

**"Feature works" is proven by passing tests, not by claims.**

### Objection 5: "This test doesn't matter, it's just a minor edge case"

**Response**: ❌ REJECTED

**Correct Action**:
1. If test doesn't matter → Remove it entirely
2. If test matters → Complete it properly
3. No middle ground

**Tests are either important (complete them) or unimportant (remove them). No in-between.**

---

## VI. Test Debt vs. Test Coverage

### These are DIFFERENT Concepts

**Test Coverage**: Percentage of code exercised by tests
- ✅ Can be 80%, 90%, 100% (depends on policy)
- ✅ Managed by coverage requirements
- ✅ Can be incremental

**Test Debt**: Incomplete or deferred tests
- ❌ Must ALWAYS be 0%
- ❌ No partial allowance
- ❌ Not incremental, must be zero

### Example

**Acceptable**:
```javascript
// Coverage: 85% (target: 80%)
// Test Debt: 0%
// All tests complete and passing
// Some code not tested yet (OK if within policy)
```

**NOT Acceptable**:
```javascript
// Coverage: 95% (above target!)
// Test Debt: 5 skipped tests
// ❌ BLOCKED - Test debt exists
```

**Priority**: Zero test debt > High coverage

Would you rather have:
- A) 100% coverage with 10 skipped tests ❌
- B) 80% coverage with 0 test debt ✅

**Answer: B**

---

## VII. Escalation for Test Debt

### When Builder Detects Test Debt in QA Suite

**Before Build Starts**:

```json
{
  "success": false,
  "error": "QASuiteViolation",
  "message": "Test debt detected in QA suite",
  "details": {
    "test_debt_found": [
      "5 skipped tests (.skip)",
      "3 TODO markers in test files",
      "2 incomplete test stubs"
    ],
    "action_required": "Foreman must fix QA suite before build can start",
    "philosophy_reference": "/foreman/governance/zero-test-debt-constitutional-rule.md"
  },
  "timestamp": "2025-12-15T16:00:00Z"
}
```

**Builder Action**: REJECT build task, escalate to Foreman

### When Builder Accidentally Introduces Test Debt

**During Build**:

```
1. Builder runs tests
2. Builder sees: "1 test skipped"
3. Builder realizes: "I introduced test debt"
4. Builder STOPS immediately
5. Builder fixes the debt
6. Builder re-runs tests
7. Builder verifies zero debt
8. Builder continues
```

**No escalation needed if caught and fixed immediately.**

---

## VIII. Metrics and Reporting

### Track These Metrics

- **Test Debt Incidents**: Number of times test debt detected
- **Test Debt Type**: Distribution of debt types (skip, todo, stub, etc.)
- **Resolution Time**: How long to fix test debt when detected
- **Repeat Offenders**: Patterns of test debt introduction
- **Prevention Success**: % of builds with zero test debt

### Report In

- Build completion reports
- QA validation reports
- Governance dashboards
- Module readiness reports

### Success Criteria

- ✅ 100% of builds have zero test debt
- ✅ Test debt detection time < 1 minute
- ✅ Test debt resolution time < 1 hour (typically)
- ✅ Zero repeat test debt introductions

---

## IX. Integration with Build Philosophy

Zero Test Debt is a direct implementation of:
- **Principle 1**: One-Time Build Correctness (tests must be complete before building)
- **Principle 2**: Zero Regression (cannot detect regressions with incomplete tests)
- **Principle 5**: Zero Ambiguity (skipped tests are ambiguous)

**Hierarchy**:
```
BUILD_PHILOSOPHY.md
    ↓
governance-supremacy-rule.md (GSR Pillar 2)
    ↓
zero-test-debt-constitutional-rule.md (This Document)
```

---

## X. Owner Override

### Johan's Override Authority

Johan may **temporarily override** this rule for:
- Emergency production fixes where test completion is blocked by external factors
- Critical security patches requiring immediate deployment

**Override Characteristics**:
- Temporary (specific instance only)
- Explicit (clearly stated)
- Documented (logged in evidence trail)
- **Followed by mandatory cleanup**: Test debt created under override MUST be resolved in immediate follow-up

**Post-Override**:
- Create tracking issue for test debt resolution
- Assign highest priority
- Resolve within 48 hours (maximum)
- Verify zero debt restoration

---

## XI. Version and Authority

**Version**: 1.0.0  
**Status**: Active and Enforced  
**Authority**: Constitutional Authority (Build Philosophy + GSR Implementation)  
**Precedence**: Constitutional Level (Enforceable by Foreman)  
**Last Updated**: 2025-12-15  
**Owner**: Johan (MaturionISMS)  
**Enforcer**: Maturion Foreman

**Changelog**:
- 1.0.0 (2025-12-15): Initial Zero Test Debt Constitutional Rule

---

## XII. Summary: The Commitment

Zero Test Debt Rule commits to:

1. ✅ **Zero Skipped Tests** - Every test runs
2. ✅ **Zero Incomplete Tests** - Every test is complete
3. ✅ **Zero Deferred Tests** - No "later" allowed
4. ✅ **Zero Test Infrastructure Gaps** - Mocks and helpers are complete
5. ✅ **Zero Hidden Debt** - No suppressed errors or excluded tests

**Test debt is not negotiable.**  
**Tests are either complete or they don't exist.**  
**No middle ground.**

---

*END OF ZERO TEST DEBT CONSTITUTIONAL RULE*
