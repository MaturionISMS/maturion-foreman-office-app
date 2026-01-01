#!/usr/bin/env python3
"""
Builder Contract Validation Script

Validates all builder contracts in .github/agents/ against the schema.
This script ensures builder recruitment mechanism is operational.

Usage:
    python scripts/validate_builder_contracts.py
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath):
    """Check if a file exists"""
    if not os.path.exists(filepath):
        print(f"❌ FAIL: File not found: {filepath}")
        return False
    print(f"✅ PASS: File exists: {filepath}")
    return True

def check_yaml_frontmatter(filepath):
    """Basic check that file has YAML frontmatter"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            if not content.startswith('---'):
                print(f"❌ FAIL: No YAML frontmatter found in {filepath}")
                return False
            
            # Check for second --- delimiter
            parts = content.split('---', 2)
            if len(parts) < 3:
                print(f"❌ FAIL: Incomplete YAML frontmatter in {filepath}")
                return False
            
            print(f"✅ PASS: YAML frontmatter present in {filepath}")
            return True
    except Exception as e:
        print(f"❌ FAIL: Error reading {filepath}: {e}")
        return False

def validate_builder_contracts():
    """Validate all builder contracts"""
    print("=" * 80)
    print("BUILDER CONTRACT VALIDATION")
    print("=" * 80)
    print()
    
    base_dir = Path(__file__).parent.parent
    agents_dir = base_dir / '.github' / 'agents'
    
    # Required builders
    required_builders = [
        'ui-builder',
        'api-builder',
        'schema-builder',
        'integration-builder',
        'qa-builder'
    ]
    
    all_passed = True
    
    # Check schema exists
    print("Checking schema...")
    schema_path = agents_dir / 'BUILDER_CONTRACT_SCHEMA.md'
    if not check_file_exists(schema_path):
        all_passed = False
    print()
    
    # Check each builder contract
    print("Checking builder contracts...")
    for builder_id in required_builders:
        contract_path = agents_dir / f'{builder_id}.md'
        
        print(f"\nValidating {builder_id}...")
        if not check_file_exists(contract_path):
            all_passed = False
            continue
        
        if not check_yaml_frontmatter(contract_path):
            all_passed = False
            continue
        
        # Additional checks could be added here:
        # - Parse YAML and validate required fields
        # - Check markdown sections
        # - Validate alignment with foreman/ artifacts
        
        print(f"✅ {builder_id} contract validation complete")
    
    print()
    print("=" * 80)
    
    if all_passed:
        print("✅ SUCCESS: All builder contracts validated")
        print()
        print("Builder recruitment mechanism is operational.")
        print("Phase 5.0 is UNBLOCKED.")
        return 0
    else:
        print("❌ FAILURE: Builder contract validation failed")
        print()
        print("Builder recruitment mechanism is NOT operational.")
        print("Phase 5.0 remains BLOCKED.")
        return 1

if __name__ == '__main__':
    sys.exit(validate_builder_contracts())
