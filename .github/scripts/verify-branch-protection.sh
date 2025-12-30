#!/bin/bash
# Script: verify-branch-protection.sh
# Purpose: Verify branch protection settings via GitHub API
# Usage: ./verify-branch-protection.sh
# Requires: GitHub CLI (gh) or GITHUB_TOKEN environment variable

set -e

REPO="MaturionISMS/maturion-foreman-office-app"
BRANCH="main"

echo "🔍 Verifying branch protection for $REPO ($BRANCH)..."
echo ""

# Check if gh CLI is available
if command -v gh &> /dev/null; then
    echo "Using GitHub CLI (gh)..."
    echo ""
    
    # Get required status checks
    echo "=== Required Status Checks ==="
    gh api repos/$REPO/branches/$BRANCH/protection \
      --jq '.required_status_checks.checks[] | .context' \
      2>/dev/null || {
        echo "⚠️ Could not retrieve branch protection settings"
        echo "This may indicate:"
        echo "  - Branch protection not configured"
        echo "  - Insufficient permissions"
        echo "  - GitHub API error"
        exit 1
      }
    
    echo ""
    echo "=== Expected Status Checks ==="
    echo "1. Enforce Architecture 100% + Block Agent Conclusion"
    echo "2. Validate Builder QA Report"
    echo "3. Enforce Agent-Scoped QA Boundaries"
    echo "4. Enforce Build-to-Green"
    echo "5. Validate Governance Artifact Compliance"
    
    echo ""
    echo "=== Branch Protection Settings ==="
    gh api repos/$REPO/branches/$BRANCH/protection \
      --jq '{
        require_pull_request_reviews: .required_pull_request_reviews.required_approving_review_count,
        require_status_checks: .required_status_checks.strict,
        enforce_admins: .enforce_admins.enabled,
        allow_force_pushes: .allow_force_pushes.enabled,
        allow_deletions: .allow_deletions.enabled
      }' \
      2>/dev/null
    
    echo ""
    echo "✅ Verification complete. Review output above."
    
elif [ -n "$GITHUB_TOKEN" ]; then
    echo "Using curl with GITHUB_TOKEN..."
    echo ""
    
    # Get required status checks
    echo "=== Required Status Checks ==="
    curl -s -H "Authorization: token $GITHUB_TOKEN" \
      "https://api.github.com/repos/$REPO/branches/$BRANCH/protection" \
      | jq -r '.required_status_checks.checks[] | .context' \
      2>/dev/null || {
        echo "⚠️ Could not retrieve branch protection settings"
        exit 1
      }
    
    echo ""
    echo "=== Expected Status Checks ==="
    echo "1. Enforce Architecture 100% + Block Agent Conclusion"
    echo "2. Validate Builder QA Report"
    echo "3. Enforce Agent-Scoped QA Boundaries"
    echo "4. Enforce Build-to-Green"
    echo "5. Validate Governance Artifact Compliance"
    
    echo ""
    echo "✅ Verification complete. Review output above."
    
else
    echo "❌ Error: Neither 'gh' CLI nor GITHUB_TOKEN found"
    echo ""
    echo "To run this script, you need either:"
    echo "1. GitHub CLI installed (gh): https://cli.github.com/"
    echo "2. GITHUB_TOKEN environment variable set"
    echo ""
    echo "Manual verification required:"
    echo "1. Navigate to: https://github.com/$REPO/settings/branches"
    echo "2. Click 'Edit' on $BRANCH branch protection rule"
    echo "3. Scroll to 'Require status checks to pass before merging'"
    echo "4. Verify all 5 gate workflows are listed as required"
    echo "5. Take screenshot for evidence"
    exit 1
fi
