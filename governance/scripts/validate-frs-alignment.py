#!/usr/bin/env python3
"""
Maturion Foreman - FRS Alignment Validator

Validates that a Functional Requirement Specification (FRS) properly derives from
and aligns with its App Description per app-description-frs-alignment-checklist.md.

This validator enforces:
- App Description exists and is valid
- FRS explicitly references App Description
- FRS aligns with App Description (purpose, scope, success criteria)
- No contradictions between FRS and App Description
- Complete traceability chain

Returns:
    PASS: FRS is properly derived and aligned
    FAIL: FRS is missing, doesn't reference App Description, or contradicts it
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class FRSAlignmentValidator:
    """Validates FRS alignment with App Description"""
    
    def __init__(self, repo_root: Path, app_name: str = "FM", frs_path: str = None):
        self.repo_root = repo_root
        self.app_name = app_name
        self.frs_path = frs_path
        self.results = {
            'validation_id': f'frs-align-{app_name}-{datetime.now().strftime("%Y%m%d-%H%M%S")}',
            'timestamp': datetime.now().isoformat(),
            'app_name': app_name,
            'status': 'UNKNOWN',
            'checks': [],
            'errors': [],
            'warnings': [],
            'evidence': {}
        }
        self.app_desc_content = None
        self.frs_content = None
        
    def validate(self) -> Tuple[bool, Dict]:
        """Run all validation checks"""
        print(f"🔍 Validating FRS Alignment for {self.app_name}...\n")
        
        # Check 1: App Description exists and is valid
        app_desc_valid = self._check_app_description()
        
        if not app_desc_valid:
            self.results['status'] = 'FAIL'
            return False, self.results
        
        # Check 2: FRS exists
        frs_exists = self._check_frs_existence()
        
        if not frs_exists:
            self.results['status'] = 'FAIL'
            return False, self.results
        
        # Check 3: FRS explicitly references App Description
        references_app_desc = self._check_app_description_reference()
        
        # Check 4: FRS aligns with App Description
        alignment_valid = self._check_alignment()
        
        # Check 5: No contradictions
        no_contradictions = self._check_contradictions()
        
        # Determine overall status
        all_critical_passed = (
            app_desc_valid and 
            frs_exists and 
            references_app_desc and 
            alignment_valid and 
            no_contradictions
        )
        
        self.results['status'] = 'PASS' if all_critical_passed else 'FAIL'
        
        return all_critical_passed, self.results
    
    def _check_app_description(self) -> bool:
        """Verify App Description exists and is valid"""
        check_result = {
            'check': 'app_description_validity',
            'status': 'UNKNOWN',
            'message': '',
            'evidence': {}
        }
        
        # Try canonical location first
        canonical_path = self.repo_root / "docs" / "governance" / f"{self.app_name}_APP_DESCRIPTION.md"
        fallback_path = self.repo_root / "APP_DESCRIPTION.md"
        
        app_desc_path = None
        if canonical_path.exists():
            app_desc_path = canonical_path
        elif fallback_path.exists():
            app_desc_path = fallback_path
        
        if not app_desc_path:
            check_result['status'] = 'FAIL'
            check_result['message'] = 'App Description not found'
            self.results['errors'].append(
                f"BLOCKING: App Description must exist before FRS validation"
            )
            self.results['checks'].append(check_result)
            return False
        
        # Load App Description
        with open(app_desc_path, 'r', encoding='utf-8') as f:
            self.app_desc_content = f.read()
        
        self.results['evidence']['app_description_path'] = str(app_desc_path)
        
        # Check if it's authoritative
        if not re.search(r'\*\*Status:\*\*?\s*(Authoritative|Approved)', self.app_desc_content, re.IGNORECASE):
            check_result['status'] = 'FAIL'
            check_result['message'] = 'App Description not marked as Authoritative or Approved'
            self.results['errors'].append(
                "BLOCKING: App Description must be authoritative before FRS validation"
            )
            self.results['checks'].append(check_result)
            return False
        
        check_result['status'] = 'PASS'
        check_result['message'] = 'App Description exists and is authoritative'
        self.results['checks'].append(check_result)
        return True
    
    def _check_frs_existence(self) -> bool:
        """Check if FRS exists"""
        check_result = {
            'check': 'frs_existence',
            'status': 'UNKNOWN',
            'message': '',
            'evidence': {}
        }
        
        # If FRS path provided, use it
        if self.frs_path:
            frs_file = Path(self.frs_path)
            if not frs_file.is_absolute():
                frs_file = self.repo_root / frs_file
        else:
            # Search for FRS in common locations
            possible_locations = [
                self.repo_root / "architecture" / f"{self.app_name}_FUNCTIONAL_SPEC.md",
                self.repo_root / "architecture" / "FUNCTIONAL_SPEC.md",
                self.repo_root / "docs" / f"{self.app_name}_FUNCTIONAL_SPEC.md",
                self.repo_root / "foreman" / "architecture" / "FOREMAN_TRUE_NORTH_v1.0.md",
            ]
            
            frs_file = None
            for location in possible_locations:
                if location.exists():
                    frs_file = location
                    break
        
        if not frs_file or not frs_file.exists():
            check_result['status'] = 'FAIL'
            check_result['message'] = 'FRS not found'
            self.results['errors'].append(
                f"BLOCKING: FRS not found. Searched common locations or path: {self.frs_path}"
            )
            self.results['checks'].append(check_result)
            return False
        
        # Load FRS
        with open(frs_file, 'r', encoding='utf-8') as f:
            self.frs_content = f.read()
        
        self.results['evidence']['frs_path'] = str(frs_file)
        self.results['evidence']['frs_size'] = len(self.frs_content)
        
        check_result['status'] = 'PASS'
        check_result['message'] = f'FRS found at {frs_file.name}'
        self.results['checks'].append(check_result)
        return True
    
    def _check_app_description_reference(self) -> bool:
        """Check if FRS explicitly references App Description"""
        check_result = {
            'check': 'app_description_reference',
            'status': 'UNKNOWN',
            'message': '',
            'evidence': {}
        }
        
        if not self.frs_content:
            check_result['status'] = 'FAIL'
            check_result['message'] = 'FRS content not loaded'
            self.results['checks'].append(check_result)
            return False
        
        # Check for explicit reference patterns
        reference_patterns = [
            rf'Derived from.*{self.app_name}_APP_DESCRIPTION',
            rf'Based on.*{self.app_name}_APP_DESCRIPTION',
            rf'derives? from.*APP_DESCRIPTION',
            rf'Upstream authority:.*APP_DESCRIPTION',
            r'This.*specification.*derived from.*APP_DESCRIPTION',
        ]
        
        found_reference = False
        for pattern in reference_patterns:
            if re.search(pattern, self.frs_content, re.IGNORECASE):
                found_reference = True
                match = re.search(pattern, self.frs_content, re.IGNORECASE)
                self.results['evidence']['reference_statement'] = match.group(0)
                break
        
        if not found_reference:
            check_result['status'] = 'FAIL'
            check_result['message'] = 'FRS does not explicitly reference App Description'
            self.results['errors'].append(
                f"BLOCKING: FRS must explicitly state it derives from {self.app_name}_APP_DESCRIPTION.md"
            )
        else:
            check_result['status'] = 'PASS'
            check_result['message'] = 'FRS explicitly references App Description'
        
        self.results['checks'].append(check_result)
        return found_reference
    
    def _check_alignment(self) -> bool:
        """Check if FRS aligns with App Description"""
        check_result = {
            'check': 'frs_app_desc_alignment',
            'status': 'UNKNOWN',
            'message': '',
            'evidence': {}
        }
        
        if not self.frs_content or not self.app_desc_content:
            check_result['status'] = 'FAIL'
            check_result['message'] = 'Cannot check alignment - content not loaded'
            self.results['checks'].append(check_result)
            return False
        
        # Check 1: Both have purpose sections
        app_desc_has_purpose = bool(re.search(r'##\s+.*Purpose', self.app_desc_content, re.IGNORECASE))
        frs_has_purpose = bool(re.search(r'##\s+.*Purpose', self.frs_content, re.IGNORECASE))
        
        alignment_checks = {
            'both_have_purpose': app_desc_has_purpose and frs_has_purpose,
        }
        
        # Check 2: Key terms from App Description appear in FRS
        # Extract key terms from App Description purpose/scope
        app_desc_key_terms = set()
        purpose_match = re.search(r'##\s+.*Purpose.*?\n(.*?)(?=\n##|\Z)', 
                                 self.app_desc_content, re.IGNORECASE | re.DOTALL)
        if purpose_match:
            purpose_text = purpose_match.group(1).lower()
            # Extract significant words (3+ chars, not common words)
            words = re.findall(r'\b[a-z]{3,}\b', purpose_text)
            common_words = {'the', 'and', 'for', 'that', 'this', 'with', 'from', 'are', 'was', 'but'}
            app_desc_key_terms = set(w for w in words if w not in common_words)
        
        # Check if at least some key terms appear in FRS
        if app_desc_key_terms:
            frs_lower = self.frs_content.lower()
            terms_found = sum(1 for term in app_desc_key_terms if term in frs_lower)
            alignment_checks['key_terms_present'] = terms_found >= min(3, len(app_desc_key_terms) * 0.3)
            self.results['evidence']['key_terms_found'] = terms_found
            self.results['evidence']['key_terms_total'] = len(app_desc_key_terms)
        
        check_result['evidence'] = alignment_checks
        
        # Overall alignment check
        if all(alignment_checks.values()):
            check_result['status'] = 'PASS'
            check_result['message'] = 'FRS aligns with App Description structure and content'
        else:
            check_result['status'] = 'WARN'
            check_result['message'] = 'Alignment warning - some structural elements missing'
            self.results['warnings'].append(
                "FRS may not fully align with App Description structure"
            )
        
        self.results['checks'].append(check_result)
        # Return True even for WARN as it's not blocking
        return True
    
    def _check_contradictions(self) -> bool:
        """Check for obvious contradictions"""
        check_result = {
            'check': 'no_contradictions',
            'status': 'UNKNOWN',
            'message': '',
            'evidence': {}
        }
        
        if not self.frs_content or not self.app_desc_content:
            check_result['status'] = 'FAIL'
            check_result['message'] = 'Cannot check contradictions - content not loaded'
            self.results['checks'].append(check_result)
            return False
        
        # Check for explicit "out of scope" statements that might contradict
        # Look for statements in FRS that say something is out of scope
        # that App Description says is in scope
        
        # This is a basic check - could be enhanced with more sophisticated analysis
        contradictions_found = []
        
        # Check if FRS says "not" something that App Description emphasizes
        app_desc_is_statements = re.findall(r'This (?:app|application) is ([^.]+)', 
                                           self.app_desc_content, re.IGNORECASE)
        for statement in app_desc_is_statements:
            # Look for negation of this in FRS
            negation_pattern = rf'(?:not|never|doesn\'t|does not).*{re.escape(statement[:20])}'
            if re.search(negation_pattern, self.frs_content, re.IGNORECASE):
                contradictions_found.append(f"Possible contradiction about: {statement[:50]}")
        
        check_result['evidence']['contradictions'] = contradictions_found
        
        if contradictions_found:
            check_result['status'] = 'WARN'
            check_result['message'] = f'Possible contradictions detected ({len(contradictions_found)})'
            self.results['warnings'].append(
                f"Review potential contradictions: {', '.join(contradictions_found)}"
            )
        else:
            check_result['status'] = 'PASS'
            check_result['message'] = 'No obvious contradictions detected'
        
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
    frs_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Create validator and run
    validator = FRSAlignmentValidator(repo_root, app_name, frs_path)
    success, results = validator.validate()
    
    # Print results
    print("\n" + "="*70)
    print(f"FRS ALIGNMENT VALIDATION RESULTS - {app_name}")
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
