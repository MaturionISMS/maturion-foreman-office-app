"""
Race Condition Handler

Purpose: Detect and handle race conditions with retry strategies
Authority: Wave 2.0 Subwave 2.8 - Full Watchdog Coverage (QA-398)
Tenant Isolation: All operations scoped by organisation_id
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import threading


@dataclass
class AccessAttempt:
    """Record of a resource access attempt"""
    resource_id: str
    accessor_id: str
    operation: str
    timestamp: datetime
    organisation_id: str


@dataclass
class Escalation:
    """Escalation record"""
    escalation_id: str
    escalation_type: str
    organisation_id: str
    timestamp: datetime
    details: Dict[str, Any]


class RaceDetector:
    """Detects race conditions on resources"""
    
    def __init__(self):
        self._access_attempts: Dict[str, List[AccessAttempt]] = {}
        self._lock = threading.Lock()
    
    def record_access(self, attempt: AccessAttempt) -> None:
        """Record an access attempt"""
        with self._lock:
            if attempt.resource_id not in self._access_attempts:
                self._access_attempts[attempt.resource_id] = []
            self._access_attempts[attempt.resource_id].append(attempt)
    
    def is_race_detected(self, resource_id: str, time_window_ms: int = 100) -> bool:
        """
        Detect if race condition exists
        
        Race detected if multiple write operations attempted concurrently
        """
        with self._lock:
            if resource_id not in self._access_attempts:
                return False
            
            attempts = self._access_attempts[resource_id]
            
            # Check for concurrent write operations
            write_attempts = [a for a in attempts if a.operation == "write"]
            
            if len(write_attempts) < 2:
                return False
            
            # Check if they're within time window
            write_attempts.sort(key=lambda a: a.timestamp)
            
            for i in range(len(write_attempts) - 1):
                time_diff = (write_attempts[i + 1].timestamp - write_attempts[i].timestamp).total_seconds() * 1000
                if time_diff < time_window_ms:
                    return True
            
            return False


class RetryStrategy:
    """Manages retry logic with exponential backoff"""
    
    def __init__(
        self,
        max_retries: int = 5,
        initial_backoff_ms: int = 100,
        backoff_multiplier: float = 2.0
    ):
        self.max_retries = max_retries
        self.initial_backoff_ms = initial_backoff_ms
        self.backoff_multiplier = backoff_multiplier
        self._retry_counts: Dict[str, Dict[str, int]] = {}  # resource -> accessor -> count
    
    def retry(
        self,
        resource_id: str,
        accessor_id: str,
        operation: str,
        attempt: int
    ) -> Dict[str, Any]:
        """
        Determine if retry should occur and calculate backoff
        
        Returns:
        - should_retry: bool
        - backoff_ms: int
        """
        if attempt >= self.max_retries:
            return {
                "should_retry": False,
                "backoff_ms": 0,
                "reason": "max_retries_exceeded"
            }
        
        # Calculate exponential backoff
        backoff_ms = int(self.initial_backoff_ms * (self.backoff_multiplier ** (attempt - 1)))
        
        # Record retry count
        if resource_id not in self._retry_counts:
            self._retry_counts[resource_id] = {}
        self._retry_counts[resource_id][accessor_id] = attempt
        
        return {
            "should_retry": True,
            "backoff_ms": backoff_ms,
            "attempt": attempt
        }
    
    def get_retry_count(self, resource_id: str, accessor_id: str) -> int:
        """Get current retry count"""
        if resource_id not in self._retry_counts:
            return 0
        if accessor_id not in self._retry_counts[resource_id]:
            return 0
        return self._retry_counts[resource_id][accessor_id]


class RaceEscalator:
    """Manages escalation of persistent race conditions"""
    
    def __init__(self):
        self._escalations: Dict[str, List[Escalation]] = {}
    
    def escalate(
        self,
        escalation_type: str,
        organisation_id: str,
        details: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create an escalation"""
        escalation_id = f"esc_{organisation_id}_{int(datetime.now(UTC).timestamp())}"
        
        escalation = Escalation(
            escalation_id=escalation_id,
            escalation_type=escalation_type,
            organisation_id=organisation_id,
            timestamp=datetime.now(UTC),
            details=details or {}
        )
        
        if organisation_id not in self._escalations:
            self._escalations[organisation_id] = []
        
        self._escalations[organisation_id].append(escalation)
        return escalation_id
    
    def get_escalations(self, organisation_id: str) -> List[Dict[str, Any]]:
        """Get escalations for an organisation"""
        if organisation_id not in self._escalations:
            return []
        
        return [
            {
                "escalation_id": e.escalation_id,
                "type": e.escalation_type,
                "timestamp": e.timestamp.isoformat(),
                "details": e.details
            }
            for e in self._escalations[organisation_id]
        ]


class RaceConditionHandler:
    """
    Handles race conditions with detection and retry
    
    Responsibilities:
    - Detect concurrent access conflicts
    - Apply retry strategies with backoff
    - Escalate persistent race conditions
    - Maintain tenant isolation
    """
    
    def __init__(self, organisation_id: str):
        self.organisation_id = organisation_id
        self._race_detector = RaceDetector()
        self._retry_strategy = RetryStrategy()
        self._escalator = RaceEscalator()
    
    def attempt_access(
        self,
        resource_id: str,
        accessor_id: str,
        operation: str
    ) -> Dict[str, Any]:
        """
        Attempt to access a resource
        
        Returns access result with race detection info
        """
        attempt = AccessAttempt(
            resource_id=resource_id,
            accessor_id=accessor_id,
            operation=operation,
            timestamp=datetime.now(UTC),
            organisation_id=self.organisation_id
        )
        
        self._race_detector.record_access(attempt)
        
        return {
            "resource_id": resource_id,
            "accessor_id": accessor_id,
            "operation": operation,
            "timestamp": attempt.timestamp.isoformat()
        }
    
    def get_race_detector(self) -> RaceDetector:
        """Get race detector"""
        return self._race_detector
    
    def get_retry_strategy(self) -> RetryStrategy:
        """Get retry strategy"""
        return self._retry_strategy
    
    def get_escalator(self) -> RaceEscalator:
        """Get escalator"""
        return self._escalator
    
    def escalate_persistent_race(
        self,
        resource_id: str,
        accessor_id: str
    ) -> str:
        """Escalate a persistent race condition"""
        return self._escalator.escalate(
            escalation_type="race_condition_persistent",
            organisation_id=self.organisation_id,
            details={
                "resource_id": resource_id,
                "accessor_id": accessor_id,
                "retry_count": self._retry_strategy.get_retry_count(resource_id, accessor_id)
            }
        )
