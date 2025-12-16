"""
Notification Manager - manages notifications and escalations.

Implements notification creation and delivery.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime


# Global notification registry
_notification_registry: List[Dict[str, Any]] = []


class NotificationManager:
    """
    Manages notifications and escalations.
    
    Responsibilities:
    - Notification creation
    - Notification routing
    - Escalation tracking
    
    Note: Notifications are stored in a global registry so they can be accessed
    by any NotificationManager instance.
    """
    
    def __init__(self):
        """Initialize NotificationManager."""
        pass
    
    def send_notification(
        self,
        recipient: str,
        type: str,
        task_id: str,
        severity: str,
        message: str
    ) -> None:
        """
        Send a notification.
        
        Args:
            recipient: Notification recipient (e.g., "foreman", "johan")
            type: Notification type (e.g., "escalation", "info")
            task_id: Related task ID
            severity: Severity level (e.g., "critical", "high", "medium")
            message: Notification message
        """
        notification = {
            'recipient': recipient,
            'type': type,
            'task_id': task_id,
            'severity': severity,
            'message': message,
            'timestamp': datetime.utcnow().isoformat()
        }
        _notification_registry.append(notification)
    
    def get_notifications(
        self,
        recipient: Optional[str] = None,
        type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get notifications, optionally filtered.
        
        Args:
            recipient: Optional recipient filter
            type: Optional type filter
            
        Returns:
            List of matching notifications
        """
        results = _notification_registry
        
        if recipient:
            results = [n for n in results if n['recipient'] == recipient]
        
        if type:
            results = [n for n in results if n['type'] == type]
        
        return results
