#!/usr/bin/env python3
"""
Maturion Foreman - Build Task Generation Script (Phase 6 - Build Orchestration)

This script generates specific build tasks for each builder agent based on
the build plan. It creates actionable tasks with dependencies, acceptance
criteria, and QA gates.

Usage:
    python3 create-build-tasks.py
    python3 create-build-tasks.py --plan build-plan.json
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import argparse


class BuildTaskGenerator:
    """Generates build tasks for builder agents"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.build_plan = {}
        self.module_name = None
        self.tasks = []
        self.task_counter = 0
        self.errors = []
        self.warnings = []
        
    def load_build_plan(self, plan_file: Optional[Path] = None) -> bool:
        """Load build plan JSON"""
        if not plan_file:
            plan_file = self.repo_root / "build-plan.json"
        
        if not plan_file.exists():
            self.errors.append(f"Build plan not found: {plan_file}")
            self.errors.append("Run plan-build.py first to generate a build plan")
            return False
        
        try:
            with open(plan_file, 'r') as f:
                self.build_plan = json.load(f)
            
            self.module_name = self.build_plan.get('module', 'UNKNOWN')
            print(f"✓ Loaded build plan for {self.module_name}")
            return True
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in build plan: {e}")
            return False
    
    def generate_task_id(self, builder: str, phase: int, task_type: str) -> str:
        """Generate unique task ID"""
        self.task_counter += 1
        return f"{self.module_name}-{builder.upper()}-P{phase}-T{self.task_counter:03d}-{task_type.upper()}"
    
    def create_schema_tasks(self, phase: Dict) -> List[Dict]:
        """Create tasks for schema-builder"""
        tasks = []
        phase_num = phase['phase']
        
        # Task 1: Design and implement database schema
        tasks.append({
            'task_id': self.generate_task_id('schema-builder', phase_num, 'schema'),
            'title': f'{self.module_name} - Database Schema Design and Implementation',
            'builder': 'schema-builder',
            'phase': phase_num,
            'priority': 'HIGH',
            'status': 'NOT_STARTED',
            'description': f'Design and implement the complete database schema for {self.module_name} module',
            'acceptance_criteria': [
                'All tables and relationships defined',
                'Schema follows naming conventions',
                'Foreign keys and constraints properly defined',
                'Schema documentation complete',
                'Schema passes validation tests'
            ],
            'dependencies': [],
            'deliverables': [
                'Database schema DDL',
                'Schema diagram',
                'Migration scripts',
                'Schema documentation'
            ],
            'qa_gates': [
                'Schema validation passes',
                'No circular dependencies',
                'Follows architecture standards',
                'QA-of-QA review complete'
            ],
            'estimated_effort': 'MEDIUM',
            'governance_checks': [
                'Must not access other module schemas directly',
                'Must respect privacy guardrails',
                'Must include organisation_id for multi-tenancy'
            ]
        })
        
        # Task 2: Create model definitions
        tasks.append({
            'task_id': self.generate_task_id('schema-builder', phase_num, 'models'),
            'title': f'{self.module_name} - Model Definitions',
            'builder': 'schema-builder',
            'phase': phase_num,
            'priority': 'HIGH',
            'status': 'NOT_STARTED',
            'description': 'Create TypeScript model definitions for all database entities',
            'acceptance_criteria': [
                'All models match schema',
                'Type safety enforced',
                'Models include validation logic',
                'Models documented'
            ],
            'dependencies': [tasks[0]['task_id']],
            'deliverables': [
                'TypeScript model files',
                'Validation logic',
                'Model tests'
            ],
            'qa_gates': [
                'Type checking passes',
                'Models align with schema',
                'Validation tests pass'
            ],
            'estimated_effort': 'MEDIUM'
        })
        
        # Task 3: Schema validation tests
        tasks.append({
            'task_id': self.generate_task_id('schema-builder', phase_num, 'tests'),
            'title': f'{self.module_name} - Schema Validation Tests',
            'builder': 'schema-builder',
            'phase': phase_num,
            'priority': 'MEDIUM',
            'status': 'NOT_STARTED',
            'description': 'Create comprehensive tests for schema validation',
            'acceptance_criteria': [
                'All constraints tested',
                'Migration tests included',
                'Edge cases covered',
                'Test coverage >= 80%'
            ],
            'dependencies': [tasks[1]['task_id']],
            'deliverables': [
                'Schema test suite',
                'Migration tests',
                'Test coverage report'
            ],
            'qa_gates': [
                'All tests pass',
                'Coverage threshold met'
            ],
            'estimated_effort': 'MEDIUM'
        })
        
        return tasks
    
    def create_api_tasks(self, phase: Dict, schema_tasks: List[Dict]) -> List[Dict]:
        """Create tasks for api-builder"""
        tasks = []
        phase_num = phase['phase']
        
        # Get schema completion dependency
        schema_task_ids = [t['task_id'] for t in schema_tasks]
        
        # Task 1: Edge functions implementation
        tasks.append({
            'task_id': self.generate_task_id('api-builder', phase_num, 'edge'),
            'title': f'{self.module_name} - Edge Functions Implementation',
            'builder': 'api-builder',
            'phase': phase_num,
            'priority': 'HIGH',
            'status': 'NOT_STARTED',
            'description': f'Implement all edge functions for {self.module_name} API',
            'acceptance_criteria': [
                'All CRUD operations implemented',
                'Authentication and authorization included',
                'Input validation implemented',
                'Error handling complete',
                'API follows REST conventions'
            ],
            'dependencies': schema_task_ids,
            'deliverables': [
                'Edge function implementations',
                'API route definitions',
                'Request/response schemas',
                'API documentation'
            ],
            'qa_gates': [
                'All API endpoints functional',
                'Authentication tests pass',
                'Input validation works',
                'Error handling validated'
            ],
            'estimated_effort': 'HIGH',
            'governance_checks': [
                'No direct database access outside models',
                'Respects module boundaries',
                'Includes tenant isolation'
            ]
        })
        
        # Task 2: Business logic implementation
        tasks.append({
            'task_id': self.generate_task_id('api-builder', phase_num, 'logic'),
            'title': f'{self.module_name} - Business Logic Implementation',
            'builder': 'api-builder',
            'phase': phase_num,
            'priority': 'HIGH',
            'status': 'NOT_STARTED',
            'description': 'Implement core business logic and workflows',
            'acceptance_criteria': [
                'All workflows implemented',
                'State transitions validated',
                'Business rules enforced',
                'Logic properly tested'
            ],
            'dependencies': [tasks[0]['task_id']],
            'deliverables': [
                'Business logic modules',
                'Workflow implementations',
                'State management',
                'Logic tests'
            ],
            'qa_gates': [
                'Business rules validated',
                'Workflow tests pass',
                'State transitions correct'
            ],
            'estimated_effort': 'HIGH'
        })
        
        # Task 3: API tests
        tasks.append({
            'task_id': self.generate_task_id('api-builder', phase_num, 'tests'),
            'title': f'{self.module_name} - API Test Suite',
            'builder': 'api-builder',
            'phase': phase_num,
            'priority': 'MEDIUM',
            'status': 'NOT_STARTED',
            'description': 'Create comprehensive API test suite',
            'acceptance_criteria': [
                'All endpoints tested',
                'Error scenarios covered',
                'Authentication tests included',
                'Test coverage >= 80%'
            ],
            'dependencies': [tasks[1]['task_id']],
            'deliverables': [
                'API test suite',
                'Integration tests',
                'Coverage report'
            ],
            'qa_gates': [
                'All tests pass',
                'Coverage threshold met'
            ],
            'estimated_effort': 'MEDIUM'
        })
        
        return tasks
    
    def create_integration_tasks(self, phase: Dict, api_tasks: List[Dict]) -> List[Dict]:
        """Create tasks for integration-builder"""
        tasks = []
        phase_num = phase['phase']
        
        api_task_ids = [t['task_id'] for t in api_tasks]
        
        # Task 1: Inter-module integration
        tasks.append({
            'task_id': self.generate_task_id('integration-builder', phase_num, 'inter'),
            'title': f'{self.module_name} - Inter-Module Integration',
            'builder': 'integration-builder',
            'phase': phase_num,
            'priority': 'HIGH',
            'status': 'NOT_STARTED',
            'description': f'Implement integrations between {self.module_name} and other ISMS modules',
            'acceptance_criteria': [
                'All integration points identified',
                'Integration contracts defined',
                'Event handlers implemented',
                'Integration documented'
            ],
            'dependencies': api_task_ids,
            'deliverables': [
                'Integration implementation',
                'Event handlers',
                'Integration contracts',
                'Integration documentation'
            ],
            'qa_gates': [
                'Integration tests pass',
                'No tight coupling detected',
                'Events properly handled'
            ],
            'estimated_effort': 'MEDIUM',
            'governance_checks': [
                'No direct module-to-module calls',
                'Uses event-driven architecture',
                'Respects integration boundaries'
            ]
        })
        
        # Task 2: Integration tests
        tasks.append({
            'task_id': self.generate_task_id('integration-builder', phase_num, 'tests'),
            'title': f'{self.module_name} - Integration Test Suite',
            'builder': 'integration-builder',
            'phase': phase_num,
            'priority': 'MEDIUM',
            'status': 'NOT_STARTED',
            'description': 'Create integration test suite',
            'acceptance_criteria': [
                'All integrations tested',
                'Event flows validated',
                'Error handling tested',
                'Coverage >= 80%'
            ],
            'dependencies': [tasks[0]['task_id']],
            'deliverables': [
                'Integration test suite',
                'Event flow tests',
                'Coverage report'
            ],
            'qa_gates': [
                'All tests pass',
                'Integration contracts validated'
            ],
            'estimated_effort': 'MEDIUM'
        })
        
        return tasks
    
    def create_ui_tasks(self, phase: Dict, api_tasks: List[Dict]) -> List[Dict]:
        """Create tasks for ui-builder"""
        tasks = []
        phase_num = phase['phase']
        
        api_task_ids = [t['task_id'] for t in api_tasks]
        
        # Task 1: UI components
        tasks.append({
            'task_id': self.generate_task_id('ui-builder', phase_num, 'components'),
            'title': f'{self.module_name} - UI Components Implementation',
            'builder': 'ui-builder',
            'phase': phase_num,
            'priority': 'HIGH',
            'status': 'NOT_STARTED',
            'description': f'Implement all UI components for {self.module_name}',
            'acceptance_criteria': [
                'All components match wireframes',
                'Components are responsive',
                'Accessibility standards met',
                'Components properly tested'
            ],
            'dependencies': api_task_ids,
            'deliverables': [
                'React components',
                'Component styles',
                'Component tests',
                'Storybook stories'
            ],
            'qa_gates': [
                'Components render correctly',
                'Accessibility tests pass',
                'Component tests pass'
            ],
            'estimated_effort': 'HIGH',
            'governance_checks': [
                'No business logic in UI',
                'Uses API calls for data',
                'Follows UI component standards'
            ]
        })
        
        # Task 2: Page layouts
        tasks.append({
            'task_id': self.generate_task_id('ui-builder', phase_num, 'layouts'),
            'title': f'{self.module_name} - Page Layouts',
            'builder': 'ui-builder',
            'phase': phase_num,
            'priority': 'MEDIUM',
            'status': 'NOT_STARTED',
            'description': 'Implement page layouts and navigation',
            'acceptance_criteria': [
                'All pages implemented',
                'Navigation working',
                'Layouts responsive',
                'UX validated'
            ],
            'dependencies': [tasks[0]['task_id']],
            'deliverables': [
                'Page layouts',
                'Navigation components',
                'Route definitions'
            ],
            'qa_gates': [
                'Navigation works correctly',
                'Layouts match design',
                'Responsive tests pass'
            ],
            'estimated_effort': 'MEDIUM'
        })
        
        # Task 3: UI tests
        tasks.append({
            'task_id': self.generate_task_id('ui-builder', phase_num, 'tests'),
            'title': f'{self.module_name} - UI Test Suite',
            'builder': 'ui-builder',
            'phase': phase_num,
            'priority': 'MEDIUM',
            'status': 'NOT_STARTED',
            'description': 'Create UI test suite',
            'acceptance_criteria': [
                'Component tests complete',
                'E2E tests included',
                'Visual regression tests',
                'Coverage >= 70%'
            ],
            'dependencies': [tasks[1]['task_id']],
            'deliverables': [
                'Component test suite',
                'E2E tests',
                'Visual tests',
                'Coverage report'
            ],
            'qa_gates': [
                'All tests pass',
                'Visual regression clean'
            ],
            'estimated_effort': 'MEDIUM'
        })
        
        return tasks
    
    def create_qa_tasks(self, phase: Dict, all_prev_tasks: List[Dict]) -> List[Dict]:
        """Create tasks for qa-builder"""
        tasks = []
        phase_num = phase['phase']
        
        prev_task_ids = [t['task_id'] for t in all_prev_tasks]
        
        # Task 1: End-to-end tests
        tasks.append({
            'task_id': self.generate_task_id('qa-builder', phase_num, 'e2e'),
            'title': f'{self.module_name} - End-to-End Test Suite',
            'builder': 'qa-builder',
            'phase': phase_num,
            'priority': 'HIGH',
            'status': 'NOT_STARTED',
            'description': f'Create comprehensive E2E test suite for {self.module_name}',
            'acceptance_criteria': [
                'All user journeys tested',
                'Integration flows validated',
                'Error scenarios covered',
                'Performance benchmarks met'
            ],
            'dependencies': prev_task_ids,
            'deliverables': [
                'E2E test suite',
                'Performance tests',
                'Load tests',
                'Test report'
            ],
            'qa_gates': [
                'All E2E tests pass',
                'Performance acceptable',
                'No critical bugs'
            ],
            'estimated_effort': 'HIGH'
        })
        
        # Task 2: QA-of-QA validation
        tasks.append({
            'task_id': self.generate_task_id('qa-builder', phase_num, 'qa-of-qa'),
            'title': f'{self.module_name} - QA-of-QA Validation',
            'builder': 'qa-builder',
            'phase': phase_num,
            'priority': 'HIGH',
            'status': 'NOT_STARTED',
            'description': 'Validate completeness and quality of all QA artifacts',
            'acceptance_criteria': [
                'All QA plans executed',
                'Test coverage validated',
                'QA gaps identified',
                'QA-of-QA report complete'
            ],
            'dependencies': [tasks[0]['task_id']],
            'deliverables': [
                'QA-of-QA report',
                'Coverage analysis',
                'Gap analysis',
                'Recommendations'
            ],
            'qa_gates': [
                'QA coverage >= 80%',
                'No critical gaps',
                'All QA checklists complete'
            ],
            'estimated_effort': 'MEDIUM',
            'governance_checks': [
                'QA follows QA governance rules',
                'QA-of-QA checklist completed',
                'Architecture alignment validated'
            ]
        })
        
        # Task 3: Compliance validation
        tasks.append({
            'task_id': self.generate_task_id('qa-builder', phase_num, 'compliance'),
            'title': f'{self.module_name} - Compliance Validation',
            'builder': 'qa-builder',
            'phase': phase_num,
            'priority': 'HIGH',
            'status': 'NOT_STARTED',
            'description': 'Validate compliance with all relevant standards',
            'acceptance_criteria': [
                'All compliance controls validated',
                'Security requirements met',
                'Privacy requirements met',
                'Compliance report complete'
            ],
            'dependencies': [tasks[1]['task_id']],
            'deliverables': [
                'Compliance validation report',
                'Security audit',
                'Privacy audit',
                'Recommendations'
            ],
            'qa_gates': [
                'No compliance violations',
                'Security tests pass',
                'Privacy guardrails validated'
            ],
            'estimated_effort': 'MEDIUM'
        })
        
        return tasks
    
    def generate_tasks(self) -> bool:
        """Generate all build tasks from build plan"""
        if not self.build_plan:
            self.errors.append("No build plan loaded")
            return False
        
        phases = self.build_plan.get('build_phases', [])
        if not phases:
            self.errors.append("No build phases found in plan")
            return False
        
        all_tasks = []
        schema_tasks = []
        api_tasks = []
        integration_tasks = []
        ui_tasks = []
        qa_tasks = []
        
        # Generate tasks for each phase
        for phase in phases:
            builder = phase.get('builder', '')
            
            if builder == 'schema-builder':
                schema_tasks = self.create_schema_tasks(phase)
                all_tasks.extend(schema_tasks)
                
            elif builder == 'api-builder':
                api_tasks = self.create_api_tasks(phase, schema_tasks)
                all_tasks.extend(api_tasks)
                
            elif builder == 'integration-builder':
                integration_tasks = self.create_integration_tasks(phase, api_tasks)
                all_tasks.extend(integration_tasks)
                
            elif builder == 'ui-builder':
                ui_tasks = self.create_ui_tasks(phase, api_tasks)
                all_tasks.extend(ui_tasks)
                
            elif builder == 'qa-builder':
                prev_tasks = schema_tasks + api_tasks + integration_tasks + ui_tasks
                qa_tasks = self.create_qa_tasks(phase, prev_tasks)
                all_tasks.extend(qa_tasks)
        
        self.tasks = all_tasks
        return True
    
    def save_tasks(self, output_file: Optional[Path] = None) -> bool:
        """Save tasks to JSON file"""
        if not output_file:
            output_file = self.repo_root / "build-tasks.json"
        
        # Load governance evidence for lineage
        governance_evidence = self._load_governance_evidence()
        
        task_data = {
            'version': '1.0',
            'generated': datetime.now().isoformat(),
            'module': self.module_name,
            'build_wave': 0,
            'total_tasks': len(self.tasks),
            'governance_lineage': governance_evidence,  # Add governance lineage
            'tasks_by_builder': {
                'schema-builder': len([t for t in self.tasks if t['builder'] == 'schema-builder']),
                'api-builder': len([t for t in self.tasks if t['builder'] == 'api-builder']),
                'integration-builder': len([t for t in self.tasks if t['builder'] == 'integration-builder']),
                'ui-builder': len([t for t in self.tasks if t['builder'] == 'ui-builder']),
                'qa-builder': len([t for t in self.tasks if t['builder'] == 'qa-builder'])
            },
            'tasks': self.tasks,
            'notes': [
                'This is Build Wave 0 - tasks are for orchestration validation',
                'Tasks follow builder capability boundaries',
                'All tasks include QA gates and acceptance criteria',
                'Dependencies ensure proper sequencing',
                'Governance lineage tracked for audit trail'
            ]
        }
        
        try:
            with open(output_file, 'w') as f:
                json.dump(task_data, f, indent=2)
            print(f"✓ Build tasks written: {output_file}")
            return True
        except Exception as e:
            self.errors.append(f"Failed to save tasks: {e}")
            return False
    
    def _load_governance_evidence(self) -> Dict:
        """Load governance evidence for lineage tracking"""
        evidence = {
            'app_description': None,
            'frs_reference': None,
            'architecture_compilation': None,
            'build_authorization_gate': None
        }
        
        # Check for App Description
        app_desc_paths = [
            self.repo_root / "docs" / "governance" / "FM_APP_DESCRIPTION.md",
            self.repo_root / "APP_DESCRIPTION.md"
        ]
        for path in app_desc_paths:
            if path.exists():
                evidence['app_description'] = {
                    'path': str(path),
                    'exists': True
                }
                break
        
        # Check for FRS/True North
        frs_path = self.repo_root / "foreman" / "architecture" / "FOREMAN_TRUE_NORTH_v1.0.md"
        if frs_path.exists():
            evidence['frs_reference'] = {
                'path': str(frs_path),
                'exists': True
            }
        
        # Check for latest governance gate evidence
        evidence_dir = self.repo_root / "governance" / "evidence"
        if evidence_dir.exists():
            # Find latest build-gate evidence
            gate_files = sorted(evidence_dir.glob("build-gate-*.json"), reverse=True)
            if gate_files:
                evidence['build_authorization_gate'] = {
                    'evidence_file': str(gate_files[0]),
                    'timestamp': gate_files[0].stat().st_mtime
                }
            
            # Find latest arch-compile evidence
            arch_files = sorted(evidence_dir.glob("arch-compile-*.json"), reverse=True)
            if arch_files:
                evidence['architecture_compilation'] = {
                    'evidence_file': str(arch_files[0]),
                    'timestamp': arch_files[0].stat().st_mtime
                }
        
        return evidence
            print(f"✓ Build tasks saved to: {output_file}")
            return True
        except Exception as e:
            self.errors.append(f"Failed to save tasks: {e}")
            return False
    
    def print_summary(self):
        """Print task generation summary"""
        print("\n" + "=" * 80)
        print(f"BUILD TASKS SUMMARY - {self.module_name}")
        print("=" * 80)
        
        print(f"\nTotal Tasks Generated: {len(self.tasks)}")
        
        # Group by builder
        by_builder = {}
        for task in self.tasks:
            builder = task['builder']
            if builder not in by_builder:
                by_builder[builder] = []
            by_builder[builder].append(task)
        
        print("\nTasks by Builder:")
        for builder, tasks in sorted(by_builder.items()):
            print(f"  {builder}: {len(tasks)} tasks")
        
        # Group by phase
        by_phase = {}
        for task in self.tasks:
            phase = task['phase']
            if phase not in by_phase:
                by_phase[phase] = []
            by_phase[phase].append(task)
        
        print("\nTasks by Phase:")
        for phase in sorted(by_phase.keys()):
            print(f"  Phase {phase}: {len(by_phase[phase])} tasks")
            for task in by_phase[phase]:
                print(f"    - {task['task_id']}: {task['title']}")
        
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
    parser = argparse.ArgumentParser(description='Generate build tasks from build plan')
    parser.add_argument('--plan', type=str, help='Path to build plan JSON file')
    args = parser.parse_args()
    
    # Find repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir
    
    print(f"\n🔨 Maturion Foreman - Build Task Generation")
    print(f"Repository: {repo_root}\n")
    
    generator = BuildTaskGenerator(repo_root)
    
    # Load build plan
    plan_file = Path(args.plan) if args.plan else None
    if not generator.load_build_plan(plan_file):
        print("\n✗ Task generation failed:")
        for error in generator.errors:
            print(f"  - {error}")
        sys.exit(1)
    
    # Generate tasks
    if not generator.generate_tasks():
        print("\n✗ Task generation failed:")
        for error in generator.errors:
            print(f"  - {error}")
        sys.exit(1)
    
    # Save and summarize
    generator.save_tasks()
    generator.print_summary()
    
    print("\n✓ Build task generation complete")
    sys.exit(0)


if __name__ == "__main__":
    main()
