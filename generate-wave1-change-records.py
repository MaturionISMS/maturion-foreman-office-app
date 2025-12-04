#!/usr/bin/env python3
"""
Maturion Foreman - Build Wave 1 Change Records Generator

Generates Change Records for all modules with architectural gaps identified
during Build Wave 1 planning.

Usage:
    python3 generate-wave1-change-records.py
"""

import json
import os
from pathlib import Path
from datetime import datetime


class Wave1ChangeRecordGenerator:
    """Generates Change Records for Build Wave 1 architectural gaps"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.build_plan = {}
        self.change_records = []
        self.cr_dir = repo_root / 'foreman' / 'change-management'
        
    def load_build_plan(self) -> bool:
        """Load Build Wave 1 plan"""
        plan_file = self.repo_root / 'build-plan-wave-1.json'
        if not plan_file.exists():
            print(f"ERROR: {plan_file} not found")
            return False
            
        with open(plan_file, 'r') as f:
            self.build_plan = json.load(f)
        return True
        
    def generate_change_records(self):
        """Generate a CR for each module with gaps"""
        gaps = self.build_plan.get('architectural_gaps', [])
        
        print(f"Generating Change Records for {len(gaps)} modules with gaps...")
        
        for idx, gap_info in enumerate(gaps, 1):
            module = gap_info['module']
            cr_id = f"CR-BW1-{idx:03d}"
            
            # Extract gap details
            missing_components = []
            for gap in gap_info.get('gaps', []):
                if gap.get('category') == 'MISSING_COMPONENTS':
                    for component in gap.get('details', []):
                        missing_components.append({
                            "component": component,
                            "description": self._get_component_description(component),
                            "priority": self._get_component_priority(component),
                            "reason": self._get_component_reason(component)
                        })
            
            # Create CR
            cr = {
                "change_record_id": cr_id,
                "title": f"Complete {module} Module Architecture Components for Build Wave 1",
                "created_at": datetime.utcnow().isoformat() + 'Z',
                "created_by": "Maturion Foreman - Build Wave 1 Orchestration",
                "source": "Build Wave 1 - Multi-Module Readiness Assessment",
                "type": "ARCHITECTURE_GAP",
                "priority": "HIGH",
                "status": "OPEN",
                "affected_modules": [module],
                "description": f"{module} module has {len(missing_components)} missing architecture components. These must be completed before full build implementation can proceed. Build Wave 1 proceeds with skeleton build only.",
                "business_justification": f"Complete architecture for {module} is required for future full implementation builds (Wave 2+). Skeleton builds can proceed in Wave 1, but full functionality requires complete architecture.",
                "impact_analysis": {
                    "scope": f"{module} Module",
                    "affected_systems": ["Build Orchestration", f"{module} Module"],
                    "risk_level": "MEDIUM",
                    "impact_areas": [
                        "Build Wave 1 proceeds with skeleton only",
                        f"{module} module full implementation blocked until architecture complete",
                        "Dependent modules may have limited integration capability"
                    ],
                    "user_impact": "No direct user impact - internal build process",
                    "compliance_impact": "None - architecture gap only",
                    "data_impact": "None"
                },
                "missing_components": missing_components,
                "proposed_solution": {
                    "approach": f"Create all missing architecture components for {module} following minimum-architecture-template.md",
                    "steps": self._generate_solution_steps(module, missing_components),
                    "estimated_effort": "1-2 weeks",
                    "resources_required": [
                        "Architecture expertise",
                        f"Domain knowledge of {module} functionality",
                        "Integration knowledge of ISMS ecosystem",
                        "QA expertise"
                    ],
                    "dependencies": [
                        "Integrated ISMS Architecture",
                        "Module integration map",
                        "Compliance control library"
                    ]
                },
                "risk_assessment": {
                    "implementation_risk": "MEDIUM",
                    "rollback_complexity": "LOW",
                    "risks": [
                        {
                            "risk": "Architecture components incomplete or incorrect",
                            "likelihood": "MEDIUM",
                            "impact": "HIGH",
                            "mitigation": "Use architecture validation checklist, peer review, Foreman validation"
                        },
                        {
                            "risk": "Integration specifications conflict with other modules",
                            "likelihood": "LOW",
                            "impact": "MEDIUM",
                            "mitigation": "Review integration map, validate against dependencies"
                        }
                    ]
                },
                "test_plan": {
                    "validation_steps": [
                        "Run standardise-architecture.py to validate completeness",
                        "Run plan-build.py to verify readiness",
                        "Architecture validation checklist review",
                        "Foreman validation of architecture alignment"
                    ],
                    "success_criteria": [
                        f"{module} module completeness >= 80%",
                        "All critical components complete",
                        "Module status changes to READY for full build"
                    ]
                },
                "rollback_plan": {
                    "approach": "Not applicable - architecture addition has no rollback",
                    "steps": [],
                    "recovery_time": "N/A"
                },
                "approval_workflow": {
                    "required_approvers": ["Johan (Human Review)"],
                    "approval_status": "PENDING",
                    "approvals": []
                },
                "implementation_timeline": {
                    "planned_start": "Post Build Wave 1",
                    "planned_completion": "Before Build Wave 2",
                    "actual_start": None,
                    "actual_completion": None,
                    "milestones": [
                        {
                            "milestone": "Critical components complete",
                            "target": "Week 1",
                            "components": self._get_critical_components(missing_components)
                        },
                        {
                            "milestone": "All components complete",
                            "target": "Week 2",
                            "components": "All remaining components"
                        }
                    ]
                },
                "related_issues": [cr_id],
                "communication_plan": {
                    "stakeholders": ["Johan", "Maturion Foreman", "Builder Agents"],
                    "notifications": [
                        {
                            "event": "CR Created",
                            "recipients": ["Johan"],
                            "method": "GitHub Issue / Build Wave 1 Summary"
                        }
                    ]
                },
                "lessons_learned": {
                    "captured_during": "Build Wave 1 Planning",
                    "key_insights": [
                        "Skeleton builds can proceed without complete architecture",
                        "Full implementation requires complete architecture foundation",
                        "Early identification of gaps enables proactive planning"
                    ],
                    "improvements_for_future": [
                        "Establish architecture-first approach",
                        "Set minimum completeness threshold as policy",
                        "Create architecture templates for new modules"
                    ]
                },
                "ai_memory_links": {
                    "historical_issue": f"BW1-{module}",
                    "reasoning_patterns": ["Multi-module build orchestration"],
                    "upgrade_insights": "build-wave-1-architectural-gaps.md"
                }
            }
            
            self.change_records.append(cr)
            
            # Save CR to file
            cr_file = self.cr_dir / f"{cr_id}-{module}-Architecture-Gaps.json"
            with open(cr_file, 'w') as f:
                json.dump(cr, f, indent=2)
            
            print(f"  ✅ Generated {cr_id} for {module} ({len(missing_components)} gaps)")
        
        return True
        
    def _get_component_description(self, component: str) -> str:
        """Get human-readable description for component"""
        descriptions = {
            "TRUE_NORTH": "Module Vision and Objectives",
            "ARCHITECTURE": "System Architecture Document",
            "INTEGRATION_SPEC": "Module Integration Specification",
            "DATABASE_SCHEMA": "Data Model and Schema",
            "FRONTEND_COMPONENT_MAP": "UI Components Map",
            "WIREFRAMES": "UI Design Wireframes",
            "QA_IMPLEMENTATION_PLAN": "Quality Assurance Plan",
            "IMPLEMENTATION_GUIDE": "Implementation Guide",
            "SPRINT_PLAN": "Development Sprint Plan",
            "CHANGELOG": "Version History",
            "EDGE_FUNCTIONS": "Backend API Specification",
            "WATCHDOG_LOGIC": "Monitoring Logic",
            "MODEL_ROUTING_SPEC": "AI Model Routing",
            "EXPORT_SPEC": "Data Export Specification"
        }
        return descriptions.get(component, component.replace('_', ' ').title())
        
    def _get_component_priority(self, component: str) -> str:
        """Get priority for component"""
        critical = ["INTEGRATION_SPEC", "DATABASE_SCHEMA", "EDGE_FUNCTIONS"]
        high = ["FRONTEND_COMPONENT_MAP", "WIREFRAMES", "QA_IMPLEMENTATION_PLAN", "TRUE_NORTH", "ARCHITECTURE"]
        
        if component in critical:
            return "CRITICAL"
        elif component in high:
            return "HIGH"
        else:
            return "MEDIUM"
            
    def _get_component_reason(self, component: str) -> str:
        """Get reason for component importance"""
        reasons = {
            "TRUE_NORTH": "Defines module vision and objectives",
            "ARCHITECTURE": "Defines system structure and design",
            "INTEGRATION_SPEC": "Required for inter-module communication design",
            "DATABASE_SCHEMA": "Foundation for all data operations",
            "FRONTEND_COMPONENT_MAP": "Required for UI builder",
            "WIREFRAMES": "Required for UI implementation",
            "QA_IMPLEMENTATION_PLAN": "Required for QA builder",
            "IMPLEMENTATION_GUIDE": "Guides builder implementation",
            "SPRINT_PLAN": "Organizes development timeline",
            "CHANGELOG": "Tracks changes over time",
            "EDGE_FUNCTIONS": "Required for API builder",
            "WATCHDOG_LOGIC": "Required for runtime monitoring",
            "MODEL_ROUTING_SPEC": "Required for AI integration",
            "EXPORT_SPEC": "Required for data export functionality"
        }
        return reasons.get(component, "Required for complete architecture")
        
    def _generate_solution_steps(self, module: str, components: list) -> list:
        """Generate solution steps for completing architecture"""
        steps = []
        for idx, comp in enumerate(components, 1):
            comp_name = comp['component']
            steps.append(f"{idx}. Create {comp_name} for {module} module")
        steps.append(f"{len(components) + 1}. Validate all components with standardise-architecture.py")
        steps.append(f"{len(components) + 2}. Review and approve architecture")
        return steps
        
    def _get_critical_components(self, components: list) -> list:
        """Get list of critical component names"""
        critical = [c['component'] for c in components if c['priority'] == 'CRITICAL']
        return critical if critical else ["All critical components"]
        
    def generate_summary(self):
        """Generate summary of CRs created"""
        summary_file = self.cr_dir / 'WAVE1_CHANGE_RECORDS_SUMMARY.md'
        
        with open(summary_file, 'w') as f:
            f.write("# Build Wave 1 - Change Records Summary\n\n")
            f.write(f"**Generated**: {datetime.utcnow().isoformat()}Z\n")
            f.write(f"**Total Change Records**: {len(self.change_records)}\n\n")
            f.write("---\n\n")
            f.write("## Change Records Created\n\n")
            
            for cr in self.change_records:
                f.write(f"### {cr['change_record_id']}: {cr['title']}\n\n")
                f.write(f"- **Module**: {cr['affected_modules'][0]}\n")
                f.write(f"- **Missing Components**: {len(cr['missing_components'])}\n")
                f.write(f"- **Priority**: {cr['priority']}\n")
                f.write(f"- **Status**: {cr['status']}\n")
                f.write(f"- **File**: `{cr['change_record_id']}-{cr['affected_modules'][0]}-Architecture-Gaps.json`\n\n")
                
                f.write("**Missing Components**:\n")
                for comp in cr['missing_components']:
                    f.write(f"- {comp['component']} ({comp['priority']}): {comp['description']}\n")
                f.write("\n")
                
            f.write("---\n\n")
            f.write("## Next Steps\n\n")
            f.write("1. Review all Change Records\n")
            f.write("2. Prioritize architecture completion work\n")
            f.write("3. Assign resources for architecture completion\n")
            f.write("4. Complete architecture components post Build Wave 1\n")
            f.write("5. Validate architecture with standardise-architecture.py\n\n")
            f.write("---\n\n")
            f.write("*Generated by Maturion Foreman - Build Wave 1 Orchestration*\n")
        
        print(f"\n✅ Summary saved to {summary_file}")


def main():
    """Main execution"""
    repo_root = Path(__file__).parent
    
    print("=" * 80)
    print("Maturion Foreman - Build Wave 1 Change Records Generator")
    print("=" * 80)
    print()
    
    generator = Wave1ChangeRecordGenerator(repo_root)
    
    # Load build plan
    if not generator.load_build_plan():
        print("ERROR: Failed to load build plan")
        return 1
        
    # Generate CRs
    if not generator.generate_change_records():
        print("ERROR: Failed to generate change records")
        return 1
        
    # Generate summary
    generator.generate_summary()
    
    print()
    print("=" * 80)
    print(f"✅ Successfully generated {len(generator.change_records)} Change Records")
    print("=" * 80)
    
    return 0


if __name__ == '__main__':
    exit(main())
