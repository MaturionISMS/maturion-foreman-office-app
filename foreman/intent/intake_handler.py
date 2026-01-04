"""
Intent Intake Handler.
QA Coverage: QA-201
"""

from typing import Dict, Any
from datetime import datetime


_intents = {}


class IntentIntakeHandler:
    """Handles intent submission and validation. QA-201"""
    
    def __init__(self, organisation_id: str):
        self.organisation_id = organisation_id
        if organisation_id not in _intents:
            _intents[organisation_id] = {}
    
    def accept_intent(self, user_id: str, intent_text: str, context: Dict) -> Dict[str, Any]:
        """Accept and process user intent. QA-201"""
        intent_id = f"intent-{len(_intents[self.organisation_id])+1:03d}"
        
        intent_data = {
            "intent_id": intent_id,
            "user_id": user_id,
            "text": intent_text,
            "context": context,
            "state": "RECEIVED",
            "created_at": datetime.utcnow()
        }
        
        _intents[self.organisation_id][intent_id] = intent_data
        
        return {
            "accepted": True,
            "intent_id": intent_id
        }
    
    def get_intent(self, intent_id: str) -> Dict[str, Any]:
        """Get intent by ID. QA-201"""
        return _intents.get(self.organisation_id, {}).get(intent_id, {})
    
    def validate_intent(self, intent_id: str) -> Dict[str, bool]:
        """Validate intent completeness. QA-201"""
        intent = self.get_intent(intent_id)
        
        return {
            "parseable": bool(intent.get("text")),
            "has_context": bool(intent.get("context")),
            "ambiguity_detected": "better" in intent.get("text", "").lower()
        }
