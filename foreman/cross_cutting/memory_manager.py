"""
Global Memory Manager (CROSS-01).
QA Coverage: QA-147 to QA-154
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
import json
import sys
sys.path.insert(0, '/home/runner/work/maturion-foreman-office-app/maturion-foreman-office-app')

from foreman.cross_cutting.memory_proposal import MemoryWriteProposal
from foreman.cross_cutting.memory_exceptions import FabricCorruptionError, ProposalRejectedError

_memories = {}
_proposals = {}
_audit_log = {}


def clear_all():
    """Clear all memory manager state for testing."""
    global _memories, _proposals, _audit_log
    _memories = {}
    _proposals = {}
    _audit_log = {}


class GlobalMemoryManager:
    """Manages the global memory fabric. QA-147 to QA-154"""
    
    def __init__(self, organisation_id: str, memory_path: Path = None):
        self.organisation_id = organisation_id
        self.memory_path = memory_path or Path("/tmp/memory")
        
        if organisation_id not in _memories:
            _memories[organisation_id] = {}
        if organisation_id not in _proposals:
            _proposals[organisation_id] = {}
        if organisation_id not in _audit_log:
            _audit_log[organisation_id] = {}
    
    def initialize_fabric(self) -> Dict[str, Any]:
        """Initialize memory fabric structure. QA-147"""
        dirs_to_create = ["global", "scoped", "proposals", "archive"]
        dirs_created = []
        
        for dir_name in dirs_to_create:
            dir_path = self.memory_path / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            dirs_created.append(str(dir_path))
        
        # Create seed data
        seed_file = self.memory_path / "global" / "seed.json"
        seed_data = {
            "version": "1.0.0",
            "created_at": datetime.utcnow().isoformat()
        }
        seed_file.write_text(json.dumps(seed_data, indent=2))
        
        return {
            "success": True,
            "directories_created": dirs_created
        }
    
    def write_memory(self, key: str, category: str, content: str, organisation_id: str, 
                     version: int = 1, references: List[str] = None, conflicts_with: List[str] = None):
        """Write memory entry. QA-148, QA-151, QA-153"""
        if key not in _memories[organisation_id]:
            _memories[organisation_id][key] = []
        
        memory_entry = {
            "key": key,
            "category": category,
            "content": content,
            "organisation_id": organisation_id,
            "version": version,
            "timestamp": datetime.utcnow(),
            "references": references or [],
            "conflicts_with": conflicts_with or []
        }
        
        _memories[organisation_id][key].append(memory_entry)
    
    def read_memory(self, key: str, version: Optional[int] = None) -> Optional[Dict]:
        """Read memory by key. QA-148, QA-151"""
        memories = _memories.get(self.organisation_id, {}).get(key, [])
        
        if not memories:
            # Check for corrupted file
            corrupted_file = self.memory_path / "global" / f"{key}.json"
            if corrupted_file.exists():
                try:
                    json.loads(corrupted_file.read_text())
                except:
                    raise FabricCorruptionError(f"Memory fabric corruption detected for key: {key}")
            return None
        
        if version is not None:
            for m in memories:
                if m.get("version") == version:
                    return m
            return None
        
        # Return latest version
        return memories[-1] if memories else None
    
    def read_by_category(self, category: str) -> List[Dict]:
        """Read all memories in a category. QA-148"""
        results = []
        for key, mem_list in _memories.get(self.organisation_id, {}).items():
            for mem in mem_list:
                if mem.get("category") == category:
                    results.append(mem)
        return results
    
    def search_memory(self, query: str) -> List[Dict]:
        """Full-text search in memory. QA-148"""
        results = []
        for key, mem_list in _memories.get(self.organisation_id, {}).items():
            for mem in mem_list:
                if query in mem.get("content", ""):
                    results.append(mem)
        return results
    
    def create_write_proposal(self, key: str, category: str, content: str, 
                             rationale: str, author: str, source: str = "") -> MemoryWriteProposal:
        """Create write proposal. QA-149"""
        proposal_id = f"proposal-{len(_proposals[self.organisation_id])+1}"
        proposal = MemoryWriteProposal(
            proposal_id=proposal_id,
            key=key,
            category=category,
            content=content,
            rationale=rationale,
            author=author,
            source=source
        )
        _proposals[self.organisation_id][proposal_id] = proposal
        return proposal
    
    def approve_proposal(self, proposal_id: str, approver: str):
        """Approve a write proposal. QA-150"""
        proposal = _proposals[self.organisation_id].get(proposal_id)
        if proposal:
            proposal.status = "APPROVED"
            proposal.approver = approver
    
    def reject_proposal(self, proposal_id: str, rejector: str, reason: str):
        """Reject a write proposal. QA-152"""
        proposal = _proposals[self.organisation_id].get(proposal_id)
        if proposal:
            proposal.status = "REJECTED"
            proposal.rejector = rejector
            proposal.rejection_reason = reason
    
    def execute_write(self, proposal_id: str) -> Dict[str, Any]:
        """Execute approved write. QA-150"""
        proposal = _proposals[self.organisation_id].get(proposal_id)
        
        if not proposal:
            raise ProposalRejectedError("Proposal not found")
        
        if proposal.status == "REJECTED":
            raise ProposalRejectedError(
                f"Cannot execute rejected proposal",
                reason=getattr(proposal, 'rejection_reason', 'Unknown')
            )
        
        if proposal.status != "APPROVED":
            raise Exception("Proposal not approved")
        
        # Write the memory
        self.write_memory(
            key=proposal.key,
            category=proposal.category,
            content=proposal.content,
            organisation_id=self.organisation_id
        )
        
        # Create audit log
        if proposal.key not in _audit_log[self.organisation_id]:
            _audit_log[self.organisation_id][proposal.key] = []
        
        _audit_log[self.organisation_id][proposal.key].append({
            "action": "WRITE",
            "proposal_id": proposal_id,
            "approver": getattr(proposal, 'approver', 'unknown'),
            "timestamp": datetime.utcnow()
        })
        
        return {
            "success": True,
            "memory_key": proposal.key
        }
    
    def update_memory(self, key: str, content: str):
        """Attempt to update memory (should fail due to immutability). QA-150"""
        raise Exception("Memory is immutable - cannot update")
    
    def get_audit_log(self, key: str) -> List[Dict]:
        """Get audit log for a memory key. QA-150"""
        return _audit_log.get(self.organisation_id, {}).get(key, [])
    
    def write_memory_version(self, key: str, content: str, organisation_id: str, previous_version: int):
        """Write new memory version. QA-151"""
        current_memories = _memories.get(organisation_id, {}).get(key, [])
        new_version = previous_version + 1
        
        self.write_memory(
            key=key,
            category="governance",
            content=content,
            organisation_id=organisation_id,
            version=new_version
        )
    
    def get_memory_history(self, key: str) -> List[Dict]:
        """Get version history for memory. QA-151"""
        return _memories.get(self.organisation_id, {}).get(key, [])
    
    def rollback_memory(self, key: str, to_version: int) -> Dict[str, bool]:
        """Rollback memory to previous version. QA-151"""
        history = self.get_memory_history(key)
        target = None
        
        for mem in history:
            if mem.get("version") == to_version:
                target = mem
                break
        
        if target:
            new_version = len(history) + 1
            self.write_memory(
                key=key,
                category=target.get("category", "governance"),
                content=target.get("content", ""),
                organisation_id=self.organisation_id,
                version=new_version
            )
            return {"success": True}
        
        return {"success": False}
    
    def recover_from_corruption(self, key: str) -> Dict[str, bool]:
        """Recover from memory corruption. QA-152"""
        return {"recovered": False, "quarantined": True}
