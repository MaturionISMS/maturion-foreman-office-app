# Branch Protection Enforcement - Tier-0 Governance Invariant

## Overview

Branch protection enforcement is now a **Tier-0 Governance Invariant**. This means that the presence and configuration of required CI checks in GitHub branch protection is a constitutional requirement that MUST be verified before FM runtime execution begins.

## Constitutional Authority

- **governance/TIER_0_CANON_MANIFEST.json** - `branch_protection_enforcement` section
- **BUILD_PHILOSOPHY.md** - Zero Regression Guarantee
- **Issue**: Enforce Branch Protection as Tier-0 Governance Invariant

## Required CI Checks

The following CI checks are **non-negotiable** and MUST be configured in GitHub branch protection for the main branch:

### BP-001: Tier-0 Governance Activation Gate
- **Workflow**: `.github/workflows/tier0-activation-gate.yml`
- **Job**: `validate-tier0-activation`
- **Purpose**: Validates Tier-0 canonical governance runtime activation
- **Classification**: CATASTROPHIC if missing

### BP-002: Governance Coupling Gate
- **Workflow**: `.github/workflows/governance-coupling-gate.yml`
- **Job**: `validate-governance-coupling`
- **Purpose**: Enforces coupling rule - Tier-0 governance changes MUST be coupled with enforcement updates
- **Classification**: CATASTROPHIC if missing

### BP-003: Code Review Closure Gate
- **Enforcement**: Contractual (via `.agent` file)
- **Purpose**: Ensures code review closure ratchet is enforced at end of session
- **Classification**: CATASTROPHIC if missing
- **Note**: This is enforced contractually, not as a separate CI workflow

## Enforcement Mechanism

### 1. Tier-0 Manifest Declaration

The `branch_protection_enforcement` section in `governance/TIER_0_CANON_MANIFEST.json` defines:
- Required CI checks (with IDs, names, workflow files)
- Verification requirements
- Failure handling semantics (STOP + ESCALATE)
- Ratchet semantics (regression impossible without governance violation)

### 2. Validation Scripts

#### `scripts/validate_branch_protection_enforcement.py`
- Validates that all required checks are configured in branch protection
- Uses GitHub CLI to query branch protection settings
- Produces detailed diagnostic output on failure
- Exit code 0 = success, 1 = failure

#### `scripts/validate_tier0_activation.py`
- Updated to include branch protection enforcement validation
- Checks that the `branch_protection_enforcement` section exists in manifest
- Validates required fields and failure handlers

### 3. FM Runtime Validation

#### `foreman/runtime/tier0_validator.py`
- New module for Tier-0 invariant validation at runtime initialization
- Calls `validate_branch_protection_enforcement.py` on startup
- **STOPS execution** if validation fails
- **ESCALATES** to Johan Ras with diagnostic output

## Failure Semantics

### When Required Checks Are Missing

**Action**: STOP  
**Escalation**: MANDATORY  
**Target**: Johan Ras  
**Message**: "CATASTROPHIC: Required CI checks not configured in branch protection"

**What Happens:**
1. Branch protection enforcement validator detects missing checks
2. Validator produces diagnostic output identifying which checks are missing
3. FM runtime initialization validation fails
4. Runtime STOPS before any execution begins
5. Escalation output includes clear diagnostic and remediation steps

### When Verification Cannot Be Performed

**Action**: STOP  
**Escalation**: MANDATORY  
**Target**: Johan Ras  
**Message**: "CATASTROPHIC: Cannot verify branch protection status"

**What Happens:**
1. GitHub CLI or API is unavailable
2. Validator cannot authoritatively verify branch protection
3. FM runtime treats this as a failure (fail-safe)
4. Runtime STOPS and escalates

## Ratchet Semantics

**"Required checks are non-negotiable. Absence is a system failure."**

Once required checks are configured:
- They MUST remain configured
- Removing them violates governance
- Regression is impossible without governance violation
- Any attempt to remove checks will fail Tier-0 validation

## Usage

### Manual Validation

```bash
# Validate branch protection enforcement
python scripts/validate_branch_protection_enforcement.py \
  --repo MaturionISMS/maturion-foreman-office-app \
  --branch main

# Validate Tier-0 activation (includes branch protection)
python scripts/validate_tier0_activation.py

# Test FM runtime initialization
python foreman/runtime/tier0_validator.py \
  --repo MaturionISMS/maturion-foreman-office-app \
  --branch main
```

### Runtime Integration

```python
from foreman.runtime.tier0_validator import initialize_fm_runtime

# At FM runtime startup
if not initialize_fm_runtime():
    # STOP - Tier-0 validation failed
    # Escalation output already produced
    sys.exit(1)

# Safe to proceed with runtime execution
```

## CI Integration

The `tier0-activation-gate.yml` workflow automatically validates:
1. All 13 Tier-0 constitutional documents
2. Branch protection enforcement declaration in manifest
3. Required checks are properly defined

**Note**: The workflow does NOT query GitHub branch protection directly (that's done at runtime). It validates that the governance definition is correct.

## Diagnostic Output

When validation fails, the validator produces:

1. **Category**: Type of problem (e.g., MISSING_REQUIRED_CHECK_BP-001)
2. **Problem**: Clear description of what's wrong
3. **Solution**: Actionable remediation steps

Example:
```
Category: MISSING_REQUIRED_CHECK_BP-001
Problem:  Required CI check 'Tier-0 Governance Activation Gate' (job: validate-tier0-activation) 
          is not configured in branch protection
Solution: Add 'validate-tier0-activation' to required status checks in GitHub branch protection settings
```

## Remediation

If branch protection enforcement validation fails:

1. **Identify missing checks** - Review validator output
2. **Go to GitHub repository settings** - Settings → Branches → Branch protection rules
3. **Edit protection rule for 'main' branch**
4. **Add missing checks** to "Require status checks to pass before merging"
5. **Save changes**
6. **Re-run validation** to confirm

## Testing

To test the implementation:

```bash
# Run all governance tests
pytest tests/ -k governance

# Run Tier-0 activation test
python scripts/validate_tier0_activation.py

# Test with GitHub CLI (requires GH_TOKEN)
export GH_TOKEN="your_token_here"
python scripts/validate_branch_protection_enforcement.py
```

## Version History

- **v1.0.0** (2026-01-01) - Initial implementation
  - Added branch_protection_enforcement to TIER_0_CANON_MANIFEST.json
  - Created validate_branch_protection_enforcement.py
  - Created foreman/runtime/tier0_validator.py
  - Updated validate_tier0_activation.py
  - Documented enforcement mechanism

## References

- [TIER_0_CANON_MANIFEST.json](../governance/TIER_0_CANON_MANIFEST.json)
- [validate_branch_protection_enforcement.py](../scripts/validate_branch_protection_enforcement.py)
- [tier0_validator.py](../foreman/runtime/tier0_validator.py)
- [BUILD_PHILOSOPHY.md](../BUILD_PHILOSOPHY.md)
