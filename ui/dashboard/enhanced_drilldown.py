"""
Enhanced Dashboard - Drill-Down Navigation

Implements drill-down navigation for Enhanced Dashboard (Wave 2).
Part of Subwave 2.1: QA-361 to QA-365.

Architecture: Enhanced Dashboard Drill-Down Navigation
Tenant Isolation: All operations scoped by organisation_id
"""

from typing import Dict, Any, List, Optional


class DrillDownNavigator:
    """
    Drill-down navigation for Enhanced Dashboard.
    
    Provides hierarchical navigation through dashboard data with:
    - Multi-level drill-down
    - Breadcrumb trail
    - Navigation state management
    - Context-aware data loading
    """
    
    def __init__(self, context: Dict[str, Any]):
        """
        Initialize drill-down navigator.
        
        Args:
            context: UI context with organisation_id for tenant isolation
        """
        self.context = context
        self.organisation_id = context.get("organisation_id")
        self.current_level = 0
        self.navigation_history: List[Dict[str, Any]] = []
        self.state = {
            "current_level": 0,
            "history": [],
            "organisation_id": self.organisation_id
        }
    
    def render(self) -> Dict[str, Any]:
        """
        Render drill-down navigation component.
        
        Returns:
            Component rendering data with interactive elements
        """
        return {
            "component": "drill_down_navigator",
            "interactive_elements": [
                {"type": "click_target", "action": "drill_down", "enabled": True},
                {"type": "click_target", "action": "drill_up", "enabled": self.current_level > 0},
                {"type": "click_target", "action": "navigate_root", "enabled": self.current_level > 0}
            ],
            "hierarchy_levels": self._get_hierarchy_levels(),
            "aria_label": "Dashboard drill-down navigation",
            "role": "navigation"
        }
    
    def _get_hierarchy_levels(self) -> List[str]:
        """Get available hierarchy levels for current context."""
        return ["Dashboard", "Domain", "Subsystem", "Component", "Detail"]
    
    def get_state(self) -> Dict[str, Any]:
        """
        Get current navigation state.
        
        Returns:
            Current state including level, history, and organisation context
        """
        return {
            "current_level": self.current_level,
            "history": self.navigation_history.copy(),
            "organisation_id": self.organisation_id
        }
    
    def navigate_to_level(self, level: int, label: str):
        """
        Navigate to specific drill-down level.
        
        Args:
            level: Target drill-down level (0 = root)
            label: Label for the navigation target
        """
        self.current_level = level
        self.navigation_history.append({
            "level": level,
            "label": label,
            "timestamp": self._get_timestamp()
        })
    
    def navigate_down(self, target: str) -> Dict[str, Any]:
        """
        Navigate down one level in hierarchy.
        
        Args:
            target: Target item to drill down into
            
        Returns:
            Navigation result with success status and new level
        """
        new_level = self.current_level + 1
        self.current_level = new_level
        self.navigation_history.append({
            "level": new_level,
            "target": target,
            "action": "drill_down"
        })
        
        return {
            "success": True,
            "new_level": new_level,
            "target": target
        }
    
    def navigate_up(self) -> Dict[str, Any]:
        """
        Navigate up one level in hierarchy.
        
        Returns:
            Navigation result with success status and new level
        """
        if self.current_level == 0:
            return {
                "success": False,
                "message": "Already at root level",
                "new_level": 0
            }
        
        new_level = self.current_level - 1
        self.current_level = new_level
        
        return {
            "success": True,
            "new_level": new_level
        }
    
    def navigate_to_root(self) -> Dict[str, Any]:
        """
        Navigate to root level.
        
        Returns:
            Navigation result with success status
        """
        self.current_level = 0
        
        return {
            "success": True,
            "new_level": 0
        }
    
    def get_breadcrumbs(self) -> List[Dict[str, Any]]:
        """
        Get breadcrumb trail for current navigation state.
        
        Returns:
            List of breadcrumb items with labels and navigation info
        """
        breadcrumbs = [
            {
                "level": 0,
                "label": "Dashboard",
                "clickable": self.current_level > 0,
                "is_current": self.current_level == 0
            }
        ]
        
        # Add breadcrumbs from navigation history
        for i, nav_item in enumerate(self.navigation_history[:self.current_level]):
            level = i + 1
            breadcrumbs.append({
                "level": level,
                "label": nav_item.get("target", nav_item.get("label", f"Level {level}")),
                "clickable": level < self.current_level,
                "is_current": level == self.current_level
            })
        
        return breadcrumbs
    
    def click_breadcrumb(self, breadcrumb_level: int) -> Dict[str, Any]:
        """
        Navigate by clicking a breadcrumb.
        
        Args:
            breadcrumb_level: Target level from breadcrumb
            
        Returns:
            Navigation result
        """
        if breadcrumb_level < 0 or breadcrumb_level > self.current_level:
            return {
                "success": False,
                "message": "Invalid breadcrumb level"
            }
        
        self.current_level = breadcrumb_level
        
        return {
            "success": True,
            "new_level": breadcrumb_level
        }
    
    def get_current_level_data(self) -> Dict[str, Any]:
        """
        Get data for current drill-down level.
        
        Returns:
            Data filtered for current navigation context
        """
        context_label = "root"
        if self.current_level > 0 and self.navigation_history:
            last_nav = self.navigation_history[self.current_level - 1]
            context_label = last_nav.get("target", last_nav.get("label", f"Level {self.current_level}"))
        
        return {
            "level": self.current_level,
            "context": context_label,
            "organisation_id": self.organisation_id,
            "data": self._load_level_data(self.current_level, context_label)
        }
    
    def _load_level_data(self, level: int, context: str) -> Dict[str, Any]:
        """
        Load data for specific level and context.
        
        Args:
            level: Drill-down level
            context: Navigation context
            
        Returns:
            Level-specific data
        """
        # Return different data based on level
        if level == 0:
            return {"type": "root_dashboard", "domains": 11, "summary": "all_domains"}
        else:
            return {
                "type": f"level_{level}_data",
                "context": context,
                "filtered_by": context
            }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now(UTC).isoformat() + "Z"
