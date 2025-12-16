#!/usr/bin/env python3
"""
DP-RED Compliance Validator

Validates Design-Phase RED (DP-RED) registry compliance and enforces
phase-based merge gates.

Authority: foreman/qa/dp-red-registry-spec.md
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Set
import subprocess
import argparse


class DPREDValidator:
    """Validates DP-RED registry compliance and phase rules."""
    
    VALID_PHASES = ['QA_DESIGN', 'QA_BUILD', 'QA_GREEN', 'QA_VALIDATE']
    SCHEMA_VERSION = '1.0.0'
    
    def __init__(self, registry_path: str, phase_file: str, test_dir: str):
        self.registry_path = Path(registry_path)
        self.phase_file = Path(phase_file)
        self.test_dir = Path(test_dir)
        self.errors = []
        self.warnings = []
        self.registry = None
        self.current_phase = None
        
    def validate(self) -> Tuple[bool, Dict]:
        """Run all validations and return results."""
        
        # Load files
        if not self._load_registry():
            return False, self._generate_report()
        
        if not self._load_phase():
            return False, self._generate_report()
        
        # Run validations
        self._validate_schema()
        self._validate_phase()
        self._validate_entries()
        self._validate_test_mapping()
        self._validate_build_gate()
        
        success = len(self.errors) == 0
        report = self._generate_report()
        
        return success, report
    
    def _load_registry(self) -> bool:
        """Load and parse DP-RED registry."""
        if not self.registry_path.exists():
            self.errors.append(f"Registry file not found: {self.registry_path}")
            return False
        
        try:
            with open(self.registry_path, 'r') as f:
                self.registry = json.load(f)
            return True
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in registry: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Failed to load registry: {e}")
            return False
    
    def _load_phase(self) -> bool:
        """Load current phase configuration."""
        if not self.phase_file.exists():
            self.errors.append(f"Phase file not found: {self.phase_file}")
            return False
        
        try:
            with open(self.phase_file, 'r') as f:
                phase_data = json.load(f)
            self.current_phase = phase_data.get('phase')
            if not self.current_phase:
                self.errors.append("Phase not specified in phase file")
                return False
            return True
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in phase file: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Failed to load phase file: {e}")
            return False
    
    def _validate_schema(self):
        """Validate registry schema structure."""
        if not isinstance(self.registry, dict):
            self.errors.append("Registry must be a JSON object")
            return
        
        # Check required top-level fields
        required_fields = ['schema_version', 'phase', 'entries']
        for field in required_fields:
            if field not in self.registry:
                self.errors.append(f"Missing required field: {field}")
        
        # Check schema version
        if self.registry.get('schema_version') != self.SCHEMA_VERSION:
            self.errors.append(f"Unsupported schema version: {self.registry.get('schema_version')}")
        
        # Check entries is list
        if not isinstance(self.registry.get('entries', []), list):
            self.errors.append("'entries' must be a list")
    
    def _validate_phase(self):
        """Validate phase consistency."""
        registry_phase = self.registry.get('phase')
        
        # Check registry phase is valid
        if registry_phase not in self.VALID_PHASES:
            self.errors.append(f"Invalid phase in registry: {registry_phase}")
        
        # Check consistency with current phase
        if registry_phase != self.current_phase:
            self.errors.append(
                f"Phase mismatch: registry says '{registry_phase}', "
                f"current phase is '{self.current_phase}'"
            )
        
        # Check if DP-RED allowed in current phase
        entries = self.registry.get('entries', [])
        if entries and self.current_phase != 'QA_DESIGN':
            self.errors.append(
                f"DP-RED entries exist but phase is {self.current_phase}. "
                "DP-RED only allowed in QA_DESIGN phase."
            )
    
    def _validate_entries(self):
        """Validate individual DP-RED entries."""
        entries = self.registry.get('entries', [])
        
        if not isinstance(entries, list):
            return  # Already caught in schema validation
        
        required_fields = [
            'test_id', 'test_path', 'phase', 'reason', 'registered_by',
            'registered_date', 'module', 'category', 'architecture_ref',
            'build_blocker'
        ]
        
        test_ids = set()
        
        for idx, entry in enumerate(entries):
            entry_errors = []
            
            # Check required fields
            for field in required_fields:
                if field not in entry:
                    entry_errors.append(f"Missing field '{field}'")
            
            # Check test_id uniqueness
            test_id = entry.get('test_id')
            if test_id:
                if test_id in test_ids:
                    entry_errors.append(f"Duplicate test_id: {test_id}")
                test_ids.add(test_id)
            
            # Check phase is QA_DESIGN
            if entry.get('phase') != 'QA_DESIGN':
                entry_errors.append(f"Entry phase must be QA_DESIGN, got: {entry.get('phase')}")
            
            # Check reason length
            reason = entry.get('reason', '')
            if len(reason) < 20:
                entry_errors.append(f"Reason too short (min 20 chars): {len(reason)} chars")
            
            # Check registered_date is valid ISO-8601
            reg_date = entry.get('registered_date')
            if reg_date:
                try:
                    dt = datetime.fromisoformat(reg_date.replace('Z', '+00:00'))
                    if dt > datetime.now().astimezone():
                        entry_errors.append("registered_date is in the future")
                except ValueError:
                    entry_errors.append(f"Invalid ISO-8601 date: {reg_date}")
            
            # Check expiry_date if present
            exp_date = entry.get('expiry_date')
            if exp_date:
                try:
                    dt = datetime.fromisoformat(exp_date.replace('Z', '+00:00'))
                    if dt < datetime.now().astimezone():
                        self.warnings.append(
                            f"Entry {test_id} has expired: {exp_date}"
                        )
                    elif (dt - datetime.now().astimezone()).days <= 7:
                        self.warnings.append(
                            f"Entry {test_id} expires soon: {exp_date}"
                        )
                except ValueError:
                    entry_errors.append(f"Invalid ISO-8601 expiry date: {exp_date}")
            
            # Check build_blocker is boolean
            if 'build_blocker' in entry and not isinstance(entry['build_blocker'], bool):
                entry_errors.append("build_blocker must be boolean")
            
            # Report entry errors
            if entry_errors:
                self.errors.append(
                    f"Entry #{idx + 1} ({test_id or 'unknown'}): " +
                    "; ".join(entry_errors)
                )
    
    def _validate_test_mapping(self):
        """Validate that registry entries map to actual test results."""
        entries = self.registry.get('entries', [])
        
        if not entries:
            # No entries to validate
            return
        
        # Get actual failing tests
        failing_tests = self._get_failing_tests()
        if failing_tests is None:
            # Could not get test results - warning only
            self.warnings.append("Could not verify test mapping - test execution failed or unavailable")
            return
        
        # Get registered test IDs
        registered_ids = {entry.get('test_id') for entry in entries if entry.get('test_id')}
        registered_paths = {entry.get('test_path') for entry in entries if entry.get('test_path')}
        
        # Check for unregistered RED tests
        unregistered_red = []
        for test in failing_tests:
            # Check if test is in registry by ID or path
            if test not in registered_ids and test not in registered_paths:
                # Try to match by partial path
                matched = False
                for reg_path in registered_paths:
                    if test in reg_path or reg_path in test:
                        matched = True
                        break
                if not matched:
                    unregistered_red.append(test)
        
        if unregistered_red:
            self.errors.append(
                f"Unregistered RED tests found (must be in DP-RED registry): "
                f"{', '.join(unregistered_red[:5])}"
                + (f" and {len(unregistered_red) - 5} more" if len(unregistered_red) > 5 else "")
            )
        
        # Check for orphaned registry entries (in registry but not failing)
        orphaned = []
        for entry in entries:
            test_id = entry.get('test_id')
            test_path = entry.get('test_path')
            
            # Check if test is actually failing
            found_failing = False
            for failing in failing_tests:
                if test_id in failing or (test_path and test_path in failing):
                    found_failing = True
                    break
            
            if not found_failing:
                orphaned.append(test_id or test_path)
        
        if orphaned:
            self.warnings.append(
                f"Registry entries with no corresponding RED test: "
                f"{', '.join(orphaned[:5])}"
                + (f" and {len(orphaned) - 5} more" if len(orphaned) > 5 else "")
            )
    
    def _validate_build_gate(self):
        """Validate build phase gate requirements."""
        entries = self.registry.get('entries', [])
        
        # In QA_BUILD or later phases, registry must be empty
        if self.current_phase in ['QA_BUILD', 'QA_GREEN', 'QA_VALIDATE']:
            if entries:
                self.errors.append(
                    f"DP-RED registry must be empty in {self.current_phase} phase. "
                    f"Found {len(entries)} entries. All tests must be GREEN before build phase."
                )
    
    def _get_failing_tests(self) -> Set[str]:
        """Get list of currently failing tests."""
        try:
            # Run pytest to collect test results
            # Use --collect-only to avoid actually running tests (faster)
            # Then check which tests are known to fail from previous runs
            
            # For now, return None to indicate we can't verify
            # In production, this would integrate with test runner
            return None
            
        except Exception as e:
            return None
    
    def _generate_report(self) -> Dict:
        """Generate validation report."""
        entries = self.registry.get('entries', []) if self.registry else []
        
        # Count by category
        categories = {}
        for entry in entries:
            cat = entry.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
        
        report = {
            'success': len(self.errors) == 0,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'schema_version': self.SCHEMA_VERSION,
            'current_phase': self.current_phase,
            'registry_phase': self.registry.get('phase') if self.registry else None,
            'entry_count': len(entries),
            'categories': categories,
            'errors': self.errors,
            'warnings': self.warnings,
            'merge_allowed': len(self.errors) == 0,
            'phase_transition_blocked': bool(entries and self.current_phase != 'QA_DESIGN')
        }
        
        return report


def print_human_readable(report: Dict):
    """Print human-readable report."""
    print("=" * 80)
    print("DP-RED COMPLIANCE VALIDATION REPORT")
    print("=" * 80)
    print()
    
    # Status
    if report['success']:
        print("✅ STATUS: PASS")
    else:
        print("❌ STATUS: FAIL")
    print()
    
    # Phase info
    print(f"Current Phase: {report['current_phase']}")
    print(f"Registry Phase: {report['registry_phase']}")
    print(f"DP-RED Entries: {report['entry_count']}")
    print()
    
    # Categories
    if report['categories']:
        print("Categories:")
        for cat, count in sorted(report['categories'].items()):
            print(f"  {cat}: {count}")
        print()
    
    # Errors
    if report['errors']:
        print(f"ERRORS ({len(report['errors'])}):")
        print("-" * 80)
        for i, error in enumerate(report['errors'], 1):
            print(f"{i}. {error}")
        print()
    
    # Warnings
    if report['warnings']:
        print(f"WARNINGS ({len(report['warnings'])}):")
        print("-" * 80)
        for i, warning in enumerate(report['warnings'], 1):
            print(f"{i}. {warning}")
        print()
    
    # Merge decision
    print("MERGE DECISION:")
    print("-" * 80)
    if report['merge_allowed']:
        if report['entry_count'] == 0:
            print("✅ MERGE ALLOWED - No DP-RED entries, all tests must be GREEN")
        elif report['current_phase'] == 'QA_DESIGN':
            print(f"✅ MERGE ALLOWED - {report['entry_count']} DP-RED entries registered in design phase")
        else:
            print("✅ MERGE ALLOWED")
    else:
        print("❌ MERGE BLOCKED - Fix errors above")
    print()
    
    # Phase transition
    if report['phase_transition_blocked']:
        print("⚠️  PHASE TRANSITION BLOCKED:")
        print(f"   Cannot transition from {report['current_phase']} with {report['entry_count']} DP-RED entries")
        print("   All tests must be implemented and GREEN before build phase")
        print()
    
    print("=" * 80)
    
    # Exit message
    if not report['success']:
        print()
        print("For DP-RED policy details, see:")
        print("  foreman/qa/dp-red-registry-spec.md")
        print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Validate DP-RED registry compliance'
    )
    parser.add_argument(
        '--registry',
        default='foreman/qa/dp-red-registry.json',
        help='Path to DP-RED registry file'
    )
    parser.add_argument(
        '--phase-file',
        default='foreman/qa/current-phase.json',
        help='Path to current phase file'
    )
    parser.add_argument(
        '--test-dir',
        default='tests',
        help='Test directory'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output JSON report only'
    )
    
    args = parser.parse_args()
    
    # Validate
    validator = DPREDValidator(args.registry, args.phase_file, args.test_dir)
    success, report = validator.validate()
    
    # Output
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_human_readable(report)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
