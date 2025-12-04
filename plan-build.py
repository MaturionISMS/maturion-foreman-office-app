#!/usr/bin/env python3
"""
Maturion Foreman - Build Planning Script (Phase 6 - Build Orchestration)

This script generates a comprehensive build plan for a module based on:
- Module readiness reports
- Architecture standardisation results
- Builder capabilities
- Change management rules
- QA and compliance requirements

Usage:
    python3 plan-build.py <module_name>
    python3 plan-build.py PIT
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class BuildPlanner:
    """Generates build plans for ISMS modules"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.module_name = None
        self.module_readiness = {}
        self.standardisation_data = {}
        self.builder_manifest = {}
        self.builder_capabilities = {}
        self.architecture_index = {}
        self.build_plan = {}
        self.errors = []
        self.warnings = []
        
    def load_module_readiness(self, module_name: str) -> bool:
        """Load module readiness report"""
        readiness_file = (
            self.repo_root / 
            "MODULE_READINESS_REPORTS" / 
            f"{module_name}_READINESS_REPORT.md"
        )
        
        if not readiness_file.exists():
            self.errors.append(f"Module readiness report not found: {readiness_file}")
            return False
            
        # Parse the readiness report (markdown format)
        with open(readiness_file, 'r') as f:
            content = f.read()
            
        # Extract key information
        self.module_readiness = {
            'module': module_name,
            'report_file': str(readiness_file),
            'exists': True,
            'content': content
        }
        
        # Parse completeness score
        import re
        # Try multiple patterns for completeness
        completeness_match = re.search(r'Completeness Score[:\s]+(\d+\.?\d*)%', content)
        if not completeness_match:
            completeness_match = re.search(r'(\d+\.?\d*)%\s+\(\d+/\d+ components\)', content)
        if completeness_match:
            self.module_readiness['completeness'] = float(completeness_match.group(1))
        
        # Parse status - try multiple patterns
        status_match = re.search(r'\*\*Readiness Status\*\*:\s+\*\*([A-Z_]+)\*\*', content)
        if not status_match:
            status_match = re.search(r'Readiness Status[:\s]+\*\*([A-Z_]+)\*\*', content)
        if not status_match:
            status_match = re.search(r'Status[:\s]+\*\*([A-Z_]+)\*\*', content)
        if status_match:
            self.module_readiness['status'] = status_match.group(1)
            
        return True
    
    def load_standardisation_results(self) -> bool:
        """Load architecture standardisation results"""
        std_file = self.repo_root / "standardisation_results.json"
        
        if not std_file.exists():
            self.warnings.append("Standardisation results not found - using defaults")
            return True
            
        try:
            with open(std_file, 'r') as f:
                self.standardisation_data = json.load(f)
            return True
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in standardisation_results.json: {e}")
            return False
    
    def load_builder_manifest(self) -> bool:
        """Load builder manifest"""
        manifest_file = self.repo_root / "foreman" / "builder-manifest.json"
        
        if not manifest_file.exists():
            self.errors.append("Builder manifest not found")
            return False
            
        try:
            with open(manifest_file, 'r') as f:
                self.builder_manifest = json.load(f)
            return True
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in builder-manifest.json: {e}")
            return False
    
    def load_builder_capabilities(self) -> bool:
        """Load builder capability map"""
        cap_file = self.repo_root / "foreman" / "builder" / "builder-capability-map.json"
        
        if not cap_file.exists():
            self.errors.append("Builder capability map not found")
            return False
            
        try:
            with open(cap_file, 'r') as f:
                self.builder_capabilities = json.load(f)
            return True
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in builder-capability-map.json: {e}")
            return False
    
    def load_architecture_index(self) -> bool:
        """Load architecture index"""
        index_file = self.repo_root / "ARCHITECTURE_INDEX.json"
        
        if not index_file.exists():
            self.warnings.append("Architecture index not found - build plan may be incomplete")
            return True
            
        try:
            with open(index_file, 'r') as f:
                self.architecture_index = json.load(f)
            return True
        except json.JSONDecodeError as e:
            self.warnings.append(f"Could not parse architecture index: {e}")
            return True
    
    def analyze_module_dependencies(self) -> List[str]:
        """Analyze module dependencies"""
        dependencies = []
        
        # Check standardisation data for dependencies
        if self.standardisation_data and 'modules' in self.standardisation_data:
            modules = self.standardisation_data['modules']
            if isinstance(modules, dict) and self.module_name in modules:
                module_data = modules[self.module_name]
                dependencies = module_data.get('dependencies', [])
            elif isinstance(modules, list):
                for mod in modules:
                    if mod.get('module') == self.module_name:
                        dependencies = mod.get('dependencies', [])
                        break
        
        return dependencies
    
    def identify_missing_components(self) -> List[Dict]:
        """Identify missing architecture components"""
        missing = []
        
        # Parse from readiness report
        content = self.module_readiness.get('content', '')
        
        # Find all missing components in the report
        import re
        missing_pattern = r'❌.*?Missing:\s+([A-Z_]+)'
        matches = re.findall(missing_pattern, content)
        
        for component in matches:
            missing.append({
                'component': component,
                'priority': 'HIGH' if component in ['INTEGRATION_SPEC', 'DATABASE_SCHEMA'] else 'MEDIUM'
            })
        
        return missing
    
    def assess_build_readiness(self) -> Dict:
        """Assess overall build readiness"""
        readiness = {
            'ready_for_build': False,
            'blockers': [],
            'warnings': [],
            'prerequisites': []
        }
        
        # Check module status
        status = self.module_readiness.get('status', 'UNKNOWN')
        if status != 'READY':
            readiness['blockers'].append(f"Module status is {status}, not READY")
        
        # Check completeness
        completeness = self.module_readiness.get('completeness', 0)
        if completeness < 50:
            readiness['blockers'].append(f"Module completeness is only {completeness}%")
        elif completeness < 80:
            readiness['warnings'].append(f"Module completeness is {completeness}% - some components missing")
        
        # Check for missing critical components
        missing = self.identify_missing_components()
        critical_missing = [m for m in missing if m['priority'] == 'HIGH']
        
        if critical_missing:
            readiness['blockers'].append(
                f"Critical components missing: {', '.join([m['component'] for m in critical_missing])}"
            )
        
        # Determine if ready
        readiness['ready_for_build'] = len(readiness['blockers']) == 0
        
        return readiness
    
    def create_build_phases(self) -> List[Dict]:
        """Create build phases based on builder sequencing"""
        phases = []
        
        # Phase 1: Schema Foundation
        phases.append({
            'phase': 1,
            'name': 'Schema Foundation',
            'description': 'Database schema, models, and migrations',
            'builder': 'schema-builder',
            'dependencies': [],
            'deliverables': [
                'Database schema implementation',
                'Schema migrations',
                'Model definitions',
                'Schema validation tests'
            ]
        })
        
        # Phase 2: API Implementation
        phases.append({
            'phase': 2,
            'name': 'API Implementation',
            'description': 'Backend API routes, edge functions, business logic',
            'builder': 'api-builder',
            'dependencies': ['Phase 1: Schema Foundation'],
            'deliverables': [
                'API routes and handlers',
                'Edge functions',
                'Business logic implementation',
                'API tests'
            ]
        })
        
        # Phase 3: Integration Layer
        phases.append({
            'phase': 3,
            'name': 'Integration Layer',
            'description': 'Inter-module integrations and event handling',
            'builder': 'integration-builder',
            'dependencies': ['Phase 2: API Implementation'],
            'deliverables': [
                'Module integration logic',
                'Event handlers',
                'Integration tests',
                'Integration documentation'
            ]
        })
        
        # Phase 4: UI Components
        phases.append({
            'phase': 4,
            'name': 'UI Components',
            'description': 'Frontend components, layouts, and user interface',
            'builder': 'ui-builder',
            'dependencies': ['Phase 2: API Implementation'],
            'deliverables': [
                'UI components',
                'Page layouts',
                'Component tests',
                'UI documentation'
            ]
        })
        
        # Phase 5: QA & Validation
        phases.append({
            'phase': 5,
            'name': 'QA & Validation',
            'description': 'End-to-end testing, QA-of-QA, compliance validation',
            'builder': 'qa-builder',
            'dependencies': ['Phase 3: Integration Layer', 'Phase 4: UI Components'],
            'deliverables': [
                'End-to-end tests',
                'Integration test suite',
                'QA-of-QA report',
                'Compliance validation report',
                'Test coverage report'
            ]
        })
        
        return phases
    
    def generate_build_plan(self, module_name: str) -> Dict:
        """Generate complete build plan"""
        self.module_name = module_name
        
        # Load all required data
        if not self.load_module_readiness(module_name):
            return {'success': False, 'errors': self.errors}
        
        self.load_standardisation_results()
        
        if not self.load_builder_manifest():
            return {'success': False, 'errors': self.errors}
        
        if not self.load_builder_capabilities():
            return {'success': False, 'errors': self.errors}
        
        self.load_architecture_index()
        
        # Analyze module
        dependencies = self.analyze_module_dependencies()
        missing_components = self.identify_missing_components()
        readiness = self.assess_build_readiness()
        phases = self.create_build_phases()
        
        # Build the plan
        self.build_plan = {
            'version': '1.0',
            'generated': datetime.now().isoformat(),
            'module': module_name,
            'build_wave': 0,
            'metadata': {
                'completeness': self.module_readiness.get('completeness', 0),
                'status': self.module_readiness.get('status', 'UNKNOWN'),
                'dependencies': dependencies,
                'missing_components_count': len(missing_components)
            },
            'readiness': readiness,
            'missing_components': missing_components,
            'build_phases': phases,
            'builders_required': [
                'schema-builder',
                'api-builder',
                'integration-builder',
                'ui-builder',
                'qa-builder'
            ],
            'estimated_tasks': len(missing_components) + len(phases) * 3,
            'warnings': self.warnings,
            'notes': [
                'This is Build Wave 0 - a dry-run to validate orchestration',
                'Actual module construction requires architecture completion',
                'All builders must respect governance boundaries',
                'QA-of-QA gates must pass before proceeding to next phase'
            ]
        }
        
        return {'success': True, 'plan': self.build_plan}
    
    def save_build_plan(self, output_file: Optional[Path] = None) -> bool:
        """Save build plan to JSON file"""
        if not output_file:
            output_file = self.repo_root / "build-plan.json"
        
        try:
            with open(output_file, 'w') as f:
                json.dump(self.build_plan, f, indent=2)
            print(f"✓ Build plan saved to: {output_file}")
            return True
        except Exception as e:
            self.errors.append(f"Failed to save build plan: {e}")
            return False
    
    def print_summary(self):
        """Print build plan summary"""
        print("\n" + "=" * 80)
        print(f"BUILD PLAN SUMMARY - {self.module_name}")
        print("=" * 80)
        
        if self.build_plan:
            print(f"\nModule: {self.build_plan['module']}")
            print(f"Build Wave: {self.build_plan['build_wave']}")
            print(f"Generated: {self.build_plan['generated']}")
            print(f"\nCompleteness: {self.build_plan['metadata']['completeness']}%")
            print(f"Status: {self.build_plan['metadata']['status']}")
            
            readiness = self.build_plan['readiness']
            print(f"\nReady for Build: {'✓ YES' if readiness['ready_for_build'] else '✗ NO'}")
            
            if readiness['blockers']:
                print("\n⚠️  BLOCKERS:")
                for blocker in readiness['blockers']:
                    print(f"  - {blocker}")
            
            if readiness['warnings']:
                print("\n⚠️  WARNINGS:")
                for warning in readiness['warnings']:
                    print(f"  - {warning}")
            
            print(f"\nMissing Components: {len(self.build_plan['missing_components'])}")
            print(f"Build Phases: {len(self.build_plan['build_phases'])}")
            print(f"Estimated Tasks: {self.build_plan['estimated_tasks']}")
            
            print("\nBUILD PHASES:")
            for phase in self.build_plan['build_phases']:
                print(f"  Phase {phase['phase']}: {phase['name']}")
                print(f"    Builder: {phase['builder']}")
                print(f"    Deliverables: {len(phase['deliverables'])}")
        
        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if self.errors:
            print("\n✗ ERRORS:")
            for error in self.errors:
                print(f"  - {error}")
        
        print("\n" + "=" * 80)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 plan-build.py <module_name>")
        print("Example: python3 plan-build.py PIT")
        sys.exit(1)
    
    module_name = sys.argv[1].upper()
    
    # Find repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir
    
    print(f"\n🔨 Maturion Foreman - Build Planning")
    print(f"Module: {module_name}")
    print(f"Repository: {repo_root}\n")
    
    planner = BuildPlanner(repo_root)
    result = planner.generate_build_plan(module_name)
    
    if result['success']:
        planner.save_build_plan()
        planner.print_summary()
        sys.exit(0)
    else:
        print("\n✗ Build planning failed:")
        for error in result['errors']:
            print(f"  - {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
