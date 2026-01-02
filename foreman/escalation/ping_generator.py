"""
ESC-01: Ping Generator
QA-093 to QA-096

Generates "pings" (attention-required notifications) when system components
need human attention. Routes pings to notification service and tracks lifecycle.

**Inputs:**
- AttentionRequired event from any component
- CriticalStatusDetected event from DASH-01

**Outputs:**
- PingGenerated event → Notification Service
- PingLifecycleUpdated event → ESC-04 Message Inbox

**Failure Modes:**
- Delivery failure → Retry 3x → Escalate to ESC-02
- Duplicate detection → Suppress duplicate pings
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Literal
from dataclasses import dataclass, field
import uuid


PingStatus = Literal["sent", "delivered", "acknowledged", "timeout"]
PingPriority = Literal["normal", "high", "urgent", "critical"]


@dataclass
class Ping:
    """Represents a ping for attention required."""
    ping_id: str
    context: Dict[str, any]
    priority: PingPriority
    status: PingStatus = "sent"
    created_at: datetime = field(default_factory=datetime.now)
    delivered_at: Optional[datetime] = None
    acknowledged_at: Optional[datetime] = None
    retry_count: int = 0
    timeout_threshold: timedelta = field(default_factory=lambda: timedelta(hours=24))


class PingGenerator:
    """
    ESC-01: Ping Generator
    
    Generates and manages attention-required notifications.
    Implements QA-093 to QA-096.
    """
    
    def __init__(self):
        self.pings: Dict[str, Ping] = {}
        self.recent_contexts: List[Dict[str, any]] = []
        self.max_retries = 3
        self.duplicate_window = timedelta(minutes=5)
    
    def generate_ping(
        self,
        context: Dict[str, any],
        priority: PingPriority = "normal"
    ) -> Ping:
        """
        QA-093: Generate ping for attention required.
        
        Creates a ping with context and priority assignment.
        Detects and prevents duplicate pings within time window.
        
        Args:
            context: Context information about why attention is needed
            priority: Priority level for the ping
            
        Returns:
            Ping: Generated ping object
            
        Raises:
            ValueError: If context is invalid or duplicate detected
        """
        # Validate context
        if not context or not isinstance(context, dict):
            raise ValueError("Context must be a non-empty dictionary")
        
        # Check for duplicates
        if self._is_duplicate(context):
            raise ValueError("Duplicate ping detected within time window")
        
        # Generate ping
        ping = Ping(
            ping_id=str(uuid.uuid4()),
            context=context,
            priority=priority
        )
        
        self.pings[ping.ping_id] = ping
        self.recent_contexts.append({
            'context': context,
            'timestamp': datetime.now()
        })
        
        return ping
    
    def route_ping(self, ping_id: str) -> Dict[str, any]:
        """
        QA-094: Route ping to notification service.
        
        Triggers delivery and tracks acknowledgment.
        
        Args:
            ping_id: ID of ping to route
            
        Returns:
            Dict containing delivery status and tracking info
            
        Raises:
            KeyError: If ping_id not found
            RuntimeError: If delivery fails after retries
        """
        if ping_id not in self.pings:
            raise KeyError(f"Ping {ping_id} not found")
        
        ping = self.pings[ping_id]
        
        # Simulate delivery
        try:
            self._deliver_to_notification_service(ping)
            ping.status = "delivered"
            ping.delivered_at = datetime.now()
            
            return {
                'ping_id': ping_id,
                'status': 'delivered',
                'delivery_trigger': True,
                'acknowledgment_tracking': True,
                'delivered_at': ping.delivered_at.isoformat()
            }
        except Exception as e:
            ping.retry_count += 1
            if ping.retry_count >= self.max_retries:
                # Escalate to ESC-02
                raise RuntimeError(
                    f"Ping delivery failed after {self.max_retries} retries: {str(e)}"
                )
            raise
    
    def track_lifecycle(self, ping_id: str) -> Dict[str, any]:
        """
        QA-095: Track ping lifecycle.
        
        Returns current state and detects timeouts.
        
        Args:
            ping_id: ID of ping to track
            
        Returns:
            Dict containing lifecycle state information
        """
        if ping_id not in self.pings:
            raise KeyError(f"Ping {ping_id} not found")
        
        ping = self.pings[ping_id]
        
        # Check for timeout
        is_timeout = False
        if ping.status != "acknowledged":
            elapsed = datetime.now() - ping.created_at
            if elapsed > ping.timeout_threshold:
                ping.status = "timeout"
                is_timeout = True
        
        return {
            'ping_id': ping_id,
            'status': ping.status,
            'created_at': ping.created_at.isoformat(),
            'delivered_at': ping.delivered_at.isoformat() if ping.delivered_at else None,
            'acknowledged_at': ping.acknowledged_at.isoformat() if ping.acknowledged_at else None,
            'is_timeout': is_timeout,
            'retry_count': ping.retry_count
        }
    
    def acknowledge_ping(self, ping_id: str) -> None:
        """Mark ping as acknowledged."""
        if ping_id not in self.pings:
            raise KeyError(f"Ping {ping_id} not found")
        
        ping = self.pings[ping_id]
        ping.status = "acknowledged"
        ping.acknowledged_at = datetime.now()
    
    def _is_duplicate(self, context: Dict[str, any]) -> bool:
        """
        QA-096: Duplicate ping prevention.
        
        Checks if similar ping was generated recently.
        """
        cutoff_time = datetime.now() - self.duplicate_window
        
        for recent in self.recent_contexts:
            if recent['timestamp'] > cutoff_time:
                # Simple duplicate check - compare context keys
                if self._contexts_similar(recent['context'], context):
                    return True
        
        # Clean up old contexts
        self.recent_contexts = [
            r for r in self.recent_contexts
            if r['timestamp'] > cutoff_time
        ]
        
        return False
    
    def _contexts_similar(self, context1: Dict[str, any], context2: Dict[str, any]) -> bool:
        """Check if two contexts are similar enough to be duplicates."""
        # Simple similarity check - same keys and similar values
        if context1.keys() != context2.keys():
            return False
        
        # Check if all key values are identical
        for key in context1:
            if context1[key] != context2[key]:
                return False
        
        return True
    
    def _deliver_to_notification_service(self, ping: Ping) -> None:
        """
        Deliver ping to notification service.
        
        In production, this would make an actual API call or publish event.
        For now, we simulate successful delivery.
        """
        # Simulate delivery - in production this would be actual integration
        pass
    
    def handle_failure_modes(self, failure_type: str, **kwargs) -> Dict[str, any]:
        """
        QA-096: Handle ping generator failure modes.
        
        Handles:
        - Delivery failure with retry/escalation
        - Duplicate ping prevention
        
        Args:
            failure_type: Type of failure ('delivery_failure' or 'duplicate')
            **kwargs: Additional context for the failure
            
        Returns:
            Dict describing how failure was handled
        """
        if failure_type == 'delivery_failure':
            ping_id = kwargs.get('ping_id')
            if not ping_id or ping_id not in self.pings:
                return {'status': 'error', 'reason': 'Invalid ping_id'}
            
            ping = self.pings[ping_id]
            
            if ping.retry_count < self.max_retries:
                return {
                    'status': 'retry',
                    'retry_count': ping.retry_count,
                    'max_retries': self.max_retries
                }
            else:
                return {
                    'status': 'escalated',
                    'escalated_to': 'ESC-02',
                    'reason': 'Max retries exceeded'
                }
        
        elif failure_type == 'duplicate':
            context = kwargs.get('context')
            if self._is_duplicate(context):
                return {
                    'status': 'suppressed',
                    'reason': 'Duplicate ping within time window'
                }
            else:
                return {
                    'status': 'allowed',
                    'reason': 'Not a duplicate'
                }
        
        return {'status': 'error', 'reason': f'Unknown failure type: {failure_type}'}
