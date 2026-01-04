"""
ConversationUIRenderer (CONV-05)

QA Coverage: QA-019 to QA-022

Renders conversation UI with message display, real-time updates,
state indicators, and error handling.
"""

from typing import Dict, Any, List
from datetime import datetime


class ConversationUIRenderer:
    """
    CONV-05: Conversation UI Renderer
    
    Responsible for rendering conversation UI components including:
    - Message display with visual distinction
    - Real-time updates
    - Conversation state indicators
    - Error handling and graceful degradation
    """
    
    def __init__(self, context: Dict[str, Any]):
        """
        Initialize renderer with context.
        
        Args:
            context: UI context with organisation_id, user_id, session_id
        """
        self.context = context
        self.connection_lost = False
        self.messages = []
    
    def render_conversation(self, conversation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        QA-019: Render conversation UI.
        
        Renders complete conversation UI with:
        - Message list
        - Visual distinction between Johan and FM
        - Timestamps
        - Conversation controls
        - Input field
        
        Args:
            conversation_data: Conversation data with messages
            
        Returns:
            UI output structure with rendered components
        """
        # Store messages for internal tracking
        self.messages = conversation_data.get("messages", [])
        
        # Render each message with visual styling
        rendered_messages = []
        for message in self.messages:
            sender_role = message.get("senderRole", "Unknown")
            
            # Determine visual class based on sender
            if sender_role == "Johan":
                visual_class = "message-johan"
            elif sender_role == "FM":
                visual_class = "message-fm"
            else:
                visual_class = "message-unknown"
            
            rendered_message = {
                "messageId": message.get("messageId"),
                "content": message.get("content"),
                "senderRole": sender_role,
                "visualClass": visual_class,
                "timestamp": message.get("timestamp"),
                "timestampDisplay": self._format_timestamp(message.get("timestamp")),
                "status": message.get("status", "unread")
            }
            rendered_messages.append(rendered_message)
        
        # Build conversation controls
        controls = {
            "archiveButton": {
                "enabled": conversation_data.get("status") != "archived",
                "label": "Archive Conversation"
            }
        }
        
        # Build input field
        input_field = {
            "enabled": not self.connection_lost and conversation_data.get("status") == "active",
            "placeholder": "Type your message..."
        }
        
        # Build status indicator
        status = conversation_data.get("status", "active")
        status_indicator = self._build_status_indicator(status)
        
        # Build connection status
        connection_status = {
            "connected": not self.connection_lost
        }
        
        if self.connection_lost:
            connection_status["errorMessage"] = "Connection lost. Attempting to reconnect..."
        
        # Build complete UI output
        ui_output = {
            "messages": rendered_messages,
            "controls": controls,
            "inputField": input_field,
            "statusIndicator": status_indicator,
            "connectionStatus": connection_status,
            "degradedMode": self.connection_lost,
            "readOnly": self.connection_lost or status != "active"
        }
        
        # Add retry control if connection lost
        if self.connection_lost:
            ui_output["retryControl"] = {
                "retryButton": {
                    "enabled": True,
                    "label": "Retry Connection"
                },
                "autoRetry": {
                    "enabled": True,
                    "interval": 5,
                    "maxAttempts": 3
                }
            }
        
        return ui_output
    
    def update_with_new_message(self, new_message: Dict[str, Any]) -> Dict[str, Any]:
        """
        QA-020: Update conversation UI with new message (real-time).
        
        Handles real-time message updates with:
        - Incremental update (no full refresh)
        - Auto-scroll to new message
        - New message highlighting
        
        Args:
            new_message: New message data
            
        Returns:
            Updated UI output with new message
        """
        # Add new message to internal tracking
        self.messages.append(new_message)
        
        # Render all messages (including new one)
        rendered_messages = []
        for idx, message in enumerate(self.messages):
            sender_role = message.get("senderRole", "Unknown")
            
            # Determine visual class
            if sender_role == "Johan":
                visual_class = "message-johan"
            elif sender_role == "FM":
                visual_class = "message-fm"
            else:
                visual_class = "message-unknown"
            
            rendered_message = {
                "messageId": message.get("messageId"),
                "content": message.get("content"),
                "senderRole": sender_role,
                "visualClass": visual_class,
                "timestamp": message.get("timestamp"),
                "timestampDisplay": self._format_timestamp(message.get("timestamp")),
                "status": message.get("status", "unread"),
                # Highlight only the new message (last one)
                "highlighted": (idx == len(self.messages) - 1)
            }
            rendered_messages.append(rendered_message)
        
        # Build updated UI output
        updated_ui = {
            "messages": rendered_messages,
            "scrollBehavior": "auto-scroll-to-bottom",
            "updateType": "incremental"
        }
        
        return updated_ui
    
    def _build_status_indicator(self, status: str) -> Dict[str, Any]:
        """
        QA-021: Build conversation state indicator.
        
        Creates visual indicators for conversation states:
        - active: Green, editable
        - paused: Yellow, read-only temporarily
        - archived: Gray, read-only permanently
        
        Args:
            status: Conversation status
            
        Returns:
            Status indicator structure
        """
        visual_cues = {
            "active": "status-active-green",
            "paused": "status-paused-yellow",
            "archived": "status-archived-gray"
        }
        
        indicator = {
            "status": status,
            "visualCue": visual_cues.get(status, "status-unknown"),
            "readonly": (status == "archived")
        }
        
        return indicator
    
    def simulate_connection_loss(self):
        """
        QA-022: Simulate connection loss for error handling testing.
        """
        self.connection_lost = True
    
    def simulate_connection_restore(self):
        """
        QA-022: Simulate connection restoration for error recovery testing.
        """
        self.connection_lost = False
    
    def _format_timestamp(self, timestamp_str: str) -> str:
        """
        Format ISO timestamp for display.
        
        Args:
            timestamp_str: ISO format timestamp
            
        Returns:
            Human-readable timestamp
        """
        if not timestamp_str:
            return ""
        
        try:
            # Parse ISO timestamp
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            # Format for display
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            return timestamp_str
