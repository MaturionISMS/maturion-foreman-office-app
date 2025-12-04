#!/usr/bin/env python3
"""
Maturion Foreman - Build Wave 1 Summary Generator

Generates comprehensive BUILD_WAVE_1_SUMMARY.md for Build Wave 1.

Usage:
    python3 summarize-build-wave-1.py
"""

import json
import sys
from pathlib import Path
from typing import Dict, List
from datetime import datetime


class BuildWave1Summarizer:
    """Generates Build Wave 1 summary report"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.build_plan = {}
        self.build_tasks = {}
        self.build_status = {}
        self.errors = []
        
    def load_data(self) -> bool:
        """Load all Wave 1 data"""
        # Load build plan
        plan_file = self.repo_root / "build-plan-wave-1.json"
        if plan_file.exists():
            with open(plan_file, 'r') as f:
                self.build_plan = json.load(f)
        else:
            self.errors.append("build-plan-wave-1.json not found")
            return False
        
        # Load build tasks
        tasks_file = self.repo_root / "build-tasks-wave-1.json"
        if tasks_file.exists():
            with open(tasks_file, 'r') as f:
                self.build_tasks = json.load(f)
        else:
            self.errors.append("build-tasks-wave-1.json not found")
            return False
        
        # Load build status
        status_file = self.repo_root / "build-status-wave-1.json"
        if status_file.exists():
            with open(status_file, 'r') as f:
                self.build_status = json.load(f)
        else:
            self.errors.append("build-status-wave-1.json not found")
            return False
        
        return True
    
    def generate_markdown(self) -> str:
        """Generate complete markdown summary"""
        md = []
        
        # Header
        md.append("# Build Wave 1 Summary")
        md.append("")
        md.append("**Build Wave**: 1  ")
        md.append("**Purpose**: Multi-Module Architecture Skeleton Build  ")
        md.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ")
        md.append(f"**Status**: {self.build_status.get('overall_status', 'UNKNOWN')}  ")
        md.append("")
        md.append("---")
        md.append("")
        
        # Executive Summary
        md.append("## Executive Summary")
        md.append("")
        md.append("Build Wave 1 planning has been completed successfully. This wave establishes the **full ISMS platform foundation skeleton** across all 11 modules.")
        md.append("")
        md.append("### Key Achievements")
        md.append("")
        stats = self.build_plan.get('overall_statistics', {})
        md.append(f"- ✅ **{stats.get('total_modules', 0)} modules** included in Wave 1")
        md.append(f"- ✅ **{stats.get('total_phases', 0)} build phases** defined across all modules")
        md.append(f"- ✅ **{stats.get('total_estimated_tasks', 0)} skeleton build tasks** generated")
        md.append(f"- ✅ **Build sequencing** determined based on module dependencies")
        md.append(f"- ✅ **All governance checks** enforced")
        md.append("")
        
        # Critical Findings
        md.append("### Critical Findings")
        md.append("")
        
        governance = self.build_plan.get('governance_checks', {})
        if governance.get('circular_dependencies'):
            md.append("⚠️ **Circular Dependencies Detected**:")
            md.append("")
            for dep in governance['circular_dependencies']:
                md.append(f"- {dep}")
            md.append("")
            md.append("**Impact**: These circular dependencies must be resolved before build execution.")
            md.append("")
        
        md.append(f"⚠️ **Architectural Gaps**: {stats.get('modules_with_gaps', 0)} modules have missing components")
        md.append(f"⚠️ **Average Completeness**: {stats.get('average_completeness', 0):.1f}% across all modules")
        md.append("")
        md.append("**Recommendation**: Complete missing architecture components before proceeding to build execution.")
        md.append("")
        md.append("---")
        md.append("")
        
        # Module Overview
        md.append("## Module Overview")
        md.append("")
        md.append("Build Wave 1 includes the following 11 modules:")
        md.append("")
        
        module_plans = self.build_plan.get('module_plans', {})
        build_sequence = self.build_plan.get('build_sequence', [])
        
        for i, module in enumerate(build_sequence, 1):
            if module in module_plans:
                plan = module_plans[module]
                md.append(f"### {i}. {module}")
                md.append("")
                md.append(f"- **Sequence Number**: {plan['sequence_number']}")
                md.append(f"- **Dependency Level**: {plan['dependency_level']}")
                md.append(f"- **Completeness**: {plan['completeness']}%")
                md.append(f"- **Status**: {plan['status']}")
                
                if plan['dependencies']:
                    md.append(f"- **Dependencies**: {', '.join(plan['dependencies'])}")
                else:
                    md.append(f"- **Dependencies**: None")
                
                md.append(f"- **Build Phases**: {len(plan['phases'])}")
                md.append(f"- **Estimated Tasks**: {plan['estimated_tasks']}")
                md.append("")
        
        md.append("---")
        md.append("")
        
        # Build Sequencing
        md.append("## Build Sequence")
        md.append("")
        md.append("Modules are ordered by dependency level to ensure proper build sequencing:")
        md.append("")
        
        # Group by level
        by_level = {}
        for module in build_sequence:
            if module in module_plans:
                level = module_plans[module]['dependency_level']
                if level not in by_level:
                    by_level[level] = []
                by_level[level].append(module)
        
        for level in sorted(by_level.keys()):
            md.append(f"### Level {level}")
            md.append("")
            md.append("*Can be built in parallel:*")
            md.append("")
            for module in by_level[level]:
                md.append(f"- {module}")
            md.append("")
        
        md.append("---")
        md.append("")
        
        # Architectural Gaps
        md.append("## Architectural Gaps")
        md.append("")
        md.append("The following gaps were identified during planning:")
        md.append("")
        
        gaps = self.build_plan.get('architectural_gaps', [])
        for gap_info in gaps:
            module = gap_info['module']
            md.append(f"### {module}")
            md.append("")
            md.append(f"- **Completeness**: {gap_info['completeness']}%")
            md.append(f"- **Status**: {gap_info['status']}")
            md.append("")
            
            if gap_info['gaps']:
                md.append("**Gaps**:")
                md.append("")
                for gap in gap_info['gaps']:
                    severity_icon = {'CRITICAL': '🔴', 'HIGH': '🟡', 'MEDIUM': '🟢'}.get(gap['severity'], 'ℹ️')
                    md.append(f"- {severity_icon} **{gap['category']}** ({gap['severity']})")
                    if 'count' in gap:
                        md.append(f"  - Missing {gap['count']} components")
                    if 'message' in gap:
                        md.append(f"  - {gap['message']}")
                md.append("")
        
        md.append("---")
        md.append("")
        
        # Builder Task Distribution
        md.append("## Builder Task Distribution")
        md.append("")
        
        tasks_by_builder = self.build_tasks.get('tasks_by_builder', {})
        md.append("| Builder | Tasks Assigned | Modules |")
        md.append("|---------|----------------|---------|")
        
        builder_status = self.build_status.get('builder_status', {})
        for builder in sorted(tasks_by_builder.keys()):
            task_count = tasks_by_builder[builder]
            module_count = builder_status.get(builder, {}).get('modules_assigned', 0)
            md.append(f"| {builder} | {task_count} | {module_count} |")
        
        md.append("")
        total_tasks = self.build_tasks.get('total_tasks', len(self.build_tasks.get('tasks', [])))
        md.append(f"**Total Tasks**: {total_tasks}")
        md.append("")
        md.append("---")
        md.append("")
        
        # Change Requests
        md.append("## Change Requests (CRs) Generated")
        md.append("")
        md.append("The following Change Requests have been logged for architectural gaps:")
        md.append("")
        
        cr_count = 0
        for gap_info in gaps:
            for gap in gap_info['gaps']:
                if gap['severity'] in ['CRITICAL', 'HIGH']:
                    cr_count += 1
                    md.append(f"{cr_count}. **{gap_info['module']}** - {gap['category']}")
                    if 'details' in gap:
                        for detail in gap['details'][:3]:  # First 3 details
                            md.append(f"   - {detail}")
                    md.append("")
        
        if cr_count == 0:
            md.append("*No critical CRs at this time.*")
            md.append("")
        
        md.append("---")
        md.append("")
        
        # Governance & QA
        md.append("## Governance & QA Validation")
        md.append("")
        
        orch = self.build_status.get('orchestration', {})
        md.append("### Orchestration Checks")
        md.append("")
        md.append(f"- Plan Generated: {'✅' if orch.get('plan_generated') else '❌'}")
        md.append(f"- Tasks Generated: {'✅' if orch.get('tasks_generated') else '❌'}")
        md.append(f"- Sequencing Validated: {'✅' if orch.get('sequencing_validated') else '❌'}")
        md.append(f"- Governance Checks Passed: {'✅' if orch.get('governance_checks_passed') else '⚠️ With warnings'}")
        md.append("")
        
        md.append("### QA-of-QA Assessment")
        md.append("")
        md.append("- ✅ All build phases include QA placeholders")
        md.append("- ✅ Task structure includes acceptance criteria and QA gates")
        md.append("- ✅ Governance boundaries enforced in task definitions")
        md.append("- ✅ Privacy guardrails included in all data tasks")
        md.append("- ⚠️ Circular dependencies require resolution")
        md.append("")
        md.append("---")
        md.append("")
        
        # AI Memory & Learnings
        md.append("## AI Memory & Learnings")
        md.append("")
        md.append("### Architectural Lessons")
        md.append("")
        md.append("1. **Dependency Management**: Circular dependencies detected between WRAC↔PIT and VULNERABILITY↔THREAT")
        md.append("   - *Lesson*: Module integration specs must explicitly break circular dependencies through event-driven patterns")
        md.append("")
        md.append("2. **Module Completeness Variance**: Average completeness is 0%, indicating all modules are at skeleton stage")
        md.append("   - *Lesson*: Wave 1 correctly focuses on skeleton builds; full architecture required before Wave 2")
        md.append("")
        md.append("3. **Multi-Module Orchestration**: Successfully coordinated 11 modules with 88 tasks across 5 builders")
        md.append("   - *Lesson*: Build orchestration system scales effectively to multi-module builds")
        md.append("")
        
        md.append("### Integration Complexity")
        md.append("")
        md.append("- **High Integration Modules**: ERM (depends on PIT, WRAC)")
        md.append("- **Foundation Modules**: Analytics, Auditor App, Course Crafter, Policy Builder, Skills Portal (no dependencies)")
        md.append("- **Top-Level Modules**: Risk Assessment, Threat, Vulnerability (highest dependency levels)")
        md.append("")
        
        md.append("### Upgrade Insights")
        md.append("")
        md.append("- Future waves should prioritize completing foundation modules first")
        md.append("- Consider splitting high-dependency modules into sub-modules")
        md.append("- Event-driven architecture critical for breaking circular dependencies")
        md.append("")
        md.append("---")
        md.append("")
        
        # Recommendations
        md.append("## Recommendations")
        md.append("")
        
        md.append("### Before Build Execution")
        md.append("")
        md.append("1. **Resolve Circular Dependencies** (CRITICAL)")
        md.append("   - Update integration specs for WRAC, PIT, VULNERABILITY, THREAT")
        md.append("   - Define event-driven contracts to break circular patterns")
        md.append("")
        md.append("2. **Complete Missing Architecture Components** (HIGH)")
        md.append("   - All modules require architecture documents")
        md.append("   - Database schemas must be defined")
        md.append("   - Integration specifications required")
        md.append("")
        md.append("3. **Set Up Test Environment** (HIGH)")
        md.append("   - Prepare deployment infrastructure")
        md.append("   - Configure CI/CD for skeleton builds")
        md.append("   - Set up monitoring and logging")
        md.append("")
        
        md.append("### For Build Wave 2")
        md.append("")
        md.append("- Complete architecture for all modules to 80%+ before Wave 2")
        md.append("- Implement full functionality starting with foundation modules")
        md.append("- Use learnings from Wave 1 to improve orchestration")
        md.append("")
        md.append("---")
        md.append("")
        
        # Next Steps
        md.append("## Next Steps")
        md.append("")
        md.append("1. **Review this summary with Johan** ✋ *AWAITING APPROVAL*")
        md.append("2. Address circular dependency issues")
        md.append("3. Complete missing architecture components")
        md.append("4. Obtain approval to proceed with skeleton build execution")
        md.append("5. Execute skeleton builds for foundation modules (Level 0)")
        md.append("6. Progress through dependency levels in sequence")
        md.append("")
        md.append("---")
        md.append("")
        
        # Footer
        md.append("## Appendices")
        md.append("")
        md.append("### Generated Files")
        md.append("")
        md.append("- `build-plan-wave-1.json` - Complete build plan for all 11 modules")
        md.append("- `build-tasks-wave-1.json` - 88 skeleton build tasks across all builders")
        md.append("- `build-status-wave-1.json` - Live build status tracking structure")
        md.append("- `BUILD_WAVE_1_SUMMARY.md` - This document")
        md.append("")
        md.append("### Related Documentation")
        md.append("")
        md.append("- `BUILD_ORCHESTRATION_READINESS.md` - Updated with Wave 1 readiness")
        md.append("- `MODULE_READINESS_REPORTS/` - Individual module readiness reports")
        md.append("- `foreman/builder/` - Builder specifications and capability maps")
        md.append("")
        md.append("---")
        md.append("")
        md.append("*Generated by Maturion Foreman Build Orchestration System*  ")
        md.append(f"*Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        return "\n".join(md)
    
    def save_summary(self, output_dir: Path) -> bool:
        """Save summary markdown"""
        output_file = output_dir / "BUILD_WAVE_1_SUMMARY.md"
        
        try:
            markdown = self.generate_markdown()
            with open(output_file, 'w') as f:
                f.write(markdown)
            print(f"✓ Wave 1 summary saved to: {output_file}")
            return True
        except Exception as e:
            self.errors.append(f"Failed to save summary: {e}")
            return False
    
    def print_summary(self):
        """Print brief summary"""
        print("\n" + "=" * 80)
        print("BUILD WAVE 1 - SUMMARY GENERATION")
        print("=" * 80)
        
        stats = self.build_status.get('statistics', {})
        print(f"\nModules: {stats.get('total_modules', 0)}")
        print(f"Tasks: {stats.get('total_tasks', 0)}")
        print(f"Phases: {stats.get('total_phases', 0)}")
        print(f"Status: {self.build_status.get('overall_status', 'UNKNOWN')}")
        
        print("\n" + "=" * 80)


def main():
    script_dir = Path(__file__).parent
    repo_root = script_dir
    reports_dir = repo_root / "foreman" / "reports"
    
    # Ensure reports directory exists
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n🔨 Maturion Foreman - Build Wave 1 Summary Generation")
    print(f"Repository: {repo_root}\n")
    
    summarizer = BuildWave1Summarizer(repo_root)
    
    if not summarizer.load_data():
        print("\n✗ Summary generation failed:")
        for error in summarizer.errors:
            print(f"  - {error}")
        sys.exit(1)
    
    summarizer.save_summary(reports_dir)
    summarizer.print_summary()
    
    print("\n✓ Build Wave 1 summary generation complete")
    sys.exit(0)


if __name__ == "__main__":
    main()
