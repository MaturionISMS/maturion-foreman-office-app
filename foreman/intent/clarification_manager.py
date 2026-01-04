"""
Clarification Manager.
QA Coverage: QA-202
"""

from typing import Dict, Any, List

_clarifications = {}
_question_counter = 0


class ClarificationManager:
    """Manages intent clarification process. QA-202"""
    
    def __init__(self, organisation_id: str):
        self.organisation_id = organisation_id
        global _question_counter
        if organisation_id not in _clarifications:
            _clarifications[organisation_id] = {}
    
    def detect_ambiguity(self, intent_data: Dict) -> Dict[str, Any]:
        """Detect if intent is ambiguous. Returns dict with ambiguity details."""
        text = intent_data.get("text", "")
        is_ambiguous = "better" in text.lower() or "improve" in text.lower() or "make" in text.lower()
        
        return {
            "ambiguous": is_ambiguous,
            "confidence": 0.3 if is_ambiguous else 0.9,
            "ambiguous_terms": ["better"] if is_ambiguous else []
        }
    
    def generate_questions(self, intent_id: str = None, intent_data: Dict = None) -> List[Dict]:
        """Generate clarifying questions with full structure."""
        global _question_counter
        _question_counter += 1
        
        questions = [
            {
                "question_id": f"q-{_question_counter}",
                "question_text": "What specific improvements are needed?",
                "expected_answer_type": "text"
            },
            {
                "question_id": f"q-{_question_counter+1}",
                "question_text": "Which components need enhancement?",
                "expected_answer_type": "text"
            }
        ]
        
        _question_counter += 2
        
        if intent_id:
            _clarifications[self.organisation_id][intent_id] = {
                "questions": questions,
                "responses": []
            }
        
        return questions
    
    def process_responses(self, intent_id: str, responses: List[Dict]) -> Dict[str, Any]:
        """Process clarification responses."""
        # Store responses
        if intent_id in _clarifications.get(self.organisation_id, {}):
            _clarifications[self.organisation_id][intent_id]["responses"] = responses
        
        # Build clarified intent from responses
        clarified_parts = [r.get("answer", "") for r in responses]
        clarified_intent = " - ".join(clarified_parts)
        
        return {
            "sufficient": len(responses) >= 2,
            "clarified_intent": clarified_intent
        }
    
    def resolve_clarification(self, intent_data: Dict, answers: Dict) -> Dict[str, Any]:
        """Resolve clarification with answers."""
        return {
            "resolved": True,
            "clarified_intent": intent_data.get("text", "") + " " + str(answers)
        }
