# Git Hooks for Build-to-Green Enforcement

This directory contains Git hooks that enforce Build-to-Green semantics locally before code is committed.

## Constitutional Authority

These hooks implement:
- **Zero Test Debt Constitutional Rule**
- **Governance Supremacy Rule**
- **Build-to-Green Rule**

## Available Hooks

### pre-commit

Runs before every `git commit` to check for:

1. **Test Debt Detection**
   - Scans for test skip and focus patterns
   - Checks for TODO/FIXME markers in test files
   - Detects commented out tests
   - Identifies stub tests

2. **Staged File Validation**
   - Validates test files being committed
   - Prevents committing test debt

3. **Protected File Monitoring**
   - Warns when constitutional files are modified
   - Reminds about CS2 approval requirement

## Installation

### Automatic Installation

```bash
# From repository root
cp .githooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### Configure Git to Use .githooks Directory

```bash
# Tell git to use .githooks as hooks directory
git config core.hooksPath .githooks
```

This will automatically use all hooks in `.githooks/` without manual copying.

## Usage

Once installed, hooks run automatically:

```bash
# When you commit, hooks run automatically
git commit -m "Your commit message"

# Output will show enforcement checks:
🔍 Build-to-Green Enforcement: Pre-commit checks...

1. Checking for test debt...
✅ No test debt detected

2. Checking staged test files for violations...
✅ No violations in staged test files

3. Checking for protected file modifications...

✅ All pre-commit checks passed
```

## Bypass (NOT RECOMMENDED)

Bypassing hooks is **strongly discouraged** as it violates constitutional rules.

If absolutely necessary for emergency fixes:

```bash
git commit --no-verify -m "Emergency fix"
```

**WARNING**: Bypassing hooks may result in:
- CI/CD failures
- Merge blocks
- Governance violations
- Audit trail issues

**Only use in genuine emergencies with Owner approval.**

## Troubleshooting

### Hook not running

```bash
# Check hook is installed
ls -la .git/hooks/pre-commit

# Check hook is executable
chmod +x .git/hooks/pre-commit

# Verify git hooks path
git config core.hooksPath
```

### Python not found

Hooks require Python 3. Install Python 3 or update shebang in hook file.

### False positives

If hook incorrectly blocks commit:
1. Review the violation reported
2. Verify it's actually a false positive
3. Report issue if hook logic needs adjustment
4. DO NOT bypass without investigation

## Testing Hooks

Test hooks without committing:

```bash
# Run test debt detection manually
python3 foreman/scripts/detect-test-debt.py --test-dir tests

# Dry-run the hook
bash .githooks/pre-commit
```

## Maintenance

Hooks are maintained in `.githooks/` directory and version controlled.

Updates to enforcement logic should:
1. Update hook scripts in `.githooks/`
2. Update this README
3. Test thoroughly
4. Document changes

## Support

For issues or questions:
- See: `foreman/governance/build-to-green-enforcement-spec.md`
- See: `foreman/governance/zero-test-debt-constitutional-rule.md`
- Contact: Repository maintainers
