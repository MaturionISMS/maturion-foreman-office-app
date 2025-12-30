# Branch Protection Configuration

**Repository**: maturion-foreman-office-app  
**Branch**: main  
**Last Verified**: 2025-12-30  
**Authority**: Repository Admin (Johan Ras)  
**Status**: Documented (Verification Required)

---

## Purpose

This document specifies the required branch protection configuration for the `main` branch to enforce PR gate requirements mechanically.

**Governance Requirement**: All PR gates must be configured as required status checks to ensure merge is impossible when any gate is RED.

**Reference**: 
- `governance/alignment/PR_GATE_REQUIREMENTS_CANON.md`
- `governance/policies/RED_GATE_AUTHORITY_AND_OWNERSHIP.md`
- BL-0008: PR gate layer-down prerequisite

---

## Required Status Checks

The following workflows **MUST** be configured as required status checks before merge:

### 1. FM Architecture Gate
- **Workflow**: `.github/workflows/fm-architecture-gate.yml`
- **Job Name**: `fm-architecture-gate`
- **Status Check Name**: "Enforce Architecture 100% + Block Agent Conclusion"
- **Applicability**: FM Agent role ONLY
- **Purpose**: Enforces FM architecture completeness (100%) and drift status (NONE)
- **Failure Semantics**: Architecture incomplete → Block merge

### 2. Builder QA Gate
- **Workflow**: `.github/workflows/builder-qa-gate.yml`
- **Job Name**: `validate-builder-qa`
- **Status Check Name**: "Validate Builder QA Report"
- **Applicability**: Builder role (ISMS module repos); Advisory for FM repo
- **Purpose**: Validates Builder QA Report presence, schema, and READY status
- **Failure Semantics**: Builder declares NOT_READY → Block merge (trust Builder)

### 3. Agent Boundary Gate
- **Workflow**: `.github/workflows/agent-boundary-gate.yml`
- **Job Name**: `enforce-agent-boundaries`
- **Status Check Name**: "Enforce Agent-Scoped QA Boundaries"
- **Applicability**: ALL roles
- **Purpose**: Enforces agent-scoped QA boundaries (Builder/FM/Governance QA separation)
- **Failure Semantics**: Cross-agent QA violation → Catastrophic governance violation → Block merge + escalation

### 4. Build-to-Green Enforcement
- **Workflow**: `.github/workflows/build-to-green-enforcement.yml`
- **Job Name**: `build-to-green`
- **Status Check Name**: "Enforce Build-to-Green"
- **Applicability**: ALL roles
- **Purpose**: Enforces Build-to-Green contract by running test suite and checking for test dodging
- **Failure Semantics**: Test failures → Block merge; Test dodging → Block merge

### 5. Governance Compliance Gate
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

### Manual Verification (Required Before Builder Appointment)

1. Navigate to: `https://github.com/MaturionISMS/maturion-foreman-office-app/settings/branches`
2. Click "Edit" on the `main` branch protection rule
3. Scroll to "Require status checks to pass before merging"
4. Verify the section "Status checks that are required" includes:
   - ✅ Enforce Architecture 100% + Block Agent Conclusion
   - ✅ Validate Builder QA Report
   - ✅ Enforce Agent-Scoped QA Boundaries
   - ✅ Enforce Build-to-Green
   - ✅ Validate Governance Artifact Compliance
5. Take screenshot for evidence
6. Document verification in assessment

### Automated Verification (Future Enhancement)

**Script**: `.github/scripts/verify-branch-protection.sh`

```bash
#!/bin/bash
# Script: verify-branch-protection.sh
# Purpose: Verify branch protection settings via GitHub API

REPO="MaturionISMS/maturion-foreman-office-app"
BRANCH="main"

echo "🔍 Verifying branch protection for $REPO ($BRANCH)..."

# Requires GitHub CLI (gh) or curl with token
gh api repos/$REPO/branches/$BRANCH/protection \
  --jq '.required_status_checks.checks[] | .context' \
  > /tmp/required-checks.txt

echo "Required status checks:"
cat /tmp/required-checks.txt

echo ""
echo "Expected checks:"
echo "- Enforce Architecture 100% + Block Agent Conclusion"
echo "- Validate Builder QA Report"
echo "- Enforce Agent-Scoped QA Boundaries"
echo "- Enforce Build-to-Green"
echo "- Validate Governance Artifact Compliance"

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

For BL-0008 completion, the following evidence MUST be provided:

1. **Screenshot**: GitHub Settings > Branches > main > Edit showing:
   - Required status checks list
   - All 5 gate workflows listed
   - Branch protection settings enabled

2. **API Output** (Optional): Output from `gh api` command showing:
   - Required status checks configuration
   - Branch protection settings JSON

3. **Verification Date**: Date when configuration was last verified

4. **Verifier**: Name of person who performed verification

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
