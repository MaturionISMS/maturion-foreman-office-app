#!/usr/bin/env python3
"""
QA Green Validation Script

Validates that QA suite meets 100% pass requirement:
- 100% tests passing (no failures, no errors)
- Zero skipped tests
- Zero warnings
- Clean exit code

Constitutional Authority: Governance Supremacy Rule (GSR)
Enforcement Level: CI/CD blocking
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional

# Constants
MAX_OUTPUT_LENGTH = 5000  # Maximum length for test output in reports


class QAGreenValidator:
    """Validates QA green status (100% pass requirement)"""

    def __init__(self, test_dir: str):
        self.test_dir = Path(test_dir)
        self.report: Dict = {}

    def validate(self) -> Dict:
        """Validate QA green status"""
        print(f"🔍 Validating QA green status for: {self.test_dir}")

        if not self.test_dir.exists():
            return self._create_report(
                success=False,
                message=f"Test directory not found: {self.test_dir}",
                blocking_reason="NO_TEST_DIRECTORY"
            )

        # Run tests
        test_result = self._run_tests()

        # Validate results
        if not test_result:
            return self._create_report(
                success=False,
                message="Failed to run tests",
                blocking_reason="TEST_EXECUTION_FAILED"
            )

        # Check for violations
        violations = self._check_violations(test_result)

        if violations:
            return self._create_report(
                success=False,
                message=f"❌ QA NOT GREEN: {len(violations)} violations detected",
                test_result=test_result,
                violations=violations,
                blocking_reason="GOVERNANCE_SUPREMACY_RULE_VIOLATION"
            )
        else:
            return self._create_report(
                success=True,
                message=f"✅ QA IS GREEN: 100% pass ({test_result['passed']}/{test_result['total']} tests)",
                test_result=test_result,
                violations=[]
            )

    def _run_tests(self) -> Optional[Dict]:
        """Run the test suite and capture results"""
        try:
            # Detect test framework and run appropriate command
            if self._has_pytest():
                return self._run_pytest()
            elif self._has_jest():
                return self._run_jest()
            else:
                # Default to pytest
                return self._run_pytest()

        except Exception as e:
            print(f"❌ Error running tests: {e}", file=sys.stderr)
            return None

    def _has_pytest(self) -> bool:
        """Check if pytest is available"""
        try:
            subprocess.run(['pytest', '--version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _has_jest(self) -> bool:
        """Check if jest is available"""
        try:
            subprocess.run(['jest', '--version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _run_pytest(self) -> Dict:
        """Run pytest and parse results"""
        print("  Running pytest...")

        # Run pytest with JSON report
        cmd = [
            'python', '-m', 'pytest',
            str(self.test_dir),
            '-v',
            '--tb=short',
            '--color=no',
            '-W', 'error'  # Treat warnings as errors
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        # Parse output
        output = result.stdout + result.stderr
        lines = output.split('\n')

        # Extract test counts from pytest summary
        total = 0
        passed = 0
        failed = 0
        skipped = 0
        errors = 0
        warnings = 0

        for line in lines:
            # Look for summary line like: "5 passed in 0.12s"
            if 'passed' in line or 'failed' in line:
                # Parse counts
                passed_match = re.search(r'(\d+)\s+passed', line)
                failed_match = re.search(r'(\d+)\s+failed', line)
                skipped_match = re.search(r'(\d+)\s+skipped', line)
                error_match = re.search(r'(\d+)\s+error', line)

                if passed_match:
                    passed = int(passed_match.group(1))
                if failed_match:
                    failed = int(failed_match.group(1))
                if skipped_match:
                    skipped = int(skipped_match.group(1))
                if error_match:
                    errors = int(error_match.group(1))

            # Check for warnings
            if 'warning' in line.lower():
                warnings += 1

        total = passed + failed + skipped + errors

        # If we couldn't parse, try to at least get exit code info
        if total == 0 and result.returncode != 0:
            # Tests failed but we couldn't parse - log warning and assume failure
            print("⚠️  Warning: Could not parse test output, counts may be inaccurate", file=sys.stderr)
            failed = 1
            total = 1

        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'skipped': skipped,
            'errors': errors,
            'warnings': warnings,
            'exit_code': result.returncode,
            'output': output[:MAX_OUTPUT_LENGTH]
        }

    def _run_jest(self) -> Dict:
        """Run jest and parse results"""
        print("  Running jest...")

        cmd = ['jest', '--json', '--testPathPattern', str(self.test_dir)]
        result = subprocess.run(cmd, capture_output=True, text=True)

        # Parse JSON output
        try:
            data = json.loads(result.stdout)
            return {
                'total': data.get('numTotalTests', 0),
                'passed': data.get('numPassedTests', 0),
                'failed': data.get('numFailedTests', 0),
                'skipped': data.get('numPendingTests', 0),
                'errors': 0,
                'warnings': 0,
                'exit_code': result.returncode,
                'output': result.stdout[:MAX_OUTPUT_LENGTH]
            }
        except json.JSONDecodeError:
            # Fallback to text parsing
            return {
                'total': 0,
                'passed': 0,
                'failed': 1,  # Assume failure if can't parse
                'skipped': 0,
                'errors': 1,
                'warnings': 0,
                'exit_code': result.returncode,
                'output': result.stdout[:MAX_OUTPUT_LENGTH]
            }

    def _check_violations(self, test_result: Dict) -> list:
        """Check for Governance Supremacy Rule violations"""
        violations = []

        # Rule 1: ALL tests must pass (100%)
        if test_result['failed'] > 0:
            violations.append({
                'rule': 'GSR Pillar 1: 100% Pass Required',
                'violation': f"{test_result['failed']} test(s) failed",
                'severity': 'CRITICAL',
                'blocking': True,
                'message': f"❌ {test_result['failed']} tests FAILED. GSR requires 100% pass. No exceptions."
            })

        if test_result['errors'] > 0:
            violations.append({
                'rule': 'GSR Pillar 1: 100% Pass Required',
                'violation': f"{test_result['errors']} test error(s)",
                'severity': 'CRITICAL',
                'blocking': True,
                'message': f"❌ {test_result['errors']} tests had ERRORS. GSR requires 100% pass. No exceptions."
            })

        # Rule 2: Zero skipped tests
        if test_result['skipped'] > 0:
            violations.append({
                'rule': 'GSR Pillar 2: Zero Test Debt',
                'violation': f"{test_result['skipped']} test(s) skipped",
                'severity': 'CRITICAL',
                'blocking': True,
                'message': f"❌ {test_result['skipped']} tests SKIPPED. Zero test debt rule violated."
            })

        # Rule 3: Zero warnings
        if test_result['warnings'] > 0:
            violations.append({
                'rule': 'GSR: Zero Warnings',
                'violation': f"{test_result['warnings']} warning(s) detected",
                'severity': 'HIGH',
                'blocking': True,
                'message': f"❌ {test_result['warnings']} WARNINGS detected. Clean build required."
            })

        # Rule 4: Exit code must be 0
        if test_result['exit_code'] != 0:
            violations.append({
                'rule': 'GSR: Clean Exit Required',
                'violation': f"Non-zero exit code: {test_result['exit_code']}",
                'severity': 'CRITICAL',
                'blocking': True,
                'message': f"❌ Test exit code: {test_result['exit_code']}. Must be 0 for GREEN."
            })

        # Rule 5: Partial pass = FAILURE
        if test_result['total'] > 0:
            pass_rate = (test_result['passed'] / test_result['total']) * 100
            if 0 < pass_rate < 100:
                violations.append({
                    'rule': 'GSR Pillar 1: No Partial Passes',
                    'violation': f"Partial pass: {pass_rate:.1f}% ({test_result['passed']}/{test_result['total']})",
                    'severity': 'CRITICAL',
                    'blocking': True,
                    'message': f"❌ {pass_rate:.1f}% pass rate. GSR requires 100%. 99% = FAILURE."
                })

        return violations

    def _create_report(self, success: bool, message: str, test_result: Dict = None,
                      violations: list = None, blocking_reason: str = None) -> Dict:
        """Create the validation report"""
        report = {
            'success': success,
            'message': message,
            'timestamp': self._get_timestamp(),
            'test_directory': str(self.test_dir),
            'constitutional_authority': 'Governance Supremacy Rule (GSR)',
            'enforcement_level': 'BLOCKING'
        }

        if test_result:
            report['test_result'] = test_result

        if violations is not None:
            report['violations'] = violations
            report['violations_count'] = len(violations)

        if blocking_reason:
            report['blocking_reason'] = blocking_reason

        return report

    @staticmethod
    def _get_timestamp() -> str:
        """Get ISO 8601 timestamp"""
        return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Validate QA green status (100% pass requirement)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Constitutional Authority: Governance Supremacy Rule (GSR)
Enforcement: CI/CD blocking

Exit Codes:
  0 = QA is GREEN (100% pass)
  1 = QA is NOT GREEN (violations detected)
  2 = Validation error
'''
    )
    parser.add_argument('--test-dir', required=True, help='Test directory to validate')
    parser.add_argument('--json', action='store_true', help='Output JSON format')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    # Run validation
    validator = QAGreenValidator(args.test_dir)
    report = validator.validate()

    # Output report
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(report['message'])
        if report.get('violations') and args.verbose:
            print("\n📋 Violations:")
            for v in report['violations']:
                print(f"  - [{v['severity']}] {v['rule']}")
                print(f"    {v['message']}")

    # Exit with appropriate code
    sys.exit(0 if report['success'] else 1)


if __name__ == '__main__':
    main()
