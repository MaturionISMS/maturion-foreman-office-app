#!/usr/bin/env python3
"""
Builder Agent Modular Link Validation Script

Validates all modular links between core builder agent .md files in .github/agents/
and their extended reference documentation in governance/agents/builder-references/.

This ensures the split-modular pattern maintains integrity and all references
are accessible and correctly linked.

Version: 1.0.0
Authority: PR #453 (Builder Agent Modularization)
Status: ACTIVE

Usage:
    python scripts/validate_builder_modular_links.py [--verbose]
"""

import os
import sys
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

def log_info(message: str, verbose: bool = False):
    """Log informational message"""
    if verbose:
        print(f"ℹ️  {message}")

def log_success(message: str):
    """Log success message"""
    print(f"✅ {message}")

def log_warning(message: str):
    """Log warning message"""
    print(f"⚠️  {message}")

def log_error(message: str):
    """Log error message"""
    print(f"❌ {message}")

def extract_reference_links(content: str, source_file: str) -> List[Dict[str, str]]:
    """
    Extract all reference links to extended documentation from agent file content.
    
    Looks for patterns like:
    - See `governance/agents/builder-references/...` 
    - **Detailed ...**: See `governance/agents/builder-references/...`
    - See extended reference: `governance/agents/builder-references/...`
    """
    links = []
    
    # Pattern 1: Backtick wrapped paths
    pattern1 = r'`(governance/agents/builder-references/[^`]+\.md)`'
    for match in re.finditer(pattern1, content, re.MULTILINE):
        path = match.group(1)
        links.append({
            'path': path,
            'line': content[:match.start()].count('\n') + 1,
            'context': content[max(0, match.start()-50):min(len(content), match.end()+50)].strip(),
            'source': source_file
        })
    
    # Pattern 2: Markdown links [text](path)
    pattern2 = r'\[([^\]]+)\]\((governance/agents/builder-references/[^\)]+\.md)\)'
    for match in re.finditer(pattern2, content, re.MULTILINE):
        path = match.group(2)
        links.append({
            'path': path,
            'line': content[:match.start()].count('\n') + 1,
            'context': content[max(0, match.start()-50):min(len(content), match.end()+50)].strip(),
            'source': source_file
        })
    
    return links

def validate_file_exists(base_dir: Path, link: Dict[str, str]) -> Tuple[bool, Optional[str]]:
    """
    Validate that the referenced file exists.
    Returns (success, error_message)
    """
    file_path = base_dir / link['path']
    
    if not file_path.exists():
        return False, f"Referenced file does not exist: {link['path']}"
    
    if not file_path.is_file():
        return False, f"Referenced path is not a file: {link['path']}"
    
    return True, None

def validate_section_reference(base_dir: Path, link: Dict[str, str]) -> Tuple[bool, Optional[str]]:
    """
    Validate section references if present (§ "Section Name" syntax).
    Returns (success, error_message)
    """
    # Check if link has section reference
    section_pattern = r'§\s*"([^"]+)"'
    section_match = re.search(section_pattern, link['context'])
    
    if not section_match:
        # No section reference, just file reference is OK
        return True, None
    
    section_name = section_match.group(1)
    file_path = base_dir / link['path']
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Look for section header
            # Support both ## and ### headers
            section_patterns = [
                f"## {re.escape(section_name)}",
                f"### {re.escape(section_name)}",
                f"#### {re.escape(section_name)}"
            ]
            
            for pattern in section_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    return True, None
            
            return False, f"Section '{section_name}' not found in {link['path']}"
    
    except Exception as e:
        return False, f"Error reading file {link['path']}: {str(e)}"

def validate_builder_agent_file(base_dir: Path, agent_file: Path, verbose: bool = False) -> Tuple[bool, Dict]:
    """
    Validate a single builder agent file's modular links.
    Returns (success, results_dict)
    """
    agent_name = agent_file.stem
    log_info(f"Validating {agent_name}...", verbose)
    
    results = {
        'agent': agent_name,
        'file': str(agent_file.relative_to(base_dir)),
        'links_found': 0,
        'links_valid': 0,
        'links_broken': 0,
        'errors': [],
        'warnings': []
    }
    
    # Read agent file
    try:
        with open(agent_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        results['errors'].append(f"Failed to read file: {str(e)}")
        return False, results
    
    # Extract reference links
    links = extract_reference_links(content, agent_name)
    results['links_found'] = len(links)
    
    if len(links) == 0:
        results['warnings'].append("No reference links found - agent may not use modular pattern")
        log_warning(f"{agent_name}: No modular reference links found")
        return True, results  # Not an error, just informational
    
    log_info(f"{agent_name}: Found {len(links)} reference link(s)", verbose)
    
    # Validate each link
    for link in links:
        log_info(f"  Checking: {link['path']} (line {link['line']})", verbose)
        
        # Validate file exists
        file_ok, file_error = validate_file_exists(base_dir, link)
        if not file_ok:
            results['errors'].append({
                'link': link['path'],
                'line': link['line'],
                'error': file_error
            })
            results['links_broken'] += 1
            log_error(f"  {file_error}")
            continue
        
        # Validate section reference if present
        section_ok, section_error = validate_section_reference(base_dir, link)
        if not section_ok:
            results['errors'].append({
                'link': link['path'],
                'line': link['line'],
                'error': section_error
            })
            results['links_broken'] += 1
            log_error(f"  {section_error}")
            continue
        
        results['links_valid'] += 1
        log_info(f"  ✓ Valid: {link['path']}", verbose)
    
    success = results['links_broken'] == 0
    return success, results

def get_builders_from_filesystem(agents_dir: Path) -> List[str]:
    """
    Dynamically discover builders from the filesystem.
    Returns list of builder names (without .md extension).
    """
    builders = []
    if agents_dir.exists():
        for file in agents_dir.glob('*-builder.md'):
            builders.append(file.stem)
    return sorted(builders)

def validate_extended_reference_files(base_dir: Path, verbose: bool = False) -> Tuple[bool, Dict]:
    """
    Validate that all expected extended reference files exist and are accessible.
    """
    reference_dir = base_dir / 'governance' / 'agents' / 'builder-references'
    agents_dir = base_dir / '.github' / 'agents'
    
    results = {
        'directory': str(reference_dir.relative_to(base_dir)),
        'directory_exists': reference_dir.exists(),
        'readme_exists': False,
        'reference_files': [],
        'errors': []
    }
    
    if not reference_dir.exists():
        results['errors'].append(f"Reference directory does not exist: {reference_dir}")
        return False, results
    
    # Check README exists
    readme_path = reference_dir / 'README.md'
    results['readme_exists'] = readme_path.exists()
    
    if not results['readme_exists']:
        results['errors'].append("README.md not found in builder-references directory")
    
    # Dynamically discover builders from filesystem
    expected_builders = get_builders_from_filesystem(agents_dir)
    
    for builder in expected_builders:
        ref_file = reference_dir / f'{builder}-extended-reference.md'
        file_info = {
            'builder': builder,
            'file': f'{builder}-extended-reference.md',
            'exists': ref_file.exists(),
            'readable': False,
            'size': 0
        }
        
        if ref_file.exists():
            try:
                with open(ref_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    file_info['readable'] = True
                    file_info['size'] = len(content)
            except Exception as e:
                file_info['error'] = f"File exists but not readable: {str(e)}"
                results['errors'].append(file_info['error'])
        else:
            file_info['error'] = f"Extended reference file missing: {ref_file.name}"
            results['errors'].append(file_info['error'])
        
        results['reference_files'].append(file_info)
    
    success = len(results['errors']) == 0
    return success, results

def generate_evidence_report(all_results: Dict, output_path: Path):
    """Generate evidence report in JSON format"""
    evidence = {
        'validation_timestamp': datetime.now().astimezone().isoformat(),
        'validator': 'validate_builder_modular_links.py',
        'version': '1.0.0',
        'authority': 'PR #453 (Builder Agent Modularization)',
        'status': 'COMPLETE' if all_results['overall_success'] else 'FAILED',
        'summary': {
            'total_agents_validated': all_results['total_agents'],
            'agents_passed': all_results['agents_passed'],
            'agents_failed': all_results['agents_failed'],
            'total_links_found': all_results['total_links'],
            'total_links_valid': all_results['valid_links'],
            'total_links_broken': all_results['broken_links']
        },
        'builder_results': all_results['builder_results'],
        'reference_directory_validation': all_results['reference_validation'],
        'compliance_status': {
            'modular_pattern_compliant': all_results['overall_success'],
            'all_links_accessible': all_results['broken_links'] == 0,
            'reference_files_complete': all_results['reference_validation']['directory_exists'] 
                                       and all_results['reference_validation']['readme_exists']
        }
    }
    
    # Write JSON evidence
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(evidence, f, indent=2)
    
    log_success(f"Evidence report written to: {output_path}")

def main():
    """Main validation function"""
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    
    print("=" * 80)
    print("BUILDER AGENT MODULAR LINK VALIDATION")
    print("=" * 80)
    print()
    print("Authority: PR #453 (Builder Agent Modularization)")
    print("Pattern: Core + Reference Modular")
    print("Version: 1.0.0")
    print()
    
    base_dir = Path(__file__).parent.parent
    agents_dir = base_dir / '.github' / 'agents'
    
    # Track overall results
    all_results = {
        'overall_success': True,
        'total_agents': 0,
        'agents_passed': 0,
        'agents_failed': 0,
        'total_links': 0,
        'valid_links': 0,
        'broken_links': 0,
        'builder_results': [],
        'reference_validation': {}
    }
    
    # Validate extended reference directory structure
    print("Validating extended reference directory structure...")
    print("-" * 80)
    ref_success, ref_results = validate_extended_reference_files(base_dir, verbose)
    all_results['reference_validation'] = ref_results
    
    if ref_success:
        log_success("Reference directory structure valid")
    else:
        log_error("Reference directory structure has issues:")
        for error in ref_results['errors']:
            log_error(f"  {error}")
        all_results['overall_success'] = False
    
    print()
    
    # Validate each builder agent file
    print("Validating builder agent modular links...")
    print("-" * 80)
    
    # Dynamically discover builders from filesystem
    builders = get_builders_from_filesystem(agents_dir)
    
    if not builders:
        log_warning("No builder files found in .github/agents/")
        all_results['overall_success'] = False
    
    for builder in builders:
        agent_file = agents_dir / f'{builder}.md'
        
        if not agent_file.exists():
            log_warning(f"Builder file not found: {agent_file.name}")
            continue
        
        all_results['total_agents'] += 1
        success, results = validate_builder_agent_file(base_dir, agent_file, verbose)
        
        all_results['builder_results'].append(results)
        all_results['total_links'] += results['links_found']
        all_results['valid_links'] += results['links_valid']
        all_results['broken_links'] += results['links_broken']
        
        if success:
            all_results['agents_passed'] += 1
            if results['links_found'] > 0:
                log_success(f"{builder}: {results['links_valid']}/{results['links_found']} links valid")
            else:
                log_info(f"{builder}: No modular links (may not use pattern)", True)
        else:
            all_results['agents_failed'] += 1
            all_results['overall_success'] = False
            log_error(f"{builder}: {results['links_broken']} broken link(s)")
            for error in results['errors']:
                if isinstance(error, dict):
                    log_error(f"  Line {error['line']}: {error['error']}")
                else:
                    log_error(f"  {error}")
    
    print()
    print("=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print()
    
    print(f"Agents Validated: {all_results['total_agents']}")
    print(f"  Passed: {all_results['agents_passed']}")
    print(f"  Failed: {all_results['agents_failed']}")
    print()
    print(f"Modular Links: {all_results['total_links']}")
    print(f"  Valid: {all_results['valid_links']}")
    print(f"  Broken: {all_results['broken_links']}")
    print()
    
    # Generate evidence report
    evidence_path = base_dir / 'builder-modular-link-validation-evidence.json'
    generate_evidence_report(all_results, evidence_path)
    print()
    
    if all_results['overall_success']:
        log_success("✅ ALL VALIDATIONS PASSED")
        print()
        print("✅ All modular links are valid and accessible")
        print("✅ Reference directory structure is complete")
        print("✅ Split-modular pattern maintains integrity")
        print()
        print("Builder agent modularization is compliant.")
        return 0
    else:
        log_error("❌ VALIDATION FAILED")
        print()
        print("❌ One or more modular links are broken")
        print("❌ Builder agent modularization has integrity issues")
        print()
        print("Review errors above and fix broken links.")
        print("Ensure all referenced files exist and sections are present.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
