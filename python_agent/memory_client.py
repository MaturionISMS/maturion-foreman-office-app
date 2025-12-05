#!/usr/bin/env python3
"""
Maturion Foreman - Python Memory Client

This module provides memory fabric integration for Python-based agents.
It enables loading, filtering, and writing memory entries according to
the Unified Memory Fabric schema.

Usage:
    from memory_client import load_memory, write_memory, memory_health_check
    
    # Load memories before reasoning
    memories = load_memory(scopes=["global", "foreman"], tags=["architecture"])
    
    # Write memory after significant events
    write_memory({
        "scope": "foreman",
        "title": "Build Wave Completed",
        "summary": "Successfully completed build wave 1.2",
        "importance": "high",
        "tags": ["build", "governance"]
    })
"""

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any


class MemoryClient:
    """Client for interacting with the Unified Memory Fabric."""
    
    def __init__(self, memory_root: Optional[Path] = None):
        """
        Initialize the memory client.
        
        Args:
            memory_root: Root directory for memory files. Defaults to ./memory
        """
        if memory_root is None:
            # Assume we're running from repo root or find it
            current = Path.cwd()
            # Try to find memory directory
            if (current / "memory").exists():
                self.memory_root = current / "memory"
            elif (current.parent / "memory").exists():
                self.memory_root = current.parent / "memory"
            else:
                # Default to ./memory
                self.memory_root = current / "memory"
        else:
            self.memory_root = Path(memory_root)
        
        self.schema_path = self.memory_root / "schema" / "memory-entry.json"
        self.schema = self._load_schema()
    
    def _load_schema(self) -> Dict[str, Any]:
        """Load the memory entry schema."""
        if not self.schema_path.exists():
            return {}
        
        try:
            with open(self.schema_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load memory schema: {e}")
            return {}
    
    def load_memory(
        self, 
        scopes: List[str], 
        tags: Optional[List[str]] = None,
        importance_min: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Load memory entries matching the specified criteria.
        
        Args:
            scopes: List of scopes to load (e.g., ["global", "foreman"])
            tags: Optional list of tags to filter by
            importance_min: Minimum importance level (low, medium, high, critical)
        
        Returns:
            List of memory entries matching the criteria
        """
        memories = []
        importance_order = {"low": 0, "medium": 1, "high": 2, "critical": 3}
        min_importance_val = importance_order.get(importance_min or "low", 0)
        
        # Load from each scope directory
        for scope in scopes:
            scope_dir = self.memory_root / scope
            if not scope_dir.exists():
                continue
            
            # Load all JSON files in the scope directory
            for json_file in scope_dir.glob("*.json"):
                try:
                    with open(json_file, 'r') as f:
                        data = json.load(f)
                    
                    # Check if this is a collection or single entry
                    if "entries" in data:
                        # This is a collection file
                        entries = data["entries"]
                    elif "id" in data and "scope" in data:
                        # This is a single entry
                        entries = [data]
                    else:
                        # Unknown format, skip
                        continue
                    
                    # Filter entries
                    for entry in entries:
                        # Check scope match
                        if entry.get("scope") not in scopes:
                            continue
                        
                        # Check importance
                        entry_importance = entry.get("importance", "low")
                        if importance_order.get(entry_importance, 0) < min_importance_val:
                            continue
                        
                        # Check tags if specified
                        if tags:
                            entry_tags = entry.get("tags", [])
                            if not any(tag in entry_tags for tag in tags):
                                continue
                        
                        memories.append(entry)
                
                except Exception as e:
                    print(f"Warning: Could not load memory file {json_file}: {e}")
        
        # Sort by importance (critical first) and then by created_at (newest first)
        memories.sort(
            key=lambda m: (
                -importance_order.get(m.get("importance", "low"), 0),
                m.get("created_at", "")
            ),
            reverse=True
        )
        
        return memories
    
    def write_memory(self, entry: Dict[str, Any], scope: Optional[str] = None) -> str:
        """
        Write a new memory entry to the fabric.
        
        Args:
            entry: Memory entry dictionary (can be partial, will be enriched)
            scope: Override scope (uses entry['scope'] if not provided)
        
        Returns:
            The ID of the created memory entry
        """
        # Determine scope
        entry_scope = scope or entry.get("scope")
        if not entry_scope:
            raise ValueError("Scope must be specified either in entry or as parameter")
        
        # Generate ID if not provided
        if "id" not in entry:
            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            unique_id = str(uuid.uuid4())[:8]
            entry["id"] = f"mem-{entry_scope}-{timestamp}-{unique_id}"
        
        # Set created_at if not provided
        if "created_at" not in entry:
            entry["created_at"] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        
        # Set author if not provided
        if "author" not in entry:
            entry["author"] = "builder"
        
        # Ensure scope is set
        entry["scope"] = entry_scope
        
        # Validate required fields
        required = ["id", "scope", "title", "summary", "importance", "tags"]
        missing = [field for field in required if field not in entry]
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")
        
        # Create scope directory if needed
        scope_dir = self.memory_root / entry_scope
        scope_dir.mkdir(parents=True, exist_ok=True)
        
        # Determine filename (use date-based naming)
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        filename = f"events-{date_str}.json"
        file_path = scope_dir / filename
        
        # Load existing entries or create new collection
        if file_path.exists():
            with open(file_path, 'r') as f:
                data = json.load(f)
        else:
            data = {
                "memory_collection": f"{entry_scope.capitalize()} Events - {date_str}",
                "version": "1.0.0",
                "description": f"Memory entries for {entry_scope} scope on {date_str}",
                "entries": []
            }
        
        # Append new entry
        data["entries"].append(entry)
        
        # Write back to file
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        return entry["id"]
    
    def memory_health_check(self) -> Dict[str, Any]:
        """
        Perform a health check on the memory fabric.
        
        Returns:
            Dictionary with health status information
        """
        health = {
            "status": "healthy",
            "memory_root_exists": self.memory_root.exists(),
            "schema_exists": self.schema_path.exists(),
            "scopes": {},
            "total_entries": 0,
            "issues": []
        }
        
        if not self.memory_root.exists():
            health["status"] = "error"
            health["issues"].append("Memory root directory does not exist")
            return health
        
        if not self.schema_path.exists():
            health["status"] = "warning"
            health["issues"].append("Memory schema not found")
        
        # Check each standard scope
        standard_scopes = ["global", "foreman", "platform", "runtime"]
        for scope in standard_scopes:
            scope_dir = self.memory_root / scope
            if scope_dir.exists():
                json_files = list(scope_dir.glob("*.json"))
                entry_count = 0
                
                for json_file in json_files:
                    try:
                        with open(json_file, 'r') as f:
                            data = json.load(f)
                        
                        if "entries" in data:
                            entry_count += len(data["entries"])
                        elif "id" in data:
                            entry_count += 1
                    except Exception as e:
                        health["issues"].append(f"Error reading {json_file}: {e}")
                
                health["scopes"][scope] = {
                    "exists": True,
                    "file_count": len(json_files),
                    "entry_count": entry_count
                }
                health["total_entries"] += entry_count
            else:
                health["scopes"][scope] = {
                    "exists": False,
                    "file_count": 0,
                    "entry_count": 0
                }
        
        if health["total_entries"] == 0:
            health["status"] = "warning"
            health["issues"].append("No memory entries found")
        
        return health
    
    def format_memories_for_prompt(
        self, 
        memories: List[Dict[str, Any]], 
        max_memories: int = 20
    ) -> str:
        """
        Format loaded memories for inclusion in an AI agent prompt.
        
        Args:
            memories: List of memory entries from load_memory()
            max_memories: Maximum number of memories to include
        
        Returns:
            Formatted string ready for prompt injection
        """
        if not memories:
            return "No relevant memories loaded."
        
        # Limit to max_memories
        memories = memories[:max_memories]
        
        output = ["=== MEMORY CONTEXT ===\n"]
        output.append("The following memories are critical context for your reasoning:\n")
        
        for i, memory in enumerate(memories, 1):
            output.append(f"\n--- Memory {i}: {memory.get('title', 'Untitled')} ---")
            output.append(f"Scope: {memory.get('scope', 'unknown')}")
            output.append(f"Importance: {memory.get('importance', 'unknown').upper()}")
            output.append(f"Tags: {', '.join(memory.get('tags', []))}")
            output.append(f"\nSummary: {memory.get('summary', 'No summary')}")
            
            # Include key details if present
            details = memory.get("details", {})
            if details:
                if "rationale" in details:
                    output.append(f"\nRationale: {details['rationale']}")
                if "constraints" in details:
                    output.append(f"\nConstraints:")
                    for constraint in details["constraints"]:
                        output.append(f"  - {constraint}")
            
            output.append("")  # Blank line separator
        
        output.append("=== END MEMORY CONTEXT ===\n")
        return "\n".join(output)


# Module-level convenience functions
_default_client = None

def get_client() -> MemoryClient:
    """Get or create the default memory client instance."""
    global _default_client
    if _default_client is None:
        _default_client = MemoryClient()
    return _default_client


def load_memory(
    scopes: List[str], 
    tags: Optional[List[str]] = None,
    importance_min: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Load memory entries (convenience function).
    
    Args:
        scopes: List of scopes to load
        tags: Optional list of tags to filter by
        importance_min: Minimum importance level
    
    Returns:
        List of memory entries
    """
    return get_client().load_memory(scopes, tags, importance_min)


def write_memory(entry: Dict[str, Any], scope: Optional[str] = None) -> str:
    """
    Write a memory entry (convenience function).
    
    Args:
        entry: Memory entry dictionary
        scope: Optional scope override
    
    Returns:
        Entry ID
    """
    return get_client().write_memory(entry, scope)


def memory_health_check() -> Dict[str, Any]:
    """
    Check memory fabric health (convenience function).
    
    Returns:
        Health status dictionary
    """
    return get_client().memory_health_check()


def format_memories_for_prompt(
    memories: List[Dict[str, Any]], 
    max_memories: int = 20
) -> str:
    """
    Format memories for AI prompt (convenience function).
    
    Args:
        memories: List of memory entries
        max_memories: Maximum to include
    
    Returns:
        Formatted string
    """
    return get_client().format_memories_for_prompt(memories, max_memories)


if __name__ == "__main__":
    # Simple CLI for testing
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python memory_client.py [health|load|test]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "health":
        health = memory_health_check()
        print(json.dumps(health, indent=2))
    
    elif command == "load":
        # Load all critical memories
        memories = load_memory(
            scopes=["global", "foreman"],
            importance_min="critical"
        )
        print(f"Loaded {len(memories)} critical memories")
        print(format_memories_for_prompt(memories, max_memories=5))
    
    elif command == "test":
        # Test write
        test_entry = {
            "scope": "foreman",
            "title": "Memory Client Test",
            "summary": "Testing memory write functionality",
            "importance": "low",
            "tags": ["test", "memory"]
        }
        entry_id = write_memory(test_entry)
        print(f"Created test memory entry: {entry_id}")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
