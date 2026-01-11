#!/usr/bin/env python3
"""
Validation script for PREHANDOVER_PROOF documents.

This script validates that a PREHANDOVER_PROOF document contains all required
sections and evidence for the Execution Bootstrap Protocol (v2.0.0+).

Usage:
    python3 governance/scripts/validate_prehandover_proof.py <path-to-proof-file>
    
Exit Codes:
    0 - Validation passed
    1 - Validation failed
    2 - File not found or invalid
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple


def check_section_exists(content: str, section_name: str) -> bool:
    """Check if a section exists in the content."""
    pattern = rf"##\s+{re.escape(section_name)}"
    return bool(re.search(pattern, content, re.IGNORECASE))


def check_category_0_complete(content: str) -> Tuple[bool, List[str]]:
    """Check if Category 0 (7-step protocol) is complete."""
    errors = []
    
    # Check for Category 0 section
    if not check_section_exists(content, "Category 0: Execution Bootstrap Protocol"):
        errors.append("Missing 'Category 0: Execution Bootstrap Protocol' section")
        return False, errors
    
    # Check for all 7 steps
    steps = [
        "Step 1: Identify Execution Artifacts",
        "Step 2: Local Execution",
        "Step 3: Validate Exit Codes",
        "Step 4: Evidence Collection",
        "Step 5: Failure Remediation",
        "Step 6: Green Attestation",
        "Step 7: Handover Authorization",
    ]
    
    for step in steps:
        if not check_section_exists(content, step):
            errors.append(f"Missing '{step}' section")
    
    # Check for critical attestations
    if "All checks GREEN" not in content:
        errors.append("Missing 'All checks GREEN' attestation")
    
    if "Handover authorized" not in content:
        errors.append("Missing 'Handover authorized' statement")
    
    if "CI is confirmation, NOT diagnostic" not in content:
        errors.append("Missing hard rule acknowledgment: 'CI is confirmation, NOT diagnostic'")
    
    return len(errors) == 0, errors


def check_agent_attestation(content: str) -> Tuple[bool, List[str]]:
    """Check if agent attestation section exists."""
    errors = []
    
    if not check_section_exists(content, "Agent Attestation"):
        errors.append("Missing 'Agent Attestation' section")
    
    return len(errors) == 0, errors


def check_metadata(content: str) -> Tuple[bool, List[str]]:
    """Check if required metadata exists."""
    errors = []
    
    required_fields = [
        "Agent:",
        "PR:",
        "Branch:",
        "Date:",
        "Latest Commit:",
        "Protocol Version:",
    ]
    
    for field in required_fields:
        if field not in content:
            errors.append(f"Missing required field: {field}")
    
    # Check protocol version
    if "Protocol Version:" in content:
        if "2.0.0" not in content:
            errors.append("Protocol version must be 2.0.0 or higher")
    
    return len(errors) == 0, errors


def validate_prehandover_proof(file_path: Path) -> Tuple[bool, List[str]]:
    """
    Validate a PREHANDOVER_PROOF document.
    
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    if not file_path.exists():
        return False, [f"File not found: {file_path}"]
    
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return False, [f"Error reading file: {e}"]
    
    all_errors = []
    
    # Check metadata
    metadata_valid, metadata_errors = check_metadata(content)
    if not metadata_valid:
        all_errors.extend(metadata_errors)
    
    # Check if this is an execution-related PR (Category 0 applicable)
    # If "N/A" is explicitly stated for Category 0, skip detailed validation
    if "Category 0:" in content and "N/A" in content.split("Category 0:")[1].split("\n")[0]:
        print("Category 0 marked as N/A - skipping 7-step validation")
    else:
        # Check Category 0 completeness
        category_0_valid, category_0_errors = check_category_0_complete(content)
        if not category_0_valid:
            all_errors.extend(category_0_errors)
    
    # Check agent attestation
    attestation_valid, attestation_errors = check_agent_attestation(content)
    if not attestation_valid:
        all_errors.extend(attestation_errors)
    
    return len(all_errors) == 0, all_errors


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: validate_prehandover_proof.py <path-to-proof-file>")
        print("Example: validate_prehandover_proof.py PREHANDOVER_PROOF_PR_123.md")
        sys.exit(2)
    
    file_path = Path(sys.argv[1])
    
    print(f"Validating PREHANDOVER_PROOF: {file_path}")
    print("-" * 60)
    
    is_valid, errors = validate_prehandover_proof(file_path)
    
    if is_valid:
        print("✅ VALIDATION PASSED")
        print("\nPREHANDOVER_PROOF is complete and valid.")
        sys.exit(0)
    else:
        print("❌ VALIDATION FAILED")
        print("\nErrors found:")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
        print("\nPlease fix these issues before handover.")
        sys.exit(1)


if __name__ == "__main__":
    main()
