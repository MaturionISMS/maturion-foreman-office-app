"""
Test Suite: CONV-04 Clarification Engine Data Layer

QA Coverage: QA-014 to QA-018
Architecture Component: CONV-04 Clarification Engine
Architecture Reference: FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md (Section 3.4)

Data Contract:
- Entity: Clarification
- Operations: CREATE, READ, UPDATE
- Fields: clarificationId, messageId, questions, responses, state, resolvedAt
"""

import pytest
import uuid
from datetime import datetime, timezone

from fm.data.models import (
    ClarificationSession,
    ClarificationState,
)


@pytest.mark.wave1
@pytest.mark.schema
class TestClarificationEngine:
    """
    Test suite for CONV-04 Clarification Engine data layer.
    
    Tests clarification: detect ambiguity, generate questions, resolve, loop limits, failure modes.
    """
    
    def test_qa014_detect_ambiguity(self, db_session, sample_conversation, test_organisation_id):
        """
        QA-014: Detect ambiguity
        
        Verify:
        - Pattern detection (ambiguity type captured)
        - Confidence scoring (ambiguity_score)
        - Clarification trigger (session created)
        """
        # Detect ambiguity in user message
        session_id = f"clar-{uuid.uuid4()}"
        message_id = f"msg-{uuid.uuid4()}"
        ambiguity_score = 0.85  # High ambiguity
        ambiguity_type = "insufficient_context"
        
        # Create clarification session
        session = ClarificationSession(
            id=session_id,
            organisation_id=test_organisation_id,
            conversation_id=sample_conversation.id,
            message_id=message_id,
            ambiguity_score=ambiguity_score,
            ambiguity_type=ambiguity_type,
            state=ClarificationState.DETECTING,
        )
        
        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)
        
        # Verify pattern detection
        assert session.ambiguity_type == ambiguity_type, "Ambiguity type should be captured"
        
        # Verify confidence scoring
        assert session.ambiguity_score == ambiguity_score, "Ambiguity score should match"
        assert 0.0 <= session.ambiguity_score <= 1.0, "Ambiguity score should be between 0.0 and 1.0"
        
        # Verify clarification trigger
        assert session.state == ClarificationState.DETECTING, "State should be DETECTING"
        assert session.id is not None, "Session should be created with ID"
    
    def test_qa014_ambiguity_score_validation(self, db_session):
        """
        QA-014: Detect ambiguity - score validation
        
        Verify:
        - Ambiguity score must be between 0.0 and 1.0
        - Invalid scores rejected
        """
        # Valid scores
        ClarificationSession.validate_ambiguity_score(0.0)
        ClarificationSession.validate_ambiguity_score(0.5)
        ClarificationSession.validate_ambiguity_score(1.0)
        
        # Invalid scores
        with pytest.raises(ValueError):
            ClarificationSession.validate_ambiguity_score(-0.1)
        
        with pytest.raises(ValueError):
            ClarificationSession.validate_ambiguity_score(1.1)
    
    def test_qa015_generate_clarifying_questions(self, db_session, sample_clarification_session):
        """
        QA-015: Generate clarifying questions
        
        Verify:
        - Question quality (questions stored)
        - Context inclusion (iteration tracking)
        - Option presentation (questions array)
        """
        # Generate clarifying questions
        questions = [
            "What is the specific module you want to modify?",
            "Do you want to create a new feature or modify existing?",
            "What is your expected timeline?"
        ]
        
        sample_clarification_session.add_clarification_round(questions)
        db_session.commit()
        db_session.refresh(sample_clarification_session)
        
        # Verify questions stored
        assert len(sample_clarification_session.questions) > 0, "Questions should be stored"
        stored_questions = sample_clarification_session.questions[0]
        assert stored_questions["questions"] == questions, "Questions should match"
        
        # Verify context inclusion
        assert "iteration" in stored_questions, "Iteration should be tracked"
        assert stored_questions["iteration"] == 1, "Should be first iteration"
        assert "timestamp" in stored_questions, "Timestamp should be included"
        
        # Verify state transition
        assert sample_clarification_session.state == ClarificationState.ACTIVE, "State should be ACTIVE"
        assert sample_clarification_session.iteration_count == 1, "Iteration count should be 1"
    
    def test_qa016_resolve_clarification(self, db_session, sample_clarification_session):
        """
        QA-016: Resolve clarification
        
        Verify:
        - Sufficient information check (resolved state)
        - Intent transition (resolved intent captured)
        - Resolution criteria (resolved_at timestamp)
        """
        # Add clarification round with response
        questions = ["What module?"]
        response = "Risk Assessment module"
        sample_clarification_session.add_clarification_round(questions, response)
        db_session.commit()
        
        # Resolve clarification with sufficient information
        resolved_intent = {
            "module": "risk-assessment",
            "action": "modify",
            "feature": "assessment_template",
            "confidence": 0.95
        }
        
        before_resolve = datetime.now(timezone.utc).replace(tzinfo=None)
        sample_clarification_session.resolve(resolved_intent)
        db_session.commit()
        db_session.refresh(sample_clarification_session)
        after_resolve = datetime.now(timezone.utc).replace(tzinfo=None)
        
        # Verify sufficient information check
        assert sample_clarification_session.state == ClarificationState.RESOLVED, "State should be RESOLVED"
        
        # Verify intent transition
        final_response = sample_clarification_session.responses[-1]
        assert "resolved_intent" in final_response, "Resolved intent should be captured"
        assert final_response["resolved_intent"] == resolved_intent, "Resolved intent should match"
        
        # Verify resolution criteria
        assert sample_clarification_session.resolved_at is not None, "resolved_at should be set"
        assert before_resolve <= sample_clarification_session.resolved_at <= after_resolve, "resolved_at should be in time window"
    
    def test_qa017_clarification_loop_limits_iteration_count(self, db_session, sample_conversation, test_organisation_id):
        """
        QA-017: Clarification loop limits
        
        Verify:
        - Iteration count tracked
        - Escalation after N loops (default: 3)
        - Structured capture maintained
        """
        # Create session with max iterations
        session = ClarificationSession(
            id=f"clar-{uuid.uuid4()}",
            organisation_id=test_organisation_id,
            conversation_id=sample_conversation.id,
            message_id=f"msg-{uuid.uuid4()}",
            ambiguity_score=0.8,
            state=ClarificationState.ACTIVE,
            max_iterations=3,
        )
        
        db_session.add(session)
        db_session.commit()
        
        # Add clarification rounds up to limit
        for i in range(3):
            questions = [f"Clarification question {i+1}"]
            response = f"User response {i+1}"
            session.add_clarification_round(questions, response)
            db_session.commit()
        
        # Verify iteration count
        assert session.iteration_count == 3, "Iteration count should be 3"
        
        # Try to add one more round (should trigger escalation)
        with pytest.raises(ValueError) as exc_info:
            session.add_clarification_round(["Question 4"])
        
        assert "exceeded max iterations" in str(exc_info.value).lower(), "Error should indicate max iterations exceeded"
        
        # Commit the state change that happened before the exception
        db_session.commit()
        
        # Verify escalation trigger
        db_session.refresh(session)
        assert session.state == ClarificationState.STALLED, "State should be STALLED"
        assert session.stalled_at is not None, "stalled_at should be set"
    
    def test_qa017_clarification_loop_check_stalled(self, db_session, sample_conversation, test_organisation_id):
        """
        QA-017: Clarification loop limits - stall detection
        
        Verify:
        - Stall detection method
        - State transition to STALLED
        - Timestamp capture
        """
        # Create session
        session = ClarificationSession(
            id=f"clar-{uuid.uuid4()}",
            organisation_id=test_organisation_id,
            conversation_id=sample_conversation.id,
            message_id=f"msg-{uuid.uuid4()}",
            ambiguity_score=0.7,
            state=ClarificationState.ACTIVE,
            max_iterations=2,
        )
        
        db_session.add(session)
        db_session.commit()
        
        # Not stalled initially
        assert not session.check_stalled(), "Should not be stalled initially"
        
        # Reach max iterations
        for i in range(2):
            session.add_clarification_round([f"Question {i+1}"])
        
        db_session.commit()
        
        # Check stalled
        assert session.check_stalled(), "Should be stalled after max iterations"
        db_session.commit()
        db_session.refresh(session)
        
        assert session.state == ClarificationState.STALLED, "State should be STALLED"
        assert session.stalled_at is not None, "stalled_at should be set"
    
    def test_qa017_clarification_structured_capture(self, db_session, sample_clarification_session):
        """
        QA-017: Clarification loop structured capture
        
        Verify:
        - All iterations captured
        - Questions and responses preserved
        - Timestamps maintained
        """
        # Add multiple clarification rounds
        rounds = [
            (["Q1a", "Q1b"], "R1"),
            (["Q2a"], "R2"),
            (["Q3a", "Q3b", "Q3c"], "R3"),
        ]
        
        for questions, response in rounds:
            sample_clarification_session.add_clarification_round(questions, response)
            db_session.commit()
        
        db_session.refresh(sample_clarification_session)
        
        # Verify structured capture
        assert len(sample_clarification_session.questions) == 3, "Should have 3 question rounds"
        assert len(sample_clarification_session.responses) == 3, "Should have 3 response rounds"
        
        # Verify iteration tracking
        for i, question_round in enumerate(sample_clarification_session.questions):
            assert question_round["iteration"] == i + 1, f"Iteration {i+1} should be tracked"
            assert "timestamp" in question_round, "Timestamp should be present"
        
        # Verify all data preserved
        assert sample_clarification_session.questions[0]["questions"] == ["Q1a", "Q1b"], "First questions should match"
        assert sample_clarification_session.responses[2]["response"] == "R3", "Last response should match"
    
    def test_qa018_clarification_engine_failure_ambiguity_detection(self, db_session, sample_conversation, test_organisation_id):
        """
        QA-018: Clarification Engine failure modes
        
        Verify:
        - Ambiguity detection failure handling
        - Safe default behavior (assume no ambiguity)
        """
        # Simulate ambiguity detection failure:
        # No session created, safe default assumed
        # In real system, this would be logged as warning
        
        # For data layer test: verify no session required for safe default
        # Query for non-existent session
        message_id = f"msg-{uuid.uuid4()}"
        session = db_session.query(ClarificationSession).filter_by(
            message_id=message_id
        ).first()
        
        # Verify safe default: no session = assume clear
        assert session is None, "No session should exist for safe default (assume clear)"
        
        # If ambiguity detection succeeds later, session can be created
        session = ClarificationSession(
            id=f"clar-{uuid.uuid4()}",
            organisation_id=test_organisation_id,
            conversation_id=sample_conversation.id,
            message_id=message_id,
            ambiguity_score=0.3,  # Low ambiguity (recovered detection)
            state=ClarificationState.DETECTING,
        )
        
        db_session.add(session)
        db_session.commit()
        
        assert session.id is not None, "Session can be created after recovery"
    
    def test_qa018_clarification_engine_failure_storage(self, db_session, sample_conversation, test_organisation_id):
        """
        QA-018: Clarification Engine failure modes
        
        Verify:
        - Clarification storage failure detection
        - Data integrity after failure
        """
        # Create session
        session = ClarificationSession(
            id=f"clar-{uuid.uuid4()}",
            organisation_id=test_organisation_id,
            conversation_id=sample_conversation.id,
            message_id=f"msg-{uuid.uuid4()}",
            ambiguity_score=0.6,
            state=ClarificationState.ACTIVE,
        )
        
        db_session.add(session)
        db_session.commit()
        
        # Add clarification round
        session.add_clarification_round(["Question 1"])
        db_session.commit()
        
        # Verify data persisted
        db_session.refresh(session)
        assert session.iteration_count == 1, "Iteration should be persisted"
        assert len(session.questions) == 1, "Questions should be persisted"
        
        # Simulate partial failure: rollback transaction
        session.add_clarification_round(["Question 2"])
        db_session.rollback()  # Simulate failure
        
        # Verify integrity: previous data still intact
        db_session.refresh(session)
        assert session.iteration_count == 1, "Previous data should be intact after rollback"
        assert len(session.questions) == 1, "Previous questions should be intact"
    
    def test_qa018_clarification_engine_failure_timeout(self, db_session, sample_conversation, test_organisation_id):
        """
        QA-018: Clarification Engine failure modes
        
        Verify:
        - Question generation timeout handling
        - Graceful degradation
        """
        # Simulate timeout scenario:
        # Session created but questions not generated within timeout
        session = ClarificationSession(
            id=f"clar-{uuid.uuid4()}",
            organisation_id=test_organisation_id,
            conversation_id=sample_conversation.id,
            message_id=f"msg-{uuid.uuid4()}",
            ambiguity_score=0.8,
            state=ClarificationState.DETECTING,
        )
        
        db_session.add(session)
        db_session.commit()
        
        # Session exists but no questions yet (timeout before generation)
        db_session.refresh(session)
        assert session.iteration_count == 0, "No iterations yet (timeout)"
        assert len(session.questions) == 0, "No questions generated (timeout)"
        
        # System can recover by generating questions later
        # Or escalate if timeout persists
        
        # For this test: verify session can be marked as stalled
        session.state = ClarificationState.STALLED
        session.stalled_at = datetime.now(timezone.utc).replace(tzinfo=None)
        db_session.commit()
        
        db_session.refresh(session)
        assert session.state == ClarificationState.STALLED, "Can mark as stalled after timeout"
