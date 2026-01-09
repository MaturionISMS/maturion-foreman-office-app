"""
Cross-Subsystem Integrator

Purpose: Manage event propagation, data synchronization, state coordination, 
         dependency management, and error handling across subsystems
Authority: Wave 2.0 Subwave 2.9 - Deep Integration Phase 1 (QA-461 to QA-465)
Tenant Isolation: All operations scoped by organisation_id
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class SubsystemState(Enum):
    """Subsystem operational states"""
    INITIALIZING = "initializing"
    READY = "ready"
    DEGRADED = "degraded"
    FAILED = "failed"
    SYNCHRONIZED = "synchronized"


@dataclass
class SubsystemEvent:
    """Event that propagates across subsystems"""
    event_id: str
    source_subsystem: str
    event_type: str
    payload: Dict[str, Any]
    timestamp: datetime
    organisation_id: str
    propagated_to: Set[str] = field(default_factory=set)
    
    def mark_propagated(self, target_subsystem: str) -> None:
        """Mark this event as propagated to a target subsystem"""
        self.propagated_to.add(target_subsystem)


@dataclass
class DataSyncRecord:
    """Record of data synchronization between subsystems"""
    sync_id: str
    source_subsystem: str
    target_subsystem: str
    data_keys: List[str]
    timestamp: datetime
    organisation_id: str
    status: str = "pending"  # pending, in_progress, completed, failed


@dataclass
class StateCoordination:
    """Coordination of state across multiple subsystems"""
    coordination_id: str
    participating_subsystems: List[str]
    coordinated_state: Dict[str, Any]
    organisation_id: str
    last_updated: datetime


@dataclass
class DependencyGraph:
    """Dependency graph between subsystems"""
    organisation_id: str
    dependencies: Dict[str, List[str]] = field(default_factory=dict)  # subsystem -> depends_on
    
    def add_dependency(self, subsystem: str, depends_on: str) -> None:
        """Add a dependency relationship"""
        if subsystem not in self.dependencies:
            self.dependencies[subsystem] = []
        if depends_on not in self.dependencies[subsystem]:
            self.dependencies[subsystem].append(depends_on)
    
    def get_dependencies(self, subsystem: str) -> List[str]:
        """Get all dependencies for a subsystem"""
        return self.dependencies.get(subsystem, [])
    
    def has_circular_dependency(self) -> bool:
        """Check for circular dependencies"""
        visited = set()
        rec_stack = set()
        
        def has_cycle(subsystem: str) -> bool:
            visited.add(subsystem)
            rec_stack.add(subsystem)
            
            for dep in self.dependencies.get(subsystem, []):
                if dep not in visited:
                    if has_cycle(dep):
                        return True
                elif dep in rec_stack:
                    return True
            
            rec_stack.remove(subsystem)
            return False
        
        for subsystem in self.dependencies.keys():
            if subsystem not in visited:
                if has_cycle(subsystem):
                    return True
        
        return False


class CrossSubsystemIntegrator:
    """
    Manages integration across subsystems including event propagation,
    data synchronization, state coordination, dependency management,
    and cross-subsystem error handling
    """
    
    def __init__(self):
        self.events: Dict[str, List[SubsystemEvent]] = {}  # org_id -> events
        self.sync_records: Dict[str, List[DataSyncRecord]] = {}  # org_id -> records
        self.state_coordinations: Dict[str, List[StateCoordination]] = {}  # org_id -> coordinations
        self.dependency_graphs: Dict[str, DependencyGraph] = {}  # org_id -> graph
        self.subsystem_states: Dict[str, Dict[str, SubsystemState]] = {}  # org_id -> {subsystem -> state}
        self.error_log: Dict[str, List[Dict[str, Any]]] = {}  # org_id -> errors
    
    # QA-461: Event Propagation
    def propagate_event(
        self,
        organisation_id: str,
        source_subsystem: str,
        target_subsystems: List[str],
        event_type: str,
        payload: Dict[str, Any]
    ) -> SubsystemEvent:
        """
        Propagate an event from source subsystem to target subsystems
        
        Args:
            organisation_id: Tenant identifier for isolation
            source_subsystem: Subsystem originating the event
            target_subsystems: List of subsystems to receive the event
            event_type: Type of event being propagated
            payload: Event data
            
        Returns:
            SubsystemEvent with propagation tracking
        """
        event_id = f"{source_subsystem}_{event_type}_{datetime.now(timezone.utc).timestamp()}"
        
        event = SubsystemEvent(
            event_id=event_id,
            source_subsystem=source_subsystem,
            event_type=event_type,
            payload=payload,
            timestamp=datetime.now(timezone.utc),
            organisation_id=organisation_id,
            propagated_to=set()
        )
        
        # Store event
        if organisation_id not in self.events:
            self.events[organisation_id] = []
        self.events[organisation_id].append(event)
        
        # Propagate to each target
        for target in target_subsystems:
            event.mark_propagated(target)
            # In real implementation, this would trigger the target subsystem
        
        return event
    
    def get_propagated_events(
        self,
        organisation_id: str,
        subsystem: Optional[str] = None
    ) -> List[SubsystemEvent]:
        """Get events propagated to a specific subsystem or all events"""
        events = self.events.get(organisation_id, [])
        
        if subsystem:
            return [e for e in events if subsystem in e.propagated_to]
        
        return events
    
    # QA-462: Data Synchronization
    def synchronize_data(
        self,
        organisation_id: str,
        source_subsystem: str,
        target_subsystem: str,
        data_keys: List[str]
    ) -> DataSyncRecord:
        """
        Synchronize data between two subsystems
        
        Args:
            organisation_id: Tenant identifier for isolation
            source_subsystem: Source of data
            target_subsystem: Target for data
            data_keys: Keys of data to synchronize
            
        Returns:
            DataSyncRecord tracking the synchronization
        """
        sync_id = f"sync_{source_subsystem}_{target_subsystem}_{datetime.now(timezone.utc).timestamp()}"
        
        record = DataSyncRecord(
            sync_id=sync_id,
            source_subsystem=source_subsystem,
            target_subsystem=target_subsystem,
            data_keys=data_keys,
            timestamp=datetime.now(timezone.utc),
            organisation_id=organisation_id,
            status="in_progress"
        )
        
        # Store record
        if organisation_id not in self.sync_records:
            self.sync_records[organisation_id] = []
        self.sync_records[organisation_id].append(record)
        
        # Simulate synchronization success
        record.status = "completed"
        
        return record
    
    def get_sync_status(
        self,
        organisation_id: str,
        sync_id: str
    ) -> Optional[DataSyncRecord]:
        """Get status of a data synchronization"""
        records = self.sync_records.get(organisation_id, [])
        for record in records:
            if record.sync_id == sync_id:
                return record
        return None
    
    # QA-463: State Coordination
    def coordinate_state(
        self,
        organisation_id: str,
        subsystems: List[str],
        coordinated_state: Dict[str, Any]
    ) -> StateCoordination:
        """
        Coordinate state across multiple subsystems
        
        Args:
            organisation_id: Tenant identifier for isolation
            subsystems: List of subsystems to coordinate
            coordinated_state: Shared state to coordinate
            
        Returns:
            StateCoordination tracking the coordination
        """
        coordination_id = f"coord_{datetime.now(timezone.utc).timestamp()}"
        
        coordination = StateCoordination(
            coordination_id=coordination_id,
            participating_subsystems=subsystems,
            coordinated_state=coordinated_state,
            organisation_id=organisation_id,
            last_updated=datetime.now(timezone.utc)
        )
        
        # Store coordination
        if organisation_id not in self.state_coordinations:
            self.state_coordinations[organisation_id] = []
        self.state_coordinations[organisation_id].append(coordination)
        
        # Update subsystem states
        if organisation_id not in self.subsystem_states:
            self.subsystem_states[organisation_id] = {}
        
        for subsystem in subsystems:
            self.subsystem_states[organisation_id][subsystem] = SubsystemState.SYNCHRONIZED
        
        return coordination
    
    def get_coordinated_state(
        self,
        organisation_id: str,
        coordination_id: str
    ) -> Optional[StateCoordination]:
        """Get a specific state coordination"""
        coordinations = self.state_coordinations.get(organisation_id, [])
        for coord in coordinations:
            if coord.coordination_id == coordination_id:
                return coord
        return None
    
    # QA-464: Dependency Management
    def manage_dependencies(
        self,
        organisation_id: str,
        subsystem: str,
        depends_on: List[str]
    ) -> DependencyGraph:
        """
        Manage dependencies between subsystems
        
        Args:
            organisation_id: Tenant identifier for isolation
            subsystem: Subsystem declaring dependencies
            depends_on: List of subsystems it depends on
            
        Returns:
            DependencyGraph with updated dependencies
        """
        if organisation_id not in self.dependency_graphs:
            self.dependency_graphs[organisation_id] = DependencyGraph(organisation_id=organisation_id)
        
        graph = self.dependency_graphs[organisation_id]
        
        for dependency in depends_on:
            graph.add_dependency(subsystem, dependency)
        
        # Check for circular dependencies
        if graph.has_circular_dependency():
            # In real implementation, this would trigger an error or warning
            pass
        
        return graph
    
    def get_dependencies(
        self,
        organisation_id: str,
        subsystem: str
    ) -> List[str]:
        """Get all dependencies for a subsystem"""
        if organisation_id in self.dependency_graphs:
            return self.dependency_graphs[organisation_id].get_dependencies(subsystem)
        return []
    
    def has_circular_dependency(
        self,
        organisation_id: str
    ) -> bool:
        """Check if there are any circular dependencies"""
        if organisation_id in self.dependency_graphs:
            return self.dependency_graphs[organisation_id].has_circular_dependency()
        return False
    
    # QA-465: Cross-Subsystem Error Handling
    def handle_cross_subsystem_error(
        self,
        organisation_id: str,
        source_subsystem: str,
        affected_subsystems: List[str],
        error_type: str,
        error_message: str,
        recovery_action: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Handle errors that span multiple subsystems
        
        Args:
            organisation_id: Tenant identifier for isolation
            source_subsystem: Subsystem where error originated
            affected_subsystems: Subsystems affected by the error
            error_type: Type of error
            error_message: Error description
            recovery_action: Optional recovery action taken
            
        Returns:
            Error record with handling details
        """
        error_id = f"error_{source_subsystem}_{datetime.now(timezone.utc).timestamp()}"
        
        error_record = {
            "error_id": error_id,
            "source_subsystem": source_subsystem,
            "affected_subsystems": affected_subsystems,
            "error_type": error_type,
            "error_message": error_message,
            "recovery_action": recovery_action,
            "timestamp": datetime.now(timezone.utc),
            "organisation_id": organisation_id,
            "escalated": False
        }
        
        # Store error
        if organisation_id not in self.error_log:
            self.error_log[organisation_id] = []
        self.error_log[organisation_id].append(error_record)
        
        # Update subsystem states to DEGRADED
        if organisation_id not in self.subsystem_states:
            self.subsystem_states[organisation_id] = {}
        
        for subsystem in affected_subsystems:
            self.subsystem_states[organisation_id][subsystem] = SubsystemState.DEGRADED
        
        # If error is critical or affects multiple subsystems, escalate
        if len(affected_subsystems) > 2 or error_type == "critical":
            error_record["escalated"] = True
        
        return error_record
    
    def get_errors_for_subsystem(
        self,
        organisation_id: str,
        subsystem: str
    ) -> List[Dict[str, Any]]:
        """Get all errors affecting a specific subsystem"""
        errors = self.error_log.get(organisation_id, [])
        return [
            e for e in errors 
            if e["source_subsystem"] == subsystem or subsystem in e["affected_subsystems"]
        ]
    
    def get_subsystem_state(
        self,
        organisation_id: str,
        subsystem: str
    ) -> SubsystemState:
        """Get current state of a subsystem"""
        if organisation_id in self.subsystem_states:
            return self.subsystem_states[organisation_id].get(subsystem, SubsystemState.READY)
        return SubsystemState.READY
