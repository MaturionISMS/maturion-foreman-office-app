#!/usr/bin/env python3
"""
Maturion Foreman - App Description Validator

Validates that an App Description exists, is authoritative, and meets all
governance requirements per APP_DESCRIPTION_REQUIREMENT_POLICY.md.

This validator enforces:
- Existence at canonical location
- Authority markers (Owner, Status, Version)
- Content completeness (Purpose, Scope, Success Criteria)
- Approval status

Returns:
    PASS: App Description is valid and authoritative
    FAIL: App Description is missing, incomplete, or not authoritative
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class AppDescriptionValidator:
    """Validates App Description against governance requirements"""
    
    def __init__(self, repo_root: Path, app_name: str = "FM"):
        self.repo_root = repo_root
        self.app_name = app_name
        self.results = {
            'validation_id': f'app-desc-{app_name}-{datetime.now().strftime("%Y%m%d-%H%M%S")}',
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
        print(f"🔍 Validating App Description for {self.app_name}...\n")
        
        # Check 1: Existence at canonical location
        canonical_exists = self._check_canonical_location()
        
        if not canonical_exists:
            self.results['status'] = 'FAIL'
            return False, self.results
        
        # Check 2: Authority markers
        authority_valid = self._check_authority_markers()
        
        # Check 3: Content completeness
        content_complete = self._check_content_completeness()
        
        # Check 4: Approval status
        approval_valid = self._check_approval_status()
        
        # Determine overall status
        all_critical_passed = (
            canonical_exists and 
            authority_valid and 
            content_complete and 
            approval_valid
        )
        
        self.results['status'] = 'PASS' if all_critical_passed else 'FAIL'
        
        return all_critical_passed, self.results
    
    def _check_canonical_location(self) -> bool:
        """Check if App Description exists at canonical location"""
        canonical_path = self.repo_root / "docs" / "governance" / f"{self.app_name}_APP_DESCRIPTION.md"
        fallback_path = self.repo_root / "APP_DESCRIPTION.md"
        
        check_result = {
            'check': 'canonical_location',
            'status': 'UNKNOWN',
            'message': '',
            'evidence': {}
        }
        
        # Check canonical location first
        if canonical_path.exists():
            check_result['status'] = 'PASS'
            check_result['message'] = f'App Description found at canonical location'
            check_result['evidence'] = {
                'path': str(canonical_path),
                'exists': True,
                'size': canonical_path.stat().st_size
            }
            self.results['evidence']['canonical_path'] = str(canonical_path)
            self._load_content(canonical_path)
        # Check fallback location
        elif fallback_path.exists():
            check_result['status'] = 'PASS'
            check_result['message'] = f'App Description found at fallback location (root)'
            check_result['evidence'] = {
                'path': str(fallback_path),
                'exists': True,
                'size': fallback_path.stat().st_size
            }
            self.results['evidence']['canonical_path'] = str(fallback_path)
            self.results['warnings'].append(
                f"App Description at root instead of canonical location: {canonical_path}"
            )
            self._load_content(fallback_path)
        else:
            check_result['status'] = 'FAIL'
            check_result['message'] = f'App Description NOT found at canonical or fallback location'
            check_result['evidence'] = {
                'canonical_path': str(canonical_path),
                'fallback_path': str(fallback_path),
                'exists': False
            }
            self.results['errors'].append(
                f"BLOCKING: App Description missing. Expected at: {canonical_path}"
            )
            self.results['checks'].append(check_result)
            return False
        
        self.results['checks'].append(check_result)
        return True
    
    def _load_content(self, path: Path):
        """Load App Description content"""
        with open(path, 'r', encoding='utf-8') as f:
            self.content = f.read()
        self.results['evidence']['content_length'] = len(self.content)
    
    def _check_authority_markers(self) -> bool:
        """Check for required authority markers"""
        if not hasattr(self, 'content'):
            return False
        
        markers_found = {
            'owner': False,
            'status': False,
            'version': False
        }
        
        # Check for Owner
        owner_patterns = [
            r'Owner:\s*(.+)',
            r'Product Owner:\s*(.+)',
            r'\*\*Owner\*\*:\s*(.+)'
        ]
        for pattern in owner_patterns:
            match = re.search(pattern, self.content, re.IGNORECASE)
            if match:
                markers_found['owner'] = True
                self.results['evidence']['owner'] = match.group(1).strip()
                break
        
        # Check for Status (Authoritative or Approved)
        status_patterns = [
            r'Status:\s*(Authoritative|Approved)',
            r'\*\*Status\*\*:\s*(Authoritative|Approved)',
            r'##\s+Application Description\s+\((Wave \d+\s*[–-]\s*)?(Authoritative|Approved)',
            r'Status:\*\*\s*(Authoritative|Approved)',
        ]
        for pattern in status_patterns:
            match = re.search(pattern, self.content, re.IGNORECASE)
            if match:
                markers_found['status'] = True
                # Get the last group which is the status
                groups = match.groups()
                self.results['evidence']['status'] = groups[-1].strip()
                break
        
        # Check for Version
        version_patterns = [
            r'Version:\s*(.+)',
            r'\*\*Version\*\*:\s*(.+)',
            r'Wave\s+\d+',
            r'v\d+\.?\d*',
            r'\d{4}-\d{2}-\d{2}',
            r'Authoritative\s+v\d+',
        ]
        for pattern in version_patterns:
            match = re.search(pattern, self.content)
            if match:
                markers_found['version'] = True
                self.results['evidence']['version'] = match.group(0).strip()
                break
        
        # Record check results
        check_result = {
            'check': 'authority_markers',
            'status': 'PASS' if all(markers_found.values()) else 'FAIL',
            'message': '',
            'evidence': markers_found
        }
        
        missing = [k for k, v in markers_found.items() if not v]
        if missing:
            check_result['message'] = f'Missing authority markers: {", ".join(missing)}'
            self.results['errors'].append(
                f"BLOCKING: App Description missing required markers: {', '.join(missing)}"
            )
        else:
            check_result['message'] = 'All authority markers present'
        
        self.results['checks'].append(check_result)
        return all(markers_found.values())
    
    def _check_content_completeness(self) -> bool:
        """Check for required content sections"""
        if not hasattr(self, 'content'):
            return False
        
        required_sections = {
            'purpose': False,
            'scope': False,
            'success_criteria': False
        }
        
        # Check for Purpose section
        purpose_patterns = [
            r'##\s+.*Purpose',
            r'###\s+.*Purpose',
            r'\*\*Purpose\*\*:',
        ]
        for pattern in purpose_patterns:
            if re.search(pattern, self.content, re.IGNORECASE):
                required_sections['purpose'] = True
                break
        
        # Check for Scope section (can be explicit or implicit via "What This App Is/Is Not")
        scope_patterns = [
            r'##\s+.*Scope',
            r'###\s+.*Scope',
            r'\*\*Scope\*\*:',
            r'##\s+.*What This App Is',
            r'##\s+.*What This App Is Not',
        ]
        for pattern in scope_patterns:
            if re.search(pattern, self.content, re.IGNORECASE):
                required_sections['scope'] = True
                break
        
        # Check for Success Criteria
        success_patterns = [
            r'##\s+.*Success',
            r'###\s+.*Success',
            r'\*\*Success\*\*:',
            r'Success Criteria',
            r'Success Definition'
        ]
        for pattern in success_patterns:
            if re.search(pattern, self.content, re.IGNORECASE):
                required_sections['success_criteria'] = True
                break
        
        # Check for minimum content length (not just empty sections)
        if len(self.content) < 500:
            self.results['warnings'].append(
                f"App Description is very short ({len(self.content)} characters). Consider adding more detail."
            )
        
        check_result = {
            'check': 'content_completeness',
            'status': 'PASS' if all(required_sections.values()) else 'FAIL',
            'message': '',
            'evidence': required_sections
        }
        
        missing = [k for k, v in required_sections.items() if not v]
        if missing:
            check_result['message'] = f'Missing required sections: {", ".join(missing)}'
            self.results['errors'].append(
                f"BLOCKING: App Description missing required sections: {', '.join(missing)}"
            )
        else:
            check_result['message'] = 'All required content sections present'
        
        self.results['checks'].append(check_result)
        return all(required_sections.values())
    
    def _check_approval_status(self) -> bool:
        """Verify approval status"""
        if not hasattr(self, 'content'):
            return False
        
        # Check if status indicates approval
        status = self.results['evidence'].get('status', '').lower()
        is_approved = status in ['authoritative', 'approved']
        
        # Check for draft or TBD markers that would block
        blocking_markers = ['draft', 'tbd', 'todo', 'work in progress', 'wip']
        has_blocking_markers = any(
            marker in self.content.lower()[:500]  # Check first 500 chars for status area
            for marker in blocking_markers
        )
        
        check_result = {
            'check': 'approval_status',
            'status': 'PASS' if (is_approved and not has_blocking_markers) else 'FAIL',
            'message': '',
            'evidence': {
                'is_approved': is_approved,
                'has_blocking_markers': has_blocking_markers
            }
        }
        
        if not is_approved:
            check_result['message'] = 'App Description not marked as Authoritative or Approved'
            self.results['errors'].append(
                "BLOCKING: App Description must be marked as 'Authoritative' or 'Approved'"
            )
        elif has_blocking_markers:
            check_result['message'] = 'App Description contains draft/TBD markers'
            self.results['errors'].append(
                "BLOCKING: App Description contains draft, TBD, or TODO markers"
            )
        else:
            check_result['message'] = 'App Description is approved and ready'
        
        self.results['checks'].append(check_result)
        return is_approved and not has_blocking_markers
    
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
    validator = AppDescriptionValidator(repo_root, app_name)
    success, results = validator.validate()
    
    # Print results
    print("\n" + "="*70)
    print(f"APP DESCRIPTION VALIDATION RESULTS - {app_name}")
    print("="*70)
    print(f"\nOverall Status: {'✅ PASS' if success else '❌ FAIL'}")
    print(f"Validation ID: {results['validation_id']}")
    print(f"Timestamp: {results['timestamp']}")
    
    print(f"\n📋 Checks Performed: {len(results['checks'])}")
    for check in results['checks']:
        status_icon = '✅' if check['status'] == 'PASS' else '❌'
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
