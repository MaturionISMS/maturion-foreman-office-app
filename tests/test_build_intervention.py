"""
Tests for Build Intervention Controller

Tests BUILD_INTERVENTION_AND_ALERT_MODEL.md (G-C10) implementation.
"""

import pytest
import json
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from fm.orchestration.build_intervention import BuildInterventionController, create_intervention_controller


@pytest.fixture
def repo_root(tmp_path):
    """Create a temporary repository root for testing."""
    return tmp_path


@pytest.fixture
def intervention_controller(repo_root):
    """Create an intervention controller instance for testing."""
    return BuildInterventionController(repo_root)


class TestInterventionControllerInitialization:
    """Test intervention controller initialization."""
    
    def test_controller_initialization(self, repo_root):
        """Test that controller initializes correctly."""
        controller = BuildInterventionController(repo_root)
        
        assert controller.repo_root == repo_root
        assert controller.intervention_log_dir.exists()
        assert controller.intervention_log_dir.name == "interventions"
    
    def test_factory_function(self, repo_root):
        """Test factory function creates controller."""
        controller = create_intervention_controller(repo_root)
        
        assert isinstance(controller, BuildInterventionController)
        assert controller.repo_root == repo_root


class TestAlertIssuance:
    """Test alert issuance functionality."""
    
    def test_issue_alert_success(self, intervention_controller):
        """Test successful alert issuance."""
        result = intervention_controller.issue_alert(
            scope_level='step',
            target_node_id='task-test-001',
            rationale='This is a test alert with sufficient detail',
            triggered_by='test_user'
        )
        
        assert result['success'] is True
        assert 'alert_id' in result
        assert result['alert_id'].startswith('alert-')
        assert 'routed_to' in result
        assert result['status'] == 'open'
        assert 'timestamp' in result
    
    def test_issue_alert_invalid_scope(self, intervention_controller):
        """Test alert with invalid scope level."""
        with pytest.raises(ValueError, match="Invalid scope_level"):
            intervention_controller.issue_alert(
                scope_level='invalid',
                target_node_id='task-test-001',
                rationale='This is a test alert',
                triggered_by='test_user'
            )
    
    def test_issue_alert_rationale_too_short(self, intervention_controller):
        """Test alert with rationale below minimum length."""
        with pytest.raises(ValueError, match="at least 20 characters"):
            intervention_controller.issue_alert(
                scope_level='step',
                target_node_id='task-test-001',
                rationale='Too short',
                triggered_by='test_user'
            )
    
    def test_issue_alert_routing_step(self, intervention_controller):
        """Test alert routing for step scope."""
        result = intervention_controller.issue_alert(
            scope_level='step',
            target_node_id='task-test-001',
            rationale='This is a test alert for step scope routing',
            triggered_by='test_user'
        )
        
        assert 'builder_agent' in result['routed_to']
        assert 'fm' in result['routed_to']
    
    def test_issue_alert_routing_application(self, intervention_controller):
        """Test alert routing for application scope."""
        result = intervention_controller.issue_alert(
            scope_level='application',
            target_node_id='program-test-001',
            rationale='This is a critical application-level alert',
            triggered_by='test_user'
        )
        
        assert 'human_authority' in result['routed_to']
        assert 'johan' in result['routed_to']
    
    def test_alert_persistence(self, intervention_controller):
        """Test that alert is persisted to disk."""
        result = intervention_controller.issue_alert(
            scope_level='wave',
            target_node_id='wave-test-001',
            rationale='This alert should be persisted to disk',
            triggered_by='test_user'
        )
        
        alert_id = result['alert_id']
        alert_file = intervention_controller.intervention_log_dir / f"{alert_id}.json"
        
        assert alert_file.exists()
        
        with open(alert_file, 'r') as f:
            alert_data = json.load(f)
        
        assert alert_data['alert_id'] == alert_id
        assert alert_data['alert_type'] == 'alert'
        assert alert_data['scope']['level'] == 'wave'
        assert alert_data['status'] == 'open'


class TestEmergencyStop:
    """Test emergency stop functionality."""
    
    def test_issue_emergency_stop_success(self, intervention_controller):
        """Test successful emergency stop issuance."""
        result = intervention_controller.issue_emergency_stop(
            scope_level='step',
            target_node_id='task-test-001',
            critical_rationale='This is a critical emergency stop with detailed explanation',
            triggered_by='test_user',
            confirmation={
                'acknowledged_impact': True,
                'typed_confirmation': 'STOP'
            }
        )
        
        assert result['success'] is True
        assert 'stop_id' in result
        assert result['stop_id'].startswith('stop-')
        assert result['status'] == 'active'
        assert 'stopped_at' in result
        assert 'affected_nodes' in result
        assert 'resumption_requires' in result
    
    def test_emergency_stop_invalid_scope(self, intervention_controller):
        """Test stop with invalid scope level."""
        with pytest.raises(ValueError, match="Invalid scope_level"):
            intervention_controller.issue_emergency_stop(
                scope_level='invalid',
                target_node_id='task-test-001',
                critical_rationale='This is a critical emergency stop',
                triggered_by='test_user',
                confirmation={'acknowledged_impact': True, 'typed_confirmation': 'STOP'}
            )
    
    def test_emergency_stop_rationale_too_short(self, intervention_controller):
        """Test stop with rationale below minimum length."""
        with pytest.raises(ValueError, match="at least 50 characters"):
            intervention_controller.issue_emergency_stop(
                scope_level='step',
                target_node_id='task-test-001',
                critical_rationale='Too short rationale',
                triggered_by='test_user',
                confirmation={'acknowledged_impact': True, 'typed_confirmation': 'STOP'}
            )
    
    def test_emergency_stop_missing_acknowledgment(self, intervention_controller):
        """Test stop without impact acknowledgment."""
        with pytest.raises(ValueError, match="acknowledged_impact=true"):
            intervention_controller.issue_emergency_stop(
                scope_level='step',
                target_node_id='task-test-001',
                critical_rationale='This is a critical emergency stop with detailed explanation',
                triggered_by='test_user',
                confirmation={'acknowledged_impact': False, 'typed_confirmation': 'STOP'}
            )
    
    def test_emergency_stop_wrong_confirmation(self, intervention_controller):
        """Test stop with wrong typed confirmation."""
        with pytest.raises(ValueError, match="typed_confirmation='STOP'"):
            intervention_controller.issue_emergency_stop(
                scope_level='step',
                target_node_id='task-test-001',
                critical_rationale='This is a critical emergency stop with detailed explanation',
                triggered_by='test_user',
                confirmation={'acknowledged_impact': True, 'typed_confirmation': 'WRONG'}
            )
    
    def test_emergency_stop_affected_nodes_step(self, intervention_controller):
        """Test affected nodes for step scope."""
        result = intervention_controller.issue_emergency_stop(
            scope_level='step',
            target_node_id='task-test-001',
            critical_rationale='This is a critical emergency stop for step scope testing',
            triggered_by='test_user',
            confirmation={'acknowledged_impact': True, 'typed_confirmation': 'STOP'}
        )
        
        assert len(result['affected_nodes']) == 1
        assert 'task-test-001' in result['affected_nodes']
    
    def test_emergency_stop_affected_nodes_application(self, intervention_controller):
        """Test affected nodes for application scope."""
        result = intervention_controller.issue_emergency_stop(
            scope_level='application',
            target_node_id='program-test-001',
            critical_rationale='This is a catastrophic emergency stop for entire application',
            triggered_by='test_user',
            confirmation={'acknowledged_impact': True, 'typed_confirmation': 'STOP'}
        )
        
        assert 'all_waves' in result['affected_nodes']
        assert 'all_tasks' in result['affected_nodes']
    
    def test_stop_persistence(self, intervention_controller):
        """Test that stop is persisted to disk."""
        result = intervention_controller.issue_emergency_stop(
            scope_level='wave',
            target_node_id='wave-test-001',
            critical_rationale='This emergency stop should be persisted with full evidence',
            triggered_by='test_user',
            confirmation={'acknowledged_impact': True, 'typed_confirmation': 'STOP'}
        )
        
        stop_id = result['stop_id']
        stop_file = intervention_controller.intervention_log_dir / f"{stop_id}.json"
        
        assert stop_file.exists()
        
        with open(stop_file, 'r') as f:
            stop_data = json.load(f)
        
        assert stop_data['stop_id'] == stop_id
        assert stop_data['stop_type'] == 'emergency_stop'
        assert stop_data['scope']['level'] == 'wave'
        assert stop_data['status'] == 'active'
        assert 'execution_snapshot' in stop_data
        assert 'evidence_package' in stop_data


class TestInterventionContext:
    """Test intervention context retrieval."""
    
    def test_get_alert_context(self, intervention_controller):
        """Test retrieving context for an alert."""
        # First create an alert
        alert_result = intervention_controller.issue_alert(
            scope_level='step',
            target_node_id='task-test-001',
            rationale='This alert is for context retrieval testing',
            triggered_by='test_user'
        )
        
        alert_id = alert_result['alert_id']
        
        # Now retrieve context
        context = intervention_controller.get_intervention_context(alert_id)
        
        assert context['success'] is True
        assert context['intervention_id'] == alert_id
        assert 'context' in context
        assert 'intervention' in context['context']
        assert 'node' in context['context']
    
    def test_get_stop_context(self, intervention_controller):
        """Test retrieving context for an emergency stop."""
        # First create a stop
        stop_result = intervention_controller.issue_emergency_stop(
            scope_level='sub-wave',
            target_node_id='sub-wave-test-001',
            critical_rationale='This emergency stop is for context retrieval testing purposes',
            triggered_by='test_user',
            confirmation={'acknowledged_impact': True, 'typed_confirmation': 'STOP'}
        )
        
        stop_id = stop_result['stop_id']
        
        # Now retrieve context
        context = intervention_controller.get_intervention_context(stop_id)
        
        assert context['success'] is True
        assert context['intervention_id'] == stop_id
        assert 'context' in context
        assert 'intervention' in context['context']
        assert context['context']['intervention']['stop_type'] == 'emergency_stop'
    
    def test_get_context_not_found(self, intervention_controller):
        """Test retrieving context for non-existent intervention."""
        with pytest.raises(FileNotFoundError):
            intervention_controller.get_intervention_context('nonexistent-id')


class TestResumption:
    """Test resumption after emergency stop."""
    
    def test_resume_after_stop_success(self, intervention_controller):
        """Test successful resumption after stop."""
        # First create a stop
        stop_result = intervention_controller.issue_emergency_stop(
            scope_level='step',
            target_node_id='task-test-001',
            critical_rationale='This emergency stop will be resumed after resolution',
            triggered_by='test_user',
            confirmation={'acknowledged_impact': True, 'typed_confirmation': 'STOP'}
        )
        
        stop_id = stop_result['stop_id']
        
        # Now resume
        resume_result = intervention_controller.resume_after_stop(
            stop_id=stop_id,
            authorized_by='test_authority',
            resolution_summary='Issue has been identified and resolved. Safe to proceed.',
            resume_conditions=['Issue resolved', 'Tests passing', 'Architecture validated']
        )
        
        assert resume_result['success'] is True
        assert resume_result['stop_id'] == stop_id
        assert resume_result['status'] == 'resumed'
        assert 'resumed_at' in resume_result
    
    def test_resume_not_found(self, intervention_controller):
        """Test resuming non-existent stop."""
        with pytest.raises(FileNotFoundError):
            intervention_controller.resume_after_stop(
                stop_id='nonexistent-stop',
                authorized_by='test_authority',
                resolution_summary='This should fail because stop does not exist but has enough text',
                resume_conditions=['N/A']
            )
    
    def test_resume_already_resumed(self, intervention_controller):
        """Test resuming stop that's already resumed."""
        # First create and resume a stop
        stop_result = intervention_controller.issue_emergency_stop(
            scope_level='step',
            target_node_id='task-test-001',
            critical_rationale='This stop will be resumed and then attempted again',
            triggered_by='test_user',
            confirmation={'acknowledged_impact': True, 'typed_confirmation': 'STOP'}
        )
        
        stop_id = stop_result['stop_id']
        
        intervention_controller.resume_after_stop(
            stop_id=stop_id,
            authorized_by='test_authority',
            resolution_summary='First resumption with proper resolution details and length',
            resume_conditions=['Issue resolved']
        )
        
        # Try to resume again
        with pytest.raises(ValueError, match="already been resumed"):
            intervention_controller.resume_after_stop(
                stop_id=stop_id,
                authorized_by='test_authority',
                resolution_summary='Second resumption should fail but has enough characters',
                resume_conditions=['N/A']
            )
    
    def test_resume_resolution_too_short(self, intervention_controller):
        """Test resumption with insufficient resolution summary."""
        stop_result = intervention_controller.issue_emergency_stop(
            scope_level='step',
            target_node_id='task-test-001',
            critical_rationale='This stop will attempt resume with short resolution',
            triggered_by='test_user',
            confirmation={'acknowledged_impact': True, 'typed_confirmation': 'STOP'}
        )
        
        stop_id = stop_result['stop_id']
        
        with pytest.raises(ValueError, match="at least 50 characters"):
            intervention_controller.resume_after_stop(
                stop_id=stop_id,
                authorized_by='test_authority',
                resolution_summary='Too short',
                resume_conditions=['N/A']
            )
    
    def test_resume_persistence(self, intervention_controller):
        """Test that resumption is persisted."""
        stop_result = intervention_controller.issue_emergency_stop(
            scope_level='wave',
            target_node_id='wave-test-001',
            critical_rationale='This stop resumption should be persisted with full details',
            triggered_by='test_user',
            confirmation={'acknowledged_impact': True, 'typed_confirmation': 'STOP'}
        )
        
        stop_id = stop_result['stop_id']
        
        intervention_controller.resume_after_stop(
            stop_id=stop_id,
            authorized_by='test_authority',
            resolution_summary='Complete resolution with all details documented properly',
            resume_conditions=['Blocker removed', 'Tests green', 'Approval received']
        )
        
        # Load from disk
        stop_file = intervention_controller.intervention_log_dir / f"{stop_id}.json"
        with open(stop_file, 'r') as f:
            stop_data = json.load(f)
        
        assert stop_data['status'] == 'resumed'
        assert 'resumption' in stop_data
        assert stop_data['resumption']['authorized_by'] == 'test_authority'
        assert len(stop_data['resumption']['resume_conditions']) == 3


class TestAuditTrail:
    """Test audit trail functionality."""
    
    def test_audit_log_created(self, intervention_controller):
        """Test that audit log is created."""
        intervention_controller.issue_alert(
            scope_level='step',
            target_node_id='task-test-001',
            rationale='This alert should create audit log entry',
            triggered_by='test_user'
        )
        
        audit_log = intervention_controller.intervention_log_dir / "audit.log"
        assert audit_log.exists()
    
    def test_audit_log_contains_entries(self, intervention_controller):
        """Test that audit log contains intervention entries."""
        intervention_controller.issue_alert(
            scope_level='step',
            target_node_id='task-test-001',
            rationale='This alert should be in audit log',
            triggered_by='test_user'
        )
        
        audit_log = intervention_controller.intervention_log_dir / "audit.log"
        content = audit_log.read_text()
        
        assert 'alert_issued' in content
        assert 'task-test-001' in content


class TestDataModel:
    """Test that intervention data conforms to schema."""
    
    def test_alert_data_schema(self, intervention_controller):
        """Test that alert data matches schema."""
        result = intervention_controller.issue_alert(
            scope_level='wave',
            target_node_id='wave-test-001',
            rationale='Testing alert data schema conformance',
            triggered_by='test_user',
            ip_address='192.168.1.1'
        )
        
        alert_id = result['alert_id']
        alert = intervention_controller._load_intervention(alert_id)
        
        # Check required fields
        required_fields = [
            'alert_id', 'alert_type', 'triggered_at', 'triggered_by',
            'scope', 'rationale', 'routing', 'status', 'response_timeline',
            'context_package'
        ]
        
        for field in required_fields:
            assert field in alert, f"Missing required field: {field}"
        
        # Check nested structures
        assert 'type' in alert['triggered_by']
        assert 'level' in alert['scope']
        assert 'primary' in alert['routing']
    
    def test_stop_data_schema(self, intervention_controller):
        """Test that stop data matches schema."""
        result = intervention_controller.issue_emergency_stop(
            scope_level='application',
            target_node_id='program-test-001',
            critical_rationale='Testing emergency stop data schema conformance and completeness',
            triggered_by='test_user',
            confirmation={'acknowledged_impact': True, 'typed_confirmation': 'STOP'},
            ip_address='192.168.1.1'
        )
        
        stop_id = result['stop_id']
        stop = intervention_controller._load_intervention(stop_id)
        
        # Check required fields
        required_fields = [
            'stop_id', 'stop_type', 'triggered_at', 'triggered_by',
            'scope', 'critical_rationale', 'confirmation', 'execution_snapshot',
            'routing', 'status', 'timeline', 'evidence_package'
        ]
        
        for field in required_fields:
            assert field in stop, f"Missing required field: {field}"
        
        # Check nested structures
        assert 'affected_nodes' in stop['scope']
        assert 'required_authorization' in stop['routing']
        assert 'stopped_at' in stop['timeline']
