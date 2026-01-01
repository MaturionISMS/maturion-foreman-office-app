#!/usr/bin/env python3
"""
Code Review Closure Artifact Validator

Validates that code review closure artifact exists and meets all requirements.

This is a MERGE-BLOCKING check. If code review closure is missing or invalid, 
the PR MUST NOT merge.

Version: 1.0.0
Authority: .agent governance.compliance.code_review_closure
Status: MANDATORY (merge-blocking)

Usage:
    python scripts/validate_code_review_closure.py [artifact_path]
    
    If no artifact_path is provided, searches for code-review-closure.json
    in the repository root.
"""

import os
import sys
import json
import jsonschema
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class CodeReviewClosureValidator:
    """Validates code review closure artifacts"""
    
    SCHEMA_PATH = "governance/schemas/code-review-closure-schema.json"
    DEFAULT_ARTIFACT_NAME = "code-review-closure.json"
    
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.errors = []
        self.warnings = []
        self.validations = []
        self.schema = None
        
    def load_schema(self) -> bool:
        """Load the code review closure schema"""
        schema_file = self.repo_root / self.SCHEMA_PATH
        
        if not schema_file.exists():
            self.errors.append({
                "check": "schema_exists",
                "status": "FAIL",
                "message": f"Code review closure schema not found: {self.SCHEMA_PATH}"
            })
            print(f"❌ FAIL: Schema not found: {self.SCHEMA_PATH}")
            return False
        
        try:
            with open(schema_file, 'r') as f:
                self.schema = json.load(f)
            
            self.validations.append({
                "check": "schema_exists",
                "status": "PASS",
                "message": "Code review closure schema loaded successfully"
            })
            print("✅ PASS: Schema loaded successfully")
            return True
            
        except Exception as e:
            self.errors.append({
                "check": "schema_exists",
                "status": "FAIL",
                "message": f"Error loading schema: {str(e)}"
            })
            print(f"❌ FAIL: Error loading schema: {str(e)}")
            return False
    
    def find_artifact(self, explicit_path: str = None) -> Tuple[bool, str]:
        """Find code review closure artifact"""
        if explicit_path:
            artifact_path = Path(explicit_path)
            if not artifact_path.is_absolute():
                artifact_path = self.repo_root / artifact_path
        else:
            # Search for artifact in repo root
            artifact_path = self.repo_root / self.DEFAULT_ARTIFACT_NAME
        
        if not artifact_path.exists():
            self.errors.append({
                "check": "artifact_exists",
                "status": "FAIL",
                "message": f"Code review closure artifact not found: {artifact_path}"
            })
            print(f"❌ FAIL: Artifact not found: {artifact_path}")
            return False, str(artifact_path)
        
        self.validations.append({
            "check": "artifact_exists",
            "status": "PASS",
            "message": f"Code review closure artifact found: {artifact_path}"
        })
        print(f"✅ PASS: Artifact found: {artifact_path}")
        return True, str(artifact_path)
    
    def validate_artifact_json(self, artifact_path: str) -> Tuple[bool, Dict]:
        """Validate artifact is valid JSON"""
        try:
            with open(artifact_path, 'r') as f:
                artifact = json.load(f)
            
            self.validations.append({
                "check": "artifact_valid_json",
                "status": "PASS",
                "message": "Artifact is valid JSON"
            })
            print("✅ PASS: Artifact is valid JSON")
            return True, artifact
            
        except json.JSONDecodeError as e:
            self.errors.append({
                "check": "artifact_valid_json",
                "status": "FAIL",
                "message": f"Artifact is not valid JSON: {str(e)}"
            })
            print(f"❌ FAIL: Artifact is not valid JSON: {str(e)}")
            return False, {}
        except Exception as e:
            self.errors.append({
                "check": "artifact_valid_json",
                "status": "FAIL",
                "message": f"Error reading artifact: {str(e)}"
            })
            print(f"❌ FAIL: Error reading artifact: {str(e)}")
            return False, {}
    
    def validate_schema_compliance(self, artifact: Dict) -> bool:
        """Validate artifact against schema"""
        try:
            jsonschema.validate(instance=artifact, schema=self.schema)
            
            self.validations.append({
                "check": "schema_compliance",
                "status": "PASS",
                "message": "Artifact complies with schema"
            })
            print("✅ PASS: Artifact complies with schema")
            return True
            
        except jsonschema.ValidationError as e:
            self.errors.append({
                "check": "schema_compliance",
                "status": "FAIL",
                "message": f"Schema validation failed: {e.message}",
                "path": list(e.absolute_path)
            })
            print(f"❌ FAIL: Schema validation failed: {e.message}")
            print(f"   Path: {'/'.join(str(p) for p in e.absolute_path)}")
            return False
        except Exception as e:
            self.errors.append({
                "check": "schema_compliance",
                "status": "FAIL",
                "message": f"Error validating schema: {str(e)}"
            })
            print(f"❌ FAIL: Error validating schema: {str(e)}")
            return False
    
    def validate_immutability(self, artifact: Dict) -> bool:
        """Validate artifact is marked immutable"""
        if not artifact.get('immutable'):
            self.errors.append({
                "check": "immutability",
                "status": "FAIL",
                "message": "Artifact not marked immutable"
            })
            print("❌ FAIL: Artifact not marked immutable")
            return False
        
        self.validations.append({
            "check": "immutability",
            "status": "PASS",
            "message": "Artifact is immutable"
        })
        print("✅ PASS: Artifact is immutable")
        return True
    
    def validate_verdict(self, artifact: Dict) -> bool:
        """Validate final verdict is present and complete"""
        verdict = artifact.get('final_verdict', {})
        
        if not verdict:
            self.errors.append({
                "check": "verdict_present",
                "status": "FAIL",
                "message": "Final verdict missing"
            })
            print("❌ FAIL: Final verdict missing")
            return False
        
        status = verdict.get('status')
        reasoning = verdict.get('reasoning', '')
        
        if status not in ['APPROVED', 'REQUIRES_CHANGES']:
            self.errors.append({
                "check": "verdict_valid",
                "status": "FAIL",
                "message": f"Invalid verdict status: {status}"
            })
            print(f"❌ FAIL: Invalid verdict status: {status}")
            return False
        
        if len(reasoning) < 20:
            self.errors.append({
                "check": "verdict_reasoning",
                "status": "FAIL",
                "message": "Verdict reasoning too short (minimum 20 characters)"
            })
            print("❌ FAIL: Verdict reasoning too short")
            return False
        
        self.validations.append({
            "check": "verdict_complete",
            "status": "PASS",
            "message": f"Final verdict: {status}"
        })
        print(f"✅ PASS: Final verdict: {status}")
        return True
    
    def validate_reviewed_files(self, artifact: Dict) -> bool:
        """Validate that at least one file was reviewed"""
        reviewed = artifact.get('what_was_reviewed', {})
        files = reviewed.get('files', [])
        
        if not files or len(files) == 0:
            self.errors.append({
                "check": "files_reviewed",
                "status": "FAIL",
                "message": "No files listed in what_was_reviewed"
            })
            print("❌ FAIL: No files listed in what_was_reviewed")
            return False
        
        self.validations.append({
            "check": "files_reviewed",
            "status": "PASS",
            "message": f"{len(files)} file(s) reviewed"
        })
        print(f"✅ PASS: {len(files)} file(s) reviewed")
        return True
    
    def validate_artifact_type(self, artifact: Dict) -> bool:
        """Validate artifact type is correct"""
        metadata = artifact.get('artifact_metadata', {})
        artifact_type = metadata.get('artifact_type')
        
        if artifact_type != 'code_review_closure':
            self.errors.append({
                "check": "artifact_type",
                "status": "FAIL",
                "message": f"Invalid artifact type: {artifact_type}"
            })
            print(f"❌ FAIL: Invalid artifact type: {artifact_type}")
            return False
        
        self.validations.append({
            "check": "artifact_type",
            "status": "PASS",
            "message": "Artifact type is correct"
        })
        print("✅ PASS: Artifact type is correct")
        return True
    
    def validate_all(self, artifact_path: str = None) -> bool:
        """Run all validation checks"""
        print("🔒 Code Review Closure Artifact Validator v1.0")
        print("=" * 70)
        print()
        
        success = True
        
        # Check 1: Load schema
        if not self.load_schema():
            success = False
            self.print_summary()
            return False
        
        print()
        
        # Check 2: Find artifact
        found, path = self.find_artifact(artifact_path)
        if not found:
            success = False
            self.print_summary()
            return False
        
        print()
        
        # Check 3: Validate JSON
        valid_json, artifact = self.validate_artifact_json(path)
        if not valid_json:
            success = False
            self.print_summary()
            return False
        
        print()
        
        # Check 4: Schema compliance
        if not self.validate_schema_compliance(artifact):
            success = False
        
        print()
        
        # Check 5: Artifact type
        if not self.validate_artifact_type(artifact):
            success = False
        
        print()
        
        # Check 6: Immutability
        if not self.validate_immutability(artifact):
            success = False
        
        print()
        
        # Check 7: Reviewed files
        if not self.validate_reviewed_files(artifact):
            success = False
        
        print()
        
        # Check 8: Final verdict
        if not self.validate_verdict(artifact):
            success = False
        
        print()
        self.print_summary()
        return success
    
    def print_summary(self):
        """Print validation summary"""
        print("=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)
        print()
        
        if self.validations:
            print(f"✅ Passed Checks: {len(self.validations)}")
            for v in self.validations:
                print(f"   - {v['check']}: {v['message']}")
            print()
        
        if self.warnings:
            print(f"⚠️  Warnings: {len(self.warnings)}")
            for w in self.warnings:
                print(f"   - {w['check']}: {w['message']}")
            print()
        
        if self.errors:
            print(f"❌ Failed Checks: {len(self.errors)}")
            for e in self.errors:
                print(f"   - {e['check']}: {e['message']}")
            print()
        
        if self.errors:
            print("RESULT: ❌ VALIDATION FAILED")
            print()
            print("Code review closure artifact is invalid or missing.")
            print("This is a MERGE-BLOCKING failure.")
            print()
            print("Required actions:")
            print("1. Create code-review-closure.json in repository root")
            print("2. Follow schema: governance/schemas/code-review-closure-schema.json")
            print("3. Use template: governance/templates/code-review-closure-template.json")
            print("4. Ensure all required fields are present")
            print("5. Re-run validation")
        else:
            print("RESULT: ✅ VALIDATION PASSED")
            print()
            print("Code review closure artifact is valid.")
            print("All governance requirements met.")
        
        print("=" * 70)


def main():
    """Main entry point"""
    repo_root = os.getcwd()
    artifact_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    validator = CodeReviewClosureValidator(repo_root)
    success = validator.validate_all(artifact_path)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
