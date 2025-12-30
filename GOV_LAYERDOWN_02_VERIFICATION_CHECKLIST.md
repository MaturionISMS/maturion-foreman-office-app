# GOV-LAYERDOWN-02 — Verification Checklist

**Issue**: GOV-LAYERDOWN-02  
**For**: Repository Owner (Johan Ras)  
**Purpose**: Verify branch protection and complete layer-down  
**Date**: 2025-12-30

---

## I. Quick Summary

The FM Repository has **substantially complete** PR gate layer-down from canonical governance.

**Status**: ✅ READY FOR BUILDER APPOINTMENT  
**Remaining**: 2 verification tasks (requires admin access)

---

## II. What's Already Complete ✅

### Implemented PR Gates (4 of 5 standalone workflows)

1. ✅ **Builder QA Gate** (`.github/workflows/builder-qa-gate.yml`)
   - Validates Builder QA Report presence, schema, READY status
   - Role-aware (skips for FM/Governance)
   - Canonical Gate 1

2. ✅ **Agent Boundary Gate** (`.github/workflows/agent-boundary-gate.yml`)
   - Validates agent-scoped QA boundaries
   - Detects cross-agent QA violations (CATASTROPHIC)
   - Canonical Gate 2

3. ✅ **Build-to-Green Enforcement** (`.github/workflows/build-to-green-enforcement.yml`)
   - Validates test dodging patterns
   - Enforces DP-RED governance
   - Canonical Gate 5

4. ✅ **FM Architecture Gate** (`.github/workflows/fm-architecture-gate.yml`)
   - Validates architecture completeness = 100%
   - Enforces zero drift
   - Role-aware (FM Agent only)
   - Canonical Gate 4

### Governance Documentation ✅

1. ✅ `governance/alignment/PR_GATE_REQUIREMENTS_CANON.md` — Canonical mirror
2. ✅ `governance/alignment/PR_GATE_FAILURE_HANDLING_PROTOCOL.md` — Failure classifications
3. ✅ `governance/alignment/TWO_GATEKEEPER_MODEL.md` — Dual gatekeeper model
4. ✅ `governance/policies/RED_GATE_AUTHORITY_AND_OWNERSHIP.md` — Gate ownership
5. ✅ `governance/policies/FM_GOVERNANCE_ADOPTION_POLICY.md` — Governance translation

---

## III. Verification Tasks (Requires Admin Access)

### Task 1: Verify Branch Protection Settings

**Action**: Check that all PR gate workflows are **required status checks**

**Steps**:

1. Navigate to: https://github.com/MaturionISMS/maturion-foreman-office-app/settings/branches

2. Click "Edit" on the `main` branch protection rule

3. Scroll to "Require status checks to pass before merging"

4. Verify the following are checked:
   - ☐ "Require status checks to pass before merging" = ✅ Enabled
   - ☐ "Require branches to be up to date before merging" = ✅ Enabled

5. In "Status checks that are required", verify these are listed:
   - ☐ **Enforce Build-to-Green** (from build-to-green-enforcement.yml)
   - ☐ **Validate Builder QA Report** (from builder-qa-gate.yml)
   - ☐ **Enforce Agent-Scoped QA Boundaries** (from agent-boundary-gate.yml)
   - ☐ **Enforce Architecture 100% + Block Agent Conclusion** (from fm-architecture-gate.yml)

**If any are missing**:
- Click "Add status check"
- Search for the workflow name
- Select and save

**Evidence**:
- Take screenshot showing all required checks
- Save to: `.github/branch-protection-evidence-YYYY-MM-DD.png`

---

### Task 2: Document Branch Protection Configuration

**Action**: Create documentation of branch protection settings

**Steps**:

1. Copy the template from `GOV_LAYERDOWN_02_GAP_CLOSURE_SPEC.md` Section III.5

2. Create file: `.github/BRANCH_PROTECTION.md`

3. Fill in:
   - Last Verified date
   - Verified By name
   - Evidence link (screenshot from Task 1)

4. Commit and push:
   ```bash
   git add .github/BRANCH_PROTECTION.md .github/branch-protection-evidence-*.png
   git commit -m "Document branch protection configuration"
   git push
   ```

---

## IV. Optional Enhancements (Can Defer)

### Enhancement 1: Governance Artifact Gate (Gap 1)

**Status**: Validation logic exists (distributed), standalone workflow would improve clarity

**If you want to implement**:
- Complete workflow YAML is in `GOV_LAYERDOWN_02_GAP_CLOSURE_SPEC.md` Section 1.4
- Copy to: `.github/workflows/governance-artifact-gate.yml`
- Add to branch protection required checks

**If you want to defer**:
- Current distributed validation is sufficient
- Can implement in future wave

---

### Enhancement 2: CODEOWNERS File

**Status**: Not required for layer-down, but improves workflow

**If you want to implement**:
- Template is in `GOV_LAYERDOWN_02_GAP_CLOSURE_SPEC.md` Section IV.1
- Copy to: `.github/CODEOWNERS`
- Requires GitHub teams to exist:
  - `@MaturionISMS/governance-liaisons`
  - `@MaturionISMS/fm-builders`

---

## V. Verification Commands (For Reference)

If you have GitHub CLI with admin permissions:

```bash
# Check branch protection
gh api repos/MaturionISMS/maturion-foreman-office-app/branches/main/protection \
  --jq '.required_status_checks.checks[] | .context'

# Expected output:
# Enforce Build-to-Green
# Validate Builder QA Report
# Enforce Agent-Scoped QA Boundaries
# Enforce Architecture 100% + Block Agent Conclusion
```

---

## VI. Completion Criteria

Layer-down is **100% complete** when:

- [x] All 5 canonical PR gates have enforcement logic (DONE)
- [x] 4 of 5 gates have standalone workflows (DONE)
- [ ] All gate workflows are required status checks in branch protection (VERIFY)
- [ ] Branch protection configuration is documented (VERIFY)

**Current**: 2/4 complete  
**Remaining**: 2 verification tasks (both require admin access)

---

## VII. After Verification Complete

Once you've completed Tasks 1-2:

1. Update `GOV_LAYERDOWN_02_ASSESSMENT.md`:
   - Change "Gap 2" status from "Not verified" to "VERIFIED"
   - Add evidence reference (screenshot link)
   - Update determination to "100% COMPLETE"

2. Close issue GOV-LAYERDOWN-02 with comment:
   ```
   PR gate layer-down is 100% complete.
   
   ✅ All 5 canonical gates implemented
   ✅ All gates role-aware
   ✅ All gates are required status checks
   ✅ Branch protection documented
   
   Evidence: .github/branch-protection-evidence-YYYY-MM-DD.png
   ```

3. Builder agents can now rely on PR gate enforcement for Build-to-Green operations

---

## VIII. Questions or Issues?

If any status checks are missing or you need help:

1. Verify workflow files exist in `.github/workflows/`
2. Check that workflows have run at least once (they must succeed to be available as required checks)
3. Check GitHub Actions > Workflows to see if workflows are enabled
4. If a workflow hasn't run yet, make a test commit to trigger it

**Note**: GitHub only lists workflows as available status checks after they've run at least once successfully.

---

## IX. Summary for Johan

**What I did**:
- Analyzed all canonical PR gate requirements
- Verified 4 of 5 gates are implemented as standalone workflows
- Confirmed all 5 gates have enforcement logic (1 distributed)
- Verified role-aware enforcement
- Verified canonical failure classifications
- Verified prohibited actions absent
- Created comprehensive assessment + gap closure spec

**What you need to do**:
1. ✅ Verify branch protection settings (5 minutes)
2. ✅ Document configuration (5 minutes)

**Result**:
- Layer-down will be 100% complete
- Builder agents can rely on PR gate enforcement
- FM Repository governance-aligned

---

**Assessment Complete**: ✅ YES  
**Implementation Ready**: ✅ YES  
**Blockers**: None (just verification)  
**Time Required**: ~10 minutes (admin tasks only)
