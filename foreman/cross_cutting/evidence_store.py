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
    
    def store_artifact(self, artifact_type: str = None, content: Any = None, 
                      metadata: Dict = None, organisation_id: str = None,
                      artifact_id: str = None, category: str = "general") -> Dict[str, Any]:
        """Store evidence artifact. QA-180"""
        # Generate artifact_id if not provided
        if artifact_id is None:
            artifact_id = f"artifact-{len(_evidence_artifacts[self.organisation_id])+1}"
        
        artifact = {
            "artifact_id": artifact_id,
            "content": content,
            "artifact_type": artifact_type or category,
            "metadata": metadata or {},
            "category": category,
            "created_at": datetime.utcnow(),
            "timestamp": datetime.utcnow().isoformat(),
            "immutable": True
        }
        
        _evidence_artifacts[self.organisation_id][artifact_id] = artifact
        
        return artifact
    
    def retrieve_artifact(self, artifact_id: str) -> Optional[Dict]:
        """Retrieve evidence by ID. QA-166"""
        return _evidence_artifacts.get(self.organisation_id, {}).get(artifact_id)
    
    def modify_artifact(self, artifact_id: str, **kwargs):
        """Attempt to modify artifact (should fail due to immutability). QA-180"""
        raise Exception("Evidence artifacts are immutable - cannot modify")
    
    def query_by_category(self, category: str) -> list:
        """Query evidence by category. QA-167"""
        artifacts = _evidence_artifacts.get(self.organisation_id, {})
        return [a for a in artifacts.values() if a.get("category") == category]
