"""
Test Governance Memory Sync & Invalidation Contract

Tests for:
- Governance version detection and tracking
- Memory state transitions (UNINITIALIZED → LOADING → LOADED → STALE)
- Change detection via version and checksum
- Atomic reload mechanism
- Cache invalidation tracking
- Soft stop on version mismatch

These tests validate the Governance Memory Sync & Invalidation Contract
as specified in /fm/governance/MEMORY_SYNC_CONTRACT.md

Governance Authority:
- /fm/governance/MEMORY_SYNC_CONTRACT.md
- /memory/schema/governance-version.json
- /foreman/behaviours/memory-rules.md
"""

import pytest
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.mark.governance_sync
class TestGovernanceVersionTracking:
    """Test governance version detection and tracking"""
    
    def test_governance_version_file_exists(self):
        """
        Test that governance version file exists.
        
        Expected: .governance-version.json exists in memory root
        """
        version_file = project_root / 'memory' / '.governance-version.json'
        
        assert version_file.exists(), \
            "Governance version file must exist at memory/.governance-version.json"
    
    def test_governance_version_has_required_fields(self):
        """
        Test that governance version has all required fields.
        
        Expected: version, timestamp, checksum, schema_version, files
        """
        version_file = project_root / 'memory' / '.governance-version.json'
        
        with open(version_file, 'r') as f:
            version_data = json.load(f)
        
        required_fields = ['version', 'timestamp', 'checksum', 'schema_version', 'files']
        
        for field in required_fields:
            assert field in version_data, \
                f"Governance version missing required field: {field}"
    
    def test_governance_version_format_is_valid(self):
        """
        Test that governance version follows semver format.
        
        Expected: Version format is X.Y.Z
        """
        version_file = project_root / 'memory' / '.governance-version.json'
        
        with open(version_file, 'r') as f:
            version_data = json.load(f)
        
        version = version_data['version']
        parts = version.split('.')
        
        assert len(parts) == 3, \
            f"Version must be semver (X.Y.Z), got: {version}"
        
        for part in parts:
            assert part.isdigit(), \
                f"Version parts must be numeric, got: {version}"
    
    def test_governance_version_files_list_not_empty(self):
        """
        Test that governance version tracks memory files.
        
        Expected: Files array is not empty
        """
        version_file = project_root / 'memory' / '.governance-version.json'
        
        with open(version_file, 'r') as f:
            version_data = json.load(f)
        
        files = version_data.get('files', [])
        
        assert len(files) > 0, \
            "Governance version must track at least one memory file"
        
        # Each file entry must have path and checksum
        for file_entry in files:
            assert 'path' in file_entry, \
                "File entry must have path"
            assert 'checksum' in file_entry, \
                "File entry must have checksum"
    
    def test_governance_version_schema_exists(self):
        """
        Test that governance version schema file exists.
        
        Expected: governance-version.json schema exists
        """
        schema_file = project_root / 'memory' / 'schema' / 'governance-version.json'
        
        assert schema_file.exists(), \
            "Governance version schema must exist at memory/schema/governance-version.json"
        
        # Schema must be valid JSON
        with open(schema_file, 'r') as f:
            schema = json.load(f)
        
        assert 'schema' in schema, \
            "Schema file must define schema structure"


@pytest.mark.governance_sync
class TestMemoryStateTransitions:
    """Test memory state machine transitions"""
    
    def test_memory_state_types_defined(self):
        """
        Test that memory states are properly defined.
        
        Expected: UNINITIALIZED, LOADING, LOADED, STALE, INVALID
        """
        # This test validates that the contract defines these states
        contract_file = project_root / 'fm' / 'governance' / 'MEMORY_SYNC_CONTRACT.md'
        
        assert contract_file.exists(), \
            "Memory sync contract must exist"
        
        with open(contract_file, 'r') as f:
            content = f.read()
        
        required_states = ['UNINITIALIZED', 'LOADING', 'LOADED', 'STALE', 'INVALID']
        
        for state in required_states:
            assert state in content, \
                f"Contract must define state: {state}"
    
    def test_state_transition_rules_documented(self):
        """
        Test that state transitions are documented in contract.
        
        Expected: State machine diagram present
        """
        contract_file = project_root / 'fm' / 'governance' / 'MEMORY_SYNC_CONTRACT.md'
        
        with open(contract_file, 'r') as f:
            content = f.read()
        
        # Check for state transition documentation
        assert 'STATE MACHINE' in content or 'TRANSITIONS' in content, \
            "Contract must document state transitions"
        
        # Key transitions that must be documented
        transitions = [
            'UNINITIALIZED',
            'LOADING',
            'LOADED',
            'STALE'
        ]
        
        for transition in transitions:
            assert transition in content, \
                f"Contract must document {transition} state"


@pytest.mark.governance_sync
class TestChangeDetection:
    """Test governance memory change detection"""
    
    def test_version_comparison_logic_exists(self):
        """
        Test that version comparison is part of contract.
        
        Expected: Contract specifies version comparison
        """
        contract_file = project_root / 'fm' / 'governance' / 'MEMORY_SYNC_CONTRACT.md'
        
        with open(contract_file, 'r') as f:
            content = f.read()
        
        # Must have version comparison logic
        assert 'version' in content.lower(), \
            "Contract must mention version comparison"
        assert 'checksum' in content.lower(), \
            "Contract must mention checksum validation"
    
    def test_checksum_validation_defined(self):
        """
        Test that checksum validation is defined.
        
        Expected: Contract specifies SHA-256 checksum
        """
        contract_file = project_root / 'fm' / 'governance' / 'MEMORY_SYNC_CONTRACT.md'
        
        with open(contract_file, 'r') as f:
            content = f.read()
        
        # Must specify checksum algorithm
        assert 'SHA-256' in content or 'sha256' in content.lower(), \
            "Contract must specify SHA-256 checksum algorithm"
    
    def test_stale_detection_triggers_defined(self):
        """
        Test that stale detection triggers are documented.
        
        Expected: Version mismatch and checksum mismatch documented
        """
        contract_file = project_root / 'fm' / 'governance' / 'MEMORY_SYNC_CONTRACT.md'
        
        with open(contract_file, 'r') as f:
            content = f.read()
        
        # Must document when memory becomes stale
        assert 'version mismatch' in content.lower() or 'version_mismatch' in content, \
            "Contract must document version mismatch trigger"
        assert 'checksum mismatch' in content.lower() or 'checksum_mismatch' in content, \
            "Contract must document checksum mismatch trigger"


@pytest.mark.governance_sync
class TestAtomicReload:
    """Test atomic memory reload mechanism"""
    
    def test_atomic_reload_requirement_documented(self):
        """
        Test that atomic reload is a requirement.
        
        Expected: Contract requires all-or-nothing reload
        """
        contract_file = project_root / 'fm' / 'governance' / 'MEMORY_SYNC_CONTRACT.md'
        
        with open(contract_file, 'r') as f:
            content = f.read()
        
        # Must require atomic reload
        assert 'atomic' in content.lower(), \
            "Contract must require atomic reload"
        assert 'all or nothing' in content.lower() or 'all-or-nothing' in content.lower(), \
            "Contract must specify all-or-nothing reload behavior"
    
    def test_partial_load_prohibition_documented(self):
        """
        Test that partial loads are explicitly forbidden.
        
        Expected: Contract prohibits partial loads
        """
        contract_file = project_root / 'fm' / 'governance' / 'MEMORY_SYNC_CONTRACT.md'
        
        with open(contract_file, 'r') as f:
            content = f.read()
        
        # Must prohibit partial loads
        assert 'partial' in content.lower(), \
            "Contract must address partial loads"
        assert 'forbidden' in content.lower() or 'prohibited' in content.lower(), \
            "Contract must forbid partial loads"
    
    def test_reload_logging_required(self):
        """
        Test that reload events must be logged.
        
        Expected: Contract requires reload logging
        """
        contract_file = project_root / 'fm' / 'governance' / 'MEMORY_SYNC_CONTRACT.md'
        
        with open(contract_file, 'r') as f:
            content = f.read()
        
        # Must require logging
        assert 'log' in content.lower(), \
            "Contract must require reload logging"


@pytest.mark.governance_sync
class TestInvalidationTracking:
    """Test cache invalidation tracking"""
    
    def test_invalidation_event_structure_defined(self):
        """
        Test that invalidation event structure is defined.
        
        Expected: InvalidationEvent interface documented
        """
        contract_file = project_root / 'fm' / 'governance' / 'MEMORY_SYNC_CONTRACT.md'
        
        with open(contract_file, 'r') as f:
            content = f.read()
        
        # Must define InvalidationEvent
        assert 'InvalidationEvent' in content, \
            "Contract must define InvalidationEvent structure"
        
        # Must have required fields
        required_fields = ['timestamp', 'old_version', 'new_version', 'reason']
        for field in required_fields:
            assert field in content, \
                f"InvalidationEvent must have field: {field}"
    
    def test_invalidation_reasons_defined(self):
        """
        Test that invalidation reasons are enumerated.
        
        Expected: version_mismatch, checksum_mismatch, manual, initialization
        """
        contract_file = project_root / 'fm' / 'governance' / 'MEMORY_SYNC_CONTRACT.md'
        
        with open(contract_file, 'r') as f:
            content = f.read()
        
        reasons = ['version_mismatch', 'checksum_mismatch', 'manual', 'initialization']
        
        for reason in reasons:
            assert reason in content, \
                f"Contract must define invalidation reason: {reason}"
    
    def test_invalidation_auditability_required(self):
        """
        Test that invalidation must be auditable.
        
        Expected: Contract requires audit trail
        """
        contract_file = project_root / 'fm' / 'governance' / 'MEMORY_SYNC_CONTRACT.md'
        
        with open(contract_file, 'r') as f:
            content = f.read()
        
        assert 'audit' in content.lower(), \
            "Contract must require auditable invalidation"


@pytest.mark.governance_sync
class TestSoftStopBehavior:
    """Test soft stop on version mismatch"""
    
    def test_soft_stop_on_version_mismatch_documented(self):
        """
        Test that soft stop behavior is documented.
        
        Expected: Contract specifies soft stop on mismatch
        """
        contract_file = project_root / 'fm' / 'governance' / 'MEMORY_SYNC_CONTRACT.md'
        
        with open(contract_file, 'r') as f:
            content = f.read()
        
        assert 'soft stop' in content.lower() or 'SOFT STOP' in content, \
            "Contract must document soft stop behavior"
    
    def test_version_mismatch_state_transition_defined(self):
        """
        Test that version mismatch causes STALE state.
        
        Expected: LOADED → STALE on version mismatch
        """
        contract_file = project_root / 'fm' / 'governance' / 'MEMORY_SYNC_CONTRACT.md'
        
        with open(contract_file, 'r') as f:
            content = f.read()
        
        # Must document transition to STALE
        assert 'STALE' in content, \
            "Contract must define STALE state for version mismatch"


@pytest.mark.governance_sync
class TestAPIExtensions:
    """Test new API methods for sync functionality"""
    
    def test_api_extensions_documented(self):
        """
        Test that new API methods are documented in contract.
        
        Expected: getGovernanceVersion, isMemoryStale, reloadIfStale, etc.
        """
        contract_file = project_root / 'fm' / 'governance' / 'MEMORY_SYNC_CONTRACT.md'
        
        with open(contract_file, 'r') as f:
            content = f.read()
        
        api_methods = [
            'getGovernanceVersion',
            'isMemoryStale',
            'reloadIfStale',
            'forceReload',
            'getMemoryState',
            'getLastInvalidation'
        ]
        
        for method in api_methods:
            assert method in content, \
                f"Contract must document API method: {method}"
    
    def test_state_getter_documented(self):
        """
        Test that state getter for UI is documented.
        
        Expected: getMemoryState() returns current state
        """
        contract_file = project_root / 'fm' / 'governance' / 'MEMORY_SYNC_CONTRACT.md'
        
        with open(contract_file, 'r') as f:
            content = f.read()
        
        assert 'getMemoryState' in content, \
            "Contract must document getMemoryState() for UI integration"


@pytest.mark.governance_sync
class TestIntegrationPatterns:
    """Test integration pattern documentation"""
    
    def test_startup_pattern_documented(self):
        """
        Test that startup initialization pattern is documented.
        
        Expected: Pattern for app startup memory check
        """
        contract_file = project_root / 'fm' / 'governance' / 'MEMORY_SYNC_CONTRACT.md'
        
        with open(contract_file, 'r') as f:
            content = f.read()
        
        assert 'startup' in content.lower() or 'initialization' in content.lower(), \
            "Contract must document startup pattern"
    
    def test_periodic_sync_check_pattern_documented(self):
        """
        Test that periodic sync check pattern is documented.
        
        Expected: Background task to check for stale memory
        """
        contract_file = project_root / 'fm' / 'governance' / 'MEMORY_SYNC_CONTRACT.md'
        
        with open(contract_file, 'r') as f:
            content = f.read()
        
        assert 'periodic' in content.lower() or 'background' in content.lower(), \
            "Contract must document periodic sync check pattern"
    
    def test_ui_state_display_pattern_documented(self):
        """
        Test that UI state display pattern is documented.
        
        Expected: How UI displays memory state
        """
        contract_file = project_root / 'fm' / 'governance' / 'MEMORY_SYNC_CONTRACT.md'
        
        with open(contract_file, 'r') as f:
            content = f.read()
        
        assert 'UI' in content or 'display' in content.lower(), \
            "Contract must document UI integration pattern"


@pytest.mark.governance_sync
class TestAcceptanceCriteria:
    """Test that all acceptance criteria are addressed"""
    
    def test_ac1_change_detection_addressed(self):
        """
        AC1: FM App detects governance memory changes
        
        Expected: Contract addresses change detection
        """
        contract_file = project_root / 'fm' / 'governance' / 'MEMORY_SYNC_CONTRACT.md'
        
        with open(contract_file, 'r') as f:
            content = f.read()
        
        assert 'detect' in content.lower() and 'change' in content.lower(), \
            "AC1: Contract must address change detection"
    
    def test_ac2_reload_without_restart_addressed(self):
        """
        AC2: Memory reloads without restart
        
        Expected: Contract addresses runtime reload
        """
        contract_file = project_root / 'fm' / 'governance' / 'MEMORY_SYNC_CONTRACT.md'
        
        with open(contract_file, 'r') as f:
            content = f.read()
        
        assert 'reload' in content.lower(), \
            "AC2: Contract must address memory reload"
        assert 'restart' in content.lower() or 'without restart' in content.lower(), \
            "AC2: Contract must address reload without restart"
    
    def test_ac3_invalidation_explicit_and_auditable(self):
        """
        AC3: Invalidation is explicit and auditable
        
        Expected: Contract requires audit trail
        """
        contract_file = project_root / 'fm' / 'governance' / 'MEMORY_SYNC_CONTRACT.md'
        
        with open(contract_file, 'r') as f:
            content = f.read()
        
        assert 'explicit' in content.lower() and 'invalidation' in content.lower(), \
            "AC3: Contract must require explicit invalidation"
        assert 'audit' in content.lower(), \
            "AC3: Contract must require auditable invalidation"
    
    def test_ac4_ui_shows_memory_state(self):
        """
        AC4: UI shows memory state (LOADED/STALE/INVALID)
        
        Expected: Contract addresses UI state display
        """
        contract_file = project_root / 'fm' / 'governance' / 'MEMORY_SYNC_CONTRACT.md'
        
        with open(contract_file, 'r') as f:
            content = f.read()
        
        states = ['LOADED', 'STALE', 'INVALID']
        for state in states:
            assert state in content, \
                f"AC4: Contract must define state: {state}"
        
        assert 'UI' in content, \
            "AC4: Contract must address UI integration"


@pytest.mark.governance_sync
class TestComplianceAndScope:
    """Test compliance and scope boundaries"""
    
    def test_read_only_enforcement_maintained(self):
        """
        Test that read-only enforcement is maintained.
        
        Expected: No write operations introduced
        """
        contract_file = project_root / 'fm' / 'governance' / 'MEMORY_SYNC_CONTRACT.md'
        
        with open(contract_file, 'r') as f:
            content = f.read()
        
        # Must maintain read-only
        assert 'read-only' in content.lower() or 'READ-ONLY' in content, \
            "Contract must maintain read-only enforcement"
    
    def test_out_of_scope_clearly_defined(self):
        """
        Test that out-of-scope items are clearly defined.
        
        Expected: Writing memory, auto-learning, tenant memory excluded
        """
        contract_file = project_root / 'fm' / 'governance' / 'MEMORY_SYNC_CONTRACT.md'
        
        with open(contract_file, 'r') as f:
            content = f.read()
        
        out_of_scope_items = [
            'Writing',
            'auto-learning',
            'tenant',
            'CI/CD'
        ]
        
        # Check OUT OF SCOPE section exists
        assert 'OUT OF SCOPE' in content or 'OUT-OF-SCOPE' in content, \
            "Contract must have OUT OF SCOPE section"
        
        # At least some out-of-scope items must be listed
        found_items = sum(1 for item in out_of_scope_items if item in content)
        assert found_items >= 2, \
            "Contract must explicitly list out-of-scope items"


# Mark all tests in this module with governance_sync marker
pytestmark = pytest.mark.governance_sync
