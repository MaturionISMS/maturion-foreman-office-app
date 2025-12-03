#!/usr/bin/env python3
"""
Maturion Foreman - Builder Agent Registry Initializer

This script loads, validates, and registers all builder agents for the
Maturion ISMS ecosystem. It ensures proper configuration alignment and
generates a comprehensive validation report.

Usage:
    python3 foreman/init-builders.py
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class BuilderRegistry:
    """Manages builder agent registration and validation."""
    
    def __init__(self, foreman_dir: Path):
        self.foreman_dir = foreman_dir
        self.builder_dir = foreman_dir / "builder"
        self.manifest = {}
        self.capabilities = {}
        self.permissions = {}
        self.spec_files = []
        self.validation_results = []
        self.errors = []
        self.warnings = []
    
    def load_json_file(self, file_path: Path, file_type: str) -> dict:
        """Load and parse a JSON file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                self.validation_results.append(
                    f"✓ Successfully loaded {file_type}: {file_path.name}"
                )
                return data
        except FileNotFoundError:
            error = f"✗ ERROR: {file_type} not found: {file_path}"
            self.errors.append(error)
            return {}
        except json.JSONDecodeError as e:
            error = f"✗ ERROR: Invalid JSON in {file_type}: {e}"
            self.errors.append(error)
            return {}
    
    def load_manifest(self):
        """Load builder-manifest.json."""
        manifest_path = self.foreman_dir / "builder-manifest.json"
        self.manifest = self.load_json_file(manifest_path, "builder-manifest.json")
    
    def load_capabilities(self):
        """Load builder-capability-map.json."""
        capability_path = self.builder_dir / "builder-capability-map.json"
        self.capabilities = self.load_json_file(
            capability_path, "builder-capability-map.json"
        )
    
    def load_permissions(self):
        """Load builder-permission-policy.json."""
        permission_path = self.builder_dir / "builder-permission-policy.json"
        self.permissions = self.load_json_file(
            permission_path, "builder-permission-policy.json"
        )
    
    def discover_spec_files(self):
        """Discover all builder specification files."""
        if not self.builder_dir.exists():
            error = f"✗ ERROR: Builder directory not found: {self.builder_dir}"
            self.errors.append(error)
            return
        
        self.spec_files = list(self.builder_dir.glob("*-builder-spec.md"))
        self.validation_results.append(
            f"✓ Discovered {len(self.spec_files)} builder specification files"
        )
    
    def validate_spec_files(self):
        """Validate that each spec file corresponds to a builder in the manifest."""
        if not self.manifest.get('agents'):
            self.errors.append("✗ ERROR: No agents defined in manifest")
            return
        
        manifest_agents = set(self.manifest['agents'].keys())
        spec_agents = set()
        
        for spec_file in self.spec_files:
            # Extract agent name from filename (e.g., "ui-builder-spec.md" -> "ui-builder")
            agent_name = spec_file.stem.replace("-spec", "")
            spec_agents.add(agent_name)
            
            if agent_name not in manifest_agents:
                warning = f"⚠ WARNING: Spec file found for '{agent_name}' but not in manifest"
                self.warnings.append(warning)
            else:
                self.validation_results.append(
                    f"✓ Spec file validated for '{agent_name}'"
                )
        
        # Check for missing spec files
        for agent_name in manifest_agents:
            if agent_name not in spec_agents:
                error = f"✗ ERROR: Missing spec file for agent '{agent_name}'"
                self.errors.append(error)
    
    def validate_capability_alignment(self):
        """Validate that capabilities align with manifest agents."""
        if not self.capabilities.get('capabilities'):
            self.errors.append("✗ ERROR: No capabilities defined")
            return
        
        if not self.manifest.get('agents'):
            return
        
        manifest_agents = set(self.manifest['agents'].keys())
        capability_agents = set(self.capabilities['capabilities'].keys())
        
        # Check for agents in manifest but missing capabilities
        missing_caps = manifest_agents - capability_agents
        for agent in missing_caps:
            error = f"✗ ERROR: Agent '{agent}' in manifest has no capability definition"
            self.errors.append(error)
        
        # Check for capabilities without manifest entry
        extra_caps = capability_agents - manifest_agents
        for agent in extra_caps:
            warning = f"⚠ WARNING: Capability defined for '{agent}' but not in manifest"
            self.warnings.append(warning)
        
        # Validate agents that are properly aligned
        aligned = manifest_agents & capability_agents
        for agent in aligned:
            caps = self.capabilities['capabilities'][agent]
            self.validation_results.append(
                f"✓ Capability alignment validated for '{agent}': {len(caps)} capabilities"
            )
    
    def validate_permission_alignment(self):
        """Validate that permissions align with manifest agents."""
        if not self.permissions.get('builders'):
            self.errors.append("✗ ERROR: No permissions defined")
            return
        
        if not self.manifest.get('agents'):
            return
        
        manifest_agents = set(self.manifest['agents'].keys())
        permission_agents = set(self.permissions['builders'].keys())
        
        # Check for agents in manifest but missing permissions
        missing_perms = manifest_agents - permission_agents
        for agent in missing_perms:
            error = f"✗ ERROR: Agent '{agent}' in manifest has no permission policy"
            self.errors.append(error)
        
        # Check for permissions without manifest entry
        extra_perms = permission_agents - manifest_agents
        for agent in extra_perms:
            warning = f"⚠ WARNING: Permission defined for '{agent}' but not in manifest"
            self.warnings.append(warning)
        
        # Validate agents that are properly aligned
        aligned = manifest_agents & permission_agents
        for agent in aligned:
            perms = self.permissions['builders'][agent]
            read_paths = len(perms.get('read', []))
            write_paths = len(perms.get('write', []))
            self.validation_results.append(
                f"✓ Permission alignment validated for '{agent}': "
                f"{read_paths} read, {write_paths} write"
            )
    
    def validate_manifest_structure(self):
        """Validate the structure and content of the manifest."""
        if not self.manifest:
            return
        
        if 'version' not in self.manifest:
            warning = "⚠ WARNING: Manifest missing version field"
            self.warnings.append(warning)
        
        if 'agents' not in self.manifest:
            error = "✗ ERROR: Manifest missing 'agents' section"
            self.errors.append(error)
            return
        
        # Validate each agent definition
        for agent_name, agent_config in self.manifest['agents'].items():
            if 'responsibilities' not in agent_config:
                error = f"✗ ERROR: Agent '{agent_name}' missing 'responsibilities'"
                self.errors.append(error)
            elif len(agent_config['responsibilities']) == 0:
                warning = f"⚠ WARNING: Agent '{agent_name}' has empty responsibilities"
                self.warnings.append(warning)
            
            if 'forbidden' not in agent_config:
                warning = f"⚠ WARNING: Agent '{agent_name}' missing 'forbidden' actions"
                self.warnings.append(warning)
    
    def generate_report(self) -> str:
        """Generate a comprehensive validation report."""
        report_lines = []
        
        # Header
        report_lines.append("=" * 80)
        report_lines.append("MATURION FOREMAN - BUILDER AGENT REGISTRY REPORT")
        report_lines.append("=" * 80)
        report_lines.append("")
        
        # Summary
        total_agents = len(self.manifest.get('agents', {}))
        report_lines.append("SUMMARY")
        report_lines.append("-" * 80)
        report_lines.append(f"Total Agents Registered: {total_agents}")
        report_lines.append(f"Specification Files Found: {len(self.spec_files)}")
        report_lines.append(f"Validation Checks: {len(self.validation_results)}")
        report_lines.append(f"Errors: {len(self.errors)}")
        report_lines.append(f"Warnings: {len(self.warnings)}")
        report_lines.append("")
        
        # Registered Agents
        if self.manifest.get('agents'):
            report_lines.append("REGISTERED AGENTS")
            report_lines.append("-" * 80)
            for agent_name, config in self.manifest['agents'].items():
                report_lines.append(f"\n[{agent_name}]")
                
                # Responsibilities
                responsibilities = config.get('responsibilities', [])
                report_lines.append(f"  Responsibilities: {', '.join(responsibilities)}")
                
                # Forbidden actions
                forbidden = config.get('forbidden', [])
                report_lines.append(f"  Forbidden: {', '.join(forbidden)}")
                
                # Capabilities
                caps = self.capabilities.get('capabilities', {}).get(agent_name, [])
                if caps:
                    report_lines.append(f"  Capabilities: {', '.join(caps)}")
                
                # Permissions
                perms = self.permissions.get('builders', {}).get(agent_name, {})
                if perms:
                    read_paths = perms.get('read', [])
                    write_paths = perms.get('write', [])
                    report_lines.append(f"  Read Access: {', '.join(read_paths)}")
                    report_lines.append(f"  Write Access: {', '.join(write_paths)}")
            report_lines.append("")
        
        # Validation Results
        if self.validation_results:
            report_lines.append("VALIDATION RESULTS")
            report_lines.append("-" * 80)
            for result in self.validation_results:
                report_lines.append(result)
            report_lines.append("")
        
        # Warnings
        if self.warnings:
            report_lines.append("WARNINGS")
            report_lines.append("-" * 80)
            for warning in self.warnings:
                report_lines.append(warning)
            report_lines.append("")
        
        # Errors
        if self.errors:
            report_lines.append("ERRORS")
            report_lines.append("-" * 80)
            for error in self.errors:
                report_lines.append(error)
            report_lines.append("")
        
        # Status
        report_lines.append("STATUS")
        report_lines.append("-" * 80)
        if self.errors:
            report_lines.append("✗ FAILED: Builder agent initialization failed with errors")
            report_lines.append("         Please resolve all errors before proceeding.")
        elif self.warnings:
            report_lines.append("⚠ PASSED WITH WARNINGS: Builder agents initialized successfully")
            report_lines.append("         Please review warnings for potential issues.")
        else:
            report_lines.append("✓ SUCCESS: All builder agents initialized and validated successfully")
        
        report_lines.append("=" * 80)
        
        return "\n".join(report_lines)
    
    def initialize(self) -> Tuple[bool, str]:
        """
        Execute the full initialization and validation process.
        
        Returns:
            Tuple of (success: bool, report: str)
        """
        print("Initializing Maturion Builder Agent Registry...")
        print()
        
        # Load configuration files
        self.load_manifest()
        self.load_capabilities()
        self.load_permissions()
        
        # Discover and validate specifications
        self.discover_spec_files()
        
        # Run validations
        self.validate_manifest_structure()
        self.validate_spec_files()
        self.validate_capability_alignment()
        self.validate_permission_alignment()
        
        # Generate report
        report = self.generate_report()
        
        # Determine success
        success = len(self.errors) == 0
        
        return success, report


def main():
    """Main entry point for builder initialization."""
    # Determine foreman directory
    script_path = Path(__file__).resolve()
    foreman_dir = script_path.parent
    
    # Initialize registry
    registry = BuilderRegistry(foreman_dir)
    success, report = registry.initialize()
    
    # Print report
    print(report)
    
    # Save report to file
    report_path = foreman_dir / "builder-registry-report.md"
    with open(report_path, 'w') as f:
        f.write(report)
    
    print()
    print(f"Report saved to: {report_path}")
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
