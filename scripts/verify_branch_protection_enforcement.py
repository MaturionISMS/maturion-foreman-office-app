#!/usr/bin/env python3
"""
Branch Protection Enforcement Verification Script

This script verifies that required CI checks are enforced via GitHub branch protection.
This is a TIER-0 GOVERNANCE INVARIANT that MUST be satisfied before FM runtime can proceed.

If any required check is missing from branch protection, execution STOPS with ESCALATION.

Version: 1.0.0
Authority: Tier-0 Governance Invariant (CATASTROPHIC severity)
Status: MANDATORY (execution-blocking)

Usage:
    python scripts/verify_branch_protection_enforcement.py [--repo REPO] [--branch BRANCH]
"""

import os
import sys
import json
import subprocess
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime

class BranchProtectionEnforcementVerifier:
    """Verifies that required CI checks are enforced via branch protection."""
    
    MANIFEST_PATH = "governance/TIER_0_CANON_MANIFEST.json"
    
    def __init__(self, repo_root: str, repo: str = None, branch: str = "main"):
        self.repo_root = Path(repo_root)
        self.repo = repo or os.environ.get("GITHUB_REPOSITORY")
        if not self.repo:
            raise ValueError("Repository must be specified via --repo argument or GITHUB_REPOSITORY environment variable")
        self.branch = branch
        self.errors = []
        self.warnings = []
        self.validations = []
        self.manifest = None
        self.required_checks = []
        self.actual_checks = []
        
    def load_manifest(self) -> bool:
        """Load the Tier-0 canonical manifest"""
        manifest_file = self.repo_root / self.MANIFEST_PATH
        
        if not manifest_file.exists():
            self.errors.append({
                "check": "manifest_exists",
                "status": "FAIL",
                "message": f"Tier-0 manifest not found: {self.MANIFEST_PATH}"
            })
            print(f"❌ FAIL: Tier-0 manifest not found: {self.MANIFEST_PATH}")
            return False
        
        try:
            with open(manifest_file, 'r') as f:
                self.manifest = json.load(f)
            
            self.validations.append({
                "check": "manifest_exists",
                "status": "PASS",
                "message": "Tier-0 manifest loaded successfully"
            })
            print("✅ PASS: Tier-0 manifest loaded successfully")
            return True
            
        except Exception as e:
            self.errors.append({
                "check": "manifest_exists",
                "status": "FAIL",
                "message": f"Error loading manifest: {str(e)}"
            })
            print(f"❌ FAIL: Error loading manifest: {str(e)}")
            return False
    
    def extract_required_checks(self) -> bool:
        """Extract required checks from manifest"""
        if not self.manifest:
            return False
        
        branch_protection = self.manifest.get('branch_protection_enforcement', {})
        
        if not branch_protection:
            self.errors.append({
                "check": "required_checks_defined",
                "status": "FAIL",
                "message": "Branch protection enforcement section not found in manifest"
            })
            print("❌ FAIL: Branch protection enforcement section not found in manifest")
            return False
        
        self.required_checks = branch_protection.get('required_checks', [])
        
        if not self.required_checks:
            self.errors.append({
                "check": "required_checks_defined",
                "status": "FAIL",
                "message": "No required checks defined in manifest"
            })
            print("❌ FAIL: No required checks defined in manifest")
            return False
        
        self.validations.append({
            "check": "required_checks_defined",
            "status": "PASS",
            "message": f"{len(self.required_checks)} required checks defined"
        })
        print(f"✅ PASS: {len(self.required_checks)} required checks defined")
        
        print("\n📋 Required Checks:")
        for check in self.required_checks:
            print(f"  - {check['check_name']} (ID: {check['id']})")
        
        return True
    
    def fetch_branch_protection(self) -> bool:
        """Fetch branch protection configuration from GitHub"""
        print(f"\n🔍 Fetching branch protection for {self.repo}:{self.branch}...")
        
        # Check if GitHub CLI is available
        if not self._has_github_cli():
            self.warnings.append({
                "check": "github_cli_available",
                "status": "WARN",
                "message": "GitHub CLI (gh) not available, attempting fallback"
            })
            print("⚠️  GitHub CLI (gh) not available")
            
            # Try direct API call with token
            if not self._fetch_via_api():
                self.errors.append({
                    "check": "fetch_branch_protection",
                    "status": "FAIL",
                    "message": "Cannot fetch branch protection: no GitHub CLI and API call failed"
                })
                print("❌ FAIL: Cannot fetch branch protection")
                return False
            return True
        
        # Use GitHub CLI
        return self._fetch_via_cli()
    
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
    
    def _fetch_via_cli(self) -> bool:
        """Fetch branch protection using GitHub CLI"""
        try:
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
                protection_data = json.loads(result.stdout)
                return self._extract_required_status_checks(protection_data)
            elif result.returncode == 404:
                self.errors.append({
                    "check": "branch_protection_enabled",
                    "status": "FAIL",
                    "message": f"Branch protection not enabled for {self.branch}"
                })
                print(f"❌ FAIL: Branch protection not enabled for {self.branch}")
                return False
            else:
                self.errors.append({
                    "check": "fetch_branch_protection",
                    "status": "FAIL",
                    "message": f"GitHub API error: {result.stderr}"
                })
                print(f"❌ FAIL: GitHub API error: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.errors.append({
                "check": "fetch_branch_protection",
                "status": "FAIL",
                "message": "Timeout querying GitHub API"
            })
            print("❌ FAIL: Timeout querying GitHub API")
            return False
        except Exception as e:
            self.errors.append({
                "check": "fetch_branch_protection",
                "status": "FAIL",
                "message": f"Error: {str(e)}"
            })
            print(f"❌ FAIL: Error: {str(e)}")
            return False
    
    def _fetch_via_api(self) -> bool:
        """Fetch branch protection using direct API call"""
        # Check for GitHub token
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        
        if not token:
            self.errors.append({
                "check": "github_token_available",
                "status": "FAIL",
                "message": "No GitHub token available (GITHUB_TOKEN or GH_TOKEN)"
            })
            print("❌ FAIL: No GitHub token available")
            return False
        
        try:
            url = f"https://api.github.com/repos/{self.repo}/branches/{self.branch}/protection"
            
            req = urllib.request.Request(url)
            req.add_header("Authorization", f"Bearer {token}")
            req.add_header("Accept", "application/vnd.github+json")
            req.add_header("X-GitHub-Api-Version", "2022-11-28")
            
            with urllib.request.urlopen(req, timeout=30) as response:
                protection_data = json.loads(response.read().decode())
                return self._extract_required_status_checks(protection_data)
                
        except urllib.error.HTTPError as e:
            if e.code == 404:
                self.errors.append({
                    "check": "branch_protection_enabled",
                    "status": "FAIL",
                    "message": f"Branch protection not enabled for {self.branch}"
                })
                print(f"❌ FAIL: Branch protection not enabled for {self.branch}")
            else:
                self.errors.append({
                    "check": "fetch_branch_protection",
                    "status": "FAIL",
                    "message": f"GitHub API error: {e.code} {e.reason}"
                })
                print(f"❌ FAIL: GitHub API error: {e.code} {e.reason}")
            return False
        except Exception as e:
            self.errors.append({
                "check": "fetch_branch_protection",
                "status": "FAIL",
                "message": f"Error: {str(e)}"
            })
            print(f"❌ FAIL: Error: {str(e)}")
            return False
    
    def _extract_required_status_checks(self, protection_data: Dict[str, Any]) -> bool:
        """Extract required status checks from protection data"""
        if "required_status_checks" not in protection_data or not protection_data["required_status_checks"]:
            self.errors.append({
                "check": "status_checks_configured",
                "status": "FAIL",
                "message": "No required status checks configured"
            })
            print("❌ FAIL: No required status checks configured")
            return False
        
        # Extract check contexts/names
        checks_data = protection_data["required_status_checks"]
        
        # GitHub API v3 uses 'contexts' field for status checks
        # GitHub API when using GitHub Apps uses 'checks' field with check runs
        if "contexts" in checks_data:
            self.actual_checks = checks_data["contexts"]
        elif "checks" in checks_data:
            # When using GitHub Apps check runs, extract context name
            self.actual_checks = [check.get("context", check.get("name", "")) for check in checks_data["checks"]]
        else:
            self.actual_checks = []
        
        if not self.actual_checks:
            self.errors.append({
                "check": "status_checks_configured",
                "status": "FAIL",
                "message": "Required status checks section exists but is empty"
            })
            print("❌ FAIL: Required status checks section exists but is empty")
            return False
        
        self.validations.append({
            "check": "status_checks_configured",
            "status": "PASS",
            "message": f"{len(self.actual_checks)} status checks configured"
        })
        print(f"✅ PASS: {len(self.actual_checks)} status checks configured")
        
        print("\n📋 Configured Checks:")
        for check in self.actual_checks:
            print(f"  - {check}")
        
        return True
    
    def verify_required_checks_enforced(self) -> bool:
        """Verify that all required checks are enforced"""
        print("\n🔍 Verifying required checks are enforced...")
        
        missing_checks = []
        
        for required_check in self.required_checks:
            check_name = required_check['check_name']
            
            if check_name not in self.actual_checks:
                missing_checks.append(required_check)
                self.errors.append({
                    "check": "required_check_enforced",
                    "check_id": required_check['id'],
                    "check_name": check_name,
                    "status": "FAIL",
                    "message": f"Required check not enforced: {check_name}"
                })
                print(f"  ❌ MISSING: {check_name} (ID: {required_check['id']})")
            else:
                self.validations.append({
                    "check": "required_check_enforced",
                    "check_id": required_check['id'],
                    "check_name": check_name,
                    "status": "PASS",
                    "message": f"Required check enforced: {check_name}"
                })
                print(f"  ✅ ENFORCED: {check_name} (ID: {required_check['id']})")
        
        if missing_checks:
            print("\n❌ VERIFICATION FAILED")
            print(f"\n{len(missing_checks)} required check(s) NOT enforced via branch protection:")
            for check in missing_checks:
                print(f"  - {check['check_name']} (ID: {check['id']})")
                print(f"    Purpose: {check['purpose']}")
                print(f"    Workflow: {check['workflow_file']}")
            return False
        
        print("\n✅ All required checks are enforced")
        return True
    
    def validate_all(self) -> bool:
        """Run all verification checks"""
        print("🔒 Branch Protection Enforcement Verifier (Tier-0 Invariant)")
        print("=" * 70)
        print()
        
        success = True
        
        # Check 1: Load manifest
        if not self.load_manifest():
            success = False
            self.print_summary()
            return False
        
        # Check 2: Extract required checks
        if not self.extract_required_checks():
            success = False
            self.print_summary()
            return False
        
        # Check 3: Fetch branch protection
        if not self.fetch_branch_protection():
            success = False
            self.print_summary()
            return False
        
        # Check 4: Verify required checks are enforced
        if not self.verify_required_checks_enforced():
            success = False
        
        # Print summary
        print()
        print("=" * 70)
        self.print_summary()
        
        return success
    
    def print_summary(self):
        """Print validation summary"""
        print("VALIDATION SUMMARY")
        print("=" * 70)
        print()
        print(f"Repository: {self.repo}")
        print(f"Branch: {self.branch}")
        print()
        print(f"✅ Passed: {len(self.validations)}")
        print(f"❌ Failed: {len(self.errors)}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        print()
        
        if self.errors:
            print("ERRORS:")
            for error in self.errors:
                print(f"  - {error['message']}")
            print()
            print("❌ BRANCH PROTECTION ENFORCEMENT VERIFICATION FAILED")
            print()
            print("CATASTROPHIC: Required CI checks are not enforced via branch protection.")
            print()
            print("This is a TIER-0 GOVERNANCE INVARIANT violation.")
            print()
            print("IMPACT:")
            print("  - FM runtime CANNOT proceed")
            print("  - Execution STOPPED")
            print("  - Manual intervention REQUIRED")
            print()
            print("REQUIRED ACTIONS:")
            print()
            print(f"1. Navigate to: https://github.com/{self.repo}/settings/branches")
            print(f"2. Edit branch protection rule for '{self.branch}'")
            print("3. Enable 'Require status checks to pass before merging'")
            print("4. Add the following required status checks:")
            for check in self.required_checks:
                print(f"   - {check['check_name']}")
            print("5. Save branch protection settings")
            print("6. Re-run this verification")
            print()
            print("ESCALATION REQUIRED: Johan Ras must be notified")
            print()
            print("Authority: governance/TIER_0_CANON_MANIFEST.json")
            print("Enforcement Level: TIER-0 INVARIANT")
        else:
            print("✅ ALL CHECKS PASSED")
            print()
            print("Branch protection enforcement is VALID.")
            print("All required CI checks are properly enforced.")
            print("FM runtime may proceed.")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Verify branch protection enforcement (Tier-0 Invariant)"
    )
    parser.add_argument(
        "--repo",
        default=None,
        help="Repository in owner/repo format (defaults to GITHUB_REPOSITORY env var)"
    )
    parser.add_argument(
        "--branch",
        default="main",
        help="Branch to verify (default: main)"
    )
    
    args = parser.parse_args()
    
    repo_root = os.getcwd()
    
    verifier = BranchProtectionEnforcementVerifier(
        repo_root,
        repo=args.repo,
        branch=args.branch
    )
    
    success = verifier.validate_all()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
