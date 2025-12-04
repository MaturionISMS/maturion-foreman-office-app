#!/usr/bin/env python3
"""
Maturion Foreman - Build Status Generator for Wave 1

Generates build-status-wave-1.json tracking all modules, phases, and tasks.

Usage:
    python3 generate-build-status-wave-1.py
"""

import json
import sys
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime


class BuildStatusGenerator:
    """Generates build status structure for Wave 1"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.build_plan = {}
        self.build_tasks = {}
        self.build_status = {}
        self.errors = []
        
    def load_data(self) -> bool:
        """Load build plan and tasks"""
        # Load build plan
        plan_file = self.repo_root / "build-plan-wave-1.json"
        if not plan_file.exists():
            self.errors.append("build-plan-wave-1.json not found")
            return False
        
        with open(plan_file, 'r') as f:
            self.build_plan = json.load(f)
        
        # Load build tasks
        tasks_file = self.repo_root / "build-tasks-wave-1.json"
        if not tasks_file.exists():
            self.errors.append("build-tasks-wave-1.json not found")
            return False
        
        with open(tasks_file, 'r') as f:
            self.build_tasks = json.load(f)
        
        return True
    
    def generate_status(self) -> Dict:
        """Generate build status structure"""
        module_status = {}
        
        # Process each module
        for module_name, module_plan in self.build_plan['module_plans'].items():
            phases_status = {}
            
            # Process each phase
            for phase in module_plan['phases']:
                phase_key = f"Phase {phase['phase']}: {phase['name']}"
                
                # Count tasks for this phase
                phase_tasks = [
                    t for t in self.build_tasks['tasks']
                    if t['module'] == module_name and t['phase'] == phase['phase']
                ]
                
                phases_status[phase_key] = {
                    'status': 'NOT_STARTED',
                    'builder': phase['builder'],
                    'tasks_total': len(phase_tasks),
                    'tasks_complete': 0,
                    'tasks_in_progress': 0,
                    'blockers': []
                }
            
            module_status[module_name] = {
                'sequence_number': module_plan['sequence_number'],
                'completeness': module_plan['completeness'],
                'status': module_plan['status'],
                'ready_for_skeleton': module_plan['ready_for_skeleton'],
                'dependency_level': module_plan['dependency_level'],
                'dependencies': module_plan['dependencies'],
                'phases': phases_status,
                'overall_progress': 0.0
            }
        
        # Generate builder status
        builder_status = {}
        for builder in self.build_plan['builders_required']:
            builder_tasks = [
                t for t in self.build_tasks['tasks']
                if t['builder'] == builder
            ]
            
            builder_status[builder] = {
                'ready': True,
                'tasks_assigned': len(builder_tasks),
                'tasks_complete': 0,
                'tasks_in_progress': 0,
                'modules_assigned': len(set(t['module'] for t in builder_tasks))
            }
        
        self.build_status = {
            'version': '1.0',
            'generated': datetime.now().isoformat(),
            'build_wave': 1,
            'overall_status': 'PLANNING_COMPLETE',
            'execution_status': 'AWAITING_APPROVAL',
            'modules': module_status,
            'builder_status': builder_status,
            'orchestration': {
                'plan_generated': True,
                'tasks_generated': True,
                'sequencing_validated': True,
                'governance_checks_passed': self.build_plan['governance_checks']['dependency_graph_valid'],
                'circular_dependencies': self.build_plan['governance_checks']['circular_dependencies']
            },
            'statistics': {
                'total_modules': self.build_plan['module_count'],
                'total_tasks': self.build_tasks['total_tasks'],
                'total_phases': sum(len(m['phases']) for m in module_status.values()),
                'tasks_completed': 0,
                'overall_progress_percent': 0.0
            },
            'notes': [
                'Build Wave 1 planning complete',
                'All skeleton tasks defined',
                'Awaiting Johan approval to proceed',
                'No execution has started - this is planning phase only'
            ]
        }
        
        return self.build_status
    
    def save_status(self, output_file: Optional[Path] = None) -> bool:
        """Save build status to JSON"""
        if not output_file:
            output_file = self.repo_root / "build-status-wave-1.json"
        
        try:
            with open(output_file, 'w') as f:
                json.dump(self.build_status, f, indent=2)
            print(f"✓ Build status saved to: {output_file}")
            return True
        except Exception as e:
            self.errors.append(f"Failed to save status: {e}")
            return False
    
    def print_summary(self):
        """Print status summary"""
        print("\n" + "=" * 80)
        print("BUILD WAVE 1 - STATUS SUMMARY")
        print("=" * 80)
        
        stats = self.build_status['statistics']
        print(f"\nOverall Status: {self.build_status['overall_status']}")
        print(f"Execution Status: {self.build_status['execution_status']}")
        
        print(f"\n📊 Statistics:")
        print(f"  Total Modules: {stats['total_modules']}")
        print(f"  Total Tasks: {stats['total_tasks']}")
        print(f"  Total Phases: {stats['total_phases']}")
        print(f"  Overall Progress: {stats['overall_progress_percent']}%")
        
        orch = self.build_status['orchestration']
        print(f"\n✅ Orchestration:")
        print(f"  Plan Generated: {'✓' if orch['plan_generated'] else '✗'}")
        print(f"  Tasks Generated: {'✓' if orch['tasks_generated'] else '✗'}")
        print(f"  Sequencing Validated: {'✓' if orch['sequencing_validated'] else '✗'}")
        print(f"  Governance Checks: {'✓' if orch['governance_checks_passed'] else '✗'}")
        
        if orch['circular_dependencies']:
            print(f"\n⚠️  Circular Dependencies:")
            for dep in orch['circular_dependencies']:
                print(f"    - {dep}")
        
        print("\n" + "=" * 80)


def main():
    script_dir = Path(__file__).parent
    repo_root = script_dir
    
    print(f"\n🔨 Maturion Foreman - Build Wave 1 Status Generation")
    print(f"Repository: {repo_root}\n")
    
    generator = BuildStatusGenerator(repo_root)
    
    if not generator.load_data():
        print("\n✗ Status generation failed:")
        for error in generator.errors:
            print(f"  - {error}")
        sys.exit(1)
    
    generator.generate_status()
    generator.save_status()
    generator.print_summary()
    
    print("\n✓ Build Wave 1 status generation complete")
    sys.exit(0)


if __name__ == "__main__":
    main()
