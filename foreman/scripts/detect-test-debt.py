#!/usr/bin/env python3
"""
Test Debt Detection Script

Scans test directories for patterns that indicate test debt:
- .skip(), .todo(), .only() markers
- Commented out tests
- Stub tests with no assertions
- TODO/FIXME markers in tests
- Incomplete test infrastructure

Constitutional Authority: Zero Test Debt Constitutional Rule
Enforcement Level: CI/CD + Pre-commit hooks
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Set

# Constants
MAX_CONTENT_LENGTH = 100  # Maximum length for violation content snippets

# Test debt patterns to detect
TEST_DEBT_PATTERNS = {
    'skip_markers': [
        r'\.skip\s*\(',  # .skip()
        r'describe\.skip',  # describe.skip
        r'it\.skip',  # it.skip
        r'test\.skip',  # test.skip
        r'@pytest\.mark\.skip',  # pytest skip decorator
    ],
    'todo_markers': [
        r'\.todo\s*\(',  # .todo()
        r'test\.todo',  # test.todo
        r'it\.todo',  # it.todo
        r'@pytest\.mark\.xfail',  # pytest expected fail
    ],
    'only_markers': [
        r'\.only\s*\(',  # .only() (should not be committed)
        r'fdescribe',  # focused describe
        r'fit\s*\(',  # focused it
    ],
    'todo_comments': [
        r'#\s*TODO',  # TODO comments
        r'#\s*FIXME',  # FIXME comments
        r'//\s*TODO',  # JS/TS TODO
        r'//\s*FIXME',  # JS/TS FIXME
    ],
    'commented_tests': [
        r'#\s*def\s+test_',  # Commented Python test
        r'#\s*it\s*\(',  # Commented JS/TS test
        r'#\s*test\s*\(',  # Commented test
        r'//\s*it\s*\(',  # JS commented test
        r'//\s*test\s*\(',  # JS commented test
    ],
}


class TestDebtDetector:
    """Detects test debt in test files"""

    def __init__(self, test_dir: str):
        self.test_dir = Path(test_dir)
        self.violations: List[Dict] = []
        self.files_scanned = 0
        self.test_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.test.js', '.spec.js'}

    def scan(self) -> Dict:
        """Scan test directory for test debt"""
        print(f"🔍 Scanning for test debt in: {self.test_dir}")

        if not self.test_dir.exists():
            return self._create_report(success=False, message=f"Test directory not found: {self.test_dir}")

        # Find all test files
        test_files = self._find_test_files()

        if not test_files:
            return self._create_report(success=False, message="No test files found")

        # Scan each file
        for test_file in test_files:
            self._scan_file(test_file)
            self.files_scanned += 1

        # Generate report
        if self.violations:
            return self._create_report(
                success=False,
                message=f"❌ TEST DEBT DETECTED: {len(self.violations)} violations found"
            )
        else:
            return self._create_report(
                success=True,
                message=f"✅ ZERO TEST DEBT: Scanned {self.files_scanned} files, no violations found"
            )

    def _find_test_files(self) -> List[Path]:
        """Find all test files in the test directory"""
        test_files = []
        for ext in ['.py', '.js', '.ts', '.jsx', '.tsx']:
            test_files.extend(self.test_dir.rglob(f'*test*{ext}'))
            test_files.extend(self.test_dir.rglob(f'*spec*{ext}'))
        return list(set(test_files))  # Remove duplicates

    def _scan_file(self, file_path: Path):
        """Scan a single file for test debt patterns"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')

            # Check each pattern category
            for category, patterns in TEST_DEBT_PATTERNS.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        # Find line number
                        line_num = content[:match.start()].count('\n') + 1
                        line_content = lines[line_num - 1].strip() if line_num <= len(lines) else ""

                        self.violations.append({
                            'file': str(file_path.relative_to(self.test_dir.parent)),
                            'line': line_num,
                            'category': category,
                            'pattern': pattern,
                            'content': line_content[:MAX_CONTENT_LENGTH]
                        })

            # Check for stub tests (tests with no assertions)
            self._check_stub_tests(file_path, content, lines)

        except Exception as e:
            print(f"⚠️  Warning: Could not scan {file_path}: {e}", file=sys.stderr)

    def _check_stub_tests(self, file_path: Path, content: str, lines: List[str]):
        """Check for stub tests with no assertions"""
        # Python stub tests
        if file_path.suffix == '.py':
            # Find test functions
            test_func_pattern = r'def\s+(test_\w+)\s*\('
            for match in re.finditer(test_func_pattern, content):
                func_start = match.start()
                func_name = match.group(1)

                # Find function body (simplified - looks for next def or class)
                func_end = content.find('\ndef ', func_start + 1)
                if func_end == -1:
                    func_end = content.find('\nclass ', func_start + 1)
                if func_end == -1:
                    func_end = len(content)

                func_body = content[func_start:func_end]

                # Check if function has assertions or test operations
                has_assertion = any(keyword in func_body for keyword in [
                    'assert', 'assertEqual', 'assertTrue', 'assertFalse',
                    'expect(', 'toBe(', 'toEqual(', 'pytest.raises',
                    'validate(', 'raises(', 'self.assert'
                ])

                # Check if it's just a placeholder
                is_placeholder = 'pass' in func_body and len(func_body.strip().split('\n')) <= 3
                
                # Only flag if it has NO assertions AND is short OR is an obvious placeholder
                if (not has_assertion and len(func_body.strip().split('\n')) <= 5) or is_placeholder:
                    line_num = content[:func_start].count('\n') + 1
                    self.violations.append({
                        'file': str(file_path.relative_to(self.test_dir.parent)),
                        'line': line_num,
                        'category': 'stub_test',
                        'pattern': 'Test with no assertions',
                        'content': f'def {func_name}(...)'
                    })

    def _create_report(self, success: bool, message: str) -> Dict:
        """Create the final report"""
        return {
            'success': success,
            'message': message,
            'timestamp': self._get_timestamp(),
            'test_directory': str(self.test_dir),
            'files_scanned': self.files_scanned,
            'violations_count': len(self.violations),
            'violations': self.violations,
            'constitutional_authority': 'Zero Test Debt Constitutional Rule',
            'enforcement_level': 'BLOCKING'
        }

    @staticmethod
    def _get_timestamp() -> str:
        """Get ISO 8601 timestamp"""
        return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Detect test debt in test files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Constitutional Authority: Zero Test Debt Constitutional Rule
Enforcement: Pre-commit hooks + CI/CD

Exit Codes:
  0 = Zero test debt (success)
  1 = Test debt detected (failure)
  2 = Scan error
'''
    )
    parser.add_argument('--test-dir', required=True, help='Test directory to scan')
    parser.add_argument('--json', action='store_true', help='Output JSON format')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    # Run detection
    detector = TestDebtDetector(args.test_dir)
    report = detector.scan()

    # Output report
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(report['message'])
        if report['violations'] and args.verbose:
            print("\n📋 Violations:")
            for v in report['violations']:
                print(f"  - {v['file']}:{v['line']} [{v['category']}] {v['content']}")

    # Exit with appropriate code
    sys.exit(0 if report['success'] else 1)


if __name__ == '__main__':
    main()
