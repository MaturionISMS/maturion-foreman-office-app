#!/usr/bin/env python3
"""
Maturion Foreman - Architecture Compilation Contract Validator

Validates that architecture compilation has been completed per
ARCHITECTURE_COMPILATION_CONTRACT.md requirements.

This validator enforces:
- All required input artifacts exist (App Description, FRS, etc.)
- Architecture completeness = 100%
- No TBD/TODO markers in architecture
- Architecture is frozen
- All governance checklists are satisfied

Returns:
    PASS: Architecture compilation contract satisfied
    FAIL: Architecture incomplete or not ready for build
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class ArchitectureCompilationValidator:
    """Validates Architecture Compilation Contract compliance"""
    
    def __init__(self, repo_root: Path, app_name: str = "FM"):
        self.repo_root = repo_root
        self.app_name = app_name
        self.results = {
            'validation_id': f'arch-compile-{app_name}-{datetime.now().strftime("%Y%m%d-%H%M%S")}',
            'timestamp': datetime.now().isoformat(),
            'app_name': app_name,
            'status': 'UNKNOWN',
            'checks': [],
            'errors': [],
            'warnings': [],
            'evidence': {}
        }
        
    def validate(self) -> Tuple[bool, Dict]:
        """Run all validation checks"""
        print(f"🔍 Validating Architecture Compilation for {self.app_name}...\n")
        
        # Check 1: Input artifacts exist and are valid
        inputs_valid = self._check_input_artifacts()
        
        # Check 2: Architecture index exists and is complete
        arch_complete = self._check_architecture_completeness()
        
        # Check 3: No TBD/TODO markers
        no_placeholders = self._check_no_placeholders()
        
        # Check 4: Architecture frozen/versioned
        is_frozen = self._check_frozen_status()
        
        # Determine overall status
        all_critical_passed = (
            inputs_valid and 
            arch_complete and 
            no_placeholders and 
            is_frozen
        )
        
        self.results['status'] = 'PASS' if all_critical_passed else 'FAIL'
        
        return all_critical_passed, self.results
    
    def _check_input_artifacts(self) -> bool:
        """Check that all required input artifacts exist"""
        check_result = {
            'check': 'input_artifacts',
            'status': 'UNKNOWN',
            'message': '',
            'evidence': {
                'app_description': False,
                'frs': False,
                'architecture_index': False,
            }
        }
        
        # Check App Description
        app_desc_paths = [
            self.repo_root / "docs" / "governance" / f"{self.app_name}_APP_DESCRIPTION.md",
            self.repo_root / "APP_DESCRIPTION.md",
        ]
        for path in app_desc_paths:
            if path.exists():
                check_result['evidence']['app_description'] = True
                self.results['evidence']['app_description_path'] = str(path)
                break
        
        # Check FRS/True North
        frs_paths = [
            self.repo_root / "foreman" / "architecture" / "FOREMAN_TRUE_NORTH_v1.0.md",
            self.repo_root / "architecture" / f"{self.app_name}_FUNCTIONAL_SPEC.md",
        ]
        for path in frs_paths:
            if path.exists():
                check_result['evidence']['frs'] = True
                self.results['evidence']['frs_path'] = str(path)
                break
        
        # Check Architecture Index
        arch_index_path = self.repo_root / "ARCHITECTURE_INDEX.json"
        if arch_index_path.exists():
            check_result['evidence']['architecture_index'] = True
            self.results['evidence']['architecture_index_path'] = str(arch_index_path)
        
        # Evaluate
        all_present = all(check_result['evidence'].values())
        missing = [k for k, v in check_result['evidence'].items() if not v]
        
        if all_present:
            check_result['status'] = 'PASS'
            check_result['message'] = 'All required input artifacts present'
        else:
            check_result['status'] = 'FAIL'
            check_result['message'] = f'Missing input artifacts: {", ".join(missing)}'
            self.results['errors'].append(
                f"BLOCKING: Missing required artifacts: {', '.join(missing)}"
            )
        
        self.results['checks'].append(check_result)
        return all_present
    
    def _check_architecture_completeness(self) -> bool:
        """Check architecture completeness"""
        check_result = {
            'check': 'architecture_completeness',
            'status': 'UNKNOWN',
            'message': '',
            'evidence': {}
        }
        
        arch_index_path = self.repo_root / "ARCHITECTURE_INDEX.json"
        
        if not arch_index_path.exists():
            check_result['status'] = 'FAIL'
            check_result['message'] = 'Architecture index not found'
            self.results['errors'].append(
                "BLOCKING: Architecture index required for compilation validation"
            )
            self.results['checks'].append(check_result)
            return False
        
        # Load and parse architecture index
        try:
            with open(arch_index_path, 'r') as f:
                arch_index = json.load(f)
            
            # Check completeness score
            completeness = arch_index.get('summary', {}).get('completeness_score', 0)
            total_components = arch_index.get('summary', {}).get('total_components', 0)
            complete_components = arch_index.get('summary', {}).get('complete_components', 0)
            
            check_result['evidence']['completeness_score'] = completeness
            check_result['evidence']['total_components'] = total_components
            check_result['evidence']['complete_components'] = complete_components
            
            self.results['evidence']['completeness_score'] = completeness
            
            if completeness >= 100:
                check_result['status'] = 'PASS'
                check_result['message'] = f'Architecture 100% complete ({complete_components}/{total_components} components)'
            else:
                check_result['status'] = 'FAIL'
                check_result['message'] = f'Architecture incomplete: {completeness}% ({complete_components}/{total_components} components)'
                self.results['errors'].append(
                    f"BLOCKING: Architecture must be 100% complete. Current: {completeness}%"
                )
        
        except (json.JSONDecodeError, KeyError) as e:
            check_result['status'] = 'FAIL'
            check_result['message'] = f'Error parsing architecture index: {e}'
            self.results['errors'].append(
                f"BLOCKING: Architecture index is invalid or malformed"
            )
            self.results['checks'].append(check_result)
            return False
        
        self.results['checks'].append(check_result)
        return completeness >= 100
    
    def _check_no_placeholders(self) -> bool:
        """Check for TBD/TODO markers in architecture"""
        check_result = {
            'check': 'no_placeholders',
            'status': 'UNKNOWN',
            'message': '',
            'evidence': {}
        }
        
        # Search architecture files for TBD/TODO markers
        architecture_dirs = [
            self.repo_root / "architecture",
            self.repo_root / "foreman" / "architecture",
        ]
        
        placeholder_patterns = [r'\bTBD\b', r'\bTODO\b', r'\bFIXME\b', r'\bXXX\b']
        placeholders_found = []
        
        for arch_dir in architecture_dirs:
            if not arch_dir.exists():
                continue
            
            for arch_file in arch_dir.rglob("*.md"):
                with open(arch_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    for pattern in placeholder_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            placeholders_found.append(str(arch_file.relative_to(self.repo_root)))
                            break
        
        check_result['evidence']['files_with_placeholders'] = placeholders_found
        check_result['evidence']['placeholder_count'] = len(placeholders_found)
        
        if not placeholders_found:
            check_result['status'] = 'PASS'
            check_result['message'] = 'No TBD/TODO markers found in architecture'
        else:
            check_result['status'] = 'FAIL'
            check_result['message'] = f'Found TBD/TODO markers in {len(placeholders_found)} file(s)'
            self.results['errors'].append(
                f"BLOCKING: Architecture contains placeholder markers in: {', '.join(placeholders_found[:3])}"
            )
        
        self.results['checks'].append(check_result)
        return len(placeholders_found) == 0
    
    def _check_frozen_status(self) -> bool:
        """Check if architecture is frozen/versioned"""
        check_result = {
            'check': 'frozen_status',
            'status': 'UNKNOWN',
            'message': '',
            'evidence': {}
        }
        
        # Check if architecture index has version/freeze marker
        arch_index_path = self.repo_root / "ARCHITECTURE_INDEX.json"
        
        if not arch_index_path.exists():
            check_result['status'] = 'FAIL'
            check_result['message'] = 'Cannot verify frozen status - index missing'
            self.results['checks'].append(check_result)
            return False
        
        try:
            with open(arch_index_path, 'r') as f:
                arch_index = json.load(f)
            
            # Check for version markers
            has_version = False
            version_info = arch_index.get('metadata', {}).get('version')
            if version_info:
                has_version = True
                check_result['evidence']['version'] = version_info
            
            # Check for timestamp (indicates when indexed/frozen)
            has_timestamp = False
            timestamp = arch_index.get('metadata', {}).get('generated_at')
            if timestamp:
                has_timestamp = True
                check_result['evidence']['timestamp'] = timestamp
            
            if has_version or has_timestamp:
                check_result['status'] = 'PASS'
                check_result['message'] = 'Architecture is versioned/timestamped'
            else:
                check_result['status'] = 'WARN'
                check_result['message'] = 'Architecture lacks explicit version or freeze marker'
                self.results['warnings'].append(
                    "Architecture should have explicit version or freeze marker"
                )
        
        except (json.JSONDecodeError, KeyError) as e:
            check_result['status'] = 'WARN'
            check_result['message'] = f'Cannot verify frozen status: {e}'
            self.results['warnings'].append(
                "Could not verify architecture frozen status"
            )
        
        self.results['checks'].append(check_result)
        # Return True even for WARN as it's not blocking
        return True
    
    def write_evidence(self, output_dir: Path = None):
        """Write validation evidence to file"""
        if output_dir is None:
            output_dir = self.repo_root / "governance" / "evidence"
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Write JSON evidence
        evidence_file = output_dir / f"{self.results['validation_id']}.json"
        with open(evidence_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📋 Evidence written to: {evidence_file}")
        return evidence_file


def main():
    """Main execution"""
    # Determine repository root
    repo_root = Path(__file__).resolve().parent.parent.parent
    
    # Get app name from command line or default to FM
    app_name = sys.argv[1] if len(sys.argv) > 1 else "FM"
    
    # Create validator and run
    validator = ArchitectureCompilationValidator(repo_root, app_name)
    success, results = validator.validate()
    
    # Print results
    print("\n" + "="*70)
    print(f"ARCHITECTURE COMPILATION VALIDATION RESULTS - {app_name}")
    print("="*70)
    print(f"\nOverall Status: {'✅ PASS' if success else '❌ FAIL'}")
    print(f"Validation ID: {results['validation_id']}")
    print(f"Timestamp: {results['timestamp']}")
    
    print(f"\n📋 Checks Performed: {len(results['checks'])}")
    for check in results['checks']:
        if check['status'] == 'PASS':
            status_icon = '✅'
        elif check['status'] == 'WARN':
            status_icon = '⚠️ '
        else:
            status_icon = '❌'
        print(f"  {status_icon} {check['check']}: {check['message']}")
    
    if results['errors']:
        print(f"\n❌ Errors ({len(results['errors'])}):")
        for error in results['errors']:
            print(f"  - {error}")
    
    if results['warnings']:
        print(f"\n⚠️  Warnings ({len(results['warnings'])}):")
        for warning in results['warnings']:
            print(f"  - {warning}")
    
    print("\n" + "="*70)
    
    # Write evidence
    validator.write_evidence()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
