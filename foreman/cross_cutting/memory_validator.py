"""Memory Consistency Validator. QA-153"""

from typing import Dict, Any, List


class MemoryConsistencyValidator:
    """Validates memory consistency."""
    
    def __init__(self, manager):
        self.manager = manager
    
    def validate_consistency(self) -> Dict[str, Any]:
        """Validate memory consistency. QA-153"""
        import sys
        sys.path.insert(0, '/home/runner/work/maturion-foreman-office-app/maturion-foreman-office-app')
        from foreman.cross_cutting.memory_manager import _memories
        
        conflicts = []
        org_memories = _memories.get(self.manager.organisation_id, {})
        
        for key, mem_list in org_memories.items():
            for mem in mem_list:
                if mem.get("conflicts_with"):
                    conflicts.append({
                        "involved_keys": [key] + mem.get("conflicts_with", []),
                        "severity": "HIGH"
                    })
        
        return {
            "consistent": len(conflicts) == 0,
            "issues": [],
            "conflicts": conflicts
        }
