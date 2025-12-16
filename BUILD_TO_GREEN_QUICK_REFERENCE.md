# Build-to-Green Quick Reference

**Status**: Active Enforcement  
**Authority**: Build Philosophy + Governance Supremacy Rule  
**Version**: 1.0.0

---

## What is Build-to-Green?

Build-to-Green is the **constitutional enforcement** of quality standards in the Maturion ISMS ecosystem.

**Core Principle**: 100% or blocked. No partial passes. No test debt. No exceptions.

---

## Quick Rules

### 🚫 What's FORBIDDEN

1. **Test Debt** (Zero tolerance)
   - ❌ `.skip()`, `.todo()`, `.only()` markers
   - ❌ Commented out tests
   - ❌ Stub tests with no assertions
   - ❌ `TODO`/`FIXME` in test files
   - ❌ Skipped tests

2. **Partial Passes** (100% required)
   - ❌ 99% pass rate = FAILURE
   - ❌ 301/303 tests = FAILURE
   - ❌ ANY test failure = BLOCKED
   - ❌ ANY warnings = BLOCKED

3. **Non-Zero Exit Codes**
   - ❌ Exit code must be 0
   - ❌ Build must succeed
   - ❌ Lint must pass

---

## How It Works

### 3 Enforcement Layers

```
┌─────────────────────────────────────┐
│  1. Pre-Commit Hook (Local)         │
│     - Detects test debt              │
│     - Warns on constitutional mods   │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  2. CI/CD Workflow (Automated)       │
│     - 5 sequential stages            │
│     - Hard-fails on violations       │
│     - Posts PR comments              │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  3. Foreman QA-of-QA (Oversight)     │
│     - Validates enforcement          │
│     - Audit trail                    │
└─────────────────────────────────────┘
```

### CI/CD Workflow Stages

1. **Test Debt Detection**
   - Scans for `.skip()`, `.todo()`, `.only()`
   - Finds commented tests
   - Detects stub tests
   - **Blocks on detection**

2. **100% Pass Validation**
   - Runs full test suite
   - Validates 100% pass rate
   - Checks for warnings
   - **Blocks on any failure**

3. **Suppression Check**
   - Runs with strict settings
   - Detects hidden failures
   - **Blocks on suppression**

4. **Constitutional Compliance**
   - Verifies protected file integrity
   - Checks governance adherence
   - **Warns on modifications**

5. **Report & Comment**
   - Generates enforcement report
   - Posts to PR
   - Creates artifacts

---

## For Developers

### Local Setup

```bash
# Install pre-commit hook
git config core.hooksPath .githooks

# Verify installation
ls -la .githooks/pre-commit
```

### Before Committing

```bash
# Check for test debt
python3 foreman/scripts/detect-test-debt.py --test-dir tests

# Validate tests pass
python3 foreman/scripts/validate-qa-green.py --test-dir tests

# Both must exit 0
```

### If Tests Fail

```bash
# ❌ DON'T: Skip the test
# it.skip('broken test', () => { ... })

# ✅ DO: Fix the test
# Fix the code or the test until it passes
```

### If Test is Hard to Write

```bash
# ❌ DON'T: Leave TODO
# it.todo('write this test later')

# ✅ DO: Escalate
# If test is hard → architecture may be wrong
# Escalate to Foreman for review
```

---

## For Agents

### Accepting Build Tasks

**Only accept**: "Build to Green" format

```markdown
BUILD TO GREEN

Architecture Reference: path/to/architecture.md
QA Suite Location: tests/module/
QA Current Status: RED (5 tests failing)
Acceptance Criteria: All tests must pass (100% green)
```

**Reject**: Any other format
- "Build feature X" → REJECTED
- "Implement Y" → REJECTED
- "Fix bug Z" → REJECTED

### Build Process

```
1. Validate instruction format
2. Load architecture
3. Load QA suite (must be RED)
4. Run tests → identify failures
5. Implement minimal code to pass ONE test
6. Re-run full suite
7. Repeat until 100% pass
8. Final validation checklist
9. Report completion
```

### Completion Criteria

```
Final Validation Checklist:
☐ QA Status: 100% passing
☐ Test Failures: 0
☐ Test Errors: 0
☐ Skipped Tests: 0
☐ Test Debt: 0
☐ Build: ✅ succeeds
☐ Lint: ✅ zero errors, zero warnings
☐ Exit Code: 0

IF ALL CHECKED → Report Green
IF ANY UNCHECKED → Continue iteration
```

---

## Common Scenarios

### Scenario 1: Test Fails in CI

**What Happened**: CI detected test failure

**Action**:
1. Check workflow logs
2. Download `qa-green-report.json` artifact
3. Fix failing test(s)
4. Re-run CI
5. Verify 100% pass

### Scenario 2: Test Debt Detected

**What Happened**: `.skip()` or `.todo()` found

**Action**:
1. Find the test debt (check logs)
2. Remove `.skip()` / `.todo()`
3. Complete the test properly
4. Re-run validation
5. Verify zero debt

### Scenario 3: 99% Pass Rate

**What Happened**: 1 test fails, 99 pass

**Response**: ❌ BLOCKED

**Action**:
1. 99% = FAILURE (GSR Pillar 1)
2. Fix the 1 failing test
3. Achieve 100% pass
4. Re-run CI

### Scenario 4: Constitutional File Modified

**What Happened**: Workflow warns about protected file

**Action**:
1. If unauthorized → Revert changes
2. If authorized → Get CS2 approval
3. Require Owner (Johan) review
4. Proceed only with approval

---

## Exit Codes

### Scripts

| Exit Code | Meaning |
|-----------|---------|
| 0 | ✅ Success (green / zero debt) |
| 1 | ❌ Failure (violations detected) |
| 2 | ⚠️  Error (script error) |

### CI/CD

| Status | Meaning |
|--------|---------|
| ✅ Pass | All stages passed, build approved |
| ❌ Fail | Violation detected, build BLOCKED |
| ⚠️  Skip | Dependent stage failed, skipped |

---

## Key Documents

### Constitutional Authority
- `BUILD_PHILOSOPHY.md` - Supreme authority
- `foreman/governance/governance-supremacy-rule.md` - GSR
- `foreman/governance/zero-test-debt-constitutional-rule.md` - Test debt rule
- `foreman/builder-specs/build-to-green-rule.md` - Builder protocol

### Implementation
- `foreman/governance/build-to-green-enforcement-spec.md` - Full spec
- `.github/workflows/build-to-green-enforcement.yml` - Workflow
- `foreman/scripts/detect-test-debt.py` - Debt detection
- `foreman/scripts/validate-qa-green.py` - 100% pass validation
- `.githooks/pre-commit` - Local hook

### Reference
- `ISSUE_B4_IMPLEMENTATION_SUMMARY.md` - Implementation details
- `BUILD_TO_GREEN_QUICK_REFERENCE.md` - This document

---

## FAQ

### Q: Can I merge with 1 failing test?
**A**: ❌ No. 100% pass required. GSR Pillar 1 is absolute.

### Q: Can I skip a flaky test temporarily?
**A**: ❌ No. Fix the flakiness. Tests must be reliable.

### Q: What if the test is wrong, not the code?
**A**: Fix the test. Tests must be correct. Both code and tests must be right.

### Q: Can I leave a TODO and finish later?
**A**: ❌ No. Zero test debt rule. Complete tests now.

### Q: What if Owner (Johan) overrides?
**A**: Temporary override possible for emergencies. Must be documented and followed by cleanup.

### Q: How do I bypass enforcement?
**A**: You don't. That's the point. No bypasses without Owner override.

---

## Support

### If Stuck
1. Check workflow logs
2. Download artifacts
3. Read error messages
4. Check constitutional docs
5. Escalate to Foreman

### If Constitutional Violation
1. Stop immediately
2. Do NOT proceed
3. Escalate to Foreman
4. Wait for resolution

---

## Summary

**Build-to-Green = 100% or Blocked**

✅ Zero test debt  
✅ 100% pass rate  
✅ No warnings  
✅ No exceptions  

**This is the only way.**

---

*END OF QUICK REFERENCE*
