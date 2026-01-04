"""
Wave 1.0 UI Tests Configuration

Fixtures and configuration for UI builder tests (QA-019 to QA-057).
"""

import pytest
from pathlib import Path
from typing import Dict, Any


@pytest.fixture
def ui_test_context():
    """Provides base context for UI tests."""
    return {
        "organisation_id": "test-org-001",
        "user_id": "test-user-001",
        "session_id": "test-session-001"
    }


@pytest.fixture
def conversation_data():
    """Sample conversation data for testing."""
    return {
        "conversationId": "conv-001",
        "organisationId": "test-org-001",
        "participantJohan": "test-user-001",
        "participantFM": "foreman",
        "status": "active",
        "createdAt": "2026-01-01T00:00:00Z",
        "messages": [
            {
                "messageId": "msg-001",
                "conversationId": "conv-001",
                "sender": "test-user-001",
                "senderRole": "Johan",
                "content": "Hello, I need help with a task",
                "timestamp": "2026-01-01T00:00:00Z",
                "status": "read"
            },
            {
                "messageId": "msg-002",
                "conversationId": "conv-001",
                "sender": "foreman",
                "senderRole": "FM",
                "content": "I understand. What task do you need help with?",
                "timestamp": "2026-01-01T00:01:00Z",
                "status": "read"
            }
        ]
    }


@pytest.fixture
def domain_status_data():
    """Sample domain status data for testing."""
    return {
        "Governance Integrity": {
            "status": "GREEN",
            "reason": "All governance rules enforced",
            "timestamp": "2026-01-01T00:00:00Z"
        },
        "Build Execution": {
            "status": "AMBER",
            "reason": "Build in progress, one warning detected",
            "timestamp": "2026-01-01T00:00:00Z"
        },
        "QA & Test Coverage": {
            "status": "RED",
            "reason": "Test coverage below 80% threshold",
            "timestamp": "2026-01-01T00:00:00Z"
        }
    }


@pytest.fixture
def parked_items_data():
    """Sample parked items data for testing."""
    return [
        {
            "itemId": "park-001",
            "organisationId": "test-org-001",
            "title": "Enhancement: Add dark mode support",
            "content": "Consider adding dark mode to improve accessibility",
            "category": "enhancement",
            "status": "parked",
            "reason": "Deferred to future iteration",
            "parkedAt": "2026-01-01T00:00:00Z",
            "parkedBy": "foreman"
        },
        {
            "itemId": "park-002",
            "organisationId": "test-org-001",
            "title": "Idea: Implement caching layer",
            "content": "Add Redis caching for frequently accessed data",
            "category": "performance",
            "status": "parked",
            "reason": "Not authorized for current wave",
            "parkedAt": "2026-01-01T00:00:00Z",
            "parkedBy": "foreman"
        }
    ]


@pytest.fixture
def build_progress_data():
    """Sample build progress data for testing."""
    return {
        "currentWave": "1.0",
        "totalQA": 210,
        "greenQA": 85,
        "redQA": 125,
        "progressPercentage": 40.5,
        "builders": [
            {
                "name": "schema-builder",
                "status": "complete",
                "assignedQA": "QA-001 to QA-018",
                "greenCount": 18,
                "totalCount": 18
            },
            {
                "name": "ui-builder",
                "status": "in_progress",
                "assignedQA": "QA-019 to QA-057",
                "greenCount": 10,
                "totalCount": 39
            }
        ]
    }


@pytest.fixture
def escalation_data():
    """Sample escalation data for testing."""
    return [
        {
            "escalationId": "esc-001",
            "organisationId": "test-org-001",
            "title": "Build blocked: dependency missing",
            "priority": "HIGH",
            "status": "pending",
            "context": {
                "builder": "ui-builder",
                "blockedOn": "schema-builder",
                "reason": "Missing data model definition"
            },
            "createdAt": "2026-01-01T00:00:00Z",
            "escalatedBy": "ui-builder"
        },
        {
            "escalationId": "esc-002",
            "organisationId": "test-org-001",
            "title": "Test failure: repeated UI render error",
            "priority": "MEDIUM",
            "status": "acknowledged",
            "context": {
                "component": "ConversationUIRenderer",
                "errorCount": 5,
                "timeWindow": "1 minute"
            },
            "createdAt": "2026-01-01T00:05:00Z",
            "escalatedBy": "conversation-ui-renderer"
        }
    ]
