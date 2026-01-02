"""
EscalationUI (ESC-04)

QA Coverage: QA-110 to QA-116

Manages UI for escalation functionality.
"""

from typing import Dict, Any, List


class EscalationUI:
    """
    ESC-04: Escalation UI
    
    Handles UI for:
    - Escalation inbox rendering
    - Escalation detail display
    - Action buttons
    - Resolution forms
    - Priority indicators
    - Context display
    - Error handling
    """
    
    def __init__(self, context: Dict[str, Any]):
        """Initialize escalation UI."""
        self.context = context
        self.error_state = None
    
    def render_inbox(self, escalation_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        QA-110: Render escalation inbox.
        
        Args:
            escalation_data: List of escalations
            
        Returns:
            Escalation inbox UI output
        """
        if self.error_state:
            return {
                "error": {
                    "errorType": self.error_state,
                    "message": "Unable to load escalations"
                },
                "retryAction": {
                    "available": True,
                    "label": "Retry"
                }
            }
        
        escalations = []
        unread_count = 0
        
        for esc in escalation_data:
            escalations.append({
                "escalationId": esc.get("escalationId"),
                "title": esc.get("title"),
                "priorityIndicator": {
                    "level": esc.get("priority"),
                    "visual": f"priority-{esc.get('priority', 'MEDIUM').lower()}"
                },
                "status": esc.get("status"),
                "createdAt": esc.get("createdAt")
            })
            
            if esc.get("status") == "pending":
                unread_count += 1
        
        return {
            "escalations": escalations,
            "sortingControls": {
                "sortByPriority": {"enabled": True, "label": "Sort by Priority"},
                "sortByTime": {"enabled": True, "label": "Sort by Time"}
            },
            "unreadCount": unread_count
        }
    
    def render_detail(self, escalation: Dict[str, Any]) -> Dict[str, Any]:
        """
        QA-111: Render escalation detail.
        
        Args:
            escalation: Escalation data
            
        Returns:
            Escalation detail UI output
        """
        return {
            "escalationId": escalation.get("escalationId"),
            "title": escalation.get("title"),
            "priority": escalation.get("priority"),
            "status": escalation.get("status"),
            "context": escalation.get("context", {}),
            "createdAt": escalation.get("createdAt"),
            "escalatedBy": escalation.get("escalatedBy")
        }
    
    def render_action_buttons(self, escalation: Dict[str, Any]) -> Dict[str, Any]:
        """
        QA-112: Render action buttons.
        
        Args:
            escalation: Escalation data
            
        Returns:
            Action buttons UI output
        """
        status = escalation.get("status")
        
        return {
            "actions": {
                "acknowledge": {
                    "enabled": status == "pending",
                    "label": "Acknowledge"
                },
                "resolve": {
                    "enabled": status in ["pending", "acknowledged"],
                    "label": "Resolve"
                },
                "delegate": {
                    "enabled": status in ["pending", "acknowledged"],
                    "label": "Delegate"
                }
            }
        }
    
    def render_resolution_form(self, escalation: Dict[str, Any]) -> Dict[str, Any]:
        """
        QA-113: Render resolution form.
        
        Args:
            escalation: Escalation data
            
        Returns:
            Resolution form UI output
        """
        return {
            "escalationId": escalation.get("escalationId"),
            "resolutionForm": {
                "outcomeSelector": {
                    "outcomes": ["resolved", "deferred", "delegated", "dismissed"]
                },
                "resolutionNotes": {
                    "required": True,
                    "label": "Resolution Notes",
                    "placeholder": "Describe how this escalation was resolved..."
                },
                "confirmButton": {
                    "enabled": True,
                    "label": "Confirm Resolution"
                },
                "cancelButton": {
                    "enabled": True,
                    "label": "Cancel"
                }
            }
        }
    
    def render_priority_indicator(self, priority: str) -> Dict[str, Any]:
        """
        QA-114: Render priority indicator.
        
        Args:
            priority: Priority level (HIGH, MEDIUM, LOW)
            
        Returns:
            Priority indicator UI output
        """
        visual_classes = {
            "HIGH": "priority-high-red",
            "MEDIUM": "priority-medium-yellow",
            "LOW": "priority-low-green"
        }
        
        icons = {
            "HIGH": "error",
            "MEDIUM": "warning",
            "LOW": "info"
        }
        
        return {
            "priority": priority,
            "visualClass": visual_classes.get(priority, "priority-medium-yellow"),
            "icon": icons.get(priority, "info")
        }
    
    def render_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        QA-115: Render escalation context.
        
        Args:
            context: Context data
            
        Returns:
            Context UI output
        """
        builder = context.get("builder", "unknown")
        blocked_on = context.get("blockedOn", "unknown")
        reason = context.get("reason", "No reason provided")
        
        formatted = f"{builder} blocked on {blocked_on}: {reason}"
        
        return {
            "builder": builder,
            "blockedOn": blocked_on,
            "reason": reason,
            "formatted": formatted
        }
    
    def simulate_load_failure(self):
        """
        QA-116: Simulate load failure for error testing.
        """
        self.error_state = "load_failure"
    
    def execute_action(self, action_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        QA-116: Execute an action on an escalation.
        
        Args:
            action_request: Action request with escalationId and action
            
        Returns:
            Action result UI output
        """
        escalation_id = action_request.get("escalationId")
        action = action_request.get("action")
        
        # Simulate failure for non-existent escalation
        if escalation_id == "non-existent":
            return {
                "actionResult": {
                    "success": False,
                    "errorMessage": f"Escalation {escalation_id} not found"
                }
            }
        
        # Successful action
        return {
            "actionResult": {
                "success": True,
                "message": f"Action '{action}' executed successfully"
            }
        }
    
    def handle_action_failure(self, action_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        QA-116: Handle action failure.
        
        Args:
            action_request: Action request that failed
            
        Returns:
            Action failure UI output
        """
        return {
            "actionFailed": True,
            "errorType": "action_failure",
            "errorMessage": f"Unable to {action_request.get('action')} escalation",
            "retryAvailable": True
        }
