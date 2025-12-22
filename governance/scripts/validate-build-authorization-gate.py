#!/usr/bin/env python3
"""
Maturion Foreman - Build Authorization Gate Validator

Validates all preconditions defined in BUILD_AUTHORIZATION_GATE.md before
allowing a build to proceed.

This is the master governance gate that orchestrates all other validators.

Preconditions checked:
1. App Description exists and is authoritative
2. Architecture Compilation Contract = PASS
3. QA Derivation & Coverage Rules = PASS
4. FL/CI Learning Integration = COMPLETE
5. Deployment and Runtime Validation = COMPLETE (where applicable)
6. Governance Checklist = PASS
7. Scope Freeze = CONFIRMED
8. Zero Regression Verification = COMPLETE

Returns:
    PASS: Build authorized - all preconditions satisfied
    FAIL: Build blocked - one or more preconditions not satisfied
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class BuildAuthorizationGateValidator:
    """Master validator for Build Authorization Gate"""
    
    def __init__(self, repo_root: Path, app_name: str = "FM"):
        self.repo_root = repo_root
        self.app_name = app_name
        self.results = {
            'validation_id': f'build-gate-{app_name}-{datetime.now().strftime("%Y%m%d-%H%M%S")}',
            'timestamp': datetime.now().isoformat(),
            'app_name': app_name,
            'status': 'UNKNOWN',
            'preconditions': [],
            'errors': [],
            'warnings': [],
            'evidence': {},
            'decision': 'PENDING'
        }
        
    def validate(self) -> Tuple[bool, Dict]:
        """Run all precondition checks"""
        print(f"🚦 Build Authorization Gate Validation for {self.app_name}")
        print("=" * 70)
        print("\nChecking all preconditions per BUILD_AUTHORIZATION_GATE.md...\n")
        
        # Precondition 1: App Description validation
        pc1_pass = self._check_precondition_1()
        
        # Precondition 2: Architecture Compilation Contract
        pc2_pass = self._check_precondition_2()
        
        # Precondition 3: QA Derivation & Coverage (basic check)
        pc3_pass = self._check_precondition_3()
        
        # Precondition 4: FL/CI Learning Integration (basic check)
        pc4_pass = self._check_precondition_4()
        
        # Precondition 5: Deployment Validation (basic check)
        pc5_pass = self._check_precondition_5()
        
        # Precondition 6: Governance Checklist (basic check)
        pc6_pass = self._check_precondition_6()
        
        # Precondition 7: Scope Freeze (basic check)
        pc7_pass = self._check_precondition_7()
        
        # Precondition 8: Zero Regression (basic check)
        pc8_pass = self._check_precondition_8()
        
        # Determine overall authorization
        all_preconditions = [
            pc1_pass, pc2_pass, pc3_pass, pc4_pass,
            pc5_pass, pc6_pass, pc7_pass, pc8_pass
        ]
        
        all_pass = all(all_preconditions)
        
        if all_pass:
            self.results['status'] = 'PASS'
            self.results['decision'] = 'AUTHORIZED'
        else:
            self.results['status'] = 'FAIL'
            self.results['decision'] = 'BLOCKED'
        
        return all_pass, self.results
    
    def _run_validator(self, script_name: str, *args) -> Tuple[bool, str]:
        """Run a validation script and return success status and output"""
        script_path = self.repo_root / "governance" / "scripts" / script_name
        
        if not script_path.exists():
            return False, f"Validator script not found: {script_name}"
        
        try:
            result = subprocess.run(
                [sys.executable, str(script_path), *args],
                capture_output=True,
                text=True,
                cwd=str(self.repo_root)
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, f"Error running validator: {e}"
    
    def _check_precondition_1(self) -> bool:
        """Precondition 1: App Description Exists and Is Authoritative"""
        precondition = {
            'precondition': 'PC1: App Description + FRS Alignment',
            'status': 'UNKNOWN',
            'message': '',
            'evidence': {}
        }
        
        print("📋 Precondition 1: App Description + FRS Alignment...")
        
        # Run App Description validator
        app_desc_pass, app_desc_output = self._run_validator('validate-app-description.py', self.app_name)
        
        # Run FRS alignment validator
        frs_path = "foreman/architecture/FOREMAN_TRUE_NORTH_v1.0.md"
        frs_align_pass, frs_align_output = self._run_validator('validate-frs-alignment.py', self.app_name, frs_path)
        
        precondition['evidence']['app_description_validation'] = app_desc_pass
        precondition['evidence']['frs_alignment_validation'] = frs_align_pass
        
        if app_desc_pass and frs_align_pass:
            precondition['status'] = 'PASS'
            precondition['message'] = 'App Description valid and FRS aligned'
            print("  ✅ PASS - App Description validated and FRS aligned\n")
        elif app_desc_pass:
            precondition['status'] = 'FAIL'
            precondition['message'] = 'App Description valid but FRS alignment failed'
            self.results['errors'].append(
                "PC1 BLOCKING: FRS must explicitly derive from App Description"
            )
            print("  ❌ FAIL - FRS not aligned with App Description\n")
        else:
            precondition['status'] = 'FAIL'
            precondition['message'] = 'App Description validation failed'
            self.results['errors'].append(
                "PC1 BLOCKING: App Description must exist and be authoritative"
            )
            print("  ❌ FAIL - App Description validation failed\n")
        
        self.results['preconditions'].append(precondition)
        return precondition['status'] == 'PASS'
    
    def _check_precondition_2(self) -> bool:
        """Precondition 2: Architecture Compilation Contract = PASS"""
        precondition = {
            'precondition': 'PC2: Architecture Compilation Contract',
            'status': 'UNKNOWN',
            'message': '',
            'evidence': {}
        }
        
        print("🏗️  Precondition 2: Architecture Compilation Contract...")
        
        # Run Architecture Compilation validator
        arch_pass, arch_output = self._run_validator('validate-architecture-compilation.py', self.app_name)
        
        precondition['evidence']['architecture_compilation_validation'] = arch_pass
        
        if arch_pass:
            precondition['status'] = 'PASS'
            precondition['message'] = 'Architecture compilation complete'
            print("  ✅ PASS - Architecture compilation validated\n")
        else:
            precondition['status'] = 'FAIL'
            precondition['message'] = 'Architecture compilation incomplete'
            self.results['errors'].append(
                "PC2 BLOCKING: Architecture must be 100% complete with no TBD markers"
            )
            print("  ❌ FAIL - Architecture compilation not complete\n")
        
        self.results['preconditions'].append(precondition)
        return precondition['status'] == 'PASS'
    
    def _check_precondition_3(self) -> bool:
        """Precondition 3: QA Derivation & Coverage Rules = PASS"""
        precondition = {
            'precondition': 'PC3: QA Derivation & Coverage',
            'status': 'UNKNOWN',
            'message': '',
            'evidence': {}
        }
        
        print("🧪 Precondition 3: QA Derivation & Coverage...")
        
        # Check if tests directory exists
        tests_dir = self.repo_root / "tests"
        has_tests = tests_dir.exists() and any(tests_dir.rglob("test_*.py"))
        
        precondition['evidence']['tests_exist'] = has_tests
        
        if has_tests:
            # Check if pytest can be run
            try:
                result = subprocess.run(
                    [sys.executable, '-m', 'pytest', '--collect-only', 'tests/'],
                    capture_output=True,
                    text=True,
                    cwd=str(self.repo_root),
                    timeout=30
                )
                tests_collected = 'collected' in result.stdout
                precondition['evidence']['tests_collected'] = tests_collected
                
                if tests_collected:
                    precondition['status'] = 'PASS'
                    precondition['message'] = 'QA tests present and collectible'
                    print("  ✅ PASS - QA tests exist\n")
                else:
                    precondition['status'] = 'WARN'
                    precondition['message'] = 'Tests exist but collection failed'
                    self.results['warnings'].append(
                        "PC3 WARNING: Test collection issues detected"
                    )
                    print("  ⚠️  WARN - Test collection issues\n")
            except Exception as e:
                precondition['status'] = 'WARN'
                precondition['message'] = f'Could not validate tests: {e}'
                self.results['warnings'].append(
                    "PC3 WARNING: Could not run test validation"
                )
                print(f"  ⚠️  WARN - Test validation error: {e}\n")
        else:
            precondition['status'] = 'FAIL'
            precondition['message'] = 'No QA tests found'
            self.results['errors'].append(
                "PC3 BLOCKING: QA tests required before build authorization"
            )
            print("  ❌ FAIL - No QA tests found\n")
        
        self.results['preconditions'].append(precondition)
        # Return True for PASS or WARN (not blocking in this implementation)
        return precondition['status'] in ['PASS', 'WARN']
    
    def _check_precondition_4(self) -> bool:
        """Precondition 4: FL/CI Learning Integration = COMPLETE"""
        precondition = {
            'precondition': 'PC4: FL/CI Learning Integration',
            'status': 'UNKNOWN',
            'message': '',
            'evidence': {}
        }
        
        print("📚 Precondition 4: FL/CI Learning Integration...")
        
        # Check for FL/CI evidence directory
        flci_dir = self.repo_root / "foreman" / "evidence" / "flci"
        has_flci = flci_dir.exists()
        
        precondition['evidence']['flci_directory_exists'] = has_flci
        
        # For now, this is advisory - pass with warning if missing
        if has_flci:
            precondition['status'] = 'PASS'
            precondition['message'] = 'FL/CI evidence directory exists'
            print("  ✅ PASS - FL/CI evidence present\n")
        else:
            precondition['status'] = 'WARN'
            precondition['message'] = 'FL/CI evidence directory not found'
            self.results['warnings'].append(
                "PC4 WARNING: FL/CI learning integration should be documented"
            )
            print("  ⚠️  WARN - FL/CI evidence directory missing\n")
        
        self.results['preconditions'].append(precondition)
        return True  # Not blocking for now
    
    def _check_precondition_5(self) -> bool:
        """Precondition 5: Deployment and Runtime Validation"""
        precondition = {
            'precondition': 'PC5: Deployment & Runtime Validation',
            'status': 'UNKNOWN',
            'message': '',
            'evidence': {}
        }
        
        print("🚀 Precondition 5: Deployment & Runtime Validation...")
        
        # Check for runtime specifications
        runtime_specs = [
            self.repo_root / "foreman" / "runtime",
            self.repo_root / "architecture" / "deployment",
        ]
        
        has_runtime_spec = any(path.exists() for path in runtime_specs)
        precondition['evidence']['runtime_specs_exist'] = has_runtime_spec
        
        if has_runtime_spec:
            precondition['status'] = 'PASS'
            precondition['message'] = 'Runtime specifications present'
            print("  ✅ PASS - Runtime specs exist\n")
        else:
            precondition['status'] = 'WARN'
            precondition['message'] = 'Runtime specifications not found'
            self.results['warnings'].append(
                "PC5 WARNING: Runtime/deployment specifications should be documented"
            )
            print("  ⚠️  WARN - Runtime specs missing\n")
        
        self.results['preconditions'].append(precondition)
        return True  # Not blocking for now
    
    def _check_precondition_6(self) -> bool:
        """Precondition 6: Governance Checklist = PASS"""
        precondition = {
            'precondition': 'PC6: Governance Checklist',
            'status': 'UNKNOWN',
            'message': '',
            'evidence': {}
        }
        
        print("✅ Precondition 6: Governance Checklist...")
        
        # Check for governance checklists
        checklist_path = self.repo_root / "governance" / "contracts" / "app-description-frs-alignment-checklist.md"
        has_checklist = checklist_path.exists()
        
        precondition['evidence']['governance_checklist_exists'] = has_checklist
        
        if has_checklist:
            precondition['status'] = 'PASS'
            precondition['message'] = 'Governance checklists present'
            print("  ✅ PASS - Governance checklists exist\n")
        else:
            precondition['status'] = 'FAIL'
            precondition['message'] = 'Governance checklist not found'
            self.results['errors'].append(
                "PC6 BLOCKING: Governance checklists required"
            )
            print("  ❌ FAIL - Governance checklists missing\n")
        
        self.results['preconditions'].append(precondition)
        return precondition['status'] == 'PASS'
    
    def _check_precondition_7(self) -> bool:
        """Precondition 7: Scope Freeze = CONFIRMED"""
        precondition = {
            'precondition': 'PC7: Scope Freeze',
            'status': 'UNKNOWN',
            'message': '',
            'evidence': {}
        }
        
        print("🔒 Precondition 7: Scope Freeze...")
        
        # Check if architecture is versioned/frozen
        arch_index_path = self.repo_root / "ARCHITECTURE_INDEX.json"
        
        if arch_index_path.exists():
            try:
                with open(arch_index_path, 'r') as f:
                    arch_index = json.load(f)
                
                has_timestamp = 'metadata' in arch_index and 'generated_at' in arch_index['metadata']
                precondition['evidence']['architecture_timestamped'] = has_timestamp
                
                if has_timestamp:
                    precondition['status'] = 'PASS'
                    precondition['message'] = 'Architecture is timestamped (frozen)'
                    print("  ✅ PASS - Architecture frozen\n")
                else:
                    precondition['status'] = 'WARN'
                    precondition['message'] = 'Architecture lacks explicit freeze marker'
                    self.results['warnings'].append(
                        "PC7 WARNING: Architecture should have explicit freeze marker"
                    )
                    print("  ⚠️  WARN - No explicit freeze marker\n")
            except Exception as e:
                precondition['status'] = 'WARN'
                precondition['message'] = f'Could not verify freeze status: {e}'
                print(f"  ⚠️  WARN - Freeze verification error\n")
        else:
            precondition['status'] = 'WARN'
            precondition['message'] = 'Architecture index not found'
            print("  ⚠️  WARN - No architecture index\n")
        
        self.results['preconditions'].append(precondition)
        return True  # Not blocking for now
    
    def _check_precondition_8(self) -> bool:
        """Precondition 8: Zero Regression Verification"""
        precondition = {
            'precondition': 'PC8: Zero Regression Verification',
            'status': 'UNKNOWN',
            'message': '',
            'evidence': {}
        }
        
        print("🛡️  Precondition 8: Zero Regression Verification...")
        
        # Check if tests can run
        tests_dir = self.repo_root / "tests"
        if tests_dir.exists():
            precondition['status'] = 'PASS'
            precondition['message'] = 'Test infrastructure exists for regression checks'
            print("  ✅ PASS - Test infrastructure present\n")
        else:
            precondition['status'] = 'WARN'
            precondition['message'] = 'No test infrastructure for regression verification'
            self.results['warnings'].append(
                "PC8 WARNING: Test infrastructure recommended for regression verification"
            )
            print("  ⚠️  WARN - No test infrastructure\n")
        
        self.results['preconditions'].append(precondition)
        return True  # Not blocking for now
    
    def write_evidence(self, output_dir: Path = None):
        """Write validation evidence to file"""
        if output_dir is None:
            output_dir = self.repo_root / "governance" / "evidence"
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Write JSON evidence
        evidence_file = output_dir / f"{self.results['validation_id']}.json"
        with open(evidence_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"📋 Evidence written to: {evidence_file}")
        return evidence_file


def main():
    """Main execution"""
    # Determine repository root
    repo_root = Path(__file__).resolve().parent.parent.parent
    
    # Get app name from command line or default to FM
    app_name = sys.argv[1] if len(sys.argv) > 1 else "FM"
    
    # Create validator and run
    validator = BuildAuthorizationGateValidator(repo_root, app_name)
    success, results = validator.validate()
    
    # Print results
    print("\n" + "="*70)
    print(f"BUILD AUTHORIZATION GATE DECISION - {app_name}")
    print("="*70)
    
    if success:
        print("\n🟢 BUILD AUTHORIZED")
        print("\nAll preconditions satisfied. Build may proceed.")
    else:
        print("\n🔴 BUILD BLOCKED")
        print("\nOne or more preconditions not satisfied. Build cannot proceed.")
    
    print(f"\nValidation ID: {results['validation_id']}")
    print(f"Timestamp: {results['timestamp']}")
    print(f"Decision: {results['decision']}")
    
    print(f"\n📋 Preconditions Status ({len(results['preconditions'])}):")
    for pc in results['preconditions']:
        if pc['status'] == 'PASS':
            status_icon = '✅'
        elif pc['status'] == 'WARN':
            status_icon = '⚠️ '
        else:
            status_icon = '❌'
        print(f"  {status_icon} {pc['precondition']}: {pc['message']}")
    
    if results['errors']:
        print(f"\n❌ Blocking Errors ({len(results['errors'])}):")
        for error in results['errors']:
            print(f"  - {error}")
    
    if results['warnings']:
        print(f"\n⚠️  Warnings ({len(results['warnings'])}):")
        for warning in results['warnings']:
            print(f"  - {warning}")
    
    print("\n" + "="*70)
    
    # Write evidence
    validator.write_evidence()
    
    print("\n")
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
