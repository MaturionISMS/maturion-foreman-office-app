"""
Authority Enforcer (CROSS-02).
QA Coverage: QA-158 to QA-168
"""

from typing import Dict, Any, List

_override_audit = {}


def clear_all():
    """Clear all authority enforcer state for testing."""
    global _override_audit
    _override_audit = {}


class AuthorityEnforcer:
    """Enforces authority and permission checks. QA-158 to QA-168"""
    
    def __init__(self):
        pass
    
    def check_authority(self, context, action: str, resource: str) -> bool:
        """Check if context has authority for action. QA-158"""
        if context.role == "JOHAN":
            return True
        if "ALL" in context.permissions:
            return True
        return action in context.permissions
    
    def can_override(self, context, policy: str) -> bool:
        """Check if context can override policy. QA-158"""
        return context.role == "JOHAN"
    
    def execute_override(self, context, policy: str, reason: str) -> Dict[str, Any]:
        """Execute override with audit. QA-158"""
        if context.user_id not in _override_audit:
            _override_audit[context.user_id] = []
        
        _override_audit[context.user_id].append({
            "user_id": context.user_id,
            "policy": policy,
            "reason": reason,
            "timestamp": "2026-01-02T16:00:00"
        })
        
        return {"success": True}
    
    def get_override_audit(self, user_id: str) -> List[Dict]:
        """Get override audit log. QA-158"""
        return _override_audit.get(user_id, [])
