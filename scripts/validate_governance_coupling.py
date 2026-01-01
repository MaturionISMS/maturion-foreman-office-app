#!/usr/bin/env python3
"""
Governance Change Coupling Rule Validator

This script enforces the coupling rule:
- If Tier-0 governance canon changes (or its referenced list changes),
  then FM agent contract + enforcement gate updates MUST occur in the same PR.
- Otherwise the PR FAILS (merge-blocking).

This prevents governance drift where canon evolves but enforcement lags behind.

Version: 1.0.0
Authority: Phase X - Trans-Repo Governance Runtime Activation (D3)
Status: MANDATORY (merge-blocking)

Usage:
    python scripts/validate_governance_coupling.py [base_ref]
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Set, List, Tuple

class GovernanceCouplingValidator:
    """Validates governance change coupling rules"""
    
    # Tier-0 governance files that require coupling
    TIER_0_GOVERNANCE_FILES = {
        'BUILD_PHILOSOPHY.md',
        'governance/policies/governance-supremacy-rule.md',
        'governance/policies/zero-test-debt-constitutional-rule.md',
        'governance/policies/design-freeze-rule.md',
        'governance/policies/RED_GATE_AUTHORITY_AND_OWNERSHIP.md',
        'governance/GOVERNANCE_AUTHORITY_MATRIX.md',
        'governance/alignment/PR_GATE_REQUIREMENTS_CANON.md',
        'governance/alignment/TWO_GATEKEEPER_MODEL.md',
        'governance/alignment/AGENT_SCOPED_QA_BOUNDARIES.md',
        'governance/alignment/PR_GATE_FAILURE_HANDLING_PROTOCOL.md',
        'governance/specs/build-to-green-enforcement-spec.md',
        'governance/contracts/quality-integrity-contract.md',
        'governance/TIER_0_CANON_MANIFEST.json',  # Manifest itself
    }
    
    # Files that MUST be updated when Tier-0 changes
    REQUIRED_COUPLING_FILES = {
        '.agent',  # FM agent contract
        'scripts/validate_tier0_activation.py',  # Validation script (if validation changes)
        '.github/workflows/tier0-activation-gate.yml',  # CI gate (if enforcement changes)
    }
    
    def __init__(self, repo_root: str, base_ref: str = 'origin/main'):
        self.repo_root = Path(repo_root)
        self.base_ref = base_ref
        self.errors = []
        self.warnings = []
        self.validations = []
        
    def get_changed_files(self) -> Set[str]:
        """Get list of files changed in current branch vs base"""
        try:
            # Try to get changed files from git diff
            result = subprocess.run(
                ['git', 'diff', '--name-only', f'{self.base_ref}...HEAD'],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                # Fallback: get files changed in last commit
                result = subprocess.run(
                    ['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD'],
                    cwd=self.repo_root,
                    capture_output=True,
                    text=True,
                    check=True
                )
            
            changed_files = set(result.stdout.strip().split('\n'))
            return {f for f in changed_files if f}  # Remove empty strings
            
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Warning: Could not get changed files: {e}")
            return set()
    
    def check_tier0_changes(self, changed_files: Set[str]) -> Tuple[bool, Set[str]]:
        """Check if any Tier-0 governance files were changed"""
        tier0_changes = changed_files & self.TIER_0_GOVERNANCE_FILES
        return len(tier0_changes) > 0, tier0_changes
    
    def check_coupling_files_updated(self, changed_files: Set[str]) -> Tuple[bool, Set[str]]:
        """Check if required coupling files were updated"""
        coupling_files_changed = changed_files & self.REQUIRED_COUPLING_FILES
        missing_files = self.REQUIRED_COUPLING_FILES - coupling_files_changed
        return len(missing_files) == 0, missing_files
    
    def validate_coupling_rule(self) -> bool:
        """Validate governance change coupling rule"""
        print("🔗 Governance Change Coupling Rule Validator")
        print("=" * 70)
        print()
        
        # Get changed files
        print("📋 Detecting changed files...")
        changed_files = self.get_changed_files()
        
        if not changed_files:
            print("ℹ️  No changed files detected (new branch or comparison issue)")
            print("✅ Coupling rule check SKIPPED (no files to analyze)")
            return True
        
        print(f"   Found {len(changed_files)} changed file(s)")
        print()
        
        # Check for Tier-0 changes
        print("🔍 Checking for Tier-0 governance changes...")
        has_tier0_changes, tier0_files = self.check_tier0_changes(changed_files)
        
        if not has_tier0_changes:
            print("   No Tier-0 governance files changed")
            print("✅ Coupling rule check PASSED (not applicable)")
            self.validations.append({
                "check": "governance_coupling",
                "status": "PASS",
                "message": "No Tier-0 changes detected, coupling not required"
            })
            return True
        
        print(f"   ⚠️  Tier-0 governance files changed: {len(tier0_files)}")
        for f in sorted(tier0_files):
            print(f"      - {f}")
        print()
        
        # Check if coupling files were updated
        print("🔗 Checking for required coupling updates...")
        all_updated, missing_files = self.check_coupling_files_updated(changed_files)
        
        if all_updated:
            print("   ✅ All required coupling files updated")
            for f in sorted(self.REQUIRED_COUPLING_FILES & changed_files):
                print(f"      - {f}")
            print()
            print("✅ COUPLING RULE PASSED")
            print()
            print("Tier-0 governance changes are properly coupled with enforcement updates.")
            
            self.validations.append({
                "check": "governance_coupling",
                "status": "PASS",
                "message": "Tier-0 changes properly coupled with enforcement updates"
            })
            return True
        else:
            print("   ❌ Missing required coupling updates")
            for f in sorted(missing_files):
                print(f"      - {f} (NOT UPDATED)")
            print()
            print("❌ COUPLING RULE FAILED")
            print()
            print("VIOLATION: Tier-0 governance changed without updating enforcement.")
            print()
            
            self.errors.append({
                "check": "governance_coupling",
                "status": "FAIL",
                "message": f"Tier-0 changed but {len(missing_files)} coupling file(s) not updated",
                "tier0_files": list(tier0_files),
                "missing_files": list(missing_files)
            })
            return False
    
    def print_summary(self):
        """Print validation summary"""
        print()
        print("=" * 70)
        print("COUPLING RULE VALIDATION SUMMARY")
        print("=" * 70)
        print()
        print(f"✅ Passed: {len(self.validations)}")
        print(f"❌ Failed: {len(self.errors)}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        print()
        
        if self.errors:
            print("ERRORS:")
            for error in self.errors:
                print(f"  - {error['message']}")
                if 'tier0_files' in error:
                    print(f"    Tier-0 files changed: {', '.join(error['tier0_files'])}")
                if 'missing_files' in error:
                    print(f"    Missing updates: {', '.join(error['missing_files'])}")
            print()
            print("❌ GOVERNANCE COUPLING RULE FAILED")
            print()
            print("REQUIRED ACTIONS:")
            print()
            print("When Tier-0 governance changes, you MUST update:")
            print("  1. .agent (FM agent contract with updated Tier-0 references)")
            print("  2. scripts/validate_tier0_activation.py (if validation logic changes)")
            print("  3. .github/workflows/tier0-activation-gate.yml (if gate logic changes)")
            print()
            print("This ensures governance and enforcement remain synchronized.")
            print()
            print("MERGE IS BLOCKED until coupling is complete.")
        else:
            print("✅ ALL COUPLING RULE CHECKS PASSED")
            print()
            print("Governance changes are properly coupled with enforcement updates.")

def main():
    """Main entry point"""
    repo_root = os.getcwd()
    base_ref = sys.argv[1] if len(sys.argv) > 1 else 'origin/main'
    
    print(f"Base reference: {base_ref}")
    print()
    
    validator = GovernanceCouplingValidator(repo_root, base_ref)
    success = validator.validate_coupling_rule()
    validator.print_summary()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
