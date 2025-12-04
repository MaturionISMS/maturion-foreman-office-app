#!/usr/bin/env python3
"""
Maturion Foreman - Multi-Module Build Task Generation Script (Build Wave 1)

This script generates specific build tasks for all modules in Build Wave 1.
It creates skeleton build tasks across all builder agents with proper dependencies
and sequencing.

Usage:
    python3 create-build-tasks-wave-1.py
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class MultiModuleBuildTaskGenerator:
    """Generates skeleton build tasks for all modules in Wave 1"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.build_plan = {}
        self.all_tasks = []
        self.task_counter = 0
        self.errors = []
        self.warnings = []
        
    def load_build_plan(self, plan_file: Optional[Path] = None) -> bool:
        """Load Wave 1 build plan JSON"""
        if not plan_file:
            plan_file = self.repo_root / "build-plan-wave-1.json"
        
        if not plan_file.exists():
            self.errors.append(f"Build Wave 1 plan not found: {plan_file}")
            self.errors.append("Run plan-build-wave-1.py first")
            return False
        
        try:
            with open(plan_file, 'r') as f:
                self.build_plan = json.load(f)
            
            print(f"✓ Loaded Build Wave 1 plan")
            print(f"  Modules: {self.build_plan['module_count']}")
            return True
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in build plan: {e}")
            return False
    
    def generate_task_id(self, module: str, builder: str, phase: int, task_type: str) -> str:
        """Generate unique task ID for Wave 1"""
        self.task_counter += 1
        return f"WAVE1-{module}-{builder.upper()}-P{phase}-T{self.task_counter:04d}-{task_type.upper()}"
    
    def create_skeleton_schema_tasks(self, module: str, phase: Dict, sequence: int) -> List[Dict]:
        """Create skeleton schema tasks"""
        tasks = []
        phase_num = phase['phase']
        
        # Task 1: Schema skeleton
        tasks.append({
            'task_id': self.generate_task_id(module, 'schema', phase_num, 'skeleton'),
            'title': f'{module} - Database Schema Skeleton',
            'module': module,
            'builder': 'schema-builder',
            'phase': phase_num,
            'priority': 'MEDIUM',
            'status': 'NOT_STARTED',
            'build_wave': 1,
            'is_skeleton': True,
            'description': f'Create database schema skeleton for {module} module',
            'acceptance_criteria': [
                'Table definitions created (skeleton)',
                'Basic relationships defined',
                'Placeholder migrations created',
                'Schema follows naming conventions'
            ],
            'dependencies': [],
            'deliverables': [
                'Schema definition files',
                'Migration skeleton',
                'Basic model interfaces'
            ],
            'qa_gates': [
                'Schema structure valid',
                'Follows architecture standards'
            ],
            'estimated_effort': 'SMALL',
            'governance_checks': [
                'Must include organisation_id for multi-tenancy',
                'Must respect privacy guardrails'
            ],
            'notes': [
                'Skeleton only - no full implementation',
                'Establishes structural foundation'
            ]
        })
        
        # Task 2: Model skeletons
        tasks.append({
            'task_id': self.generate_task_id(module, 'schema', phase_num, 'models'),
            'title': f'{module} - Model Definition Skeletons',
            'module': module,
            'builder': 'schema-builder',
            'phase': phase_num,
            'priority': 'MEDIUM',
            'status': 'NOT_STARTED',
            'build_wave': 1,
            'is_skeleton': True,
            'description': 'Create TypeScript model definition skeletons',
            'acceptance_criteria': [
                'Model interfaces defined',
                'Type definitions created',
                'Basic validation placeholders'
            ],
            'dependencies': [tasks[0]['task_id']],
            'deliverables': [
                'TypeScript model files',
                'Type definition files'
            ],
            'qa_gates': [
                'Type checking passes'
            ],
            'estimated_effort': 'SMALL'
        })
        
        return tasks
    
    def create_skeleton_api_tasks(self, module: str, phase: Dict, schema_tasks: List[str]) -> List[Dict]:
        """Create skeleton API tasks"""
        tasks = []
        phase_num = phase['phase']
        
        # Task 1: API skeleton
        tasks.append({
            'task_id': self.generate_task_id(module, 'api', phase_num, 'skeleton'),
            'title': f'{module} - API Route Skeletons',
            'module': module,
            'builder': 'api-builder',
            'phase': phase_num,
            'priority': 'MEDIUM',
            'status': 'NOT_STARTED',
            'build_wave': 1,
            'is_skeleton': True,
            'description': f'Create API route skeletons for {module}',
            'acceptance_criteria': [
                'Route definitions created',
                'Edge function placeholders created',
                'Basic request/response types defined',
                'Authentication placeholders included'
            ],
            'dependencies': schema_tasks,
            'deliverables': [
                'API route files',
                'Edge function skeletons',
                'Type definitions'
            ],
            'qa_gates': [
                'Routes accessible',
                'Type definitions valid'
            ],
            'estimated_effort': 'SMALL',
            'governance_checks': [
                'Respects module boundaries',
                'Includes tenant isolation placeholders'
            ]
        })
        
        # Task 2: Handler placeholders
        tasks.append({
            'task_id': self.generate_task_id(module, 'api', phase_num, 'handlers'),
            'title': f'{module} - Request Handler Placeholders',
            'module': module,
            'builder': 'api-builder',
            'phase': phase_num,
            'priority': 'LOW',
            'status': 'NOT_STARTED',
            'build_wave': 1,
            'is_skeleton': True,
            'description': 'Create request handler placeholder functions',
            'acceptance_criteria': [
                'Handler functions created',
                'Basic error handling included',
                'Placeholder responses defined'
            ],
            'dependencies': [tasks[0]['task_id']],
            'deliverables': [
                'Handler function files',
                'Error handler placeholders'
            ],
            'qa_gates': [
                'Functions callable'
            ],
            'estimated_effort': 'SMALL'
        })
        
        return tasks
    
    def create_skeleton_integration_tasks(self, module: str, phase: Dict, api_tasks: List[str]) -> List[Dict]:
        """Create skeleton integration tasks"""
        tasks = []
        phase_num = phase['phase']
        
        tasks.append({
            'task_id': self.generate_task_id(module, 'integration', phase_num, 'contracts'),
            'title': f'{module} - Integration Contract Definitions',
            'module': module,
            'builder': 'integration-builder',
            'phase': phase_num,
            'priority': 'MEDIUM',
            'status': 'NOT_STARTED',
            'build_wave': 1,
            'is_skeleton': True,
            'description': f'Define integration contracts for {module}',
            'acceptance_criteria': [
                'Integration points identified',
                'Contract interfaces defined',
                'Event definitions created'
            ],
            'dependencies': api_tasks,
            'deliverables': [
                'Integration contract files',
                'Event type definitions',
                'Interface documentation'
            ],
            'qa_gates': [
                'Contracts well-defined',
                'No tight coupling'
            ],
            'estimated_effort': 'SMALL',
            'governance_checks': [
                'Uses event-driven architecture',
                'Respects integration boundaries'
            ]
        })
        
        return tasks
    
    def create_skeleton_ui_tasks(self, module: str, phase: Dict, api_tasks: List[str]) -> List[Dict]:
        """Create skeleton UI tasks"""
        tasks = []
        phase_num = phase['phase']
        
        # Task 1: Component shells
        tasks.append({
            'task_id': self.generate_task_id(module, 'ui', phase_num, 'components'),
            'title': f'{module} - UI Component Shells',
            'module': module,
            'builder': 'ui-builder',
            'phase': phase_num,
            'priority': 'MEDIUM',
            'status': 'NOT_STARTED',
            'build_wave': 1,
            'is_skeleton': True,
            'description': f'Create UI component shells for {module}',
            'acceptance_criteria': [
                'Component files created',
                'Basic structure defined',
                'Props interfaces defined'
            ],
            'dependencies': api_tasks,
            'deliverables': [
                'React component files',
                'Component type definitions',
                'Placeholder layouts'
            ],
            'qa_gates': [
                'Components render',
                'No console errors'
            ],
            'estimated_effort': 'SMALL',
            'governance_checks': [
                'No business logic in UI',
                'Uses API calls for data'
            ]
        })
        
        # Task 2: Routing
        tasks.append({
            'task_id': self.generate_task_id(module, 'ui', phase_num, 'routing'),
            'title': f'{module} - Route Definitions',
            'module': module,
            'builder': 'ui-builder',
            'phase': phase_num,
            'priority': 'LOW',
            'status': 'NOT_STARTED',
            'build_wave': 1,
            'is_skeleton': True,
            'description': 'Define module routes',
            'acceptance_criteria': [
                'Routes defined',
                'Navigation structure created',
                'Route guards placeholders added'
            ],
            'dependencies': [tasks[0]['task_id']],
            'deliverables': [
                'Route configuration files',
                'Navigation components'
            ],
            'qa_gates': [
                'Routes accessible'
            ],
            'estimated_effort': 'SMALL'
        })
        
        return tasks
    
    def create_skeleton_qa_tasks(self, module: str, phase: Dict, all_prev_tasks: List[str]) -> List[Dict]:
        """Create skeleton QA tasks"""
        tasks = []
        phase_num = phase['phase']
        
        tasks.append({
            'task_id': self.generate_task_id(module, 'qa', phase_num, 'structure'),
            'title': f'{module} - QA Test Structure',
            'module': module,
            'builder': 'qa-builder',
            'phase': phase_num,
            'priority': 'MEDIUM',
            'status': 'NOT_STARTED',
            'build_wave': 1,
            'is_skeleton': True,
            'description': f'Create QA test structure for {module}',
            'acceptance_criteria': [
                'Test directory structure created',
                'Test file placeholders created',
                'QA documentation templates added'
            ],
            'dependencies': all_prev_tasks,
            'deliverables': [
                'Test directory structure',
                'Test file templates',
                'QA documentation'
            ],
            'qa_gates': [
                'Structure follows standards',
                'All areas covered'
            ],
            'estimated_effort': 'SMALL',
            'governance_checks': [
                'QA follows QA governance rules'
            ]
        })
        
        return tasks
    
    def generate_module_tasks(self, module_name: str, module_plan: Dict) -> List[Dict]:
        """Generate all skeleton tasks for a module"""
        module_tasks = []
        
        schema_task_ids = []
        api_task_ids = []
        integration_task_ids = []
        ui_task_ids = []
        
        for phase in module_plan['phases']:
            builder = phase['builder']
            
            if builder == 'schema-builder':
                tasks = self.create_skeleton_schema_tasks(module_name, phase, module_plan['sequence_number'])
                schema_task_ids = [t['task_id'] for t in tasks]
                module_tasks.extend(tasks)
                
            elif builder == 'api-builder':
                tasks = self.create_skeleton_api_tasks(module_name, phase, schema_task_ids)
                api_task_ids = [t['task_id'] for t in tasks]
                module_tasks.extend(tasks)
                
            elif builder == 'integration-builder':
                tasks = self.create_skeleton_integration_tasks(module_name, phase, api_task_ids)
                integration_task_ids = [t['task_id'] for t in tasks]
                module_tasks.extend(tasks)
                
            elif builder == 'ui-builder':
                tasks = self.create_skeleton_ui_tasks(module_name, phase, api_task_ids)
                ui_task_ids = [t['task_id'] for t in tasks]
                module_tasks.extend(tasks)
                
            elif builder == 'qa-builder':
                prev_tasks = schema_task_ids + api_task_ids + integration_task_ids + ui_task_ids
                tasks = self.create_skeleton_qa_tasks(module_name, phase, prev_tasks)
                module_tasks.extend(tasks)
        
        return module_tasks
    
    def generate_all_tasks(self) -> bool:
        """Generate tasks for all modules"""
        if not self.build_plan:
            self.errors.append("No build plan loaded")
            return False
        
        print(f"\n📝 Generating tasks for {self.build_plan['module_count']} modules...")
        
        build_sequence = self.build_plan.get('build_sequence', [])
        module_plans = self.build_plan.get('module_plans', {})
        
        for module_name in build_sequence:
            if module_name in module_plans:
                module_plan = module_plans[module_name]
                tasks = self.generate_module_tasks(module_name, module_plan)
                self.all_tasks.extend(tasks)
                print(f"  ✓ {module_name}: {len(tasks)} tasks generated")
        
        return True
    
    def save_tasks(self, output_file: Optional[Path] = None) -> bool:
        """Save tasks to JSON file"""
        if not output_file:
            output_file = self.repo_root / "build-tasks-wave-1.json"
        
        # Group tasks by module and builder
        tasks_by_module = {}
        tasks_by_builder = {}
        
        for task in self.all_tasks:
            module = task['module']
            builder = task['builder']
            
            if module not in tasks_by_module:
                tasks_by_module[module] = 0
            tasks_by_module[module] += 1
            
            if builder not in tasks_by_builder:
                tasks_by_builder[builder] = 0
            tasks_by_builder[builder] += 1
        
        task_data = {
            'version': '1.0',
            'generated': datetime.now().isoformat(),
            'build_wave': 1,
            'purpose': 'Multi-Module Architecture Skeleton Build Tasks',
            'total_tasks': len(self.all_tasks),
            'total_modules': self.build_plan['module_count'],
            'tasks_by_module': tasks_by_module,
            'tasks_by_builder': tasks_by_builder,
            'build_sequence': self.build_plan.get('build_sequence', []),
            'tasks': self.all_tasks,
            'notes': [
                'Build Wave 1 - Skeleton build tasks',
                'All tasks are skeleton/placeholder builds',
                'No full implementation - structural foundation only',
                'Tasks respect module dependencies and sequencing',
                'All governance boundaries enforced'
            ]
        }
        
        try:
            with open(output_file, 'w') as f:
                json.dump(task_data, f, indent=2)
            print(f"\n✓ Build Wave 1 tasks saved to: {output_file}")
            return True
        except Exception as e:
            self.errors.append(f"Failed to save tasks: {e}")
            return False
    
    def print_summary(self):
        """Print task generation summary"""
        print("\n" + "=" * 80)
        print("BUILD WAVE 1 - TASK GENERATION SUMMARY")
        print("=" * 80)
        
        print(f"\nTotal Tasks Generated: {len(self.all_tasks)}")
        
        # Group by module
        by_module = {}
        for task in self.all_tasks:
            module = task['module']
            if module not in by_module:
                by_module[module] = []
            by_module[module].append(task)
        
        print(f"\nTasks by Module ({len(by_module)} modules):")
        for module in sorted(by_module.keys()):
            print(f"  {module}: {len(by_module[module])} tasks")
        
        # Group by builder
        by_builder = {}
        for task in self.all_tasks:
            builder = task['builder']
            if builder not in by_builder:
                by_builder[builder] = []
            by_builder[builder].append(task)
        
        print(f"\nTasks by Builder ({len(by_builder)} builders):")
        for builder in sorted(by_builder.keys()):
            print(f"  {builder}: {len(by_builder[builder])} tasks")
        
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
    
    print(f"\n🔨 Maturion Foreman - Build Wave 1 Task Generation")
    print(f"Repository: {repo_root}\n")
    
    generator = MultiModuleBuildTaskGenerator(repo_root)
    
    # Load build plan
    if not generator.load_build_plan():
        print("\n✗ Task generation failed:")
        for error in generator.errors:
            print(f"  - {error}")
        sys.exit(1)
    
    # Generate tasks
    if not generator.generate_all_tasks():
        print("\n✗ Task generation failed:")
        for error in generator.errors:
            print(f"  - {error}")
        sys.exit(1)
    
    # Save and summarize
    generator.save_tasks()
    generator.print_summary()
    
    print("\n✓ Build Wave 1 task generation complete")
    sys.exit(0)


if __name__ == "__main__":
    main()
