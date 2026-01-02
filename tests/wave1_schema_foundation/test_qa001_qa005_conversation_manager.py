"""
Test Suite: CONV-01 Conversation Manager Data Layer

QA Coverage: QA-001 to QA-005
Architecture Component: CONV-01 Conversation Manager
Architecture Reference: FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md (Section 3.1)

Data Contract:
- Entity: Conversation
- Operations: CREATE, READ, UPDATE
- Fields: conversationId, userId, state, createdAt, archivedAt, resumedAt
"""

import pytest
import uuid
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from fm.data.models import (
    Conversation,
    ConversationState,
)


@pytest.mark.wave1
@pytest.mark.schema
class TestConversationManager:
    """
    Test suite for CONV-01 Conversation Manager data layer.
    
    Tests conversation lifecycle: create, retrieve, archive, resume.
    """
    
    def test_qa001_create_conversation(self, db_session, test_organisation_id, test_user_id):
        """
        QA-001: Create conversation
        
        Verify:
        - Database write succeeds
        - Audit log created (created_at, updated_at)
        - Initial state is ACTIVE
        - Tenant isolation (organisation_id present)
        """
        # Create conversation
        conversation_id = f"conv-{uuid.uuid4()}"
        conversation = Conversation(
            id=conversation_id,
            organisation_id=test_organisation_id,
            user_id=test_user_id,
            state=ConversationState.ACTIVE,
        )
        
        # Save to database
        db_session.add(conversation)
        db_session.commit()
        db_session.refresh(conversation)
        
        # Verify database write
        assert conversation.id == conversation_id, "Conversation ID should match"
        assert conversation.organisation_id == test_organisation_id, "Organisation ID should match (tenant isolation)"
        assert conversation.user_id == test_user_id, "User ID should match"
        
        # Verify initial state
        assert conversation.state == ConversationState.ACTIVE, "Initial state should be ACTIVE"
        
        # Verify audit timestamps
        assert conversation.created_at is not None, "created_at must be set"
        assert conversation.updated_at is not None, "updated_at must be set"
        assert isinstance(conversation.created_at, datetime), "created_at must be datetime"
        assert isinstance(conversation.updated_at, datetime), "updated_at must be datetime"
        
        # Verify optional fields are None
        assert conversation.archived_at is None, "archived_at should be None for new conversation"
        assert conversation.resumed_at is None, "resumed_at should be None for new conversation"
        assert conversation.archived_reason is None, "archived_reason should be None for new conversation"
        
        # Verify message tracking fields
        assert conversation.message_count == 0, "message_count should be 0 for new conversation"
        assert conversation.last_message_at is None, "last_message_at should be None for new conversation"
    
    def test_qa002_retrieve_conversation(self, db_session, sample_conversation):
        """
        QA-002: Retrieve conversation
        
        Verify:
        - Data persistence (conversation can be retrieved)
        - Message loading (relationships work)
        - State consistency (state is preserved)
        """
        # Retrieve conversation by ID
        retrieved = db_session.query(Conversation).filter_by(id=sample_conversation.id).first()
        
        # Verify data persistence
        assert retrieved is not None, "Conversation should be retrievable"
        assert retrieved.id == sample_conversation.id, "ID should match"
        assert retrieved.organisation_id == sample_conversation.organisation_id, "Organisation ID should match"
        assert retrieved.user_id == sample_conversation.user_id, "User ID should match"
        
        # Verify state consistency
        assert retrieved.state == sample_conversation.state, "State should be preserved"
        
        # Verify relationships work (messages, contexts, clarification_sessions)
        assert hasattr(retrieved, 'messages'), "Conversation should have messages relationship"
        assert hasattr(retrieved, 'contexts'), "Conversation should have contexts relationship"
        assert hasattr(retrieved, 'clarification_sessions'), "Conversation should have clarification_sessions relationship"
        
        # Verify audit timestamps persisted
        assert retrieved.created_at == sample_conversation.created_at, "created_at should be preserved"
        assert retrieved.updated_at == sample_conversation.updated_at, "updated_at should be preserved"
    
    def test_qa003_archive_conversation(self, db_session, sample_conversation):
        """
        QA-003: Archive conversation
        
        Verify:
        - State transition (ACTIVE → ARCHIVED)
        - Reason captured
        - Archive timestamp set
        - Audit trail updated
        """
        # Archive conversation
        archive_reason = "User completed conversation"
        before_archive = datetime.utcnow()
        
        sample_conversation.archive(archive_reason)
        db_session.commit()
        db_session.refresh(sample_conversation)
        
        after_archive = datetime.utcnow()
        
        # Verify state transition
        assert sample_conversation.state == ConversationState.ARCHIVED, "State should be ARCHIVED"
        
        # Verify reason captured
        assert sample_conversation.archived_reason == archive_reason, "Archive reason should be captured"
        
        # Verify archive timestamp
        assert sample_conversation.archived_at is not None, "archived_at should be set"
        assert isinstance(sample_conversation.archived_at, datetime), "archived_at should be datetime"
        assert before_archive <= sample_conversation.archived_at <= after_archive, "archived_at should be within time window"
        
        # Verify audit trail
        assert sample_conversation.updated_at >= before_archive, "updated_at should be updated"
    
    def test_qa003_archive_conversation_already_archived(self, db_session, sample_conversation):
        """
        QA-003: Archive conversation (failure mode)
        
        Verify:
        - Cannot archive already archived conversation
        - State conflict handling (raises ValueError)
        """
        # Archive conversation first time
        sample_conversation.archive("First archive")
        db_session.commit()
        
        # Try to archive again
        with pytest.raises(ValueError) as exc_info:
            sample_conversation.archive("Second archive")
        
        assert "already archived" in str(exc_info.value).lower(), "Error message should indicate already archived"
    
    def test_qa004_resume_conversation(self, db_session, sample_conversation):
        """
        QA-004: Resume conversation
        
        Verify:
        - State transition (ARCHIVED → RESUMED)
        - Audit trail updated
        - Resume timestamp set
        """
        # Archive conversation first
        sample_conversation.archive("Temporary pause")
        db_session.commit()
        
        # Resume conversation
        before_resume = datetime.utcnow()
        
        sample_conversation.resume()
        db_session.commit()
        db_session.refresh(sample_conversation)
        
        after_resume = datetime.utcnow()
        
        # Verify state transition
        assert sample_conversation.state == ConversationState.RESUMED, "State should be RESUMED"
        
        # Verify resume timestamp
        assert sample_conversation.resumed_at is not None, "resumed_at should be set"
        assert isinstance(sample_conversation.resumed_at, datetime), "resumed_at should be datetime"
        assert before_resume <= sample_conversation.resumed_at <= after_resume, "resumed_at should be within time window"
        
        # Verify audit trail
        assert sample_conversation.updated_at >= before_resume, "updated_at should be updated"
    
    def test_qa004_resume_conversation_not_archived(self, db_session, sample_conversation):
        """
        QA-004: Resume conversation (failure mode)
        
        Verify:
        - Cannot resume non-archived conversation
        - State conflict handling (raises ValueError)
        """
        # Try to resume active conversation (not archived)
        with pytest.raises(ValueError) as exc_info:
            sample_conversation.resume()
        
        assert "not archived" in str(exc_info.value).lower(), "Error message should indicate not archived"
    
    def test_qa005_conversation_manager_failure_database_write(self, db_session, test_organisation_id, test_user_id):
        """
        QA-005: Conversation Manager failure modes
        
        Verify:
        - Database write failure detection
        - Constraint violations handled
        """
        # Test 1: Missing required field (organisation_id)
        conversation_missing_org = Conversation(
            id=f"conv-{uuid.uuid4()}",
            organisation_id=None,  # Missing required field
            user_id=test_user_id,
            state=ConversationState.ACTIVE,
        )
        
        with pytest.raises((IntegrityError, Exception)):
            db_session.add(conversation_missing_org)
            db_session.commit()
        
        db_session.rollback()
        
        # Test 2: Missing required field (user_id)
        conversation_missing_user = Conversation(
            id=f"conv-{uuid.uuid4()}",
            organisation_id=test_organisation_id,
            user_id=None,  # Missing required field
            state=ConversationState.ACTIVE,
        )
        
        with pytest.raises((IntegrityError, Exception)):
            db_session.add(conversation_missing_user)
            db_session.commit()
        
        db_session.rollback()
    
    def test_qa005_conversation_manager_failure_state_conflict(self, db_session, sample_conversation):
        """
        QA-005: Conversation Manager failure modes
        
        Verify:
        - State conflict handling
        - Invalid state transitions rejected
        """
        # Try invalid state transition: archive already archived conversation
        sample_conversation.archive("First archive")
        db_session.commit()
        
        with pytest.raises(ValueError):
            sample_conversation.archive("Second archive")
        
        # Try invalid state transition: resume non-archived conversation
        active_conversation = Conversation(
            id=f"conv-{uuid.uuid4()}",
            organisation_id=sample_conversation.organisation_id,
            user_id=sample_conversation.user_id,
            state=ConversationState.ACTIVE,
        )
        db_session.add(active_conversation)
        db_session.commit()
        
        with pytest.raises(ValueError):
            active_conversation.resume()
