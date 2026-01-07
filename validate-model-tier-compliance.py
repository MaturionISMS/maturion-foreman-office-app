#!/usr/bin/env python3
"""
Validate MODEL_TIER_AGENT_CONTRACT_BINDING compliance for all agent contracts.

Authority: governance/escalation/MODEL_TIER_AGENT_CONTRACT_BINDING.md
"""

import os
import sys
import yaml
import re
from pathlib import Path

# Expected tier assignments per policy
EXPECTED_TIERS = {
    'ui-builder.md': {'tier': 'standard', 'level': 'L1', 'model': 'gpt-4-1', 'class': 'coding'},
    'api-builder.md': {'tier': 'standard', 'level': 'L1', 'model': 'gpt-4-1', 'class': 'coding'},
    'schema-builder.md': {'tier': 'standard', 'level': 'L1', 'model': 'gpt-4-1', 'class': 'coding'},
    'integration-builder.md': {'tier': 'standard', 'level': 'L1', 'model': 'gpt-4-1', 'class': 'coding'},
    'qa-builder.md': {'tier': 'standard', 'level': 'L1', 'model': 'gpt-4-1', 'class': 'coding'},
    'governance-liaison.md': {'tier': 'premium', 'level': 'L2', 'model': 'claude-sonnet-4-5', 'class': 'extended-reasoning'},
    'CodexAdvisor-agent.md': {'tier': 'reasoning', 'level': 'L3', 'model': 'gpt-5-1', 'class': 'constitutional-interpretation'},
}

MANDATORY_FIELDS = ['model', 'model_tier', 'model_tier_level', 'model_class', 'temperature']

def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown file."""
    # Match YAML frontmatter between --- markers (closing with --- or ...)
    match = re.match(r'^---\s*\n(.*?)\n(?:---|\.\.\.)(?:\s|$)', content, re.DOTALL)
    if not match:
        return None, False
    
    frontmatter_text = match.group(1)
    
    # Parse YAML, handling comments
    try:
        data = yaml.safe_load(frontmatter_text)
        
        # Also extract inline comments for tier justification
        has_justification = 'Tier Justification:' in frontmatter_text or 'tier justification' in frontmatter_text.lower()
        
        return data, has_justification
    except yaml.YAMLError as e:
        print(f"YAML parsing error: {e}")
        return None, False

def validate_contract(file_path, expected):
    """Validate a single agent contract."""
    print(f"\n{'='*80}")
    print(f"Validating: {file_path.name}")
    print(f"{'='*80}")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    result = extract_frontmatter(content)
    if not result:
        print("❌ FAIL: No valid frontmatter found")
        return False
    
    frontmatter, has_justification = result
    
    # Check mandatory fields
    all_passed = True
    for field in MANDATORY_FIELDS:
        if field in frontmatter:
            print(f"✅ {field}: {frontmatter[field]}")
        else:
            print(f"❌ MISSING: {field}")
            all_passed = False
    
    # Check model_fallback (recommended but optional)
    if 'model_fallback' in frontmatter:
        print(f"✅ model_fallback: {frontmatter['model_fallback']}")
    else:
        print(f"⚠️  model_fallback: Not present (optional)")
    
    # Check tier justification
    if has_justification:
        print(f"✅ Tier justification: Present")
    else:
        print(f"❌ MISSING: Tier justification comment")
        all_passed = False
    
    # Verify against expected values
    if 'model' in frontmatter:
        if frontmatter['model'] == 'auto':
            print(f"❌ FAIL: model is 'auto', must be explicit")
            all_passed = False
        elif frontmatter['model'] == expected['model']:
            print(f"✅ Model matches expected: {expected['model']}")
        else:
            print(f"⚠️  Model is {frontmatter['model']}, expected {expected['model']}")
    
    if 'model_tier' in frontmatter and frontmatter['model_tier'] == expected['tier']:
        print(f"✅ Tier matches expected: {expected['tier']}")
    elif 'model_tier' in frontmatter:
        print(f"❌ Tier is {frontmatter['model_tier']}, expected {expected['tier']}")
        all_passed = False
    
    if 'model_tier_level' in frontmatter and frontmatter['model_tier_level'] == expected['level']:
        print(f"✅ Level matches expected: {expected['level']}")
    elif 'model_tier_level' in frontmatter:
        print(f"❌ Level is {frontmatter['model_tier_level']}, expected {expected['level']}")
        all_passed = False
    
    if 'model_class' in frontmatter and frontmatter['model_class'] == expected['class']:
        print(f"✅ Class matches expected: {expected['class']}")
    elif 'model_class' in frontmatter:
        print(f"❌ Class is {frontmatter['model_class']}, expected {expected['class']}")
        all_passed = False
    
    if all_passed:
        print(f"\n✅ PASS: {file_path.name} is compliant")
    else:
        print(f"\n❌ FAIL: {file_path.name} has compliance issues")
    
    return all_passed

def main():
    """Main validation function."""
    print("="*80)
    print("MODEL_TIER_AGENT_CONTRACT_BINDING Compliance Validation")
    print("Authority: governance/escalation/MODEL_TIER_AGENT_CONTRACT_BINDING.md")
    print("="*80)
    
    agents_dir = Path(__file__).parent / '.github' / 'agents'
    
    if not agents_dir.exists():
        print(f"❌ ERROR: Agents directory not found: {agents_dir}")
        sys.exit(1)
    
    results = {}
    
    for agent_file, expected in EXPECTED_TIERS.items():
        file_path = agents_dir / agent_file
        if not file_path.exists():
            print(f"❌ ERROR: Agent contract not found: {agent_file}")
            results[agent_file] = False
        else:
            results[agent_file] = validate_contract(file_path, expected)
    
    # Summary
    print("\n" + "="*80)
    print("VALIDATION SUMMARY")
    print("="*80)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    for agent_file, passed_check in results.items():
        status = "✅ PASS" if passed_check else "❌ FAIL"
        print(f"{status}: {agent_file}")
    
    print(f"\nTotal: {total} | Passed: {passed} | Failed: {failed}")
    
    if failed == 0:
        print("\n✅ ALL AGENT CONTRACTS ARE COMPLIANT")
        print("Wave authorization is UNBLOCKED")
        sys.exit(0)
    else:
        print(f"\n❌ {failed} AGENT CONTRACT(S) HAVE COMPLIANCE ISSUES")
        print("Wave authorization is BLOCKED until compliance is achieved")
        sys.exit(1)

if __name__ == '__main__':
    main()
