#!/usr/bin/env python3
"""
Maturion AI Foreman - ISMS Architecture Indexing System
Indexes all architecture files, builds module maps, dependency graphs, and compliance mappings
"""

import json
import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
from datetime import datetime


class ISMSArchitectureIndexer:
    """Comprehensive indexing system for all ISMS architecture files"""
    
    # Health score calculation constants
    MISSING_ELEMENT_PENALTY = 5  # Points deducted per missing element
    HIGH_SEVERITY_INCONSISTENCY_PENALTY = 10  # Points deducted per high severity issue
    VERSION_SPREAD_THRESHOLD = 3  # Number of different versions before flagging
    COMPLIANCE_REFERENCE_LENGTH_LIMIT = 100  # Max characters for compliance reference text
    
    # Known modules in the ISMS ecosystem
    MODULES = [
        'COURSE_CRAFTER',
        'ERM',
        'PIT',
        'THREAT',
        'VULNERABILITY',
        'RISK_ASSESSMENT',
        'WRAC',
        'RISK_THREAT',
        'RISK_VULNERABILITY',
        'POLICY_BUILDER',
        'ANALYTICS_REMOTE_ASSURANCE',
        'AUDITOR_MOBILE_APP',
        'SKILLS_DEVELOPMENT_PORTAL'
    ]
    
    # Architecture specification types
    SPEC_TYPES = {
        'TRUE_NORTH': 'Module Architecture',
        'ARCHITECTURE': 'Architecture Design',
        'DATABASE_SCHEMA': 'Data Model',
        'FRONTEND_COMPONENT_MAP': 'UI Components',
        'WIREFRAMES': 'UI Design',
        'EDGE_FUNCTIONS': 'Backend API',
        'INTEGRATION_SPEC': 'Module Integration',
        'INTEGRATION_MAP': 'Module Integration',
        'EXPORT_SPEC': 'Data Export',
        'QA_IMPLEMENTATION_PLAN': 'Quality Assurance',
        'IMPLEMENTATION_GUIDE': 'Implementation',
        'SPRINT_PLAN': 'Development Plan',
        'CHANGELOG': 'Version History',
        'WATCHDOG_LOGIC': 'Monitoring',
        'MODEL_ROUTING_SPEC': 'AI Routing'
    }
    
    # Compliance standards
    COMPLIANCE_STANDARDS = [
        'ISO 27001',
        'ISO 27005',
        'ISO 31000',
        'ISO 22301',
        'NIST CSF',
        'NIST 800-53',
        'COBIT',
        'GDPR',
        'POPIA',
        'OWASP ASVS',
        'OWASP Top 10'
    ]
    
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.index = {
            'metadata': {
                'indexed_at': datetime.now().isoformat(),
                'repo_root': str(repo_root),
                'total_modules': 0,
                'total_files': 0
            },
            'modules': {},
            'true_north_index': {},
            'dependency_map': {},
            'compliance_mapping': {},
            'missing_elements': [],
            'inconsistencies': []
        }
        
    def index_all(self) -> Dict:
        """Run complete indexing process"""
        print("🔍 Starting ISMS Architecture Indexing...\n")
        
        self.build_module_map()
        self.build_true_north_index()
        self.build_dependency_map()
        self.build_compliance_mapping()
        self.validate_completeness()
        self.identify_missing_elements()
        self.detect_inconsistencies()
        
        # Update metadata
        self.index['metadata']['total_modules'] = len(self.index['modules'])
        self.index['metadata']['total_files'] = sum(
            len(mod['files']) for mod in self.index['modules'].values()
        )
        
        return self.index
    
    def _extract_version(self, filename: str) -> Tuple[int, int]:
        """
        Extract version number from filename.
        
        Supports format: _vMAJOR.MINOR (e.g., _v1.0, _v2.1)
        Returns (0, 0) for files without version or with non-standard version format.
        This ensures unversioned files sort before versioned files.
        """
        match = re.search(r'_v(\d+)\.(\d+)', filename)
        if match:
            return (int(match.group(1)), int(match.group(2)))
        return (0, 0)  # Fallback for unversioned or non-standard formats
    
    def _get_latest_version(self, files: List[Path]) -> Path:
        """Get the file with the latest version"""
        return max(files, key=lambda f: self._extract_version(f.name))
    
    def _extract_dependencies_from_file(self, file_path: Path) -> Set[str]:
        """
        Extract module dependencies from file content.
        
        Uses word boundary matching to avoid false positives from partial matches
        (e.g., 'THREAT' within 'RISK_THREAT' or in URLs).
        """
        dependencies = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for references to other modules with word boundaries
            for module in self.MODULES:
                # Use word boundary pattern to avoid partial matches
                pattern = r'\b' + re.escape(module) + r'\b'
                if re.search(pattern, content):
                    dependencies.add(module)
            
            # Look for integration patterns
            integration_patterns = [
                r'integrates?\s+with\s+(\w+)',
                r'depends?\s+on\s+(\w+)',
                r'references?\s+(\w+)',
                r'links?\s+to\s+(\w+)'
            ]
            
            for pattern in integration_patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    potential_module = match.group(1).upper()
                    if potential_module in self.MODULES:
                        dependencies.add(potential_module)
        
        except Exception as e:
            print(f"  ⚠️  Could not read {file_path.name}: {e}")
        
        return dependencies
    
    def _extract_compliance_references(self, file_path: Path) -> Dict[str, List[str]]:
        """
        Extract compliance standard references from file.
        
        Limits reference text to COMPLIANCE_REFERENCE_LENGTH_LIMIT characters
        to keep the index file manageable while preserving context.
        """
        compliance_refs = defaultdict(list)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for standard in self.COMPLIANCE_STANDARDS:
                # Look for standard references
                pattern = re.escape(standard) + r'[:\s]+([A-Z0-9.\-\s]+)'
                matches = re.finditer(pattern, content, re.IGNORECASE)
                
                for match in matches:
                    reference = match.group(1).strip()[:self.COMPLIANCE_REFERENCE_LENGTH_LIMIT]
                    compliance_refs[standard].append(reference)
                
                # Simple presence check
                if standard in content and not compliance_refs[standard]:
                    compliance_refs[standard].append('Referenced')
        
        except Exception as e:
            print(f"  ⚠️  Could not read {file_path.name}: {e}")
        
        return dict(compliance_refs)
    
    def build_module_map(self):
        """Build comprehensive module map"""
        print("📊 Building Module Map...")
        
        for module in self.MODULES:
            module_data = {
                'name': module,
                'files': {},
                'versions': {},
                'completeness': {},
                'file_count': 0
            }
            
            # Find all files for this module
            # Search in both maturion-isms/apps subdirectories and repo root
            pattern = f"{module}_*_v*.md"
            matching_files = []
            
            # Search in maturion-isms/apps structure
            apps_dir = self.repo_root / 'maturion-isms' / 'apps'
            if apps_dir.exists():
                # Search in all subdirectories under apps
                for module_dir in apps_dir.iterdir():
                    if module_dir.is_dir():
                        # Search in architecture/ and qa-plans/ subdirectories
                        for arch_file in (module_dir / 'architecture').glob(pattern):
                            matching_files.append(arch_file)
                        for qa_file in (module_dir / 'qa-plans').glob(pattern):
                            matching_files.append(qa_file)
            
            # Also search in repo root for backward compatibility
            matching_files.extend(self.repo_root.glob(pattern))
            
            if not matching_files:
                print(f"  ⚠️  No files found for module: {module}")
                continue
            
            # Group files by spec type
            spec_files = defaultdict(list)
            for file_path in matching_files:
                # Extract spec type
                for spec_type in self.SPEC_TYPES.keys():
                    if spec_type in file_path.name:
                        spec_files[spec_type].append(file_path)
                        break
            
            # Build file inventory with latest versions
            for spec_type, files in spec_files.items():
                if files:
                    latest_file = self._get_latest_version(files)
                    version = self._extract_version(latest_file.name)
                    
                    module_data['files'][spec_type] = {
                        'path': str(latest_file.relative_to(self.repo_root)),
                        'version': f"{version[0]}.{version[1]}",
                        'description': self.SPEC_TYPES[spec_type],
                        'size': latest_file.stat().st_size,
                        'all_versions': [f.name for f in files]
                    }
                    module_data['file_count'] += 1
            
            # Calculate completeness
            total_specs = len(self.SPEC_TYPES)
            present_specs = len(module_data['files'])
            completeness_pct = (present_specs / total_specs) * 100
            
            module_data['completeness'] = {
                'percentage': round(completeness_pct, 1),
                'present': present_specs,
                'total': total_specs,
                'missing': [spec for spec in self.SPEC_TYPES.keys() 
                           if spec not in module_data['files']]
            }
            
            self.index['modules'][module] = module_data
            print(f"  ✓ Indexed {module}: {present_specs}/{total_specs} specs ({completeness_pct:.1f}%)")
        
        print(f"  ✓ Indexed {len(self.index['modules'])} modules\n")
    
    def build_true_north_index(self):
        """Build True North architecture index"""
        print("🧭 Building True North Index...")
        
        # Search in both maturion-isms/apps structure and repo root
        true_north_files = []
        
        # Search in maturion-isms/apps structure
        apps_dir = self.repo_root / 'maturion-isms' / 'apps'
        if apps_dir.exists():
            for module_dir in apps_dir.iterdir():
                if module_dir.is_dir():
                    true_north_files.extend((module_dir / 'architecture').glob("*TRUE_NORTH*.md"))
        
        # Also search in repo root for backward compatibility
        true_north_files.extend(self.repo_root.glob("*TRUE_NORTH*.md"))
        
        for file_path in true_north_files:
            # Determine which module this belongs to
            module = None
            for mod in self.MODULES:
                if file_path.name.startswith(mod):
                    module = mod
                    break
            
            if not module:
                print(f"  ⚠️  Could not determine module for: {file_path.name}")
                continue
            
            version = self._extract_version(file_path.name)
            
            true_north_data = {
                'module': module,
                'path': str(file_path.relative_to(self.repo_root)),
                'version': f"{version[0]}.{version[1]}",
                'size': file_path.stat().st_size,
                'exists': True
            }
            
            # Try to extract key information
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Count sections (marked by #)
                sections = len(re.findall(r'^#+\s+', content, re.MULTILINE))
                true_north_data['sections'] = sections
                
                # Look for key architecture elements
                true_north_data['has_purpose'] = 'purpose' in content.lower()
                true_north_data['has_architecture'] = 'architecture' in content.lower()
                true_north_data['has_data_model'] = 'data model' in content.lower() or 'schema' in content.lower()
                true_north_data['has_integration'] = 'integration' in content.lower()
                
            except Exception as e:
                print(f"  ⚠️  Could not analyze {file_path.name}: {e}")
            
            self.index['true_north_index'][module] = true_north_data
            print(f"  ✓ Indexed True North for {module} (v{true_north_data['version']})")
        
        # Identify modules without True North
        modules_without_tn = set(self.MODULES) - set(self.index['true_north_index'].keys())
        if modules_without_tn:
            print(f"  ⚠️  Modules without True North: {', '.join(modules_without_tn)}")
        
        print(f"  ✓ Indexed {len(self.index['true_north_index'])} True North documents\n")
    
    def build_dependency_map(self):
        """Build module dependency map"""
        print("🔗 Building Dependency Map...")
        
        # Check for integration map document
        integration_map_file = self.repo_root / "INTEGRATED_ISMS_MODULE_INTEGRATION_MAP_v1.0.md"
        if integration_map_file.exists():
            print(f"  ✓ Found master integration map: {integration_map_file.name}")
            
            try:
                with open(integration_map_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.index['dependency_map']['master_integration_map'] = {
                    'path': str(integration_map_file.relative_to(self.repo_root)),
                    'size': integration_map_file.stat().st_size,
                    'has_hub_spoke_diagram': 'hub-and-spoke' in content.lower(),
                    'has_workflow_map': 'workflow' in content.lower()
                }
            except Exception as e:
                print(f"  ⚠️  Could not read integration map: {e}")
        
        # Build module-level dependencies
        module_dependencies = {}
        
        for module, module_data in self.index['modules'].items():
            dependencies = set()
            
            # Check each file for dependencies
            for spec_type, file_info in module_data['files'].items():
                file_path = self.repo_root / file_info['path']
                deps = self._extract_dependencies_from_file(file_path)
                dependencies.update(deps)
            
            # Remove self-reference
            dependencies.discard(module)
            
            module_dependencies[module] = {
                'depends_on': sorted(list(dependencies)),
                'dependency_count': len(dependencies)
            }
            
            if dependencies:
                print(f"  ✓ {module} depends on: {', '.join(sorted(dependencies))}")
        
        self.index['dependency_map']['modules'] = module_dependencies
        
        # Calculate dependency statistics
        total_dependencies = sum(d['dependency_count'] for d in module_dependencies.values())
        avg_dependencies = total_dependencies / len(module_dependencies) if module_dependencies else 0
        
        self.index['dependency_map']['statistics'] = {
            'total_dependencies': total_dependencies,
            'average_per_module': round(avg_dependencies, 2),
            'most_dependent': max(module_dependencies.items(), 
                                 key=lambda x: x[1]['dependency_count'])[0] if module_dependencies else None,
            'most_referenced': self._find_most_referenced_module(module_dependencies)
        }
        
        print(f"  ✓ Mapped {total_dependencies} module dependencies\n")
    
    def _find_most_referenced_module(self, dependencies: Dict) -> str:
        """Find the module that is most frequently referenced by others"""
        reference_count = defaultdict(int)
        
        for module_deps in dependencies.values():
            for dep in module_deps['depends_on']:
                reference_count[dep] += 1
        
        if reference_count:
            return max(reference_count.items(), key=lambda x: x[1])[0]
        return None
    
    def build_compliance_mapping(self):
        """Build compliance standard mapping"""
        print("📜 Building Compliance Mapping...")
        
        # Check compliance reference map
        compliance_ref_map = self.repo_root / "foreman/compliance/compliance-reference-map.md"
        if compliance_ref_map.exists():
            print(f"  ✓ Found compliance reference map")
            
            self.index['compliance_mapping']['reference_map'] = {
                'path': str(compliance_ref_map.relative_to(self.repo_root)),
                'size': compliance_ref_map.stat().st_size
            }
        
        # Map compliance by standard
        compliance_by_standard = defaultdict(lambda: defaultdict(list))
        
        for module, module_data in self.index['modules'].items():
            for spec_type, file_info in module_data['files'].items():
                file_path = self.repo_root / file_info['path']
                compliance_refs = self._extract_compliance_references(file_path)
                
                for standard, references in compliance_refs.items():
                    compliance_by_standard[standard][module].extend(references)
        
        # Calculate coverage
        coverage_by_standard = {}
        total_modules = len(self.index['modules'])
        
        for standard in self.COMPLIANCE_STANDARDS:
            modules_with_standard = len(compliance_by_standard.get(standard, {}))
            coverage_pct = (modules_with_standard / total_modules * 100) if total_modules else 0
            
            coverage_by_standard[standard] = {
                'modules_covered': modules_with_standard,
                'total_modules': total_modules,
                'coverage_percentage': round(coverage_pct, 1),
                'modules': list(compliance_by_standard.get(standard, {}).keys())
            }
            
            print(f"  ✓ {standard}: {coverage_pct:.1f}% coverage ({modules_with_standard}/{total_modules} modules)")
        
        self.index['compliance_mapping']['coverage_by_standard'] = coverage_by_standard
        self.index['compliance_mapping']['module_references'] = dict(compliance_by_standard)
        
        # Overall compliance coverage
        total_coverage = sum(c['coverage_percentage'] for c in coverage_by_standard.values())
        avg_coverage = total_coverage / len(self.COMPLIANCE_STANDARDS) if self.COMPLIANCE_STANDARDS else 0
        
        self.index['compliance_mapping']['overall'] = {
            'average_coverage': round(avg_coverage, 1),
            'standards_tracked': len(self.COMPLIANCE_STANDARDS),
            'fully_covered_standards': sum(1 for c in coverage_by_standard.values() 
                                          if c['coverage_percentage'] == 100)
        }
        
        print(f"  ✓ Overall compliance coverage: {avg_coverage:.1f}%\n")
    
    def validate_completeness(self):
        """Validate architecture completeness"""
        print("✅ Validating Architecture Completeness...")
        
        # Check for master architecture documents
        master_docs = [
            'SRMF_MASTER_BUILD_REFERENCE_v1.0.md',
            'Integrated_ISMS_Architecture_v1.1.md',
            'INTEGRATED_ISMS_MODULE_INTEGRATION_MAP_v1.0.md'
        ]
        
        for doc in master_docs:
            doc_path = self.repo_root / doc
            if doc_path.exists():
                print(f"  ✓ Found master document: {doc}")
            else:
                print(f"  ✗ Missing master document: {doc}")
                self.index['missing_elements'].append({
                    'type': 'master_document',
                    'name': doc,
                    'severity': 'critical'
                })
        
        print()
    
    def identify_missing_elements(self):
        """Identify missing architecture elements"""
        print("🔍 Identifying Missing Architecture Elements...")
        
        missing_count = 0
        
        # Check each module for missing specs
        for module, module_data in self.index['modules'].items():
            missing_specs = module_data['completeness']['missing']
            
            # Critical specs that should always be present
            critical_specs = ['TRUE_NORTH', 'DATABASE_SCHEMA']
            
            for spec in missing_specs:
                severity = 'critical' if spec in critical_specs else 'medium'
                
                if severity == 'critical' or module_data['completeness']['percentage'] < 50:
                    self.index['missing_elements'].append({
                        'type': 'specification',
                        'module': module,
                        'specification': spec,
                        'severity': severity
                    })
                    missing_count += 1
        
        # Check for modules without True North
        for module in self.MODULES:
            if module not in self.index['true_north_index']:
                self.index['missing_elements'].append({
                    'type': 'true_north',
                    'module': module,
                    'severity': 'critical'
                })
                missing_count += 1
                print(f"  ✗ Missing True North for: {module}")
        
        print(f"  ✓ Identified {missing_count} missing critical elements\n")
    
    def detect_inconsistencies(self):
        """Detect dependency and versioning inconsistencies"""
        print("🔎 Detecting Inconsistencies...")
        
        inconsistency_count = 0
        
        # Check for circular dependencies
        for module, deps in self.index['dependency_map'].get('modules', {}).items():
            for dep in deps['depends_on']:
                if dep in self.index['dependency_map'].get('modules', {}):
                    if module in self.index['dependency_map']['modules'][dep]['depends_on']:
                        self.index['inconsistencies'].append({
                            'type': 'circular_dependency',
                            'modules': [module, dep],
                            'severity': 'high'
                        })
                        inconsistency_count += 1
                        print(f"  ⚠️  Circular dependency: {module} ↔ {dep}")
        
        # Check for orphaned modules (no dependencies and not referenced)
        for module, deps in self.index['dependency_map'].get('modules', {}).items():
            if deps['dependency_count'] == 0:
                # Check if any other module depends on this one
                is_referenced = any(
                    module in other_deps['depends_on']
                    for other_module, other_deps in self.index['dependency_map']['modules'].items()
                    if other_module != module
                )
                
                if not is_referenced:
                    self.index['inconsistencies'].append({
                        'type': 'orphaned_module',
                        'module': module,
                        'severity': 'low'
                    })
                    inconsistency_count += 1
                    print(f"  ⚠️  Orphaned module (no dependencies): {module}")
        
        # Check for version inconsistencies
        # Flag modules with too many different versions as this may indicate
        # incomplete migration or inconsistent versioning practices
        for module, module_data in self.index['modules'].items():
            versions = set()
            for spec_type, file_info in module_data['files'].items():
                versions.add(file_info['version'])
            
            if len(versions) > self.VERSION_SPREAD_THRESHOLD:
                self.index['inconsistencies'].append({
                    'type': 'version_spread',
                    'module': module,
                    'versions': sorted(list(versions)),
                    'severity': 'low'
                })
                inconsistency_count += 1
                print(f"  ⚠️  High version spread in {module}: {len(versions)} different versions")
        
        print(f"  ✓ Detected {inconsistency_count} inconsistencies\n")
    
    def generate_report(self) -> str:
        """Generate comprehensive architecture index report"""
        print("📄 Generating Architecture Index Report...")
        
        report = []
        report.append("=" * 100)
        report.append("MATURION ISMS - ARCHITECTURE INDEX REPORT")
        report.append("=" * 100)
        report.append(f"Generated: {self.index['metadata']['indexed_at']}")
        report.append(f"Repository: {self.index['metadata']['repo_root']}")
        report.append("")
        
        # Executive Summary
        report.append("📊 EXECUTIVE SUMMARY")
        report.append("-" * 100)
        report.append(f"Total Modules Indexed: {self.index['metadata']['total_modules']}")
        report.append(f"Total Architecture Files: {self.index['metadata']['total_files']}")
        report.append(f"True North Documents: {len(self.index['true_north_index'])}")
        report.append(f"Overall Compliance Coverage: {self.index['compliance_mapping']['overall']['average_coverage']:.1f}%")
        report.append(f"Missing Critical Elements: {len(self.index['missing_elements'])}")
        report.append(f"Detected Inconsistencies: {len(self.index['inconsistencies'])}")
        report.append("")
        
        # Module Map
        report.append("📊 MODULE MAP")
        report.append("-" * 100)
        for module, module_data in sorted(self.index['modules'].items()):
            completeness = module_data['completeness']['percentage']
            status_icon = "✓" if completeness >= 80 else ("⚠" if completeness >= 50 else "✗")
            
            report.append(f"\n{status_icon} {module}")
            report.append(f"   Completeness: {completeness}% ({module_data['completeness']['present']}/{module_data['completeness']['total']} specs)")
            report.append(f"   Files: {module_data['file_count']}")
            
            if module_data['completeness']['missing']:
                missing_critical = [s for s in module_data['completeness']['missing'] 
                                   if s in ['TRUE_NORTH', 'DATABASE_SCHEMA']]
                if missing_critical:
                    report.append(f"   ⚠️  Missing Critical: {', '.join(missing_critical)}")
            
            # List key files
            for spec_type in ['TRUE_NORTH', 'DATABASE_SCHEMA', 'INTEGRATION_MAP']:
                if spec_type in module_data['files']:
                    file_info = module_data['files'][spec_type]
                    report.append(f"   • {spec_type}: v{file_info['version']}")
        
        report.append("")
        
        # True North Index
        report.append("🧭 TRUE NORTH INDEX")
        report.append("-" * 100)
        for module, tn_data in sorted(self.index['true_north_index'].items()):
            report.append(f"✓ {module}")
            report.append(f"  Version: {tn_data['version']}")
            report.append(f"  Path: {tn_data['path']}")
            
            if 'sections' in tn_data:
                report.append(f"  Sections: {tn_data['sections']}")
            
            completeness_indicators = []
            if tn_data.get('has_purpose'): completeness_indicators.append('Purpose')
            if tn_data.get('has_architecture'): completeness_indicators.append('Architecture')
            if tn_data.get('has_data_model'): completeness_indicators.append('Data Model')
            if tn_data.get('has_integration'): completeness_indicators.append('Integration')
            
            if completeness_indicators:
                report.append(f"  Contains: {', '.join(completeness_indicators)}")
            report.append("")
        
        # Dependency Map
        report.append("🔗 ARCHITECTURE DEPENDENCY MAP")
        report.append("-" * 100)
        
        if 'master_integration_map' in self.index['dependency_map']:
            report.append("Master Integration Map:")
            map_info = self.index['dependency_map']['master_integration_map']
            report.append(f"  ✓ {map_info['path']}")
            if map_info.get('has_hub_spoke_diagram'):
                report.append(f"  • Contains Hub-and-Spoke architecture diagram")
            if map_info.get('has_workflow_map'):
                report.append(f"  • Contains workflow map")
            report.append("")
        
        report.append("Module Dependencies:")
        for module, deps in sorted(self.index['dependency_map']['modules'].items()):
            if deps['depends_on']:
                report.append(f"  {module} → {', '.join(deps['depends_on'])}")
        
        stats = self.index['dependency_map']['statistics']
        report.append(f"\nDependency Statistics:")
        report.append(f"  Total Dependencies: {stats['total_dependencies']}")
        report.append(f"  Average per Module: {stats['average_per_module']}")
        if stats['most_dependent']:
            report.append(f"  Most Dependent Module: {stats['most_dependent']}")
        if stats['most_referenced']:
            report.append(f"  Most Referenced Module: {stats['most_referenced']}")
        report.append("")
        
        # Compliance Mapping
        report.append("📜 COMPLIANCE COVERAGE")
        report.append("-" * 100)
        
        overall = self.index['compliance_mapping']['overall']
        report.append(f"Overall Coverage: {overall['average_coverage']:.1f}%")
        report.append(f"Standards Tracked: {overall['standards_tracked']}")
        report.append(f"Fully Covered Standards: {overall['fully_covered_standards']}")
        report.append("")
        
        report.append("Coverage by Standard:")
        for standard, coverage in sorted(self.index['compliance_mapping']['coverage_by_standard'].items()):
            pct = coverage['coverage_percentage']
            bar_length = int(pct / 5)  # 20 chars = 100%
            bar = "█" * bar_length + "░" * (20 - bar_length)
            
            report.append(f"  {standard:20s} {bar} {pct:5.1f}% ({coverage['modules_covered']}/{coverage['total_modules']} modules)")
        
        report.append("")
        
        # Missing Elements
        report.append("⚠️  MISSING ARCHITECTURE ELEMENTS")
        report.append("-" * 100)
        
        if self.index['missing_elements']:
            critical = [e for e in self.index['missing_elements'] if e['severity'] == 'critical']
            medium = [e for e in self.index['missing_elements'] if e['severity'] == 'medium']
            
            if critical:
                report.append("Critical Missing Elements:")
                for element in critical:
                    if element['type'] == 'true_north':
                        report.append(f"  🔴 {element['module']}: Missing True North document")
                    elif element['type'] == 'specification':
                        report.append(f"  🔴 {element['module']}: Missing {element['specification']}")
                    elif element['type'] == 'master_document':
                        report.append(f"  🔴 Missing master document: {element['name']}")
                report.append("")
            
            if medium:
                report.append("Medium Priority Missing Elements:")
                for element in medium[:10]:  # Limit to first 10
                    if element['type'] == 'specification':
                        report.append(f"  🟡 {element['module']}: Missing {element['specification']}")
                
                if len(medium) > 10:
                    report.append(f"  ... and {len(medium) - 10} more")
                report.append("")
        else:
            report.append("✓ No critical missing elements detected")
            report.append("")
        
        # Inconsistencies
        report.append("🔍 DEPENDENCY INCONSISTENCIES")
        report.append("-" * 100)
        
        if self.index['inconsistencies']:
            high = [i for i in self.index['inconsistencies'] if i['severity'] == 'high']
            medium = [i for i in self.index['inconsistencies'] if i['severity'] == 'medium']
            low = [i for i in self.index['inconsistencies'] if i['severity'] == 'low']
            
            if high:
                report.append("High Severity:")
                for issue in high:
                    if issue['type'] == 'circular_dependency':
                        report.append(f"  🔴 Circular dependency: {' ↔ '.join(issue['modules'])}")
                report.append("")
            
            if low:
                report.append("Low Severity:")
                for issue in low[:5]:  # Limit to first 5
                    if issue['type'] == 'orphaned_module':
                        report.append(f"  🟡 Orphaned module: {issue['module']}")
                    elif issue['type'] == 'version_spread':
                        report.append(f"  🟡 Version spread in {issue['module']}: {len(issue['versions'])} versions")
                
                if len(low) > 5:
                    report.append(f"  ... and {len(low) - 5} more")
                report.append("")
        else:
            report.append("✓ No major inconsistencies detected")
            report.append("")
        
        # Recommendations
        report.append("💡 RECOMMENDATIONS")
        report.append("-" * 100)
        
        recommendations = []
        
        # Based on completeness
        incomplete_modules = [m for m, d in self.index['modules'].items() 
                             if d['completeness']['percentage'] < 80]
        if incomplete_modules:
            recommendations.append(f"🔹 Complete architecture specifications for: {', '.join(incomplete_modules)}")
        
        # Based on True North
        missing_tn = set(self.MODULES) - set(self.index['true_north_index'].keys())
        if missing_tn:
            recommendations.append(f"🔹 Create True North documents for: {', '.join(missing_tn)}")
        
        # Based on compliance
        low_coverage_standards = [s for s, c in self.index['compliance_mapping']['coverage_by_standard'].items()
                                 if c['coverage_percentage'] < 50]
        if low_coverage_standards:
            recommendations.append(f"🔹 Improve compliance coverage for: {', '.join(low_coverage_standards)}")
        
        # Based on dependencies
        if self.index['inconsistencies']:
            circular = [i for i in self.index['inconsistencies'] if i['type'] == 'circular_dependency']
            if circular:
                recommendations.append(f"🔹 Resolve {len(circular)} circular dependencies")
        
        if recommendations:
            for rec in recommendations:
                report.append(rec)
        else:
            report.append("✓ Architecture is well-structured and complete")
        
        report.append("")
        
        # Summary
        report.append("=" * 100)
        
        # Calculate overall health score
        # Formula: Average of (completeness + compliance) minus penalties
        # Penalties are configurable class constants to allow tuning
        completeness_score = sum(m['completeness']['percentage'] for m in self.index['modules'].values()) / len(self.index['modules']) if self.index['modules'] else 0
        compliance_score = self.index['compliance_mapping']['overall']['average_coverage']
        missing_penalty = len(self.index['missing_elements']) * self.MISSING_ELEMENT_PENALTY
        inconsistency_penalty = len([i for i in self.index['inconsistencies'] if i['severity'] == 'high']) * self.HIGH_SEVERITY_INCONSISTENCY_PENALTY
        
        health_score = max(0, min(100, (completeness_score + compliance_score) / 2 - missing_penalty - inconsistency_penalty))
        
        report.append(f"ARCHITECTURE HEALTH SCORE: {health_score:.1f}/100")
        
        if health_score >= 90:
            report.append("Status: EXCELLENT ✅")
        elif health_score >= 75:
            report.append("Status: GOOD ✓")
        elif health_score >= 60:
            report.append("Status: NEEDS IMPROVEMENT ⚠️")
        else:
            report.append("Status: REQUIRES ATTENTION ❌")
        
        report.append("=" * 100)
        
        return "\n".join(report)
    
    def save_index(self, output_file: str = "ARCHITECTURE_INDEX.json"):
        """Save index to JSON file"""
        output_path = self.repo_root / output_file
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, indent=2)
        
        print(f"✓ Saved index to: {output_file}")
        return output_path


def main():
    """Main execution function"""
    repo_root = Path(__file__).parent.absolute()
    
    indexer = ISMSArchitectureIndexer(str(repo_root))
    indexer.index_all()
    
    # Generate and save report
    report = indexer.generate_report()
    print("\n" + report)
    
    report_path = repo_root / 'ARCHITECTURE_INDEX_REPORT.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n📄 Architecture index report saved to: ARCHITECTURE_INDEX_REPORT.md")
    
    # Save JSON index
    indexer.save_index()
    
    print("\n✅ ISMS Architecture Indexing Complete!")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
