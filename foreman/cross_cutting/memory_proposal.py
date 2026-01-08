"""Memory Write Proposal. QA-149"""

from datetime import datetime
from typing import Dict, Any


class MemoryWriteProposal:
    """Represents a memory write proposal."""
    
    def __init__(self, proposal_id: str, key: str, category: str, content: str, 
                 rationale: str, author: str, source: str):
        self.proposal_id = proposal_id
        self.key = key
        self.category = category
        self.content = content
        self.rationale = rationale
        self.author = author
        self.source = source
        self.status = "PENDING"
        self.created_at = datetime.now(UTC)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict. QA-149"""
        return {
            "proposal_id": self.proposal_id,
            "key": self.key,
            "category": self.category,
            "content": self.content,
            "rationale": self.rationale,
            "author": self.author,
            "source": self.source,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }
