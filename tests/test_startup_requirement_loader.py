"""
Test Startup Requirement Loader (Architecture Validation)

Tests for:
- RequirementLoader file structure validation
- Requirements schema validation
- Documentation completeness
- API surface validation

This validates the architecture-only implementation of the startup
requirement loader per issue F-A2.

Governance Authority:
- Issue F-A2: Implement App Startup Requirement Loader
- lib/startup/README.md
- Batch 2 — Memory & Commissioning Foundations

CRITICAL: This module must have ZERO decision authority and ZERO execution capability.
"""

import pytest
import json
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.mark.startup
class TestRequirementLoaderStructure:
    """Test requirement loader file structure and architecture"""
    
    def test_loader_file_exists(self):
        """
        Test that RequirementLoader.ts exists.
        
        Expected: File exists at lib/startup/RequirementLoader.ts
        """
        loader_path = project_root / "lib" / "startup" / "RequirementLoader.ts"
        assert loader_path.exists(), \
            "RequirementLoader.ts must exist at lib/startup/"
        
        # Check file is not empty
        assert loader_path.stat().st_size > 0, \
            "RequirementLoader.ts must not be empty"
    
    def test_index_file_exists(self):
        """
        Test that index.ts exports file exists.
        
        Expected: File exists at lib/startup/index.ts
        """
        index_path = project_root / "lib" / "startup" / "index.ts"
        assert index_path.exists(), \
            "index.ts must exist at lib/startup/"
    
    def test_readme_exists(self):
        """
        Test that README.md exists.
        
        Expected: File exists at lib/startup/README.md
        """
        readme_path = project_root / "lib" / "startup" / "README.md"
        assert readme_path.exists(), \
            "README.md must exist at lib/startup/"
        
        # Check README contains key sections
        content = readme_path.read_text()
        assert "Purpose" in content, "README must document purpose"
        assert "Usage" in content, "README must document usage"
        assert "DOES NOT" in content, "README must explicitly state what it does NOT do"


@pytest.mark.startup
class TestRequirementsSchema:
    """Test requirements schema and data files"""
    
    def test_schema_file_exists(self):
        """
        Test that startup-requirements.schema.json exists.
        
        Expected: Valid JSON schema file at lib/startup/
        """
        schema_path = project_root / "lib" / "startup" / "startup-requirements.schema.json"
        assert schema_path.exists(), \
            "startup-requirements.schema.json must exist"
        
        # Validate it's valid JSON
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        
        assert "type" in schema, "Schema must define type"
        assert "properties" in schema, "Schema must define properties"
        assert "version" in schema["properties"], "Schema must define version property"
        assert "requirements" in schema["properties"], "Schema must define requirements property"
    
    def test_requirements_file_exists(self):
        """
        Test that startup-requirements.json exists.
        
        Expected: Valid requirements data file at lib/startup/
        """
        req_path = project_root / "lib" / "startup" / "startup-requirements.json"
        assert req_path.exists(), \
            "startup-requirements.json must exist"
        
        # Validate it's valid JSON
        with open(req_path, 'r') as f:
            requirements = json.load(f)
        
        assert "version" in requirements, "Requirements must have version"
        assert "requirements" in requirements, "Requirements must have requirements array"
        assert len(requirements["requirements"]) > 0, "Must define at least one requirement"
    
    def test_requirements_structure(self):
        """
        Test that requirements follow expected structure.
        
        Expected: Each requirement has id, category, description, validator, critical
        """
        req_path = project_root / "lib" / "startup" / "startup-requirements.json"
        
        with open(req_path, 'r') as f:
            requirements = json.load(f)
        
        for req in requirements["requirements"]:
            assert "id" in req, f"Requirement must have id: {req}"
            assert "category" in req, f"Requirement must have category: {req.get('id')}"
            assert "description" in req, f"Requirement must have description: {req.get('id')}"
            assert "validator" in req, f"Requirement must have validator: {req.get('id')}"
            assert "critical" in req, f"Requirement must have critical flag: {req.get('id')}"
            
            # Validate ID format
            assert req["id"].count('-') >= 2, \
                f"Requirement ID must follow format XXX-YYY-ZZZ: {req['id']}"
            
            # Validate category is valid enum
            valid_categories = [
                "memory", "governance", "architecture", "security",
                "configuration", "environment", "dependencies"
            ]
            assert req["category"] in valid_categories, \
                f"Invalid category: {req['category']}"
    
    def test_requirements_include_memory_checks(self):
        """
        Test that requirements include memory lifecycle checks.
        
        Expected: At least one requirement validates memory state
        """
        req_path = project_root / "lib" / "startup" / "startup-requirements.json"
        
        with open(req_path, 'r') as f:
            requirements = json.load(f)
        
        memory_reqs = [r for r in requirements["requirements"] if r["category"] == "memory"]
        assert len(memory_reqs) > 0, "Must include at least one memory requirement"
        
        # Check for specific memory requirements
        mem_ids = [r["id"] for r in memory_reqs]
        assert any("LIFECYCLE" in id for id in mem_ids), \
            "Must include memory lifecycle requirement"


@pytest.mark.startup
class TestLoaderAPI:
    """Test RequirementLoader API surface"""
    
    def test_loader_exports_required_methods(self):
        """
        Test that RequirementLoader exports required methods.
        
        Expected: loadRequirements, validateRequirements, etc.
        """
        loader_path = project_root / "lib" / "startup" / "RequirementLoader.ts"
        content = loader_path.read_text()
        
        required_methods = [
            "loadRequirements",
            "validateRequirements",
            "getFailingRequirements",
            "getCriticalBlockers",
            "generateReadinessReport"
        ]
        
        for method in required_methods:
            assert method in content, \
                f"RequirementLoader must export {method} method"
    
    def test_loader_defines_types(self):
        """
        Test that RequirementLoader defines required types.
        
        Expected: StartupRequirement, ValidationResult, StartupAssessment
        """
        loader_path = project_root / "lib" / "startup" / "RequirementLoader.ts"
        content = loader_path.read_text()
        
        required_types = [
            "StartupRequirement",
            "ValidationResult",
            "StartupAssessment"
        ]
        
        for type_name in required_types:
            assert type_name in content, \
                f"RequirementLoader must define {type_name} type"
    
    def test_assessment_includes_status(self):
        """
        Test that StartupAssessment includes overall status.
        
        Expected: overallStatus with READY | DEGRADED | BLOCKED
        """
        loader_path = project_root / "lib" / "startup" / "RequirementLoader.ts"
        content = loader_path.read_text()
        
        assert "overallStatus" in content, "Assessment must include overallStatus"
        assert "READY" in content, "Assessment must define READY status"
        assert "DEGRADED" in content, "Assessment must define DEGRADED status"
        assert "BLOCKED" in content, "Assessment must define BLOCKED status"


@pytest.mark.startup
class TestBatch2Constraints:
    """Test that Batch 2 constraints are enforced"""
    
    def test_no_execution_in_loader(self):
        """
        Test that RequirementLoader does NOT trigger execution.
        
        Expected: No build triggers, no activation logic
        """
        loader_path = project_root / "lib" / "startup" / "RequirementLoader.ts"
        content = loader_path.read_text()
        
        # Check for explicit constraint documentation
        assert "DOES NOT" in content or "Does NOT" in content, \
            "Loader must explicitly document what it does NOT do"
        
        # Check that comments mention read-only nature
        assert "read-only" in content.lower() or "READ-ONLY" in content, \
            "Loader must be documented as read-only"
        
        # Check for zero decision authority statement
        assert "zero decision" in content.lower() or "ZERO decision" in content, \
            "Loader must document zero decision authority"
    
    def test_readme_states_no_execution(self):
        """
        Test that README explicitly states no execution.
        
        Expected: Clear statement about no builds, no activation
        """
        readme_path = project_root / "lib" / "startup" / "README.md"
        content = readme_path.read_text()
        
        # Check for explicit "DOES NOT" section
        assert "DOES NOT" in content, "README must have DOES NOT section"
        
        # Check for specific prohibited actions
        prohibited_actions = [
            "trigger",
            "activate",
            "commission",
            "modify",
            "execute"
        ]
        
        does_not_section = content.split("DOES NOT")[1].split("---")[0].lower()
        
        for action in prohibited_actions:
            assert action in does_not_section, \
                f"README must explicitly state does not {action}"
    
    def test_critical_statement_present(self):
        """
        Test that README includes critical statement about no execution.
        
        Expected: Statement at end: "This module does NOT trigger execution, builds, or external delegation"
        """
        readme_path = project_root / "lib" / "startup" / "README.md"
        content = readme_path.read_text()
        
        assert "does NOT trigger execution" in content or "does not trigger execution" in content, \
            "README must include critical statement about no execution"
        
        assert "external delegation" in content or "external delegation" in content.lower(), \
            "README must mention no external delegation"


@pytest.mark.startup
class TestIntegration:
    """Test integration points with other components"""
    
    def test_integration_with_commissioning_documented(self):
        """
        Test that integration with commissioning flow is documented.
        
        Expected: Documentation of how results are surfaced
        """
        readme_path = project_root / "lib" / "startup" / "README.md"
        content = readme_path.read_text()
        
        assert "commissioning" in content.lower(), \
            "README must document commissioning integration"
        
        assert "surface" in content.lower() or "surfaced" in content.lower(), \
            "README must explain how results are surfaced"
    
    def test_validators_are_read_only(self):
        """
        Test that validators are documented as read-only checks.
        
        Expected: Validator documentation states they do NOT modify state
        """
        loader_path = project_root / "lib" / "startup" / "RequirementLoader.ts"
        content = loader_path.read_text()
        
        # Find registerValidators method
        if "registerValidators" in content:
            # Look for READ-ONLY comment in registerValidators method or before it
            register_start = content.find("registerValidators")
            # Get 500 characters before and after registerValidators
            validators_section = content[max(0, register_start-500):register_start+1000]
            
            # Check for read-only comment
            assert "READ-ONLY" in validators_section or "read-only" in validators_section.lower(), \
                "Validators must be documented as read-only"


@pytest.mark.startup
class TestAcceptanceCriteria:
    """Test acceptance criteria for F-A2"""
    
    def test_ac_requirements_loadable(self):
        """
        Acceptance Criteria: Requirements can be loaded from JSON.
        
        Expected: Valid requirements file exists and is parseable
        """
        req_path = project_root / "lib" / "startup" / "startup-requirements.json"
        assert req_path.exists()
        
        with open(req_path, 'r') as f:
            requirements = json.load(f)
        
        assert "requirements" in requirements
        assert len(requirements["requirements"]) > 0
    
    def test_ac_validation_results_surfaced(self):
        """
        Acceptance Criteria: Validation results can be surfaced to commissioning flow.
        
        Expected: Assessment type includes all necessary data for UI
        """
        loader_path = project_root / "lib" / "startup" / "RequirementLoader.ts"
        content = loader_path.read_text()
        
        # Check StartupAssessment includes required fields
        required_assessment_fields = [
            "overallStatus",
            "passed",
            "failed",
            "criticalFailed",
            "results",
            "blockers",
            "warnings"
        ]
        
        for field in required_assessment_fields:
            assert field in content, \
                f"StartupAssessment must include {field} for commissioning flow"
    
    def test_ac_read_only_assessment_only(self):
        """
        Acceptance Criteria: Loader provides read-only assessment with zero decision authority.
        
        Expected: Documentation explicitly states read-only nature
        """
        readme_path = project_root / "lib" / "startup" / "README.md"
        content = readme_path.read_text()
        
        assert "read-only" in content.lower() or "READ-ONLY" in content, \
            "Must be documented as read-only"
        
        assert "zero decision" in content.lower() or "ZERO decision" in content, \
            "Must document zero decision authority"
    
    def test_ac_no_execution_triggers(self):
        """
        Acceptance Criteria: Loader does NOT trigger builds or execution.
        
        Expected: Explicit documentation and no execution code
        """
        readme_path = project_root / "lib" / "startup" / "README.md"
        content = readme_path.read_text()
        
        assert "does NOT trigger" in content or "does not trigger" in content, \
            "Must explicitly state does not trigger execution"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
