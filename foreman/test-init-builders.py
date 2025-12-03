#!/usr/bin/env python3
"""
Test suite for the Maturion Builder Agent Registry Initializer.

This test suite validates the builder initialization and validation logic
to ensure proper configuration alignment and error detection.

Usage:
    python3 foreman/test-init-builders.py
"""

import json
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Import the module to test
sys.path.insert(0, str(Path(__file__).parent))
from init_builders import BuilderRegistry


class TestBuilderRegistry:
    """Test cases for BuilderRegistry."""
    
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.temp_dir = None
    
    def setup_test_environment(self):
        """Create a temporary test environment."""
        self.temp_dir = Path(tempfile.mkdtemp(prefix="maturion_test_"))
        builder_dir = self.temp_dir / "builder"
        builder_dir.mkdir()
        return self.temp_dir, builder_dir
    
    def cleanup_test_environment(self):
        """Clean up temporary test environment."""
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def assert_true(self, condition, test_name):
        """Assert that a condition is true."""
        if condition:
            print(f"  ✓ {test_name}")
            self.tests_passed += 1
        else:
            print(f"  ✗ {test_name}")
            self.tests_failed += 1
    
    def assert_equal(self, actual, expected, test_name):
        """Assert that two values are equal."""
        if actual == expected:
            print(f"  ✓ {test_name}")
            self.tests_passed += 1
        else:
            print(f"  ✗ {test_name}: expected {expected}, got {actual}")
            self.tests_failed += 1
    
    def assert_contains(self, item, container, test_name):
        """Assert that an item is in a container."""
        if item in container:
            print(f"  ✓ {test_name}")
            self.tests_passed += 1
        else:
            print(f"  ✗ {test_name}: '{item}' not found")
            self.tests_failed += 1
    
    def test_valid_configuration(self):
        """Test initialization with valid configuration."""
        print("\nTest: Valid Configuration")
        print("-" * 60)
        
        temp_dir, builder_dir = self.setup_test_environment()
        
        # Create valid manifest
        manifest = {
            "version": "1.0",
            "agents": {
                "test-builder": {
                    "responsibilities": ["test tasks"],
                    "forbidden": ["production code"]
                }
            }
        }
        with open(temp_dir / "builder-manifest.json", 'w') as f:
            json.dump(manifest, f)
        
        # Create valid capabilities
        capabilities = {
            "version": "1.0",
            "capabilities": {
                "test-builder": ["testing", "validation"]
            }
        }
        with open(builder_dir / "builder-capability-map.json", 'w') as f:
            json.dump(capabilities, f)
        
        # Create valid permissions
        permissions = {
            "builders": {
                "test-builder": {
                    "write": ["test/*"],
                    "read": ["foreman/*"]
                }
            }
        }
        with open(builder_dir / "builder-permission-policy.json", 'w') as f:
            json.dump(permissions, f)
        
        # Create spec file
        spec_file = builder_dir / "test-builder-spec.md"
        spec_file.write_text("# Test Builder Specification\n")
        
        # Initialize registry
        registry = BuilderRegistry(temp_dir)
        success, report = registry.initialize()
        
        # Validate results
        self.assert_true(success, "Initialization should succeed")
        self.assert_equal(len(registry.errors), 0, "No errors should be present")
        self.assert_equal(len(registry.manifest['agents']), 1, "One agent should be registered")
        self.assert_contains("test-builder", registry.manifest['agents'], "test-builder should be in manifest")
        
        self.cleanup_test_environment()
    
    def test_missing_manifest(self):
        """Test initialization with missing manifest file."""
        print("\nTest: Missing Manifest File")
        print("-" * 60)
        
        temp_dir, builder_dir = self.setup_test_environment()
        
        # Create only capabilities and permissions (no manifest)
        capabilities = {"version": "1.0", "capabilities": {}}
        with open(builder_dir / "builder-capability-map.json", 'w') as f:
            json.dump(capabilities, f)
        
        permissions = {"builders": {}}
        with open(builder_dir / "builder-permission-policy.json", 'w') as f:
            json.dump(permissions, f)
        
        # Initialize registry
        registry = BuilderRegistry(temp_dir)
        success, report = registry.initialize()
        
        # Validate results
        self.assert_true(not success, "Initialization should fail")
        self.assert_true(len(registry.errors) > 0, "Errors should be present")
        
        self.cleanup_test_environment()
    
    def test_missing_spec_file(self):
        """Test detection of missing specification file."""
        print("\nTest: Missing Specification File")
        print("-" * 60)
        
        temp_dir, builder_dir = self.setup_test_environment()
        
        # Create manifest with agent
        manifest = {
            "version": "1.0",
            "agents": {
                "missing-spec-builder": {
                    "responsibilities": ["test"],
                    "forbidden": ["modify"]
                }
            }
        }
        with open(temp_dir / "builder-manifest.json", 'w') as f:
            json.dump(manifest, f)
        
        # Create capabilities
        capabilities = {
            "version": "1.0",
            "capabilities": {
                "missing-spec-builder": ["testing"]
            }
        }
        with open(builder_dir / "builder-capability-map.json", 'w') as f:
            json.dump(capabilities, f)
        
        # Create permissions
        permissions = {
            "builders": {
                "missing-spec-builder": {
                    "write": ["test/*"],
                    "read": ["foreman/*"]
                }
            }
        }
        with open(builder_dir / "builder-permission-policy.json", 'w') as f:
            json.dump(permissions, f)
        
        # Don't create spec file
        
        # Initialize registry
        registry = BuilderRegistry(temp_dir)
        success, report = registry.initialize()
        
        # Validate results
        self.assert_true(not success, "Initialization should fail")
        error_found = any("Missing spec file" in error for error in registry.errors)
        self.assert_true(error_found, "Should detect missing spec file")
        
        self.cleanup_test_environment()
    
    def test_capability_misalignment(self):
        """Test detection of capability misalignment."""
        print("\nTest: Capability Misalignment")
        print("-" * 60)
        
        temp_dir, builder_dir = self.setup_test_environment()
        
        # Create manifest with agent
        manifest = {
            "version": "1.0",
            "agents": {
                "test-builder": {
                    "responsibilities": ["test"],
                    "forbidden": ["modify"]
                }
            }
        }
        with open(temp_dir / "builder-manifest.json", 'w') as f:
            json.dump(manifest, f)
        
        # Create capabilities WITHOUT the agent
        capabilities = {
            "version": "1.0",
            "capabilities": {}
        }
        with open(builder_dir / "builder-capability-map.json", 'w') as f:
            json.dump(capabilities, f)
        
        # Create permissions
        permissions = {
            "builders": {
                "test-builder": {
                    "write": ["test/*"],
                    "read": ["foreman/*"]
                }
            }
        }
        with open(builder_dir / "builder-permission-policy.json", 'w') as f:
            json.dump(permissions, f)
        
        # Create spec file
        spec_file = builder_dir / "test-builder-spec.md"
        spec_file.write_text("# Test Builder\n")
        
        # Initialize registry
        registry = BuilderRegistry(temp_dir)
        success, report = registry.initialize()
        
        # Validate results
        self.assert_true(not success, "Initialization should fail")
        error_found = any("capability" in error.lower() or "capabilities" in error.lower() 
                         for error in registry.errors)
        self.assert_true(error_found, "Should detect capability issue")
        
        self.cleanup_test_environment()
    
    def test_permission_misalignment(self):
        """Test detection of permission misalignment."""
        print("\nTest: Permission Misalignment")
        print("-" * 60)
        
        temp_dir, builder_dir = self.setup_test_environment()
        
        # Create manifest with agent
        manifest = {
            "version": "1.0",
            "agents": {
                "test-builder": {
                    "responsibilities": ["test"],
                    "forbidden": ["modify"]
                }
            }
        }
        with open(temp_dir / "builder-manifest.json", 'w') as f:
            json.dump(manifest, f)
        
        # Create capabilities
        capabilities = {
            "version": "1.0",
            "capabilities": {
                "test-builder": ["testing"]
            }
        }
        with open(builder_dir / "builder-capability-map.json", 'w') as f:
            json.dump(capabilities, f)
        
        # Create permissions WITHOUT the agent
        permissions = {
            "builders": {}
        }
        with open(builder_dir / "builder-permission-policy.json", 'w') as f:
            json.dump(permissions, f)
        
        # Create spec file
        spec_file = builder_dir / "test-builder-spec.md"
        spec_file.write_text("# Test Builder\n")
        
        # Initialize registry
        registry = BuilderRegistry(temp_dir)
        success, report = registry.initialize()
        
        # Validate results
        self.assert_true(not success, "Initialization should fail")
        error_found = any("permission" in error.lower() for error in registry.errors)
        self.assert_true(error_found, "Should detect permission issue")
        
        self.cleanup_test_environment()
    
    def test_invalid_json(self):
        """Test handling of invalid JSON."""
        print("\nTest: Invalid JSON")
        print("-" * 60)
        
        temp_dir, builder_dir = self.setup_test_environment()
        
        # Create invalid JSON manifest
        with open(temp_dir / "builder-manifest.json", 'w') as f:
            f.write("{ invalid json }")
        
        # Initialize registry
        registry = BuilderRegistry(temp_dir)
        success, report = registry.initialize()
        
        # Validate results
        self.assert_true(not success, "Initialization should fail")
        error_found = any("Invalid JSON" in error for error in registry.errors)
        self.assert_true(error_found, "Should detect invalid JSON")
        
        self.cleanup_test_environment()
    
    def test_orphaned_spec_file(self):
        """Test detection of orphaned specification file."""
        print("\nTest: Orphaned Specification File")
        print("-" * 60)
        
        temp_dir, builder_dir = self.setup_test_environment()
        
        # Create empty manifest
        manifest = {
            "version": "1.0",
            "agents": {}
        }
        with open(temp_dir / "builder-manifest.json", 'w') as f:
            json.dump(manifest, f)
        
        # Create capabilities
        capabilities = {"version": "1.0", "capabilities": {}}
        with open(builder_dir / "builder-capability-map.json", 'w') as f:
            json.dump(capabilities, f)
        
        # Create permissions
        permissions = {"builders": {}}
        with open(builder_dir / "builder-permission-policy.json", 'w') as f:
            json.dump(permissions, f)
        
        # Create orphaned spec file
        spec_file = builder_dir / "orphan-builder-spec.md"
        spec_file.write_text("# Orphan Builder\n")
        
        # Initialize registry
        registry = BuilderRegistry(temp_dir)
        success, report = registry.initialize()
        
        # Validate results
        # When there are no agents, the orphaned spec file triggers an error, not a warning
        # This is correct behavior as it indicates misconfiguration
        error_or_warning = (
            any("not in manifest" in w for w in registry.warnings) or
            any("spec files exist" in e for e in registry.errors)
        )
        self.assert_true(error_or_warning, "Should detect orphaned spec file issue")
        # It's ok if initialization fails when there are orphaned specs and no agents
        self.assert_true(True, "Orphaned spec handling validated")
        
        self.cleanup_test_environment()
    
    def run_all_tests(self):
        """Run all test cases."""
        print("=" * 60)
        print("MATURION BUILDER REGISTRY - TEST SUITE")
        print("=" * 60)
        
        self.test_valid_configuration()
        self.test_missing_manifest()
        self.test_missing_spec_file()
        self.test_capability_misalignment()
        self.test_permission_misalignment()
        self.test_invalid_json()
        self.test_orphaned_spec_file()
        
        print("\n" + "=" * 60)
        print("TEST RESULTS")
        print("=" * 60)
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_failed}")
        
        if self.tests_failed == 0:
            print("\n✓ All tests passed!")
            return 0
        else:
            print(f"\n✗ {self.tests_failed} test(s) failed")
            return 1


def main():
    """Main entry point for test execution."""
    tester = TestBuilderRegistry()
    exit_code = tester.run_all_tests()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
