"""
Tests for Build Node Inspector

Tests the BUILD_NODE_INSPECTION_MODEL.md (G-C9) implementation.
"""

import pytest
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'fm' / 'orchestration'))

from build_node_inspector import BuildNodeInspector, create_inspector


class TestBuildNodeInspector:
    """Test suite for BuildNodeInspector"""
    
    @pytest.fixture
    def inspector(self, tmp_path):
        """Create inspector instance with temp repo root"""
        return BuildNodeInspector(repo_root=tmp_path)
    
    def test_inspector_initialization(self, tmp_path):
        """Test inspector initializes correctly"""
        inspector = BuildNodeInspector(repo_root=tmp_path)
        assert inspector.repo_root == tmp_path
        assert inspector.architecture_dir == tmp_path / "architecture"
        assert inspector.governance_dir == tmp_path / "governance"
    
    def test_create_inspector_factory(self):
        """Test factory function creates inspector"""
        inspector = create_inspector()
        assert isinstance(inspector, BuildNodeInspector)
        assert inspector.repo_root is not None
    
    def test_inspect_node_invalid_type(self, inspector):
        """Test inspection with invalid node type raises ValueError"""
        with pytest.raises(ValueError, match="Invalid node_type"):
            inspector.inspect_node("invalid_type", "test-id")
    
    def test_inspect_node_invalid_depth(self, inspector):
        """Test inspection with invalid depth raises ValueError"""
        with pytest.raises(ValueError, match="Invalid depth"):
            inspector.inspect_node("task", "test-id", depth=0)
        
        with pytest.raises(ValueError, match="Invalid depth"):
            inspector.inspect_node("task", "test-id", depth=6)
    
    def test_inspect_node_level_1(self, inspector):
        """Test Level 1 inspection (quick status)"""
        result = inspector.inspect_node("task", "test-task", depth=1)
        
        # Level 1 fields always present
        assert result["node_id"] == "test-task"
        assert result["node_type"] == "task"
        assert "name" in result
        assert "description" in result
        assert "created_at" in result
        assert "updated_at" in result
        assert "last_inspected_at" in result
        
        # Level 2+ fields not present
        assert "current_state" not in result
        assert "governing_checks" not in result
        assert "requirements" not in result
        assert "evidence" not in result
        assert "decisions" not in result
        assert "blockers" not in result
    
    def test_inspect_node_level_2(self, inspector):
        """Test Level 2 inspection (state explanation)"""
        result = inspector.inspect_node("task", "test-task", depth=2)
        
        # Level 1 + 2 fields present
        assert result["node_id"] == "test-task"
        assert "current_state" in result
        assert "execution_state" in result["current_state"]
        assert "activation_state" in result["current_state"]
        assert "status" in result["current_state"]
        assert "completion_percentage" in result["current_state"]
        
        # Level 3+ fields not present
        assert "governing_checks" not in result
        assert "evidence" not in result
    
    def test_inspect_node_level_3(self, inspector):
        """Test Level 3 inspection (evidence & requirements)"""
        result = inspector.inspect_node("wave", "test-wave", depth=3)
        
        # Level 1 + 2 + 3 fields present
        assert result["node_id"] == "test-wave"
        assert "current_state" in result
        assert "governing_checks" in result
        assert "requirements" in result
        assert "evidence" in result
        assert "evidence_summary" in result
        
        # Level 4+ fields not present
        assert "decisions" not in result
        assert "blockers" not in result
    
    def test_inspect_node_level_4(self, inspector):
        """Test Level 4 inspection (decisions & audit)"""
        result = inspector.inspect_node("task", "test-task", depth=4)
        
        # Level 1-4 fields present
        assert "current_state" in result
        assert "evidence" in result
        assert "decisions" in result
        assert "audit_reports" in result
        assert "surveys" in result
        
        # Level 5 fields not present
        assert "blockers" not in result
        assert "stop_conditions" not in result
    
    def test_inspect_node_level_5(self, inspector):
        """Test Level 5 inspection (blockers & STOP conditions)"""
        result = inspector.inspect_node("program", "test-program", depth=5)
        
        # All levels present
        assert "current_state" in result
        assert "evidence" in result
        assert "decisions" in result
        assert "blockers" in result
        assert "blocker_resolution_paths" in result
        assert "stop_conditions" in result
    
    def test_inspect_node_with_children(self, inspector):
        """Test inspection with include_children flag"""
        result = inspector.inspect_node(
            "wave", "test-wave", depth=3, include_children=True
        )
        
        assert "children" in result
    
    def test_inspect_node_without_children(self, inspector):
        """Test inspection without include_children flag"""
        result = inspector.inspect_node(
            "wave", "test-wave", depth=3, include_children=False
        )
        
        assert "children" not in result
    
    def test_state_explanation_structure(self, inspector):
        """Test state explanation has correct structure"""
        result = inspector.inspect_node("task", "test-task", depth=2)
        state = result["current_state"]
        
        # Required execution state fields
        assert "execution_state" in state
        assert "execution_state_reason" in state
        assert "execution_state_since" in state
        
        # Required activation state fields
        assert "activation_state" in state
        assert "activation_state_reason" in state
        assert "activation_state_since" in state
        
        # Required status fields
        assert "status" in state
        assert state["status"] in ["RED", "AMBER", "GREEN"]
        assert "status_reason" in state
        assert "status_contributing_factors" in state
        
        # Required completion fields
        assert "completion_percentage" in state
        assert "completion_calculation" in state
        assert "completion_is_authoritative" in state
        assert state["completion_is_authoritative"] is False  # Always informational
    
    def test_governing_checks_structure(self, inspector):
        """Test governing checks have correct structure"""
        result = inspector.inspect_node("task", "test-task", depth=3)
        checks = result["governing_checks"]
        
        assert isinstance(checks, list)
        if len(checks) > 0:
            check = checks[0]
            assert "check_id" in check
            assert "check_name" in check
            assert "check_type" in check
            assert "description" in check
            assert "required" in check
            assert "status" in check
            assert check["status"] in ["PASS", "FAIL", "PENDING", "NOT_APPLICABLE"]
    
    def test_requirements_structure(self, inspector):
        """Test requirements have correct structure"""
        result = inspector.inspect_node("task", "test-task", depth=3)
        requirements = result["requirements"]
        
        assert isinstance(requirements, list)
        if len(requirements) > 0:
            req = requirements[0]
            assert "requirement_id" in req
            assert "requirement_name" in req
            assert "requirement_type" in req
            assert "description" in req
            assert "mandatory" in req
            assert "satisfied" in req
    
    def test_evidence_structure(self, inspector):
        """Test evidence artifacts have correct structure"""
        result = inspector.inspect_node("task", "test-task", depth=3)
        evidence = result["evidence"]
        
        assert isinstance(evidence, list)
        if len(evidence) > 0:
            ev = evidence[0]
            assert "id" in ev
            assert "category" in ev
            assert ev["category"] in ["ARCHITECTURE", "QA", "BUILD", "COMPLETION"]
            assert "artifact_type" in ev
            assert "artifact_location" in ev
            assert "artifact_description" in ev
            assert "validated" in ev
    
    def test_evidence_summary_structure(self, inspector):
        """Test evidence summary has correct structure"""
        result = inspector.inspect_node("task", "test-task", depth=3)
        summary = result["evidence_summary"]
        
        assert "total_evidence_items" in summary
        assert "validated_items" in summary
        assert "pending_items" in summary
        assert "by_category" in summary
        assert "ARCHITECTURE" in summary["by_category"]
        assert "QA" in summary["by_category"]
        assert "BUILD" in summary["by_category"]
        assert "COMPLETION" in summary["by_category"]
    
    def test_decisions_structure(self, inspector):
        """Test decisions have correct structure"""
        result = inspector.inspect_node("task", "test-task", depth=4)
        decisions = result["decisions"]
        
        assert isinstance(decisions, list)
        if len(decisions) > 0:
            dec = decisions[0]
            assert "decision_id" in dec
            assert "decision_type" in dec
            assert "decision_summary" in dec
            assert "decision_rationale" in dec
            assert "decision_authority" in dec
            assert "decided_at" in dec
    
    def test_audit_reports_structure(self, inspector):
        """Test audit reports have correct structure"""
        result = inspector.inspect_node("task", "test-task", depth=4)
        reports = result["audit_reports"]
        
        assert isinstance(reports, list)
        if len(reports) > 0:
            report = reports[0]
            assert "report_id" in report
            assert "report_type" in report
            assert "report_title" in report
            assert "report_location" in report
            assert "created_at" in report
            assert "created_by" in report
            assert "findings_summary" in report
    
    def test_blockers_structure(self, inspector):
        """Test blockers have correct structure"""
        result = inspector.inspect_node("task", "test-task", depth=5)
        blockers = result["blockers"]
        
        assert isinstance(blockers, list)
        # Blockers can be empty (no active blockers)
    
    def test_stop_conditions_structure(self, inspector):
        """Test STOP conditions have correct structure"""
        result = inspector.inspect_node("task", "test-task", depth=5)
        stop_conditions = result["stop_conditions"]
        
        assert isinstance(stop_conditions, list)
        # STOP conditions can be empty (no active conditions)
    
    def test_log_inspection(self, inspector):
        """Test inspection logging"""
        # Should not raise exception
        inspector.log_inspection(
            node_id="test-task",
            node_type="task",
            inspected_by="test-user",
            inspection_depth=3,
            ip_address="127.0.0.1",
            user_agent="test-agent"
        )
    
    def test_node_types_supported(self, inspector):
        """Test all node types are supported"""
        node_types = ["program", "wave", "sub-wave", "task"]
        
        for node_type in node_types:
            result = inspector.inspect_node(node_type, f"test-{node_type}", depth=1)
            assert result["node_type"] == node_type
    
    def test_inspection_is_read_only(self, inspector):
        """Test that inspection does not modify state"""
        # First inspection
        result1 = inspector.inspect_node("task", "test-task", depth=5)
        
        # Second inspection
        result2 = inspector.inspect_node("task", "test-task", depth=5)
        
        # Results should be consistent (read-only)
        assert result1["node_id"] == result2["node_id"]
        assert result1["node_type"] == result2["node_type"]
        # Note: last_inspected_at will differ, which is expected


class TestBuildNodeInspectorAPI:
    """Test suite for API-related functionality"""
    
    def test_inspector_response_format(self):
        """Test that inspector returns correct response format for API"""
        inspector = create_inspector()
        result = inspector.inspect_node("task", "api-test", depth=3)
        
        # Check that result is JSON-serializable
        import json
        try:
            json.dumps(result, default=str)  # default=str for datetime objects
        except Exception as e:
            pytest.fail(f"Result is not JSON-serializable: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
