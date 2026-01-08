"""
Enhanced Dashboard - Update Notifications

Manages update notifications for Enhanced Dashboard.
Part of Subwave 2.1: QA-371 to QA-375.

Architecture: Enhanced Dashboard Notifications
Tenant Isolation: All operations scoped by organisation_id
"""

from typing import Dict, Any, List
from datetime import datetime


class UpdateNotificationManager:
    """
    Manages update notifications for Enhanced Dashboard.
    
    Provides:
    - Notification creation and display
    - Priority handling
    - Dismissal logic
    - Notification queue management
    """
    
    def __init__(self, context: Dict[str, Any], connection=None):
        """
        Initialize notification manager.
        
        Args:
            context: UI context with organisation_id
            connection: Optional real-time connection for auto-notifications
        """
        self.context = context
        self.organisation_id = context.get("organisation_id")
        self.active_notifications: List[Dict[str, Any]] = []
        self.notification_counter = 0
        self.connection = connection
        
        # Auto-handle incoming messages from connection if provided
        if connection:
            connection.on_update(self._auto_create_notification)
    
    def _auto_create_notification(self, update: Dict[str, Any]):
        """
        Automatically create notification from update.
        
        Args:
            update: Update message
        """
        # Only create notifications for important updates
        if update.get("priority") in ["high", "medium"]:
            message = update.get("message", "Dashboard update received")
            priority = update.get("priority", "medium")
            self.add_notification(message, priority, update.get("type", "info"))
    
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
            "timestamp": datetime.now(UTC).isoformat()
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
