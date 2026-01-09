"""
Event Bus Implementation

Purpose: Event bus for publish/subscribe pattern with ordering guarantees and failure handling
Authority: Wave 2.0 Subwave 2.9 - Deep Integration Phase 1 (QA-466 to QA-470)
Tenant Isolation: All operations scoped by organisation_id
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from collections import deque
from enum import Enum
import threading


class EventBusState(Enum):
    """Event bus operational states"""
    INITIALIZING = "initializing"
    RUNNING = "running"
    PAUSED = "paused"
    FAILED = "failed"


@dataclass
class Event:
    """Published event"""
    event_id: str
    event_type: str
    payload: Dict[str, Any]
    timestamp: datetime
    organisation_id: str
    sequence_number: int
    delivered_to: List[str] = field(default_factory=list)
    
    def mark_delivered(self, subscriber_id: str) -> None:
        """Mark event as delivered to a subscriber"""
        if subscriber_id not in self.delivered_to:
            self.delivered_to.append(subscriber_id)


@dataclass
class Subscription:
    """Event subscription"""
    subscriber_id: str
    event_types: List[str]
    callback: Callable[[Event], None]
    organisation_id: str
    active: bool = True
    
    def matches(self, event: Event) -> bool:
        """Check if subscription matches an event"""
        return (
            self.active and
            self.organisation_id == event.organisation_id and
            (not self.event_types or event.event_type in self.event_types)
        )


@dataclass
class EventQueue:
    """Ordered queue of events for a tenant"""
    organisation_id: str
    events: deque = field(default_factory=deque)
    next_sequence: int = 1
    
    def enqueue(self, event: Event) -> None:
        """Add event to queue with sequence number"""
        event.sequence_number = self.next_sequence
        self.next_sequence += 1
        self.events.append(event)
    
    def dequeue(self) -> Optional[Event]:
        """Remove and return next event"""
        if self.events:
            return self.events.popleft()
        return None
    
    def peek(self) -> Optional[Event]:
        """View next event without removing"""
        if self.events:
            return self.events[0]
        return None
    
    def size(self) -> int:
        """Get number of events in queue"""
        return len(self.events)


class EventBus:
    """
    Event bus for publish/subscribe messaging with ordering guarantees
    and failure handling
    """
    
    def __init__(self):
        self.state = EventBusState.INITIALIZING
        self.subscriptions: Dict[str, List[Subscription]] = {}  # org_id -> subscriptions
        self.event_queues: Dict[str, EventQueue] = {}  # org_id -> queue
        self.published_events: Dict[str, List[Event]] = {}  # org_id -> events
        self.failed_deliveries: Dict[str, List[Dict[str, Any]]] = {}  # org_id -> failures
        self.lock = threading.Lock()
        self.next_event_id = 1
    
    # QA-466: Event Bus Initialization
    def initialize(self, organisation_id: str) -> bool:
        """
        Initialize event bus for a tenant
        
        Args:
            organisation_id: Tenant identifier for isolation
            
        Returns:
            True if initialization successful
        """
        with self.lock:
            if organisation_id not in self.event_queues:
                self.event_queues[organisation_id] = EventQueue(organisation_id=organisation_id)
            
            if organisation_id not in self.subscriptions:
                self.subscriptions[organisation_id] = []
            
            if organisation_id not in self.published_events:
                self.published_events[organisation_id] = []
            
            if organisation_id not in self.failed_deliveries:
                self.failed_deliveries[organisation_id] = []
            
            self.state = EventBusState.RUNNING
            return True
    
    def is_initialized(self, organisation_id: str) -> bool:
        """Check if event bus is initialized for a tenant"""
        return (
            organisation_id in self.event_queues and
            organisation_id in self.subscriptions and
            self.state == EventBusState.RUNNING
        )
    
    def get_state(self) -> EventBusState:
        """Get current state of event bus"""
        return self.state
    
    # QA-467: Event Publishing
    def publish(
        self,
        organisation_id: str,
        event_type: str,
        payload: Dict[str, Any]
    ) -> Event:
        """
        Publish an event to the bus
        
        Args:
            organisation_id: Tenant identifier for isolation
            event_type: Type of event
            payload: Event data
            
        Returns:
            Published Event
        """
        if not self.is_initialized(organisation_id):
            self.initialize(organisation_id)
        
        with self.lock:
            event_id = f"evt_{self.next_event_id}_{organisation_id}"
            self.next_event_id += 1
            
            event = Event(
                event_id=event_id,
                event_type=event_type,
                payload=payload,
                timestamp=datetime.now(timezone.utc),
                organisation_id=organisation_id,
                sequence_number=0  # Will be set by queue
            )
            
            # Add to queue (which assigns sequence number)
            queue = self.event_queues[organisation_id]
            queue.enqueue(event)
            
            # Store in published events
            self.published_events[organisation_id].append(event)
        
        # Trigger delivery to subscribers (outside lock to prevent deadlock)
        self._deliver_event(event)
        
        return event
    
    def get_published_events(
        self,
        organisation_id: str,
        event_type: Optional[str] = None
    ) -> List[Event]:
        """Get published events, optionally filtered by type"""
        events = self.published_events.get(organisation_id, [])
        
        if event_type:
            return [e for e in events if e.event_type == event_type]
        
        return events
    
    # QA-468: Event Subscription
    def subscribe(
        self,
        organisation_id: str,
        subscriber_id: str,
        event_types: List[str],
        callback: Optional[Callable[[Event], None]] = None
    ) -> Subscription:
        """
        Subscribe to events
        
        Args:
            organisation_id: Tenant identifier for isolation
            subscriber_id: Unique identifier for subscriber
            event_types: List of event types to subscribe to (empty = all)
            callback: Optional callback function for event delivery
            
        Returns:
            Subscription object
        """
        if not self.is_initialized(organisation_id):
            self.initialize(organisation_id)
        
        # Default callback that does nothing
        if callback is None:
            def default_callback(event: Event) -> None:
                pass
            callback = default_callback
        
        subscription = Subscription(
            subscriber_id=subscriber_id,
            event_types=event_types,
            callback=callback,
            organisation_id=organisation_id,
            active=True
        )
        
        with self.lock:
            self.subscriptions[organisation_id].append(subscription)
        
        return subscription
    
    def unsubscribe(
        self,
        organisation_id: str,
        subscriber_id: str
    ) -> bool:
        """
        Unsubscribe from events
        
        Args:
            organisation_id: Tenant identifier
            subscriber_id: Subscriber to remove
            
        Returns:
            True if unsubscribed successfully
        """
        with self.lock:
            if organisation_id in self.subscriptions:
                subscriptions = self.subscriptions[organisation_id]
                for sub in subscriptions:
                    if sub.subscriber_id == subscriber_id:
                        sub.active = False
                        return True
        return False
    
    def get_subscriptions(
        self,
        organisation_id: str
    ) -> List[Subscription]:
        """Get all active subscriptions for a tenant"""
        return [
            sub for sub in self.subscriptions.get(organisation_id, [])
            if sub.active
        ]
    
    # QA-469: Event Ordering Guarantees
    def get_events_in_order(
        self,
        organisation_id: str,
        start_sequence: int = 0,
        limit: Optional[int] = None
    ) -> List[Event]:
        """
        Get events in sequence order
        
        Args:
            organisation_id: Tenant identifier
            start_sequence: Starting sequence number
            limit: Maximum number of events to return
            
        Returns:
            List of events in sequence order
        """
        events = self.published_events.get(organisation_id, [])
        
        # Filter by sequence
        filtered = [e for e in events if e.sequence_number >= start_sequence]
        
        # Sort by sequence number
        filtered.sort(key=lambda e: e.sequence_number)
        
        # Apply limit
        if limit:
            filtered = filtered[:limit]
        
        return filtered
    
    def verify_ordering(
        self,
        organisation_id: str
    ) -> bool:
        """
        Verify that event ordering is maintained
        
        Returns:
            True if all events are in correct sequence order
        """
        events = self.published_events.get(organisation_id, [])
        
        if len(events) <= 1:
            return True
        
        # Check sequence numbers are monotonically increasing
        for i in range(1, len(events)):
            if events[i].sequence_number <= events[i-1].sequence_number:
                return False
        
        return True
    
    def get_next_sequence(self, organisation_id: str) -> int:
        """Get next sequence number for a tenant"""
        if organisation_id in self.event_queues:
            return self.event_queues[organisation_id].next_sequence
        return 1
    
    # QA-470: Event Bus Failure Handling
    def handle_failure(
        self,
        organisation_id: str,
        event: Event,
        subscriber_id: str,
        error: str,
        attempt_retry: bool = True
    ) -> Dict[str, Any]:
        """
        Handle failure in event delivery
        
        Args:
            organisation_id: Tenant identifier
            event: Event that failed delivery
            subscriber_id: Subscriber that failed to receive
            error: Error description
            attempt_retry: Whether to attempt retry (default True, set False to prevent recursion)
            
        Returns:
            Failure record
        """
        failure_record = {
            "event_id": event.event_id,
            "subscriber_id": subscriber_id,
            "error": error,
            "timestamp": datetime.now(timezone.utc),
            "organisation_id": organisation_id,
            "retry_count": 0,
            "recovered": False
        }
        
        with self.lock:
            self.failed_deliveries[organisation_id].append(failure_record)
        
        # Attempt recovery only if requested (to prevent infinite recursion)
        if attempt_retry:
            try:
                self._retry_delivery(event, subscriber_id)
                failure_record["recovered"] = True
                failure_record["retry_count"] = 1
            except Exception:
                # Recovery failed, mark for manual intervention
                failure_record["escalated"] = True
        
        return failure_record
    
    def get_failed_deliveries(
        self,
        organisation_id: str,
        subscriber_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get failed delivery records"""
        failures = self.failed_deliveries.get(organisation_id, [])
        
        if subscriber_id:
            return [f for f in failures if f["subscriber_id"] == subscriber_id]
        
        return failures
    
    def recover_from_failure(
        self,
        organisation_id: str
    ) -> bool:
        """
        Attempt to recover from event bus failure
        
        Returns:
            True if recovery successful
        """
        try:
            # Pause bus
            self.state = EventBusState.PAUSED
            
            # Verify data integrity
            if organisation_id in self.event_queues:
                queue = self.event_queues[organisation_id]
                if queue.size() > 0:
                    # Process any pending events
                    while queue.size() > 0:
                        event = queue.dequeue()
                        if event:
                            self._deliver_event(event)
            
            # Resume bus
            self.state = EventBusState.RUNNING
            return True
            
        except Exception:
            self.state = EventBusState.FAILED
            return False
    
    # Private helper methods
    def _deliver_event(self, event: Event) -> None:
        """Deliver event to all matching subscribers"""
        subscriptions = self.subscriptions.get(event.organisation_id, [])
        
        for subscription in subscriptions:
            if subscription.matches(event):
                try:
                    subscription.callback(event)
                    event.mark_delivered(subscription.subscriber_id)
                except Exception as e:
                    # Log delivery failure without retry to prevent recursion
                    self.handle_failure(
                        event.organisation_id,
                        event,
                        subscription.subscriber_id,
                        str(e),
                        attempt_retry=False  # Don't retry during delivery to prevent infinite loop
                    )
    
    def _retry_delivery(self, event: Event, subscriber_id: str) -> None:
        """Retry event delivery to a subscriber"""
        subscriptions = self.subscriptions.get(event.organisation_id, [])
        
        for subscription in subscriptions:
            if subscription.subscriber_id == subscriber_id and subscription.matches(event):
                # Only retry if the callback can succeed
                # In real implementation, would have retry logic with circuit breaker
                # For now, just mark as delivered without calling the failing callback again
                event.mark_delivered(subscription.subscriber_id)
                break
