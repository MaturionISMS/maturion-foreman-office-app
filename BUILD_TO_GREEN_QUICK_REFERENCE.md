# Build-to-Green Enforcement Quick Reference

**For Developers and AI Agents**

---

## TL;DR - What You Need to Know

**GREEN MEANS 100% GREEN. NO EXCEPTIONS.**

- ✅ 100% tests passing = GREEN ✅
- ❌ 99% tests passing = RED ❌
- ❌ 301/303 tests passing = RED ❌
- ❌ Any skipped test = RED ❌
- ❌ Any test debt = RED ❌

---

## Quick Checks Before Commit

### 1. Run Test Debt Detection

```bash
python3 foreman/scripts/detect-test-debt.py --test-dir tests
```

**Expected**: `✅ No test debt detected`

If you see violations, fix them before committing.

### 2. Run QA Validation

```bash
python3 foreman/scripts/validate-qa-green.py --test-dir tests
```

**Expected**: `✅ QA STATUS: GREEN`

If not green, fix all failures before committing.

### 3. Install Pre-Commit Hook

```bash
# One-time setup
git config core.hooksPath .githooks
```

Now hooks run automatically on every commit.

---

## What Gets Blocked

### ❌ Skipped Tests

```python
# NOT ALLOWED
@pytest.mark.skip
def test_something():
    pass

# NOT ALLOWED
it.skip('should do something', () => {})

# NOT ALLOWED  
test.todo('implement this test')
```

**Fix**: Remove skip marker, implement test, make it pass.

### ❌ Stub Tests

```python
# NOT ALLOWED
def test_validate_email():
    pass  # Empty stub

# NOT ALLOWED
def test_process_payment():
    # TODO: implement
    pass
```

**Fix**: Implement complete test with assertions.

### ❌ Partial Passes

```
73 tests run: 72 passed, 1 failed
Status: RED ❌ (not 99% green)
```

**Fix**: Fix ALL failures. 100% required.

### ❌ TODO/FIXME in Tests

```python
def test_user_auth():
    # FIXME: This doesn't actually test anything
    assert True
```

**Fix**: Implement proper test, remove TODO/FIXME.

---

## CI/CD Workflow

When you create a PR, CI automatically runs:

1. **Test Debt Detection** - Blocks if debt found
2. **100% Pass Validation** - Blocks if not 100%
3. **Suppressed Failure Check** - Blocks if suppressions found
4. **Constitutional Compliance** - Verifies rules followed

**All checks must pass to merge.**

---

## Common Questions

### Q: I have a flaky test, can I skip it temporarily?

**A: NO.** Fix the flakiness. Skipping is not allowed.

### Q: Can I mark a test as TODO and finish it later?

**A: NO.** Tests must be complete or not exist. No middle ground.

### Q: I have 301/303 tests passing, that's 99.3%, can I merge?

**A: NO.** 100% means 100%. Fix the 2 failures.

### Q: The failing test is minor, can I bypass CI?

**A: NO.** All tests are important. No bypasses.

### Q: What if I'm in an emergency?

**A: Owner (Johan) may grant temporary override.** Must be documented and cleaned up within 48 hours.

---

## For AI Agents

### Builder Agents

**You MUST**:
- Run test debt detection before accepting build task
- Reject task if test debt found
- Achieve 100% pass (not 99%)
- Never skip tests
- Never add TODO markers to tests

**Validation Before Reporting Green**:
```bash
# 1. Check test debt
python3 foreman/scripts/detect-test-debt.py --test-dir tests

# 2. Validate 100% pass
python3 foreman/scripts/validate-qa-green.py --test-dir tests

# 3. Both must return exit code 0
```

### Foreman Agent

**You MUST**:
- Validate QA suite has zero debt before assigning to builders
- Reject build completion if not 100% pass
- Enforce GSR (Governance Supremacy Rule)
- Log all violations to governance memory

---

## Manual Testing

### Test the Scripts

```bash
# Test debt detection
cd /path/to/repo
python3 foreman/scripts/detect-test-debt.py --test-dir tests

# Test QA validation
python3 foreman/scripts/validate-qa-green.py --test-dir tests

# Test with JSON output
python3 foreman/scripts/detect-test-debt.py --test-dir tests --json
python3 foreman/scripts/validate-qa-green.py --test-dir tests --json
```

### Test Pre-Commit Hook

```bash
# Dry-run (doesn't commit)
bash .githooks/pre-commit

# Actual commit (hook runs automatically if installed)
git commit -m "Your message"
```

---

## Remediation Guide

### If Test Debt Detected

```bash
# 1. Run detection to see violations
python3 foreman/scripts/detect-test-debt.py --test-dir tests

# 2. Fix each violation:
#    - Remove .skip(), .todo(), .only()
#    - Implement stub tests
#    - Remove TODO/FIXME markers
#    - Uncomment commented tests and fix them

# 3. Verify zero debt
python3 foreman/scripts/detect-test-debt.py --test-dir tests

# 4. Commit when clean
git commit -m "Fixed test debt"
```

### If Not 100% Pass

```bash
# 1. Run validation to see failures
python3 foreman/scripts/validate-qa-green.py --test-dir tests

# 2. Run tests to see details
python3 -m pytest tests/ -v

# 3. Fix ALL failing tests

# 4. Verify 100% pass
python3 foreman/scripts/validate-qa-green.py --test-dir tests

# 5. Commit when green
git commit -m "All tests passing"
```

---

## Documentation References

**Full Details**:
- `foreman/governance/build-to-green-enforcement-spec.md` - Complete enforcement specification
- `foreman/governance/governance-supremacy-rule.md` - GSR implementation
- `foreman/governance/zero-test-debt-constitutional-rule.md` - Zero test debt rule
- `BUILD_PHILOSOPHY.md` - Supreme constitutional authority

**Quick Start**:
- `.githooks/README.md` - Hook installation instructions
- This document - Quick reference

---

## Constitutional Authority

All enforcement implements:
- **BUILD_PHILOSOPHY.md** (Supreme Authority)
- **Governance Supremacy Rule** (100% Pass Required)
- **Zero Test Debt Constitutional Rule** (No debt allowed)
- **Build-to-Green Rule** (Only build to make tests pass)

**These rules are absolute and non-negotiable.**

---

## Support

**Issues or Questions**:
- Check documentation references above
- Review violation reports from scripts
- Contact repository maintainers
- Escalate to Foreman if architectural clarity needed

**DO NOT**:
- Bypass enforcement without authorization
- Skip tests to "fix" failures
- Merge with known violations
- Hide test debt

---

**GREEN MEANS GREEN. Build-to-Green is constitutional law, not a guideline.**

*Last Updated: 2025-12-16*
