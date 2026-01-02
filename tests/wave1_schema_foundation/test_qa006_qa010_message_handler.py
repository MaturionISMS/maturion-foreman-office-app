"""
Test Suite: CONV-02 Message Handler Data Layer

QA Coverage: QA-006 to QA-010
Architecture Component: CONV-02 Message Handler
Architecture Reference: FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md (Section 3.2)

Data Contract:
- Entity: Message
- Operations: CREATE, READ, UPDATE
- Fields: messageId, conversationId, senderId, content, type, state, createdAt, deliveredAt, readAt
"""

import pytest
import uuid
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from fm.data.models import (
    Conversation,
    ConversationState,
    Message,
    MessageType,
    MessageState,
)


@pytest.mark.wave1
@pytest.mark.schema
class TestMessageHandler:
    """
    Test suite for CONV-02 Message Handler data layer.
    
    Tests message handling: send, deliver, read, validation, failure modes.
    """
    
    def test_qa006_send_message(self, db_session, sample_conversation, test_organisation_id, test_user_id):
        """
        QA-006: Send message
        
        Verify:
        - Validation (content not empty)
        - Persistence (message saved to database)
        - Delivery event preparation (state is PENDING)
        - Tenant isolation (organisation_id present)
        """
        # Create message
        message_id = f"msg-{uuid.uuid4()}"
        content = "This is a test message"
        
        # Validate content first
        Message.validate_content(content)
        
        message = Message(
            id=message_id,
            organisation_id=test_organisation_id,
            conversation_id=sample_conversation.id,
            sender_id=test_user_id,
            content=content,
            type=MessageType.USER,
            state=MessageState.PENDING,
        )
        
        # Save to database
        db_session.add(message)
        db_session.commit()
        db_session.refresh(message)
        
        # Verify persistence
        assert message.id == message_id, "Message ID should match"
        assert message.organisation_id == test_organisation_id, "Organisation ID should match (tenant isolation)"
        assert message.conversation_id == sample_conversation.id, "Conversation ID should match"
        assert message.sender_id == test_user_id, "Sender ID should match"
        assert message.content == content, "Content should match"
        assert message.type == MessageType.USER, "Type should be USER"
        
        # Verify initial state
        assert message.state == MessageState.PENDING, "Initial state should be PENDING"
        
        # Verify audit timestamps
        assert message.created_at is not None, "created_at must be set"
        assert message.updated_at is not None, "updated_at must be set"
        
        # Verify delivery timestamps are None
        assert message.delivered_at is None, "delivered_at should be None for pending message"
        assert message.read_at is None, "read_at should be None for pending message"
    
    def test_qa007_deliver_message(self, db_session, sample_message):
        """
        QA-007: Deliver message
        
        Verify:
        - Routing (message state transitions)
        - Timestamp captured (delivered_at)
        - State update (PENDING → DELIVERED)
        """
        # Deliver message
        before_delivery = datetime.utcnow()
        
        sample_message.deliver()
        db_session.commit()
        db_session.refresh(sample_message)
        
        after_delivery = datetime.utcnow()
        
        # Verify state transition
        assert sample_message.state == MessageState.DELIVERED, "State should be DELIVERED"
        
        # Verify timestamp
        assert sample_message.delivered_at is not None, "delivered_at should be set"
        assert isinstance(sample_message.delivered_at, datetime), "delivered_at should be datetime"
        assert before_delivery <= sample_message.delivered_at <= after_delivery, "delivered_at should be within time window"
        
        # Verify audit trail
        assert sample_message.updated_at >= before_delivery, "updated_at should be updated"
        
        # Verify read timestamp still None
        assert sample_message.read_at is None, "read_at should still be None"
    
    def test_qa007_deliver_message_invalid_state(self, db_session, sample_message):
        """
        QA-007: Deliver message (failure mode)
        
        Verify:
        - Cannot deliver already delivered message
        - State validation enforced
        """
        # Deliver message first time
        sample_message.deliver()
        db_session.commit()
        
        # Try to deliver again
        with pytest.raises(ValueError) as exc_info:
            sample_message.deliver()
        
        assert "not in PENDING state" in str(exc_info.value), "Error should indicate invalid state"
    
    def test_qa008_mark_message_read(self, db_session, sample_message, test_user_id):
        """
        QA-008: Mark message read
        
        Verify:
        - State update (DELIVERED → READ)
        - Audit log (read_at timestamp)
        - Read by user captured
        """
        # Deliver message first (prerequisite)
        sample_message.deliver()
        db_session.commit()
        
        # Mark as read
        before_read = datetime.utcnow()
        
        sample_message.mark_read(test_user_id)
        db_session.commit()
        db_session.refresh(sample_message)
        
        after_read = datetime.utcnow()
        
        # Verify state transition
        assert sample_message.state == MessageState.READ, "State should be READ"
        
        # Verify timestamp
        assert sample_message.read_at is not None, "read_at should be set"
        assert isinstance(sample_message.read_at, datetime), "read_at should be datetime"
        assert before_read <= sample_message.read_at <= after_read, "read_at should be within time window"
        
        # Verify audit trail
        assert sample_message.updated_at >= before_read, "updated_at should be updated"
    
    def test_qa008_mark_message_read_invalid_state(self, db_session, sample_message, test_user_id):
        """
        QA-008: Mark message read (failure mode)
        
        Verify:
        - Cannot mark read if not delivered
        - State validation enforced
        """
        # Try to mark read before delivery
        with pytest.raises(ValueError) as exc_info:
            sample_message.mark_read(test_user_id)
        
        assert "not in DELIVERED state" in str(exc_info.value), "Error should indicate invalid state"
    
    def test_qa009_message_validation_empty_content(self, db_session):
        """
        QA-009: Message validation
        
        Verify:
        - Empty content rejection
        - Validation error raised
        """
        # Test empty string
        with pytest.raises(ValueError) as exc_info:
            Message.validate_content("")
        
        assert "cannot be empty" in str(exc_info.value).lower(), "Error should indicate empty content"
        
        # Test whitespace only
        with pytest.raises(ValueError):
            Message.validate_content("   ")
        
        # Test None
        with pytest.raises(ValueError):
            Message.validate_content(None)
    
    def test_qa009_message_validation_invalid_conversation(self, db_session, test_organisation_id, test_user_id):
        """
        QA-009: Message validation
        
        Verify:
        - Invalid conversation ID handling
        - Foreign key constraint enforced
        """
        # Try to create message with non-existent conversation
        message = Message(
            id=f"msg-{uuid.uuid4()}",
            organisation_id=test_organisation_id,
            conversation_id="non-existent-conv-id",
            sender_id=test_user_id,
            content="Test message",
            type=MessageType.USER,
            state=MessageState.PENDING,
        )
        
        with pytest.raises((IntegrityError, Exception)):
            db_session.add(message)
            db_session.commit()
        
        db_session.rollback()
    
    def test_qa009_message_validation_max_length(self, db_session):
        """
        QA-009: Message validation
        
        Verify:
        - Maximum content length enforced
        """
        # Test content exceeding max length
        long_content = "x" * 10001
        
        with pytest.raises(ValueError) as exc_info:
            Message.validate_content(long_content)
        
        assert "maximum length" in str(exc_info.value).lower(), "Error should indicate max length exceeded"
    
    def test_qa010_message_handler_failure_persistence(self, db_session, sample_conversation, test_organisation_id):
        """
        QA-010: Message Handler failure modes
        
        Verify:
        - Persistence failure detection
        - Missing required fields
        """
        # Test missing sender_id
        message_no_sender = Message(
            id=f"msg-{uuid.uuid4()}",
            organisation_id=test_organisation_id,
            conversation_id=sample_conversation.id,
            sender_id=None,  # Missing required field
            content="Test content",
            type=MessageType.USER,
            state=MessageState.PENDING,
        )
        
        with pytest.raises((IntegrityError, Exception)):
            db_session.add(message_no_sender)
            db_session.commit()
        
        db_session.rollback()
        
        # Test missing content
        message_no_content = Message(
            id=f"msg-{uuid.uuid4()}",
            organisation_id=test_organisation_id,
            conversation_id=sample_conversation.id,
            sender_id="test-user",
            content=None,  # Missing required field
            type=MessageType.USER,
            state=MessageState.PENDING,
        )
        
        with pytest.raises((IntegrityError, Exception)):
            db_session.add(message_no_content)
            db_session.commit()
        
        db_session.rollback()
    
    def test_qa010_message_handler_failure_intent_processing(self, db_session, sample_conversation, test_organisation_id, test_user_id):
        """
        QA-010: Message Handler failure modes
        
        Verify:
        - Intent processing failure handling
        - Message persisted with PENDING state for retry
        """
        # Simulate intent processing failure scenario:
        # Message is persisted but intent processing hasn't happened yet
        message = Message(
            id=f"msg-{uuid.uuid4()}",
            organisation_id=test_organisation_id,
            conversation_id=sample_conversation.id,
            sender_id=test_user_id,
            content="Test message for intent processing",
            type=MessageType.USER,
            state=MessageState.PENDING,  # Remains PENDING for retry
        )
        
        db_session.add(message)
        db_session.commit()
        db_session.refresh(message)
        
        # Verify message persisted for later retry
        assert message.state == MessageState.PENDING, "Message should remain PENDING for intent processing retry"
        assert message.id is not None, "Message should be persisted with ID"
        
        # In real system, intent processing would be retried later
        # For this data layer test, we just verify persistence works
