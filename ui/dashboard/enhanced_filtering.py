"""
Enhanced Dashboard - Advanced Filtering

Implements advanced filtering for Enhanced Dashboard (Wave 2).
Part of Subwave 2.1: QA-366 to QA-370.

Architecture: Enhanced Dashboard Advanced Filtering
Tenant Isolation: All operations scoped by organisation_id
"""

from typing import Dict, Any, List, Optional
import json


class DashboardFilterPanel:
    """
    Advanced filtering panel for Enhanced Dashboard.
    
    Provides multi-criteria filtering with:
    - Multiple simultaneous filters
    - Filter state persistence
    - Reset and clear functionality
    - Tenant-isolated filter state
    """
    
    def __init__(self, context: Dict[str, Any]):
        """
        Initialize filter panel.
        
        Args:
            context: UI context with organisation_id for tenant isolation
        """
        self.context = context
        self.organisation_id = context.get("organisation_id")
        self.active_filters: Dict[str, Any] = {}
        self.saved_state: Optional[Dict[str, Any]] = None
    
    def render(self) -> Dict[str, Any]:
        """
        Render filter panel component.
        
        Returns:
            Component rendering data with controls and actions
        """
        return {
            "component": "filter_panel",
            "controls": self._get_filter_controls(),
            "actions": {
                "clear": {"enabled": len(self.active_filters) > 0, "label": "Clear Filters"},
                "apply": {"enabled": True, "label": "Apply Filters"},
                "reset": {"enabled": len(self.active_filters) > 0, "label": "Reset"}
            },
            "aria_label": "Dashboard filter panel"
        }
    
    def _get_filter_controls(self) -> List[Dict[str, Any]]:
        """Get available filter controls."""
        return [
            {"type": "dropdown", "name": "status", "label": "Status", "options": ["GREEN", "AMBER", "RED"]},
            {"type": "dropdown", "name": "domain", "label": "Domain", "options": ["Build Execution", "QA Coverage", "Memory", "Escalation"]},
            {"type": "dropdown", "name": "priority", "label": "Priority", "options": ["high", "medium", "low"]},
            {"type": "dropdown", "name": "builder", "label": "Builder", "options": ["ui-builder", "api-builder", "schema-builder", "integration-builder", "qa-builder"]}
        ]
    
    def get_state(self) -> Dict[str, Any]:
        """
        Get current filter state.
        
        Returns:
            Current state including active filters and organisation context
        """
        return {
            "active_filters": self.active_filters.copy(),
            "organisation_id": self.organisation_id
        }
    
    def set_filter(self, filter_name: str, filter_value: Any):
        """
        Set or update a filter.
        
        Args:
            filter_name: Name of the filter criterion
            filter_value: Value for the filter
        """
        self.active_filters[filter_name] = filter_value
    
    def apply_filters(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Apply active filters to data.
        
        Args:
            data: Data items to filter
            
        Returns:
            Filtered data matching all active filter criteria (AND logic)
        """
        if not self.active_filters:
            return data
        
        filtered = data
        
        for filter_name, filter_value in self.active_filters.items():
            filtered = [
                item for item in filtered
                if item.get(filter_name) == filter_value
            ]
        
        return filtered
    
    def clear_filters(self, permanent: bool = False):
        """
        Clear all active filters.
        
        Args:
            permanent: If True, also clear saved state
        """
        self.active_filters = {}
        
        if permanent:
            self.saved_state = None
    
    def save_state(self) -> Dict[str, Any]:
        """
        Save current filter state for later restoration.
        
        Returns:
            Result with success status
        """
        self.saved_state = {
            "active_filters": self.active_filters.copy(),
            "organisation_id": self.organisation_id
        }
        
        return {
            "success": True,
            "message": "Filter state saved"
        }
    
    def restore_state(self) -> Dict[str, Any]:
        """
        Restore previously saved filter state.
        
        Returns:
            Result with success status
        """
        if self.saved_state is None:
            return {
                "success": False,
                "message": "No saved state available"
            }
        
        self.active_filters = self.saved_state["active_filters"].copy()
        
        return {
            "success": True,
            "message": "Filter state restored"
        }
    
    def reset_filters(self, confirmed: bool = False) -> Dict[str, Any]:
        """
        Reset all filters with optional confirmation for many filters.
        
        Args:
            confirmed: Whether user has confirmed the reset
            
        Returns:
            Result with success status or confirmation request
        """
        filter_count = len(self.active_filters)
        
        # Request confirmation if 4 or more filters active
        if filter_count >= 4 and not confirmed:
            return {
                "confirmation_required": True,
                "message": f"Are you sure you want to reset {filter_count} active filters?"
            }
        
        # Perform reset
        self.active_filters = {}
        
        return {
            "success": True,
            "confirmation_required": False,
            "message": "All filters reset"
        }
