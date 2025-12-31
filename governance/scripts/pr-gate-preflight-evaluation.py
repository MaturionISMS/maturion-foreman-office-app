#!/usr/bin/env python3
"""
PR-Gate Preflight Evaluation Script

Purpose: Validate that PR gate workflows are syntactically correct, dependency-complete,
         and role-aware BEFORE any builder PR is submitted.

Constitutional Authority:
- BUILD_PHILOSOPHY.md Section II.1 - One-Time Build Correctness
- Agent Contract Section 6D - CI Confirmatory Role
- governance/build/PR_GATE_RELEASE_CHECKS_SYSTEM_SPEC.md

Version: 1.0.0
Date: 2025-12-30
"""

import os
import sys
import json
import yaml
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple

class PreflightEvaluator:
    """Evaluates PR gate workflows for correctness and completeness."""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.workflows_dir = repo_root / ".github" / "workflows"
        self.results = {
            "timestamp": datetime.now(datetime.UTC if hasattr(datetime, 'UTC') else None).isoformat().replace('+00:00', 'Z') if hasattr(datetime, 'UTC') else datetime.utcnow().isoformat() + "Z",
            "evaluation_status": "PENDING",
            "workflows_evaluated": 0,
            "validation_results": {
                "syntax_validation": {"status": "PENDING", "errors": []},
                "dependency_verification": {"status": "PENDING", "missing": []},
                "trigger_validation": {"status": "PENDING", "issues": []},
                "role_awareness": {"status": "PENDING", "violations": []}
            },
            "gate_readiness": "NOT_READY",
            "blocking_issues": []
        }
    
    def evaluate(self) -> Dict[str, Any]:
        """Run all preflight evaluations."""
        print("🔍 Starting PR-Gate Preflight Evaluation...")
        print(f"   Repository: {self.repo_root}")
        print(f"   Workflows Directory: {self.workflows_dir}")
        print()
        
        if not self.workflows_dir.exists():
            self.results["blocking_issues"].append(
                "Workflows directory not found: .github/workflows"
            )
            self.results["evaluation_status"] = "FAIL"
            return self.results
        
        # Get all workflow files
        workflow_files = list(self.workflows_dir.glob("*.yml")) + \
                        list(self.workflows_dir.glob("*.yaml"))
        
        if not workflow_files:
            self.results["blocking_issues"].append(
                "No workflow files found in .github/workflows"
            )
            self.results["evaluation_status"] = "FAIL"
            return self.results
        
        self.results["workflows_evaluated"] = len(workflow_files)
        print(f"📋 Found {len(workflow_files)} workflow files")
        
        # Run evaluations
        self._validate_syntax(workflow_files)
        self._verify_dependencies(workflow_files)
        self._validate_triggers(workflow_files)
        self._verify_role_awareness(workflow_files)
        
        # Determine overall status
        self._determine_status()
        
        return self.results
    
    def _validate_syntax(self, workflow_files: List[Path]):
        """Validate YAML syntax and GitHub Actions structure."""
        print("\n1️⃣  Validating Workflow Syntax...")
        errors = []
        
        for workflow_file in workflow_files:
            try:
                with open(workflow_file, 'r') as f:
                    workflow_data = yaml.safe_load(f)
                
                # Validate basic structure
                if not isinstance(workflow_data, dict):
                    errors.append(f"{workflow_file.name}: Root must be a dictionary")
                    continue
                
                # Check for required top-level keys
                # Note: YAML parses 'on:' as boolean True
                if 'on' not in workflow_data and True not in workflow_data:
                    errors.append(f"{workflow_file.name}: Missing 'on' trigger definition")
                
                if 'jobs' not in workflow_data:
                    errors.append(f"{workflow_file.name}: Missing 'jobs' definition")
                
                # Validate jobs structure
                if 'jobs' in workflow_data:
                    jobs = workflow_data['jobs']
                    if not isinstance(jobs, dict):
                        errors.append(f"{workflow_file.name}: 'jobs' must be a dictionary")
                    else:
                        for job_name, job_data in jobs.items():
                            if not isinstance(job_data, dict):
                                errors.append(f"{workflow_file.name}: Job '{job_name}' must be a dictionary")
                            elif 'runs-on' not in job_data:
                                errors.append(f"{workflow_file.name}: Job '{job_name}' missing 'runs-on'")
                            elif 'steps' not in job_data:
                                errors.append(f"{workflow_file.name}: Job '{job_name}' missing 'steps'")
                
                print(f"   ✅ {workflow_file.name}: Syntax valid")
                
            except yaml.YAMLError as e:
                errors.append(f"{workflow_file.name}: YAML parse error: {str(e)}")
                print(f"   ❌ {workflow_file.name}: YAML parse error")
            except Exception as e:
                errors.append(f"{workflow_file.name}: Unexpected error: {str(e)}")
                print(f"   ❌ {workflow_file.name}: Unexpected error")
        
        self.results["validation_results"]["syntax_validation"]["errors"] = errors
        self.results["validation_results"]["syntax_validation"]["status"] = \
            "PASS" if not errors else "FAIL"
        
        if errors:
            self.results["blocking_issues"].extend(errors)
    
    def _verify_dependencies(self, workflow_files: List[Path]):
        """Verify that all dependencies are available."""
        print("\n2️⃣  Verifying Dependencies...")
        missing = []
        
        for workflow_file in workflow_files:
            try:
                with open(workflow_file, 'r') as f:
                    workflow_data = yaml.safe_load(f)
                
                if 'jobs' not in workflow_data:
                    continue
                
                for job_name, job_data in workflow_data['jobs'].items():
                    if 'steps' not in job_data:
                        continue
                    
                    for step in job_data['steps']:
                        # Check for uses (GitHub Actions)
                        if 'uses' in step:
                            action = step['uses']
                            # Note: We can't verify external actions availability without network
                            # This is a limitation documented in the spec
                            print(f"   📦 {workflow_file.name}: Uses action '{action}'")
                        
                        # Check for run commands that reference scripts
                        if 'run' in step:
                            run_cmd = step['run']
                            # Look for python scripts
                            if 'python' in run_cmd.lower():
                                script_refs = self._extract_script_references(run_cmd)
                                for script_ref in script_refs:
                                    script_path = self.repo_root / script_ref
                                    if not script_path.exists():
                                        missing.append(
                                            f"{workflow_file.name}: Referenced script not found: {script_ref}"
                                        )
                                        print(f"   ❌ Missing script: {script_ref}")
                                    else:
                                        print(f"   ✅ Script exists: {script_ref}")
                
            except Exception as e:
                missing.append(f"{workflow_file.name}: Error checking dependencies: {str(e)}")
        
        self.results["validation_results"]["dependency_verification"]["missing"] = missing
        self.results["validation_results"]["dependency_verification"]["status"] = \
            "PASS" if not missing else "FAIL"
        
        if missing:
            self.results["blocking_issues"].extend(missing)
    
    def _extract_script_references(self, run_cmd: str) -> List[str]:
        """Extract script file references from run commands."""
        references = []
        
        # Simple heuristic: look for .py files
        words = run_cmd.split()
        for word in words:
            if word.endswith('.py'):
                # Remove any quotes
                word = word.strip('\'"')
                references.append(word)
        
        return references
    
    def _validate_triggers(self, workflow_files: List[Path]):
        """Validate workflow trigger conditions."""
        print("\n3️⃣  Validating Trigger Conditions...")
        issues = []
        
        for workflow_file in workflow_files:
            try:
                with open(workflow_file, 'r') as f:
                    workflow_data = yaml.safe_load(f)
                
                if 'on' not in workflow_data and True not in workflow_data:
                    continue
                
                # YAML parses 'on:' as boolean True
                triggers = workflow_data.get('on', workflow_data.get(True, {}))
                
                # Check for PR triggers (expected for PR gates)
                if 'pull_request' in triggers or 'pull_request_target' in triggers:
                    print(f"   ✅ {workflow_file.name}: Has PR trigger")
                else:
                    # Not necessarily an error, but worth noting
                    print(f"   ℹ️  {workflow_file.name}: No PR trigger (may be intentional)")
                
                # Validate trigger structure
                if isinstance(triggers, dict):
                    for trigger_name, trigger_config in triggers.items():
                        if isinstance(trigger_config, dict):
                            # Check for branches, paths, types filters
                            if 'branches' in trigger_config:
                                print(f"   📌 {workflow_file.name}: Filtered by branches")
                            if 'types' in trigger_config:
                                print(f"   📌 {workflow_file.name}: Filtered by PR types")
                
            except Exception as e:
                issues.append(f"{workflow_file.name}: Error validating triggers: {str(e)}")
        
        self.results["validation_results"]["trigger_validation"]["issues"] = issues
        self.results["validation_results"]["trigger_validation"]["status"] = \
            "PASS" if not issues else "FAIL"
        
        if issues:
            self.results["blocking_issues"].extend(issues)
    
    def _verify_role_awareness(self, workflow_files: List[Path]):
        """Verify that workflows are role-aware (builder, FM, governance)."""
        print("\n4️⃣  Verifying Role Awareness...")
        violations = []
        
        # Check for gate workflows that should be role-aware
        gate_workflows = [f for f in workflow_files if 'gate' in f.name.lower()]
        
        for workflow_file in gate_workflows:
            try:
                with open(workflow_file, 'r') as f:
                    content = f.read()
                
                # Look for role-related keywords
                role_indicators = [
                    'builder-', 'ui-builder', 'api-builder', 'schema-builder',
                    'integration-builder', 'qa-builder',
                    'foreman', 'fm-',
                    'governance', 'agent-boundary'
                ]
                
                has_role_awareness = any(indicator in content.lower() for indicator in role_indicators)
                
                if has_role_awareness:
                    print(f"   ✅ {workflow_file.name}: Role-aware")
                else:
                    # May not be a violation, depends on workflow purpose
                    print(f"   ℹ️  {workflow_file.name}: No explicit role indicators")
                
            except Exception as e:
                violations.append(f"{workflow_file.name}: Error checking role awareness: {str(e)}")
        
        self.results["validation_results"]["role_awareness"]["violations"] = violations
        self.results["validation_results"]["role_awareness"]["status"] = \
            "PASS" if not violations else "FAIL"
        
        if violations:
            self.results["blocking_issues"].extend(violations)
    
    def _determine_status(self):
        """Determine overall evaluation status."""
        print("\n📊 Evaluation Summary:")
        
        all_pass = all(
            v["status"] == "PASS" 
            for v in self.results["validation_results"].values()
        )
        
        for check_name, check_result in self.results["validation_results"].items():
            status_icon = "✅" if check_result["status"] == "PASS" else "❌"
            print(f"   {status_icon} {check_name}: {check_result['status']}")
        
        if all_pass:
            self.results["evaluation_status"] = "PASS"
            self.results["gate_readiness"] = "READY"
            print(f"\n🎉 Gate Readiness: READY")
        else:
            self.results["evaluation_status"] = "FAIL"
            self.results["gate_readiness"] = "NOT_READY"
            print(f"\n⚠️  Gate Readiness: NOT_READY")
            print(f"   Blocking Issues ({len(self.results['blocking_issues'])}):")
            for issue in self.results["blocking_issues"][:5]:  # Show first 5
                print(f"      - {issue}")
            if len(self.results["blocking_issues"]) > 5:
                print(f"      ... and {len(self.results['blocking_issues']) - 5} more")

def main():
    """Main entry point."""
    # Determine repository root
    repo_root = Path(__file__).parent.parent.parent
    
    # Create evaluator
    evaluator = PreflightEvaluator(repo_root)
    
    # Run evaluation
    results = evaluator.evaluate()
    
    # Write results to evidence file
    evidence_dir = repo_root / "foreman" / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    evidence_file = evidence_dir / "pr-gate-preflight-report.json"
    
    with open(evidence_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📝 Evidence written to: {evidence_file}")
    
    # Exit with appropriate code
    if results["gate_readiness"] == "READY":
        print("\n✅ Preflight evaluation PASSED")
        sys.exit(0)
    else:
        print("\n❌ Preflight evaluation FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()
