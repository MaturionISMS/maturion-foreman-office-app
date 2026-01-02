#!/usr/bin/env python3
"""
Tier-0 Consistency Validator

PREVENTS: Adding Tier-0 documents without updating all dependent systems
PURPOSE: Catch Tier-0 count mismatches BEFORE they reach CI

This script ensures:
1. TIER_0_CANON_MANIFEST.json count matches validation script expectation
2. .agent file tier_0_canon count matches manifest
3. ForemanApp-agent.md references match manifest
4. All Tier-0 IDs are consistent across files

RUN THIS: Before committing any Tier-0 changes

Author: FMRepoBuilder
Created: 2026-01-02 (Response to PR #338 failures)
"""

import json
import yaml
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

class Tier0ConsistencyValidator:
    """Validates Tier-0 document consistency across all files"""
    
    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root)
        self.errors = []
        self.warnings = []
        
        # File paths
        self.manifest_path = self.repo_root / "governance/TIER_0_CANON_MANIFEST.json"
        self.agent_yaml_path = self.repo_root / ".agent"
        self.agent_md_path = self.repo_root / ".github/agents/ForemanApp-agent.md"
        self.validation_script_path = self.repo_root / "scripts/validate_tier0_activation.py"
        self.workflow_path = self.repo_root / ".github/workflows/tier0-activation-gate.yml"
        
    def validate_all(self) -> bool:
        """Run all consistency checks"""
        print("=" * 70)
        print("TIER-0 CONSISTENCY VALIDATOR")
        print("=" * 70)
        print()
        
        success = True
        
        # Load manifest
        manifest_count, manifest_ids = self.load_manifest()
        if manifest_count is None:
            return False
            
        # Check validation script expectation
        script_count = self.get_validation_script_expectation()
        if script_count is None:
            success = False
        elif script_count != manifest_count:
            self.errors.append(
                f"MISMATCH: Validation script expects {script_count} documents, "
                f"manifest has {manifest_count} documents"
            )
            print(f"❌ FAIL: Validation script expects {script_count}, manifest has {manifest_count}")
            success = False
        else:
            print(f"✅ PASS: Validation script matches manifest ({manifest_count} documents)")
            
        # Check .agent file
        agent_count, agent_ids = self.get_agent_yaml_tier0_docs()
        if agent_count is None:
            success = False
        elif agent_count != manifest_count:
            self.errors.append(
                f"MISMATCH: .agent file has {agent_count} documents, "
                f"manifest has {manifest_count} documents"
            )
            print(f"❌ FAIL: .agent has {agent_count}, manifest has {manifest_count}")
            success = False
        else:
            print(f"✅ PASS: .agent file matches manifest ({manifest_count} documents)")
            
        # Check .agent IDs match manifest IDs
        if agent_ids and manifest_ids:
            missing_in_agent = manifest_ids - agent_ids
            extra_in_agent = agent_ids - manifest_ids
            
            if missing_in_agent:
                self.errors.append(f"Missing in .agent: {', '.join(sorted(missing_in_agent))}")
                print(f"❌ FAIL: .agent missing IDs: {', '.join(sorted(missing_in_agent))}")
                success = False
            
            if extra_in_agent:
                self.errors.append(f"Extra in .agent: {', '.join(sorted(extra_in_agent))}")
                print(f"❌ FAIL: .agent has extra IDs: {', '.join(sorted(extra_in_agent))}")
                success = False
                
            if not missing_in_agent and not extra_in_agent:
                print(f"✅ PASS: .agent IDs match manifest perfectly")
                
        # Check ForemanApp-agent.md references
        md_references = self.check_markdown_references(manifest_count)
        if not md_references:
            success = False
            
        # Check workflow references
        workflow_refs = self.check_workflow_references(manifest_count)
        if not workflow_refs:
            success = False
            
        # Check manifest version consistency
        if not self.check_manifest_version_consistency():
            success = False
            
        # Print summary
        print()
        print("=" * 70)
        print("SUMMARY")
        print("=" * 70)
        
        if success:
            print("✅ ALL TIER-0 CONSISTENCY CHECKS PASSED")
            print()
            print(f"Tier-0 Count: {manifest_count} documents")
            print("All files are synchronized.")
            print()
            print("Safe to commit Tier-0 changes.")
        else:
            print("❌ TIER-0 CONSISTENCY CHECK FAILED")
            print()
            print("ERRORS:")
            for error in self.errors:
                print(f"  - {error}")
            print()
            print("⛔ DO NOT COMMIT until all errors are resolved")
            print()
            print("REQUIRED ACTIONS:")
            print("  1. Review errors above")
            print("  2. Update all files to match manifest")
            print("  3. Run this script again")
            print("  4. Commit only when all checks pass")
            
        return success
        
    def load_manifest(self) -> Tuple[int, Set[str]]:
        """Load manifest and return document count and IDs"""
        if not self.manifest_path.exists():
            self.errors.append(f"Manifest not found: {self.manifest_path}")
            print(f"❌ FAIL: Manifest not found")
            return None, None
            
        try:
            with open(self.manifest_path) as f:
                manifest = json.load(f)
                
            docs = manifest.get('tier_0_canonical_documents', [])
            doc_count = len(docs)
            doc_ids = {doc['id'] for doc in docs}
            
            print(f"📄 Manifest: {doc_count} Tier-0 documents")
            return doc_count, doc_ids
            
        except Exception as e:
            self.errors.append(f"Error loading manifest: {e}")
            print(f"❌ FAIL: Error loading manifest: {e}")
            return None, None
            
    def get_validation_script_expectation(self) -> int:
        """Get expected Tier-0 count from validation script"""
        if not self.validation_script_path.exists():
            self.errors.append("Validation script not found")
            print("❌ FAIL: Validation script not found")
            return None
            
        try:
            with open(self.validation_script_path) as f:
                content = f.read()
                
            # Find EXPECTED_TIER0_COUNT = N
            match = re.search(r'EXPECTED_TIER0_COUNT\s*=\s*(\d+)', content)
            if not match:
                self.errors.append("Could not find EXPECTED_TIER0_COUNT in validation script")
                print("❌ FAIL: EXPECTED_TIER0_COUNT not found in validation script")
                return None
                
            count = int(match.group(1))
            print(f"📄 Validation script expects: {count} documents")
            return count
            
        except Exception as e:
            self.errors.append(f"Error reading validation script: {e}")
            print(f"❌ FAIL: Error reading validation script: {e}")
            return None
            
    def get_agent_yaml_tier0_docs(self) -> Tuple[int, Set[str]]:
        """Get Tier-0 document count and IDs from .agent file"""
        if not self.agent_yaml_path.exists():
            self.errors.append(".agent file not found")
            print("❌ FAIL: .agent file not found")
            return None, None
            
        try:
            with open(self.agent_yaml_path) as f:
                content = f.read()
                
            # Extract YAML frontmatter
            if not content.startswith('---'):
                self.errors.append(".agent file missing YAML frontmatter")
                print("❌ FAIL: .agent missing YAML frontmatter")
                return None, None
                
            parts = content.split('---', 2)
            if len(parts) < 3:
                self.errors.append(".agent file has incomplete YAML frontmatter")
                print("❌ FAIL: .agent incomplete YAML frontmatter")
                return None, None
                
            yaml_content = parts[1]
            config = yaml.safe_load(yaml_content)
            
            docs = config.get('governance', {}).get('tier_0_canon', {}).get('constitutional_documents', [])
            doc_count = len(docs)
            doc_ids = {doc['id'] for doc in docs if 'id' in doc}
            
            print(f"📄 .agent file: {doc_count} Tier-0 documents")
            return doc_count, doc_ids
            
        except Exception as e:
            self.errors.append(f"Error reading .agent file: {e}")
            print(f"❌ FAIL: Error reading .agent file: {e}")
            return None, None
            
    def check_markdown_references(self, expected_count: int) -> bool:
        """Check ForemanApp-agent.md references correct count"""
        if not self.agent_md_path.exists():
            self.warnings.append("ForemanApp-agent.md not found")
            print("⚠️  WARN: ForemanApp-agent.md not found")
            return True  # Not critical
            
        try:
            with open(self.agent_md_path) as f:
                content = f.read()
                
            # Find references to Tier-0 document count
            patterns = [
                r'ALL (\d+) Tier-0',
                r'all (\d+) Tier-0',
                r'(\d+) Tier-0 documents',
            ]
            
            mismatches = []
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    count = int(match)
                    if count != expected_count:
                        mismatches.append(f"Found '{match}' (should be {expected_count})")
                        
            if mismatches:
                self.errors.append(f"ForemanApp-agent.md has incorrect references: {', '.join(mismatches)}")
                print(f"❌ FAIL: ForemanApp-agent.md references incorrect count")
                return False
            else:
                print(f"✅ PASS: ForemanApp-agent.md references {expected_count} documents")
                return True
                
        except Exception as e:
            self.warnings.append(f"Error checking markdown: {e}")
            print(f"⚠️  WARN: Error checking markdown: {e}")
            return True  # Not critical
            
    def check_workflow_references(self, expected_count: int) -> bool:
        """Check workflow file references correct count"""
        if not self.workflow_path.exists():
            self.warnings.append("Workflow file not found")
            print("⚠️  WARN: Workflow file not found")
            return True  # Not critical
            
        try:
            with open(self.workflow_path) as f:
                content = f.read()
                
            # Find references to document count
            patterns = [
                r'\((\d+) documents\)',
                r'Required: (\d+) Tier-0',
                r'all (\d+) constitutional',
            ]
            
            mismatches = []
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    count = int(match)
                    if count != expected_count:
                        mismatches.append(f"Found '{match}' (should be {expected_count})")
                        
            if mismatches:
                self.errors.append(f"Workflow has incorrect references: {', '.join(mismatches)}")
                print(f"❌ FAIL: Workflow references incorrect count")
                return False
            else:
                print(f"✅ PASS: Workflow references {expected_count} documents")
                return True
                
        except Exception as e:
            self.warnings.append(f"Error checking workflow: {e}")
            print(f"⚠️  WARN: Error checking workflow: {e}")
            return True  # Not critical
            
    def check_manifest_version_consistency(self) -> bool:
        """Check manifest version is consistent between files"""
        try:
            # Get version from manifest
            with open(self.manifest_path) as f:
                manifest = json.load(f)
            manifest_version = manifest.get('version')
            
            # Get version from .agent
            with open(self.agent_yaml_path) as f:
                content = f.read()
            parts = content.split('---', 2)
            yaml_content = parts[1]
            config = yaml.safe_load(yaml_content)
            agent_version = config.get('governance', {}).get('tier_0_canon', {}).get('manifest_version')
            
            if manifest_version != agent_version:
                self.errors.append(
                    f"Version mismatch: manifest={manifest_version}, .agent={agent_version}"
                )
                print(f"❌ FAIL: Manifest version mismatch (manifest={manifest_version}, .agent={agent_version})")
                return False
            else:
                print(f"✅ PASS: Manifest version consistent ({manifest_version})")
                return True
                
        except Exception as e:
            self.warnings.append(f"Error checking version consistency: {e}")
            print(f"⚠️  WARN: Error checking version: {e}")
            return True  # Not critical

def main():
    """Main entry point"""
    import sys
    
    validator = Tier0ConsistencyValidator()
    success = validator.validate_all()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
