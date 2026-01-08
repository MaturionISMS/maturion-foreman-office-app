"""
Enhanced Dashboard - Main Dashboard Module

Main enhanced dashboard module with real-time update support.
Part of Subwave 2.1: QA-371 to QA-375.

Architecture: Enhanced Dashboard Core
Tenant Isolation: All operations scoped by organisation_id
"""

from typing import Dict, Any, List, Callable
from datetime import datetime


class EnhancedDashboard:
    """
    Enhanced Dashboard with real-time update support.
    
    Provides:
    - Dashboard data management
    - Real-time data refresh
    - Domain status tracking
    - Update notification coordination
    """
    
    def __init__(self, context: Dict[str, Any], connection):
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
    
    def _parse_timestamp(self, timestamp_str: Any) -> datetime:
        """
        Parse ISO timestamp string.
        
        Args:
            timestamp_str: ISO format timestamp
            
        Returns:
            Parsed datetime object
        """
        if not timestamp_str:
            return datetime.now(UTC)
        
        if isinstance(timestamp_str, datetime):
            return timestamp_str
        
        try:
            # Remove 'Z' suffix if present
            if timestamp_str.endswith('Z'):
                timestamp_str = timestamp_str[:-1]
            return datetime.fromisoformat(timestamp_str)
        except (ValueError, AttributeError):
            return datetime.now(UTC)
