#!/usr/bin/env python3
"""
Maturion AI Foreman - Repository Validation Script
Performs comprehensive validation of repository structure, governance, and specifications
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Set
import re

class RepositoryValidator:
    """Validates the Maturion AI Foreman repository structure and specifications"""
    
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.validation_results = {
            'folder_structure': [],
            'specification_files': [],
            'governance_completeness': [],
            'qa_specs': [],
            'compliance': [],
            'innovation_survey_admin': [],
            'builder_specs': [],
            'json_integrity': [],
            'warnings': [],
            'errors': [],
            'recommendations': []
        }
        
    def validate_all(self) -> Dict:
        """Run all validation checks"""
        print("🔍 Starting Maturion AI Foreman Repository Validation...\n")
        
        self.validate_folder_structure()
        self.validate_specification_files()
        self.validate_governance_completeness()
        self.validate_qa_specs()
        self.validate_compliance()
        self.validate_innovation_survey_admin()
        self.validate_builder_specs()
        self.validate_json_files()
        
        return self.validation_results
    
    def validate_folder_structure(self):
        """Validate foreman folder structure"""
        print("📁 Validating Folder Structure...")
        
        required_dirs = [
            'foreman',
            'foreman/admin',
            'foreman/builder',
            'foreman/compliance',
            'foreman/innovation',
            'foreman/platform',
            'foreman/survey'
        ]
        
        for dir_path in required_dirs:
            full_path = self.repo_root / dir_path
            if full_path.exists() and full_path.is_dir():
                self.validation_results['folder_structure'].append({
                    'path': dir_path,
                    'status': 'PASS',
                    'message': 'Directory exists'
                })
            else:
                self.validation_results['folder_structure'].append({
                    'path': dir_path,
                    'status': 'FAIL',
                    'message': 'Directory missing'
                })
                self.validation_results['errors'].append(f"Missing directory: {dir_path}")
        
        print(f"  ✓ Checked {len(required_dirs)} required directories\n")
    
    def validate_specification_files(self):
        """Validate Phase 1-5 specification files for each module"""
        print("📋 Validating Specification Files (Phase 1-5)...")
        
        modules = [
            'COURSE_CRAFTER',
            'ERM',
            'PIT',
            'THREAT',
            'VULNERABILITY',
            'RISK_ASSESSMENT',
            'WRAC'
        ]
        
        # Phase 1: True North
        phase1_specs = ['TRUE_NORTH']
        
        # Phase 2: Architecture & Data
        phase2_specs = ['DATABASE_SCHEMA', 'FRONTEND_COMPONENT_MAP', 'WIREFRAMES']
        
        # Phase 3: Backend & Integration
        phase3_specs = ['EDGE_FUNCTIONS', 'INTEGRATION_MAP', 'EXPORT_SPEC']
        
        # Phase 4: QA & Implementation
        phase4_specs = ['QA_IMPLEMENTATION_PLAN', 'IMPLEMENTATION_GUIDE', 'SPRINT_PLAN']
        
        # Phase 5: Advanced Features
        phase5_specs = ['CHANGELOG', 'WATCHDOG_LOGIC', 'MODEL_ROUTING_SPEC']
        
        all_phases = {
            'Phase 1 (True North)': phase1_specs,
            'Phase 2 (Architecture & Data)': phase2_specs,
            'Phase 3 (Backend & Integration)': phase3_specs,
            'Phase 4 (QA & Implementation)': phase4_specs,
            'Phase 5 (Advanced Features)': phase5_specs
        }
        
        for module in modules:
            module_results = {'module': module, 'phases': {}}
            
            for phase_name, specs in all_phases.items():
                phase_results = []
                for spec in specs:
                    # Find files matching pattern MODULE_SPEC_v*.md
                    pattern = f"{module}_{spec}_v*.md"
                    matching_files = list(self.repo_root.glob(pattern))
                    
                    if matching_files:
                        # Get latest version
                        latest_file = max(matching_files, key=lambda p: p.name)
                        phase_results.append({
                            'spec': spec,
                            'status': 'PASS',
                            'file': latest_file.name
                        })
                    else:
                        # Check if this is required or optional
                        is_optional = (
                            (spec in ['WATCHDOG_LOGIC', 'MODEL_ROUTING_SPEC'] and module not in ['PIT', 'THREAT', 'VULNERABILITY']) or
                            (spec == 'INTEGRATION_MAP' and module in ['COURSE_CRAFTER', 'WRAC', 'RISK_ASSESSMENT']) or
                            (spec == 'EXPORT_SPEC' and module in ['RISK_ASSESSMENT', 'WRAC'])
                        )
                        
                        phase_results.append({
                            'spec': spec,
                            'status': 'OPTIONAL' if is_optional else 'MISSING',
                            'file': None
                        })
                        
                        if not is_optional:
                            self.validation_results['warnings'].append(
                                f"{module}: Missing {spec} specification"
                            )
                
                module_results['phases'][phase_name] = phase_results
            
            self.validation_results['specification_files'].append(module_results)
        
        print(f"  ✓ Validated specifications for {len(modules)} modules\n")
    
    def validate_governance_completeness(self):
        """Validate governance files completeness"""
        print("⚖️  Validating Governance Completeness...")
        
        required_governance_files = [
            'foreman/identity.md',
            'foreman/command-grammar.md',
            'foreman/roles-and-duties.md',
            'foreman/architecture-folder-structure.md',
            'foreman/architecture-governance.md',
            'foreman/architecture-naming-conventions.md',
            'foreman/architecture-standardisation-policy.md',
            'foreman/architecture-validation-checklist.md',
            'foreman/task-distribution-rules.md',
            'foreman/versioning-rules.md',
            'foreman/context-awareness.md',
            'foreman/memory-model.md',
            'foreman/platform-awareness.md',
            'foreman/privacy-guardrails.md',
            'foreman/system-map.md',
            'foreman/runtime-agent-plan.md',
            'foreman/minimum-architecture-template.md',
            'foreman/module-readiness-report-template.md'
        ]
        
        for file_path in required_governance_files:
            full_path = self.repo_root / file_path
            if full_path.exists() and full_path.is_file():
                # Check if file has content
                size = full_path.stat().st_size
                self.validation_results['governance_completeness'].append({
                    'file': file_path,
                    'status': 'PASS' if size > 0 else 'EMPTY',
                    'size': size
                })
                if size == 0:
                    self.validation_results['warnings'].append(f"Empty governance file: {file_path}")
            else:
                self.validation_results['governance_completeness'].append({
                    'file': file_path,
                    'status': 'MISSING',
                    'size': 0
                })
                self.validation_results['errors'].append(f"Missing governance file: {file_path}")
        
        print(f"  ✓ Checked {len(required_governance_files)} governance files\n")
    
    def validate_qa_specs(self):
        """Validate QA and QA-of-QA specifications"""
        print("✅ Validating QA and QA-of-QA Specifications...")
        
        qa_files = [
            'foreman/qa-governance.md',
            'foreman/qa-minimum-coverage-requirements.md',
            'foreman/qa-of-qa.md',
            'foreman/qa-of-qa-validation-checklist.md'
        ]
        
        for file_path in qa_files:
            full_path = self.repo_root / file_path
            if full_path.exists() and full_path.is_file():
                size = full_path.stat().st_size
                self.validation_results['qa_specs'].append({
                    'file': file_path,
                    'status': 'PASS' if size > 0 else 'EMPTY',
                    'size': size
                })
                if size == 0:
                    self.validation_results['warnings'].append(f"Empty QA file: {file_path}")
            else:
                self.validation_results['qa_specs'].append({
                    'file': file_path,
                    'status': 'MISSING',
                    'size': 0
                })
                self.validation_results['errors'].append(f"Missing QA file: {file_path}")
        
        print(f"  ✓ Checked {len(qa_files)} QA specification files\n")
    
    def validate_compliance(self):
        """Validate compliance reference map and control library"""
        print("📜 Validating Compliance Reference Map and Control Library...")
        
        compliance_files = [
            ('foreman/compliance/compliance-reference-map.md', 'markdown'),
            ('foreman/compliance/compliance-control-library.json', 'json'),
            ('foreman/compliance/compliance-dashboard-spec.md', 'markdown'),
            ('foreman/compliance/compliance-qa-spec.md', 'markdown'),
            ('foreman/compliance/compliance-watchdog-spec.md', 'markdown')
        ]
        
        for file_path, file_type in compliance_files:
            full_path = self.repo_root / file_path
            if full_path.exists() and full_path.is_file():
                size = full_path.stat().st_size
                
                if size == 0:
                    self.validation_results['compliance'].append({
                        'file': file_path,
                        'status': 'EMPTY',
                        'type': file_type,
                        'size': size
                    })
                    self.validation_results['warnings'].append(f"Empty compliance file: {file_path}")
                else:
                    self.validation_results['compliance'].append({
                        'file': file_path,
                        'status': 'PASS',
                        'type': file_type,
                        'size': size
                    })
            else:
                self.validation_results['compliance'].append({
                    'file': file_path,
                    'status': 'MISSING',
                    'type': file_type,
                    'size': 0
                })
                self.validation_results['errors'].append(f"Missing compliance file: {file_path}")
        
        print(f"  ✓ Checked {len(compliance_files)} compliance files\n")
    
    def validate_innovation_survey_admin(self):
        """Validate Innovation, Survey, and Admin specifications"""
        print("💡 Validating Innovation, Survey, and Admin Specifications...")
        
        specs = {
            'Innovation': [
                'foreman/innovation/idea-submission-spec.md',
                'foreman/innovation/idea-summarisation-rules.md',
                'foreman/innovation/idea-voting-policy.md',
                'foreman/innovation/innovation-dashboard-spec.md',
                'foreman/innovation/innovation-workflow-spec.md',
                'foreman/innovation/roadmap-generation-spec.md',
                'foreman/innovation/threshold-policy.md'
            ],
            'Survey': [
                'foreman/survey/survey-ai-analysis-spec.md',
                'foreman/survey/survey-engine-spec.md'
            ],
            'Admin': [
                'foreman/admin/admin-innovation-chat-spec.md',
                'foreman/admin/ai-self-improvement-spec.md',
                'foreman/admin/enhancement-parking-lot-spec.md'
            ]
        }
        
        for category, files in specs.items():
            for file_path in files:
                full_path = self.repo_root / file_path
                if full_path.exists() and full_path.is_file():
                    size = full_path.stat().st_size
                    self.validation_results['innovation_survey_admin'].append({
                        'category': category,
                        'file': file_path,
                        'status': 'PASS' if size > 0 else 'EMPTY',
                        'size': size
                    })
                    if size == 0:
                        self.validation_results['warnings'].append(f"Empty {category} file: {file_path}")
                else:
                    self.validation_results['innovation_survey_admin'].append({
                        'category': category,
                        'file': file_path,
                        'status': 'MISSING',
                        'size': 0
                    })
                    self.validation_results['errors'].append(f"Missing {category} file: {file_path}")
        
        total_specs = sum(len(files) for files in specs.values())
        print(f"  ✓ Checked {total_specs} Innovation/Survey/Admin specification files\n")
    
    def validate_builder_specs(self):
        """Validate builder agent specifications and configuration"""
        print("🤖 Validating Builder Agent Specifications...")
        
        builder_files = [
            'foreman/builder/api-builder-spec.md',
            'foreman/builder/integration-builder-spec.md',
            'foreman/builder/qa-builder-spec.md',
            'foreman/builder/schema-builder-spec.md',
            'foreman/builder/ui-builder-spec.md',
            'foreman/builder/builder-collaboration-rules.md'
        ]
        
        for file_path in builder_files:
            full_path = self.repo_root / file_path
            if full_path.exists() and full_path.is_file():
                size = full_path.stat().st_size
                self.validation_results['builder_specs'].append({
                    'file': file_path,
                    'status': 'PASS' if size > 0 else 'EMPTY',
                    'size': size
                })
                if size == 0:
                    self.validation_results['warnings'].append(f"Empty builder spec: {file_path}")
            else:
                self.validation_results['builder_specs'].append({
                    'file': file_path,
                    'status': 'MISSING',
                    'size': 0
                })
                self.validation_results['errors'].append(f"Missing builder spec: {file_path}")
        
        print(f"  ✓ Checked {len(builder_files)} builder specification files\n")
    
    def validate_json_files(self):
        """Validate JSON file integrity and structure"""
        print("🔧 Validating JSON File Integrity...")
        
        json_files = [
            'foreman/builder-manifest.json',
            'foreman/builder-task-map.json',
            'foreman/builder/builder-capability-map.json',
            'foreman/builder/builder-permission-policy.json',
            'foreman/compliance/compliance-control-library.json'
        ]
        
        for file_path in json_files:
            full_path = self.repo_root / file_path
            if full_path.exists() and full_path.is_file():
                size = full_path.stat().st_size
                
                if size == 0:
                    self.validation_results['json_integrity'].append({
                        'file': file_path,
                        'status': 'EMPTY',
                        'valid_json': False,
                        'size': size,
                        'error': 'File is empty'
                    })
                    self.validation_results['errors'].append(f"Empty JSON file: {file_path}")
                else:
                    try:
                        with open(full_path, 'r') as f:
                            data = json.load(f)
                        
                        self.validation_results['json_integrity'].append({
                            'file': file_path,
                            'status': 'PASS',
                            'valid_json': True,
                            'size': size,
                            'keys': list(data.keys()) if isinstance(data, dict) else None
                        })
                    except json.JSONDecodeError as e:
                        self.validation_results['json_integrity'].append({
                            'file': file_path,
                            'status': 'INVALID',
                            'valid_json': False,
                            'size': size,
                            'error': str(e)
                        })
                        self.validation_results['errors'].append(f"Invalid JSON in {file_path}: {str(e)}")
            else:
                self.validation_results['json_integrity'].append({
                    'file': file_path,
                    'status': 'MISSING',
                    'valid_json': False,
                    'size': 0,
                    'error': 'File not found'
                })
                self.validation_results['errors'].append(f"Missing JSON file: {file_path}")
        
        print(f"  ✓ Validated {len(json_files)} JSON files\n")
    
    def generate_recommendations(self):
        """Generate recommendations based on validation results"""
        print("💡 Generating Recommendations...")
        
        # Count issues
        error_count = len(self.validation_results['errors'])
        warning_count = len(self.validation_results['warnings'])
        
        recommendations = []
        
        # Critical recommendations
        if error_count > 0:
            recommendations.append({
                'priority': 'CRITICAL',
                'category': 'Missing Files',
                'recommendation': f'Address {error_count} missing or invalid files before activation'
            })
        
        # Check for empty compliance control library
        for item in self.validation_results['compliance']:
            if 'compliance-control-library.json' in item['file'] and item['status'] in ['EMPTY', 'INVALID']:
                recommendations.append({
                    'priority': 'HIGH',
                    'category': 'Compliance',
                    'recommendation': 'Populate compliance-control-library.json with control standards mapping'
                })
        
        # Check QA coverage
        missing_qa = [item for item in self.validation_results['qa_specs'] if item['status'] != 'PASS']
        if missing_qa:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'QA Coverage',
                'recommendation': 'Complete all QA and QA-of-QA specification files'
            })
        
        # Module completeness
        incomplete_modules = []
        for module in self.validation_results['specification_files']:
            missing_specs = []
            for phase, specs in module['phases'].items():
                for spec in specs:
                    if spec['status'] == 'MISSING':
                        missing_specs.append(f"{phase}/{spec['spec']}")
            if missing_specs:
                incomplete_modules.append({
                    'module': module['module'],
                    'missing': missing_specs
                })
        
        if incomplete_modules:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Module Specifications',
                'recommendation': f'{len(incomplete_modules)} modules have incomplete specifications',
                'details': incomplete_modules
            })
        
        # Platform specifications
        platform_files = [item for item in self.validation_results['innovation_survey_admin'] 
                          if item['status'] != 'PASS']
        if platform_files:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Platform Features',
                'recommendation': 'Complete Innovation, Survey, and Admin specifications'
            })
        
        # General improvements
        if warning_count > 0:
            recommendations.append({
                'priority': 'LOW',
                'category': 'Quality Improvement',
                'recommendation': f'Review and address {warning_count} warnings for optimal governance'
            })
        
        self.validation_results['recommendations'] = recommendations
        print(f"  ✓ Generated {len(recommendations)} recommendations\n")
    
    def determine_readiness_status(self) -> str:
        """Determine activation readiness status"""
        error_count = len(self.validation_results['errors'])
        warning_count = len(self.validation_results['warnings'])
        
        critical_issues = [r for r in self.validation_results.get('recommendations', []) 
                          if r['priority'] == 'CRITICAL']
        
        if error_count == 0 and warning_count == 0:
            return "READY FOR ACTIVATION ✅"
        elif error_count == 0 and warning_count <= 5:
            return "READY WITH MINOR IMPROVEMENTS RECOMMENDED ⚠️"
        elif error_count <= 3 and not critical_issues:
            return "REQUIRES ATTENTION BEFORE ACTIVATION ⚠️"
        else:
            return "NOT READY FOR ACTIVATION ❌"
    
    def generate_report(self) -> str:
        """Generate comprehensive validation report"""
        self.generate_recommendations()
        readiness = self.determine_readiness_status()
        
        report = []
        report.append("=" * 80)
        report.append("MATURION AI FOREMAN - REPOSITORY VALIDATION REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Executive Summary
        report.append("📊 EXECUTIVE SUMMARY")
        report.append("-" * 80)
        report.append(f"Activation Readiness: {readiness}")
        report.append(f"Total Errors: {len(self.validation_results['errors'])}")
        report.append(f"Total Warnings: {len(self.validation_results['warnings'])}")
        report.append(f"Recommendations: {len(self.validation_results['recommendations'])}")
        report.append("")
        
        # Folder Structure
        report.append("📁 FOLDER STRUCTURE VALIDATION")
        report.append("-" * 80)
        passed = sum(1 for item in self.validation_results['folder_structure'] if item['status'] == 'PASS')
        total = len(self.validation_results['folder_structure'])
        report.append(f"Status: {passed}/{total} directories validated")
        for item in self.validation_results['folder_structure']:
            status_icon = "✓" if item['status'] == 'PASS' else "✗"
            report.append(f"  {status_icon} {item['path']}: {item['message']}")
        report.append("")
        
        # Specification Files
        report.append("📋 SPECIFICATION FILES VALIDATION (PHASE 1-5)")
        report.append("-" * 80)
        for module in self.validation_results['specification_files']:
            report.append(f"\n{module['module']}:")
            for phase_name, specs in module['phases'].items():
                phase_status = []
                for spec in specs:
                    if spec['status'] == 'PASS':
                        phase_status.append('✓')
                    elif spec['status'] == 'OPTIONAL':
                        phase_status.append('○')
                    else:
                        phase_status.append('✗')
                
                status_summary = ''.join(phase_status)
                report.append(f"  {phase_name}: {status_summary}")
                
                for spec in specs:
                    if spec['status'] == 'MISSING':
                        report.append(f"    ✗ MISSING: {spec['spec']}")
                    elif spec['status'] == 'OPTIONAL':
                        report.append(f"    ○ OPTIONAL: {spec['spec']}")
        report.append("")
        
        # Governance Completeness
        report.append("⚖️  GOVERNANCE COMPLETENESS")
        report.append("-" * 80)
        passed = sum(1 for item in self.validation_results['governance_completeness'] if item['status'] == 'PASS')
        total = len(self.validation_results['governance_completeness'])
        report.append(f"Status: {passed}/{total} governance files validated")
        for item in self.validation_results['governance_completeness']:
            if item['status'] != 'PASS':
                status_icon = "✗" if item['status'] == 'MISSING' else "⚠"
                report.append(f"  {status_icon} {item['file']}: {item['status']}")
        report.append("")
        
        # QA Specifications
        report.append("✅ QA AND QA-OF-QA SPECIFICATIONS")
        report.append("-" * 80)
        passed = sum(1 for item in self.validation_results['qa_specs'] if item['status'] == 'PASS')
        total = len(self.validation_results['qa_specs'])
        report.append(f"Status: {passed}/{total} QA specification files validated")
        for item in self.validation_results['qa_specs']:
            status_icon = "✓" if item['status'] == 'PASS' else "✗"
            report.append(f"  {status_icon} {item['file']}: {item['status']}")
        report.append("")
        
        # Compliance
        report.append("📜 COMPLIANCE REFERENCE MAP AND CONTROL LIBRARY")
        report.append("-" * 80)
        passed = sum(1 for item in self.validation_results['compliance'] if item['status'] == 'PASS')
        total = len(self.validation_results['compliance'])
        report.append(f"Status: {passed}/{total} compliance files validated")
        for item in self.validation_results['compliance']:
            status_icon = "✓" if item['status'] == 'PASS' else ("⚠" if item['status'] == 'EMPTY' else "✗")
            report.append(f"  {status_icon} {item['file']}: {item['status']}")
        report.append("")
        
        # Innovation, Survey, Admin
        report.append("💡 INNOVATION, SURVEY, AND ADMIN SPECIFICATIONS")
        report.append("-" * 80)
        by_category = {}
        for item in self.validation_results['innovation_survey_admin']:
            cat = item['category']
            if cat not in by_category:
                by_category[cat] = {'total': 0, 'passed': 0}
            by_category[cat]['total'] += 1
            if item['status'] == 'PASS':
                by_category[cat]['passed'] += 1
        
        for category, stats in by_category.items():
            report.append(f"{category}: {stats['passed']}/{stats['total']} files validated")
        
        missing = [item for item in self.validation_results['innovation_survey_admin'] 
                   if item['status'] != 'PASS']
        if missing:
            report.append("\nMissing/Empty files:")
            for item in missing:
                status_icon = "✗" if item['status'] == 'MISSING' else "⚠"
                report.append(f"  {status_icon} {item['file']}: {item['status']}")
        report.append("")
        
        # Builder Specifications
        report.append("🤖 BUILDER AGENT SPECIFICATIONS")
        report.append("-" * 80)
        passed = sum(1 for item in self.validation_results['builder_specs'] if item['status'] == 'PASS')
        total = len(self.validation_results['builder_specs'])
        report.append(f"Status: {passed}/{total} builder specification files validated")
        for item in self.validation_results['builder_specs']:
            if item['status'] != 'PASS':
                status_icon = "✗" if item['status'] == 'MISSING' else "⚠"
                report.append(f"  {status_icon} {item['file']}: {item['status']}")
        report.append("")
        
        # JSON Integrity
        report.append("🔧 JSON FILE INTEGRITY")
        report.append("-" * 80)
        passed = sum(1 for item in self.validation_results['json_integrity'] if item['status'] == 'PASS')
        total = len(self.validation_results['json_integrity'])
        report.append(f"Status: {passed}/{total} JSON files validated")
        for item in self.validation_results['json_integrity']:
            status_icon = "✓" if item['status'] == 'PASS' else "✗"
            report.append(f"  {status_icon} {item['file']}: {item['status']}")
            if item['status'] != 'PASS':
                report.append(f"      Error: {item.get('error', 'Unknown error')}")
        report.append("")
        
        # Errors
        if self.validation_results['errors']:
            report.append("❌ ERRORS FOUND")
            report.append("-" * 80)
            for i, error in enumerate(self.validation_results['errors'], 1):
                report.append(f"{i}. {error}")
            report.append("")
        
        # Warnings
        if self.validation_results['warnings']:
            report.append("⚠️  WARNINGS")
            report.append("-" * 80)
            for i, warning in enumerate(self.validation_results['warnings'], 1):
                report.append(f"{i}. {warning}")
            report.append("")
        
        # Recommendations
        report.append("💡 RECOMMENDATIONS")
        report.append("-" * 80)
        for i, rec in enumerate(self.validation_results['recommendations'], 1):
            priority_icon = {
                'CRITICAL': '🔴',
                'HIGH': '🟠',
                'MEDIUM': '🟡',
                'LOW': '🟢'
            }.get(rec['priority'], '⚪')
            
            report.append(f"{i}. {priority_icon} [{rec['priority']}] {rec['category']}")
            report.append(f"   {rec['recommendation']}")
            if 'details' in rec:
                report.append(f"   Details: {rec['details']}")
            report.append("")
        
        # Final Status
        report.append("=" * 80)
        report.append(f"FINAL ACTIVATION READINESS STATUS: {readiness}")
        report.append("=" * 80)
        
        return "\n".join(report)


def main():
    """Main execution function"""
    repo_root = os.path.dirname(os.path.abspath(__file__))
    
    validator = RepositoryValidator(repo_root)
    validator.validate_all()
    
    report = validator.generate_report()
    print("\n" + report)
    
    # Save report to file
    report_path = os.path.join(repo_root, 'VALIDATION_REPORT.md')
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"\n📄 Validation report saved to: VALIDATION_REPORT.md")
    
    # Exit with error code if critical issues found
    error_count = len(validator.validation_results['errors'])
    if error_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
