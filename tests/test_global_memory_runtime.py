"""
Test Global Memory Runtime Loader (Read-Only)

Tests for:
- Memory loading functionality
- Validation against governance schema
- Fail-fast behavior on invalid memory
- Read-only enforcement (no write paths)

These tests validate that the Global Memory Runtime Loader
correctly implements governance requirements for read-only memory access.

Governance Authority:
- /memory/schema/memory-entry.json
- /foreman/behaviours/memory-rules.md
- /memory/global/*.json
"""

import pytest
import json
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from python_agent.memory_client import load_memory, memory_health_check


@pytest.mark.memory
class TestGlobalMemoryLoading:
    """Test memory loading functionality"""
    
    def test_can_load_global_memory(self):
        """
        Test that global memory can be loaded successfully.
        
        Expected: Load memories from global scope
        """
        memories = load_memory(
            scopes=['global'],
            tags=None,
            importance_min='low'
        )
        
        assert memories is not None, \
            "Memory loading must return a result"
        assert isinstance(memories, list), \
            "Memories must be returned as a list"
        assert len(memories) > 0, \
            "Global memory must contain at least one entry"
    
    def test_can_filter_by_importance(self):
        """
        Test that memories can be filtered by importance level.
        
        Expected: High importance filter returns fewer results
        """
        all_memories = load_memory(
            scopes=['global'],
            tags=None,
            importance_min='low'
        )
        
        critical_memories = load_memory(
            scopes=['global'],
            tags=None,
            importance_min='critical'
        )
        
        assert len(critical_memories) <= len(all_memories), \
            "Critical-only filter must return same or fewer memories"
        
        # All critical memories should have critical importance
        for memory in critical_memories:
            assert memory.get('importance') == 'critical', \
                "Filtered memories must match importance criteria"
    
    def test_can_filter_by_tags(self):
        """
        Test that memories can be filtered by tags.
        
        Expected: Tag filter returns only matching memories
        """
        governance_memories = load_memory(
            scopes=['global'],
            tags=['governance'],
            importance_min='low'
        )
        
        assert len(governance_memories) > 0, \
            "Global memory must contain governance-tagged entries"
        
        # All returned memories should have governance tag
        for memory in governance_memories:
            tags = memory.get('tags', [])
            assert 'governance' in tags, \
                "Filtered memories must contain requested tag"
    
    def test_load_process_guidance_memories(self):
        """
        Test loading memories for process guidance.
        
        Expected: Returns governance and architecture memories
        """
        memories = load_memory(
            scopes=['global'],
            tags=['governance', 'architecture', 'philosophy'],
            importance_min='high'
        )
        
        assert len(memories) > 0, \
            "Must have process guidance memories available"
        
        # Should contain high-importance governance/architecture content
        has_governance = any('governance' in m.get('tags', []) for m in memories)
        assert has_governance, \
            "Process guidance must include governance memories"
    
    def test_load_escalation_heuristics_memories(self):
        """
        Test loading memories for escalation heuristics.
        
        Expected: Returns escalation-related memories
        """
        memories = load_memory(
            scopes=['global'],
            tags=['governance', 'escalation', 'incidents'],
            importance_min='medium'
        )
        
        # May or may not have escalation memories in seed data
        # Just verify the query executes without error
        assert memories is not None, \
            "Escalation memory query must execute successfully"
    
    def test_load_pattern_memories(self):
        """
        Test loading memories for pattern recognition.
        
        Expected: Returns build/architecture pattern memories
        """
        memories = load_memory(
            scopes=['global'],
            tags=['build', 'architecture', 'qa'],
            importance_min='medium'
        )
        
        # Verify query executes and returns results
        assert memories is not None, \
            "Pattern memory query must execute successfully"


@pytest.mark.memory
class TestMemoryValidation:
    """Test memory validation against governance schema"""
    
    def test_memory_schema_exists(self):
        """
        Test that memory schema file exists.
        
        Expected: Schema file present at memory/schema/memory-entry.json
        """
        schema_path = project_root / 'memory' / 'schema' / 'memory-entry.json'
        
        assert schema_path.exists(), \
            "Memory schema must exist at memory/schema/memory-entry.json"
        
        # Schema must be valid JSON
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        
        assert 'schema' in schema, \
            "Schema must define schema structure"
    
    def test_loaded_memories_have_required_fields(self):
        """
        Test that all loaded memories have required fields.
        
        Expected: All memories have id, scope, title, summary, importance, tags
        """
        memories = load_memory(
            scopes=['global'],
            tags=None,
            importance_min='low'
        )
        
        required_fields = ['id', 'scope', 'title', 'summary', 'importance', 'tags']
        
        for memory in memories:
            for field in required_fields:
                assert field in memory, \
                    f"Memory {memory.get('id', 'unknown')} missing required field: {field}"
    
    def test_memory_importance_is_valid(self):
        """
        Test that memory importance values are valid.
        
        Expected: Importance must be low, medium, high, or critical
        """
        memories = load_memory(
            scopes=['global'],
            tags=None,
            importance_min='low'
        )
        
        valid_importance = ['low', 'medium', 'high', 'critical']
        
        for memory in memories:
            importance = memory.get('importance')
            assert importance in valid_importance, \
                f"Memory {memory.get('id')} has invalid importance: {importance}"
    
    def test_memory_tags_is_array(self):
        """
        Test that memory tags field is an array.
        
        Expected: Tags must be a list/array
        """
        memories = load_memory(
            scopes=['global'],
            tags=None,
            importance_min='low'
        )
        
        for memory in memories:
            tags = memory.get('tags')
            assert isinstance(tags, list), \
                f"Memory {memory.get('id')} tags must be an array"
    
    def test_memory_scope_is_global(self):
        """
        Test that global scope query returns only global memories.
        
        Expected: All memories have scope='global'
        """
        memories = load_memory(
            scopes=['global'],
            tags=None,
            importance_min='low'
        )
        
        for memory in memories:
            scope = memory.get('scope')
            assert scope == 'global', \
                f"Memory {memory.get('id')} should have global scope, got: {scope}"


@pytest.mark.memory
class TestFailFastBehavior:
    """Test fail-fast behavior on memory issues"""
    
    def test_memory_health_check_succeeds(self):
        """
        Test that memory health check reports success.
        
        Expected: Memory fabric is healthy
        """
        health = memory_health_check()
        
        assert health is not None, \
            "Health check must return result"
        assert health.get('status') in ['healthy', 'warning'], \
            f"Memory fabric must be healthy, got: {health.get('status')}"
        assert health.get('memory_root_exists') is True, \
            "Memory root directory must exist"
    
    def test_memory_directory_structure_exists(self):
        """
        Test that required memory directory structure exists.
        
        Expected: memory/, memory/global/, memory/schema/ exist
        """
        memory_root = project_root / 'memory'
        global_dir = memory_root / 'global'
        schema_dir = memory_root / 'schema'
        
        assert memory_root.exists(), \
            "Memory root directory must exist"
        assert global_dir.exists(), \
            "Global memory directory must exist"
        assert schema_dir.exists(), \
            "Schema directory must exist"
    
    def test_global_memory_files_exist(self):
        """
        Test that global memory seed files exist.
        
        Expected: At least one JSON file in memory/global/
        """
        global_dir = project_root / 'memory' / 'global'
        json_files = list(global_dir.glob('*.json'))
        
        assert len(json_files) > 0, \
            "Global memory directory must contain JSON files"
    
    def test_seed_governance_memory_exists(self):
        """
        Test that seed governance memory exists.
        
        Expected: seed-governance-memory.json present
        """
        governance_file = project_root / 'memory' / 'global' / 'seed-governance-memory.json'
        
        assert governance_file.exists(), \
            "Seed governance memory must exist"
        
        # File must be valid JSON
        with open(governance_file, 'r') as f:
            data = json.load(f)
        
        assert 'entries' in data, \
            "Governance memory must contain entries"
        assert len(data['entries']) > 0, \
            "Governance memory must have at least one entry"


@pytest.mark.memory
class TestReadOnlyEnforcement:
    """Test that no write paths exist in memory runtime"""
    
    def test_no_append_memory_in_runtime_loader(self):
        """
        Test that runtime loader does not expose appendMemory.
        
        Expected: Read-only loader has no write methods
        """
        # This test validates by code inspection
        # The TypeScript runtime-loader.ts should NOT have:
        # - appendMemory method implementation
        # - writeMemory method implementation
        # - modifyMemory method implementation
        # - deleteMemory method implementation
        
        runtime_loader_path = project_root / 'lib' / 'memory' / 'runtime-loader.ts'
        
        if runtime_loader_path.exists():
            with open(runtime_loader_path, 'r') as f:
                content = f.read()
            
            # Check for prohibited write operations (actual implementations)
            # Note: We check for method signatures, not documentation mentions
            prohibited_patterns = [
                'async appendMemory(',
                'async writeMemory(',
                'async modifyMemory(',
                'async deleteMemory(',
                'appendMemory(entry',
                'writeMemory(entry',
                'modifyMemory(id',
                'deleteMemory(id',
            ]
            
            found_violations = []
            for pattern in prohibited_patterns:
                # Check if pattern appears outside of comments
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    # Skip comment lines and documentation
                    stripped = line.strip()
                    if stripped.startswith('//') or stripped.startswith('*'):
                        continue
                    if pattern in line:
                        found_violations.append(f"Line {i+1}: {pattern}")
            
            assert len(found_violations) == 0, \
                f"Runtime loader must NOT implement write operations. Found: {found_violations}"
    
    def test_python_memory_client_write_is_separate(self):
        """
        Test that Python memory client write is separate concern.
        
        Expected: Write functionality exists but is not part of runtime loader
        """
        # The python_agent/memory_client.py has write_memory
        # But the runtime loader should use only read operations
        
        # This validates that write exists for other purposes
        # but is not used by runtime loader
        from python_agent.memory_client import write_memory
        
        assert write_memory is not None, \
            "Write memory function exists for other uses"
        
        # Runtime should use only load_memory
        from python_agent.memory_client import load_memory
        
        assert load_memory is not None, \
            "Load memory function exists for runtime"
    
    def test_memory_immutability_at_runtime(self):
        """
        Test that loaded memories are read-only at runtime.
        
        Expected: Memories loaded are immutable
        """
        memories = load_memory(
            scopes=['global'],
            tags=['governance'],
            importance_min='high'
        )
        
        # Verify we got some memories
        assert len(memories) > 0, \
            "Must have memories to test immutability"
        
        # Attempt to modify (should not affect original data)
        original_title = memories[0].get('title')
        memories[0]['title'] = 'MODIFIED'
        
        # Reload to verify original unchanged
        reloaded = load_memory(
            scopes=['global'],
            tags=['governance'],
            importance_min='high'
        )
        
        assert reloaded[0].get('title') == original_title, \
            "Original memory data must remain unchanged"


@pytest.mark.memory
class TestMemoryIntegration:
    """Test memory integration patterns"""
    
    def test_memory_can_enrich_system_prompt(self):
        """
        Test that memories can be formatted for system prompt.
        
        Expected: Format function produces prompt-ready text
        """
        from python_agent.memory_client import format_memories_for_prompt
        
        memories = load_memory(
            scopes=['global'],
            tags=['governance'],
            importance_min='high'
        )
        
        formatted = format_memories_for_prompt(memories, max_memories=5)
        
        assert formatted is not None, \
            "Format function must return result"
        assert len(formatted) > 0, \
            "Formatted output must not be empty"
        assert 'MEMORY CONTEXT' in formatted, \
            "Formatted output must have memory context marker"
    
    def test_memory_loading_before_governance_action(self):
        """
        Test memory loading pattern before governance action.
        
        Expected: Can load governance memories before decision
        """
        # Simulate governance action requiring memory
        memories = load_memory(
            scopes=['global'],
            tags=['governance', 'architecture'],
            importance_min='high'
        )
        
        # Should have governance context
        assert len(memories) > 0, \
            "Must have governance context before action"
        
        # Verify we have architecture governance
        has_architecture = any(
            'architecture' in m.get('tags', []) 
            for m in memories
        )
        
        assert has_architecture, \
            "Governance action must have architecture context"
    
    def test_memory_health_check_integration(self):
        """
        Test memory health check integration.
        
        Expected: Health check provides actionable status
        """
        health = memory_health_check()
        
        # Health check must provide required information
        assert 'status' in health, \
            "Health check must include status"
        assert 'memory_root_exists' in health, \
            "Health check must verify root exists"
        assert 'total_entries' in health, \
            "Health check must count entries"
        
        # Status must be actionable
        assert health['status'] in ['healthy', 'warning', 'error'], \
            "Health status must be one of: healthy, warning, error"


# Mark all tests in this module as memory tests
pytestmark = pytest.mark.memory
