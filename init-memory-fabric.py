#!/usr/bin/env python3
"""
Maturion Foreman - Repository Memory Initialization Script

This script initializes the Unified Memory Fabric for a new repository.
It creates the required directory structure, copies the schema and seed memories,
and validates the setup.

Usage:
    python3 init-memory-fabric.py [target_repo_path]
    
If no path is provided, initializes in the current directory.
"""

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any


class MemoryFabricInitializer:
    """Initializes the Unified Memory Fabric for a repository."""
    
    def __init__(self, target_path: Path):
        self.target_path = target_path
        self.memory_root = target_path / "memory"
        
        # Find the foreman repo (this repo) to copy from
        self.foreman_repo = Path(__file__).parent
        self.source_memory = self.foreman_repo / "memory"
        
        self.results = []
        self.errors = []
    
    def check_existing_memory(self) -> bool:
        """Check if memory fabric already exists."""
        if self.memory_root.exists():
            print(f"⚠️  Memory fabric already exists at {self.memory_root}")
            print("   Use --force to reinitialize (this will preserve existing entries)")
            return True
        return False
    
    def create_directory_structure(self) -> None:
        """Create the memory directory structure."""
        print("📁 Creating memory directory structure...")
        
        directories = [
            self.memory_root / "schema",
            self.memory_root / "global",
            self.memory_root / "foreman",
            self.memory_root / "platform",
            self.memory_root / "runtime",
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            self.results.append(f"✓ Created {directory.relative_to(self.target_path)}")
    
    def copy_schema(self) -> None:
        """Copy the memory entry schema."""
        print("📋 Copying memory schema...")
        
        source_schema = self.source_memory / "schema" / "memory-entry.json"
        target_schema = self.memory_root / "schema" / "memory-entry.json"
        
        if not source_schema.exists():
            self.errors.append(f"✗ Source schema not found: {source_schema}")
            return
        
        shutil.copy2(source_schema, target_schema)
        self.results.append(f"✓ Copied memory schema")
    
    def copy_seed_memories(self) -> None:
        """Copy seed memory files to global scope."""
        print("🌱 Copying seed memories...")
        
        source_global = self.source_memory / "global"
        target_global = self.memory_root / "global"
        
        if not source_global.exists():
            self.errors.append(f"✗ Source global memories not found: {source_global}")
            return
        
        # Copy seed memory files
        seed_files = [
            "seed-build-philosophy-memory.json",
            "seed-architecture-memory.json",
            "seed-governance-memory.json",
            "seed-autonomy-memory.json",
            "seed-runtime-agent-memory.json"
        ]
        
        for seed_file in seed_files:
            source_file = source_global / seed_file
            target_file = target_global / seed_file
            
            if source_file.exists():
                shutil.copy2(source_file, target_file)
                self.results.append(f"✓ Copied {seed_file}")
            else:
                print(f"⚠️  Seed file not found: {seed_file}")
    
    def create_initialization_memory(self) -> None:
        """Create a memory entry recording this initialization."""
        print("📝 Creating initialization memory entry...")
        
        entry = {
            "id": f"mem-foreman-init-{datetime.now(timezone.utc).strftime('%Y-%m-%d-%H%M%S')}",
            "scope": "foreman",
            "title": "Memory Fabric Initialized",
            "summary": f"Initialized Unified Memory Fabric for repository at {self.target_path.name}",
            "created_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "author": "foreman",
            "importance": "medium",
            "tags": ["initialization", "memory", "governance"],
            "details": {
                "rationale": "Established memory fabric as foundation for governance and learning",
                "repository": str(self.target_path.name),
                "initialized_by": "init-memory-fabric.py"
            }
        }
        
        # Create foreman events file
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        events_file = self.memory_root / "foreman" / f"initialization-{date_str}.json"
        
        collection = {
            "memory_collection": f"Foreman Initialization - {date_str}",
            "version": "1.0.0",
            "description": f"Memory fabric initialization for {self.target_path.name}",
            "entries": [entry]
        }
        
        with open(events_file, 'w') as f:
            json.dump(collection, f, indent=2)
        
        self.results.append(f"✓ Created initialization memory entry")
    
    def validate_structure(self) -> bool:
        """Validate the created memory structure."""
        print("✅ Validating memory fabric...")
        
        validation_passed = True
        
        # Check schema exists
        schema_path = self.memory_root / "schema" / "memory-entry.json"
        if not schema_path.exists():
            self.errors.append("✗ Memory schema missing")
            validation_passed = False
        else:
            self.results.append("✓ Memory schema exists")
        
        # Check scopes exist
        scopes = ["global", "foreman", "platform", "runtime"]
        for scope in scopes:
            scope_dir = self.memory_root / scope
            if not scope_dir.exists():
                self.errors.append(f"✗ Scope directory missing: {scope}")
                validation_passed = False
            else:
                self.results.append(f"✓ Scope directory exists: {scope}")
        
        # Check seed memories exist
        global_dir = self.memory_root / "global"
        json_files = list(global_dir.glob("*.json"))
        if len(json_files) == 0:
            self.errors.append("✗ No seed memories found in global scope")
            validation_passed = False
        else:
            self.results.append(f"✓ Found {len(json_files)} seed memory files")
        
        return validation_passed
    
    def run(self, force: bool = False) -> bool:
        """Run the initialization process."""
        print("🚀 Maturion Memory Fabric Initialization")
        print(f"Target: {self.target_path}")
        print()
        
        # Check if memory already exists
        if self.check_existing_memory() and not force:
            return False
        
        # Create structure
        self.create_directory_structure()
        
        # Copy schema
        self.copy_schema()
        
        # Copy seed memories
        self.copy_seed_memories()
        
        # Create initialization memory
        self.create_initialization_memory()
        
        # Validate
        validation_passed = self.validate_structure()
        
        # Print results
        print()
        print("=" * 60)
        print("Results:")
        print("=" * 60)
        
        for result in self.results:
            print(result)
        
        if self.errors:
            print()
            print("Errors:")
            for error in self.errors:
                print(error)
        
        print()
        if validation_passed:
            print("✅ Memory fabric initialization SUCCESSFUL")
            print()
            print("Next steps:")
            print("1. Review seed memories in memory/global/")
            print("2. Verify memory schema in memory/schema/")
            print("3. Run memory health check: python3 python_agent/memory_client.py health")
            return True
        else:
            print("❌ Memory fabric initialization FAILED")
            print("Please review errors above and retry.")
            return False


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Initialize Unified Memory Fabric for a repository"
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target repository path (default: current directory)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force initialization even if memory fabric exists"
    )
    
    args = parser.parse_args()
    
    target_path = Path(args.target).resolve()
    
    if not target_path.exists():
        print(f"Error: Target path does not exist: {target_path}")
        sys.exit(1)
    
    if not target_path.is_dir():
        print(f"Error: Target path is not a directory: {target_path}")
        sys.exit(1)
    
    initializer = MemoryFabricInitializer(target_path)
    success = initializer.run(force=args.force)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
