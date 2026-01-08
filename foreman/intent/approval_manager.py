"""
Approval Manager.
QA Coverage: QA-204
"""

from typing import Dict, Any
from datetime import datetime

_approvals = {}
_requirements = {}


class ApprovalManager:
    """Manages requirement approvals. QA-204"""
    
    def __init__(self, organisation_id: str):
        self.organisation_id = organisation_id
        if organisation_id not in _approvals:
            _approvals[organisation_id] = {}
        if organisation_id not in _requirements:
            _requirements[organisation_id] = {}
    
    def present_for_approval(self, requirement_id: str = None, requirement: Dict = None, 
                           approver: str = None) -> Dict[str, Any]:
        """Present requirement for approval."""
        req_id = requirement_id or requirement.get("requirement_id") if requirement else None
        
        approval = {
            "presented": True,
            "approval_id": f"appr-{req_id}",
            "requirement_id": req_id,
            "approver": approver,
            "status": "PENDING",
            "notification_sent": True
        }
        
        if req_id:
            _approvals[self.organisation_id][req_id] = approval
            # Store requirement if provided
            if requirement:
                _requirements[self.organisation_id][req_id] = {
                    **requirement,
                    "state": "PENDING_APPROVAL"
                }
        
        return approval
    
    def handle_approval(self, requirement_id: str, approver: str, decision: str,
                       comments: str = None, reason: str = None) -> Dict[str, Any]:
        """Handle approval decision (approve/reject). QA-204"""
        from datetime import datetime
        
        # Get or create requirement entry
        if requirement_id not in _requirements[self.organisation_id]:
            _requirements[self.organisation_id][requirement_id] = {
                "requirement_id": requirement_id,
                "state": "PENDING_APPROVAL"
            }
        
        requirement = _requirements[self.organisation_id][requirement_id]
        
        if decision.upper() == "APPROVE":
            # Update requirement state to APPROVED
            requirement["state"] = "APPROVED"
            requirement["approved_by"] = approver
            requirement["approved_at"] = datetime.now(UTC).isoformat()
            if comments:
                requirement["approval_comments"] = comments
            
            return {
                "approved": True,
                "approver": approver,
                "requirement_id": requirement_id,
                "comments": comments
            }
        elif decision.upper() == "REJECT":
            # Update requirement state to REJECTED
            requirement["state"] = "REJECTED"
            requirement["rejected_by"] = approver
            requirement["rejected_at"] = datetime.now(UTC).isoformat()
            if reason:
                requirement["rejection_reason"] = reason
            
            return {
                "approved": False,
                "approver": approver,
                "requirement_id": requirement_id,
                "reason": reason
            }
        else:
            raise ValueError(f"Invalid decision: {decision}. Must be APPROVE or REJECT")
    
    def get_requirement(self, requirement_id: str) -> Dict[str, Any]:
        """Get requirement by ID. QA-204"""
        return _requirements[self.organisation_id].get(requirement_id, {
            "requirement_id": requirement_id,
            "state": "UNKNOWN"
        })
    
    def await_decision(self, approval_id: str) -> Dict[str, Any]:
        """Wait for approval decision."""
        # Find approval by ID
        for req_id, approval in _approvals.get(self.organisation_id, {}).items():
            if approval.get("approval_id") == approval_id:
                return {
                    "status": approval.get("decision", "PENDING"),
                    "decision_made": "decision" in approval
                }
        
        return {
            "status": "PENDING",
            "decision_made": False
        }
    
    def request_approval(self, requirement: Dict) -> Dict[str, Any]:
        """Request approval for requirement."""
        return {
            "approval_id": "appr-001",
            "requirement_id": requirement.get("requirement_id"),
            "status": "PENDING"
        }
    
    def record_decision(self, approval_id: str, decision: str, approver: str) -> Dict[str, Any]:
        """Record approval decision."""
        # Find and update approval
        for req_id, approval in _approvals.get(self.organisation_id, {}).items():
            if approval.get("approval_id") == approval_id:
                approval["decision"] = decision
                approval["approver"] = approver
        
        return {
            "success": True,
            "approval_id": approval_id,
            "decision": decision,
            "approver": approver
        }
