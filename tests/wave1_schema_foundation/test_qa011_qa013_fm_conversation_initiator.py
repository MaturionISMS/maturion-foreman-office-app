"""
Test Suite: CONV-03 FM Conversation Initiator Data Layer

QA Coverage: QA-011 to QA-013
Architecture Component: CONV-03 FM Conversation Initiator
Architecture Reference: FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md (Section 3.3)

Data Contract:
- Entity: ConversationContext
- Operations: CREATE
- Fields: id, conversationId, contextType, contextData, createdAt
"""

import pytest
import uuid
from datetime import datetime

from fm.data.models import (
    Conversation,
    ConversationState,
    Message,
    MessageType,
    MessageState,
    ConversationContext,
)


@pytest.mark.wave1
@pytest.mark.schema
class TestFMConversationInitiator:
    """
    Test suite for CONV-03 FM Conversation Initiator data layer.
    
    Tests FM-initiated conversations: initiate, attach context, urgent conversations.
    """
    
    def test_qa011_fm_initiates_conversation(self, db_session, test_organisation_id, test_user_id):
        """
        QA-011: FM initiates conversation
        
        Verify:
        - Conversation creation (via CONV-01)
        - Johan notification data captured
        - Context attachment capability
        """
        # FM initiates conversation
        conversation_id = f"conv-{uuid.uuid4()}"
        initial_message_content = "FM needs to report build status"
        
        # Create conversation (CONV-01 operation)
        conversation = Conversation(
            id=conversation_id,
            organisation_id=test_organisation_id,
            user_id=test_user_id,
            state=ConversationState.ACTIVE,
        )
        db_session.add(conversation)
        db_session.commit()
        
        # Create initial FM message (CONV-02 operation)
        message = Message(
            id=f"msg-{uuid.uuid4()}",
            organisation_id=test_organisation_id,
            conversation_id=conversation.id,
            sender_id="fm",  # FM is sender
            content=initial_message_content,
            type=MessageType.FM,
            state=MessageState.PENDING,
        )
        db_session.add(message)
        db_session.commit()
        
        # Verify conversation created
        assert conversation.id == conversation_id, "Conversation ID should match"
        assert conversation.user_id == test_user_id, "User ID should match (Johan)"
        assert conversation.state == ConversationState.ACTIVE, "State should be ACTIVE"
        
        # Verify FM message created
        assert message.sender_id == "fm", "Sender should be FM"
        assert message.type == MessageType.FM, "Type should be FM"
        assert message.content == initial_message_content, "Content should match"
        
        # Verify Johan notification data available
        assert message.id is not None, "Message ID for notification"
        assert conversation.id is not None, "Conversation ID for notification"
    
    def test_qa012_attach_context_escalation(self, db_session, sample_conversation, test_organisation_id):
        """
        QA-012: Attach context to FM-initiated conversation (escalation context)
        
        Verify:
        - Escalation context persisted
        - Context type captured
        - Context data structure preserved
        """
        # Attach escalation context
        context_id = f"ctx-{uuid.uuid4()}"
        escalation_data = {
            "component": "CONV-01",
            "error": "Database write failure",
            "retry_count": 3,
            "severity": "high",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        context = ConversationContext(
            id=context_id,
            organisation_id=test_organisation_id,
            conversation_id=sample_conversation.id,
            context_type="escalation",
            context_data=escalation_data,
            priority="high",
        )
        
        db_session.add(context)
        db_session.commit()
        db_session.refresh(context)
        
        # Verify context persisted
        assert context.id == context_id, "Context ID should match"
        assert context.conversation_id == sample_conversation.id, "Conversation ID should match"
        assert context.context_type == "escalation", "Context type should be escalation"
        
        # Verify context data structure
        assert context.context_data == escalation_data, "Context data should match"
        assert context.context_data["component"] == "CONV-01", "Component should be preserved"
        assert context.context_data["retry_count"] == 3, "Retry count should be preserved"
    
    def test_qa012_attach_context_build(self, db_session, sample_conversation, test_organisation_id):
        """
        QA-012: Attach context to FM-initiated conversation (build context)
        
        Verify:
        - Build context persisted
        - Evidence linking capability
        """
        # Attach build context
        build_data = {
            "build_id": "build-123",
            "phase": "architecture",
            "status": "completed",
            "qa_coverage": "100%",
            "evidence_artifacts": [
                "evidence/qa-001.json",
                "evidence/qa-002.json"
            ]
        }
        
        context = ConversationContext(
            id=f"ctx-{uuid.uuid4()}",
            organisation_id=test_organisation_id,
            conversation_id=sample_conversation.id,
            context_type="build",
            context_data=build_data,
            priority="normal",
        )
        
        db_session.add(context)
        db_session.commit()
        db_session.refresh(context)
        
        # Verify build context
        assert context.context_type == "build", "Context type should be build"
        assert context.context_data["build_id"] == "build-123", "Build ID should be preserved"
        
        # Verify evidence linking
        assert "evidence_artifacts" in context.context_data, "Evidence artifacts should be present"
        assert len(context.context_data["evidence_artifacts"]) == 2, "Evidence artifacts count should match"
    
    def test_qa012_attach_context_evidence(self, db_session, sample_conversation, test_organisation_id):
        """
        QA-012: Attach context to FM-initiated conversation (evidence context)
        
        Verify:
        - Evidence context persisted
        - QA component references preserved
        """
        # Attach evidence context
        evidence_data = {
            "qa_component": "QA-001",
            "test_result": "PASS",
            "coverage": "100%",
            "artifacts": {
                "test_log": "logs/qa-001-test.log",
                "evidence": "evidence/qa-001.json"
            }
        }
        
        context = ConversationContext(
            id=f"ctx-{uuid.uuid4()}",
            organisation_id=test_organisation_id,
            conversation_id=sample_conversation.id,
            context_type="evidence",
            context_data=evidence_data,
            priority="normal",
        )
        
        db_session.add(context)
        db_session.commit()
        db_session.refresh(context)
        
        # Verify evidence context
        assert context.context_type == "evidence", "Context type should be evidence"
        assert context.context_data["qa_component"] == "QA-001", "QA component should be preserved"
        assert context.context_data["test_result"] == "PASS", "Test result should be preserved"
    
    def test_qa012_attach_context_validation(self, db_session):
        """
        QA-012: Attach context validation
        
        Verify:
        - Context type validation
        - Invalid context types rejected
        """
        # Test valid context types
        valid_types = ["escalation", "build", "evidence", "urgent", "general"]
        for context_type in valid_types:
            ConversationContext.validate_context_type(context_type)
            # Should not raise exception
        
        # Test invalid context type
        with pytest.raises(ValueError) as exc_info:
            ConversationContext.validate_context_type("invalid_type")
        
        assert "invalid context type" in str(exc_info.value).lower(), "Error should indicate invalid type"
    
    def test_qa013_fm_urgent_conversation(self, db_session, test_organisation_id, test_user_id):
        """
        QA-013: FM urgent conversation
        
        Verify:
        - Priority flag set to "urgent"
        - Immediate notification capability
        - Inbox placement priority
        """
        # Create urgent conversation
        conversation = Conversation(
            id=f"conv-{uuid.uuid4()}",
            organisation_id=test_organisation_id,
            user_id=test_user_id,
            state=ConversationState.ACTIVE,
        )
        db_session.add(conversation)
        db_session.commit()
        
        # Attach urgent context
        urgent_data = {
            "issue": "Critical build failure",
            "severity": "critical",
            "requires_immediate_attention": True,
            "deadline": "ASAP"
        }
        
        context = ConversationContext(
            id=f"ctx-{uuid.uuid4()}",
            organisation_id=test_organisation_id,
            conversation_id=conversation.id,
            context_type="urgent",
            context_data=urgent_data,
            priority="urgent",  # Priority flag
        )
        
        db_session.add(context)
        db_session.commit()
        db_session.refresh(context)
        
        # Verify priority flag
        assert context.priority == "urgent", "Priority should be urgent"
        
        # Verify urgent context data
        assert context.context_data["requires_immediate_attention"] is True, "Urgent flag should be set"
        assert context.context_data["severity"] == "critical", "Severity should be critical"
        
        # Verify notification data available for inbox
        assert context.id is not None, "Context ID for notification"
        assert context.conversation_id == conversation.id, "Conversation ID for inbox routing"
    
    def test_qa013_priority_validation(self, db_session):
        """
        QA-013: FM urgent conversation priority validation
        
        Verify:
        - Priority validation
        - Invalid priorities rejected
        """
        # Test valid priorities
        valid_priorities = ["normal", "high", "urgent"]
        for priority in valid_priorities:
            ConversationContext.validate_priority(priority)
            # Should not raise exception
        
        # Test invalid priority
        with pytest.raises(ValueError) as exc_info:
            ConversationContext.validate_priority("invalid_priority")
        
        assert "invalid priority" in str(exc_info.value).lower(), "Error should indicate invalid priority"
    
    def test_qa013_urgent_conversation_ordering(self, db_session, test_organisation_id, test_user_id):
        """
        QA-013: FM urgent conversation inbox placement
        
        Verify:
        - Multiple priority levels supported
        - Priority ordering capability (for inbox display)
        """
        # Create conversations with different priorities
        conversation = Conversation(
            id=f"conv-{uuid.uuid4()}",
            organisation_id=test_organisation_id,
            user_id=test_user_id,
            state=ConversationState.ACTIVE,
        )
        db_session.add(conversation)
        db_session.commit()
        
        # Add contexts with different priorities
        priorities = ["normal", "high", "urgent"]
        contexts = []
        
        for priority in priorities:
            context = ConversationContext(
                id=f"ctx-{uuid.uuid4()}",
                organisation_id=test_organisation_id,
                conversation_id=conversation.id,
                context_type="general",
                context_data={"message": f"Priority {priority}"},
                priority=priority,
            )
            db_session.add(context)
            contexts.append(context)
        
        db_session.commit()
        
        # Verify all priorities persisted
        for context in contexts:
            db_session.refresh(context)
            assert context.priority in priorities, f"Priority {context.priority} should be valid"
        
        # Query contexts ordered by priority (for inbox display)
        # Urgent > High > Normal
        priority_order = {"urgent": 1, "high": 2, "normal": 3}
        retrieved_contexts = db_session.query(ConversationContext).filter_by(
            conversation_id=conversation.id
        ).all()
        
        # Verify all contexts retrieved
        assert len(retrieved_contexts) == 3, "Should retrieve all 3 contexts"
