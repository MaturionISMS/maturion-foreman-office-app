#!/usr/bin/env python3
"""
Maturion Foreman - Central Governance Gate

Single entry point for all governance validation. This script coordinates
all governance validators and provides a unified PASS/FAIL decision.

This is the mandatory entry point that must be called before any build,
architecture operation, or execution flow proceeds.

Usage:
    python3 governance-gate.py <app_name> [--strict]
    
    --strict: Fail on warnings as well as errors (default: errors only)

Returns:
    Exit 0: All governance requirements satisfied (PASS)
    Exit 1: One or more governance requirements not satisfied (FAIL)
"""

import json
import sys
from pathlib import Path
from typing import Dict, Tuple
from datetime import datetime
import subprocess


class GovernanceGate:
    """Central governance gate orchestrator"""
    
    def __init__(self, repo_root: Path, app_name: str = "FM", strict: bool = False):
        self.repo_root = repo_root
        self.app_name = app_name
        self.strict = strict
        self.results = {
            'gate_id': f'gov-gate-{app_name}-{datetime.now().strftime("%Y%m%d-%H%M%S")}',
            'timestamp': datetime.now().isoformat(),
            'app_name': app_name,
            'strict_mode': strict,
            'status': 'UNKNOWN',
            'validations': {},
            'decision': 'PENDING',
            'errors': [],
            'warnings': []
        }
        
    def validate(self) -> Tuple[bool, Dict]:
        """Run all governance validations"""
        print("="*70)
        print(f"🛡️  MATURION GOVERNANCE GATE - {self.app_name}")
        print("="*70)
        print(f"\nTimestamp: {self.results['timestamp']}")
        print(f"Strict Mode: {'ENABLED' if self.strict else 'DISABLED'}")
        print("\n" + "="*70 + "\n")
        
        # Validation 1: App Description
        print("🔍 Running App Description Validation...")
        app_desc_result = self._run_validation('validate-app-description.py', self.app_name)
        self.results['validations']['app_description'] = app_desc_result
        
        # Validation 2: FRS Alignment
        print("\n🔗 Running FRS Alignment Validation...")
        frs_path = "foreman/architecture/FOREMAN_TRUE_NORTH_v1.0.md"
        frs_result = self._run_validation('validate-frs-alignment.py', self.app_name, frs_path)
        self.results['validations']['frs_alignment'] = frs_result
        
        # Validation 3: Architecture Compilation
        print("\n🏗️  Running Architecture Compilation Validation...")
        arch_result = self._run_validation('validate-architecture-compilation.py', self.app_name)
        self.results['validations']['architecture_compilation'] = arch_result
        
        # Validation 4: Build Authorization Gate (master check)
        print("\n🚦 Running Build Authorization Gate Validation...")
        gate_result = self._run_validation('validate-build-authorization-gate.py', self.app_name)
        self.results['validations']['build_authorization_gate'] = gate_result
        
        # Determine overall status
        all_passed = all(
            result['passed'] for result in self.results['validations'].values()
        )
        
        has_warnings = any(
            result.get('has_warnings', False) for result in self.results['validations'].values()
        )
        
        if all_passed and (not self.strict or not has_warnings):
            self.results['status'] = 'PASS'
            self.results['decision'] = 'AUTHORIZED'
        else:
            self.results['status'] = 'FAIL'
            self.results['decision'] = 'BLOCKED'
            
            if not all_passed:
                self.results['errors'].append(
                    "One or more critical governance validations failed"
                )
            elif self.strict and has_warnings:
                self.results['errors'].append(
                    "Strict mode: Warnings present, blocking execution"
                )
        
        return self.results['decision'] == 'AUTHORIZED', self.results
    
    def _run_validation(self, script_name: str, *args) -> Dict:
        """Run a validation script and capture results"""
        script_path = self.repo_root / "governance" / "scripts" / script_name
        
        result = {
            'script': script_name,
            'passed': False,
            'has_warnings': False,
            'exit_code': None,
            'output': ''
        }
        
        if not script_path.exists():
            result['output'] = f"❌ Validator not found: {script_name}"
            print(f"  {result['output']}")
            return result
        
        try:
            proc_result = subprocess.run(
                [sys.executable, str(script_path), *args],
                capture_output=True,
                text=True,
                cwd=str(self.repo_root),
                timeout=60
            )
            
            result['exit_code'] = proc_result.returncode
            result['output'] = proc_result.stdout + proc_result.stderr
            result['passed'] = proc_result.returncode == 0
            
            # Check for warnings in output
            if '⚠️' in result['output'] or 'WARNING' in result['output']:
                result['has_warnings'] = True
            
            # Print summary
            if result['passed']:
                print("  ✅ PASS")
            else:
                print("  ❌ FAIL")
                
        except subprocess.TimeoutExpired:
            result['output'] = f"❌ Validation timed out after 60 seconds"
            print(f"  {result['output']}")
        except Exception as e:
            result['output'] = f"❌ Error running validation: {e}"
            print(f"  {result['output']}")
        
        return result
    
    def write_evidence(self, output_dir: Path = None):
        """Write gate decision evidence to file"""
        if output_dir is None:
            output_dir = self.repo_root / "governance" / "evidence"
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Write JSON evidence
        evidence_file = output_dir / f"{self.results['gate_id']}.json"
        with open(evidence_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        return evidence_file
    
    def print_summary(self):
        """Print governance gate decision summary"""
        print("\n" + "="*70)
        print("GOVERNANCE GATE DECISION")
        print("="*70)
        
        if self.results['decision'] == 'AUTHORIZED':
            print("\n🟢 EXECUTION AUTHORIZED")
            print("\n✅ All governance requirements satisfied.")
            print("✅ Build/execution may proceed.")
        else:
            print("\n🔴 EXECUTION BLOCKED")
            print("\n❌ One or more governance requirements not satisfied.")
            print("❌ Build/execution CANNOT proceed.")
        
        print(f"\nGate ID: {self.results['gate_id']}")
        print(f"Decision: {self.results['decision']}")
        print(f"Status: {self.results['status']}")
        
        print(f"\n📋 Validation Results:")
        for name, result in self.results['validations'].items():
            status = '✅ PASS' if result['passed'] else '❌ FAIL'
            warnings = ' ⚠️  (has warnings)' if result.get('has_warnings') else ''
            print(f"  {status}{warnings} - {name}")
        
        if self.results['errors']:
            print(f"\n❌ Blocking Issues:")
            for error in self.results['errors']:
                print(f"  - {error}")
        
        print("\n" + "="*70)


def main():
    """Main execution"""
    # Parse arguments
    import argparse
    parser = argparse.ArgumentParser(description='Maturion Governance Gate')
    parser.add_argument('app_name', nargs='?', default='FM', help='Application name (default: FM)')
    parser.add_argument('--strict', action='store_true', help='Fail on warnings as well as errors')
    args = parser.parse_args()
    
    # Determine repository root
    repo_root = Path(__file__).resolve().parent.parent.parent
    
    # Create gate and run
    gate = GovernanceGate(repo_root, args.app_name, args.strict)
    success, results = gate.validate()
    
    # Print summary
    gate.print_summary()
    
    # Write evidence
    evidence_file = gate.write_evidence()
    print(f"\n📋 Gate evidence: {evidence_file}")
    
    # Exit with appropriate code
    print()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
