"""
Test suite for Wave 1.0.4 API Builder - Intent Processing Subsystem

QA Coverage: QA-058 to QA-077 (20 QA components)
Architecture: FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md
Builder: api-builder
"""

import pytest
from datetime import datetime
from foreman.api.intent_intake import IntentIntakeHandler
from foreman.api.clarification_loop import ClarificationLoopManager
from foreman.api.requirement_generator import RequirementGenerator
from foreman.api.approval_manager import ApprovalManager


class TestIntentIntakeHandler:
    """Tests for INTENT-01: Intent Intake Handler (QA-058 to QA-061)"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.handler = IntentIntakeHandler()
    
    def test_qa_058_accept_informal_intent(self):
        """
        QA-058: Accept informal intent
        Verifies partial input acceptance, informal language handling, context capture
        """
        # Test with informal, partial input
        result = self.handler.accept_intent(
            "Need to add user management",
            {"conversation_id": "conv_123", "user_id": "johan"}
        )
        
        assert result["intent_id"] is not None
        assert result["content"] == "Need to add user management"
        assert result["state"] == "RECEIVED"
        assert result["context"]["conversation_id"] == "conv_123"
        assert result["validation_status"] == "pending"
        assert "timestamp" in result
    
    def test_qa_058_empty_content_rejection(self):
        """QA-058: Reject empty intent content"""
        with pytest.raises(ValueError, match="Intent content cannot be empty"):
            self.handler.accept_intent("", {"conversation_id": "conv_123"})
    
    def test_qa_059_validate_intent_input(self):
        """
        QA-059: Validate intent input
        Verifies required context present, intent parsability
        """
        # First accept an intent
        intent = self.handler.accept_intent(
            "Create dashboard component",
            {"conversation_id": "conv_123"}
        )
        
        # Validate it
        result = self.handler.validate_intent(intent["intent_id"])
        
        assert result["valid"] is True
        assert result["intent_id"] == intent["intent_id"]
        assert result["parseable"] is True
        assert len(result["missing_context"]) == 0
    
    def test_qa_059_validation_missing_context(self):
        """QA-059: Detect missing required context"""
        # Accept intent without conversation_id
        intent = self.handler.accept_intent(
            "Add feature X",
            {}
        )
        
        result = self.handler.validate_intent(intent["intent_id"])
        
        assert result["valid"] is False
        assert "conversation_id" in result["missing_context"]
    
    def test_qa_060_route_to_clarification(self):
        """
        QA-060: Route intent to clarification
        Verifies ambiguity detection trigger, clarification flow initiation
        """
        # Accept an intent
        intent = self.handler.accept_intent(
            "Make it better",
            {"conversation_id": "conv_123"}
        )
        
        # Route to clarification due to ambiguity
        result = self.handler.route_to_clarification(
            intent["intent_id"],
            "Unclear what 'it' refers to and how to make 'better'"
        )
        
        assert result["intent_id"] == intent["intent_id"]
        assert result["routed_to"] == "INTENT-02"
        assert result["ambiguity_detected"] is True
        assert result["clarification_flow_initiated"] is True
        assert "Unclear" in result["ambiguity_reason"]
        
        # Verify intent state updated
        intent_state = self.handler.pending_intents[intent["intent_id"]]
        assert intent_state["state"] == "CLARIFYING"
    
    def test_qa_061_handle_unparseable_input(self):
        """
        QA-061: Intent Intake failure modes - unparseable input
        """
        intent = self.handler.accept_intent(
            "Test intent",
            {"conversation_id": "conv_123"}
        )
        
        # First failure - should retry
        result = self.handler.handle_intake_failure(
            intent["intent_id"],
            "unparseable",
            "Content format unrecognizable"
        )
        
        assert result["failure_type"] == "unparseable"
        assert result["recovery_action"] == "retry"
        assert result["retry_count"] == 1
        assert result["escalated"] is False
    
    def test_qa_061_handle_context_loss(self):
        """
        QA-061: Intent Intake failure modes - context loss detection/recovery
        """
        # Try to handle failure for non-existent intent (context loss)
        result = self.handler.handle_intake_failure(
            "non_existent_intent",
            "context_loss",
            "Intent not found"
        )
        
        assert result["failure_type"] == "context_loss"
        assert result["recovery_action"] == "escalate"
        assert result["escalated"] is True
        assert "context loss detected" in result["error_details"]


class TestClarificationLoopManager:
    """Tests for INTENT-02: Clarification Loop Manager (QA-062 to QA-066)"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.manager = ClarificationLoopManager()
    
    def test_qa_062_manage_clarification_iterations(self):
        """
        QA-062: Manage clarification iterations
        Verifies iteration count, history tracking, timeout detection
        """
        clarif_id = self.manager.start_clarification(
            "intent_123",
            "Ambiguous requirements"
        )
        
        # First iteration
        result = self.manager.manage_iteration(
            clarif_id,
            "What specific feature do you want?",
            "I want a user dashboard"
        )
        
        assert result["clarification_id"] == clarif_id
        assert result["iteration_number"] == 1
        assert result["history_tracked"] is True
        assert result["timeout_detected"] is False
        assert result["can_continue"] is True
    
    def test_qa_062_timeout_detection(self):
        """QA-062: Detect timeout after max iterations"""
        clarif_id = self.manager.start_clarification(
            "intent_123",
            "Ambiguous"
        )
        
        # Simulate max iterations
        for i in range(5):
            result = self.manager.manage_iteration(
                clarif_id,
                f"Question {i+1}",
                f"Response {i+1}"
            )
        
        assert result["timeout_detected"] is True
        assert result["can_continue"] is False
        
        session = self.manager.clarification_sessions[clarif_id]
        assert session["status"] == "timeout"
    
    def test_qa_063_detect_sufficient_clarification(self):
        """
        QA-063: Detect sufficient clarification
        Verifies completeness check, confidence threshold, transition trigger
        """
        clarif_id = self.manager.start_clarification(
            "intent_123",
            "Unclear scope"
        )
        
        # Provide sufficient clarification
        result = self.manager.detect_sufficient_clarification(
            clarif_id,
            "I need a dashboard with user analytics, showing login history, session duration, and user activity graphs. It should update in real-time and support export to CSV."
        )
        
        assert result["clarification_id"] == clarif_id
        assert result["completeness_check"] is True
        assert result["confidence_score"] >= 0.0
        assert result["transition_trigger"] == result["sufficient"]
    
    def test_qa_064_handle_clarification_timeout(self):
        """
        QA-064: Handle clarification timeout
        Verifies iteration limit enforcement, escalation trigger, structured capture
        """
        clarif_id = self.manager.start_clarification(
            "intent_123",
            "Ambiguous"
        )
        
        # Add some iterations
        for i in range(3):
            self.manager.manage_iteration(
                clarif_id,
                f"Q{i}",
                f"R{i}"
            )
        
        # Handle timeout
        result = self.manager.handle_timeout(clarif_id)
        
        assert result["clarification_id"] == clarif_id
        assert result["iteration_limit_enforced"] is True
        assert result["escalation_triggered"] is True
        assert "structured_capture" in result
        assert result["structured_capture"]["total_iterations"] == 3
        assert "timeout_reason" in result["structured_capture"]
    
    def test_qa_065_preserve_clarification_history(self):
        """
        QA-065: Preserve clarification history
        Verifies audit trail, context preservation across iterations
        """
        clarif_id = self.manager.start_clarification(
            "intent_123",
            "Initial ambiguity"
        )
        
        # Multiple iterations
        self.manager.manage_iteration(clarif_id, "Q1", "R1")
        self.manager.manage_iteration(clarif_id, "Q2", "R2")
        
        # Preserve history
        result = self.manager.preserve_history(clarif_id)
        
        assert result["clarification_id"] == clarif_id
        assert result["context_preserved"] is True
        assert result["iteration_count"] == 2
        assert "audit_trail" in result
        assert len(result["audit_trail"]["iterations"]) == 2
        assert result["audit_trail"]["initial_ambiguity"] == "Initial ambiguity"
    
    def test_qa_066_infinite_loop_prevention(self):
        """
        QA-066: Clarification Loop failure modes - infinite loop prevention
        """
        clarif_id = self.manager.start_clarification(
            "intent_123",
            "Ambiguous"
        )
        
        result = self.manager.handle_failure(clarif_id, "infinite_loop")
        
        assert result["failure_type"] == "infinite_loop"
        assert result["infinite_loop_prevented"] is True
        assert result["recovery_action"] == "force_timeout"
        
        session = self.manager.clarification_sessions[clarif_id]
        assert session["status"] == "failed"
    
    def test_qa_066_resolution_failure_handling(self):
        """
        QA-066: Clarification Loop failure modes - ambiguity resolution failure
        """
        clarif_id = self.manager.start_clarification(
            "intent_123",
            "Unresolvable"
        )
        
        result = self.manager.handle_failure(clarif_id, "resolution_failure")
        
        assert result["failure_type"] == "resolution_failure"
        assert result["resolution_failure_handled"] is True
        assert result["recovery_action"] == "escalate"


class TestRequirementGenerator:
    """Tests for INTENT-03: Requirement Generator (QA-067 to QA-070)"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.generator = RequirementGenerator()
    
    def test_qa_067_generate_requirement(self):
        """
        QA-067: Generate requirement from clarified intent
        Verifies structure, acceptance criteria, traceability
        """
        result = self.generator.generate_requirement(
            "intent_123",
            "Create a user dashboard with analytics showing login history and session data"
        )
        
        assert result["requirement_id"] is not None
        assert "structure" in result
        assert result["structure"]["intent_id"] == "intent_123"
        assert result["structure"]["state"] == "DRAFT"
        assert len(result["acceptance_criteria"]) > 0
        assert "traceability" in result
        assert result["traceability"]["source_id"] == "intent_123"
    
    def test_qa_068_include_approval_metadata(self):
        """
        QA-068: Include approval workflow metadata
        Verifies approver identification, approval instructions
        """
        # First generate requirement
        req = self.generator.generate_requirement(
            "intent_123",
            "Test requirement content"
        )
        
        # Add approval metadata
        result = self.generator.include_approval_metadata(req["requirement_id"])
        
        assert result["requirement_id"] == req["requirement_id"]
        assert result["approver_id"] == "johan"
        assert "approval_instructions" in result
        assert "steps" in result["approval_instructions"]
        assert result["approval_metadata"]["approval_required"] is True
    
    def test_qa_069_link_to_intent(self):
        """
        QA-069: Link requirement to original intent
        Verifies bidirectional traceability, context preservation
        """
        req = self.generator.generate_requirement(
            "intent_123",
            "Test content"
        )
        
        result = self.generator.link_to_intent(req["requirement_id"], "intent_123")
        
        assert result["requirement_id"] == req["requirement_id"]
        assert result["intent_id"] == "intent_123"
        assert result["bidirectional_link"] is True
        assert result["context_preserved"] is True
    
    def test_qa_070_handle_generation_failure(self):
        """
        QA-070: Requirement Generator failure modes
        Verifies generation failure handling, incomplete spec detection
        """
        # Test incomplete spec failure
        result = self.generator.handle_generation_failure(
            "intent_123",
            "incomplete_spec"
        )
        
        assert result["intent_id"] == "intent_123"
        assert result["failure_handled"] is True
        assert result["incomplete_spec_detected"] is True
        assert result["recovery_action"] == "return_to_clarification"
        
        # Test generation timeout
        result2 = self.generator.handle_generation_failure(
            "intent_456",
            "generation_timeout"
        )
        
        assert result2["recovery_action"] == "retry"


class TestApprovalManager:
    """Tests for INTENT-04: Approval Manager (QA-071 to QA-077)"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.manager = ApprovalManager()
    
    def test_qa_071_present_for_approval(self):
        """
        QA-071: Present requirement for approval
        Verifies presentation format, Johan notification, approval UI
        """
        req_spec = {
            "requirement_id": "req_123",
            "title": "User Dashboard Feature",
            "description": "Create user dashboard with analytics",
            "acceptance_criteria": ["Criterion 1", "Criterion 2"],
            "traceability": {"source_id": "intent_123"}
        }
        
        result = self.manager.present_for_approval("req_123", req_spec)
        
        assert result["approval_id"] is not None
        assert result["johan_notified"] is True
        assert result["approval_ui_rendered"] is True
        assert "presentation_format" in result
        assert result["presentation_format"]["requirement_id"] == "req_123"
    
    def test_qa_072_handle_approval_accept(self):
        """
        QA-072: Handle approval (accept)
        Verifies state transition, spec freeze, build initiation trigger
        """
        # First present for approval
        req_spec = {"requirement_id": "req_123", "title": "Test"}
        approval = self.manager.present_for_approval("req_123", req_spec)
        
        # Handle approval
        result = self.manager.handle_approval(approval["approval_id"])
        
        assert result["approval_id"] == approval["approval_id"]
        assert result["spec_frozen"] is True
        assert result["build_initiation_triggered"] is True
        assert result["state_transition"]["from"] == "PENDING"
        assert result["state_transition"]["to"] == "APPROVED"
    
    def test_qa_073_handle_rejection(self):
        """
        QA-073: Handle rejection
        Verifies rejection reason capture, state transition, intent availability for rework
        """
        req_spec = {"requirement_id": "req_123", "title": "Test"}
        approval = self.manager.present_for_approval("req_123", req_spec)
        
        result = self.manager.handle_rejection(
            approval["approval_id"],
            "Requirements are too vague"
        )
        
        assert result["approval_id"] == approval["approval_id"]
        assert result["rejection_reason"] == "Requirements are too vague"
        assert result["intent_available_for_rework"] is True
        assert result["state_transition"]["to"] == "REJECTED"
    
    def test_qa_074_handle_conditional_approval(self):
        """
        QA-074: Handle conditional approval
        Verifies conditions capture, partial freeze, gated progression
        """
        req_spec = {"requirement_id": "req_123", "title": "Test"}
        approval = self.manager.present_for_approval("req_123", req_spec)
        
        conditions = [
            "Must include security review",
            "Performance benchmarks required"
        ]
        
        result = self.manager.handle_conditional_approval(
            approval["approval_id"],
            conditions
        )
        
        assert result["approval_id"] == approval["approval_id"]
        assert result["conditions_captured"] == conditions
        assert result["partial_freeze"] is True
        assert result["gated_progression"] is True
    
    def test_qa_075_detect_timeout(self):
        """
        QA-075: Approval timeout detection
        Verifies silence detection, escalation, reminder mechanism
        """
        req_spec = {"requirement_id": "req_123", "title": "Test"}
        approval = self.manager.present_for_approval("req_123", req_spec)
        
        # Immediately check timeout (should not be timed out yet)
        result = self.manager.detect_timeout(approval["approval_id"])
        
        assert result["approval_id"] == approval["approval_id"]
        assert result["silence_detected"] is False
        assert result["escalation_triggered"] is False
    
    def test_qa_076_memory_proposal_approval(self):
        """
        QA-076: Memory write proposal approval
        Verifies proposal format, approval integration, write execution
        """
        proposal_content = {
            "scope": "global",
            "content": {"key": "value"},
            "reason": "Test memory write",
            "tags": ["test"]
        }
        
        result = self.manager.handle_memory_proposal_approval(
            "prop_123",
            proposal_content
        )
        
        assert result["proposal_id"] == "prop_123"
        assert result["proposal_format_valid"] is True
        assert result["approval_integrated"] is True
        assert result["write_execution_pending"] is True
    
    def test_qa_076_invalid_proposal_format(self):
        """QA-076: Reject invalid memory proposal format"""
        invalid_proposal = {"scope": "global"}  # Missing required fields
        
        with pytest.raises(ValueError, match="Invalid proposal format"):
            self.manager.handle_memory_proposal_approval(
                "prop_123",
                invalid_proposal
            )
    
    def test_qa_077_handle_notification_failure(self):
        """
        QA-077: Approval Manager failure modes - notification failure
        """
        req_spec = {"requirement_id": "req_123", "title": "Test"}
        approval = self.manager.present_for_approval("req_123", req_spec)
        
        result = self.manager.handle_failure(
            approval["approval_id"],
            "notification_failure"
        )
        
        assert result["failure_type"] == "notification_failure"
        assert result["notification_failure_handled"] is True
        assert result["state_consistent"] is True
        assert result["recovery_action"] == "retry_notification"
    
    def test_qa_077_handle_state_consistency_failure(self):
        """
        QA-077: Approval Manager failure modes - state consistency
        """
        req_spec = {"requirement_id": "req_123", "title": "Test"}
        approval = self.manager.present_for_approval("req_123", req_spec)
        
        result = self.manager.handle_failure(
            approval["approval_id"],
            "state_consistency"
        )
        
        assert result["failure_type"] == "state_consistency"
        assert result["state_consistent"] is True
        assert result["recovery_action"] == "revert_state"
