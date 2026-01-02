"""Memory Schema Validator. QA-147"""

from pathlib import Path


class MemorySchemaValidator:
    """Validates memory fabric structure."""
    
    def validate_fabric_structure(self, fabric_path: Path) -> bool:
        """Validate fabric structure. QA-147"""
        required_dirs = ["global", "scoped", "proposals", "archive"]
        return all((fabric_path / d).exists() for d in required_dirs)
