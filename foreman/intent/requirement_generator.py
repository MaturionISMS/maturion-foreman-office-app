"""
Requirement Generator.
QA Coverage: QA-203
"""

from typing import Dict, Any, List


class RequirementGenerator:
    """Generates requirements from clarified intent. QA-203"""
    
    def __init__(self, organisation_id: str):
        self.organisation_id = organisation_id
    
    def generate_requirement(self, clarified_intent: Dict) -> Dict[str, Any]:
        """Generate comprehensive requirement specification from intent."""
        intent_text = clarified_intent.get("text", "")
        clarifications = clarified_intent.get("clarifications", [])
        
        # Generate acceptance criteria from clarifications
        acceptance_criteria = []
        for clarif in clarifications:
            criterion = {
                "criterion_id": f"ac-{len(acceptance_criteria)+1}",
                "description": f"Must satisfy: {clarif.get('answer', '')}",
                "verification_method": "manual_review"
            }
            acceptance_criteria.append(criterion)
        
        if not acceptance_criteria:
            acceptance_criteria.append({
                "criterion_id": "ac-1",
                "description": "Must implement as specified",
                "verification_method": "manual_review"
            })
        
        return {
            "requirement_id": "req-001",
            "title": intent_text[:50] if len(intent_text) > 50 else intent_text,
            "description": intent_text,
            "acceptance_criteria": acceptance_criteria,
            "scope": {
                "included": [intent_text],
                "excluded": []
            },
            "dependencies": [],
            "state": "DRAFT",
            "status": "DRAFT",
            "original_intent_id": clarified_intent.get("intent_id"),
            "clarification_history": clarifications
        }
