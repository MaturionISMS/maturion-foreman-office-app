#!/usr/bin/env python3
"""
QA-to-Red Test Existence Validation Script

Authority: BL-020 (BOOTSTRAP_EXECUTION_LEARNINGS.md)
Purpose: Verify QA-to-Red tests exist before subwave authorization

This script validates:
1. QA range exists in QA_CATALOG.md (BL-018)
2. QA semantics match subwave scope (BL-019)
3. Test files exist at claimed locations (BL-020)
4. Test coverage is complete for QA range

Usage:
  python validate-qa-tests-existence.py --subwave-spec wave2_builder_issues/SUBWAVE_2.5_qa_builder_Advanced_Flow_Scenarios.md
  python validate-qa-tests-existence.py --qa-range QA-211 QA-225 --test-file tests/wave2_0_qa_infrastructure/test_advanced_flow_scenarios.py
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional


class QATestValidator:
    """Validates QA-to-Red test existence and completeness"""
    
    def __init__(self, repo_root: Path = None):
        self.repo_root = repo_root or Path.cwd()
        self.qa_catalog_path = self.repo_root / "QA_CATALOG.md"
        self.tests_dir = self.repo_root / "tests"
        
    def parse_qa_range(self, qa_start: str, qa_end: str) -> List[int]:
        """Parse QA range (e.g., QA-211 to QA-225) into list of QA numbers"""
        start_num = int(qa_start.replace("QA-", ""))
        end_num = int(qa_end.replace("QA-", ""))
        return list(range(start_num, end_num + 1))
    
    def verify_qa_in_catalog(self, qa_numbers: List[int]) -> Tuple[bool, List[int]]:
        """Verify QA numbers exist in QA_CATALOG.md (BL-018)"""
        if not self.qa_catalog_path.exists():
            return False, qa_numbers
        
        catalog_content = self.qa_catalog_path.read_text()
        missing = []
        
        for qa_num in qa_numbers:
            qa_pattern = f"QA-{qa_num:03d}"
            if qa_pattern not in catalog_content:
                missing.append(qa_num)
        
        return len(missing) == 0, missing
    
    def get_qa_definitions(self, qa_numbers: List[int]) -> Dict[int, str]:
        """Extract QA definitions from QA_CATALOG.md"""
        if not self.qa_catalog_path.exists():
            return {}
        
        catalog_content = self.qa_catalog_path.read_text()
        definitions = {}
        
        for qa_num in qa_numbers:
            qa_pattern = f"QA-{qa_num:03d}"
            # Find line with QA-XXX: description
            match = re.search(rf"- {qa_pattern}:\s*(.+?)(?:\(|$)", catalog_content)
            if match:
                definitions[qa_num] = match.group(1).strip()
        
        return definitions
    
    def verify_test_file_exists(self, test_file_path: str) -> bool:
        """Verify test file exists in repository (BL-020)"""
        test_path = self.repo_root / test_file_path
        return test_path.exists() and test_path.is_file()
    
    def verify_test_coverage(self, test_file_path: str, qa_numbers: List[int]) -> Tuple[bool, List[int]]:
        """Verify test file contains tests for all QA numbers (BL-020)"""
        test_path = self.repo_root / test_file_path
        
        if not test_path.exists():
            return False, qa_numbers
        
        test_content = test_path.read_text()
        missing = []
        
        for qa_num in qa_numbers:
            # Look for test function with QA number in name or docstring
            qa_pattern = f"qa_{qa_num:03d}|QA-{qa_num:03d}"
            if not re.search(qa_pattern, test_content, re.IGNORECASE):
                missing.append(qa_num)
        
        return len(missing) == 0, missing
    
    def verify_tests_are_red(self, test_file_path: str, qa_numbers: List[int]) -> Tuple[bool, List[int]]:
        """Verify tests raise NotImplementedError (RED state)"""
        test_path = self.repo_root / test_file_path
        
        if not test_path.exists():
            return False, qa_numbers
        
        test_content = test_path.read_text()
        not_red = []
        
        for qa_num in qa_numbers:
            # Find test function for this QA
            test_match = re.search(
                rf"def test_qa_{qa_num:03d}.*?(?=\n    def |\nclass |\Z)",
                test_content,
                re.DOTALL
            )
            
            if test_match:
                test_body = test_match.group(0)
                if "NotImplementedError" not in test_body and "raise" not in test_body:
                    not_red.append(qa_num)
            else:
                not_red.append(qa_num)
        
        return len(not_red) == 0, not_red
    
    def validate_subwave(self, subwave_spec_path: str) -> Dict:
        """Validate complete subwave specification"""
        spec_path = self.repo_root / subwave_spec_path
        
        if not spec_path.exists():
            return {
                "valid": False,
                "error": f"Subwave spec file not found: {subwave_spec_path}"
            }
        
        spec_content = spec_path.read_text()
        
        # Extract QA range
        qa_range_match = re.search(r"QA-(\d+)\s+to\s+QA-(\d+)", spec_content)
        if not qa_range_match:
            return {
                "valid": False,
                "error": "Could not parse QA range from subwave spec"
            }
        
        qa_start = f"QA-{qa_range_match.group(1)}"
        qa_end = f"QA-{qa_range_match.group(2)}"
        qa_numbers = self.parse_qa_range(qa_start, qa_end)
        
        # Extract test file location
        test_file_match = re.search(r"\*\*Location:\*\*\s*`([^`]+)`", spec_content)
        if not test_file_match:
            return {
                "valid": False,
                "error": "Could not parse test file location from subwave spec"
            }
        
        test_file = test_file_match.group(1)
        
        # Run validations
        return self.validate_qa_range(qa_start, qa_end, test_file)
    
    def validate_qa_range(self, qa_start: str, qa_end: str, test_file_path: str) -> Dict:
        """Validate QA range has complete test coverage"""
        qa_numbers = self.parse_qa_range(qa_start, qa_end)
        
        result = {
            "valid": True,
            "qa_range": f"{qa_start} to {qa_end}",
            "qa_count": len(qa_numbers),
            "test_file": test_file_path,
            "checks": {}
        }
        
        # BL-018: Verify QA exists in catalog
        catalog_ok, catalog_missing = self.verify_qa_in_catalog(qa_numbers)
        result["checks"]["qa_catalog_exists"] = {
            "status": "PASS" if catalog_ok else "FAIL",
            "description": "QA range exists in QA_CATALOG.md (BL-018)",
            "missing": [f"QA-{n:03d}" for n in catalog_missing] if not catalog_ok else []
        }
        
        if not catalog_ok:
            result["valid"] = False
        
        # BL-019: Get QA definitions for semantic check (informational)
        qa_definitions = self.get_qa_definitions(qa_numbers)
        result["checks"]["qa_definitions"] = {
            "status": "INFO",
            "description": "QA definitions from catalog (verify semantic alignment manually)",
            "definitions": {f"QA-{k:03d}": v for k, v in qa_definitions.items()}
        }
        
        # BL-020: Verify test file exists
        test_file_exists = self.verify_test_file_exists(test_file_path)
        result["checks"]["test_file_exists"] = {
            "status": "PASS" if test_file_exists else "FAIL",
            "description": "Test file exists at claimed location (BL-020)",
            "path": test_file_path,
            "exists": test_file_exists
        }
        
        if not test_file_exists:
            result["valid"] = False
            return result  # Can't check further if file doesn't exist
        
        # BL-020: Verify test coverage
        coverage_ok, coverage_missing = self.verify_test_coverage(test_file_path, qa_numbers)
        result["checks"]["test_coverage"] = {
            "status": "PASS" if coverage_ok else "FAIL",
            "description": "All QA numbers have corresponding tests (BL-020)",
            "missing": [f"QA-{n:03d}" for n in coverage_missing] if not coverage_ok else []
        }
        
        if not coverage_ok:
            result["valid"] = False
        
        # BL-020: Verify tests are RED
        red_ok, not_red = self.verify_tests_are_red(test_file_path, qa_numbers)
        result["checks"]["tests_are_red"] = {
            "status": "PASS" if red_ok else "WARN",
            "description": "Tests raise NotImplementedError (RED state)",
            "not_red": [f"QA-{n:03d}" for n in not_red] if not red_ok else []
        }
        
        return result


def main():
    parser = argparse.ArgumentParser(
        description="Validate QA-to-Red test existence (BL-020)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate from subwave spec file
  python validate-qa-tests-existence.py --subwave-spec wave2_builder_issues/SUBWAVE_2.5_qa_builder_Advanced_Flow_Scenarios.md
  
  # Validate specific QA range
  python validate-qa-tests-existence.py --qa-range QA-211 QA-225 --test-file tests/wave2_0_qa_infrastructure/test_advanced_flow_scenarios.py
  
  # Output JSON for automation
  python validate-qa-tests-existence.py --qa-range QA-211 QA-225 --test-file tests/wave2_0_qa_infrastructure/test_advanced_flow_scenarios.py --json
        """
    )
    
    parser.add_argument(
        "--subwave-spec",
        help="Path to subwave specification file to validate"
    )
    
    parser.add_argument(
        "--qa-range",
        nargs=2,
        metavar=("QA_START", "QA_END"),
        help="QA range to validate (e.g., QA-211 QA-225)"
    )
    
    parser.add_argument(
        "--test-file",
        help="Path to test file to validate"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root directory (default: current directory)"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.subwave_spec and not (args.qa_range and args.test_file):
        parser.error("Either --subwave-spec or both --qa-range and --test-file must be provided")
    
    # Create validator
    validator = QATestValidator(repo_root=args.repo_root)
    
    # Run validation
    if args.subwave_spec:
        result = validator.validate_subwave(args.subwave_spec)
    else:
        result = validator.validate_qa_range(args.qa_range[0], args.qa_range[1], args.test_file)
    
    # Output results
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("\n" + "="*80)
        print("QA-to-Red Test Existence Validation (BL-020)")
        print("="*80)
        
        # Handle error case
        if 'error' in result:
            print(f"\n❌ ERROR: {result['error']}")
            print("="*80)
            sys.exit(1)
        
        print(f"\nQA Range: {result['qa_range']} ({result['qa_count']} components)")
        print(f"Test File: {result['test_file']}")
        print(f"\nOverall Status: {'✅ PASS' if result['valid'] else '❌ FAIL'}")
        print("\nValidation Checks:")
        print("-" * 80)
        
        for check_name, check_data in result['checks'].items():
            status_symbol = {
                "PASS": "✅",
                "FAIL": "❌",
                "WARN": "⚠️",
                "INFO": "ℹ️"
            }.get(check_data['status'], "?")
            
            print(f"\n{status_symbol} {check_data['status']}: {check_data['description']}")
            
            if check_data.get('missing'):
                print(f"   Missing: {', '.join(check_data['missing'])}")
            
            if check_data.get('not_red'):
                print(f"   Not RED: {', '.join(check_data['not_red'])}")
            
            if check_data.get('definitions'):
                print("   QA Definitions (verify semantic alignment):")
                for qa_id, definition in list(check_data['definitions'].items())[:5]:
                    print(f"     - {qa_id}: {definition}")
                if len(check_data['definitions']) > 5:
                    print(f"     ... and {len(check_data['definitions']) - 5} more")
        
        print("\n" + "="*80)
    
    # Exit with appropriate code
    sys.exit(0 if result['valid'] else 1)


if __name__ == "__main__":
    main()
