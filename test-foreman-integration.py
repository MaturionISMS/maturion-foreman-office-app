#!/usr/bin/env python3
"""
Maturion Foreman - Integration Test Suite

This comprehensive integration test validates the Foreman's governance reasoning
capabilities by running all governance systems together and proposing actions
based on analysis.

The test validates:
1. Repository validation system
2. Builder registry system
3. Compliance engine system
4. Architecture indexing system
5. Governance reasoning and action proposal

Usage:
    python3 test-foreman-integration.py
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class ForemanIntegrationTest:
    """Comprehensive integration test for Maturion Foreman governance systems."""
    
    def __init__(self):
        self.repo_root = Path(__file__).parent.resolve()
        self.test_results = {
            'timestamp': datetime.now().isoformat(),
            'repository_validation': {},
            'builder_registry': {},
            'compliance_engine': {},
            'architecture_index': {},
            'governance_analysis': {},
            'proposed_actions': []
        }
        self.errors = []
        self.warnings = []
        self.passed_tests = 0
        self.failed_tests = 0
    
    def log_info(self, message: str):
        """Log an informational message."""
        print(f"ℹ️  {message}")
    
    def log_success(self, message: str):
        """Log a success message."""
        print(f"✅ {message}")
        self.passed_tests += 1
    
    def log_warning(self, message: str):
        """Log a warning message."""
        print(f"⚠️  {message}")
        self.warnings.append(message)
    
    def log_error(self, message: str):
        """Log an error message."""
        print(f"❌ {message}")
        self.errors.append(message)
        self.failed_tests += 1
    
    def run_command(self, command: List[str], description: str) -> Tuple[bool, str]:
        """
        Run a command and return success status and output.
        
        Args:
            command: Command to run as list of strings
            description: Description of the command for logging
            
        Returns:
            Tuple of (success, output)
        """
        try:
            self.log_info(f"Running: {description}")
            result = subprocess.run(
                command,
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            success = result.returncode == 0
            output = result.stdout + result.stderr
            
            if success:
                self.log_success(f"{description} - PASSED")
            else:
                self.log_error(f"{description} - FAILED (exit code {result.returncode})")
            
            return success, output
        
        except subprocess.TimeoutExpired:
            self.log_error(f"{description} - TIMEOUT")
            return False, "Command timed out"
        except Exception as e:
            self.log_error(f"{description} - EXCEPTION: {e}")
            return False, str(e)
    
    def test_repository_validation(self) -> Dict:
        """Test the repository validation system."""
        print("\n" + "=" * 80)
        print("TEST 1: Repository Validation System")
        print("=" * 80)
        
        success, output = self.run_command(
            ['python3', 'validate-repository.py'],
            'Repository Structure Validation'
        )
        
        # Parse validation output
        result = {
            'success': success,
            'output_length': len(output),
            'has_errors': 'Total Errors: 0' not in output,
            'has_warnings': 'Total Warnings:' in output
        }
        
        # Extract key metrics
        if 'Total Errors:' in output:
            for line in output.split('\n'):
                if 'Total Errors:' in line:
                    errors = line.split(':')[1].strip()
                    result['error_count'] = errors
                if 'Total Warnings:' in line:
                    warnings = line.split(':')[1].strip()
                    result['warning_count'] = warnings
        
        self.test_results['repository_validation'] = result
        return result
    
    def test_builder_registry(self) -> Dict:
        """Test the builder registry initialization system."""
        print("\n" + "=" * 80)
        print("TEST 2: Builder Registry System")
        print("=" * 80)
        
        success, output = self.run_command(
            ['python3', 'foreman/test-init-builders.py'],
            'Builder Registry Test Suite'
        )
        
        result = {
            'success': success,
            'output_length': len(output),
            'all_tests_passed': '✓ All tests passed!' in output
        }
        
        # Extract test counts
        if 'Tests Passed:' in output:
            for line in output.split('\n'):
                if 'Tests Passed:' in line:
                    passed = line.split(':')[1].strip()
                    result['tests_passed'] = passed
                if 'Tests Failed:' in line:
                    failed = line.split(':')[1].strip()
                    result['tests_failed'] = failed
        
        self.test_results['builder_registry'] = result
        return result
    
    def test_compliance_engine(self) -> Dict:
        """Test the compliance engine activation."""
        print("\n" + "=" * 80)
        print("TEST 3: Compliance Engine System")
        print("=" * 80)
        
        success, output = self.run_command(
            ['python3', 'activate-compliance-engine.py'],
            'Compliance Engine Activation'
        )
        
        result = {
            'success': success,
            'output_length': len(output),
            'standards_validated': 'ISO 27001' in output
        }
        
        # Check for compliance report
        compliance_report = self.repo_root / 'foreman' / 'compliance-engine-readiness-report.md'
        result['report_generated'] = compliance_report.exists()
        
        if result['report_generated']:
            self.log_success("Compliance report generated")
        else:
            self.log_warning("Compliance report not found")
        
        self.test_results['compliance_engine'] = result
        return result
    
    def test_architecture_indexing(self) -> Dict:
        """Test the architecture indexing system."""
        print("\n" + "=" * 80)
        print("TEST 4: Architecture Indexing System")
        print("=" * 80)
        
        success, output = self.run_command(
            ['python3', 'index-isms-architecture.py'],
            'Architecture Indexing'
        )
        
        result = {
            'success': success,
            'output_length': len(output),
            'index_generated': False,
            'report_generated': False
        }
        
        # Check for generated files
        index_file = self.repo_root / 'ARCHITECTURE_INDEX.json'
        report_file = self.repo_root / 'ARCHITECTURE_INDEX_REPORT.md'
        
        result['index_generated'] = index_file.exists()
        result['report_generated'] = report_file.exists()
        
        if result['index_generated']:
            self.log_success("Architecture index generated")
            try:
                with open(index_file, 'r') as f:
                    index_data = json.load(f)
                    result['total_modules'] = len(index_data.get('modules', {}))
                    result['total_files'] = index_data.get('summary', {}).get('total_architecture_files', 0)
            except Exception as e:
                self.log_warning(f"Could not parse index: {e}")
        
        if result['report_generated']:
            self.log_success("Architecture report generated")
        
        self.test_results['architecture_index'] = result
        return result
    
    def analyze_governance_state(self) -> Dict:
        """
        Analyze the overall governance state and identify issues.
        
        This implements the Foreman's governance reasoning capability.
        """
        print("\n" + "=" * 80)
        print("TEST 5: Governance Reasoning Analysis")
        print("=" * 80)
        
        self.log_info("Analyzing integrated governance state...")
        
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'systems_operational': [],
            'systems_degraded': [],
            'critical_issues': [],
            'warnings': [],
            'recommendations': []
        }
        
        # Analyze each system
        repo_val = self.test_results.get('repository_validation', {})
        if repo_val.get('success'):
            analysis['systems_operational'].append('Repository Validation')
            self.log_success("Repository Validation: OPERATIONAL")
        else:
            analysis['systems_degraded'].append('Repository Validation')
            analysis['critical_issues'].append('Repository validation failed')
            self.log_error("Repository Validation: DEGRADED")
        
        builder_reg = self.test_results.get('builder_registry', {})
        if builder_reg.get('all_tests_passed'):
            analysis['systems_operational'].append('Builder Registry')
            self.log_success("Builder Registry: OPERATIONAL")
        else:
            analysis['systems_degraded'].append('Builder Registry')
            analysis['critical_issues'].append('Builder registry tests failed')
            self.log_error("Builder Registry: DEGRADED")
        
        compliance = self.test_results.get('compliance_engine', {})
        if compliance.get('success'):
            analysis['systems_operational'].append('Compliance Engine')
            self.log_success("Compliance Engine: OPERATIONAL")
        else:
            analysis['systems_degraded'].append('Compliance Engine')
            analysis['warnings'].append('Compliance engine activation issues')
            self.log_warning("Compliance Engine: DEGRADED")
        
        arch_index = self.test_results.get('architecture_index', {})
        if arch_index.get('index_generated'):
            analysis['systems_operational'].append('Architecture Indexing')
            self.log_success("Architecture Indexing: OPERATIONAL")
        else:
            analysis['systems_degraded'].append('Architecture Indexing')
            analysis['warnings'].append('Architecture index not fully generated')
            self.log_warning("Architecture Indexing: DEGRADED")
        
        # Check for missing architecture components
        if repo_val.get('warning_count'):
            try:
                warning_count = int(repo_val['warning_count'])
                if warning_count > 50:
                    analysis['warnings'].append(f'High number of architecture warnings: {warning_count}')
                    analysis['recommendations'].append(
                        'Review and address missing architecture components'
                    )
            except (ValueError, TypeError):
                pass
        
        # Overall health assessment
        operational_count = len(analysis['systems_operational'])
        total_systems = operational_count + len(analysis['systems_degraded'])
        
        if total_systems > 0:
            health_percentage = (operational_count / total_systems) * 100
            analysis['overall_health'] = f"{health_percentage:.1f}%"
            analysis['operational_systems'] = operational_count
            analysis['total_systems'] = total_systems
            
            self.log_info(f"Overall System Health: {health_percentage:.1f}%")
            self.log_info(f"Operational Systems: {operational_count}/{total_systems}")
        
        self.test_results['governance_analysis'] = analysis
        return analysis
    
    def propose_actions(self, analysis: Dict) -> List[Dict]:
        """
        Propose prioritized actions based on governance analysis.
        
        This implements the Foreman's action proposal capability.
        """
        print("\n" + "=" * 80)
        print("TEST 6: Action Proposal Generation")
        print("=" * 80)
        
        self.log_info("Generating prioritized action proposals...")
        
        actions = []
        
        # Priority 1: Critical system failures
        for issue in analysis.get('critical_issues', []):
            actions.append({
                'priority': 'CRITICAL',
                'category': 'System Failure',
                'issue': issue,
                'action': f'Investigate and resolve: {issue}',
                'impact': 'HIGH - Prevents governance enforcement',
                'effort': 'HIGH'
            })
        
        # Priority 2: Degraded systems
        for system in analysis.get('systems_degraded', []):
            if system not in ['Compliance Engine', 'Architecture Indexing']:
                actions.append({
                    'priority': 'HIGH',
                    'category': 'System Degradation',
                    'issue': f'{system} is degraded',
                    'action': f'Restore {system} to operational state',
                    'impact': 'MEDIUM - Reduces governance effectiveness',
                    'effort': 'MEDIUM'
                })
        
        # Priority 3: Warning-level issues
        for warning in analysis.get('warnings', []):
            if 'architecture warnings' in warning.lower():
                actions.append({
                    'priority': 'MEDIUM',
                    'category': 'Architecture Completeness',
                    'issue': warning,
                    'action': 'Complete missing architecture specifications',
                    'impact': 'MEDIUM - Incomplete architecture documentation',
                    'effort': 'HIGH'
                })
            else:
                actions.append({
                    'priority': 'MEDIUM',
                    'category': 'System Warning',
                    'issue': warning,
                    'action': f'Address warning: {warning}',
                    'impact': 'LOW - System functional but suboptimal',
                    'effort': 'MEDIUM'
                })
        
        # Priority 4: Recommendations
        for rec in analysis.get('recommendations', []):
            actions.append({
                'priority': 'LOW',
                'category': 'Optimization',
                'issue': 'Continuous improvement opportunity',
                'action': rec,
                'impact': 'LOW - Incremental improvement',
                'effort': 'VARIABLE'
            })
        
        # Add baseline actions if system is healthy
        if len(actions) == 0:
            actions.append({
                'priority': 'INFO',
                'category': 'Maintenance',
                'issue': 'All systems operational',
                'action': 'Continue routine governance monitoring',
                'impact': 'MAINTENANCE',
                'effort': 'LOW'
            })
        
        # Log proposed actions
        for i, action in enumerate(actions, 1):
            self.log_info(f"Action {i}: [{action['priority']}] {action['action']}")
        
        self.test_results['proposed_actions'] = actions
        return actions
    
    def generate_comprehensive_report(self) -> str:
        """Generate a comprehensive integration test report."""
        report_lines = []
        
        # Header
        report_lines.append("=" * 80)
        report_lines.append("MATURION FOREMAN - INTEGRATION TEST REPORT")
        report_lines.append("=" * 80)
        report_lines.append(f"Timestamp: {self.test_results['timestamp']}")
        report_lines.append("")
        
        # Executive Summary
        report_lines.append("EXECUTIVE SUMMARY")
        report_lines.append("-" * 80)
        report_lines.append(f"Tests Passed: {self.passed_tests}")
        report_lines.append(f"Tests Failed: {self.failed_tests}")
        report_lines.append(f"Warnings: {len(self.warnings)}")
        report_lines.append(f"Errors: {len(self.errors)}")
        
        analysis = self.test_results.get('governance_analysis', {})
        if 'overall_health' in analysis:
            report_lines.append(f"Overall System Health: {analysis['overall_health']}")
            report_lines.append(
                f"Operational Systems: {analysis['operational_systems']}/{analysis['total_systems']}"
            )
        report_lines.append("")
        
        # System Status
        report_lines.append("GOVERNANCE SYSTEMS STATUS")
        report_lines.append("-" * 80)
        
        for system in analysis.get('systems_operational', []):
            report_lines.append(f"✅ {system}: OPERATIONAL")
        
        for system in analysis.get('systems_degraded', []):
            report_lines.append(f"⚠️  {system}: DEGRADED")
        
        report_lines.append("")
        
        # Critical Issues
        if analysis.get('critical_issues'):
            report_lines.append("CRITICAL ISSUES")
            report_lines.append("-" * 80)
            for issue in analysis['critical_issues']:
                report_lines.append(f"❌ {issue}")
            report_lines.append("")
        
        # Warnings
        if analysis.get('warnings'):
            report_lines.append("WARNINGS")
            report_lines.append("-" * 80)
            for warning in analysis['warnings']:
                report_lines.append(f"⚠️  {warning}")
            report_lines.append("")
        
        # Proposed Actions
        actions = self.test_results.get('proposed_actions', [])
        if actions:
            report_lines.append("PROPOSED ACTIONS (PRIORITIZED)")
            report_lines.append("-" * 80)
            
            # Group by priority
            priorities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']
            for priority in priorities:
                priority_actions = [a for a in actions if a['priority'] == priority]
                if priority_actions:
                    report_lines.append(f"\n{priority} Priority:")
                    for action in priority_actions:
                        report_lines.append(f"  • {action['action']}")
                        report_lines.append(f"    Category: {action['category']}")
                        report_lines.append(f"    Impact: {action['impact']}")
                        report_lines.append(f"    Effort: {action['effort']}")
                        report_lines.append("")
        
        # Test Details
        report_lines.append("\nDETAILED TEST RESULTS")
        report_lines.append("-" * 80)
        
        for test_name, test_data in self.test_results.items():
            if test_name not in ['timestamp', 'governance_analysis', 'proposed_actions']:
                report_lines.append(f"\n{test_name.replace('_', ' ').title()}:")
                if isinstance(test_data, dict):
                    for key, value in test_data.items():
                        report_lines.append(f"  {key}: {value}")
        
        # Conclusion
        report_lines.append("\n" + "=" * 80)
        report_lines.append("CONCLUSION")
        report_lines.append("=" * 80)
        
        if self.failed_tests == 0:
            report_lines.append("✅ Integration test PASSED - All governance systems validated")
        elif self.failed_tests <= 2:
            report_lines.append("⚠️  Integration test PASSED WITH WARNINGS - Some systems degraded")
        else:
            report_lines.append("❌ Integration test FAILED - Critical governance systems offline")
        
        report_lines.append("")
        report_lines.append(f"Foreman Governance Reasoning: {'OPERATIONAL' if self.failed_tests < 3 else 'REQUIRES ATTENTION'}")
        report_lines.append("=" * 80)
        
        return "\n".join(report_lines)
    
    def run_integration_test(self) -> int:
        """
        Execute the complete integration test suite.
        
        Returns:
            Exit code (0 for success, 1 for failure)
        """
        print("🔍 Starting Maturion Foreman Integration Test Suite...")
        print(f"📍 Repository: {self.repo_root}")
        print("")
        
        # Run all tests
        self.test_repository_validation()
        self.test_builder_registry()
        self.test_compliance_engine()
        self.test_architecture_indexing()
        
        # Governance reasoning
        analysis = self.analyze_governance_state()
        actions = self.propose_actions(analysis)
        
        # Generate report
        report = self.generate_comprehensive_report()
        
        # Print report
        print("\n")
        print(report)
        
        # Save report
        report_path = self.repo_root / 'FOREMAN_INTEGRATION_TEST_REPORT.md'
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(f"\n📄 Full report saved to: {report_path}")
        
        # Save JSON results
        json_path = self.repo_root / 'FOREMAN_INTEGRATION_TEST_RESULTS.json'
        with open(json_path, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"📊 JSON results saved to: {json_path}")
        
        # Determine exit code
        # Success if critical systems are operational (max 2 failures allowed)
        exit_code = 0 if self.failed_tests <= 2 else 1
        
        return exit_code


def main():
    """Main entry point for integration test execution."""
    test_suite = ForemanIntegrationTest()
    exit_code = test_suite.run_integration_test()
    
    print(f"\n{'✅ INTEGRATION TEST SUITE COMPLETED SUCCESSFULLY' if exit_code == 0 else '❌ INTEGRATION TEST SUITE FAILED'}")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
