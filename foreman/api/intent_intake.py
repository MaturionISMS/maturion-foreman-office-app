"""
Intent Intake Handler (INTENT-01)

QA Coverage: QA-058 to QA-061
Architecture: FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md Section INTENT-01

Responsibilities:
- Accept informal intent from user messages
- Validate intent input for required context
- Route ambiguous intents to clarification loop
- Handle intake failure modes
"""

from typing import Dict, Any, Optional
from datetime import datetime


class IntentIntakeHandler:
    """
    INTENT-01: Intent Intake Handler
    
    Processes user messages to extract and validate intents.
    Routes to clarification if ambiguous, otherwise creates Intent entity.
    """
    
    def __init__(self):
        """Initialize Intent Intake Handler"""
        self.pending_intents = {}
    
    def accept_intent(self, message_content: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        QA-058: Accept informal intent
        
        Accepts partial input and informal language from user messages.
        Captures context and validates basic structure.
        
        Args:
            message_content: User's message content (informal, partial OK)
            context: Optional context (conversation_id, user_id, etc.)
        
        Returns:
            Dict with:
                - intent_id: Unique intent identifier
                - content: Original message content
                - context: Captured context
                - state: Initial state (RECEIVED)
                - timestamp: Creation timestamp
        """
        if not message_content or not message_content.strip():
            raise ValueError("Intent content cannot be empty")
        
        intent_id = f"intent_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        intent = {
            "intent_id": intent_id,
            "content": message_content.strip(),
            "context": context or {},
            "state": "RECEIVED",
            "timestamp": datetime.now().isoformat(),
            "validation_status": "pending"
        }
        
        self.pending_intents[intent_id] = intent
        return intent
    
    def validate_intent(self, intent_id: str) -> Dict[str, Any]:
        """
        QA-059: Validate intent input
        
        Validates that intent has required context and is parseable.
        Checks for minimum required information to proceed.
        
        Args:
            intent_id: Intent identifier to validate
        
        Returns:
            Dict with:
                - valid: Boolean validation result
                - intent_id: Intent identifier
                - missing_context: List of missing required context
                - parseable: Boolean indicating if intent is parseable
        """
        if intent_id not in self.pending_intents:
            raise ValueError(f"Intent not found: {intent_id}")
        
        intent = self.pending_intents[intent_id]
        
        # Check for required context
        required_context = ["conversation_id"]
        missing_context = [
            ctx for ctx in required_context 
            if ctx not in intent.get("context", {})
        ]
        
        # Check parseability (basic check - intent has content)
        parseable = bool(intent.get("content") and len(intent["content"]) > 0)
        
        valid = len(missing_context) == 0 and parseable
        
        validation_result = {
            "valid": valid,
            "intent_id": intent_id,
            "missing_context": missing_context,
            "parseable": parseable
        }
        
        # Update intent validation status
        intent["validation_status"] = "valid" if valid else "invalid"
        intent["validation_result"] = validation_result
        
        return validation_result
    
    def route_to_clarification(self, intent_id: str, ambiguity_reason: str) -> Dict[str, Any]:
        """
        QA-060: Route intent to clarification
        
        Detects ambiguity and initiates clarification flow.
        Triggers INTENT-02 Clarification Loop Manager.
        
        Args:
            intent_id: Intent identifier with detected ambiguity
            ambiguity_reason: Reason for ambiguity (missing info, unclear, multiple interpretations)
        
        Returns:
            Dict with:
                - intent_id: Intent identifier
                - routed_to: Destination component (INTENT-02)
                - ambiguity_detected: Boolean
                - ambiguity_reason: Reason for clarification
                - clarification_flow_initiated: Boolean
        """
        if intent_id not in self.pending_intents:
            raise ValueError(f"Intent not found: {intent_id}")
        
        intent = self.pending_intents[intent_id]
        
        # Update intent state to CLARIFYING
        intent["state"] = "CLARIFYING"
        intent["ambiguity_reason"] = ambiguity_reason
        intent["clarification_initiated_at"] = datetime.now().isoformat()
        
        routing_result = {
            "intent_id": intent_id,
            "routed_to": "INTENT-02",
            "ambiguity_detected": True,
            "ambiguity_reason": ambiguity_reason,
            "clarification_flow_initiated": True
        }
        
        return routing_result
    
    def handle_intake_failure(self, intent_id: str, failure_type: str, error_details: str) -> Dict[str, Any]:
        """
        QA-061: Intent Intake failure modes
        
        Handles unparseable input and context loss detection/recovery.
        Implements retry logic and escalation for persistent failures.
        
        Args:
            intent_id: Intent identifier experiencing failure
            failure_type: Type of failure (unparseable, context_loss, validation_error)
            error_details: Detailed error information
        
        Returns:
            Dict with:
                - intent_id: Intent identifier
                - failure_type: Type of failure
                - recovery_action: Action taken (retry, escalate, store_pending)
                - retry_count: Number of retry attempts
                - escalated: Boolean indicating if escalated
        """
        if intent_id not in self.pending_intents:
            # Context loss detected - try recovery
            return {
                "intent_id": intent_id,
                "failure_type": "context_loss",
                "recovery_action": "escalate",
                "retry_count": 0,
                "escalated": True,
                "error_details": "Intent not found in memory - context loss detected"
            }
        
        intent = self.pending_intents[intent_id]
        
        # Get or initialize retry count
        retry_count = intent.get("retry_count", 0)
        
        # Determine recovery action
        if failure_type == "unparseable":
            if retry_count < 3:
                recovery_action = "retry"
                retry_count += 1
                intent["retry_count"] = retry_count
                intent["state"] = "PENDING"
            else:
                recovery_action = "escalate"
                intent["state"] = "FAILED"
                intent["escalated"] = True
        elif failure_type == "context_loss":
            recovery_action = "escalate"
            intent["state"] = "FAILED"
            intent["escalated"] = True
        else:
            recovery_action = "store_pending"
            intent["state"] = "PENDING"
        
        intent["last_failure"] = {
            "type": failure_type,
            "details": error_details,
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "intent_id": intent_id,
            "failure_type": failure_type,
            "recovery_action": recovery_action,
            "retry_count": retry_count,
            "escalated": recovery_action == "escalate",
            "error_details": error_details
        }
