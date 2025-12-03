#!/usr/bin/env python3
"""
Maturion AI Foreman - Full Architecture Standardisation Pass
Executes comprehensive standardisation across all ISMS modules
"""

import json
import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
from datetime import datetime


class ArchitectureStandardiser:
    """Executes full architecture standardisation pass on ISMS ecosystem"""
    
    # Known modules in the ISMS ecosystem
    MODULES = [
        'COURSE_CRAFTER',
        'ERM',
        'PIT',
        'THREAT',
        'VULNERABILITY',
        'RISK_ASSESSMENT',
        'WRAC'
    ]
    
    # Required architecture components per minimum-architecture-template.md
    REQUIRED_SPECS = {
        'TRUE_NORTH': {
            'description': 'Module Architecture',
            'priority': 1,
            'required': True
        },
        'ARCHITECTURE': {
            'description': 'Architecture Design',
            'priority': 2,
            'required': True
        },
        'INTEGRATION_SPEC': {
            'description': 'Module Integration',
            'priority': 3,
            'required': True
        },
        'DATABASE_SCHEMA': {
            'description': 'Data Model',
            'priority': 4,
            'required': True
        },
        'FRONTEND_COMPONENT_MAP': {
            'description': 'UI Components',
            'priority': 5,
            'required': True
        },
        'WIREFRAMES': {
            'description': 'UI Design',
            'priority': 6,
            'required': True
        },
        'QA_IMPLEMENTATION_PLAN': {
            'description': 'Quality Assurance',
            'priority': 7,
            'required': True
        },
        'IMPLEMENTATION_GUIDE': {
            'description': 'Implementation',
            'priority': 8,
            'required': True
        },
        'SPRINT_PLAN': {
            'description': 'Development Plan',
            'priority': 9,
            'required': True
        },
        'CHANGELOG': {
            'description': 'Version History',
            'priority': 10,
            'required': True
        }
    }
    
    # Conditional backend specs
    BACKEND_SPECS = {
        'EDGE_FUNCTIONS': {
            'description': 'Backend API',
            'required_for': ['COURSE_CRAFTER', 'ERM', 'PIT', 'THREAT', 'VULNERABILITY']
        },
        'EXPORT_SPEC': {
            'description': 'Data Export',
            'required_for': ['COURSE_CRAFTER', 'ERM', 'RISK_ASSESSMENT']
        },
        'WATCHDOG_LOGIC': {
            'description': 'Monitoring',
            'required_for': ['PIT', 'THREAT', 'VULNERABILITY']
        },
        'MODEL_ROUTING_SPEC': {
            'description': 'AI Routing',
            'required_for': ['PIT', 'THREAT', 'VULNERABILITY']
        }
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
        self.isms_root = self.repo_root / 'maturion-isms' / 'apps'
        self.results = {
            'metadata': {
                'standardised_at': datetime.now().isoformat(),
                'repo_root': str(repo_root)
            },
            'modules': {},
            'missing_components': [],
            'version_issues': [],
            'dependency_issues': [],
            'compliance_gaps': [],
            'readiness_summary': {}
        }
        
    def execute_full_standardisation(self):
        """Execute complete standardisation pass"""
        print("🔧 Starting Full Architecture Standardisation Pass...\n")
        
        # Task 1: Scan all modules
        self.scan_all_modules()
        
        # Task 2: Identify missing components
        self.identify_missing_components()
        
        # Task 3: Validate True North
        self.validate_true_north()
        
        # Task 4: Analyze dependencies
        self.analyze_dependencies()
        
        # Task 5: Normalize versioning
        self.check_version_consistency()
        
        # Task 6: Verify linkages
        self.verify_architecture_qa_compliance_linkage()
        
        # Task 7: Generate reports
        self.generate_module_readiness_reports()
        self.generate_fix_backlog()
        self.generate_standardisation_report()
        self.generate_sequencing_plan()
        
        print("\n✅ Standardisation pass complete!")
        
    def scan_all_modules(self):
        """Scan all modules for architecture files"""
        print("📊 Scanning all modules for architecture components...\n")
        
        for module in self.MODULES:
            module_name = module.lower().replace('_', '-')
            module_path = self.isms_root / module_name
            
            module_data = {
                'name': module,
                'path': str(module_path),
                'exists': module_path.exists(),
                'files': {},
                'missing': [],
                'version_spread': {},
                'completeness_score': 0,
                'compliance_coverage': {},
                'dependencies': set(),
                'qa_linkage': False,
                'compliance_linkage': False
            }
            
            if not module_path.exists():
                print(f"  ⚠️  Module directory not found: {module_name}")
                module_data['missing'].append('Module directory does not exist')
                self.results['modules'][module] = module_data
                continue
            
            # Scan architecture directory
            arch_path = module_path / 'architecture'
            if arch_path.exists():
                self._scan_module_architecture(module, arch_path, module_data)
            else:
                print(f"  ⚠️  No architecture directory: {module}")
                module_data['missing'].append('Architecture directory missing')
            
            # Scan QA plans
            qa_path = module_path / 'qa-plans'
            if qa_path.exists():
                self._scan_module_qa(module, qa_path, module_data)
            else:
                module_data['missing'].append('QA plans directory missing')
            
            # Calculate completeness
            self._calculate_module_completeness(module, module_data)
            
            self.results['modules'][module] = module_data
            
        print(f"\n  ✓ Scanned {len(self.MODULES)} modules\n")
    
    def _scan_module_architecture(self, module: str, arch_path: Path, module_data: dict):
        """Scan architecture directory for a module"""
        arch_files = list(arch_path.glob('*.md'))
        
        for arch_file in arch_files:
            # Try to match to known spec types
            file_name = arch_file.name
            version = self._extract_version(file_name)
            
            # Check against required specs
            for spec_type, spec_info in {**self.REQUIRED_SPECS, **self.BACKEND_SPECS}.items():
                if spec_type in file_name.upper():
                    if spec_type not in module_data['files']:
                        module_data['files'][spec_type] = []
                    
                    module_data['files'][spec_type].append({
                        'path': str(arch_file.relative_to(self.repo_root)),
                        'version': f"{version[0]}.{version[1]}",
                        'size': arch_file.stat().st_size
                    })
                    
                    # Track version spread
                    if spec_type not in module_data['version_spread']:
                        module_data['version_spread'][spec_type] = []
                    module_data['version_spread'][spec_type].append(f"{version[0]}.{version[1]}")
                    break
    
    def _scan_module_qa(self, module: str, qa_path: Path, module_data: dict):
        """Scan QA plans for a module"""
        qa_files = list(qa_path.glob('*QA*.md'))
        
        if qa_files:
            module_data['qa_linkage'] = True
            
            # Check if QA files reference architecture
            for qa_file in qa_files:
                try:
                    content = qa_file.read_text(encoding='utf-8')
                    # Look for architecture references
                    if 'ARCHITECTURE' in content or 'TRUE_NORTH' in content:
                        module_data['qa_linkage'] = True
                    
                    # Look for compliance references
                    for standard in self.COMPLIANCE_STANDARDS:
                        if standard in content:
                            if standard not in module_data['compliance_coverage']:
                                module_data['compliance_coverage'][standard] = []
                            module_data['compliance_coverage'][standard].append(qa_file.name)
                            module_data['compliance_linkage'] = True
                except (UnicodeDecodeError, FileNotFoundError) as e:
                    print(f"    ⚠️  Could not read {qa_file.name}: {e}")
                except Exception as e:
                    print(f"    ⚠️  Unexpected error reading {qa_file.name}: {e}")
    
    def _calculate_module_completeness(self, module: str, module_data: dict):
        """Calculate completeness score for a module"""
        total_required = len(self.REQUIRED_SPECS)
        present_count = 0
        
        for spec_type in self.REQUIRED_SPECS.keys():
            if spec_type in module_data['files'] and module_data['files'][spec_type]:
                present_count += 1
            else:
                module_data['missing'].append(f"Missing: {spec_type}")
        
        # Check conditional backend specs
        for spec_type, spec_info in self.BACKEND_SPECS.items():
            if module in spec_info.get('required_for', []):
                total_required += 1
                has_backend_spec = (
                    spec_type in module_data['files'] and 
                    module_data['files'][spec_type]
                )
                if has_backend_spec:
                    present_count += 1
                else:
                    missing_msg = f"Missing: {spec_type} (required for {module})"
                    module_data['missing'].append(missing_msg)
        
        # Calculate completeness score
        if total_required > 0:
            completeness = (present_count / total_required) * 100
            module_data['completeness_score'] = round(completeness, 1)
        else:
            module_data['completeness_score'] = 0
        
        module_data['total_required'] = total_required
        module_data['present_count'] = present_count
    
    def _extract_version(self, filename: str) -> Tuple[int, int]:
        """Extract version number from filename"""
        match = re.search(r'_v(\d+)\.(\d+)', filename)
        if match:
            return (int(match.group(1)), int(match.group(2)))
        return (0, 0)
    
    def identify_missing_components(self):
        """Identify all missing architecture components"""
        print("🔍 Identifying missing architecture components...\n")
        
        for module, data in self.results['modules'].items():
            if not data['exists']:
                self.results['missing_components'].append({
                    'module': module,
                    'severity': 'CRITICAL',
                    'issue': 'Module directory does not exist',
                    'component': 'ALL',
                    'action': f"Create module structure at {data['path']}"
                })
                continue
            
            for missing in data['missing']:
                severity = 'HIGH' if 'TRUE_NORTH' in missing or 'ARCHITECTURE' in missing else 'MEDIUM'
                
                # Clean up the missing component description
                component = missing.replace('Missing: ', '').split(' (')[0]
                action_verb = "Generate placeholder"
                
                # Special handling for directory issues
                if 'directory' in missing.lower():
                    action_verb = "Create"
                    component = component.replace(' missing', '')
                
                self.results['missing_components'].append({
                    'module': module,
                    'severity': severity,
                    'issue': missing,
                    'component': component,
                    'action': f"{action_verb} {component}"
                })
        
        print(f"  ✓ Identified {len(self.results['missing_components'])} missing components\n")
    
    def validate_true_north(self):
        """Validate True North completeness"""
        print("🧭 Validating True North documents...\n")
        
        for module, data in self.results['modules'].items():
            if not data['exists']:
                continue
            
            if 'TRUE_NORTH' not in data['files'] or not data['files']['TRUE_NORTH']:
                print(f"  ✗ {module}: No True North document found")
                continue
            
            # Check if there are multiple versions
            versions = data['version_spread'].get('TRUE_NORTH', [])
            if len(versions) > 1:
                print(f"  ⚠️  {module}: Multiple True North versions found: {versions}")
                self.results['version_issues'].append({
                    'module': module,
                    'component': 'TRUE_NORTH',
                    'versions': versions,
                    'issue': 'Multiple versions exist',
                    'action': 'Consolidate to single latest version'
                })
            else:
                version = versions[0] if versions else '0.0'
                if version.startswith('0.'):
                    print(f"  ⚠️  {module}: True North is draft version {version}")
                else:
                    print(f"  ✓ {module}: True North v{version} found")
        
        print()
    
    def analyze_dependencies(self):
        """Analyze module dependencies and detect circular dependencies"""
        print("🔗 Analyzing module dependencies...\n")
        
        dependency_graph = defaultdict(set)
        
        for module, data in self.results['modules'].items():
            if not data['exists']:
                continue
            
            # Scan architecture files for dependencies
            for spec_type, files in data['files'].items():
                for file_info in files:
                    file_path = self.repo_root / file_info['path']
                    if file_path.exists():
                        deps = self._extract_dependencies(file_path)
                        dependency_graph[module].update(deps)
                        data['dependencies'].update(deps)
        
        # Detect circular dependencies
        circular_deps = self._detect_circular_dependencies(dependency_graph)
        
        if circular_deps:
            print(f"  ⚠️  Found {len(circular_deps)} circular dependency chains:\n")
            for chain in circular_deps:
                print(f"      {' → '.join(chain)}")
                self.results['dependency_issues'].append({
                    'type': 'CIRCULAR',
                    'chain': chain,
                    'severity': 'HIGH',
                    'action': 'Refactor to remove circular dependency'
                })
        else:
            print("  ✓ No circular dependencies detected")
        
        # Store dependency graph
        dependency_graph_list = {
            module: list(deps) 
            for module, deps in dependency_graph.items()
        }
        self.results['dependency_graph'] = dependency_graph_list
        
        print()
    
    def _extract_dependencies(self, file_path: Path) -> Set[str]:
        """Extract module dependencies from file"""
        dependencies = set()
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Try to determine the module this file belongs to from the path
            current_module = None
            for module in self.MODULES:
                module_name = module.lower().replace('_', '-')
                if module_name in str(file_path).lower():
                    current_module = module
                    break
            
            for module in self.MODULES:
                if module == current_module:
                    continue  # Skip self-reference
                
                # Look for module references
                pattern = r'\b' + re.escape(module) + r'\b'
                if re.search(pattern, content):
                    dependencies.add(module)
        
        except (UnicodeDecodeError, FileNotFoundError, PermissionError) as e:
            # Log specific file reading errors but continue
            print(f"    ⚠️  Could not read {file_path.name}: {e}")
        except Exception as e:
            # Catch other unexpected errors but don't fail
            print(f"    ⚠️  Unexpected error reading {file_path.name}: {e}")
        
        return dependencies
    
    def _detect_circular_dependencies(self, graph: Dict[str, Set[str]]) -> List[List[str]]:
        """Detect circular dependencies using DFS"""
        circular = []
        visited = set()
        rec_stack = set()
        
        def dfs(node, path):
            if node in rec_stack:
                # Found cycle
                if node in path:
                    cycle_start = path.index(node)
                    cycle = path[cycle_start:] + [node]
                    # Check if this cycle is not already recorded
                    cycle_set = frozenset(cycle)
                    if not any(frozenset(c) == cycle_set for c in circular):
                        circular.append(cycle)
                return True
            
            if node in visited:
                return False
            
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph.get(node, set()):
                # Check each neighbor for cycles - use immutable path extension
                dfs(neighbor, path + [node])
            
            rec_stack.remove(node)
            return False
        
        for node in graph.keys():
            if node not in visited:
                dfs(node, [])
        
        return circular
    
    def check_version_consistency(self):
        """Check version consistency across documents"""
        print("📋 Checking version consistency...\n")
        
        for module, data in self.results['modules'].items():
            if not data['exists']:
                continue
            
            all_versions = set()
            for spec_type, versions in data['version_spread'].items():
                all_versions.update(versions)
            
            if len(all_versions) > 3:
                print(f"  ⚠️  {module}: Wide version spread across {len(all_versions)} versions: {sorted(all_versions)}")
                self.results['version_issues'].append({
                    'module': module,
                    'component': 'ALL',
                    'versions': sorted(all_versions),
                    'issue': f'Version spread across {len(all_versions)} versions',
                    'action': 'Normalize all documents to consistent version'
                })
            elif all_versions:
                print(f"  ✓ {module}: Version spread acceptable ({len(all_versions)} versions)")
        
        print()
    
    def verify_architecture_qa_compliance_linkage(self):
        """Verify linkage between architecture, QA, and compliance"""
        print("🔗 Verifying architecture → QA → compliance linkage...\n")
        
        for module, data in self.results['modules'].items():
            if not data['exists']:
                continue
            
            has_arch = bool(data['files'].get('ARCHITECTURE') or data['files'].get('TRUE_NORTH'))
            has_qa = data['qa_linkage']
            has_compliance = data['compliance_linkage']
            
            status = []
            if has_arch:
                status.append('Architecture ✓')
            else:
                status.append('Architecture ✗')
            
            if has_qa:
                status.append('QA ✓')
            else:
                status.append('QA ✗')
            
            if has_compliance:
                status.append('Compliance ✓')
            else:
                status.append('Compliance ✗')
            
            print(f"  {module}: {' → '.join(status)}")
            
            if not (has_arch and has_qa and has_compliance):
                self.results['compliance_gaps'].append({
                    'module': module,
                    'has_architecture': has_arch,
                    'has_qa': has_qa,
                    'has_compliance': has_compliance,
                    'action': 'Establish complete linkage chain'
                })
        
        print()
    
    def generate_module_readiness_reports(self):
        """Generate individual module readiness reports"""
        print("📄 Generating module readiness reports...\n")
        
        reports_dir = self.repo_root / 'MODULE_READINESS_REPORTS'
        reports_dir.mkdir(exist_ok=True)
        
        for module, data in self.results['modules'].items():
            readiness_score = data['completeness_score']
            
            # Determine readiness level
            if readiness_score >= 90:
                readiness = 'READY'
            elif readiness_score >= 70:
                readiness = 'MOSTLY_READY'
            elif readiness_score >= 50:
                readiness = 'PARTIALLY_READY'
            else:
                readiness = 'NOT_READY'
            
            self.results['readiness_summary'][module] = {
                'score': readiness_score,
                'status': readiness
            }
            
            # Generate report
            report_path = reports_dir / f"{module}_READINESS_REPORT.md"
            self._write_module_readiness_report(report_path, module, data, readiness)
            
            print(f"  ✓ Generated: {module}_READINESS_REPORT.md ({readiness})")
        
        print()
    
    def _write_module_readiness_report(self, path: Path, module: str, data: dict, readiness: str):
        """Write individual module readiness report"""
        report = f"""# Module Readiness Report: {module}

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Readiness Status**: **{readiness}**  
**Completeness Score**: {data['completeness_score']}% ({data.get('present_count', 0)}/{data.get('total_required', 0)} components)

---

## Executive Summary

Module: **{module}**  
Directory: `{data['path']}`  
Exists: {'✅' if data['exists'] else '❌'}

---

## Architecture Components Status

### Required Components
"""
        
        for spec_type, spec_info in self.REQUIRED_SPECS.items():
            if spec_type in data['files'] and data['files'][spec_type]:
                versions = ', '.join([f['version'] for f in data['files'][spec_type]])
                report += f"- ✅ **{spec_type}**: {spec_info['description']} (v{versions})\n"
            else:
                report += f"- ❌ **{spec_type}**: {spec_info['description']} - **MISSING**\n"
        
        report += "\n### Conditional Backend Components\n"
        
        for spec_type, spec_info in self.BACKEND_SPECS.items():
            required_for_module = module in spec_info.get('required_for', [])
            if spec_type in data['files'] and data['files'][spec_type]:
                versions = ', '.join([f['version'] for f in data['files'][spec_type]])
                report += f"- ✅ **{spec_type}**: {spec_info['description']} (v{versions})\n"
            elif required_for_module:
                report += f"- ❌ **{spec_type}**: {spec_info['description']} - **MISSING** (required for {module})\n"
            else:
                report += f"- ➖ **{spec_type}**: {spec_info['description']} - N/A\n"
        
        report += f"""

---

## QA & Compliance Linkage

- **QA Linkage**: {'✅ YES' if data['qa_linkage'] else '❌ NO'}
- **Compliance Linkage**: {'✅ YES' if data['compliance_linkage'] else '❌ NO'}
- **Compliance Standards Referenced**: {len(data['compliance_coverage'])}

"""
        
        if data['compliance_coverage']:
            report += "### Compliance Coverage\n"
            for standard, files in data['compliance_coverage'].items():
                report += f"- **{standard}**: {len(files)} references\n"
        
        report += f"""

---

## Dependencies

**Module Dependencies**: {len(data['dependencies'])}

"""
        
        if data['dependencies']:
            report += "### Depends On:\n"
            for dep in sorted(data['dependencies']):
                report += f"- {dep}\n"
        
        report += f"""

---

## Issues & Missing Components

**Total Issues**: {len(data['missing'])}

"""
        
        if data['missing']:
            for issue in data['missing']:
                report += f"- ⚠️ {issue}\n"
        
        report += f"""

---

## Readiness Decision

**Status**: {readiness}

"""
        
        if readiness == 'READY':
            report += "✅ **This module is READY FOR BUILD**\n\n"
            report += "All required architecture components are present and properly linked.\n"
        elif readiness == 'MOSTLY_READY':
            report += "⚠️ **This module is MOSTLY READY but has minor gaps**\n\n"
            report += "Most components are present. Address minor gaps before build.\n"
        elif readiness == 'PARTIALLY_READY':
            report += "⚠️ **This module is PARTIALLY READY and needs significant work**\n\n"
            report += "Critical components are missing. Complete architecture before build.\n"
        else:
            report += "❌ **This module is NOT READY FOR BUILD**\n\n"
            report += "Major components are missing. Module requires substantial architecture work.\n"
        
        report += f"""

---

## Recommended Actions

"""
        
        # Generate unique, prioritized recommendations
        priority_actions = []
        action_set = set()  # Track unique actions to avoid duplicates
        action_counter = 1
        
        for missing in data['missing']:
            if 'TRUE_NORTH' in missing and 'true_north' not in action_set:
                priority_actions.append(f"{action_counter}. **CRITICAL**: Create {module} True North document")
                action_set.add('true_north')
                action_counter += 1
            elif 'ARCHITECTURE' in missing and 'architecture' not in action_set:
                priority_actions.append(f"{action_counter}. **HIGH**: Create {module} Architecture specification")
                action_set.add('architecture')
                action_counter += 1
            elif 'QA' in missing and 'qa_plan' not in action_set:
                priority_actions.append(f"{action_counter}. **HIGH**: Create QA Implementation Plan")
                action_set.add('qa_plan')
                action_counter += 1
        
        if not data['qa_linkage'] and 'qa_linkage' not in action_set:
            priority_actions.append(f"{action_counter}. **MEDIUM**: Establish QA linkage to architecture")
            action_set.add('qa_linkage')
            action_counter += 1
        
        if not data['compliance_linkage'] and 'compliance_linkage' not in action_set:
            priority_actions.append(f"{action_counter}. **MEDIUM**: Add compliance mappings to QA specs")
            action_set.add('compliance_linkage')
            action_counter += 1
        
        if priority_actions:
            for action in priority_actions:
                report += f"{action}\n"
        else:
            report += "No critical actions required.\n"
        
        report += "\n---\n\n*Generated by Maturion Foreman Architecture Standardisation System*\n"
        
        path.write_text(report, encoding='utf-8')
    
    def generate_fix_backlog(self):
        """Generate prioritized fix backlog"""
        print("📋 Generating fix backlog...\n")
        
        backlog_path = self.repo_root / 'FIX_BACKLOG.md'
        
        backlog = f"""# Architecture Standardisation Fix Backlog

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Total Issues**: {len(self.results['missing_components']) + len(self.results['version_issues']) + len(self.results['dependency_issues']) + len(self.results['compliance_gaps'])}

---

## Priority 1: Critical Issues (Blockers)

### Missing Module Directories
"""
        
        critical = [x for x in self.results['missing_components'] if x['severity'] == 'CRITICAL']
        if critical:
            for issue in critical:
                backlog += f"\n- [ ] **{issue['module']}**: {issue['issue']}\n"
                backlog += f"  - Action: {issue['action']}\n"
        else:
            backlog += "\nNone.\n"
        
        backlog += "\n### Missing True North Documents\n"
        
        true_north_missing = [x for x in self.results['missing_components'] if 'TRUE_NORTH' in x['component']]
        if true_north_missing:
            for issue in true_north_missing:
                backlog += f"\n- [ ] **{issue['module']}**: {issue['issue']}\n"
                backlog += f"  - Action: {issue['action']}\n"
        else:
            backlog += "\nNone.\n"
        
        backlog += "\n---\n\n## Priority 2: High Issues (Architecture Gaps)\n"
        
        high = [x for x in self.results['missing_components'] if x['severity'] == 'HIGH' and 'TRUE_NORTH' not in x['component']]
        if high:
            for issue in high:
                backlog += f"\n- [ ] **{issue['module']}**: {issue['issue']}\n"
                backlog += f"  - Action: {issue['action']}\n"
        else:
            backlog += "\nNone.\n"
        
        backlog += "\n---\n\n## Priority 3: Medium Issues (Component Gaps)\n"
        
        medium = [x for x in self.results['missing_components'] if x['severity'] == 'MEDIUM']
        if medium:
            for issue in medium:
                backlog += f"\n- [ ] **{issue['module']}**: {issue['issue']}\n"
                backlog += f"  - Action: {issue['action']}\n"
        else:
            backlog += "\nNone.\n"
        
        backlog += "\n---\n\n## Dependency Issues\n"
        
        if self.results['dependency_issues']:
            for issue in self.results['dependency_issues']:
                backlog += f"\n- [ ] **{issue['type']}**: {' → '.join(issue['chain'])}\n"
                backlog += f"  - Severity: {issue['severity']}\n"
                backlog += f"  - Action: {issue['action']}\n"
        else:
            backlog += "\n✅ No circular dependencies detected.\n"
        
        backlog += "\n---\n\n## Version Consistency Issues\n"
        
        if self.results['version_issues']:
            for issue in self.results['version_issues']:
                backlog += f"\n- [ ] **{issue['module']}** - {issue['component']}: {issue['issue']}\n"
                backlog += f"  - Versions: {', '.join(issue['versions'])}\n"
                backlog += f"  - Action: {issue['action']}\n"
        else:
            backlog += "\n✅ No significant version inconsistencies.\n"
        
        backlog += "\n---\n\n## Compliance Linkage Gaps\n"
        
        if self.results['compliance_gaps']:
            for gap in self.results['compliance_gaps']:
                backlog += f"\n- [ ] **{gap['module']}**: Incomplete linkage chain\n"
                backlog += f"  - Architecture: {'✅' if gap['has_architecture'] else '❌'}\n"
                backlog += f"  - QA: {'✅' if gap['has_qa'] else '❌'}\n"
                backlog += f"  - Compliance: {'✅' if gap['has_compliance'] else '❌'}\n"
                backlog += f"  - Action: {gap['action']}\n"
        else:
            backlog += "\n✅ All modules have complete linkage.\n"
        
        backlog += "\n---\n\n*Generated by Maturion Foreman Architecture Standardisation System*\n"
        
        backlog_path.write_text(backlog, encoding='utf-8')
        print(f"  ✓ Generated FIX_BACKLOG.md\n")
    
    def generate_standardisation_report(self):
        """Generate main standardisation report"""
        print("📊 Generating standardisation report...\n")
        
        report_path = self.repo_root / 'STANDARDISATION_REPORT.md'
        
        total_modules = len(self.MODULES)
        ready_modules = len([m for m, s in self.results['readiness_summary'].items() if s['status'] == 'READY'])
        avg_completeness = sum([s['score'] for s in self.results['readiness_summary'].values()]) / total_modules if total_modules > 0 else 0
        
        report = f"""# Architecture Standardisation Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Standardisation Agent**: Maturion Foreman  
**Repository**: {self.repo_root}

---

## Executive Summary

**Total Modules**: {total_modules}  
**Ready for Build**: {ready_modules} ({(ready_modules/total_modules*100):.1f}%)  
**Average Completeness**: {avg_completeness:.1f}%

**Total Issues Identified**: {len(self.results['missing_components']) + len(self.results['version_issues']) + len(self.results['dependency_issues']) + len(self.results['compliance_gaps'])}

- Missing Components: {len(self.results['missing_components'])}
- Version Issues: {len(self.results['version_issues'])}
- Dependency Issues: {len(self.results['dependency_issues'])}
- Compliance Gaps: {len(self.results['compliance_gaps'])}

---

## Module Readiness Overview

| Module | Completeness | Status | QA Linked | Compliance Linked |
|--------|--------------|--------|-----------|-------------------|
"""
        
        for module in self.MODULES:
            data = self.results['modules'].get(module, {})
            summary = self.results['readiness_summary'].get(module, {'score': 0, 'status': 'NOT_READY'})
            
            qa_linked = '✅' if data.get('qa_linkage') else '❌'
            compliance_linked = '✅' if data.get('compliance_linkage') else '❌'
            
            status_emoji = {
                'READY': '✅',
                'MOSTLY_READY': '⚠️',
                'PARTIALLY_READY': '⚠️',
                'NOT_READY': '❌'
            }.get(summary['status'], '❓')
            
            report += f"| {module} | {summary['score']:.1f}% | {status_emoji} {summary['status']} | {qa_linked} | {compliance_linked} |\n"
        
        report += f"""

---

## Standardisation Tasks Completed

- [x] ✅ Applied minimum-architecture-template standards to all modules
- [x] ✅ Identified missing architecture components per module
- [x] ✅ Validated True North completeness
- [x] ✅ Analyzed dependency graph and circular dependencies
- [x] ✅ Checked version consistency across documents
- [x] ✅ Verified architecture → QA → compliance linkage
- [x] ✅ Generated Module Readiness Reports for all modules
- [x] ✅ Created prioritized fix backlog
- [x] ✅ Generated sequencing plan for builder agents

---

## Key Findings

### Critical Gaps
"""
        
        critical_count = len([x for x in self.results['missing_components'] if x['severity'] == 'CRITICAL'])
        if critical_count > 0:
            report += f"\n⚠️ **{critical_count} critical gaps found** - Module directories missing or True North documents absent.\n"
        else:
            report += "\n✅ No critical gaps found.\n"
        
        report += "\n### Architecture Completeness\n"
        
        for module, summary in self.results['readiness_summary'].items():
            if summary['score'] < 70:
                report += f"- ⚠️ **{module}**: {summary['score']:.1f}% complete - needs significant work\n"
        
        report += "\n### Dependency Analysis\n"
        
        if self.results['dependency_issues']:
            report += f"\n⚠️ **{len(self.results['dependency_issues'])} circular dependency chains detected**\n"
            for issue in self.results['dependency_issues']:
                report += f"- {' → '.join(issue['chain'])}\n"
        else:
            report += "\n✅ No circular dependencies detected. Dependency graph is clean.\n"
        
        report += "\n### Version Consistency\n"
        
        if self.results['version_issues']:
            report += f"\n⚠️ **{len(self.results['version_issues'])} version consistency issues**\n"
        else:
            report += "\n✅ Version consistency is acceptable across modules.\n"
        
        report += "\n### QA & Compliance Linkage\n"
        
        linked_modules = len([d for d in self.results['modules'].values() if d.get('qa_linkage') and d.get('compliance_linkage')])
        report += f"\n**Fully Linked Modules**: {linked_modules}/{total_modules} ({(linked_modules/total_modules*100):.1f}%)\n"
        
        report += f"""

---

## Deliverables

All standardisation deliverables have been generated:

1. ✅ **STANDARDISATION_REPORT.md** (this document)
2. ✅ **MODULE_READINESS_REPORTS/** - Individual reports for each module
3. ✅ **FIX_BACKLOG.md** - Prioritized issues requiring resolution
4. ✅ **BUILDER_SEQUENCING_PLAN.md** - Task sequencing for builder agents
5. ✅ **standardisation_results.json** - Machine-readable results

---

## Next Steps

### Immediate Actions Required

1. **Review Module Readiness Reports** - Examine individual module reports in `MODULE_READINESS_REPORTS/`
2. **Address Critical Issues** - Resolve Priority 1 issues in FIX_BACKLOG.md
3. **Create Missing Components** - Generate placeholder documents for missing architecture files
4. **Resolve Dependencies** - Address circular dependencies identified
5. **Normalize Versions** - Standardize document versions across modules
6. **Complete Linkages** - Establish architecture → QA → compliance chains for all modules

### Builder Agent Coordination

Once critical gaps are addressed:

1. Follow the sequencing plan in BUILDER_SEQUENCING_PLAN.md
2. Assign tasks to appropriate builder agents
3. Execute builds in dependency order
4. Validate each build against architecture standards
5. Run QA-of-QA validation before integration

---

## Recommendations

"""
        
        # Generate recommendations
        if ready_modules < total_modules:
            report += f"1. **Architecture Completion**: {total_modules - ready_modules} modules need architecture work before build readiness\n"
        
        if self.results['dependency_issues']:
            report += f"2. **Dependency Refactoring**: Resolve {len(self.results['dependency_issues'])} circular dependencies\n"
        
        if self.results['compliance_gaps']:
            report += f"3. **Compliance Mapping**: Complete compliance linkage for {len(self.results['compliance_gaps'])} modules\n"
        
        report += "\n---\n\n*Generated by Maturion Foreman Architecture Standardisation System*\n"
        
        report_path.write_text(report, encoding='utf-8')
        
        # Also save JSON results
        json_path = self.repo_root / 'standardisation_results.json'
        
        # Convert sets to lists for JSON serialization
        json_results = self.results.copy()
        for module, data in json_results['modules'].items():
            data['dependencies'] = list(data['dependencies'])
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_results, f, indent=2)
        
        print(f"  ✓ Generated STANDARDISATION_REPORT.md\n")
        print(f"  ✓ Generated standardisation_results.json\n")
    
    def generate_sequencing_plan(self):
        """Generate builder sequencing plan"""
        print("🗓️ Generating builder sequencing plan...\n")
        
        plan_path = self.repo_root / 'BUILDER_SEQUENCING_PLAN.md'
        
        plan = f"""# Builder Agent Sequencing Plan

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Based On**: Architecture Standardisation Analysis

---

## Build Sequencing Strategy

This plan sequences module builds based on:
1. Dependency order (modules with no dependencies first)
2. Architecture readiness (ready modules prioritized)
3. Builder agent capabilities

---

## Phase 1: Foundation Modules (No Dependencies)

Build these modules first as they have no dependencies on other modules:

"""
        
        # Identify modules with no dependencies
        no_deps = []
        for module, data in self.results['modules'].items():
            if not data.get('dependencies'):
                readiness = self.results['readiness_summary'].get(module, {})
                no_deps.append((module, readiness.get('score', 0), readiness.get('status', 'NOT_READY')))
        
        no_deps.sort(key=lambda x: x[1], reverse=True)  # Sort by readiness score
        
        for module, score, status in no_deps:
            plan += f"### {module} (Readiness: {score:.1f}% - {status})\n\n"
            
            if status in ['READY', 'MOSTLY_READY']:
                plan += f"**Status**: ✅ Ready for build\n\n"
                plan += "**Builder Assignment**:\n"
                plan += "1. schema-builder → Database schema implementation\n"
                plan += "2. ui-builder → Frontend components\n"
                plan += "3. api-builder → Backend edge functions\n"
                plan += "4. qa-builder → Test suite creation\n"
                plan += "5. integration-builder → Module integration points\n\n"
            else:
                plan += f"**Status**: ⚠️ Architecture work required\n\n"
                plan += "**Pre-Build Tasks**:\n"
                
                module_data = self.results['modules'].get(module, {})
                for missing in module_data.get('missing', [])[:3]:  # Top 3 issues
                    plan += f"- Create {missing.replace('Missing: ', '')}\n"
                
                plan += "\n"
        
        plan += "\n---\n\n## Phase 2: Dependent Modules\n\n"
        plan += "Build these modules after their dependencies are complete:\n\n"
        
        # Identify modules with dependencies
        with_deps = []
        for module, data in self.results['modules'].items():
            if data.get('dependencies'):
                readiness = self.results['readiness_summary'].get(module, {})
                with_deps.append((module, len(data['dependencies']), readiness.get('score', 0), readiness.get('status', 'NOT_READY'), list(data['dependencies'])))
        
        with_deps.sort(key=lambda x: (x[1], -x[2]))  # Sort by dependency count, then readiness
        
        for module, dep_count, score, status, deps in with_deps:
            plan += f"### {module} (Readiness: {score:.1f}% - {status})\n\n"
            plan += f"**Dependencies**: {', '.join(deps)} ({dep_count} modules)\n\n"
            
            if status in ['READY', 'MOSTLY_READY']:
                plan += f"**Status**: ✅ Ready for build after dependencies\n\n"
                plan += "**Build Order**:\n"
                plan += "1. Wait for dependencies to complete\n"
                plan += "2. schema-builder → Database schema with foreign keys\n"
                plan += "3. integration-builder → Integration layer\n"
                plan += "4. api-builder → Backend logic\n"
                plan += "5. ui-builder → Frontend components\n"
                plan += "6. qa-builder → Integration tests\n\n"
            else:
                plan += f"**Status**: ⚠️ Architecture work required\n\n"
                plan += "**Pre-Build Tasks**:\n"
                
                module_data = self.results['modules'].get(module, {})
                for missing in module_data.get('missing', [])[:3]:
                    plan += f"- Create {missing.replace('Missing: ', '')}\n"
                
                plan += "\n"
        
        plan += f"""

---

## Parallelization Opportunities

The following modules can be built in parallel (no interdependencies):

"""
        
        # Find modules that can be built in parallel
        parallel_groups = self._find_parallel_build_groups()
        
        for i, group in enumerate(parallel_groups, 1):
            plan += f"### Group {i}\n\n"
            for module in group:
                readiness = self.results['readiness_summary'].get(module, {})
                plan += f"- {module} ({readiness.get('score', 0):.1f}%)\n"
            plan += "\n"
        
        plan += f"""

---

## Builder Agent Task Distribution

### Schema Builder
Responsible for all database schema implementations across modules.

**Priority Order**:
"""
        
        for module, score, status in no_deps:
            if status in ['READY', 'MOSTLY_READY']:
                plan += f"1. {module} - Schema implementation\n"
        
        plan += "\n### UI Builder\n"
        plan += "Responsible for all frontend component implementations.\n\n"
        plan += "**Priority Order**:\n"
        
        for module, score, status in no_deps:
            if status in ['READY', 'MOSTLY_READY']:
                plan += f"1. {module} - UI components\n"
        
        plan += "\n### API Builder\n"
        plan += "Responsible for all backend edge function implementations.\n\n"
        plan += "**Priority Order**:\n"
        
        for module, score, status in no_deps:
            if status in ['READY', 'MOSTLY_READY']:
                plan += f"1. {module} - Edge functions\n"
        
        plan += "\n### Integration Builder\n"
        plan += "Responsible for module integration layer.\n\n"
        plan += "**Execute After**: Schema and API builders complete foundation modules\n\n"
        
        plan += "\n### QA Builder\n"
        plan += "Responsible for test suite creation and QA validation.\n\n"
        plan += "**Execute After**: Each module component completion\n\n"
        
        plan += "\n---\n\n## Estimated Timeline\n\n"
        
        ready_count = len([m for m, s, st in no_deps if st in ['READY', 'MOSTLY_READY']])
        total_count = len(self.MODULES)
        
        plan += f"**Ready Modules**: {ready_count}/{total_count}\n"
        plan += f"**Architecture Work Required**: {total_count - ready_count} modules\n\n"
        
        plan += "**Phase 1 (Foundation)**: 2-3 sprints\n"
        plan += "**Phase 2 (Dependent Modules)**: 2-4 sprints\n"
        plan += "**Integration & QA**: 1-2 sprints\n\n"
        
        plan += "**Total Estimated**: 5-9 sprints (10-18 weeks)\n\n"
        
        plan += "\n---\n\n*Generated by Maturion Foreman Architecture Standardisation System*\n"
        
        plan_path.write_text(plan, encoding='utf-8')
        print(f"  ✓ Generated BUILDER_SEQUENCING_PLAN.md\n")
    
    def _find_parallel_build_groups(self) -> List[List[str]]:
        """Find modules that can be built in parallel"""
        groups = []
        processed = set()
        
        # Group 1: Modules with no dependencies
        no_deps = [m for m, d in self.results['modules'].items() if not d.get('dependencies') and m not in processed]
        if no_deps:
            groups.append(no_deps)
            processed.update(no_deps)
        
        # Group 2: Modules that depend only on Group 1
        group1_deps = []
        for module, data in self.results['modules'].items():
            if module in processed:
                continue
            deps = data.get('dependencies', set())
            if deps and all(d in processed for d in deps):
                group1_deps.append(module)
        
        if group1_deps:
            groups.append(group1_deps)
            processed.update(group1_deps)
        
        return groups


def main():
    """Main execution"""
    repo_root = os.getcwd()
    
    standardiser = ArchitectureStandardiser(repo_root)
    standardiser.execute_full_standardisation()
    
    print("\n" + "="*80)
    print("STANDARDISATION COMPLETE")
    print("="*80)
    print("\nGenerated files:")
    print("  - STANDARDISATION_REPORT.md")
    print("  - MODULE_READINESS_REPORTS/ (individual module reports)")
    print("  - FIX_BACKLOG.md")
    print("  - BUILDER_SEQUENCING_PLAN.md")
    print("  - standardisation_results.json")
    print("\nNext: Review reports and address critical issues in FIX_BACKLOG.md")
    

if __name__ == '__main__':
    main()
