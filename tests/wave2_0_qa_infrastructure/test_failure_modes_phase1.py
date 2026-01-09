"""
QA-241 to QA-255: Complex Failure Modes Phase 1 Tests

Architectural Reference: Wave 2.0 Complex Failure Modes Phase 1 Specification
QA Range: QA-241 to QA-255
Components: Failure Recovery, Timeout Handling, Error Cascade Management

State: RED → GREEN (Wave 2.11 Implementation)
Build-to-Green Status: IN_PROGRESS

Test Categories:
- Recovery Workflows (QA-241 to QA-245): 5 tests
- Timeout Handling (QA-246 to QA-250): 5 tests
- Error Cascade Management (QA-251 to QA-255): 5 tests
"""

import pytest
from typing import Dict, Any
from datetime import datetime, timezone
import time

# Import failure mode handlers
from runtime.failure_recovery_handler import (
    FailureRecoveryHandler,
    RecoveryStrategy,
    RecoveryState
)
from runtime.timeout_handler import (
    TimeoutHandler,
    TimeoutAction,
    TimeoutState
)
from runtime.error_cascade_manager import (
    ErrorCascadeManager,
    CascadeType,
    CascadeState
)


@pytest.mark.wave2
@pytest.mark.subwave_2_11
class TestRecoveryWorkflows:
    """Tests for Recovery Workflows (QA-241 to QA-245)"""
    
    def test_qa_241_multi_level_drill_down_recovery(self):
        """
        QA-241: Multi-level drill-down recovery
        
        Verify:
        - Nested failure recovery levels work
        - State preserved at each level
        - Recovery workflow handles complex failures
        - Nested levels tracked
        
        Status: GREEN - Implemented
        """
        # Create recovery handler
        handler = FailureRecoveryHandler(organisation_id="test-org-241")
        
        # Initiate multi-level recovery
        context = {
            "drill_down_level": 3,
            "evidence_id": "evidence-001",
            "failure_point": "level_2"
        }
        
        result = handler.initiate_recovery(
            failure_type="drill_down_failure",
            context=context,
            strategy=RecoveryStrategy.ROLLBACK
        )
        
        # Verify nested levels created
        assert result["nested_levels"] >= 2, "Multi-level recovery should have nested levels"
        assert result["state_preserved"], "State must be preserved at initiation"
        assert result["steps_planned"] > 0, "Recovery steps must be planned"
        assert result["organisation_id"] == "test-org-241", "Tenant isolation required"
        
        # Verify workflow created
        workflow_id = result["workflow_id"]
        status = handler.get_recovery_status(workflow_id)
        assert status is not None, "Recovery workflow must exist"
        assert status["state"] == RecoveryState.INITIATED.value, "Initial state must be INITIATED"
    
    def test_qa_242_drill_down_error_handling_recovery(self):
        """
        QA-242: Drill-down error handling recovery
        
        Verify:
        - Evidence not found error handled
        - Broken links recovered
        - Recovery UX maintained
        - Error handling complete
        
        Status: GREEN - Implemented
        """
        # Create recovery handler
        handler = FailureRecoveryHandler(organisation_id="test-org-242")
        
        # Initiate recovery
        context = {
            "error_type": "evidence_not_found",
            "evidence_id": "missing-evidence",
            "link_broken": True
        }
        
        recovery = handler.initiate_recovery(
            failure_type="evidence_retrieval",
            context=context,
            strategy=RecoveryStrategy.RETRY
        )
        
        workflow_id = recovery["workflow_id"]
        
        # Execute recovery step
        result = handler.execute_recovery_step(
            workflow_id=workflow_id,
            step_id=handler._workflows[workflow_id].steps[0].step_id
        )
        
        # Verify error handling
        assert result["recovery_attempted"], "Recovery must be attempted"
        assert result["error_handled"], "Error must be handled"
        assert result["next_action"] in ["continue_next_step", "complete_recovery", "retry_step"], \
            "Next action must be defined"
    
    def test_qa_243_intent_state_transition_recovery(self):
        """
        QA-243: Intent RECEIVED → CLARIFYING state transition recovery
        
        Verify:
        - Ambiguity trigger handled
        - State change recovered
        - Clarification start managed
        - Context preserved
        
        Status: GREEN - Implemented
        """
        # Create recovery handler
        handler = FailureRecoveryHandler(organisation_id="test-org-243")
        
        # Handle state transition failure
        result = handler.handle_state_transition_failure(
            from_state="RECEIVED",
            to_state="CLARIFYING",
            entity_type="intent",
            entity_id="intent-243",
            error_details={
                "error": "Ambiguity detection failed",
                "reason": "Clarification engine unavailable"
            }
        )
        
        # Verify recovery
        assert result["transition_recovered"], "Transition must be recovered"
        assert result["state_preserved"], "State must be preserved"
        assert result["context_maintained"], "Context must be maintained"
        assert result["recovery_action"].startswith("rollback"), "Should rollback on failure"
        assert result["organisation_id"] == "test-org-243", "Tenant isolation required"
    
    def test_qa_244_intent_clarification_completion_recovery(self):
        """
        QA-244: Intent CLARIFYING → CLARIFIED state transition recovery
        
        Verify:
        - Sufficient clarification detection
        - State change recovered
        - Requirement generation trigger handled
        - Context maintained
        
        Status: GREEN - Implemented
        """
        # Create recovery handler
        handler = FailureRecoveryHandler(organisation_id="test-org-244")
        
        # Handle state transition failure
        result = handler.handle_state_transition_failure(
            from_state="CLARIFYING",
            to_state="CLARIFIED",
            entity_type="intent",
            entity_id="intent-244",
            error_details={
                "error": "Clarification completion check failed",
                "reason": "Requirement generator unavailable"
            }
        )
        
        # Verify recovery
        assert result["transition_recovered"], "Transition must be recovered"
        assert result["state_preserved"], "State must be preserved via rollback"
        assert result["context_maintained"], "Context must be maintained"
        assert "workflow_id" in result, "Workflow ID must be returned"
    
    def test_qa_245_intent_rejection_recovery(self):
        """
        QA-245: Intent CLARIFYING → REJECTED state transition recovery
        
        Verify:
        - Rejection trigger handled
        - Reason captured
        - Cleanup performed
        - Recovery complete
        
        Status: GREEN - Implemented
        """
        # Create recovery handler
        handler = FailureRecoveryHandler(organisation_id="test-org-245")
        
        # Handle state transition failure
        result = handler.handle_state_transition_failure(
            from_state="CLARIFYING",
            to_state="REJECTED",
            entity_type="intent",
            entity_id="intent-245",
            error_details={
                "error": "Rejection handling failed",
                "reason": "Cleanup process interrupted"
            }
        )
        
        # Verify recovery
        assert result["transition_recovered"], "Transition must be recovered"
        assert result["state_preserved"], "State must be preserved"
        assert result["recovery_action"] is not None, "Recovery action must be specified"
        assert result["iteration_tracked"] is False, "Rejection doesn't track iterations"


@pytest.mark.wave2
@pytest.mark.subwave_2_11
class TestTimeoutHandling:
    """Tests for Timeout Handling (QA-246 to QA-250)"""
    
    def test_qa_246_intent_rework_timeout(self):
        """
        QA-246: Intent rework timeout (CLARIFIED → RECEIVED)
        
        Verify:
        - Rework trigger with timeout
        - Context preservation during timeout
        - Iteration tracking
        - Timeout handled gracefully
        
        Status: GREEN - Implemented
        """
        # Create timeout handler
        handler = TimeoutHandler(organisation_id="test-org-246")
        
        # Start timeout monitoring for rework
        context = {
            "entity_type": "intent",
            "entity_id": "intent-246",
            "rework_reason": "Clarification insufficient"
        }
        
        monitoring = handler.start_timeout_monitoring(
            operation_id="rework-246",
            operation_type="intent_rework",
            timeout_seconds=5,  # Short timeout for testing
            action=TimeoutAction.ESCALATE,
            context=context
        )
        
        # Verify monitoring started
        assert monitoring["monitoring_started"], "Monitoring must start"
        assert monitoring["timeout_seconds"] == 5, "Timeout must be configured"
        assert "expires_at" in monitoring, "Expiration time must be provided"
        
        # Handle timeout
        result = handler.handle_state_transition_timeout(
            operation_id="rework-246",
            from_state="CLARIFIED",
            to_state="RECEIVED",
            entity_type="intent",
            entity_id="intent-246",
            preserve_context=True
        )
        
        # Verify timeout handling
        assert result["timeout_handled"], "Timeout must be handled"
        assert result["context_preserved"], "Context must be preserved for rework"
        assert result["iteration_tracked"], "Rework iteration must be tracked"
        assert result["organisation_id"] == "test-org-246", "Tenant isolation required"
        
        # Cleanup
        handler.shutdown()
    
    def test_qa_247_requirement_approval_timeout(self):
        """
        QA-247: Requirement approval timeout (DRAFT → PENDING_APPROVAL)
        
        Verify:
        - Completion trigger timeout
        - Validation timeout
        - Approval presentation timeout
        - Escalation on timeout
        
        Status: GREEN - Implemented
        """
        # Create timeout handler
        handler = TimeoutHandler(organisation_id="test-org-247")
        
        # Start timeout monitoring
        monitoring = handler.start_timeout_monitoring(
            operation_id="approval-247",
            operation_type="requirement_approval",
            timeout_seconds=3,
            action=TimeoutAction.ESCALATE,
            context={"requirement_id": "req-247"}
        )
        
        # Verify monitoring
        assert monitoring["monitoring_started"], "Monitoring must start"
        
        # Handle timeout
        result = handler.handle_state_transition_timeout(
            operation_id="approval-247",
            from_state="DRAFT",
            to_state="PENDING_APPROVAL",
            entity_type="requirement",
            entity_id="req-247"
        )
        
        # Verify timeout handling
        assert result["timeout_handled"], "Timeout must be handled"
        assert result["escalation_triggered"], "Should escalate on approval timeout"
        
        # Cleanup
        handler.shutdown()
    
    def test_qa_248_requirement_approval_decision_timeout(self):
        """
        QA-248: Requirement approval decision timeout (PENDING_APPROVAL → APPROVED)
        
        Verify:
        - Approval decision timeout
        - Freeze handling on timeout
        - Build initiation trigger timeout
        - Escalation triggered
        
        Status: GREEN - Implemented
        """
        # Create timeout handler
        handler = TimeoutHandler(organisation_id="test-org-248")
        
        # Start timeout monitoring
        monitoring = handler.start_timeout_monitoring(
            operation_id="decision-248",
            operation_type="approval_decision",
            timeout_seconds=3,
            action=TimeoutAction.ESCALATE
        )
        
        assert monitoring["monitoring_started"], "Monitoring must start"
        
        # Handle timeout
        result = handler.handle_state_transition_timeout(
            operation_id="decision-248",
            from_state="PENDING_APPROVAL",
            to_state="APPROVED",
            entity_type="requirement",
            entity_id="req-248"
        )
        
        # Verify timeout handling
        assert result["timeout_handled"], "Timeout must be handled"
        assert result["escalation_triggered"], "Should escalate on decision timeout"
        
        # Cleanup
        handler.shutdown()
    
    def test_qa_249_requirement_rejection_timeout(self):
        """
        QA-249: Requirement rejection timeout (PENDING_APPROVAL → REJECTED)
        
        Verify:
        - Rejection decision timeout
        - Reason capture timeout
        - Intent availability timeout
        - Handled gracefully
        
        Status: GREEN - Implemented
        """
        # Create timeout handler
        handler = TimeoutHandler(organisation_id="test-org-249")
        
        # Start timeout monitoring
        monitoring = handler.start_timeout_monitoring(
            operation_id="rejection-249",
            operation_type="rejection_decision",
            timeout_seconds=3,
            action=TimeoutAction.ESCALATE
        )
        
        assert monitoring["monitoring_started"], "Monitoring must start"
        
        # Handle timeout
        result = handler.handle_state_transition_timeout(
            operation_id="rejection-249",
            from_state="PENDING_APPROVAL",
            to_state="REJECTED",
            entity_type="requirement",
            entity_id="req-249"
        )
        
        # Verify timeout handling
        assert result["timeout_handled"], "Timeout must be handled"
        
        # Cleanup
        handler.shutdown()
    
    def test_qa_250_conditional_approval_timeout(self):
        """
        QA-250: Conditional approval timeout (PENDING_APPROVAL → CONDITIONAL)
        
        Verify:
        - Conditional approval timeout
        - Conditions capture timeout
        - Gated progression timeout
        - Escalation or extension
        
        Status: GREEN - Implemented
        """
        # Create timeout handler
        handler = TimeoutHandler(organisation_id="test-org-250")
        
        # Start timeout monitoring with extension option
        monitoring = handler.start_timeout_monitoring(
            operation_id="conditional-250",
            operation_type="conditional_approval",
            timeout_seconds=3,
            action=TimeoutAction.EXTEND
        )
        
        assert monitoring["monitoring_started"], "Monitoring must start"
        
        # Test timeout extension
        extension = handler.extend_timeout(
            operation_id="conditional-250",
            additional_seconds=2
        )
        
        assert extension["extended"], "Timeout must be extendable"
        assert extension["new_timeout"] == 5, "New timeout must be correct"
        
        # Handle timeout
        result = handler.handle_state_transition_timeout(
            operation_id="conditional-250",
            from_state="PENDING_APPROVAL",
            to_state="CONDITIONAL",
            entity_type="requirement",
            entity_id="req-250"
        )
        
        # Verify timeout handling
        assert result["timeout_handled"], "Timeout must be handled"
        
        # Cleanup
        handler.shutdown()


@pytest.mark.wave2
@pytest.mark.subwave_2_11
class TestErrorCascadeManagement:
    """Tests for Error Cascade Management (QA-251 to QA-255)"""
    
    def test_qa_251_requirement_freeze_immutability(self):
        """
        QA-251: Requirement APPROVED → frozen state
        
        Verify:
        - Immutability enforced
        - No further changes allowed
        - Audit log maintained
        - Freeze timestamp recorded
        
        Status: GREEN - Implemented
        """
        # Create cascade manager
        manager = ErrorCascadeManager(organisation_id="test-org-251")
        
        # Freeze requirement
        requirement_data = {
            "title": "Test Requirement",
            "description": "This is a test requirement",
            "acceptance_criteria": ["Criterion 1", "Criterion 2"]
        }
        
        result = manager.enforce_requirement_freeze(
            requirement_id="req-251",
            current_state="APPROVED",
            data=requirement_data
        )
        
        # Verify freeze
        assert result["frozen"], "Requirement must be frozen"
        assert result["immutable"], "Requirement must be immutable"
        assert result["audit_logged"], "Audit log must be created"
        assert "freeze_timestamp" in result, "Freeze timestamp must be recorded"
        assert result["organisation_id"] == "test-org-251", "Tenant isolation required"
        
        # Verify immutability
        immutability_check = manager.verify_immutability("req-251")
        assert immutability_check["immutable"], "Requirement must remain immutable"
        assert immutability_check["state"] == "APPROVED", "State must be preserved"
    
    def test_qa_252_build_initiation_cascade(self):
        """
        QA-252: Build INITIATED → IN_PROGRESS cascade
        
        Verify:
        - Builder assignment cascade
        - Task creation cascade
        - Monitoring start cascade
        - State transition handled
        
        Status: GREEN - Implemented
        """
        # Create cascade manager
        manager = ErrorCascadeManager(organisation_id="test-org-252")
        
        # Handle build initiation cascade
        result = manager.handle_build_initiation_cascade(
            build_id="build-252",
            builder_assignments=[
                {"builder_id": "api-builder", "qa_range": "QA-001 to QA-010"},
                {"builder_id": "ui-builder", "qa_range": "QA-011 to QA-020"}
            ],
            tasks=[
                {"task_id": "task-001", "type": "implementation"},
                {"task_id": "task-002", "type": "testing"}
            ],
            monitoring_config={"interval_seconds": 60}
        )
        
        # Verify cascade handling
        assert result["cascade_handled"], "Cascade must be handled"
        assert result["builders_assigned"], "Builders must be assigned"
        assert result["tasks_created"], "Tasks must be created"
        assert result["monitoring_started"], "Monitoring must start"
        assert result["state_transition"] == "INITIATED → IN_PROGRESS", "State transition must be correct"
        assert result["organisation_id"] == "test-org-252", "Tenant isolation required"
    
    def test_qa_253_build_blocking_cascade(self):
        """
        QA-253: Build IN_PROGRESS → BLOCKED cascade
        
        Verify:
        - Blocker detection
        - Escalation triggered
        - Pause propagated
        - Cascade contained
        
        Status: GREEN - Implemented
        """
        # Create cascade manager
        manager = ErrorCascadeManager(organisation_id="test-org-253")
        
        # Handle build blocking cascade
        result = manager.handle_build_blocking_cascade(
            build_id="build-253",
            blocker_details={
                "blocker_id": "blocker-001",
                "message": "Dependency failure",
                "severity": "HIGH"
            },
            escalation_required=True
        )
        
        # Verify cascade handling
        assert result["cascade_handled"], "Cascade must be handled"
        assert result["blocker_detected"], "Blocker must be detected"
        assert result["escalation_triggered"], "Escalation must be triggered"
        assert result["pause_propagated"], "Pause must be propagated"
        assert result["organisation_id"] == "test-org-253", "Tenant isolation required"
    
    def test_qa_254_build_unblocking_cascade(self):
        """
        QA-254: Build BLOCKED → IN_PROGRESS cascade
        
        Verify:
        - Blocker resolution
        - Resume triggered
        - State restored
        - Cascade resolved
        
        Status: GREEN - Implemented
        """
        # Create cascade manager
        manager = ErrorCascadeManager(organisation_id="test-org-254")
        
        # Handle build unblocking cascade
        result = manager.handle_build_unblocking_cascade(
            build_id="build-254",
            resolution_details={
                "blocker_id": "blocker-001",
                "resolution": "Dependency fixed",
                "resolved_by": "integration-builder"
            },
            restore_state=True
        )
        
        # Verify cascade handling
        assert result["cascade_handled"], "Cascade must be handled"
        assert result["blocker_resolved"], "Blocker must be resolved"
        assert result["resume_triggered"], "Resume must be triggered"
        assert result["state_restored"], "State must be restored"
        assert result["organisation_id"] == "test-org-254", "Tenant isolation required"
    
    def test_qa_255_build_completion_cascade(self):
        """
        QA-255: Build IN_PROGRESS → COMPLETED cascade
        
        Verify:
        - 100% GREEN validation
        - Deliverable creation
        - Handover triggered
        - Cascade resolved
        
        Status: GREEN - Implemented
        """
        # Create cascade manager
        manager = ErrorCascadeManager(organisation_id="test-org-255")
        
        # Handle build completion cascade
        result = manager.handle_build_completion_cascade(
            build_id="build-255",
            validation_results={
                "coverage_percent": 100.0,
                "tests_passed": 15,
                "tests_failed": 0,
                "warnings": 0
            },
            deliverables=[
                {"deliverable_id": "report-001", "type": "completion_report"},
                {"deliverable_id": "evidence-001", "type": "evidence_package"}
            ],
            handover_config={"handover_type": "formal", "reviewers": ["FM"]}
        )
        
        # Verify cascade handling
        assert result["cascade_handled"], "Cascade must be handled"
        assert result["validation_passed"], "Validation must be 100% GREEN"
        assert result["deliverables_created"], "Deliverables must be created"
        assert result["handover_triggered"], "Handover must be triggered"
        assert result["organisation_id"] == "test-org-255", "Tenant isolation required"
        
        # Test with invalid validation (not 100%)
        result_invalid = manager.handle_build_completion_cascade(
            build_id="build-255-invalid",
            validation_results={
                "coverage_percent": 95.0,  # Not 100%
                "tests_passed": 14,
                "tests_failed": 1
            },
            deliverables=[],
            handover_config={}
        )
        
        # Verify failure on incomplete validation
        assert not result_invalid["cascade_handled"], "Should fail without 100% GREEN"
        assert not result_invalid["validation_passed"], "Validation should not pass"
        assert "error" in result_invalid, "Error message should be present"
