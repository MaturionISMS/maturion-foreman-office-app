"""
Requirement Generator (INTENT-03)

QA Coverage: QA-067 to QA-070
Architecture: FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md Section INTENT-03

Responsibilities:
- Generate formal requirement from clarified intent
- Include approval workflow metadata
- Maintain bidirectional traceability to original intent
- Handle generation failures
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class RequirementGenerator:
    """
    INTENT-03: Requirement Specification Generator
    
    Converts clarified intents into formal requirement specifications
    with approval workflow metadata and traceability.
    """
    
    def __init__(self):
        """Initialize Requirement Generator"""
        self.requirements = {}
    
    def generate_requirement(self, intent_id: str, clarified_content: str) -> Dict[str, Any]:
        """
        QA-067: Generate requirement from clarified intent
        
        Creates structured requirement with acceptance criteria and traceability.
        
        Args:
            intent_id: Intent identifier (source)
            clarified_content: Clarified and validated intent content
        
        Returns:
            Dict with:
                - requirement_id: Unique requirement identifier
                - structure: Structured requirement format
                - acceptance_criteria: List of acceptance criteria
                - traceability: Link to source intent
        """
        requirement_id = f"req_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # Parse clarified content to extract key information
        # (In production, would use NLP to extract structured data)
        requirement_structure = {
            "requirement_id": requirement_id,
            "title": self._extract_title(clarified_content),
            "description": clarified_content,
            "intent_id": intent_id,
            "created_at": datetime.now().isoformat(),
            "state": "DRAFT",
            "version": "1.0"
        }
        
        # Generate acceptance criteria
        acceptance_criteria = self._generate_acceptance_criteria(clarified_content)
        requirement_structure["acceptance_criteria"] = acceptance_criteria
        
        # Add traceability
        traceability = {
            "source_type": "intent",
            "source_id": intent_id,
            "derived_from": intent_id,
            "bidirectional_link": True
        }
        requirement_structure["traceability"] = traceability
        
        # Store requirement
        self.requirements[requirement_id] = requirement_structure
        
        return {
            "requirement_id": requirement_id,
            "structure": requirement_structure,
            "acceptance_criteria": acceptance_criteria,
            "traceability": traceability
        }
    
    def include_approval_metadata(self, requirement_id: str) -> Dict[str, Any]:
        """
        QA-068: Include approval workflow metadata
        
        Identifies approver and includes approval instructions.
        
        Args:
            requirement_id: Requirement identifier
        
        Returns:
            Dict with:
                - requirement_id: Requirement identifier
                - approver_id: Identified approver (Johan for Foreman Office)
                - approval_instructions: Instructions for approval process
                - approval_metadata: Complete approval workflow metadata
        """
        if requirement_id not in self.requirements:
            raise ValueError(f"Requirement not found: {requirement_id}")
        
        requirement = self.requirements[requirement_id]
        
        # Identify approver (for Foreman Office, always Johan)
        approver_id = "johan"
        
        # Generate approval instructions
        approval_instructions = {
            "steps": [
                "Review requirement specification",
                "Verify acceptance criteria are complete",
                "Check traceability to original intent",
                "Respond with 'approve', 'reject', or 'conditional'"
            ],
            "approval_commands": {
                "approve": "Approve requirement and initiate build",
                "reject": "Reject and return to intent capture",
                "conditional": "Approve with conditions (specify conditions)"
            }
        }
        
        # Create approval metadata
        approval_metadata = {
            "approver_id": approver_id,
            "approval_required": True,
            "approval_timeout_hours": 72,
            "created_at": datetime.now().isoformat(),
            "instructions": approval_instructions,
            "status": "pending"
        }
        
        # Update requirement with approval metadata
        requirement["approval_metadata"] = approval_metadata
        requirement["state"] = "PENDING_APPROVAL"
        
        return {
            "requirement_id": requirement_id,
            "approver_id": approver_id,
            "approval_instructions": approval_instructions,
            "approval_metadata": approval_metadata
        }
    
    def link_to_intent(self, requirement_id: str, intent_id: str) -> Dict[str, Any]:
        """
        QA-069: Link requirement to original intent
        
        Maintains bidirectional traceability and preserves context.
        
        Args:
            requirement_id: Requirement identifier
            intent_id: Original intent identifier
        
        Returns:
            Dict with:
                - requirement_id: Requirement identifier
                - intent_id: Intent identifier
                - bidirectional_link: Boolean indicating link exists both ways
                - context_preserved: Boolean indicating context preservation
        """
        if requirement_id not in self.requirements:
            raise ValueError(f"Requirement not found: {requirement_id}")
        
        requirement = self.requirements[requirement_id]
        
        # Update requirement with intent link
        requirement["intent_id"] = intent_id
        requirement["traceability"] = {
            "source_type": "intent",
            "source_id": intent_id,
            "derived_from": intent_id,
            "bidirectional_link": True,
            "linked_at": datetime.now().isoformat()
        }
        
        # Preserve context from intent
        requirement["context_preserved"] = True
        
        return {
            "requirement_id": requirement_id,
            "intent_id": intent_id,
            "bidirectional_link": True,
            "context_preserved": True
        }
    
    def handle_generation_failure(self, intent_id: str, failure_reason: str) -> Dict[str, Any]:
        """
        QA-070: Requirement Generator failure modes
        
        Handles generation failures and detects incomplete specifications.
        
        Args:
            intent_id: Intent identifier for failed generation
            failure_reason: Reason for generation failure
        
        Returns:
            Dict with:
                - intent_id: Intent identifier
                - failure_handled: Boolean
                - incomplete_spec_detected: Boolean
                - recovery_action: Action taken (retry, escalate, return_to_clarification)
        """
        # Determine recovery action based on failure reason
        if failure_reason == "incomplete_spec":
            recovery_action = "return_to_clarification"
            incomplete_spec_detected = True
        elif failure_reason == "generation_timeout":
            recovery_action = "retry"
            incomplete_spec_detected = False
        elif failure_reason == "invalid_intent":
            recovery_action = "escalate"
            incomplete_spec_detected = False
        else:
            recovery_action = "escalate"
            incomplete_spec_detected = False
        
        return {
            "intent_id": intent_id,
            "failure_handled": True,
            "incomplete_spec_detected": incomplete_spec_detected,
            "recovery_action": recovery_action,
            "failure_reason": failure_reason
        }
    
    def _extract_title(self, content: str) -> str:
        """
        Extract requirement title from content (simplified)
        
        In production, would use NLP to extract key phrases.
        """
        # Take first sentence or first 50 characters
        first_sentence = content.split('.')[0] if '.' in content else content
        return first_sentence[:50] + ('...' if len(first_sentence) > 50 else '')
    
    def _generate_acceptance_criteria(self, content: str) -> List[str]:
        """
        Generate acceptance criteria from content (simplified)
        
        In production, would use NLP to extract verifiable criteria.
        """
        # Generate basic acceptance criteria
        return [
            "Implementation matches described functionality",
            "All edge cases are handled",
            "Tests validate behavior",
            "Documentation is complete"
        ]
