"""
FM Runtime Initialization Module

Purpose: Validates Tier-0 invariants before FM runtime execution begins.
         This includes branch protection enforcement verification.

Constitutional Authority:
- governance/TIER_0_CANON_MANIFEST.json
- BUILD_PHILOSOPHY.md - Zero Regression Guarantee
- Issue: Enforce Branch Protection as Tier-0 Governance Invariant

Version: 1.0.0
Date: 2026-01-01
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional


class Tier0RuntimeValidator:
    """Validates Tier-0 invariants at runtime initialization"""
    
    def __init__(self, repo: str = None, branch: str = "main"):
        self.repo = repo or os.environ.get("GITHUB_REPOSITORY", "MaturionISMS/maturion-foreman-office-app")
        self.branch = branch
        self.validation_results = {
            "tier0_validation": False,
            "branch_protection_enforcement": False,
            "errors": [],
            "stop_required": False,
            "escalation_required": False
        }
    
    def validate_all(self) -> bool:
        """
        Validate all Tier-0 invariants.
        
        Returns:
            True if all validations pass, False otherwise
        """
        print("=" * 70)
        print("FM RUNTIME INITIALIZATION - TIER-0 VALIDATION")
        print("=" * 70)
        print()
        
        success = True
        
        # Validation 1: Branch Protection Enforcement
        if not self._validate_branch_protection_enforcement():
            success = False
            self.validation_results["stop_required"] = True
            self.validation_results["escalation_required"] = True
        
        # Store overall result
        self.validation_results["tier0_validation"] = success
        
        # Print results
        self._print_results()
        
        return success
    
    def _validate_branch_protection_enforcement(self) -> bool:
        """
        Validate branch protection enforcement (Tier-0 invariant).
        
        This is a CATASTROPHIC check - failure means STOP + ESCALATE.
        """
        print("🔒 Validating Branch Protection Enforcement (Tier-0 Invariant)...")
        print()
        
        # Run the validation script
        script_path = Path(__file__).parent.parent.parent / "scripts" / "validate_branch_protection_enforcement.py"
        
        if not script_path.exists():
            error = {
                "severity": "CATASTROPHIC",
                "component": "branch_protection_enforcement",
                "message": "Branch protection enforcement validator not found",
                "diagnostic": f"Expected script at: {script_path}",
                "action": "STOP + ESCALATE"
            }
            self.validation_results["errors"].append(error)
            
            print(f"❌ CATASTROPHIC: Validator script not found")
            print(f"   Expected: {script_path}")
            print()
            return False
        
        try:
            # Run validator
            result = subprocess.run(
                [sys.executable, str(script_path), "--repo", self.repo, "--branch", self.branch],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                # Validation passed
                self.validation_results["branch_protection_enforcement"] = True
                print("✅ Branch protection enforcement: VALID")
                print()
                return True
            else:
                # Validation failed
                error = {
                    "severity": "CATASTROPHIC",
                    "component": "branch_protection_enforcement",
                    "message": "Required CI checks not configured in branch protection",
                    "diagnostic": result.stdout,
                    "action": "STOP + ESCALATE"
                }
                self.validation_results["errors"].append(error)
                
                print("❌ CATASTROPHIC: Branch protection enforcement validation FAILED")
                print()
                print("Output:")
                print(result.stdout)
                if result.stderr:
                    print("\nErrors:")
                    print(result.stderr)
                print()
                return False
                
        except subprocess.TimeoutExpired:
            error = {
                "severity": "CATASTROPHIC",
                "component": "branch_protection_enforcement",
                "message": "Branch protection validation timed out",
                "diagnostic": "Validation script exceeded 60 second timeout",
                "action": "STOP + ESCALATE"
            }
            self.validation_results["errors"].append(error)
            
            print("❌ CATASTROPHIC: Validation timed out")
            print()
            return False
            
        except Exception as e:
            error = {
                "severity": "CATASTROPHIC",
                "component": "branch_protection_enforcement",
                "message": f"Exception during validation: {str(e)}",
                "diagnostic": "Unexpected error running validator",
                "action": "STOP + ESCALATE"
            }
            self.validation_results["errors"].append(error)
            
            print(f"❌ CATASTROPHIC: Validation exception: {str(e)}")
            print()
            return False
    
    def _print_results(self):
        """Print validation results and determine action"""
        print("=" * 70)
        print("TIER-0 VALIDATION RESULTS")
        print("=" * 70)
        print()
        
        if self.validation_results["tier0_validation"]:
            print("✅ STATUS: ALL TIER-0 VALIDATIONS PASSED")
            print()
            print("FM runtime may proceed with execution.")
            print()
        else:
            print("❌ STATUS: TIER-0 VALIDATION FAILED")
            print()
            print(f"Errors: {len(self.validation_results['errors'])}")
            print()
            
            for error in self.validation_results["errors"]:
                print(f"[{error['severity']}] {error['component']}")
                print(f"  Message: {error['message']}")
                print(f"  Action:  {error['action']}")
                print()
            
            if self.validation_results["stop_required"]:
                print("=" * 70)
                print("🛑 STOP EXECUTION")
                print("=" * 70)
                print()
                print("FM runtime MUST NOT proceed.")
                print("Tier-0 invariants are violated.")
                print()
            
            if self.validation_results["escalation_required"]:
                print("🚨 ESCALATION REQUIRED")
                print()
                print("Target: Johan Ras")
                print("Reason: Tier-0 invariant violation (branch protection)")
                print()
                print("Required CI checks are not configured in branch protection.")
                print("This is a system failure that must be resolved before execution.")
                print()
    
    def get_validation_results(self) -> Dict[str, Any]:
        """Get validation results for external use"""
        return self.validation_results


def initialize_fm_runtime(repo: str = None, branch: str = "main") -> bool:
    """
    Initialize FM runtime with Tier-0 validation.
    
    This function MUST be called before any FM runtime execution begins.
    If it returns False, execution MUST NOT proceed.
    
    Args:
        repo: Repository in owner/repo format (default: from GITHUB_REPOSITORY env)
        branch: Branch to validate (default: main)
    
    Returns:
        True if initialization succeeds, False if STOP required
    """
    validator = Tier0RuntimeValidator(repo, branch)
    success = validator.validate_all()
    
    if not success:
        print()
        print("=" * 70)
        print("INITIALIZATION FAILED - CANNOT PROCEED")
        print("=" * 70)
        print()
    
    return success


# Entry point for standalone execution
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="FM Runtime Tier-0 Initialization and Validation"
    )
    parser.add_argument(
        "--repo",
        default=os.environ.get("GITHUB_REPOSITORY"),
        help="Repository in owner/repo format"
    )
    parser.add_argument(
        "--branch",
        default="main",
        help="Branch to validate"
    )
    
    args = parser.parse_args()
    
    success = initialize_fm_runtime(args.repo, args.branch)
    sys.exit(0 if success else 1)
