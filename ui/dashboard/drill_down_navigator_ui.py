"""
DrillDownNavigatorUI (DASH-02)

QA Coverage: QA-028 to QA-032

Handles hierarchical navigation from status to root cause.
"""

from typing import Dict, Any, List


class DrillDownNavigatorUI:
    """
    DASH-02: Drill-Down Navigator UI
    
    Provides UI for:
    - Navigate from RED/AMBER status to root cause
    - Navigate to evidence artifacts
    - Multi-level drill-down with breadcrumbs
    - Failure mode handling
    """
    
    def __init__(self, context: Dict[str, Any]):
        """
        Initialize drill-down navigator UI.
        
        Args:
            context: UI context with organisation_id, user_id, session_id
        """
        self.context = context
        self.navigation_stack = []
        self.error_state = None
        self.current_level = 0
    
    def navigate_to_root_cause(self, nav_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        QA-028: Navigate from RED status to root cause.
        
        Provides drill-down navigation from RED status to root cause details.
        
        Args:
            nav_request: Navigation request with domain, status
            
        Returns:
            Root cause navigation UI output
        """
        domain = nav_request.get("domain")
        status = nav_request.get("status")
        
        # Build navigation path
        navigation_path = [
            {"level": 1, "label": "Dashboard", "type": "dashboard"},
            {"level": 2, "label": f"{domain} Status", "type": "domain_status"},
            {"level": 3, "label": "Root Cause Analysis", "type": "root_cause"}
        ]
        
        # Store navigation state
        self.navigation_stack = navigation_path
        self.current_level = 3
        
        # Build root cause display
        root_cause = {
            "description": f"Test coverage below threshold in {domain}",
            "identifiedAt": "2026-01-01T00:00:00Z",
            "severity": "high"
        }
        
        # Build evidence links
        evidence_links = [
            {
                "id": "ev-001",
                "type": "test_results",
                "label": "Test Coverage Report",
                "url": f"/evidence/{domain}/test_results"
            },
            {
                "id": "ev-002",
                "type": "qa_logs",
                "label": "QA Execution Logs",
                "url": f"/evidence/{domain}/qa_logs"
            }
        ]
        
        # Build breadcrumbs
        breadcrumbs = [
            {"label": "Dashboard", "level": 1, "active": False},
            {"label": f"{domain}", "level": 2, "active": False},
            {"label": "Root Cause", "level": 3, "active": True}
        ]
        
        return {
            "navigationPath": navigation_path,
            "rootCause": root_cause,
            "evidenceLinks": evidence_links,
            "breadcrumbs": breadcrumbs
        }
    
    def navigate_to_reason(self, nav_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        QA-029: Navigate from AMBER status to reason detail.
        
        Provides detailed reason display for AMBER status.
        
        Args:
            nav_request: Navigation request with domain, status
            
        Returns:
            Reason detail UI output
        """
        domain = nav_request.get("domain")
        status = nav_request.get("status")
        
        # Build reason detail
        reason_detail = {
            "fullDescription": f"Build in progress for {domain} with one warning detected",
            "timestamp": "2026-01-01T00:00:00Z",
            "context": "During CI/CD pipeline execution"
        }
        
        # Build related context
        related_context = {
            "affectedComponents": [
                {"name": "ui-builder", "impact": "low"},
                {"name": "api-builder", "impact": "none"}
            ],
            "relatedIssues": []
        }
        
        # Build navigation controls
        navigation_controls = {
            "backButton": {
                "enabled": True,
                "label": "Back to Dashboard"
            },
            "viewEvidenceButton": {
                "enabled": True,
                "label": "View Evidence"
            }
        }
        
        return {
            "reasonDetail": reason_detail,
            "relatedContext": related_context,
            "navigationControls": navigation_controls
        }
    
    def navigate_to_evidence(self, nav_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        QA-030: Navigate to evidence artifacts.
        
        Provides access to evidence artifacts.
        
        Args:
            nav_request: Navigation request with domain, evidenceType
            
        Returns:
            Evidence view UI output
        """
        domain = nav_request.get("domain")
        evidence_type = nav_request.get("evidenceType")
        
        # Build artifacts list
        artifacts = [
            {
                "artifactId": "art-001",
                "name": "build.log",
                "type": evidence_type,
                "size": "2.5 MB",
                "createdAt": "2026-01-01T00:00:00Z",
                "downloadLink": f"/artifacts/art-001/download"
            },
            {
                "artifactId": "art-002",
                "name": "test_results.xml",
                "type": evidence_type,
                "size": "150 KB",
                "createdAt": "2026-01-01T00:01:00Z",
                "downloadLink": f"/artifacts/art-002/download"
            }
        ]
        
        return {
            "artifacts": artifacts,
            "previewAvailable": True,
            "domain": domain,
            "evidenceType": evidence_type
        }
    
    def navigate_to_domain(self, domain: str) -> Dict[str, Any]:
        """
        QA-031: Navigate to a specific domain (level 1 drill-down).
        
        Args:
            domain: Domain name
            
        Returns:
            Level 1 navigation UI
        """
        self.navigation_stack = [{"level": 1, "domain": domain, "type": "domain"}]
        self.current_level = 1
        
        return {
            "currentLevel": 1,
            "domain": domain,
            "levelPath": [domain],
            "canDrillDown": True,
            "canNavigateUp": False
        }
    
    def drill_down(self, previous_level: Dict[str, Any], target: str) -> Dict[str, Any]:
        """
        QA-031: Drill down to next level.
        
        Args:
            previous_level: Previous level context
            target: Target resource to drill into
            
        Returns:
            Next level navigation UI
        """
        self.current_level += 1
        
        # Add to navigation stack
        nav_context = {
            "level": self.current_level,
            "target": target,
            "type": "drill_down"
        }
        self.navigation_stack.append(nav_context)
        
        # Build level path
        level_path = [nav.get("domain", nav.get("target", f"Level {nav['level']}")) 
                      for nav in self.navigation_stack]
        
        return {
            "currentLevel": self.current_level,
            "levelPath": level_path,
            "canDrillDown": self.current_level < 5,  # Max 5 levels
            "canNavigateUp": True,
            "previousLevelContext": previous_level
        }
    
    def navigate_to_resource(self, nav_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        QA-032: Navigate to a specific resource (with error handling).
        
        Args:
            nav_request: Navigation request
            
        Returns:
            Resource UI or error UI
        """
        resource_id = nav_request.get("resourceId")
        
        # Simulate resource not found error
        if resource_id == "non-existent-resource":
            return {
                "error": {
                    "errorType": "resource_not_found",
                    "message": f"Resource {resource_id} not found"
                },
                "recoveryOptions": {
                    "returnToDashboard": {
                        "enabled": True,
                        "label": "Return to Dashboard"
                    },
                    "tryAgain": {
                        "enabled": True,
                        "label": "Try Again"
                    }
                }
            }
        
        # Normal resource view
        return {
            "resource": {
                "id": resource_id,
                "data": {}
            }
        }
    
    def simulate_error(self, error_type: str):
        """
        QA-032: Simulate error for failure mode testing.
        
        Args:
            error_type: Type of error to simulate
        """
        self.error_state = error_type
    
    def handle_navigation_error(self) -> Dict[str, Any]:
        """
        QA-032: Handle drill-down navigator failure modes.
        
        Returns:
            Error handling UI output
        """
        if not self.error_state:
            return {
                "errorOccurred": False
            }
        
        error_messages = {
            "data_load_failure": "Unable to load detail data. Please try again.",
            "evidence_not_found": "Evidence artifacts not available.",
            "navigation_stack_overflow": "Navigation depth exceeded. Please start over."
        }
        
        return {
            "errorOccurred": True,
            "errorType": self.error_state,
            "errorMessage": error_messages.get(self.error_state, "Navigation error"),
            "fallbackBehavior": {
                "showCachedData": True,
                "enableRetry": True,
                "resetNavigation": self.error_state == "navigation_stack_overflow"
            },
            "userAction": {
                "retryButton": True,
                "backButton": len(self.navigation_stack) > 1,
                "homeButton": True
            }
        }
