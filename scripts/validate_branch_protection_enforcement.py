#!/usr/bin/env python3
"""
Branch Protection Enforcement Validator

Purpose: Validates that required CI checks are configured in branch protection.
         This is a TIER-0 INVARIANT - missing checks is a CATASTROPHIC failure.

Constitutional Authority:
- governance/TIER_0_CANON_MANIFEST.json - branch_protection_enforcement section
- BUILD_PHILOSOPHY.md - Zero Regression Guarantee
- Issue: Enforce Branch Protection as Tier-0 Governance Invariant

Version: 1.0.0
Date: 2026-01-01

Usage:
    python scripts/validate_branch_protection_enforcement.py [--repo REPO] [--branch BRANCH]
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


class BranchProtectionEnforcementValidator:
    """Validates branch protection enforcement as Tier-0 invariant"""
    
    MANIFEST_PATH = "governance/TIER_0_CANON_MANIFEST.json"
    
    def __init__(self, repo: str, branch: str = "main"):
        self.repo = repo
        self.branch = branch
        self.manifest = None
        self.required_checks = []
        self.errors = []
        self.validations = []
        self.diagnostic_output = []
        
    def validate(self) -> bool:
        """Run all branch protection enforcement validations"""
        print("🔒 Branch Protection Enforcement Validator v1.0")
        print("=" * 70)
        print(f"Repository: {self.repo}")
        print(f"Branch: {self.branch}")
        print()
        
        success = True
        
        # Step 1: Load Tier-0 manifest
        if not self._load_manifest():
            return False
        
        # Step 2: Extract required checks
        if not self._extract_required_checks():
            return False
        
        # Step 3: Verify branch protection exists
        if not self._verify_branch_protection_exists():
            success = False
        
        # Step 4: Verify required checks are configured
        if success and not self._verify_required_checks_configured():
            success = False
        
        # Step 5: Print results
        self._print_results()
        
        return success
    
    def _load_manifest(self) -> bool:
        """Load Tier-0 canonical manifest"""
        manifest_file = Path(self.MANIFEST_PATH)
        
        if not manifest_file.exists():
            self._add_error(
                "CATASTROPHIC",
                "manifest_missing",
                f"Tier-0 manifest not found: {self.MANIFEST_PATH}"
            )
            return False
        
        try:
            with open(manifest_file, 'r') as f:
                self.manifest = json.load(f)
            
            self._add_validation("manifest_loaded", "Tier-0 manifest loaded successfully")
            return True
            
        except Exception as e:
            self._add_error(
                "CATASTROPHIC",
                "manifest_load_error",
                f"Error loading manifest: {str(e)}"
            )
            return False
    
    def _extract_required_checks(self) -> bool:
        """Extract required CI checks from manifest"""
        if not self.manifest:
            return False
        
        bp_enforcement = self.manifest.get('branch_protection_enforcement', {})
        
        if not bp_enforcement:
            self._add_error(
                "CATASTROPHIC",
                "bp_enforcement_missing",
                "branch_protection_enforcement section missing from manifest"
            )
            return False
        
        self.required_checks = bp_enforcement.get('required_ci_checks', [])
        
        if not self.required_checks:
            self._add_error(
                "CATASTROPHIC",
                "no_required_checks",
                "No required CI checks defined in manifest"
            )
            return False
        
        self._add_validation(
            "required_checks_extracted",
            f"Extracted {len(self.required_checks)} required CI checks"
        )
        
        print(f"Required CI Checks ({len(self.required_checks)}):")
        for check in self.required_checks:
            print(f"  - [{check['id']}] {check['check_name']}")
        print()
        
        return True
    
    def _verify_branch_protection_exists(self) -> bool:
        """Verify that branch protection is enabled"""
        print(f"Verifying branch protection on '{self.branch}'...")
        
        # Try to use GitHub CLI
        if not self._has_github_cli():
            self._add_error(
                "CATASTROPHIC",
                "no_verification_method",
                "GitHub CLI not available - cannot verify branch protection"
            )
            self._add_diagnostic(
                "VERIFICATION_FAILURE",
                "GitHub CLI (gh) is required but not available",
                "Install gh CLI or ensure it's in PATH"
            )
            return False
        
        try:
            # Query branch protection
            cmd = [
                "gh", "api",
                f"/repos/{self.repo}/branches/{self.branch}/protection",
                "--silent"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Branch protection exists
                protection_data = json.loads(result.stdout)
                self._add_validation(
                    "branch_protection_exists",
                    f"Branch protection enabled on '{self.branch}'"
                )
                
                # Store for later verification
                self.protection_data = protection_data
                return True
                
            elif result.returncode == 404:
                # Branch protection not configured
                self._add_error(
                    "CATASTROPHIC",
                    "branch_protection_disabled",
                    f"Branch protection NOT enabled on '{self.branch}'"
                )
                self._add_diagnostic(
                    "BRANCH_PROTECTION_MISSING",
                    f"Branch '{self.branch}' has no protection rules configured",
                    "Configure branch protection in GitHub repository settings"
                )
                return False
                
            else:
                # Error querying
                self._add_error(
                    "CATASTROPHIC",
                    "verification_error",
                    f"Error querying branch protection: {result.stderr}"
                )
                self._add_diagnostic(
                    "API_ERROR",
                    f"GitHub API returned error: {result.stderr}",
                    "Check GitHub token permissions and API access"
                )
                return False
        
        except subprocess.TimeoutExpired:
            self._add_error(
                "CATASTROPHIC",
                "verification_timeout",
                "Timeout querying GitHub API"
            )
            return False
            
        except Exception as e:
            self._add_error(
                "CATASTROPHIC",
                "verification_exception",
                f"Exception during verification: {str(e)}"
            )
            return False
    
    def _verify_required_checks_configured(self) -> bool:
        """Verify that all required checks are configured in branch protection"""
        print("\nVerifying required CI checks are configured...")
        
        if not hasattr(self, 'protection_data'):
            self._add_error(
                "CATASTROPHIC",
                "no_protection_data",
                "No protection data available for verification"
            )
            return False
        
        # Extract configured status checks
        status_checks = self.protection_data.get('required_status_checks', {})
        
        if not status_checks:
            self._add_error(
                "CATASTROPHIC",
                "no_status_checks",
                "No required status checks configured in branch protection"
            )
            self._add_diagnostic(
                "MISSING_STATUS_CHECKS",
                "Branch protection exists but has no required status checks",
                "Add required status checks to branch protection settings"
            )
            return False
        
        # Get list of configured check contexts
        configured_checks = status_checks.get('contexts', [])
        
        if not configured_checks:
            self._add_error(
                "CATASTROPHIC",
                "no_check_contexts",
                "No status check contexts configured"
            )
            return False
        
        print(f"Configured status checks: {len(configured_checks)}")
        for check in configured_checks:
            print(f"  ✓ {check}")
        print()
        
        # Verify each required check
        all_present = True
        missing_checks = []
        
        for required_check in self.required_checks:
            check_id = required_check['id']
            check_name = required_check['check_name']
            job_name = required_check.get('job_name', '')
            
            # Check if this check is configured
            # For CI workflows, the check name in GitHub is typically the job name
            found = False
            
            # Try different matching strategies
            for configured in configured_checks:
                if job_name and job_name.lower() in configured.lower():
                    found = True
                    break
                if check_name.lower() in configured.lower():
                    found = True
                    break
            
            if found:
                self._add_validation(
                    f"check_{check_id}_configured",
                    f"[{check_id}] {check_name}: CONFIGURED"
                )
                print(f"  ✅ [{check_id}] {check_name}")
            else:
                # Special case for code review closure (contractual enforcement)
                if check_id == "BP-003":
                    self._add_validation(
                        f"check_{check_id}_configured",
                        f"[{check_id}] {check_name}: CONTRACTUAL (via .agent)"
                    )
                    print(f"  ✅ [{check_id}] {check_name} (contractual)")
                else:
                    all_present = False
                    missing_checks.append(required_check)
                    self._add_error(
                        "CATASTROPHIC",
                        f"check_{check_id}_missing",
                        f"[{check_id}] {check_name}: NOT CONFIGURED"
                    )
                    print(f"  ❌ [{check_id}] {check_name}")
                    
                    self._add_diagnostic(
                        f"MISSING_REQUIRED_CHECK_{check_id}",
                        f"Required CI check '{check_name}' (job: {job_name}) is not configured in branch protection",
                        f"Add '{job_name}' to required status checks in GitHub branch protection settings"
                    )
        
        if not all_present:
            print()
            print(f"❌ FAILURE: {len(missing_checks)} required check(s) missing from branch protection")
            return False
        
        print()
        print(f"✅ SUCCESS: All {len(self.required_checks)} required checks are configured")
        return True
    
    def _has_github_cli(self) -> bool:
        """Check if GitHub CLI is available"""
        try:
            result = subprocess.run(
                ["gh", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def _add_error(self, severity: str, error_type: str, message: str):
        """Add an error to the error list"""
        self.errors.append({
            "severity": severity,
            "type": error_type,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
    
    def _add_validation(self, check: str, message: str):
        """Add a validation to the validation list"""
        self.validations.append({
            "check": check,
            "status": "PASS",
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
    
    def _add_diagnostic(self, category: str, problem: str, solution: str):
        """Add diagnostic output"""
        self.diagnostic_output.append({
            "category": category,
            "problem": problem,
            "solution": solution
        })
    
    def _print_results(self):
        """Print validation results"""
        print()
        print("=" * 70)
        print("VALIDATION RESULTS")
        print("=" * 70)
        print()
        print(f"✅ Validations Passed: {len(self.validations)}")
        print(f"❌ Errors: {len(self.errors)}")
        print()
        
        if self.errors:
            print("ERRORS:")
            for error in self.errors:
                print(f"  [{error['severity']}] {error['message']}")
            print()
        
        if self.diagnostic_output:
            print("DIAGNOSTIC OUTPUT:")
            print()
            for diag in self.diagnostic_output:
                print(f"  Category: {diag['category']}")
                print(f"  Problem:  {diag['problem']}")
                print(f"  Solution: {diag['solution']}")
                print()
        
        if self.errors:
            print("=" * 70)
            print("❌ CATASTROPHIC FAILURE")
            print("=" * 70)
            print()
            print("Branch protection enforcement validation FAILED.")
            print("Required CI checks are NOT properly configured.")
            print()
            print("This is a TIER-0 INVARIANT violation.")
            print("Absence of required checks is a SYSTEM FAILURE.")
            print()
            print("🚨 ESCALATION REQUIRED: Johan Ras must be notified.")
            print()
            print("FM runtime MUST NOT proceed until this is resolved.")
        else:
            print("=" * 70)
            print("✅ VALIDATION SUCCESS")
            print("=" * 70)
            print()
            print("All required CI checks are properly configured.")
            print("Branch protection enforcement is VALID.")
            print("FM runtime may proceed.")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Validate branch protection enforcement (Tier-0 invariant)"
    )
    parser.add_argument(
        "--repo",
        default=os.environ.get("GITHUB_REPOSITORY", "MaturionISMS/maturion-foreman-office-app"),
        help="Repository in owner/repo format"
    )
    parser.add_argument(
        "--branch",
        default="main",
        help="Branch to verify"
    )
    
    args = parser.parse_args()
    
    validator = BranchProtectionEnforcementValidator(args.repo, args.branch)
    success = validator.validate()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
