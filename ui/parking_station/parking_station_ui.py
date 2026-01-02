"""
ParkingStationUI (PARK-04)

QA Coverage: QA-043 to QA-046 (actually QA-054 to QA-057 based on tests)

Manages UI for parking station functionality.
"""

from typing import Dict, Any, List
from datetime import datetime


class ParkingStationUI:
    """
    PARK-04: Parking Station UI
    
    Handles UI for:
    - Rendering parked items list
    - Park/unpark actions
    - Parking reason display
    - Error handling
    """
    
    def __init__(self, context: Dict[str, Any]):
        """
        Initialize parking station UI.
        
        Args:
            context: UI context with organisation_id, user_id, session_id
        """
        self.context = context
        self.error_state = None
    
    def render_parked_items(self, parked_items_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        QA-054: Render parked items list.
        
        Args:
            parked_items_data: List of parked items
            
        Returns:
            Parked items list UI output
        """
        # Check for error state first (QA-057)
        if self.error_state == "load_failure":
            return {
                "error": {
                    "errorType": "load_failure",
                    "message": "Unable to load parked items"
                },
                "retryAction": {
                    "available": True,
                    "label": "Retry"
                }
            }
        
        items = []
        for item_data in parked_items_data:
            item_ui = {
                "itemId": item_data.get("itemId"),
                "title": item_data.get("title"),
                "content": item_data.get("content"),
                "category": item_data.get("category"),
                "statusIndicator": {
                    "status": "parked",
                    "visual": "status-parked-gray"
                },
                "actions": {
                    "unpark": {
                        "enabled": True,
                        "label": "Unpark"
                    },
                    "viewDetail": {
                        "enabled": True,
                        "label": "View Details"
                    }
                }
            }
            items.append(item_ui)
        
        return {
            "items": items,
            "controls": {
                "sortOptions": ["date", "category", "priority"],
                "filterOptions": ["all", "enhancements", "ideas", "deferrals"]
            }
        }
    
    def park_item(self, park_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        QA-055: Park an item.
        
        Args:
            park_request: Park request with itemId, title, content, reason
            
        Returns:
            Park action UI output
        """
        # Validate required fields (QA-057)
        validation_errors = []
        if not park_request.get("title"):
            validation_errors.append("title")
        if not park_request.get("content"):
            validation_errors.append("content")
        if not park_request.get("reason"):
            validation_errors.append("reason")
        
        if validation_errors:
            return {
                "action": "park",
                "feedback": {
                    "success": False,
                    "errorMessage": "Missing required fields"
                },
                "validationErrors": validation_errors
            }
        
        return {
            "action": "park",
            "itemId": park_request.get("itemId"),
            "feedback": {
                "success": True,
                "message": f"Item '{park_request.get('title')}' parked successfully",
                "itemRemoved": False  # Item added to parking, not removed
            },
            "reasonRequired": True,
            "reasonProvided": park_request.get("reason") is not None
        }
    
    def unpark_item(self, unpark_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        QA-055: Unpark an item (request confirmation).
        
        Args:
            unpark_request: Unpark request with itemId
            
        Returns:
            Unpark action UI output (requesting confirmation)
        """
        return {
            "action": "unpark",
            "itemId": unpark_request.get("itemId"),
            "confirmation": {
                "required": True,
                "message": "Are you sure you want to unpark this item?",
                "buttons": {
                    "confirm": "Yes, Unpark",
                    "cancel": "Cancel"
                }
            }
        }
    
    def confirm_unpark(self, unpark_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        QA-055: Confirm unpark action.
        
        Args:
            unpark_request: Confirmed unpark request
            
        Returns:
            Unpark confirmation UI output
        """
        return {
            "action": "unpark",
            "itemId": unpark_request.get("itemId"),
            "feedback": {
                "success": True,
                "message": "Item unparked successfully",
                "itemRemoved": True
            }
        }
    
    def render_item_detail(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        QA-056: Render item detail with parking reason.
        
        Args:
            item_data: Parked item data
            
        Returns:
            Item detail UI output
        """
        return {
            "itemId": item_data.get("itemId"),
            "title": item_data.get("title"),
            "content": item_data.get("content"),
            "category": item_data.get("category"),
            "reason": {
                "text": item_data.get("reason"),
                "category": item_data.get("category")
            },
            "parkingMetadata": {
                "parkedBy": item_data.get("parkedBy"),
                "parkedAt": item_data.get("parkedAt"),
                "parkedAtDisplay": self._format_timestamp(item_data.get("parkedAt"))
            }
        }
    
    def simulate_error(self, error_type: str):
        """
        QA-057: Simulate error for testing.
        
        Args:
            error_type: Type of error to simulate
        """
        self.error_state = error_type
    
    def simulate_load_failure(self):
        """
        QA-057: Simulate load failure for testing.
        """
        self.error_state = "load_failure"
    
    def render_with_error_handling(self) -> Dict[str, Any]:
        """
        QA-057: Render parking station UI with error handling.
        
        Returns:
            Error UI if error state active
        """
        if not self.error_state:
            return {"errorOccurred": False}
        
        error_messages = {
            "load_failure": "Unable to load parked items. Please try again.",
            "park_failure": "Unable to park item. Please try again.",
            "unpark_failure": "Unable to unpark item. Please try again."
        }
        
        return {
            "errorOccurred": True,
            "errorType": self.error_state,
            "errorMessage": error_messages.get(self.error_state, "Unknown error"),
            "recoveryOptions": {
                "retry": {
                    "enabled": True,
                    "label": "Retry"
                },
                "backToDashboard": {
                    "enabled": True,
                    "label": "Back to Dashboard"
                }
            }
        }
    
    def _format_timestamp(self, timestamp_str: str) -> str:
        """Format ISO timestamp for display."""
        if not timestamp_str:
            return ""
        
        try:
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            return timestamp_str
