# Branch Protection Configuration

**Repository**: maturion-foreman-office-app  
**Branch**: main  
**Last Updated**: 2026-01-01  
**Authority**: Repository Admin (Johan Ras)  
**Status**: TIER-0 GOVERNANCE INVARIANT (Automatically Verified)

---

## Purpose

This document specifies the required branch protection configuration for the `main` branch to enforce PR gate requirements mechanically.

**Governance Requirement**: All PR gates must be configured as required status checks to ensure merge is impossible when any gate is RED.

**⚠️ CRITICAL CHANGE**: As of 2026-01-01, branch protection enforcement is now a **TIER-0 GOVERNANCE INVARIANT**. The FM runtime MUST verify that required checks are enforced before proceeding. See `governance/specs/branch-protection-enforcement-tier0-invariant.md` for details.

**Reference**: 
- `governance/specs/branch-protection-enforcement-tier0-invariant.md` (Tier-0 Invariant)
- `governance/alignment/PR_GATE_REQUIREMENTS_CANON.md`
- `governance/policies/RED_GATE_AUTHORITY_AND_OWNERSHIP.md`
- `governance/TIER_0_CANON_MANIFEST.json` (branch_protection_enforcement section)
- BL-0008: PR gate layer-down prerequisite

---

## Tier-0 Required Checks (MANDATORY)

The following checks are **TIER-0 MANDATORY** and automatically verified by the FM runtime:

### 1. Tier-0 Governance Activation Gate
- **Workflow**: `.github/workflows/tier0-activation-gate.yml`
- **Job Name**: `validate-tier0-activation`
- **Status Check Name**: "Validate Tier-0 Governance Activation"
- **Applicability**: ALL roles (universal)
- **Purpose**: Validates Tier-0 canonical governance activation and branch protection enforcement
- **Failure Semantics**: Tier-0 not activated → CATASTROPHIC → Block merge + Escalation
- **Enforcement Level**: TIER-0 INVARIANT

### 2. Governance Coupling Gate
- **Workflow**: `.github/workflows/governance-coupling-gate.yml`
- **Job Name**: `validate-governance-coupling`
- **Status Check Name**: "Validate Governance Coupling Rule"
- **Applicability**: ALL roles (universal)
- **Purpose**: Prevents governance drift (ensures governance changes are coupled with enforcement updates)
- **Failure Semantics**: Coupling violation → CATASTROPHIC → Block merge + Escalation
- **Enforcement Level**: TIER-0 INVARIANT

### 3. Code Review Closure Gate
- **Workflow**: `.github/workflows/code-review-closure-gate.yml`
- **Job Name**: `validate-code-review-closure`
- **Status Check Name**: "Validate Code Review Closure"
- **Applicability**: ALL roles (universal)
- **Purpose**: Enforces code review closure ratchet compliance
- **Failure Semantics**: Review closure missing → CATASTROPHIC → Block merge + Escalation
- **Enforcement Level**: TIER-0 INVARIANT

**⚠️ AUTOMATIC VERIFICATION**: These three checks are automatically verified by `scripts/verify_branch_protection_enforcement.py` at runtime. If any are missing, FM runtime will STOP with CATASTROPHIC error and escalate to Johan Ras.

---

## Additional Required Status Checks

The following workflows **MUST** also be configured as required status checks before merge:

### 4. FM Architecture Gate
- **Workflow**: `.github/workflows/fm-architecture-gate.yml`
- **Job Name**: `fm-architecture-gate`
- **Status Check Name**: "Enforce Architecture 100% + Block Agent Conclusion"
- **Applicability**: FM Agent role ONLY
- **Purpose**: Enforces FM architecture completeness (100%) and drift status (NONE)
- **Failure Semantics**: Architecture incomplete → Block merge

### 5. Builder QA Gate
- **Workflow**: `.github/workflows/builder-qa-gate.yml`
- **Job Name**: `validate-builder-qa`
- **Status Check Name**: "Validate Builder QA Report"
- **Applicability**: Builder role (ISMS module repos); Advisory for FM repo
- **Purpose**: Validates Builder QA Report presence, schema, and READY status
- **Failure Semantics**: Builder declares NOT_READY → Block merge (trust Builder)

### 6. Agent Boundary Gate
- **Workflow**: `.github/workflows/agent-boundary-gate.yml`
- **Job Name**: `enforce-agent-boundaries`
- **Status Check Name**: "Enforce Agent-Scoped QA Boundaries"
- **Applicability**: ALL roles
- **Purpose**: Enforces agent-scoped QA boundaries (Builder/FM/Governance QA separation)
- **Failure Semantics**: Cross-agent QA violation → Catastrophic governance violation → Block merge + escalation

### 7. Build-to-Green Enforcement
- **Workflow**: `.github/workflows/build-to-green-enforcement.yml`
- **Job Name**: `build-to-green`
- **Status Check Name**: "Enforce Build-to-Green"
- **Applicability**: ALL roles
- **Purpose**: Enforces Build-to-Green contract by running test suite and checking for test dodging
- **Failure Semantics**: Test failures → Block merge; Test dodging → Block merge

### 8. Governance Compliance Gate
- **Workflow**: `.github/workflows/governance-compliance-gate.yml`
- **Job Name**: `validate-governance-artifacts`
- **Status Check Name**: "Validate Governance Artifact Compliance"
- **Applicability**: Governance Admin role (strict); Advisory for Builder/FM roles
- **Purpose**: Validates governance artifact schema compliance and immutability
- **Failure Semantics**: Schema invalid → Block merge (Governance role only)

---

## Additional Branch Protection Settings

The following settings are **REQUIRED** for complete governance enforcement:

### Merge Protection
- ✅ **Require pull request reviews before merging**: Enabled
  - Required approving reviews: 1
- ✅ **Require status checks to pass before merging**: Enabled
- ✅ **Require branches to be up to date before merging**: Enabled

### Review Protection
- ✅ **Dismiss stale pull request approvals when new commits are pushed**: Enabled
- ✅ **Require approval of the most recent reviewable push**: Enabled
- ✅ **Restrict who can dismiss pull request reviews**: Enabled

### Additional Protections (Recommended)
- ✅ **Require conversation resolution before merging**: Enabled (recommended)
- ⚠️ **Require review from Code Owners**: Optional (requires .github/CODEOWNERS file)
- ⚠️ **Require signed commits**: Optional (enhanced security)
- ⚠️ **Require linear history**: Optional (cleaner history)
- ❌ **Allow force pushes**: Disabled (MUST be disabled)
- ❌ **Allow deletions**: Disabled (MUST be disabled)
- ❌ **Lock branch**: Not recommended for main

---

## Verification Procedure

### Automatic Verification (TIER-0 ENFORCEMENT)

**Status**: ACTIVE as of 2026-01-01

Branch protection enforcement is now automatically verified as a **Tier-0 Governance Invariant**:

**Verification Script**: `scripts/verify_branch_protection_enforcement.py`

**When It Runs**:
- Every PR (opened, synchronized, reopened) via `.github/workflows/tier0-activation-gate.yml`
- Push to main branch
- FM runtime startup (future implementation)

**What It Checks**:
1. Loads Tier-0 manifest (`governance/TIER_0_CANON_MANIFEST.json`)
2. Extracts required checks from `branch_protection_enforcement` section
3. Queries GitHub API for actual branch protection configuration
4. Compares required vs. actual checks
5. STOPS execution if any required check is missing

**Tier-0 Required Checks** (automatically verified):
- ✅ Validate Tier-0 Governance Activation
- ✅ Validate Governance Coupling Rule
- ✅ Validate Code Review Closure

**Failure Behavior**:
- Workflow fails immediately
- PR merge is blocked
- Diagnostic output shows missing checks
- Escalation issue is created
- Johan Ras is notified

**Exit Codes**:
- `0`: All required checks enforced (GREEN)
- `1`: Missing required checks or verification failed (RED, CATASTROPHIC)

**To Run Manually**:
```bash
# Verify current branch protection
python scripts/verify_branch_protection_enforcement.py

# Verify specific repo/branch
python scripts/verify_branch_protection_enforcement.py \
  --repo MaturionISMS/maturion-foreman-office-app \
  --branch main
```

---

### Manual Verification (Supplemental)

For administrative purposes or troubleshooting, you can manually verify branch protection:

1. Navigate to: `https://github.com/MaturionISMS/maturion-foreman-office-app/settings/branches`
2. Click "Edit" on the `main` branch protection rule
3. Scroll to "Require status checks to pass before merging"
4. Verify the section "Status checks that are required" includes at minimum:
   - ✅ **Validate Tier-0 Governance Activation** (TIER-0 MANDATORY)
   - ✅ **Validate Governance Coupling Rule** (TIER-0 MANDATORY)
   - ✅ **Validate Code Review Closure** (TIER-0 MANDATORY)
   - ✅ Enforce Architecture 100% + Block Agent Conclusion
   - ✅ Validate Builder QA Report
   - ✅ Enforce Agent-Scoped QA Boundaries
   - ✅ Enforce Build-to-Green
   - ✅ Validate Governance Artifact Compliance
5. Take screenshot for evidence
6. Document verification in assessment

**Note**: The first three checks are Tier-0 mandatory and automatically verified. Missing them will cause CATASTROPHIC failure.

echo ""
echo "Verification complete. Review output above."
```

---

## Configuration Steps

### Step 1: Enable Branch Protection
1. Go to Settings > Branches
2. Click "Add rule" or edit existing rule for `main`
3. Enter branch name pattern: `main`

### Step 2: Configure Merge Requirements
1. Check "Require pull request reviews before merging"
   - Set required approving reviews: 1
2. Check "Dismiss stale pull request approvals when new commits are pushed"
3. Check "Require approval of the most recent reviewable push"

### Step 3: Configure Status Checks
1. Check "Require status checks to pass before merging"
2. Check "Require branches to be up to date before merging"
3. In the search box under "Status checks that are required", add:
   - Search for: "Validate Tier-0"
   - Select: "Validate Tier-0 Governance Activation" (TIER-0 MANDATORY)
   - Search for: "Validate Governance Coupling"
   - Select: "Validate Governance Coupling Rule" (TIER-0 MANDATORY)
   - Search for: "Validate Code Review"
   - Select: "Validate Code Review Closure" (TIER-0 MANDATORY)
   - Search for: "Enforce Architecture"
   - Select: "Enforce Architecture 100% + Block Agent Conclusion"
   - Search for: "Validate Builder"
   - Select: "Validate Builder QA Report"
   - Search for: "Enforce Agent"
   - Select: "Enforce Agent-Scoped QA Boundaries"
   - Search for: "Enforce Build"
   - Select: "Enforce Build-to-Green"
   - Search for: "Validate Governance"
   - Select: "Validate Governance Artifact Compliance"

**Note**: Status checks only appear in the search after they have run at least once on a PR or push to main.

**⚠️ CRITICAL**: The first three checks (Tier-0) are MANDATORY and automatically verified. Missing them will cause CATASTROPHIC failure and block execution.

### Step 4: Configure Additional Protections
1. Check "Require conversation resolution before merging" (recommended)
2. Uncheck "Allow force pushes" (if checked)
3. Uncheck "Allow deletions" (if checked)

### Step 5: Save Configuration
1. Click "Create" (new rule) or "Save changes" (existing rule)
2. Verify configuration applied correctly

---

## Verification Checklist

Use this checklist to verify branch protection configuration:

**Tier-0 Mandatory Checks** (automatically verified):
- [ ] Status check "Validate Tier-0 Governance Activation" is required ⚠️ MANDATORY
- [ ] Status check "Validate Governance Coupling Rule" is required ⚠️ MANDATORY
- [ ] Status check "Validate Code Review Closure" is required ⚠️ MANDATORY

**Additional Required Checks**:
- [ ] Branch protection rule exists for `main` branch
- [ ] "Require pull request reviews before merging" is enabled (1 approval)
- [ ] "Require status checks to pass before merging" is enabled
- [ ] "Require branches to be up to date before merging" is enabled
- [ ] Status check "Enforce Architecture 100% + Block Agent Conclusion" is required
- [ ] Status check "Validate Builder QA Report" is required
- [ ] Status check "Enforce Agent-Scoped QA Boundaries" is required
- [ ] Status check "Enforce Build-to-Green" is required
- [ ] Status check "Validate Governance Artifact Compliance" is required
- [ ] "Dismiss stale pull request approvals when new commits are pushed" is enabled
- [ ] "Require approval of the most recent reviewable push" is enabled
- [ ] "Allow force pushes" is DISABLED
- [ ] "Allow deletions" is DISABLED
- [ ] Screenshot captured for evidence
- [ ] Verification documented in assessment

---

## Evidence Requirements

For governance compliance, the following evidence is automatically generated:

1. **Automatic Verification** (TIER-0):
   - Runs on every PR via `.github/workflows/tier0-activation-gate.yml`
   - Output logged in workflow run
   - Exit code 0 = GREEN (all checks enforced)
   - Exit code 1 = RED (missing checks, CATASTROPHIC)

2. **Manual Verification Evidence** (Supplemental):
   - Screenshot: GitHub Settings > Branches > main > Edit showing required status checks
   - API Output: Output from `python scripts/verify_branch_protection_enforcement.py`
   - Verification Date: Date when manual check was performed
   - Verifier: Name of person who performed verification

**Note**: Automatic verification is now MANDATORY. Manual evidence is supplemental only.

---

## Troubleshooting

### Status Check Not Appearing in Search

**Problem**: When trying to add a status check, it doesn't appear in the search results.

**Solution**: Status checks only appear after they have run at least once. To make them visible:
1. Create a test PR
2. Trigger the workflow (push a commit or open PR)
3. Wait for workflow to complete
4. Return to branch protection settings
5. Search for the status check name again

### Multiple Status Checks with Similar Names

**Problem**: Multiple entries with similar names appear in search.

**Solution**: Select the status check that matches the exact job name from the workflow file. Verify by checking recent PR status check names.

### Configuration Not Taking Effect

**Problem**: PRs can still be merged despite RED gates.

**Solution**: 
1. Verify branch protection rule applies to correct branch (`main`)
2. Verify "Require status checks to pass before merging" is checked
3. Verify status checks are added to "required" list (not just run)
4. Verify user attempting merge doesn't have bypass permissions
5. Check repository admin settings for "Allow bypass of required status checks"

---

## Governance Authority

**Constitutional Basis**: 
- BUILD_PHILOSOPHY.md Section IX: PR Gate Requirements
- governance/policies/RED_GATE_AUTHORITY_AND_OWNERSHIP.md
- governance/alignment/PR_GATE_REQUIREMENTS_CANON.md

**Modification Authority**: Johan Ras ONLY

**Weakening Prohibition**: No agent may weaken branch protection settings except via Johan emergency override (temporary, documented, bounded)

**Audit Requirement**: Quarterly verification of branch protection configuration

---

## Version History

| Version | Date | Changes | Authority |
|---------|------|---------|-----------|
| 1.0.0 | 2025-12-30 | Initial branch protection specification (BL-0008) | FM Repo Builder Agent |

---

## References

- **PR Gate Requirements Canon**: `governance/alignment/PR_GATE_REQUIREMENTS_CANON.md`
- **Red Gate Authority**: `governance/policies/RED_GATE_AUTHORITY_AND_OWNERSHIP.md`
- **Governance Authority Matrix**: `governance/GOVERNANCE_AUTHORITY_MATRIX.md`
- **Gap Closure Spec**: `GOV_LAYERDOWN_02_GAP_CLOSURE_SPEC.md`
- **GitHub Documentation**: [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

---

**VERIFICATION STATUS**: ⚠️ NOT YET VERIFIED

This document specifies required configuration but actual GitHub settings have not yet been verified against this specification. Manual verification is REQUIRED before declaring BL-0008 complete.

**Required Action**: Repository admin must verify and capture evidence of branch protection configuration.

---

*END OF BRANCH PROTECTION CONFIGURATION*
