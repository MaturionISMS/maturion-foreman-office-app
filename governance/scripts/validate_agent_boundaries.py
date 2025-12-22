#!/usr/bin/env python3
"""
Agent QA Boundary Enforcement Script

Validates that all QA reports are correctly attributed to the appropriate agent type
and scope, enforcing strict separation of duties in QA execution.

This is enforcement-only validation. It does NOT run QA.
It does NOT discover defects. It only validates agent attribution.

Exit Codes:
    0 - All agent boundaries respected
    1 - Agent boundary violation detected (CATASTROPHIC)
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional


class AgentBoundaryViolation(Exception):
    """Raised when agent boundary is violated"""
    pass


class AgentBoundaryValidator:
    """Validates agent-scoped QA boundaries"""
    
    # Valid agent type and scope combinations
    VALID_COMBINATIONS = {
        'builder': ['builder-qa'],
        'governance': ['governance-qa'],
        'fm': ['fm-qa']
    }
    
    # Expected repositories per agent type
    EXPECTED_REPOS = {
        'builder': ['isms-', 'maturion-isms-'],  # Prefixes for ISMS module repos
        'governance': ['maturion-foreman-governance'],
        'fm': ['maturion-foreman-office-app']
    }
    
    def __init__(self, current_repo: str):
        """
        Initialize validator.
        
        Args:
            current_repo: Current repository name (e.g., 'MaturionISMS/repo-name')
        """
        self.current_repo = current_repo
        self.violations = []
    
    def validate_qa_report(self, report_path: Path) -> Dict:
        """
        Validate single QA report for agent boundary compliance.
        
        Args:
            report_path: Path to QA report JSON file
            
        Returns:
            dict: Validation result with violations if any
        """
        try:
            with open(report_path) as f:
                report = json.load(f)
        except json.JSONDecodeError as e:
            return {
                'valid': False,
                'violation_type': 'INVALID_JSON',
                'severity': 'HIGH',
                'message': f'QA report is not valid JSON: {e}',
                'file': str(report_path)
            }
        except Exception as e:
            return {
                'valid': False,
                'violation_type': 'READ_ERROR',
                'severity': 'HIGH',
                'message': f'Failed to read QA report: {e}',
                'file': str(report_path)
            }
        
        # Check for agent attribution metadata
        if 'qa_report_metadata' not in report:
            return {
                'valid': False,
                'violation_type': 'MISSING_AGENT_ATTRIBUTION',
                'severity': 'HIGH',
                'message': 'QA report missing qa_report_metadata section',
                'file': str(report_path)
            }
        
        metadata = report['qa_report_metadata']
        
        # Validate required fields
        required_fields = ['agent_type', 'agent_id', 'scope', 'repository', 'timestamp']
        missing_fields = [f for f in required_fields if f not in metadata]
        
        if missing_fields:
            return {
                'valid': False,
                'violation_type': 'MISSING_AGENT_ATTRIBUTION',
                'severity': 'HIGH',
                'message': f'QA report missing required attribution fields: {missing_fields}',
                'missing_fields': missing_fields,
                'file': str(report_path)
            }
        
        agent_type = metadata['agent_type']
        scope = metadata['scope']
        repository = metadata['repository']
        
        # Check if agent type is known
        if agent_type not in self.VALID_COMBINATIONS:
            return {
                'valid': False,
                'violation_type': 'UNKNOWN_AGENT_TYPE',
                'severity': 'CATASTROPHIC',
                'message': f'Unknown agent type: {agent_type}',
                'agent_type': agent_type,
                'file': str(report_path)
            }
        
        # Check if scope matches agent type (cross-agent QA detection)
        if scope not in self.VALID_COMBINATIONS[agent_type]:
            return {
                'valid': False,
                'violation_type': 'CROSS_AGENT_QA_EXECUTION',
                'severity': 'CATASTROPHIC',
                'message': f'{agent_type} agent executed {scope} (prohibited)',
                'agent_type': agent_type,
                'scope': scope,
                'expected_scopes': self.VALID_COMBINATIONS[agent_type],
                'file': str(report_path)
            }
        
        # Check repository attribution (if strict checking enabled)
        if agent_type != 'builder':  # Builder can be in any ISMS repo
            expected = self.EXPECTED_REPOS[agent_type]
            # Check if repository matches any of the expected patterns
            matches = any(repository == expected_repo or repository.startswith(expected_repo) 
                         for expected_repo in expected)
            if not matches:
                return {
                    'valid': False,
                    'violation_type': 'INCORRECT_REPOSITORY_ATTRIBUTION',
                    'severity': 'HIGH',
                    'message': f'{agent_type} QA in wrong repository: {repository}',
                    'agent_type': agent_type,
                    'repository': repository,
                    'expected_repos': expected,
                    'file': str(report_path)
                }
        
        # All checks passed
        return {
            'valid': True,
            'agent_type': agent_type,
            'scope': scope,
            'repository': repository,
            'file': str(report_path)
        }
    
    def validate_all_reports(self, report_paths: List[Path]) -> Dict:
        """
        Validate all QA reports for agent boundary compliance.
        
        Args:
            report_paths: List of paths to QA report files
            
        Returns:
            dict: Overall validation result
        """
        results = []
        violations = []
        catastrophic_violations = []
        
        for report_path in report_paths:
            result = self.validate_qa_report(report_path)
            results.append(result)
            
            if not result['valid']:
                violations.append(result)
                if result.get('severity') == 'CATASTROPHIC':
                    catastrophic_violations.append(result)
        
        return {
            'total_reports': len(report_paths),
            'valid_reports': sum(1 for r in results if r['valid']),
            'invalid_reports': sum(1 for r in results if not r['valid']),
            'violations': violations,
            'catastrophic_violations': catastrophic_violations,
            'all_valid': len(violations) == 0,
            'results': results
        }
    
    def print_report(self, validation_result: Dict):
        """Print human-readable validation report"""
        print("=" * 70)
        print("AGENT QA BOUNDARY ENFORCEMENT REPORT")
        print("=" * 70)
        print()
        print(f"Repository: {self.current_repo}")
        print(f"Total QA Reports: {validation_result['total_reports']}")
        print(f"Valid Reports: {validation_result['valid_reports']}")
        print(f"Invalid Reports: {validation_result['invalid_reports']}")
        print()
        
        if validation_result['all_valid']:
            print("✅ ALL AGENT BOUNDARIES RESPECTED")
            print()
            print("All QA reports correctly attributed to appropriate agents.")
            print("No cross-agent QA execution detected.")
            print("Agent-scoped QA boundaries enforced.")
            return
        
        # Print violations
        print("❌ AGENT BOUNDARY VIOLATIONS DETECTED")
        print()
        
        if validation_result['catastrophic_violations']:
            print("🚨 CATASTROPHIC VIOLATIONS (Immediate Escalation Required):")
            print()
            for v in validation_result['catastrophic_violations']:
                print(f"  Type: {v['violation_type']}")
                print(f"  File: {v['file']}")
                print(f"  Message: {v['message']}")
                if 'agent_type' in v:
                    print(f"  Agent Type: {v['agent_type']}")
                if 'scope' in v:
                    print(f"  Scope: {v['scope']}")
                print()
        
        if len(validation_result['violations']) > len(validation_result['catastrophic_violations']):
            print("OTHER VIOLATIONS:")
            print()
            for v in validation_result['violations']:
                if v.get('severity') != 'CATASTROPHIC':
                    print(f"  Type: {v['violation_type']}")
                    print(f"  Severity: {v['severity']}")
                    print(f"  File: {v['file']}")
                    print(f"  Message: {v['message']}")
                    print()
        
        print("=" * 70)
        print("REQUIRED ACTIONS:")
        print("=" * 70)
        print()
        
        if validation_result['catastrophic_violations']:
            print("1. HALT all related work immediately")
            print("2. Identify which agent executed wrong QA scope")
            print("3. Remove violating QA report(s)")
            print("4. Execute QA in correct agent scope")
            print("5. Update agent contract to prevent recurrence")
            print("6. ESCALATE to Johan Ras")
            print()
            print("This is a CATASTROPHIC governance violation.")
            print("Merge is BLOCKED until violation resolved.")
        else:
            print("1. Fix agent attribution in QA reports")
            print("2. Ensure all required fields present")
            print("3. Verify repository attribution correct")
            print("4. Re-run validation")


def find_qa_reports(search_paths: List[str]) -> List[Path]:
    """
    Find all QA report JSON files in given paths.
    
    Args:
        search_paths: List of paths to search (files or directories)
        
    Returns:
        list: Paths to QA report files
    """
    reports = []
    
    for path_str in search_paths:
        if not path_str or path_str.isspace():
            continue
            
        path = Path(path_str.strip())
        
        if not path.exists():
            continue
        
        if path.is_file():
            # Check if file name suggests it's a QA report
            if 'qa' in path.name.lower() and 'report' in path.name.lower() and path.suffix == '.json':
                reports.append(path)
        elif path.is_dir():
            # Search recursively for QA report files
            reports.extend(path.rglob('*qa*report*.json'))
            reports.extend(path.rglob('*qa_report*.json'))
    
    return list(set(reports))  # Deduplicate


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Validate agent-scoped QA boundaries',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --reports "./builder-qa-report.json" --current-repo "MaturionISMS/isms-module"
  %(prog)s --reports "reports/" --current-repo "MaturionISMS/maturion-foreman-office-app"
  
Exit Codes:
  0 - All agent boundaries respected
  1 - Agent boundary violation detected
        """
    )
    
    parser.add_argument(
        '--reports',
        required=True,
        help='Space-separated list of QA report files or directories to validate'
    )
    
    parser.add_argument(
        '--current-repo',
        required=True,
        help='Current repository name (e.g., MaturionISMS/repo-name)'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output result as JSON instead of human-readable report'
    )
    
    args = parser.parse_args()
    
    # Parse report paths
    report_paths = args.reports.split()
    
    # Find all QA report files
    qa_reports = find_qa_reports(report_paths)
    
    if not qa_reports:
        print("⚠️  No QA report files found")
        print(f"Searched paths: {report_paths}")
        print()
        print("This may indicate:")
        print("  - QA reports not yet generated")
        print("  - QA reports in unexpected location")
        print("  - Incorrect path provided")
        sys.exit(0)  # Not a violation, just no reports to validate
    
    # Validate
    validator = AgentBoundaryValidator(args.current_repo)
    result = validator.validate_all_reports(qa_reports)
    
    # Output result
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        validator.print_report(result)
    
    # Exit code
    if result['all_valid']:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
