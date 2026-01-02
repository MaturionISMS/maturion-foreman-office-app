"""
Test fixtures for Wave 1 Schema Foundation tests.

QA Coverage: QA-001 to QA-018
Architecture Reference: FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md
"""

import pytest
import uuid
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fm.data.models import (
    Base,
    init_database,
    get_database,
    Conversation,
    ConversationState,
    Message,
    MessageType,
    MessageState,
    ConversationContext,
    ClarificationSession,
    ClarificationState,
)


@pytest.fixture(scope="function")
def test_db():
    """
    Create a test database for each test function.
    
    Uses in-memory SQLite for fast isolated tests.
    """
    # Use in-memory SQLite database
    database_url = "sqlite:///:memory:"
    
    # Initialize database
    db_config = init_database(database_url)
    
    # Create all tables
    db_config.create_all_tables()
    
    yield db_config
    
    # Cleanup: drop all tables
    db_config.drop_all_tables()


@pytest.fixture(scope="function")
def db_session(test_db):
    """
    Provide a database session for tests.
    
    Automatically rolls back after each test to ensure isolation.
    """
    session = test_db.get_session()
    
    yield session
    
    # Rollback any uncommitted changes
    session.rollback()
    session.close()


@pytest.fixture
def test_organisation_id():
    """Provide a test organisation ID for tenant isolation."""
    return f"org-{uuid.uuid4()}"


@pytest.fixture
def test_user_id():
    """Provide a test user ID."""
    return f"user-{uuid.uuid4()}"


@pytest.fixture
def sample_conversation(db_session, test_organisation_id, test_user_id):
    """
    Create a sample conversation for testing.
    
    QA: QA-001 (Create conversation)
    """
    conversation = Conversation(
        id=f"conv-{uuid.uuid4()}",
        organisation_id=test_organisation_id,
        user_id=test_user_id,
        state=ConversationState.ACTIVE,
    )
    db_session.add(conversation)
    db_session.commit()
    db_session.refresh(conversation)
    
    return conversation


@pytest.fixture
def sample_message(db_session, sample_conversation, test_organisation_id, test_user_id):
    """
    Create a sample message for testing.
    
    QA: QA-006 (Send message)
    """
    message = Message(
        id=f"msg-{uuid.uuid4()}",
        organisation_id=test_organisation_id,
        conversation_id=sample_conversation.id,
        sender_id=test_user_id,
        content="Test message content",
        type=MessageType.USER,
        state=MessageState.PENDING,
    )
    db_session.add(message)
    db_session.commit()
    db_session.refresh(message)
    
    return message


@pytest.fixture
def sample_context(db_session, sample_conversation, test_organisation_id):
    """
    Create a sample conversation context for testing.
    
    QA: QA-012 (Attach context)
    """
    context = ConversationContext(
        id=f"ctx-{uuid.uuid4()}",
        organisation_id=test_organisation_id,
        conversation_id=sample_conversation.id,
        context_type="escalation",
        context_data={"issue": "test", "severity": "high"},
        priority="normal",
    )
    db_session.add(context)
    db_session.commit()
    db_session.refresh(context)
    
    return context


@pytest.fixture
def sample_clarification_session(db_session, sample_conversation, test_organisation_id):
    """
    Create a sample clarification session for testing.
    
    QA: QA-014 (Detect ambiguity)
    """
    session = ClarificationSession(
        id=f"clar-{uuid.uuid4()}",
        organisation_id=test_organisation_id,
        conversation_id=sample_conversation.id,
        message_id=f"msg-{uuid.uuid4()}",
        ambiguity_score=0.75,
        ambiguity_type="insufficient_context",
        state=ClarificationState.ACTIVE,
    )
    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)
    
    return session
