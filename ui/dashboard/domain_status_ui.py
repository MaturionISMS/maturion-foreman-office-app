"""
DomainStatusUI (DASH-01)

QA Coverage: QA-023 to QA-027

Manages UI for domain status visualization and updates.
"""

from typing import Dict, Any, List
from datetime import datetime


class DomainStatusUI:
    """
    DASH-01: Domain Status Manager UI
    
    Handles UI for:
    - Domain status initialization
    - Status updates (AMBER/RED)
    - Status queries
    - Failure mode handling
    """
    
    # All 11 operational domains
    OPERATIONAL_DOMAINS = [
        "Governance Integrity",
        "Build Execution",
        "QA & Test Coverage",
        "Memory & Context",
        "Escalation Management",
        "Parking Station Health",
        "Analytics Availability",
        "Cost Controls",
        "Builder Status",
        "External Integrations (GitHub)",
        "System Performance"
    ]
    
    def __init__(self, context: Dict[str, Any]):
        """
        Initialize domain status UI.
        
        Args:
            context: UI context with organisation_id, user_id, session_id
        """
        self.context = context
        self.domain_statuses = {}
        self.error_state = None
    
    def initialize_domains(self) -> Dict[str, Any]:
        """
        QA-023: Initialize domain statuses UI.
        
        Displays all 11 domains with default states and timestamps.
        
        Returns:
            UI output with domain list
        """
        domains = []
        current_timestamp = datetime.now().isoformat()
        
        for domain_name in self.OPERATIONAL_DOMAINS:
            domain = {
                "name": domain_name,
                "status": "GREEN",  # Default status
                "reason": None,
                "timestamp": current_timestamp
            }
            domains.append(domain)
            
            # Store in internal state
            self.domain_statuses[domain_name] = domain
        
        return {
            "domains": domains
        }
    
    def update_domain_status(self, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        QA-024, QA-025: Update domain status to AMBER or RED.
        
        Handles status updates with:
        - Status visualization
        - Reason display (required for AMBER/RED)
        - Transition animation
        - Audit trail indication
        
        Args:
            update_data: Update request with domain, status, reason
            
        Returns:
            Updated UI output
        """
        domain_name = update_data.get("domain")
        new_status = update_data.get("status")
        reason = update_data.get("reason")
        timestamp = update_data.get("timestamp", datetime.now().isoformat())
        
        # Validate required fields
        if new_status in ["AMBER", "RED"] and not reason:
            return {
                "validationError": {
                    "occurred": True,
                    "missingFields": ["reason"],
                    "message": f"Reason is required for {new_status} status"
                }
            }
        
        # Validate domain exists
        if domain_name not in self.domain_statuses:
            # Initialize if needed
            self.domain_statuses[domain_name] = {
                "name": domain_name,
                "status": "GREEN",
                "reason": None,
                "timestamp": timestamp
            }
        
        # Get previous status for transition
        previous_status = self.domain_statuses[domain_name].get("status", "GREEN")
        
        # Update domain status
        self.domain_statuses[domain_name].update({
            "status": new_status,
            "reason": reason,
            "timestamp": timestamp
        })
        
        # Get visual class for status
        visual_class = f"status-{new_status.lower()}"
        
        # Build UI update with transition info
        ui_update = {
            "domain": domain_name,
            "status": new_status,
            "statusVisual": self._get_status_visual(new_status),
            "visualClass": visual_class,
            "reason": reason,
            "reasonDisplay": {
                "visible": True,
                "text": reason,
                "required": new_status in ["AMBER", "RED"]
            },
            "transitionFrom": previous_status,
            "transitionAnimation": {
                "enabled": True,
                "type": "fade-and-slide"
            },
            "auditTrail": {
                "logged": True,
                "timestamp": timestamp
            },
            "timestamp": timestamp
        }
        
        # Add priority and escalation info for RED
        if new_status == "RED":
            ui_update["priority"] = "high"
            ui_update["escalationTrigger"] = True
        
        return ui_update
    
    def query_domain_status(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        QA-026: Query domain status UI.
        
        Retrieves current status for a domain with reason and timestamp.
        Auto-initializes domains if not yet initialized.
        
        Args:
            query: Query dict with "domain" key
            
        Returns:
            Domain status UI output
        """
        domain_name = query.get("domain")
        
        # Auto-initialize if domain is valid but not yet in statuses
        if domain_name in self.OPERATIONAL_DOMAINS and domain_name not in self.domain_statuses:
            self.initialize_domains()
        
        if domain_name not in self.domain_statuses:
            return {
                "domain": domain_name,
                "found": False,
                "error": {
                    "type": "invalid_domain",
                    "errorMessage": f"Domain '{domain_name}' not found"
                }
            }
        
        domain_data = self.domain_statuses[domain_name]
        
        return {
            "domain": domain_name,
            "found": True,
            "status": domain_data.get("status"),
            "statusVisual": self._get_status_visual(domain_data.get("status")),
            "reason": domain_data.get("reason"),
            "timestamp": domain_data.get("timestamp"),
            "timestampDisplay": self._format_timestamp(domain_data.get("timestamp")),
            "historyAccess": {
                "available": True,
                "viewHistoryLink": f"/dashboard/domain/{domain_name}/history"
            }
        }
    
    def simulate_error(self, error_type: str):
        """
        QA-027: Simulate error for failure mode testing.
        
        Args:
            error_type: Type of error to simulate
        """
        self.error_state = error_type
    
    def handle_domain_status_error(self) -> Dict[str, Any]:
        """
        QA-027: Handle domain status manager failure modes.
        
        Returns:
            Error handling UI output
        """
        if not self.error_state:
            return {
                "errorOccurred": False
            }
        
        error_messages = {
            "fetch_failure": "Unable to fetch domain statuses. Using cached data.",
            "update_failure": "Status update failed. Retrying...",
            "connection_loss": "Connection to status service lost. Working offline."
        }
        
        return {
            "errorOccurred": True,
            "errorType": self.error_state,
            "errorMessage": error_messages.get(self.error_state, "Unknown error"),
            "fallbackBehavior": {
                "useCachedData": True,
                "retryEnabled": True,
                "retryCount": 3
            },
            "userFeedback": {
                "display": "banner",
                "dismissible": True,
                "severity": "warning"
            }
        }
    
    def _get_status_visual(self, status: str) -> Dict[str, Any]:
        """
        Get visual styling for status.
        
        Args:
            status: Status value (GREEN, AMBER, RED)
            
        Returns:
            Visual styling information
        """
        visuals = {
            "GREEN": {
                "color": "#4CAF50",
                "icon": "check_circle",
                "cssClass": "status-green"
            },
            "AMBER": {
                "color": "#FFC107",
                "icon": "warning",
                "cssClass": "status-amber"
            },
            "RED": {
                "color": "#F44336",
                "icon": "error",
                "cssClass": "status-red"
            }
        }
        
        return visuals.get(status, visuals["GREEN"])
    
    def _format_timestamp(self, timestamp_str: str) -> str:
        """Format ISO timestamp for display."""
        if not timestamp_str:
            return ""
        
        try:
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            return timestamp_str
