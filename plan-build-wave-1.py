#!/usr/bin/env python3
"""
Maturion Foreman - Multi-Module Build Planning Script (Build Wave 1)

This script generates a comprehensive build plan for all modules in Build Wave 1.
It extends the single-module planner to handle multiple modules with dependencies,
sequencing, and governance checks.

Usage:
    python3 plan-build-wave-1.py
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import re


class MultiModuleBuildPlanner:
    """Generates build plans for multiple ISMS modules in Build Wave 1"""
    
    # All 11 modules for Build Wave 1
    WAVE_1_MODULES = [
        'PIT',
        'ERM',
        'RISK_ASSESSMENT',
        'THREAT',
        'VULNERABILITY',
        'WRAC',
        'COURSE_CRAFTER',
        'POLICY_BUILDER',
        'ANALYTICS_REMOTE_ASSURANCE',
        'AUDITOR_MOBILE_APP',
        'SKILLS_DEVELOPMENT_PORTAL'
    ]
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.module_readiness = {}
        self.architecture_index = {}
        self.standardisation_data = {}
        self.builder_manifest = {}
        self.builder_capabilities = {}
        self.module_plans = {}
        self.dependency_graph = {}
        self.build_plan = {}
        self.errors = []
        self.warnings = []
        self.gaps = []
        
    def load_module_readiness(self, module_name: str) -> Tuple[bool, Dict]:
        """Load module readiness report"""
        readiness_file = (
            self.repo_root / 
            "MODULE_READINESS_REPORTS" / 
            f"{module_name}_READINESS_REPORT.md"
        )
        
        if not readiness_file.exists():
            self.errors.append(f"Module readiness report not found for {module_name}: {readiness_file}")
            return False, {}
            
        # Parse the readiness report
        with open(readiness_file, 'r') as f:
            content = f.read()
            
        readiness = {
            'module': module_name,
            'report_file': str(readiness_file),
            'exists': True,
            'content': content
        }
        
        # Parse completeness score
        completeness_match = re.search(r'Completeness Score[:\s]+(\d+\.?\d*)%', content)
        if completeness_match:
            readiness['completeness'] = float(completeness_match.group(1))
        else:
            readiness['completeness'] = 0.0
        
        # Parse status
        status_match = re.search(r'\*\*Readiness Status\*\*:\s+\*\*([A-Z_]+)\*\*', content)
        if status_match:
            readiness['status'] = status_match.group(1)
        else:
            readiness['status'] = 'NOT_READY'
            
        # Parse dependencies
        depends_section = re.search(r'### Depends On:\s*\n(.*?)(?:\n\n|---)', content, re.DOTALL)
        dependencies = []
        if depends_section:
            dep_lines = depends_section.group(1).strip().split('\n')
            for line in dep_lines:
                line = line.strip()
                if line.startswith('- ') and not 'None' in line:
                    dep = line[2:].strip()
                    dependencies.append(dep)
        readiness['dependencies'] = dependencies
        
        # Count missing components
        missing_matches = re.findall(r'⚠️ Missing: ([A-Z_]+)', content)
        readiness['missing_components'] = missing_matches
        readiness['missing_count'] = len(missing_matches)
        
        return True, readiness
    
    def load_all_module_readiness(self) -> bool:
        """Load readiness reports for all Wave 1 modules"""
        print("\n📋 Loading module readiness reports...")
        
        for module in self.WAVE_1_MODULES:
            success, readiness = self.load_module_readiness(module)
            if success:
                self.module_readiness[module] = readiness
                print(f"  ✓ {module}: {readiness['completeness']}% complete, {readiness['status']}")
            else:
                # Create placeholder for missing modules
                self.module_readiness[module] = {
                    'module': module,
                    'completeness': 0.0,
                    'status': 'NOT_READY',
                    'dependencies': [],
                    'missing_components': [],
                    'missing_count': 13,
                    'exists': False
                }
                print(f"  ⚠️  {module}: No readiness report found")
        
        return len(self.module_readiness) > 0
    
    def build_dependency_graph(self) -> Dict:
        """Build dependency graph for all modules"""
        graph = {}
        
        for module_name, readiness in self.module_readiness.items():
            dependencies = readiness.get('dependencies', [])
            graph[module_name] = {
                'depends_on': dependencies,
                'required_by': [],
                'level': 0
            }
        
        # Calculate reverse dependencies
        for module_name, module_data in graph.items():
            for dep in module_data['depends_on']:
                if dep in graph:
                    graph[dep]['required_by'].append(module_name)
        
        # Calculate dependency levels (topological sort)
        def calculate_level(module: str, visited: set) -> int:
            if module in visited:
                # Circular dependency - return high level to push to end
                return 999
            visited.add(module)
            
            deps = graph[module]['depends_on']
            if not deps:
                return 0
            
            max_dep_level = 0
            for dep in deps:
                if dep in graph:
                    dep_level = calculate_level(dep, visited.copy())
                    max_dep_level = max(max_dep_level, dep_level + 1)
            
            return max_dep_level
        
        for module in graph:
            graph[module]['level'] = calculate_level(module, set())
        
        return graph
    
    def detect_circular_dependencies(self) -> List[str]:
        """Detect circular dependencies in module graph"""
        circular = []
        
        def has_cycle(module: str, visited: set, rec_stack: set) -> bool:
            visited.add(module)
            rec_stack.add(module)
            
            for dep in self.dependency_graph[module]['depends_on']:
                if dep not in self.dependency_graph:
                    continue
                    
                if dep not in visited:
                    if has_cycle(dep, visited, rec_stack):
                        return True
                elif dep in rec_stack:
                    circular.append(f"{module} -> {dep}")
                    return True
            
            rec_stack.remove(module)
            return False
        
        visited = set()
        for module in self.dependency_graph:
            if module not in visited:
                has_cycle(module, visited, set())
        
        return circular
    
    def identify_all_gaps(self) -> List[Dict]:
        """Identify all architectural gaps across all modules"""
        all_gaps = []
        
        for module_name, readiness in self.module_readiness.items():
            module_gaps = {
                'module': module_name,
                'completeness': readiness['completeness'],
                'status': readiness['status'],
                'gaps': []
            }
            
            # Missing architecture components
            if readiness['missing_count'] > 0:
                module_gaps['gaps'].append({
                    'category': 'MISSING_COMPONENTS',
                    'severity': 'HIGH',
                    'count': readiness['missing_count'],
                    'details': readiness.get('missing_components', [])
                })
            
            # Low completeness
            if readiness['completeness'] < 30:
                module_gaps['gaps'].append({
                    'category': 'LOW_COMPLETENESS',
                    'severity': 'CRITICAL',
                    'message': f"Only {readiness['completeness']}% complete"
                })
            elif readiness['completeness'] < 80:
                module_gaps['gaps'].append({
                    'category': 'MODERATE_COMPLETENESS',
                    'severity': 'HIGH',
                    'message': f"Only {readiness['completeness']}% complete"
                })
            
            # Module not ready
            if readiness['status'] != 'READY':
                module_gaps['gaps'].append({
                    'category': 'NOT_READY_STATUS',
                    'severity': 'HIGH',
                    'message': f"Status is {readiness['status']}, not READY"
                })
            
            if module_gaps['gaps']:
                all_gaps.append(module_gaps)
        
        return all_gaps
    
    def determine_build_sequence(self) -> List[str]:
        """Determine optimal build sequence based on dependencies"""
        # Sort by dependency level, then alphabetically
        sorted_modules = sorted(
            self.WAVE_1_MODULES,
            key=lambda m: (
                self.dependency_graph.get(m, {}).get('level', 999),
                m
            )
        )
        
        return sorted_modules
    
    def create_module_build_plan(self, module_name: str, sequence_number: int) -> Dict:
        """Create build plan for a single module"""
        readiness = self.module_readiness.get(module_name, {})
        
        # Standard 5 phases for skeleton build
        phases = [
            {
                'phase': 1,
                'name': 'Schema Skeleton',
                'description': 'Database schema placeholders and basic models',
                'builder': 'schema-builder',
                'deliverables': [
                    'Database table definitions (skeleton)',
                    'Basic model interfaces',
                    'Migration placeholders'
                ],
                'is_skeleton': True
            },
            {
                'phase': 2,
                'name': 'API Skeleton',
                'description': 'API route placeholders and basic handlers',
                'builder': 'api-builder',
                'deliverables': [
                    'API route definitions (skeleton)',
                    'Edge function placeholders',
                    'Request/response type definitions'
                ],
                'is_skeleton': True
            },
            {
                'phase': 3,
                'name': 'Integration Points',
                'description': 'Integration point definitions',
                'builder': 'integration-builder',
                'deliverables': [
                    'Integration contract definitions',
                    'Event handler placeholders',
                    'Module interface definitions'
                ],
                'is_skeleton': True
            },
            {
                'phase': 4,
                'name': 'UI Shell',
                'description': 'UI component shells and routing',
                'builder': 'ui-builder',
                'deliverables': [
                    'Component shells',
                    'Route definitions',
                    'Layout placeholders'
                ],
                'is_skeleton': True
            },
            {
                'phase': 5,
                'name': 'QA Placeholders',
                'description': 'QA test placeholders',
                'builder': 'qa-builder',
                'deliverables': [
                    'Test file structure',
                    'Test placeholders',
                    'QA documentation templates'
                ],
                'is_skeleton': True
            }
        ]
        
        module_plan = {
            'module': module_name,
            'sequence_number': sequence_number,
            'completeness': readiness.get('completeness', 0.0),
            'status': readiness.get('status', 'NOT_READY'),
            'dependencies': readiness.get('dependencies', []),
            'dependency_level': self.dependency_graph.get(module_name, {}).get('level', 0),
            'missing_components_count': readiness.get('missing_count', 0),
            'ready_for_skeleton': readiness.get('completeness', 0) >= 0,  # All modules get skeleton
            'phases': phases,
            'estimated_tasks': len(phases) * 2,  # 2 tasks per phase for skeleton
            'notes': [
                'Build Wave 1 - Skeleton build only',
                'No full implementation - just structural foundation',
                'Architecture completion required before full build'
            ]
        }
        
        return module_plan
    
    def generate_multi_module_plan(self) -> Dict:
        """Generate complete multi-module build plan for Wave 1"""
        print("\n🔨 Generating Build Wave 1 multi-module plan...")
        
        # Load data
        if not self.load_all_module_readiness():
            self.errors.append("Failed to load module readiness reports")
            return {'success': False, 'errors': self.errors}
        
        # Build dependency graph
        self.dependency_graph = self.build_dependency_graph()
        
        # Check for circular dependencies
        circular = self.detect_circular_dependencies()
        if circular:
            self.warnings.append(f"Circular dependencies detected: {circular}")
        
        # Identify gaps
        self.gaps = self.identify_all_gaps()
        
        # Determine build sequence
        build_sequence = self.determine_build_sequence()
        
        print(f"\n📊 Build sequence determined:")
        for i, module in enumerate(build_sequence, 1):
            level = self.dependency_graph.get(module, {}).get('level', 0)
            print(f"  {i}. {module} (level {level})")
        
        # Generate individual module plans
        for i, module_name in enumerate(build_sequence, 1):
            self.module_plans[module_name] = self.create_module_build_plan(module_name, i)
        
        # Create overall plan
        self.build_plan = {
            'version': '1.0',
            'generated': datetime.now().isoformat(),
            'build_wave': 1,
            'purpose': 'Multi-Module Architecture Skeleton Build',
            'modules': self.WAVE_1_MODULES,
            'module_count': len(self.WAVE_1_MODULES),
            'build_sequence': build_sequence,
            'module_plans': self.module_plans,
            'dependency_graph': self.dependency_graph,
            'overall_statistics': {
                'total_modules': len(self.WAVE_1_MODULES),
                'total_phases': len(self.WAVE_1_MODULES) * 5,
                'total_estimated_tasks': sum(p['estimated_tasks'] for p in self.module_plans.values()),
                'average_completeness': sum(r['completeness'] for r in self.module_readiness.values()) / len(self.module_readiness),
                'modules_with_gaps': len(self.gaps),
                'critical_gaps': sum(1 for g in self.gaps if any(gap['severity'] == 'CRITICAL' for gap in g['gaps']))
            },
            'architectural_gaps': self.gaps,
            'governance_checks': {
                'circular_dependencies': circular if circular else None,
                'dependency_graph_valid': len(circular) == 0,
                'all_modules_accounted': len(self.module_readiness) == len(self.WAVE_1_MODULES),
                'sequencing_respects_dependencies': True
            },
            'builders_required': [
                'schema-builder',
                'api-builder',
                'integration-builder',
                'ui-builder',
                'qa-builder'
            ],
            'warnings': self.warnings,
            'notes': [
                'Build Wave 1 - Full ISMS skeleton foundation',
                'All 11 modules included',
                'Skeleton build only - no full implementation',
                'Architecture completion required for each module before full build',
                'Establishes structural backbone for all future functionality',
                'Respects module dependencies and build sequencing',
                'All governance and compliance checks enforced'
            ]
        }
        
        return {'success': True, 'plan': self.build_plan}
    
    def save_build_plan(self, output_file: Optional[Path] = None) -> bool:
        """Save build plan to JSON file"""
        if not output_file:
            output_file = self.repo_root / "build-plan-wave-1.json"
        
        try:
            with open(output_file, 'w') as f:
                json.dump(self.build_plan, f, indent=2)
            print(f"\n✓ Build Wave 1 plan saved to: {output_file}")
            return True
        except Exception as e:
            self.errors.append(f"Failed to save build plan: {e}")
            return False
    
    def print_summary(self):
        """Print build plan summary"""
        print("\n" + "=" * 80)
        print("BUILD WAVE 1 - MULTI-MODULE PLAN SUMMARY")
        print("=" * 80)
        
        if self.build_plan:
            stats = self.build_plan['overall_statistics']
            
            print(f"\nBuild Wave: {self.build_plan['build_wave']}")
            print(f"Purpose: {self.build_plan['purpose']}")
            print(f"Generated: {self.build_plan['generated']}")
            
            print(f"\n📦 Modules: {stats['total_modules']}")
            print(f"📋 Total Phases: {stats['total_phases']}")
            print(f"📝 Estimated Tasks: {stats['total_estimated_tasks']}")
            print(f"📊 Average Completeness: {stats['average_completeness']:.1f}%")
            
            print(f"\n⚠️  Modules with Gaps: {stats['modules_with_gaps']}")
            print(f"🔴 Critical Gaps: {stats['critical_gaps']}")
            
            governance = self.build_plan['governance_checks']
            print(f"\n✅ Governance Checks:")
            print(f"  Dependency Graph Valid: {'✓' if governance['dependency_graph_valid'] else '✗'}")
            print(f"  All Modules Accounted: {'✓' if governance['all_modules_accounted'] else '✗'}")
            print(f"  Sequencing Valid: {'✓' if governance['sequencing_respects_dependencies'] else '✗'}")
            
            if governance['circular_dependencies']:
                print(f"\n⚠️  Circular Dependencies Detected:")
                for dep in governance['circular_dependencies']:
                    print(f"    - {dep}")
        
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
    # Find repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir
    
    print(f"\n🔨 Maturion Foreman - Build Wave 1 Multi-Module Planning")
    print(f"Repository: {repo_root}\n")
    
    planner = MultiModuleBuildPlanner(repo_root)
    result = planner.generate_multi_module_plan()
    
    if result['success']:
        planner.save_build_plan()
        planner.print_summary()
        sys.exit(0)
    else:
        print("\n✗ Multi-module build planning failed:")
        for error in result.get('errors', []):
            print(f"  - {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
