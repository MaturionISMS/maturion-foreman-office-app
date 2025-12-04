#!/usr/bin/env python3
"""
Maturion Foreman - Build Wave 1 Governance QA & Validation

Performs comprehensive governance, QA, and compliance validation for Build Wave 1.

Usage:
    python3 validate-build-wave-1.py
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class BuildWave1Validator:
    """Validates Build Wave 1 completeness, governance, and compliance"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.validation_results = {
            "overall_status": "UNKNOWN",
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "checks": {},
            "errors": [],
            "warnings": [],
            "passed": 0,
            "failed": 0,
            "warnings_count": 0
        }
        
    def validate_all(self) -> bool:
        """Run all validation checks"""
        print("=" * 80)
        print("Build Wave 1 - Governance QA & Validation")
        print("=" * 80)
        print()
        
        # Check 1: Core deliverables exist
        self._check_deliverables()
        
        # Check 2: Build plan validation
        self._check_build_plan()
        
        # Check 3: Build tasks validation
        self._check_build_tasks()
        
        # Check 4: Build status validation
        self._check_build_status()
        
        # Check 5: Change Records validation
        self._check_change_records()
        
        # Check 6: Test environment validation
        self._check_test_environment()
        
        # Check 7: AI Memory validation
        self._check_ai_memory()
        
        # Check 8: Governance compliance
        self._check_governance_compliance()
        
        # Generate report
        self._generate_report()
        
        # Determine overall status
        if self.validation_results['failed'] == 0:
            if self.validation_results['warnings_count'] == 0:
                self.validation_results['overall_status'] = "PASS"
            else:
                self.validation_results['overall_status'] = "PASS_WITH_WARNINGS"
        else:
            self.validation_results['overall_status'] = "FAIL"
        
        return self.validation_results['failed'] == 0
        
    def _check_deliverables(self):
        """Check that all required deliverables exist"""
        print("Check 1: Core Deliverables")
        
        required_files = [
            'build-plan-wave-1.json',
            'build-tasks-wave-1.json',
            'build-status-wave-1.json',
            'BUILD_ORCHESTRATION_READINESS.md',
            'foreman/reports/BUILD_WAVE_1_SUMMARY.md'
        ]
        
        missing = []
        for file in required_files:
            path = self.repo_root / file
            if not path.exists():
                missing.append(file)
                
        if missing:
            self.validation_results['checks']['deliverables'] = {
                "status": "FAIL",
                "message": f"Missing files: {', '.join(missing)}"
            }
            self.validation_results['failed'] += 1
            self.validation_results['errors'].append(f"Missing deliverables: {missing}")
            print(f"  ❌ FAIL: Missing {len(missing)} files")
        else:
            self.validation_results['checks']['deliverables'] = {
                "status": "PASS",
                "message": "All core deliverables present"
            }
            self.validation_results['passed'] += 1
            print(f"  ✅ PASS: All deliverables present")
        print()
        
    def _check_build_plan(self):
        """Validate build plan structure and content"""
        print("Check 2: Build Plan Validation")
        
        plan_file = self.repo_root / 'build-plan-wave-1.json'
        
        try:
            with open(plan_file, 'r') as f:
                plan = json.load(f)
                
            # Check module count
            expected_modules = 11
            actual_modules = plan.get('module_count', 0)
            
            if actual_modules != expected_modules:
                self.validation_results['warnings'].append(
                    f"Expected {expected_modules} modules, found {actual_modules}"
                )
                self.validation_results['warnings_count'] += 1
                
            # Check build sequence exists
            if 'build_sequence' not in plan:
                self.validation_results['errors'].append("Build sequence missing")
                self.validation_results['failed'] += 1
                print(f"  ❌ FAIL: Build sequence missing")
                return
                
            # Check circular dependencies logged
            circ_deps = plan.get('governance_checks', {}).get('circular_dependencies', [])
            if circ_deps:
                self.validation_results['warnings'].append(
                    f"Circular dependencies detected: {circ_deps}"
                )
                self.validation_results['warnings_count'] += 1
                print(f"  ⚠️  WARNING: {len(circ_deps)} circular dependencies")
            
            self.validation_results['checks']['build_plan'] = {
                "status": "PASS",
                "modules": actual_modules,
                "circular_dependencies": len(circ_deps)
            }
            self.validation_results['passed'] += 1
            print(f"  ✅ PASS: Build plan valid ({actual_modules} modules)")
            
        except Exception as e:
            self.validation_results['checks']['build_plan'] = {
                "status": "FAIL",
                "error": str(e)
            }
            self.validation_results['failed'] += 1
            self.validation_results['errors'].append(f"Build plan validation error: {e}")
            print(f"  ❌ FAIL: {e}")
        print()
        
    def _check_build_tasks(self):
        """Validate build tasks structure"""
        print("Check 3: Build Tasks Validation")
        
        tasks_file = self.repo_root / 'build-tasks-wave-1.json'
        
        try:
            with open(tasks_file, 'r') as f:
                tasks = json.load(f)
                
            total_tasks = tasks.get('total_tasks', 0)
            expected_min_tasks = 88  # 11 modules * 8 tasks
            
            if total_tasks < expected_min_tasks:
                self.validation_results['warnings'].append(
                    f"Expected at least {expected_min_tasks} tasks, found {total_tasks}"
                )
                self.validation_results['warnings_count'] += 1
                
            # Check builders
            builders = tasks.get('tasks_by_builder', {})
            expected_builders = ['schema-builder', 'api-builder', 'ui-builder', 'integration-builder', 'qa-builder']
            
            missing_builders = [b for b in expected_builders if b not in builders]
            if missing_builders:
                self.validation_results['errors'].append(f"Missing builders: {missing_builders}")
                self.validation_results['failed'] += 1
                print(f"  ❌ FAIL: Missing builders: {missing_builders}")
                return
                
            self.validation_results['checks']['build_tasks'] = {
                "status": "PASS",
                "total_tasks": total_tasks,
                "builders": len(builders)
            }
            self.validation_results['passed'] += 1
            print(f"  ✅ PASS: Build tasks valid ({total_tasks} tasks, {len(builders)} builders)")
            
        except Exception as e:
            self.validation_results['checks']['build_tasks'] = {
                "status": "FAIL",
                "error": str(e)
            }
            self.validation_results['failed'] += 1
            self.validation_results['errors'].append(f"Build tasks validation error: {e}")
            print(f"  ❌ FAIL: {e}")
        print()
        
    def _check_build_status(self):
        """Validate build status structure"""
        print("Check 4: Build Status Validation")
        
        status_file = self.repo_root / 'build-status-wave-1.json'
        
        try:
            with open(status_file, 'r') as f:
                status = json.load(f)
                
            if status.get('overall_status') != 'PLANNING_COMPLETE':
                self.validation_results['warnings'].append(
                    f"Status is {status.get('overall_status')}, expected PLANNING_COMPLETE"
                )
                self.validation_results['warnings_count'] += 1
                
            self.validation_results['checks']['build_status'] = {
                "status": "PASS",
                "overall_status": status.get('overall_status')
            }
            self.validation_results['passed'] += 1
            print(f"  ✅ PASS: Build status valid")
            
        except Exception as e:
            self.validation_results['checks']['build_status'] = {
                "status": "FAIL",
                "error": str(e)
            }
            self.validation_results['failed'] += 1
            self.validation_results['errors'].append(f"Build status validation error: {e}")
            print(f"  ❌ FAIL: {e}")
        print()
        
    def _check_change_records(self):
        """Validate Change Records were created"""
        print("Check 5: Change Records Validation")
        
        cr_dir = self.repo_root / 'foreman' / 'change-management'
        cr_files = list(cr_dir.glob('CR-BW1-*.json'))
        
        expected_crs = 11  # One per module
        
        if len(cr_files) < expected_crs:
            self.validation_results['warnings'].append(
                f"Expected {expected_crs} CRs, found {len(cr_files)}"
            )
            self.validation_results['warnings_count'] += 1
            print(f"  ⚠️  WARNING: Found {len(cr_files)} CRs, expected {expected_crs}")
        else:
            self.validation_results['checks']['change_records'] = {
                "status": "PASS",
                "count": len(cr_files)
            }
            self.validation_results['passed'] += 1
            print(f"  ✅ PASS: {len(cr_files)} Change Records created")
        print()
        
    def _check_test_environment(self):
        """Validate test environment deployment stubs"""
        print("Check 6: Test Environment Validation")
        
        test_env_dir = self.repo_root / 'foreman' / 'test-environment' / 'module-stubs'
        
        if not test_env_dir.exists():
            self.validation_results['errors'].append("Test environment module-stubs directory missing")
            self.validation_results['failed'] += 1
            print(f"  ❌ FAIL: module-stubs directory missing")
            return
            
        deploy_scripts = list(test_env_dir.glob('deploy-*.sh'))
        validate_scripts = list(test_env_dir.glob('validate-*.sh'))
        
        expected_scripts = 11  # One per module
        
        if len(deploy_scripts) < expected_scripts or len(validate_scripts) < expected_scripts:
            self.validation_results['warnings'].append(
                f"Expected {expected_scripts} deploy and validate scripts each"
            )
            self.validation_results['warnings_count'] += 1
            print(f"  ⚠️  WARNING: Deploy: {len(deploy_scripts)}, Validate: {len(validate_scripts)}")
        else:
            self.validation_results['checks']['test_environment'] = {
                "status": "PASS",
                "deploy_scripts": len(deploy_scripts),
                "validate_scripts": len(validate_scripts)
            }
            self.validation_results['passed'] += 1
            print(f"  ✅ PASS: Test environment stubs created ({len(deploy_scripts)} deploy, {len(validate_scripts)} validate)")
        print()
        
    def _check_ai_memory(self):
        """Validate AI memory files"""
        print("Check 7: AI Memory Validation")
        
        memory_dir = self.repo_root / 'foreman' / 'ai-memory'
        
        required_files = [
            'build-wave-1-learnings.md',
            'build-wave-1-historical-issues.json',
            'build-wave-1-reasoning-patterns.json'
        ]
        
        missing = []
        for file in required_files:
            if not (memory_dir / file).exists():
                missing.append(file)
                
        if missing:
            self.validation_results['errors'].append(f"Missing AI memory files: {missing}")
            self.validation_results['failed'] += 1
            print(f"  ❌ FAIL: Missing {len(missing)} AI memory files")
        else:
            self.validation_results['checks']['ai_memory'] = {
                "status": "PASS",
                "files": len(required_files)
            }
            self.validation_results['passed'] += 1
            print(f"  ✅ PASS: AI memory files complete")
        print()
        
    def _check_governance_compliance(self):
        """Validate governance compliance"""
        print("Check 8: Governance Compliance")
        
        # Check that Foreman paused before execution
        status_file = self.repo_root / 'build-status-wave-1.json'
        
        try:
            with open(status_file, 'r') as f:
                status = json.load(f)
                
            exec_status = status.get('execution_status', '')
            
            if exec_status != 'AWAITING_APPROVAL':
                self.validation_results['warnings'].append(
                    "Execution status should be AWAITING_APPROVAL (Foreman must wait for Johan)"
                )
                self.validation_results['warnings_count'] += 1
                
            self.validation_results['checks']['governance'] = {
                "status": "PASS",
                "execution_status": exec_status,
                "awaiting_approval": exec_status == 'AWAITING_APPROVAL'
            }
            self.validation_results['passed'] += 1
            print(f"  ✅ PASS: Governance compliance validated")
            
        except Exception as e:
            self.validation_results['checks']['governance'] = {
                "status": "FAIL",
                "error": str(e)
            }
            self.validation_results['failed'] += 1
            print(f"  ❌ FAIL: {e}")
        print()
        
    def _generate_report(self):
        """Generate validation report"""
        report_file = self.repo_root / 'BUILD_WAVE_1_VALIDATION_REPORT.md'
        
        with open(report_file, 'w') as f:
            f.write("# Build Wave 1 - Validation Report\n\n")
            f.write(f"**Generated**: {self.validation_results['timestamp']}\n")
            f.write(f"**Overall Status**: **{self.validation_results['overall_status']}**\n\n")
            f.write("---\n\n")
            
            f.write("## Summary\n\n")
            f.write(f"- ✅ **Passed**: {self.validation_results['passed']}\n")
            f.write(f"- ❌ **Failed**: {self.validation_results['failed']}\n")
            f.write(f"- ⚠️  **Warnings**: {self.validation_results['warnings_count']}\n\n")
            f.write("---\n\n")
            
            f.write("## Validation Checks\n\n")
            for check_name, check_result in self.validation_results['checks'].items():
                status_icon = "✅" if check_result['status'] == "PASS" else "❌"
                f.write(f"### {status_icon} {check_name.replace('_', ' ').title()}\n\n")
                f.write(f"**Status**: {check_result['status']}\n\n")
                if 'message' in check_result:
                    f.write(f"{check_result['message']}\n\n")
                if check_result.get('status') != "PASS" and 'error' in check_result:
                    f.write(f"**Error**: {check_result['error']}\n\n")
                f.write("---\n\n")
                
            if self.validation_results['errors']:
                f.write("## Errors\n\n")
                for error in self.validation_results['errors']:
                    f.write(f"- ❌ {error}\n")
                f.write("\n---\n\n")
                
            if self.validation_results['warnings']:
                f.write("## Warnings\n\n")
                for warning in self.validation_results['warnings']:
                    f.write(f"- ⚠️  {warning}\n")
                f.write("\n---\n\n")
                
            f.write("## Recommendation\n\n")
            if self.validation_results['overall_status'] == "PASS":
                f.write("✅ **BUILD WAVE 1 PLANNING IS COMPLETE AND VALID**\n\n")
                f.write("All required deliverables are present and validated.\n")
                f.write("Build Wave 1 is ready for Johan's approval to proceed with execution.\n\n")
            elif self.validation_results['overall_status'] == "PASS_WITH_WARNINGS":
                f.write("⚠️  **BUILD WAVE 1 PLANNING IS COMPLETE WITH WARNINGS**\n\n")
                f.write("All critical deliverables are present, but some warnings exist.\n")
                f.write("Review warnings before proceeding. Build Wave 1 can proceed with Johan's approval.\n\n")
            else:
                f.write("❌ **BUILD WAVE 1 PLANNING HAS ISSUES**\n\n")
                f.write("Critical errors found. Address all errors before proceeding.\n\n")
                
            f.write("---\n\n")
            f.write("*Generated by Maturion Foreman - Build Wave 1 Governance QA*\n")
        
        print(f"✅ Validation report saved to {report_file}")
        
        # Also save JSON
        json_file = self.repo_root / 'BUILD_WAVE_1_VALIDATION_REPORT.json'
        with open(json_file, 'w') as f:
            json.dump(self.validation_results, f, indent=2)
        print(f"✅ Validation JSON saved to {json_file}")
        

def main():
    """Main execution"""
    repo_root = Path(__file__).parent
    
    validator = BuildWave1Validator(repo_root)
    success = validator.validate_all()
    
    print()
    print("=" * 80)
    if success:
        print(f"✅ VALIDATION PASSED: {validator.validation_results['overall_status']}")
        print("=" * 80)
        return 0
    else:
        print(f"❌ VALIDATION FAILED: {validator.validation_results['failed']} errors")
        print("=" * 80)
        return 1


if __name__ == '__main__':
    exit(main())
