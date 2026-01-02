#!/usr/bin/env python3
"""
Tier-0 Governance Runtime Activation Validator

This script validates that Tier-0 canonical governance documents are:
1. Properly referenced in the FM agent contract (all 13 documents)
2. Present and accessible in the repository
3. Schema-valid (where applicable)
4. Not out of sync with the governance repository
5. Match the machine-readable manifest

This is a MERGE-BLOCKING check. If Tier-0 activation fails, the PR MUST NOT merge.

Version: 2.0.0 (Manifest-Driven)
Authority: Phase X - Trans-Repo Governance Runtime Activation
Status: MANDATORY (merge-blocking)

Usage:
    python scripts/validate_tier0_activation.py
"""

import os
import sys
import yaml
import json
from pathlib import Path
from typing import Dict, List, Tuple

class Tier0ActivationValidator:
    """Validates Tier-0 governance runtime activation"""
    
    MANIFEST_PATH = "governance/TIER_0_CANON_MANIFEST.json"
    EXPECTED_TIER0_COUNT = 14
    
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.errors = []
        self.warnings = []
        self.validations = []
        self.manifest = None
        
    def load_manifest(self) -> bool:
        """Load the Tier-0 canonical manifest"""
        manifest_file = self.repo_root / self.MANIFEST_PATH
        
        if not manifest_file.exists():
            self.errors.append({
                "check": "manifest_exists",
                "status": "FAIL",
                "message": f"Tier-0 manifest not found: {self.MANIFEST_PATH}"
            })
            print(f"❌ FAIL: Tier-0 manifest not found: {self.MANIFEST_PATH}")
            return False
        
        try:
            with open(manifest_file, 'r') as f:
                self.manifest = json.load(f)
            
            self.validations.append({
                "check": "manifest_exists",
                "status": "PASS",
                "message": "Tier-0 manifest loaded successfully"
            })
            print("✅ PASS: Tier-0 manifest loaded successfully")
            return True
            
        except Exception as e:
            self.errors.append({
                "check": "manifest_exists",
                "status": "FAIL",
                "message": f"Error loading manifest: {str(e)}"
            })
            print(f"❌ FAIL: Error loading manifest: {str(e)}")
            return False
        
    def validate_all(self) -> bool:
        """Run all Tier-0 validation checks"""
        print("🔒 Tier-0 Governance Runtime Activation Validator v2.0")
        print("=" * 70)
        print()
        
        success = True
        
        # Check 0: Load manifest
        if not self.load_manifest():
            success = False
            self.print_summary()
            return False
            
        # Check 1: Agent contract exists
        if not self.validate_agent_contract_exists():
            success = False
            
        # Check 2: Agent contract has Tier-0 section
        if not self.validate_tier0_section_exists():
            success = False
            
        # Check 3: Validate manifest reference in agent contract
        if not self.validate_manifest_reference():
            success = False
            
        # Check 4: Tier-0 documents are referenced (all 12)
        tier0_docs = self.extract_tier0_documents()
        if not tier0_docs:
            success = False
        elif not self.validate_tier0_count(tier0_docs):
            success = False
            
        # Check 5: Tier-0 documents match manifest
        if tier0_docs and not self.validate_documents_match_manifest(tier0_docs):
            success = False
            
        # Check 6: Tier-0 documents exist
        if tier0_docs and not self.validate_tier0_documents_exist(tier0_docs):
            success = False
            
        # Check 7: Activation requirements are declared
        if not self.validate_activation_requirements():
            success = False
            
        # Check 8: Failure handling semantics are declared
        if not self.validate_failure_handling():
            success = False
            
        # Check 9: Code review closure ratchet is declared
        if not self.validate_code_review_closure():
            success = False
        
        # Check 10: Branch protection enforcement is declared
        if not self.validate_branch_protection_enforcement():
            success = False
            
        # Print summary
        print()
        print("=" * 70)
        self.print_summary()
        
        return success
    
    def validate_agent_contract_exists(self) -> bool:
        """Validate that .agent contract file exists"""
        agent_file = self.repo_root / ".agent"
        
        if not agent_file.exists():
            self.errors.append({
                "check": "agent_contract_exists",
                "status": "FAIL",
                "message": "FM agent contract (.agent) not found"
            })
            print("❌ FAIL: FM agent contract (.agent) not found")
            return False
        
        self.validations.append({
            "check": "agent_contract_exists",
            "status": "PASS",
            "message": "FM agent contract exists"
        })
        print("✅ PASS: FM agent contract exists")
        return True
    
    def validate_tier0_section_exists(self) -> bool:
        """Validate that agent contract has tier_0_canon section"""
        agent_file = self.repo_root / ".agent"
        
        try:
            with open(agent_file, 'r') as f:
                content = f.read()
                
            # Extract YAML frontmatter
            if not content.startswith('---'):
                self.errors.append({
                    "check": "tier0_section_exists",
                    "status": "FAIL",
                    "message": "Agent contract missing YAML frontmatter"
                })
                print("❌ FAIL: Agent contract missing YAML frontmatter")
                return False
                
            parts = content.split('---', 2)
            if len(parts) < 3:
                self.errors.append({
                    "check": "tier0_section_exists",
                    "status": "FAIL",
                    "message": "Agent contract has incomplete YAML frontmatter"
                })
                print("❌ FAIL: Agent contract has incomplete YAML frontmatter")
                return False
            
            yaml_content = parts[1]
            agent_config = yaml.safe_load(yaml_content)
            
            if 'governance' not in agent_config:
                self.errors.append({
                    "check": "tier0_section_exists",
                    "status": "FAIL",
                    "message": "Agent contract missing 'governance' section"
                })
                print("❌ FAIL: Agent contract missing 'governance' section")
                return False
            
            if 'tier_0_canon' not in agent_config['governance']:
                self.errors.append({
                    "check": "tier0_section_exists",
                    "status": "FAIL",
                    "message": "Agent contract missing 'tier_0_canon' section"
                })
                print("❌ FAIL: Agent contract missing 'tier_0_canon' section")
                return False
            
            self.validations.append({
                "check": "tier0_section_exists",
                "status": "PASS",
                "message": "Tier-0 canon section exists in agent contract"
            })
            print("✅ PASS: Tier-0 canon section exists in agent contract")
            return True
            
        except Exception as e:
            self.errors.append({
                "check": "tier0_section_exists",
                "status": "FAIL",
                "message": f"Error parsing agent contract: {str(e)}"
            })
            print(f"❌ FAIL: Error parsing agent contract: {str(e)}")
            return False
    
    def validate_manifest_reference(self) -> bool:
        """Validate that agent contract references the manifest file"""
        agent_file = self.repo_root / ".agent"
        
        try:
            with open(agent_file, 'r') as f:
                content = f.read()
            
            parts = content.split('---', 2)
            yaml_content = parts[1]
            agent_config = yaml.safe_load(yaml_content)
            
            manifest_ref = agent_config.get('governance', {}).get('tier_0_canon', {}).get('manifest_file')
            
            if not manifest_ref:
                self.errors.append({
                    "check": "manifest_reference",
                    "status": "FAIL",
                    "message": "Agent contract missing manifest_file reference"
                })
                print("❌ FAIL: Agent contract missing manifest_file reference")
                return False
            
            if manifest_ref != self.MANIFEST_PATH:
                self.errors.append({
                    "check": "manifest_reference",
                    "status": "FAIL",
                    "message": f"Manifest reference mismatch: expected {self.MANIFEST_PATH}, got {manifest_ref}"
                })
                print(f"❌ FAIL: Manifest reference mismatch: expected {self.MANIFEST_PATH}, got {manifest_ref}")
                return False
            
            self.validations.append({
                "check": "manifest_reference",
                "status": "PASS",
                "message": "Agent contract references correct manifest file"
            })
            print("✅ PASS: Agent contract references correct manifest file")
            return True
            
        except Exception as e:
            self.errors.append({
                "check": "manifest_reference",
                "status": "FAIL",
                "message": f"Error checking manifest reference: {str(e)}"
            })
            print(f"❌ FAIL: Error checking manifest reference: {str(e)}")
            return False
    
    def validate_tier0_count(self, tier0_docs: List[Dict]) -> bool:
        """Validate that exactly 12 Tier-0 documents are referenced"""
        doc_count = len(tier0_docs)
        
        if doc_count != self.EXPECTED_TIER0_COUNT:
            self.errors.append({
                "check": "tier0_count",
                "status": "FAIL",
                "message": f"Expected {self.EXPECTED_TIER0_COUNT} Tier-0 documents, found {doc_count}"
            })
            print(f"❌ FAIL: Expected {self.EXPECTED_TIER0_COUNT} Tier-0 documents, found {doc_count}")
            return False
        
        self.validations.append({
            "check": "tier0_count",
            "status": "PASS",
            "message": f"Correct number of Tier-0 documents: {self.EXPECTED_TIER0_COUNT}"
        })
        print(f"✅ PASS: Correct number of Tier-0 documents: {self.EXPECTED_TIER0_COUNT}")
        return True
    
    def validate_documents_match_manifest(self, tier0_docs: List[Dict]) -> bool:
        """Validate that agent contract documents match the manifest"""
        manifest_docs = {doc['id']: doc for doc in self.manifest['tier_0_canonical_documents']}
        contract_docs = {doc.get('id'): doc for doc in tier0_docs if 'id' in doc}
        
        # Check for missing IDs in contract
        if len(contract_docs) != len(tier0_docs):
            self.errors.append({
                "check": "documents_match_manifest",
                "status": "FAIL",
                "message": "Some documents in contract missing 'id' field"
            })
            print("❌ FAIL: Some documents in contract missing 'id' field")
            return False
        
        # Check for missing or extra documents
        manifest_ids = set(manifest_docs.keys())
        contract_ids = set(contract_docs.keys())
        
        missing_ids = manifest_ids - contract_ids
        extra_ids = contract_ids - manifest_ids
        
        if missing_ids:
            self.errors.append({
                "check": "documents_match_manifest",
                "status": "FAIL",
                "message": f"Missing Tier-0 documents in contract: {', '.join(sorted(missing_ids))}"
            })
            print(f"❌ FAIL: Missing Tier-0 documents in contract: {', '.join(sorted(missing_ids))}")
            return False
        
        if extra_ids:
            self.errors.append({
                "check": "documents_match_manifest",
                "status": "FAIL",
                "message": f"Extra documents in contract (not in manifest): {', '.join(sorted(extra_ids))}"
            })
            print(f"❌ FAIL: Extra documents in contract (not in manifest): {', '.join(sorted(extra_ids))}")
            return False
        
        # Check that paths match
        mismatches = []
        for doc_id in contract_ids:
            if contract_docs[doc_id]['path'] != manifest_docs[doc_id]['path']:
                mismatches.append(f"{doc_id}: path mismatch")
        
        if mismatches:
            self.errors.append({
                "check": "documents_match_manifest",
                "status": "FAIL",
                "message": f"Document path mismatches: {', '.join(mismatches)}"
            })
            print(f"❌ FAIL: Document path mismatches: {', '.join(mismatches)}")
            return False
        
        self.validations.append({
            "check": "documents_match_manifest",
            "status": "PASS",
            "message": "All contract documents match manifest"
        })
        print("✅ PASS: All contract documents match manifest")
        return True
    
    def extract_tier0_documents(self) -> List[Dict]:
        """Extract Tier-0 document references from agent contract"""
        agent_file = self.repo_root / ".agent"
        
        try:
            with open(agent_file, 'r') as f:
                content = f.read()
            
            parts = content.split('---', 2)
            yaml_content = parts[1]
            agent_config = yaml.safe_load(yaml_content)
            
            tier0_docs = agent_config.get('governance', {}).get('tier_0_canon', {}).get('constitutional_documents', [])
            
            if not tier0_docs:
                self.errors.append({
                    "check": "tier0_documents_referenced",
                    "status": "FAIL",
                    "message": "No Tier-0 constitutional documents referenced"
                })
                print("❌ FAIL: No Tier-0 constitutional documents referenced")
                return []
            
            self.validations.append({
                "check": "tier0_documents_referenced",
                "status": "PASS",
                "message": f"{len(tier0_docs)} Tier-0 documents referenced"
            })
            print(f"✅ PASS: {len(tier0_docs)} Tier-0 documents referenced")
            return tier0_docs
            
        except Exception as e:
            self.errors.append({
                "check": "tier0_documents_referenced",
                "status": "FAIL",
                "message": f"Error extracting Tier-0 documents: {str(e)}"
            })
            print(f"❌ FAIL: Error extracting Tier-0 documents: {str(e)}")
            return []
    
    def validate_tier0_documents_exist(self, tier0_docs: List[Dict]) -> bool:
        """Validate that all referenced Tier-0 documents exist"""
        all_exist = True
        
        print()
        print("Checking Tier-0 document existence:")
        
        for doc in tier0_docs:
            doc_path = self.repo_root / doc['path']
            
            if not doc_path.exists():
                self.errors.append({
                    "check": "tier0_document_exists",
                    "status": "FAIL",
                    "path": doc['path'],
                    "message": f"Tier-0 document not found: {doc['path']}"
                })
                print(f"  ❌ FAIL: {doc['path']} (NOT FOUND)")
                all_exist = False
            else:
                self.validations.append({
                    "check": "tier0_document_exists",
                    "status": "PASS",
                    "path": doc['path'],
                    "message": f"Tier-0 document exists: {doc['path']}"
                })
                print(f"  ✅ PASS: {doc['path']}")
        
        return all_exist
    
    def validate_activation_requirements(self) -> bool:
        """Validate that activation requirements are declared"""
        agent_file = self.repo_root / ".agent"
        
        try:
            with open(agent_file, 'r') as f:
                content = f.read()
            
            parts = content.split('---', 2)
            yaml_content = parts[1]
            agent_config = yaml.safe_load(yaml_content)
            
            activation_reqs = agent_config.get('governance', {}).get('tier_0_canon', {}).get('activation_requirements', [])
            
            if not activation_reqs:
                self.errors.append({
                    "check": "activation_requirements_declared",
                    "status": "FAIL",
                    "message": "Activation requirements not declared"
                })
                print("❌ FAIL: Activation requirements not declared")
                return False
            
            self.validations.append({
                "check": "activation_requirements_declared",
                "status": "PASS",
                "message": f"{len(activation_reqs)} activation requirements declared"
            })
            print(f"✅ PASS: {len(activation_reqs)} activation requirements declared")
            return True
            
        except Exception as e:
            self.errors.append({
                "check": "activation_requirements_declared",
                "status": "FAIL",
                "message": f"Error checking activation requirements: {str(e)}"
            })
            print(f"❌ FAIL: Error checking activation requirements: {str(e)}")
            return False
    
    def validate_failure_handling(self) -> bool:
        """Validate that STOP + ESCALATE semantics are declared"""
        agent_file = self.repo_root / ".agent"
        
        try:
            with open(agent_file, 'r') as f:
                content = f.read()
            
            parts = content.split('---', 2)
            yaml_content = parts[1]
            agent_config = yaml.safe_load(yaml_content)
            
            failure_handling = agent_config.get('governance', {}).get('tier_0_canon', {}).get('failure_handling', {})
            
            required_handlers = [
                'on_tier_0_load_failure',
                'on_tier_0_validation_failure',
                'on_tier_0_reference_drift'
            ]
            
            missing_handlers = []
            for handler in required_handlers:
                if handler not in failure_handling:
                    missing_handlers.append(handler)
            
            if missing_handlers:
                self.errors.append({
                    "check": "failure_handling_declared",
                    "status": "FAIL",
                    "message": f"Missing failure handlers: {', '.join(missing_handlers)}"
                })
                print(f"❌ FAIL: Missing failure handlers: {', '.join(missing_handlers)}")
                return False
            
            # Validate each handler has required fields
            for handler_name, handler_config in failure_handling.items():
                if 'action' not in handler_config or handler_config['action'] != 'STOP':
                    self.errors.append({
                        "check": "failure_handling_declared",
                        "status": "FAIL",
                        "message": f"Handler {handler_name} missing or incorrect 'action: STOP'"
                    })
                    print(f"❌ FAIL: Handler {handler_name} missing or incorrect 'action: STOP'")
                    return False
                
                if 'escalation' not in handler_config or handler_config['escalation'] != 'MANDATORY':
                    self.errors.append({
                        "check": "failure_handling_declared",
                        "status": "FAIL",
                        "message": f"Handler {handler_name} missing or incorrect 'escalation: MANDATORY'"
                    })
                    print(f"❌ FAIL: Handler {handler_name} missing or incorrect 'escalation: MANDATORY'")
                    return False
            
            self.validations.append({
                "check": "failure_handling_declared",
                "status": "PASS",
                "message": "All failure handling semantics properly declared"
            })
            print("✅ PASS: All failure handling semantics properly declared")
            return True
            
        except Exception as e:
            self.errors.append({
                "check": "failure_handling_declared",
                "status": "FAIL",
                "message": f"Error checking failure handling: {str(e)}"
            })
            print(f"❌ FAIL: Error checking failure handling: {str(e)}")
            return False
    
    def validate_code_review_closure(self) -> bool:
        """Validate that code review closure ratchet is declared"""
        agent_file = self.repo_root / ".agent"
        
        try:
            with open(agent_file, 'r') as f:
                content = f.read()
            
            parts = content.split('---', 2)
            yaml_content = parts[1]
            agent_config = yaml.safe_load(yaml_content)
            
            code_review = agent_config.get('governance', {}).get('compliance', {}).get('code_review_closure', {})
            
            if not code_review:
                self.errors.append({
                    "check": "code_review_closure_declared",
                    "status": "FAIL",
                    "message": "Code review closure section not found"
                })
                print("❌ FAIL: Code review closure section not found")
                return False
            
            # Check required fields
            if code_review.get('required') != True:
                self.errors.append({
                    "check": "code_review_closure_declared",
                    "status": "FAIL",
                    "message": "Code review closure not marked as required"
                })
                print("❌ FAIL: Code review closure not marked as required")
                return False
            
            if code_review.get('enforcement') != 'UNBREAKABLE':
                self.errors.append({
                    "check": "code_review_closure_declared",
                    "status": "FAIL",
                    "message": "Code review closure enforcement not set to UNBREAKABLE"
                })
                print("❌ FAIL: Code review closure enforcement not set to UNBREAKABLE")
                return False
            
            # Check output requirements - more robust checking
            output_reqs = code_review.get('output_requirements', [])
            if not output_reqs:
                self.errors.append({
                    "check": "code_review_closure_declared",
                    "status": "FAIL",
                    "message": "Code review closure missing output_requirements"
                })
                print("❌ FAIL: Code review closure missing output_requirements")
                return False
            
            required_outputs = ['what_was_reviewed', 'what_changed_after_review', 'final_verdict']
            
            # Check if output_requirements is a list or dict
            if isinstance(output_reqs, list):
                # List format - check for key presence
                missing_outputs = []
                for req_output in required_outputs:
                    found = False
                    for output in output_reqs:
                        if isinstance(output, dict) and req_output in output:
                            found = True
                            break
                        elif isinstance(output, str) and req_output in output:
                            found = True
                            break
                    if not found:
                        missing_outputs.append(req_output)
            elif isinstance(output_reqs, dict):
                # Dict format - check for key presence
                missing_outputs = [req for req in required_outputs if req not in output_reqs]
            else:
                self.errors.append({
                    "check": "code_review_closure_declared",
                    "status": "FAIL",
                    "message": "Code review output_requirements has unexpected format"
                })
                print("❌ FAIL: Code review output_requirements has unexpected format")
                return False
            
            if missing_outputs:
                self.errors.append({
                    "check": "code_review_closure_declared",
                    "status": "FAIL",
                    "message": f"Missing output requirements: {', '.join(missing_outputs)}"
                })
                print(f"❌ FAIL: Missing output requirements: {', '.join(missing_outputs)}")
                return False
            
            self.validations.append({
                "check": "code_review_closure_declared",
                "status": "PASS",
                "message": "Code review closure ratchet properly declared"
            })
            print("✅ PASS: Code review closure ratchet properly declared")
            return True
            
        except Exception as e:
            self.errors.append({
                "check": "code_review_closure_declared",
                "status": "FAIL",
                "message": f"Error checking code review closure: {str(e)}"
            })
            print(f"❌ FAIL: Error checking code review closure: {str(e)}")
            return False
    
    def validate_branch_protection_enforcement(self) -> bool:
        """Validate that branch protection enforcement is declared"""
        
        try:
            # Check manifest for branch protection enforcement section
            if not self.manifest:
                self.errors.append({
                    "check": "branch_protection_enforcement_declared",
                    "status": "FAIL",
                    "message": "Manifest not loaded, cannot check branch protection enforcement"
                })
                print("❌ FAIL: Manifest not loaded")
                return False
            
            bp_enforcement = self.manifest.get('branch_protection_enforcement', {})
            
            if not bp_enforcement:
                self.errors.append({
                    "check": "branch_protection_enforcement_declared",
                    "status": "FAIL",
                    "message": "Branch protection enforcement section not found in manifest"
                })
                print("❌ FAIL: Branch protection enforcement section not found in manifest")
                return False
            
            # Check required fields
            if bp_enforcement.get('required') != True:
                self.errors.append({
                    "check": "branch_protection_enforcement_declared",
                    "status": "FAIL",
                    "message": "Branch protection enforcement not marked as required"
                })
                print("❌ FAIL: Branch protection enforcement not marked as required")
                return False
            
            if bp_enforcement.get('enforcement') != 'TIER_0_INVARIANT':
                self.errors.append({
                    "check": "branch_protection_enforcement_declared",
                    "status": "FAIL",
                    "message": "Branch protection enforcement not marked as TIER_0_INVARIANT"
                })
                print("❌ FAIL: Branch protection enforcement not marked as TIER_0_INVARIANT")
                return False
            
            # Check required_ci_checks
            required_checks = bp_enforcement.get('required_ci_checks', [])
            if not required_checks:
                self.errors.append({
                    "check": "branch_protection_enforcement_declared",
                    "status": "FAIL",
                    "message": "No required CI checks defined"
                })
                print("❌ FAIL: No required CI checks defined")
                return False
            
            # Validate each required check has necessary fields
            for check in required_checks:
                if 'id' not in check or 'check_name' not in check:
                    self.errors.append({
                        "check": "branch_protection_enforcement_declared",
                        "status": "FAIL",
                        "message": f"Required check missing id or check_name: {check}"
                    })
                    print(f"❌ FAIL: Required check missing id or check_name")
                    return False
            
            # Check failure handling
            failure_handling = bp_enforcement.get('failure_handling', {})
            required_handlers = [
                'on_missing_required_checks',
                'on_verification_failure',
                'on_enforcement_bypass_detected'
            ]
            
            for handler in required_handlers:
                if handler not in failure_handling:
                    self.errors.append({
                        "check": "branch_protection_enforcement_declared",
                        "status": "FAIL",
                        "message": f"Missing failure handler: {handler}"
                    })
                    print(f"❌ FAIL: Missing failure handler: {handler}")
                    return False
                
                handler_config = failure_handling[handler]
                if handler_config.get('action') != 'STOP':
                    self.errors.append({
                        "check": "branch_protection_enforcement_declared",
                        "status": "FAIL",
                        "message": f"Handler {handler} missing or incorrect 'action: STOP'"
                    })
                    print(f"❌ FAIL: Handler {handler} missing or incorrect 'action: STOP'")
                    return False
                
                if handler_config.get('escalation') != 'MANDATORY':
                    self.errors.append({
                        "check": "branch_protection_enforcement_declared",
                        "status": "FAIL",
                        "message": f"Handler {handler} missing or incorrect 'escalation: MANDATORY'"
                    })
                    print(f"❌ FAIL: Handler {handler} missing or incorrect 'escalation: MANDATORY'")
                    return False
            
            self.validations.append({
                "check": "branch_protection_enforcement_declared",
                "status": "PASS",
                "message": f"Branch protection enforcement properly declared ({len(required_checks)} required checks)"
            })
            print(f"✅ PASS: Branch protection enforcement properly declared ({len(required_checks)} required checks)")
            return True
            
        except Exception as e:
            self.errors.append({
                "check": "branch_protection_enforcement_declared",
                "status": "FAIL",
                "message": f"Error checking branch protection enforcement: {str(e)}"
            })
            print(f"❌ FAIL: Error checking branch protection enforcement: {str(e)}")
            return False
    
    def print_summary(self):
        """Print validation summary"""
        print("VALIDATION SUMMARY")
        print("=" * 70)
        print()
        print(f"✅ Passed: {len(self.validations)}")
        print(f"❌ Failed: {len(self.errors)}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        print()
        
        if self.errors:
            print("ERRORS:")
            for error in self.errors:
                print(f"  - {error['message']}")
            print()
        
        if self.warnings:
            print("WARNINGS:")
            for warning in self.warnings:
                print(f"  - {warning['message']}")
            print()
        
        if not self.errors:
            print("✅ ALL TIER-0 ACTIVATION CHECKS PASSED")
            print()
            print("Tier-0 governance runtime activation is VALID.")
            print("All 14 constitutional documents are properly activated.")
            print("Branch protection enforcement is declared.")
            print("This PR may proceed to merge (subject to other gates).")
        else:
            print("❌ TIER-0 ACTIVATION FAILED")
            print()
            print("CATASTROPHIC: Tier-0 governance is not properly activated.")
            print(f"Target: 14/14 Tier-0 documents + branch protection enforcement")
            print(f"Status: INCOMPLETE or INVALID")
            print()
            print("This PR is BLOCKED from merge until all errors are resolved.")
            print()
            print("ESCALATION REQUIRED: Johan Ras must be notified.")

def main():
    """Main entry point"""
    repo_root = os.getcwd()
    
    validator = Tier0ActivationValidator(repo_root)
    success = validator.validate_all()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
