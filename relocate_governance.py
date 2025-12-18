#!/usr/bin/env python3
"""
Relocate FM-level governance artefacts to maturion-foreman-governance repository.

This script:
1. Moves governance files to canonical directories
2. Creates pointer READMEs in original locations
3. Generates a manifest of all changes
"""

import os
import shutil
import json
from pathlib import Path

# Base repository URL for canonical links
GOVERNANCE_REPO_URL = "https://github.com/MaturionISMS/maturion-foreman-governance"

# File classifications
FILE_MOVES = {
    "governance/policies": [
        "foreman/governance/governance-supremacy-rule.md",
        "foreman/governance/zero-test-debt-constitutional-rule.md",
        "foreman/governance/design-freeze-rule.md",
        "foreman/governance/dp-red-policy.md",
        "foreman/platform/ai-cost-optimization-policy.md",
        "foreman/platform/image-generation-policy.md",
        "foreman/platform/security-escalation-policy.md",
        "foreman/innovation/idea-voting-policy.md",
        "foreman/innovation/threshold-policy.md",
        "foreman/change-management/change-policy.md",
        "foreman/privacy-guardrails.md",
        "foreman/memory-model.md",
        "foreman/versioning-rules.md",
        "foreman/architecture-naming-conventions.md",
        "foreman/architecture-folder-structure.md",
        "foreman/architecture-standardisation-policy.md",
    ],
    "governance/contracts": [
        "foreman/constitution/architecture-design-checklist.md",
        "foreman/qa/quality-integrity-contract.md",
        "foreman/evidence/GOVERNANCE_GATE_SPEC.md",
    ],
    "governance/specs": [
        "foreman/governance/build-to-green-enforcement-spec.md",
        "foreman/governance/foreman-execution-state-model.md",
        "foreman/compliance/compliance-qa-spec.md",
        "foreman/compliance/compliance-watchdog-spec.md",
        "foreman/compliance/compliance-reference-map.md",
        "foreman/qa-governance.md",
        "foreman/qa-of-qa.md",
        "foreman/qa-minimum-coverage-requirements.md",
        "foreman/minimum-architecture-template.md",
        "foreman/architecture-validation-checklist.md",
        "foreman/qa-of-qa-validation-checklist.md",
        "foreman/module-readiness-report-template.md",
        "foreman/task-distribution-rules.md",
        "foreman/innovation/idea-submission-spec.md",
        "foreman/innovation/idea-summarisation-rules.md",
        "foreman/innovation/innovation-workflow-spec.md",
        "foreman/innovation/roadmap-generation-spec.md",
        "foreman/survey/survey-engine-spec.md",
        "foreman/survey/survey-ai-analysis-spec.md",
        "foreman/admin/enhancement-parking-lot-spec.md",
        "foreman/admin/admin-innovation-chat-spec.md",
        "foreman/admin/ai-self-improvement-spec.md",
        "foreman/runtime/ai-drift-monitor-spec.md",
        "foreman/runtime/behaviour-log-spec.md",
        "foreman/runtime/db-observer-spec.md",
        "foreman/runtime/incident-detection-spec.md",
        "foreman/runtime/runtime-risk-model-spec.md",
        "foreman/runtime/runtime-state-spec.md",
        "foreman/runtime/system-health-checks-spec.md",
        "foreman/self-test/self-test-spec.md",
        "foreman/test-environment/test-env-architecture.md",
        "foreman/test-environment/test-env-data-policy.md",
        "foreman/platform/privacy-leak-detection-spec.md",
        "foreman/platform/watchdog-standard-spec.md",
        "foreman/platform/ui-branding-standard.md",
        "foreman/platform/ui-theme-overrides.md",
        "foreman/platform/ui-navigation-spec.md",
        "foreman/platform/ui-multiwindow-spec.md",
        "foreman/platform/ui-ai-edit-session-spec.md",
        "foreman/platform/image-model-routing-spec.md",
        "foreman/platform/ai-performance-metrics-spec.md",
        "foreman/platform/ai-usage-analytics-spec.md",
    ],
    "governance/dashboards": [
        "foreman/platform/qa-dashboard-spec.md",
        "foreman/platform/governance-qa-dashboard-spec.md",
        "foreman/compliance/compliance-dashboard-spec.md",
        "foreman/innovation/innovation-dashboard-spec.md",
    ],
}


def create_pointer_readme(original_path: str, canonical_path: str) -> str:
    """Create pointer README content."""
    filename = os.path.basename(original_path)
    canonical_url = f"{GOVERNANCE_REPO_URL}/tree/main/{canonical_path}"
    
    content = f"""# {filename}

**This document is governed by Foreman Governance.**

**The canonical version is located at:** [{canonical_url}]({canonical_url})

---

## What This Means

This file has been relocated to the **maturion-foreman-governance** repository to:
- Centralize FM-level governance artefacts
- Separate governance from implementation
- Maintain a single source of truth for governance policies, contracts, and specifications

## How to Access

Visit the canonical location above to access the current version of this document.

## Repository Structure

FM-level governance is now organized in the maturion-foreman-governance repository under:
- `governance/policies/` - Governance policies and rules
- `governance/contracts/` - Contracts and checklists
- `governance/specs/` - Specifications and standards
- `governance/dashboards/` - Dashboard specifications

This change is normalization only. No enforcement, CI, doctrine, or runtime changes were made.
"""
    return content


def relocate_files(dry_run: bool = False):
    """Relocate files and create pointers."""
    manifest = {
        "moved_files": [],
        "pointer_readmes": [],
        "issues": [],
    }
    
    for dest_dir, file_list in FILE_MOVES.items():
        # Ensure destination directory exists
        if not dry_run:
            os.makedirs(dest_dir, exist_ok=True)
        
        for source_path in file_list:
            if not os.path.exists(source_path):
                manifest["issues"].append(f"Source file not found: {source_path}")
                continue
            
            # Determine destination path
            filename = os.path.basename(source_path)
            dest_path = os.path.join(dest_dir, filename)
            
            # Move the file
            if not dry_run:
                shutil.copy2(source_path, dest_path)
            
            manifest["moved_files"].append({
                "source": source_path,
                "destination": dest_path,
                "category": dest_dir.split("/")[-1],  # policies, contracts, specs, dashboards
            })
            
            # Create pointer README
            pointer_readme_path = source_path.replace(".md", "_README.md")
            if source_path.endswith(".md"):
                # For .md files, replace the original with pointer
                pointer_readme_path = source_path
            
            pointer_content = create_pointer_readme(source_path, dest_path)
            
            if not dry_run:
                with open(pointer_readme_path, "w") as f:
                    f.write(pointer_content)
            
            manifest["pointer_readmes"].append({
                "path": pointer_readme_path,
                "points_to": dest_path,
            })
    
    return manifest


def main():
    """Main execution."""
    print("=== FM-Level Governance Relocation ===\n")
    
    # Perform dry run first
    print("Performing dry run...")
    manifest = relocate_files(dry_run=True)
    
    print(f"\nFiles to move: {len(manifest['moved_files'])}")
    print(f"Pointer READMEs to create: {len(manifest['pointer_readmes'])}")
    print(f"Issues found: {len(manifest['issues'])}")
    
    if manifest["issues"]:
        print("\nIssues:")
        for issue in manifest["issues"]:
            print(f"  - {issue}")
        return
    
    # Perform actual relocation
    print("\nPerforming actual relocation...")
    manifest = relocate_files(dry_run=False)
    
    # Save manifest
    with open("GOVERNANCE_RELOCATION_MANIFEST.json", "w") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\n✅ Relocation complete!")
    print(f"   Files moved: {len(manifest['moved_files'])}")
    print(f"   Pointer READMEs created: {len(manifest['pointer_readmes'])}")
    print(f"\nManifest saved to: GOVERNANCE_RELOCATION_MANIFEST.json")
    
    # Print summary by category
    print("\n=== Summary by Category ===")
    by_category = {}
    for item in manifest["moved_files"]:
        cat = item["category"]
        by_category[cat] = by_category.get(cat, 0) + 1
    
    for cat, count in sorted(by_category.items()):
        print(f"  {cat}: {count} files")


if __name__ == "__main__":
    main()
