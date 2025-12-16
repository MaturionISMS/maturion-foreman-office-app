# Git Hooks for Build-to-Green Enforcement

This directory contains Git hooks that enforce Build-to-Green requirements locally before commits reach CI/CD.

## Installation

To enable these hooks, run:

```bash
git config core.hooksPath .githooks
```

## Available Hooks

### pre-commit

**Purpose**: Prevents commits with test debt or unauthorized constitutional changes

**What it checks**:
1. **Test Debt Detection**
   - Scans for `.skip()`, `.todo()`, `.only()` markers
   - Finds commented out tests
   - Detects stub tests with no assertions
   - Blocks commit if debt found

2. **Constitutional File Protection**
   - Warns when modifying protected files:
     - `BUILD_PHILOSOPHY.md`
     - `foreman/constitution/`
     - `foreman/governance/*.md`
     - `foreman/builder-specs/build-to-green-rule.md`
     - `.github/workflows/`
   - Prompts for authorization
   - Blocks if unauthorized

**Usage**:
```bash
# Hook runs automatically on every commit
git commit -m "your message"

# If test debt is found, commit is blocked
# If constitutional files are modified, you'll be prompted
```

**Output**:
- ✅ Green text = checks passed
- ❌ Red text = checks failed, commit blocked
- ⚠️  Yellow text = warning (constitutional files)

## Requirements

- Python 3.x installed
- Scripts in `foreman/scripts/` must be present:
  - `detect-test-debt.py`
  - `validate-qa-green.py`

## Bypassing (Not Recommended)

To temporarily bypass hooks (emergency only):

```bash
git commit --no-verify -m "emergency fix"
```

**Warning**: CI/CD will still enforce rules. Use only in emergencies.

## Troubleshooting

### Hook not running

Check if hooks path is configured:
```bash
git config core.hooksPath
# Should output: .githooks
```

If not set:
```bash
git config core.hooksPath .githooks
```

### Permission denied

Make sure hook is executable:
```bash
chmod +x .githooks/pre-commit
```

### Script not found errors

Ensure detection scripts exist:
```bash
ls -l foreman/scripts/detect-test-debt.py
ls -l foreman/scripts/validate-qa-green.py
```

## Constitutional Authority

These hooks enforce:
- **Zero Test Debt Constitutional Rule**
- **Governance Supremacy Rule (GSR) Pillar 4**: Constitutional File Protection

For details, see:
- `foreman/governance/zero-test-debt-constitutional-rule.md`
- `foreman/governance/governance-supremacy-rule.md`
- `foreman/governance/build-to-green-enforcement-spec.md`

---

*Local enforcement layer of the Build-to-Green system*
