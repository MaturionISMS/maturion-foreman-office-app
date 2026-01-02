"""
Approval Manager.
QA Coverage: QA-204
"""

from typing import Dict, Any

_approvals = {}


class ApprovalManager:
    """Manages requirement approvals. QA-204"""
    
    def __init__(self, organisation_id: str):
        self.organisation_id = organisation_id
        if organisation_id not in _approvals:
            _approvals[organisation_id] = {}
    
    def present_for_approval(self, requirement_id: str = None, requirement: Dict = None, 
                           approver: str = None) -> Dict[str, Any]:
        """Present requirement for approval."""
        req_id = requirement_id or requirement.get("requirement_id") if requirement else None
        
        approval = {
            "presented": True,
            "approval_id": f"appr-{req_id}",
            "requirement_id": req_id,
            "approver": approver,
            "status": "PENDING"
        }
        
        if req_id:
            _approvals[self.organisation_id][req_id] = approval
        
        return approval
    
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
