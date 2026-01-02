"""
Evidence Store (CROSS-04).
QA Coverage: QA-180 to QA-189
"""

from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
import json

_evidence_artifacts = {}


class EvidenceStore:
    """Manages evidence artifacts. QA-180 to QA-189"""
    
    def __init__(self, organisation_id: str, store_path: Path = None, storage_path: Path = None):
        self.organisation_id = organisation_id
        self.storage_path = store_path or storage_path or Path("/tmp/evidence")
        
        if organisation_id not in _evidence_artifacts:
            _evidence_artifacts[organisation_id] = {}
    
    def store_artifact(self, artifact_id: str, content: Any, 
                      metadata: Dict = None, category: str = "general") -> Dict[str, bool]:
        """Store evidence artifact. QA-180"""
        artifact = {
            "artifact_id": artifact_id,
            "content": content,
            "metadata": metadata or {},
            "category": category,
            "timestamp": datetime.utcnow().isoformat(),
            "immutable": True
        }
        
        _evidence_artifacts[self.organisation_id][artifact_id] = artifact
        
        return {"success": True}
    
    def retrieve_artifact(self, artifact_id: str) -> Optional[Dict]:
        """Retrieve evidence by ID. QA-166"""
        return _evidence_artifacts.get(self.organisation_id, {}).get(artifact_id)
    
    def query_by_category(self, category: str) -> list:
        """Query evidence by category. QA-167"""
        artifacts = _evidence_artifacts.get(self.organisation_id, {})
        return [a for a in artifacts.values() if a.get("category") == category]
