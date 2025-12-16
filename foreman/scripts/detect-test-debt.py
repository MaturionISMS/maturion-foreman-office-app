#!/usr/bin/env python3
"""
Test Debt Detection Script

Constitutional Authority: Zero Test Debt Constitutional Rule
Purpose: Detect all forms of test debt and block builds when found

This script scans test files for:
- Skipped tests (.skip(), .todo(), .only())
- Commented out tests
- Incomplete test stubs (no assertions)
- TODO/FIXME markers in tests
- Incomplete test infrastructure
"""

import os
import re
import sys
import json
from pathlib import Path
from typing import List, Dict, Tuple

class TestDebtDetector:
    """Detects test debt in test files"""
    
    # Patterns for different types of test debt
    SKIP_PATTERNS = [
        r'\.skip\(',
        r'\.todo\(',
        r'\.only\(',
        r'describe\.skip',
        r'it\.skip',
        r'test\.skip',
        r'xdescribe\(',
        r'xit\(',
        r'@pytest\.mark\.skip',
        r'@pytest\.mark\.xfail',
        r'@unittest\.skip',
    ]
    
    # Patterns for conditional suppression (test dodging)
    SUPPRESSION_PATTERNS = [
        r'\|\|\s*true\b',  # || true
        r'2>/dev/null',    # Stderr suppression
        r'2>&1\s*\|\s*true',  # Combined suppression
        r'--passWithNoTests',  # Jest pass with no tests
        r'-x\s+\|\|\s*true',  # Exit on first failure suppressed
        r';\s*true\s*$',  # Command followed by true to ignore exit code
    ]
    
    TODO_PATTERNS = [
        r'#\s*TODO',
        r'#\s*FIXME',
        r'#\s*XXX',
        r'//\s*TODO',
        r'//\s*FIXME',
        r'//\s*XXX',
    ]
    
    STUB_PATTERNS = [
        r'def\s+test_\w+\(.*?\):\s*(?:#.*?\n\s*)*pass\s*(?:\n|$)',  # Python stub tests
        r'it\([\'"].*?[\'"]\s*,\s*\(\)\s*=>\s*\{\s*\}\s*\)',  # JS/TS empty tests
        r'expect\(true\)\.toBe\(true\)',  # Meaningless assertions
    ]
    
    def __init__(self, test_dir: str = "tests"):
        self.test_dir = Path(test_dir)
        self.violations: List[Dict] = []
        
    def scan(self) -> Tuple[bool, List[Dict]]:
        """
        Scan test directory for test debt.
        
        Returns:
            Tuple of (has_debt: bool, violations: List[Dict])
        """
        if not self.test_dir.exists():
            return False, []
            
        # Scan all test files
        test_files = self._find_test_files()
        
        for test_file in test_files:
            self._scan_file(test_file)
        
        # Also scan CI/workflow files for suppression patterns
        self._scan_ci_files()
            
        has_debt = len(self.violations) > 0
        return has_debt, self.violations
        
    def _scan_ci_files(self):
        """Scan CI/workflow files and scripts for suppression patterns"""
        ci_paths = [
            Path(".github/workflows"),
            Path(".github/actions"),
            Path("scripts"),
        ]
        
        for ci_path in ci_paths:
            if not ci_path.exists():
                continue
                
            # Find YAML and shell script files
            ci_files = list(ci_path.glob("**/*.yml"))
            ci_files.extend(ci_path.glob("**/*.yaml"))
            ci_files.extend(ci_path.glob("**/*.sh"))
            
            for ci_file in ci_files:
                self._scan_file_for_suppression(ci_file)
    
    def _scan_file_for_suppression(self, file_path: Path):
        """Scan a file specifically for suppression patterns"""
        try:
            content = file_path.read_text()
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                # Check only suppression patterns in CI files
                for pattern in self.SUPPRESSION_PATTERNS:
                    if re.search(pattern, line):
                        self.violations.append({
                            "type": "test_suppression",
                            "file": str(file_path),
                            "line": line_num,
                            "content": line.strip(),
                            "pattern": pattern,
                            "severity": "CRITICAL",
                            "message": "Test failure suppression detected in CI/script - hiding failures is forbidden",
                            "remedy": "Remove suppression and fix the underlying failures"
                        })
        except Exception as e:
            # Silently skip files that can't be read
            pass
        
    def _find_test_files(self) -> List[Path]:
        """Find all test files in test directory"""
        test_files = []
        
        # Python test files
        test_files.extend(self.test_dir.glob("**/test_*.py"))
        test_files.extend(self.test_dir.glob("**/*_test.py"))
        
        # JavaScript/TypeScript test files
        test_files.extend(self.test_dir.glob("**/*.test.js"))
        test_files.extend(self.test_dir.glob("**/*.test.ts"))
        test_files.extend(self.test_dir.glob("**/*.spec.js"))
        test_files.extend(self.test_dir.glob("**/*.spec.ts"))
        
        return list(test_files)
        
    def _scan_file(self, file_path: Path):
        """Scan a single test file for debt"""
        try:
            content = file_path.read_text()
            lines = content.split('\n')
            
            # Check for skip patterns
            for line_num, line in enumerate(lines, 1):
                # Skip patterns
                for pattern in self.SKIP_PATTERNS:
                    if re.search(pattern, line):
                        self.violations.append({
                            "type": "skipped_test",
                            "file": str(file_path),
                            "line": line_num,
                            "content": line.strip(),
                            "pattern": pattern,
                            "severity": "HIGH",
                            "message": "Skipped test detected - tests must not be skipped",
                            "remedy": "Use Enhancement Parking Lot (foreman/admin/enhancement-parking-lot-spec.md) to track incomplete features"
                        })
                        
                # TODO/FIXME patterns
                for pattern in self.TODO_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        self.violations.append({
                            "type": "todo_marker",
                            "file": str(file_path),
                            "line": line_num,
                            "content": line.strip(),
                            "pattern": pattern,
                            "severity": "HIGH",
                            "message": "TODO/FIXME marker in test - tests must be complete",
                            "remedy": "Complete the test or use Enhancement Parking Lot to track future work"
                        })
                        
                # Suppression patterns (test dodging)
                for pattern in self.SUPPRESSION_PATTERNS:
                    if re.search(pattern, line):
                        self.violations.append({
                            "type": "test_suppression",
                            "file": str(file_path),
                            "line": line_num,
                            "content": line.strip(),
                            "pattern": pattern,
                            "severity": "CRITICAL",
                            "message": "Test failure suppression detected - hiding failures is forbidden",
                            "remedy": "Fix failing tests or use Enhancement Parking Lot for incomplete features"
                        })
                        
            # Check for stub patterns (multi-line)
            for pattern in self.STUB_PATTERNS:
                for match in re.finditer(pattern, content, re.MULTILINE):
                    line_num = content[:match.start()].count('\n') + 1
                    self.violations.append({
                        "type": "stub_test",
                        "file": str(file_path),
                        "line": line_num,
                        "content": match.group(0).strip()[:100],
                        "pattern": pattern,
                        "severity": "HIGH",
                        "message": "Stub or incomplete test detected",
                        "remedy": "Complete the test with proper assertions or remove it"
                    })
                    
            # Check for commented out test blocks
            self._check_commented_tests(file_path, lines)
            
        except Exception as e:
            print(f"Warning: Could not scan {file_path}: {e}", file=sys.stderr)
            
    def _check_commented_tests(self, file_path: Path, lines: List[str]):
        """Check for blocks of commented out test code"""
        in_comment_block = False
        comment_start = 0
        comment_lines = []
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Check if line is a comment
            if stripped.startswith('#') or stripped.startswith('//'):
                if not in_comment_block:
                    in_comment_block = True
                    comment_start = line_num
                comment_lines.append(stripped)
            else:
                # End of comment block
                if in_comment_block and len(comment_lines) >= 3:
                    # Check if comment block looks like test code
                    comment_text = ' '.join(comment_lines)
                    if any(keyword in comment_text for keyword in ['test', 'it(', 'describe(', 'def test_', 'expect(', 'assert']):
                        self.violations.append({
                            "type": "commented_test",
                            "file": str(file_path),
                            "line": comment_start,
                            "content": f"Commented test block ({len(comment_lines)} lines)",
                            "severity": "HIGH",
                            "message": "Commented out test code detected - remove or uncomment",
                            "remedy": "Uncomment and fix the test, or delete if no longer needed"
                        })
                        
                in_comment_block = False
                comment_lines = []
                
    def report(self) -> str:
        """Generate a human-readable report of violations"""
        if not self.violations:
            return "✅ No test debt detected"
            
        report_lines = [
            "❌ TEST DEBT DETECTED - BUILD BLOCKED",
            "=" * 80,
            f"Total violations: {len(self.violations)}",
            "",
            "GREEN must never be achieved by omission.",
            "",
            "VIOLATIONS:",
            ""
        ]
        
        # Group by type
        by_type = {}
        for violation in self.violations:
            vtype = violation['type']
            if vtype not in by_type:
                by_type[vtype] = []
            by_type[vtype].append(violation)
            
        for vtype, violations in sorted(by_type.items()):
            report_lines.append(f"\n{vtype.upper().replace('_', ' ')}: {len(violations)}")
            report_lines.append("-" * 80)
            for i, v in enumerate(violations[:10], 1):  # Show first 10 of each type
                report_lines.append(f"\n{i}. File: {v['file']}")
                report_lines.append(f"   Line: {v['line']}")
                report_lines.append(f"   Pattern: {v.get('pattern', 'N/A')}")
                report_lines.append(f"   Code: {v['content'][:100]}")
                report_lines.append(f"   ❌ Issue: {v['message']}")
                report_lines.append(f"   ✅ Fix: {v.get('remedy', 'See Zero Test Debt Constitutional Rule')}")
            if len(violations) > 10:
                report_lines.append(f"\n... and {len(violations) - 10} more")
            report_lines.append("")
            
        report_lines.extend([
            "=" * 80,
            "Build BLOCKED by Zero Test Debt Constitutional Rule",
            "",
            "All test debt must be fixed before merge.",
            "",
            "📋 APPROVED ALTERNATIVE FOR INCOMPLETE FEATURES:",
            "   Use Enhancement Parking Lot to explicitly track deferred work:",
            "   foreman/admin/enhancement-parking-lot-spec.md",
            "",
            "For complete guidance, see:",
            "   foreman/governance/zero-test-debt-constitutional-rule.md"
        ])
        
        return '\n'.join(report_lines)
        
    def report_json(self) -> str:
        """Generate JSON report of violations"""
        return json.dumps({
            "test_debt_detected": len(self.violations) > 0,
            "violation_count": len(self.violations),
            "violations": self.violations,
            "status": "BLOCKED" if self.violations else "PASS"
        }, indent=2)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Detect test debt in test files",
        epilog="Constitutional Authority: Zero Test Debt Constitutional Rule"
    )
    parser.add_argument(
        '--test-dir',
        default='tests',
        help='Directory containing test files (default: tests)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    
    args = parser.parse_args()
    
    # Run detection
    detector = TestDebtDetector(args.test_dir)
    has_debt, violations = detector.scan()
    
    # Output results
    if args.json:
        print(detector.report_json())
    else:
        print(detector.report())
        
    # Exit with error code if debt detected
    sys.exit(1 if has_debt else 0)


if __name__ == '__main__':
    main()
