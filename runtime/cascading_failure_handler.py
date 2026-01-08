"""
Cascading Failure Handler

Purpose: Detect and handle cascading component failures with circuit breakers and isolation
Authority: Wave 2.0 Subwave 2.8 - Full Watchdog Coverage (QA-396)
Tenant Isolation: All operations scoped by organisation_id
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta


class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"      # Failures detected, circuit open
    HALF_OPEN = "half_open"  # Testing recovery


@dataclass
class FailureRecord:
    """Record of a component failure"""
    component_id: str
    failure_message: str
    timestamp: datetime
    organisation_id: str
    caused_by: Optional[str] = None  # Parent component if cascading


@dataclass
class CircuitBreaker:
    """Circuit breaker for component failure management"""
    component_id: str
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    failure_threshold: int = 3
    last_failure_time: Optional[datetime] = None
    reset_timeout_seconds: int = 60
    
    def record_failure(self) -> None:
        """Record a failure and update state"""
        self.failure_count += 1
        self.last_failure_time = datetime.now(UTC)
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
    
    def can_attempt(self) -> bool:
        """Check if operation can be attempted"""
        if self.state == CircuitState.CLOSED:
            return True
        
        if self.state == CircuitState.OPEN:
            # Check if timeout elapsed for half-open attempt
            if self.last_failure_time:
                elapsed = (datetime.now(UTC) - self.last_failure_time).total_seconds()
                if elapsed >= self.reset_timeout_seconds:
                    self.state = CircuitState.HALF_OPEN
                    return True
            return False
        
        # HALF_OPEN state: allow single attempt
        return True
    
    def record_success(self) -> None:
        """Record a successful operation"""
        if self.state == CircuitState.HALF_OPEN:
            # Recovery successful
            self.state = CircuitState.CLOSED
            self.failure_count = 0


class ComponentIsolationManager:
    """Manages isolation of failed components"""
    
    def __init__(self):
        self._isolated_components: Dict[str, datetime] = {}
    
    def isolate_component(self, component_id: str) -> None:
        """Isolate a component"""
        self._isolated_components[component_id] = datetime.now(UTC)
    
    def is_component_isolated(self, component_id: str) -> bool:
        """Check if component is isolated"""
        return component_id in self._isolated_components
    
    def release_component(self, component_id: str) -> None:
        """Release a component from isolation"""
        if component_id in self._isolated_components:
            del self._isolated_components[component_id]
    
    def get_isolated_components(self) -> List[str]:
        """Get list of isolated components"""
        return list(self._isolated_components.keys())


@dataclass
class Escalation:
    """Escalation record"""
    escalation_id: str
    escalation_type: str
    severity: str
    organisation_id: str
    timestamp: datetime
    details: Dict[str, Any]


class FailureEscalator:
    """Manages escalation of failures"""
    
    def __init__(self):
        self._escalations: Dict[str, List[Escalation]] = {}
    
    def escalate(
        self,
        escalation_type: str,
        organisation_id: str,
        severity: str = "high",
        details: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create an escalation"""
        escalation_id = f"esc_{organisation_id}_{int(datetime.now(UTC).timestamp())}"
        
        escalation = Escalation(
            escalation_id=escalation_id,
            escalation_type=escalation_type,
            severity=severity,
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
                "severity": e.severity,
                "timestamp": e.timestamp.isoformat(),
                "details": e.details
            }
            for e in self._escalations[organisation_id]
        ]


class CascadingFailureHandler:
    """
    Handles cascading component failures
    
    Responsibilities:
    - Detect cascading failures
    - Activate circuit breakers
    - Isolate failed components
    - Escalate critical failures
    """
    
    def __init__(self, organisation_id: str):
        self.organisation_id = organisation_id
        self._failure_records: List[FailureRecord] = []
        self._circuit_breakers: Dict[str, CircuitBreaker] = {}
        self._isolation_manager = ComponentIsolationManager()
        self._escalator = FailureEscalator()
    
    def record_failure(self, component_id: str, failure_message: str) -> None:
        """Record a component failure"""
        record = FailureRecord(
            component_id=component_id,
            failure_message=failure_message,
            timestamp=datetime.now(UTC),
            organisation_id=self.organisation_id
        )
        self._failure_records.append(record)
        
        # Update circuit breaker
        circuit_breaker = self._get_or_create_circuit_breaker(component_id)
        circuit_breaker.record_failure()
    
    def record_cascading_failure(
        self,
        component_id: str,
        caused_by: str,
        failure_message: str
    ) -> None:
        """Record a cascading failure"""
        record = FailureRecord(
            component_id=component_id,
            failure_message=failure_message,
            timestamp=datetime.now(UTC),
            organisation_id=self.organisation_id,
            caused_by=caused_by
        )
        self._failure_records.append(record)
        
        # Update circuit breaker
        circuit_breaker = self._get_or_create_circuit_breaker(component_id)
        circuit_breaker.record_failure()
        
        # Check if cascading failure threshold reached
        if self.is_cascading_failure_detected():
            self._activate_isolation()
            self._escalate_cascading_failure()
    
    def is_cascading_failure_detected(self) -> bool:
        """Detect if cascading failure is occurring"""
        # Check if we have failures with causal relationships
        cascading_failures = [
            r for r in self._failure_records
            if r.caused_by is not None
        ]
        
        # If we have 2 or more cascading failures, it's a cascade
        return len(cascading_failures) >= 2
    
    def _activate_isolation(self) -> None:
        """Activate component isolation for cascade"""
        # Isolate all components involved in cascade
        for record in self._failure_records:
            self._isolation_manager.isolate_component(record.component_id)
            # Open circuit breakers for all components in cascade
            circuit_breaker = self._get_or_create_circuit_breaker(record.component_id)
            # Force circuit to open for cascading failures
            if circuit_breaker.state != CircuitState.OPEN:
                circuit_breaker.failure_count = circuit_breaker.failure_threshold
                circuit_breaker.state = CircuitState.OPEN
    
    def _escalate_cascading_failure(self) -> None:
        """Escalate cascading failure"""
        cascade_components = [
            r.component_id for r in self._failure_records
            if r.caused_by is not None
        ]
        
        self._escalator.escalate(
            escalation_type="cascading_failure",
            organisation_id=self.organisation_id,
            severity="critical",
            details={
                "cascade_components": cascade_components,
                "cascade_depth": len(cascade_components)
            }
        )
    
    def _get_or_create_circuit_breaker(self, component_id: str) -> CircuitBreaker:
        """Get or create circuit breaker for component"""
        if component_id not in self._circuit_breakers:
            self._circuit_breakers[component_id] = CircuitBreaker(
                component_id=component_id
            )
        return self._circuit_breakers[component_id]
    
    def get_circuit_breaker(self, component_id: str) -> CircuitBreaker:
        """Get circuit breaker for component"""
        return self._get_or_create_circuit_breaker(component_id)
    
    def get_isolation_manager(self) -> ComponentIsolationManager:
        """Get isolation manager"""
        return self._isolation_manager
    
    def get_escalator(self) -> FailureEscalator:
        """Get escalator"""
        return self._escalator
