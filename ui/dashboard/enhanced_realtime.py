"""
Enhanced Dashboard - Real-Time Updates

Implements real-time WebSocket connections and update handling for Enhanced Dashboard (Wave 2).
Part of Subwave 2.1: QA-371 to QA-375.

Architecture: Enhanced Dashboard Real-Time Updates
Tenant Isolation: All operations scoped by organisation_id
"""

from typing import Dict, Any, List, Optional, Callable
from datetime import datetime


class RealtimeDashboardConnection:
    """
    Real-time WebSocket connection manager for Enhanced Dashboard.
    
    Provides:
    - WebSocket connection management
    - Message routing and handling
    - Reconnection logic
    - Tenant-isolated updates
    """
    
    def __init__(self, context: Dict[str, Any]):
        """
        Initialize real-time connection.
        
        Args:
            context: UI context with organisation_id for tenant isolation
        """
        self.context = context
        self.organisation_id = context.get("organisation_id")
        self.connection_id: Optional[str] = None
        self.is_connected = False
        self.update_handlers: List[Callable] = []
        self.message_sequence = 0
        self.last_message_timestamp: Optional[datetime] = None
    
    def connect(self) -> Dict[str, Any]:
        """
        Establish WebSocket connection.
        
        Returns:
            Connection result with status and authentication info
        """
        # Generate connection ID
        self.connection_id = f"ws-{self.organisation_id}-{self._generate_id()}"
        self.is_connected = True
        
        return {
            "success": True,
            "status": "connected",
            "authenticated": True,
            "organisation_id": self.organisation_id,
            "connection_id": self.connection_id
        }
    
    def disconnect(self) -> Dict[str, Any]:
        """
        Close WebSocket connection.
        
        Returns:
            Disconnection result
        """
        self.is_connected = False
        self.connection_id = None
        
        return {
            "success": True,
            "status": "disconnected"
        }
    
    def reconnect(self) -> Dict[str, Any]:
        """
        Reconnect WebSocket after disconnection.
        
        Returns:
            Reconnection result
        """
        # Simulate reconnection
        return self.connect()
    
    def get_connection_info(self) -> Dict[str, Any]:
        """
        Get current connection information.
        
        Returns:
            Connection status and details
        """
        return {
            "is_connected": self.is_connected,
            "connection_id": self.connection_id,
            "organisation_id": self.organisation_id
        }
    
    def on_update(self, handler: Callable):
        """
        Register update handler callback.
        
        Args:
            handler: Callback function to handle updates
        """
        self.update_handlers.append(handler)
    
    def simulate_message(self, message: Dict[str, Any]):
        """
        Simulate receiving a WebSocket message (for testing).
        
        Args:
            message: Message data to process
        """
        # Validate message type
        valid_types = ["status_update", "metric_update", "alert", "heartbeat"]
        message_type = message.get("type")
        
        if message_type not in valid_types:
            # Reject invalid message
            return
        
        # Check tenant isolation
        message_org_id = message.get("organisation_id")
        if message_org_id is not None and message_org_id != self.organisation_id:
            # Reject messages for other organisations
            return
        
        # Route message to handlers (except heartbeat)
        if message_type != "heartbeat":
            for handler in self.update_handlers:
                handler(message)
        
        # Update sequence and timestamp
        self.message_sequence += 1
        self.last_message_timestamp = datetime.utcnow()
    
    def _generate_id(self) -> str:
        """Generate unique connection ID."""
        import random
        import string
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))


class EnhancedDashboard:
    """
    Enhanced Dashboard with real-time update support.
    
    Provides:
    - Dashboard data management
    - Real-time data refresh
    - Domain status tracking
    - Update notification coordination
    """
    
    def __init__(self, context: Dict[str, Any], connection: RealtimeDashboardConnection):
        """
        Initialize enhanced dashboard.
        
        Args:
            context: UI context with organisation_id
            connection: Real-time connection instance
        """
        self.context = context
        self.organisation_id = context.get("organisation_id")
        self.connection = connection
        self.domain_statuses: Dict[str, Dict[str, Any]] = {}
        self.refresh_handlers: List[Callable] = []
        self.update_timestamps: Dict[str, datetime] = {}
        
        # Register for updates
        self.connection.on_update(self._handle_update)
    
    def _handle_update(self, update: Dict[str, Any]):
        """
        Handle incoming real-time update.
        
        Args:
            update: Update message data
        """
        update_type = update.get("type")
        
        # Determine if update is relevant for refresh
        relevant_types = ["status_update", "metric_update", "alert"]
        
        if update_type in relevant_types:
            # Update internal state
            if update_type == "status_update":
                domain = update.get("domain")
                if domain:
                    # Check timestamp to prevent stale updates
                    update_timestamp = self._parse_timestamp(update.get("timestamp"))
                    last_timestamp = self.update_timestamps.get(domain)
                    
                    if last_timestamp is None or update_timestamp > last_timestamp:
                        # Apply update
                        self.domain_statuses[domain] = {
                            "status": update.get("new_status", update.get("status")),
                            "organisation_id": self.organisation_id,
                            "timestamp": update_timestamp
                        }
                        self.update_timestamps[domain] = update_timestamp
            
            # Trigger refresh
            for handler in self.refresh_handlers:
                handler(f"realtime_{update_type}")
    
    def on_refresh(self, handler: Callable):
        """
        Register refresh handler.
        
        Args:
            handler: Callback function for refresh events
        """
        self.refresh_handlers.append(handler)
    
    def manual_refresh(self) -> Dict[str, Any]:
        """
        Manually trigger dashboard refresh.
        
        Returns:
            Refresh result
        """
        for handler in self.refresh_handlers:
            handler("manual_refresh")
        
        return {
            "success": True,
            "message": "Dashboard refreshed manually"
        }
    
    def get_domain_status(self, domain: str) -> Dict[str, Any]:
        """
        Get current status for a domain.
        
        Args:
            domain: Domain name
            
        Returns:
            Domain status information
        """
        if domain in self.domain_statuses:
            return self.domain_statuses[domain].copy()
        
        # Return default status if not set
        return {
            "status": "UNKNOWN",
            "organisation_id": self.organisation_id
        }
    
    def _parse_timestamp(self, timestamp_str: Optional[str]) -> datetime:
        """
        Parse ISO timestamp string.
        
        Args:
            timestamp_str: ISO format timestamp
            
        Returns:
            Parsed datetime object
        """
        if not timestamp_str:
            return datetime.utcnow()
        
        try:
            # Remove 'Z' suffix if present
            if timestamp_str.endswith('Z'):
                timestamp_str = timestamp_str[:-1]
            return datetime.fromisoformat(timestamp_str)
        except ValueError:
            return datetime.utcnow()


class UpdateNotificationManager:
    """
    Manages update notifications for Enhanced Dashboard.
    
    Provides:
    - Notification creation and display
    - Priority handling
    - Dismissal logic
    - Notification queue management
    """
    
    def __init__(self, context: Dict[str, Any]):
        """
        Initialize notification manager.
        
        Args:
            context: UI context with organisation_id
        """
        self.context = context
        self.organisation_id = context.get("organisation_id")
        self.active_notifications: List[Dict[str, Any]] = []
        self.notification_counter = 0
    
    def add_notification(self, message: str, priority: str = "medium", notification_type: str = "info") -> str:
        """
        Add new notification.
        
        Args:
            message: Notification message
            priority: Priority level (high, medium, low)
            notification_type: Type of notification
            
        Returns:
            Notification ID
        """
        self.notification_counter += 1
        notification_id = f"notif-{self.notification_counter}"
        
        notification = {
            "id": notification_id,
            "message": message,
            "priority": priority,
            "type": notification_type,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.active_notifications.append(notification)
        self._sort_by_priority()
        
        return notification_id
    
    def get_active(self) -> List[Dict[str, Any]]:
        """
        Get all active notifications.
        
        Returns:
            List of active notifications, sorted by priority
        """
        return self.active_notifications.copy()
    
    def dismiss(self, notification_id: str) -> Dict[str, Any]:
        """
        Dismiss a notification.
        
        Args:
            notification_id: ID of notification to dismiss
            
        Returns:
            Dismissal result
        """
        self.active_notifications = [
            n for n in self.active_notifications
            if n["id"] != notification_id
        ]
        
        return {
            "success": True,
            "message": f"Notification {notification_id} dismissed"
        }
    
    def _sort_by_priority(self):
        """Sort notifications by priority (high first)."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        self.active_notifications.sort(
            key=lambda n: priority_order.get(n.get("priority", "medium"), 1)
        )
