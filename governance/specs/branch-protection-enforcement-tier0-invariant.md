# Branch Protection Enforcement as Tier-0 Governance Invariant

**Authority**: Tier-0 Governance (CATASTROPHIC)  
**Status**: MANDATORY  
**Enforcement**: Automatic (Execution-Blocking)  
**Version**: 1.0.0  
**Date**: 2026-01-01

---

## Overview

This specification defines branch protection enforcement as a **Tier-0 Governance Invariant**.

Branch protection is not merely a best practice or configuration detail—it is a **constitutional requirement** that MUST be verified before FM runtime can proceed.

---

## Problem Statement

### The Silent Bypass Vector

Current governance runtime assumes required CI checks are enforced via GitHub branch protection. However, this assumption is **not itself governed or verified**, creating a potential silent bypass vector:

1. Governance defines required checks (Tier-0 activation, coupling, code review)
2. CI workflows implement these checks
3. **BUT**: If branch protection is not configured, these checks can be bypassed
4. **RESULT**: Governance appears enforced but is actually optional

### Why This Is Catastrophic

Without verification of branch protection configuration:

- Required checks become advisory (can be ignored)
- Merge can proceed despite RED gates
- Governance violations become silent
- Tier-0 activation becomes optional
- Constitutional protections are bypassed

This violates the foundational principle: **Governance is absolute, not advisory**.

---

## Solution: Branch Protection as Tier-0 Invariant

### Definition

Branch protection enforcement is elevated to a **Tier-0 Governance Invariant**:

- **Level**: TIER-0 (Constitutional)
- **Status**: MANDATORY (Non-negotiable)
- **Verification**: Automatic (Runtime-verified)
- **Failure Semantics**: STOP + ESCALATE

### Required Checks

The following CI checks MUST be enforced via GitHub branch protection:

1. **Tier-0 Activation Gate**
   - Check Name: "Validate Tier-0 Governance Activation"
   - Workflow: `.github/workflows/tier0-activation-gate.yml`
   - Purpose: Validates Tier-0 canonical governance activation

2. **Governance Coupling Gate**
   - Check Name: "Validate Governance Coupling Rule"
   - Workflow: `.github/workflows/governance-coupling-gate.yml`
   - Purpose: Prevents governance drift (canon changes must couple with enforcement)

3. **Code Review Closure Gate**
   - Check Name: "Validate Code Review Closure"
   - Workflow: `.github/workflows/code-review-closure-gate.yml`
   - Purpose: Enforces code review closure ratchet

### Enforcement Mechanism

```
┌─────────────────────────────────────────────────────┐
│ FM Runtime Startup                                   │
└─────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│ Load Tier-0 Manifest                                 │
│ (governance/TIER_0_CANON_MANIFEST.json)             │
└─────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│ Extract Required Checks                              │
│ (branch_protection_enforcement section)             │
└─────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│ Fetch Branch Protection Config                       │
│ (via GitHub API or CLI)                             │
└─────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│ Verify Required Checks Are Enforced                 │
│ (compare manifest vs. actual config)                │
└─────────────────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
    ✅ PASS                  ❌ FAIL
    Continue                 STOP + ESCALATE
```

### Verification Script

**Location**: `scripts/verify_branch_protection_enforcement.py`

**Responsibilities**:
1. Load Tier-0 manifest
2. Extract required checks list
3. Query GitHub API for branch protection config
4. Compare required vs. actual checks
5. Report missing checks with CATASTROPHIC severity
6. STOP execution if any check is missing
7. Escalate to Johan Ras

**Exit Codes**:
- `0`: All required checks enforced (GREEN)
- `1`: Missing required checks or verification failed (RED)

---

## Failure Handling

### On Missing Required Check

**Action**: STOP  
**Escalation**: MANDATORY  
**Target**: Johan Ras  
**Blocking**: YES  
**Message**: "CATASTROPHIC: Required CI check not enforced via branch protection"

**Diagnostic Output**:
```
❌ VERIFICATION FAILED

Missing required checks:
  - Validate Tier-0 Governance Activation (ID: tier0-activation)
    Purpose: Validates Tier-0 activation in FM agent contract
    Workflow: .github/workflows/tier0-activation-gate.yml

IMPACT:
  - FM runtime CANNOT proceed
  - Execution STOPPED
  - Manual intervention REQUIRED

REQUIRED ACTIONS:
1. Navigate to: https://github.com/{repo}/settings/branches
2. Edit branch protection rule for 'main'
3. Enable 'Require status checks to pass before merging'
4. Add missing required status checks
5. Save branch protection settings
6. Re-run verification

ESCALATION REQUIRED: Johan Ras must be notified
```

### On Verification Failure

**Action**: STOP  
**Escalation**: MANDATORY  
**Target**: Johan Ras  
**Blocking**: YES  
**Message**: "CATASTROPHIC: Cannot verify branch protection configuration"

**Causes**:
- GitHub API unavailable
- Authentication failure
- Network timeout
- Repository access denied
- Branch protection API disabled

**Resolution**:
- Check GitHub API status
- Verify GITHUB_TOKEN permissions
- Verify network connectivity
- Escalate to platform administrator

---

## Integration Points

### 1. Tier-0 Manifest

**File**: `governance/TIER_0_CANON_MANIFEST.json`

**Section**: `branch_protection_enforcement`

```json
{
  "branch_protection_enforcement": {
    "required": true,
    "enforcement_level": "TIER_0_INVARIANT",
    "purpose": "Ensures required CI checks are enforced via GitHub branch protection",
    "required_checks": [
      {
        "id": "tier0-activation",
        "check_name": "Validate Tier-0 Governance Activation",
        "workflow_file": ".github/workflows/tier0-activation-gate.yml",
        "blocking": true,
        "purpose": "Validates Tier-0 activation in FM agent contract"
      },
      ...
    ],
    "verification_script": "scripts/verify_branch_protection_enforcement.py",
    "failure_handling": {
      "on_missing_required_check": {
        "action": "STOP",
        "escalation": "MANDATORY",
        "escalation_target": "Johan Ras",
        "blocking": true,
        "message": "CATASTROPHIC: Required CI check not enforced via branch protection"
      }
    }
  }
}
```

### 2. Tier-0 Activation Gate

**File**: `.github/workflows/tier0-activation-gate.yml`

**Integration**: New step added after Tier-0 activation validation

```yaml
- name: Verify Branch Protection Enforcement
  id: verify_branch_protection
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    python scripts/verify_branch_protection_enforcement.py
```

**Failure Behavior**:
- Workflow fails if verification fails
- PR merge is blocked
- Escalation issue is created
- Johan Ras is notified

### 3. FM Runtime (Future)

When FM runtime is implemented, it MUST:

1. Run `verify_branch_protection_enforcement.py` at startup
2. STOP execution if verification fails
3. Log CATASTROPHIC error with diagnostic output
4. Refuse to accept any build tasks
5. Escalate to Johan Ras

**Pseudocode**:
```python
def initialize_fm_runtime():
    # Load Tier-0 governance
    load_tier0_manifest()
    
    # MANDATORY: Verify branch protection enforcement
    if not verify_branch_protection_enforcement():
        log.catastrophic("Required CI checks not enforced via branch protection")
        escalate_to_johan_ras()
        sys.exit(1)  # STOP execution
    
    # Proceed with normal initialization
    ...
```

---

## Testing & Validation

### Manual Testing

```bash
# Test verification script
python scripts/verify_branch_protection_enforcement.py

# Test with specific repo and branch
python scripts/verify_branch_protection_enforcement.py \
  --repo MaturionISMS/maturion-foreman-office-app \
  --branch main
```

### CI Testing

The verification runs automatically in the Tier-0 activation gate on:
- Every PR (opened, synchronized, reopened)
- Push to main branch

### Expected Outcomes

**When branch protection is properly configured**:
```
✅ PASS: Tier-0 manifest loaded successfully
✅ PASS: 3 required checks defined
✅ PASS: Branch protection enabled
✅ PASS: 3 status checks configured
  ✅ ENFORCED: Validate Tier-0 Governance Activation
  ✅ ENFORCED: Validate Governance Coupling Rule
  ✅ ENFORCED: Validate Code Review Closure

✅ ALL CHECKS PASSED
```

**When branch protection is missing checks**:
```
✅ PASS: Tier-0 manifest loaded successfully
✅ PASS: 3 required checks defined
✅ PASS: Branch protection enabled
✅ PASS: 2 status checks configured
  ❌ MISSING: Validate Code Review Closure (ID: code-review-closure)

❌ VERIFICATION FAILED
```

---

## Regression Prevention

This specification prevents regression by:

1. **Making the assumption explicit**: Branch protection is now a verified requirement, not an assumption
2. **Automatic verification**: Runs on every PR and main push
3. **Merge blocking**: PR cannot merge if verification fails
4. **Escalation**: Johan Ras is notified of failures
5. **Tier-0 status**: Cannot be weakened or removed without constitutional change

### Ratchet Condition

Once this enforcement is activated:
- Branch protection verification becomes MANDATORY
- Absence of verification is a CATASTROPHIC failure
- Regression is impossible without governance violation
- Any attempt to bypass or weaken triggers escalation

---

## Authority & Compliance

**Constitutional Basis**:
- BUILD_PHILOSOPHY.md (Supreme Authority)
- governance/policies/governance-supremacy-rule.md
- governance/TIER_0_CANON_MANIFEST.json

**Modification Authority**: Johan Ras ONLY

**Weakening Prohibition**: No agent may weaken or bypass branch protection enforcement except via Johan emergency override (temporary, documented, bounded)

**Audit Requirement**: Continuous verification via CI (every PR, every push)

---

## Summary

Branch protection enforcement is now a **Tier-0 Governance Invariant**:

✅ **Explicit**: Defined in manifest, not assumed  
✅ **Verified**: Automatically checked at runtime  
✅ **Enforced**: STOP + ESCALATE on failure  
✅ **Constitutional**: Cannot be weakened  
✅ **Regression-proof**: Automatic verification prevents bypass  

**Result**: Governance is truly absolute, not advisory.

---

**Version History**:

| Version | Date | Changes | Authority |
|---------|------|---------|-----------|
| 1.0.0 | 2026-01-01 | Initial specification | FM Repo Builder Agent |

---

*END OF SPECIFICATION*
