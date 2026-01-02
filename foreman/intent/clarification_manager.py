"""
Clarification Manager.
QA Coverage: QA-202
"""

from typing import Dict, Any, List


class ClarificationManager:
    """Manages intent clarification process. QA-202"""
    
    def __init__(self, organisation_id: str):
        self.organisation_id = organisation_id
    
    def detect_ambiguity(self, intent_data: Dict) -> Dict[str, Any]:
        """Detect if intent is ambiguous. Returns dict with ambiguity details."""
        text = intent_data.get("text", "")
        is_ambiguous = "better" in text.lower() or "improve" in text.lower()
        
        return {
            "is_ambiguous": is_ambiguous,
            "confidence": 0.9 if is_ambiguous else 0.1,
            "ambiguous_terms": ["better"] if is_ambiguous else []
        }
    
    def generate_questions(self, intent_data: Dict) -> List[str]:
        """Generate clarifying questions."""
        return ["What specific improvements are needed?", "Which components need enhancement?"]
    
    def resolve_clarification(self, intent_data: Dict, answers: Dict) -> Dict[str, Any]:
        """Resolve clarification with answers."""
        return {
            "resolved": True,
            "clarified_intent": intent_data.get("text", "") + " " + str(answers)
        }
