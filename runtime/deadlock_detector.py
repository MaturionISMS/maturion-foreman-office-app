"""
Deadlock Detector

Purpose: Detect and recover from deadlock conditions
Authority: Wave 2.0 Subwave 2.8 - Full Watchdog Coverage (QA-397)
Tenant Isolation: All operations scoped by organisation_id
"""

from enum import Enum
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import threading


class DeadlockStatus(Enum):
    """Deadlock detection status"""
    NONE = "none"
    DETECTED = "detected"
    RECOVERING = "recovering"
    RECOVERED = "recovered"


@dataclass
class LockRequest:
    """Lock request record"""
    resource_id: str
    holder_id: str
    requested_at: datetime
    granted: bool = False
    lock_id: Optional[str] = None


@dataclass
class ResourceLock:
    """Resource lock state"""
    resource_id: str
    holder_id: str
    lock_id: str
    acquired_at: datetime
    organisation_id: str


class TimeoutManager:
    """Manages timeouts for lock operations"""
    
    def __init__(self, timeout_seconds: int = 30):
        self.timeout_seconds = timeout_seconds
        self._lock_requests: Dict[str, LockRequest] = {}
    
    def record_request(self, resource_id: str, holder_id: str) -> None:
        """Record a lock request"""
        request_key = f"{resource_id}:{holder_id}"
        self._lock_requests[request_key] = LockRequest(
            resource_id=resource_id,
            holder_id=holder_id,
            requested_at=datetime.now(UTC)
        )
    
    def has_timeout_occurred(self, resource_id: str, holder_id: str) -> bool:
        """Check if timeout has occurred for a request"""
        request_key = f"{resource_id}:{holder_id}"
        if request_key not in self._lock_requests:
            return False
        
        request = self._lock_requests[request_key]
        elapsed = (datetime.now(UTC) - request.requested_at).total_seconds()
        return elapsed > self.timeout_seconds


@dataclass
class Escalation:
    """Escalation record"""
    escalation_id: str
    escalation_type: str
    organisation_id: str
    timestamp: datetime
    details: Dict[str, Any]


class DeadlockRecovery:
    """Handles recovery from deadlocks"""
    
    def __init__(self, detector: 'DeadlockDetector'):
        self._recovery_history: List[Dict[str, Any]] = []
        self._detector = detector
    
    def recover_from_deadlock(
        self,
        resources: List[str],
        holders: List[str]
    ) -> Dict[str, Any]:
        """
        Recover from deadlock by releasing locks
        
        Strategy: Release all locks in deadlock cycle
        """
        recovery_id = f"recovery_{int(datetime.now(UTC).timestamp())}"
        
        # Release all locks
        for resource_id in resources:
            for holder_id in holders:
                self._detector.release_lock(resource_id, holder_id)
        
        recovery_record = {
            "recovery_id": recovery_id,
            "status": "recovered",
            "resources_released": resources,
            "holders_released": holders,
            "timestamp": datetime.now(UTC).isoformat()
        }
        
        self._recovery_history.append(recovery_record)
        return recovery_record


class DeadlockDetector:
    """
    Detects and recovers from deadlocks
    
    Responsibilities:
    - Track resource locks
    - Detect circular wait conditions
    - Manage timeouts
    - Coordinate recovery
    - Escalate unrecoverable deadlocks
    """
    
    def __init__(self, organisation_id: str, timeout_seconds: int = 30):
        self.organisation_id = organisation_id
        self.timeout_seconds = timeout_seconds
        self._locks: Dict[str, ResourceLock] = {}
        self._lock_requests: Dict[str, List[str]] = {}  # resource -> list of waiting holders
        self._timeout_manager = TimeoutManager(timeout_seconds)
        self._recovery = DeadlockRecovery(self)
        self._escalations: List[Escalation] = []
        self._lock_counter = 0
        self._lock = threading.Lock()
    
    def acquire_lock(self, resource_id: str, holder_id: str) -> Optional[str]:
        """
        Acquire a lock on a resource
        
        Returns lock_id if successful, None if resource already locked
        """
        with self._lock:
            lock_key = f"{resource_id}"
            
            # Check if resource is already locked
            if lock_key in self._locks:
                # Resource is locked by someone else
                if self._locks[lock_key].holder_id != holder_id:
                    return None
                # Already held by this holder
                return self._locks[lock_key].lock_id
            
            # Grant lock
            self._lock_counter += 1
            lock_id = f"lock_{self.organisation_id}_{self._lock_counter}"
            
            self._locks[lock_key] = ResourceLock(
                resource_id=resource_id,
                holder_id=holder_id,
                lock_id=lock_id,
                acquired_at=datetime.now(UTC),
                organisation_id=self.organisation_id
            )
            
            return lock_id
    
    def request_lock(self, resource_id: str, holder_id: str) -> None:
        """Record a lock request (waiting)"""
        with self._lock:
            if resource_id not in self._lock_requests:
                self._lock_requests[resource_id] = []
            
            if holder_id not in self._lock_requests[resource_id]:
                self._lock_requests[resource_id].append(holder_id)
        
        self._timeout_manager.record_request(resource_id, holder_id)
    
    def release_lock(self, resource_id: str, holder_id: str) -> bool:
        """Release a lock"""
        with self._lock:
            lock_key = f"{resource_id}"
            
            if lock_key not in self._locks:
                return False
            
            if self._locks[lock_key].holder_id != holder_id:
                return False
            
            del self._locks[lock_key]
            
            # Remove from waiting list if present
            if resource_id in self._lock_requests and holder_id in self._lock_requests[resource_id]:
                self._lock_requests[resource_id].remove(holder_id)
            
            return True
    
    def is_lock_held(self, resource_id: str, holder_id: str) -> bool:
        """Check if a lock is held by holder"""
        with self._lock:
            lock_key = f"{resource_id}"
            if lock_key not in self._locks:
                return False
            return self._locks[lock_key].holder_id == holder_id
    
    def detect_deadlock(self) -> DeadlockStatus:
        """
        Detect if deadlock exists
        
        Uses cycle detection in wait-for graph
        """
        with self._lock:
            # Build wait-for graph
            # holder -> list of resources they're waiting for
            wait_for: Dict[str, Set[str]] = {}
            
            # holder -> list of resources they hold
            holds: Dict[str, Set[str]] = {}
            
            # Build holds mapping
            for lock_key, lock in self._locks.items():
                if lock.holder_id not in holds:
                    holds[lock.holder_id] = set()
                holds[lock.holder_id].add(lock.resource_id)
            
            # Build wait-for mapping
            for resource_id, waiting_holders in self._lock_requests.items():
                for holder_id in waiting_holders:
                    if holder_id not in wait_for:
                        wait_for[holder_id] = set()
                    wait_for[holder_id].add(resource_id)
            
            # Check for cycles
            # If holder A waits for resource X held by holder B,
            # and holder B waits for resource Y held by holder A,
            # we have a deadlock
            
            for waiting_holder, waited_resources in wait_for.items():
                for resource in waited_resources:
                    # Find who holds this resource
                    holder = None
                    for h, resources in holds.items():
                        if resource in resources:
                            holder = h
                            break
                    
                    if holder and holder in wait_for:
                        # Check if holder waits for something that waiting_holder holds
                        holder_waiting_for = wait_for[holder]
                        if waiting_holder in holds:
                            waiting_holder_resources = holds[waiting_holder]
                            if holder_waiting_for & waiting_holder_resources:
                                # Cycle detected!
                                return DeadlockStatus.DETECTED
            
            return DeadlockStatus.NONE
    
    def get_timeout_manager(self) -> TimeoutManager:
        """Get timeout manager"""
        return self._timeout_manager
    
    def get_recovery(self) -> DeadlockRecovery:
        """Get recovery manager"""
        return self._recovery
    
    def record_unrecoverable_deadlock(self, *resources: str) -> None:
        """Record an unrecoverable deadlock for escalation"""
        escalation = Escalation(
            escalation_id=f"esc_{self.organisation_id}_{int(datetime.now(UTC).timestamp())}",
            escalation_type="deadlock_unrecoverable",
            organisation_id=self.organisation_id,
            timestamp=datetime.now(UTC),
            details={
                "resources": list(resources)
            }
        )
        self._escalations.append(escalation)
    
    def get_escalations(self, organisation_id: str) -> List[Dict[str, Any]]:
        """Get escalations for organisation"""
        if organisation_id != self.organisation_id:
            return []
        
        return [
            {
                "escalation_id": e.escalation_id,
                "type": e.escalation_type,
                "timestamp": e.timestamp.isoformat(),
                "details": e.details
            }
            for e in self._escalations
        ]
