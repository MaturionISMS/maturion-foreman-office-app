#!/usr/bin/env python3
"""
Wave 2 QA Alignment Validation Script

Purpose: Automated validation of Wave 2 subwave QA range semantic alignment with QA Catalog.
Authority: BL-019 Emergency Response - Prevent Third Occurrence
Status: MANDATORY - Must PASS before ANY Wave 2 subwave authorization

Usage:
    python3 validate-wave2-qa-alignment.py

Exit Codes:
    0 - All subwaves aligned with QA Catalog
    1 - Misalignments detected (BLOCKING)
    2 - Validation error (script failure)

Integration:
    - Run before EVERY Wave 2 subwave authorization
    - Add to pre-authorization gate checklist
    - Treat as HARD GATE (no authorization if exit != 0)
"""

import re
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set

# Color codes for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def read_qa_catalog() -> Dict[int, str]:
    """Read QA_CATALOG.md and extract all QA allocations."""
    qa_catalog = {}
    
    try:
        with open('QA_CATALOG.md', 'r') as f:
            content = f.read()
        
        # Extract QA-XXX: Description patterns
        lines = content.split('\n')
        for line in lines:
            match = re.search(r'\bQA-(\d+)\b[:\s]+(.+)', line)
            if match:
                qa_num = int(match.group(1))
                desc = match.group(2).strip()
                # Remove markdown formatting
                desc = re.sub(r'\*\*', '', desc)
                qa_catalog[qa_num] = desc
        
        return qa_catalog
    
    except FileNotFoundError:
        print(f"{Colors.RED}ERROR: QA_CATALOG.md not found{Colors.END}")
        sys.exit(2)
    except Exception as e:
        print(f"{Colors.RED}ERROR reading QA_CATALOG.md: {e}{Colors.END}")
        sys.exit(2)

def extract_subwave_qa_range(filepath: Path) -> Tuple[int, int, str]:
    """Extract QA range and claimed purpose from subwave spec file."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Extract QA range (format: QA-XXX to QA-YYY)
        range_match = re.search(r'\*\*QA Range:\*\*\s+QA-(\d+)\s+to\s+QA-(\d+)', content)
        if not range_match:
            return None, None, None
        
        start = int(range_match.group(1))
        end = int(range_match.group(2))
        
        # Extract claimed purpose from filename
        filename = filepath.stem  # e.g., SUBWAVE_2.3_API_BUILDER_SYSTEM_OPTIMIZATIONS_PHASE1
        purpose = filename.split('_', 3)[-1] if '_' in filename else "Unknown"
        purpose = purpose.replace('_', ' ').title()
        
        return start, end, purpose
    
    except Exception as e:
        print(f"{Colors.YELLOW}WARNING: Could not parse {filepath.name}: {e}{Colors.END}")
        return None, None, None

def check_semantic_alignment(qa_range: range, qa_catalog: Dict[int, str], claimed_purpose: str) -> Tuple[str, List[str]]:
    """
    Check semantic alignment between claimed purpose and catalog allocations.
    
    Returns:
        (status, issues)
        status: 'ALIGNED' | 'MISALIGNED' | 'PARTIAL' | 'UNDEFINED'
        issues: List of specific alignment issues
    """
    issues = []
    
    # Extract catalog descriptions for this range
    catalog_descs = []
    missing_qa = []
    
    for qa_num in qa_range:
        if qa_num in qa_catalog:
            catalog_descs.append(qa_catalog[qa_num])
        else:
            missing_qa.append(qa_num)
    
    if not catalog_descs:
        return 'UNDEFINED', [f"No QA definitions found in catalog for this range"]
    
    if missing_qa:
        issues.append(f"Missing QA IDs in catalog: {missing_qa[:5]}{'...' if len(missing_qa) > 5 else ''}")
    
    # Combine all catalog descriptions into one text for analysis
    catalog_text = ' '.join(catalog_descs).lower()
    claimed_lower = claimed_purpose.lower()
    
    # Semantic mismatch detection
    failure_keywords = ['failure', 'error', 'timeout', 'corruption', 'crash', 'unavailable', 'exhaustion']
    state_keywords = ['transition', 'state', 'pending', 'completed', 'resolved']
    flow_keywords = ['flow', 'end-to-end', 'e2e', 'escalation flow', 'parking flow']
    
    has_failure = any(kw in catalog_text for kw in failure_keywords)
    has_state = any(kw in catalog_text for kw in state_keywords)
    has_flow = any(kw in catalog_text for kw in flow_keywords)
    
    # Check for obvious mismatches
    if 'optimization' in claimed_lower and has_failure:
        issues.append(f"MISMATCH: Claimed 'optimization' but catalog shows failure modes")
        return 'MISALIGNED', issues
    
    if 'integration' in claimed_lower and (has_state and not 'integration' in catalog_text):
        issues.append(f"MISMATCH: Claimed 'integration' but catalog shows state transitions")
        return 'MISALIGNED', issues
    
    if 'analytics' in claimed_lower and ('parking' in catalog_text or 'dashboard' in catalog_text):
        issues.append(f"MISMATCH: Claimed 'analytics' but catalog shows parking/dashboard flows")
        return 'MISALIGNED', issues
    
    if 'parking' in claimed_lower and ('network' in catalog_text or 'resource' in catalog_text):
        issues.append(f"MISMATCH: Claimed 'parking' but catalog shows network/resource failure modes")
        return 'MISALIGNED', issues
    
    if 'dashboard' in claimed_lower and 'database' in catalog_text and not 'dashboard' in catalog_text:
        issues.append(f"MISMATCH: Claimed 'dashboard' but catalog shows database failure modes")
        return 'MISALIGNED', issues
    
    if 'e2e' in claimed_lower or 'end-to-end' in claimed_lower:
        if not has_flow:
            issues.append(f"MISMATCH: Claimed 'E2E flows' but catalog does not show flow definitions")
            return 'UNDEFINED', issues
    
    # If we have concerns but not total mismatch
    if issues:
        return 'PARTIAL', issues
    
    # Check for undefined (no real descriptions, just placeholders)
    if len(catalog_descs) < (qa_range.stop - qa_range.start) * 0.5:  # Less than 50% coverage
        issues.append(f"SPARSE: Only {len(catalog_descs)} descriptions for {len(qa_range)} QA IDs")
        return 'UNDEFINED', issues
    
    return 'ALIGNED', []

def validate_all_subwaves() -> Tuple[bool, Dict]:
    """
    Validate ALL Wave 2 subwaves.
    
    Returns:
        (all_pass, results_dict)
    """
    print(f"\n{Colors.BOLD}=== Wave 2 QA Alignment Validation ==={Colors.END}\n")
    print(f"Authority: BL-019 Emergency Response")
    print(f"Purpose: Prevent third occurrence of QA misalignment\n")
    
    # Read QA Catalog
    print(f"Loading QA Catalog... ", end='')
    qa_catalog = read_qa_catalog()
    print(f"{Colors.GREEN}OK{Colors.END} ({len(qa_catalog)} QA definitions)")
    
    # Find all subwave specification files
    subwave_dir = Path('wave2_builder_issues')
    if not subwave_dir.exists():
        print(f"{Colors.RED}ERROR: wave2_builder_issues directory not found{Colors.END}")
        sys.exit(2)
    
    subwave_files = sorted(subwave_dir.glob('SUBWAVE_*.md'))
    if not subwave_files:
        print(f"{Colors.RED}ERROR: No SUBWAVE_*.md files found{Colors.END}")
        sys.exit(2)
    
    print(f"Found {len(subwave_files)} subwave specification files\n")
    
    # Validate each subwave
    results = {}
    all_pass = True
    
    for filepath in subwave_files:
        subwave_id = filepath.stem.split('_')[1]  # e.g., "2.3"
        
        # Extract QA range and purpose
        start, end, purpose = extract_subwave_qa_range(filepath)
        
        if start is None:
            print(f"{Colors.YELLOW}⚠️  Subwave {subwave_id}: Could not extract QA range (SKIP){Colors.END}")
            continue
        
        qa_range = range(start, end + 1)
        
        # Check semantic alignment
        status, issues = check_semantic_alignment(qa_range, qa_catalog, purpose)
        
        # Store results
        results[subwave_id] = {
            'qa_range': f'QA-{start} to QA-{end}',
            'count': end - start + 1,
            'purpose': purpose,
            'status': status,
            'issues': issues
        }
        
        # Print result
        if status == 'ALIGNED':
            status_icon = f"{Colors.GREEN}✅{Colors.END}"
        elif status == 'PARTIAL':
            status_icon = f"{Colors.YELLOW}⚠️ {Colors.END}"
            all_pass = False
        elif status == 'MISALIGNED':
            status_icon = f"{Colors.RED}❌{Colors.END}"
            all_pass = False
        else:  # UNDEFINED
            status_icon = f"{Colors.YELLOW}⚠️ {Colors.END}"
            all_pass = False
        
        print(f"{status_icon} Subwave {subwave_id}: QA-{start} to QA-{end} ({end - start + 1} QA)")
        print(f"   Purpose: {purpose}")
        print(f"   Status: {status}")
        
        if issues:
            for issue in issues:
                print(f"   Issue: {issue}")
        print()
    
    return all_pass, results

def main():
    """Main validation entry point."""
    try:
        all_pass, results = validate_all_subwaves()
        
        # Summary
        print(f"\n{Colors.BOLD}=== Validation Summary ==={Colors.END}\n")
        
        aligned = sum(1 for r in results.values() if r['status'] == 'ALIGNED')
        misaligned = sum(1 for r in results.values() if r['status'] == 'MISALIGNED')
        partial = sum(1 for r in results.values() if r['status'] == 'PARTIAL')
        undefined = sum(1 for r in results.values() if r['status'] == 'UNDEFINED')
        
        print(f"Total Subwaves: {len(results)}")
        print(f"✅ Aligned: {aligned}")
        print(f"⚠️  Partial: {partial}")
        print(f"❌ Misaligned: {misaligned}")
        print(f"⚠️  Undefined: {undefined}")
        print()
        
        if all_pass:
            print(f"{Colors.GREEN}{Colors.BOLD}✅ VALIDATION PASS{Colors.END}")
            print(f"All Wave 2 subwaves aligned with QA Catalog")
            print(f"Authorization may proceed (subject to other gates)")
            sys.exit(0)
        else:
            print(f"{Colors.RED}{Colors.BOLD}❌ VALIDATION FAIL{Colors.END}")
            print(f"One or more subwaves NOT aligned with QA Catalog")
            print(f"{Colors.BOLD}BLOCKING: Cannot authorize ANY Wave 2 subwave until corrected{Colors.END}")
            
            # Save detailed results for review
            with open('wave2-qa-alignment-validation-results.json', 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\nDetailed results saved to: wave2-qa-alignment-validation-results.json")
            
            sys.exit(1)
    
    except Exception as e:
        print(f"\n{Colors.RED}{Colors.BOLD}VALIDATION ERROR{Colors.END}")
        print(f"Script failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(2)

if __name__ == '__main__':
    main()
