#!/usr/bin/env python3
"""
Maturion AI Foreman - Runtime Context Export System
Exports architecture, compliance, and governance data to runtime-ready JSON bundles
"""

import json
import os
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime
import re


class RuntimeContextExporter:
    """Export build-time context to runtime-ready JSON bundles"""
    
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
        'RISK_VULNERABILITY'
    ]
    
    # Compliance standards
    COMPLIANCE_STANDARDS = {
        'ISO_27001': 'ISO/IEC 27001:2022 - Information Security Management',
        'ISO_27005': 'ISO/IEC 27005:2022 - Information Security Risk Management',
        'ISO_31000': 'ISO 31000:2018 - Risk Management Guidelines',
        'ISO_22301': 'ISO 22301:2019 - Business Continuity Management',
        'NIST_CSF': 'NIST Cybersecurity Framework',
        'NIST_800_53': 'NIST SP 800-53 - Security and Privacy Controls',
        'COBIT': 'COBIT 2019 - Control Objectives for Information Technologies',
        'GDPR': 'General Data Protection Regulation',
        'POPIA': 'Protection of Personal Information Act',
        'OWASP_ASVS': 'OWASP Application Security Verification Standard',
        'OWASP_TOP_10': 'OWASP Top 10 Web Application Security Risks'
    }
    
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.foreman_path = self.repo_root / 'foreman'
        self.isms_path = self.repo_root / 'maturion-isms'
        self.runtime_export_path = self.isms_path / 'runtime' / 'export'
        
        # Ensure export directory exists
        self.runtime_export_path.mkdir(parents=True, exist_ok=True)
        
        self.export_timestamp = datetime.now().isoformat()
        self.errors = []
        self.warnings = []
        
    def export_all(self) -> Dict:
        """Export all runtime context"""
        print("🚀 Exporting Runtime Context...\n")
        
        results = {
            'export_timestamp': self.export_timestamp,
            'architecture': None,
            'compliance': None,
            'runtime_profile': None,
            'errors': [],
            'warnings': []
        }
        
        try:
            results['architecture'] = self.export_architecture_summary()
            print("✅ Architecture summary exported\n")
        except Exception as e:
            error_msg = f"Failed to export architecture: {str(e)}"
            results['errors'].append(error_msg)
            self.errors.append(error_msg)
            print(f"❌ {error_msg}\n")
        
        try:
            results['compliance'] = self.export_compliance_summary()
            print("✅ Compliance summary exported\n")
        except Exception as e:
            error_msg = f"Failed to export compliance: {str(e)}"
            results['errors'].append(error_msg)
            self.errors.append(error_msg)
            print(f"❌ {error_msg}\n")
        
        try:
            results['runtime_profile'] = self.export_runtime_profile()
            print("✅ Runtime profile exported\n")
        except Exception as e:
            error_msg = f"Failed to export runtime profile: {str(e)}"
            results['errors'].append(error_msg)
            self.errors.append(error_msg)
            print(f"❌ {error_msg}\n")
        
        results['errors'] = self.errors
        results['warnings'] = self.warnings
        
        return results
    
    def export_architecture_summary(self) -> str:
        """Export architecture summary to JSON"""
        print("📐 Exporting Architecture Summary...")
        
        architecture_summary = {
            'metadata': {
                'version': '1.0',
                'export_date': self.export_timestamp,
                'architecture_version': self._get_architecture_version(),
                'export_source': 'export-runtime-context.py'
            },
            'modules': self._collect_module_summaries(),
            'integration_contracts': self._collect_integration_contracts(),
            'architecture_principles': self._collect_architecture_principles(),
            'module_boundaries': self._collect_module_boundaries(),
            'technology_stack': self._collect_technology_stack(),
            'known_issues': []
        }
        
        # Validate against schema
        if not self._validate_architecture_schema(architecture_summary):
            self.warnings.append("Architecture summary may not match expected schema")
        
        # Write to file
        output_path = self.runtime_export_path / 'architecture-summary.json'
        with open(output_path, 'w') as f:
            json.dump(architecture_summary, f, indent=2)
        
        return str(output_path)
    
    def export_compliance_summary(self) -> str:
        """Export compliance summary to JSON"""
        print("📋 Exporting Compliance Summary...")
        
        compliance_summary = {
            'metadata': {
                'version': '1.0',
                'export_date': self.export_timestamp,
                'compliance_version': '1.0',
                'export_source': 'export-runtime-context.py'
            },
            'supported_standards': self._collect_supported_standards(),
            'control_mappings': self._collect_control_mappings(),
            'compliance_coverage_by_module': self._collect_compliance_coverage(),
            'compliance_gaps': [],
            'watchdog_rules': self._collect_watchdog_rules(),
            'audit_requirements': self._collect_audit_requirements()
        }
        
        # Validate against schema
        if not self._validate_compliance_schema(compliance_summary):
            self.warnings.append("Compliance summary may not match expected schema")
        
        # Write to file
        output_path = self.runtime_export_path / 'compliance-summary.json'
        with open(output_path, 'w') as f:
            json.dump(compliance_summary, f, indent=2)
        
        return str(output_path)
    
    def export_runtime_profile(self) -> str:
        """Export runtime profile to JSON"""
        print("🤖 Exporting Runtime Profile...")
        
        runtime_profile = {
            'metadata': {
                'version': '1.0',
                'export_date': self.export_timestamp,
                'profile_version': '1.0',
                'export_source': 'export-runtime-context.py'
            },
            'identity': self._collect_runtime_identity(),
            'tenant_isolation_rules': self._collect_tenant_isolation_rules(),
            'monitoring_configuration': self._collect_monitoring_configuration(),
            'autonomous_actions': self._collect_autonomous_actions(),
            'escalation_configuration': self._collect_escalation_configuration(),
            'learning_configuration': self._collect_learning_configuration(),
            'compliance_frameworks_active': list(self.COMPLIANCE_STANDARDS.keys()),
            'module_awareness': self._collect_module_awareness(),
            'guardrails': self._collect_guardrails(),
            'integration_points': self._collect_integration_points()
        }
        
        # Validate against schema
        if not self._validate_runtime_profile_schema(runtime_profile):
            self.warnings.append("Runtime profile may not match expected schema")
        
        # Write to file
        output_path = self.runtime_export_path / 'runtime-profile.json'
        with open(output_path, 'w') as f:
            json.dump(runtime_profile, f, indent=2)
        
        return str(output_path)
    
    # ========== ARCHITECTURE COLLECTORS ==========
    
    def _get_architecture_version(self) -> str:
        """Get current architecture version"""
        # Try to read from VERSION file or default to 1.0
        version_file = self.isms_path / 'VERSION'
        if version_file.exists():
            return version_file.read_text().strip()
        return '1.0.0'
    
    def _collect_module_summaries(self) -> List[Dict]:
        """Collect summaries of all modules"""
        modules = []
        
        for module_id in self.MODULES:
            module_path = self.isms_path / 'architecture' / module_id.lower()
            if not module_path.exists():
                continue
            
            module_summary = {
                'module_id': module_id,
                'module_name': module_id.replace('_', ' ').title(),
                'version': '1.0.0',  # Default version
                'status': 'active',
                'purpose': f"{module_id.replace('_', ' ').title()} module",
                'database_tables': self._extract_database_tables(module_path),
                'api_endpoints': self._extract_api_endpoints(module_path),
                'ui_routes': self._extract_ui_routes(module_path),
                'dependencies': [],
                'dependents': [],
                'compliance_mapping': []
            }
            
            modules.append(module_summary)
        
        return modules
    
    def _extract_database_tables(self, module_path: Path) -> List[str]:
        """Extract database table names from schema files"""
        tables = []
        schema_file = module_path / 'DATABASE_SCHEMA.md'
        
        if schema_file.exists():
            content = schema_file.read_text()
            # Look for CREATE TABLE statements or table names
            table_matches = re.findall(r'CREATE TABLE\s+(\w+)', content, re.IGNORECASE)
            tables.extend(table_matches)
            
            # Also look for markdown table headers that might indicate table names
            table_matches = re.findall(r'###\s+(\w+)\s+Table', content, re.IGNORECASE)
            tables.extend(table_matches)
        
        return list(set(tables))  # Remove duplicates
    
    def _extract_api_endpoints(self, module_path: Path) -> List[Dict]:
        """Extract API endpoints from edge functions spec"""
        endpoints = []
        edge_file = module_path / 'EDGE_FUNCTIONS.md'
        
        if edge_file.exists():
            content = edge_file.read_text()
            # Look for endpoint patterns like GET /api/path or POST /api/path
            endpoint_matches = re.findall(r'(GET|POST|PUT|PATCH|DELETE)\s+(/[\w/-]+)', content, re.IGNORECASE)
            
            for method, path in endpoint_matches:
                endpoints.append({
                    'path': path,
                    'method': method.upper(),
                    'purpose': ''  # Could be extracted from surrounding context
                })
        
        return endpoints
    
    def _extract_ui_routes(self, module_path: Path) -> List[str]:
        """Extract UI routes from component map or wireframes"""
        routes = []
        
        # Check component map
        component_file = module_path / 'FRONTEND_COMPONENT_MAP.md'
        if component_file.exists():
            content = component_file.read_text()
            # Look for route patterns
            route_matches = re.findall(r'Route:\s*(/[\w/-]+)', content, re.IGNORECASE)
            routes.extend(route_matches)
        
        return list(set(routes))
    
    def _collect_integration_contracts(self) -> List[Dict]:
        """Collect integration contracts between modules"""
        contracts = []
        
        # Check integration map files
        for module_id in self.MODULES:
            integration_file = self.isms_path / 'architecture' / module_id.lower() / 'INTEGRATION_MAP.md'
            if integration_file.exists():
                content = integration_file.read_text()
                # Extract integration information
                # This is a simplified extraction - could be enhanced
                contracts.append({
                    'contract_id': f'INT-{module_id}',
                    'source_module': module_id,
                    'target_module': 'MULTIPLE',
                    'integration_type': 'api_call',
                    'data_flow': 'Module integrations',
                    'breaking_change_risk': 'medium'
                })
        
        return contracts
    
    def _collect_architecture_principles(self) -> List[str]:
        """Collect core architecture principles"""
        principles = [
            'One-Time Build Correctness',
            'Zero Regression',
            'Strict Module Boundaries',
            'Tenant Isolation',
            'Compliance by Design',
            'Test-Driven Development',
            'API-First Design',
            'Schema-Driven Development'
        ]
        
        # Could read from build philosophy or governance files
        build_philosophy_file = self.repo_root / 'README.md'
        if build_philosophy_file.exists():
            content = build_philosophy_file.read_text()
            if 'One-Time Build' in content:
                pass  # Already in list
        
        return principles
    
    def _collect_module_boundaries(self) -> Dict:
        """Collect module boundary rules"""
        return {
            'strict_separation': True,
            'allowed_cross_module_access': []
        }
    
    def _collect_technology_stack(self) -> Dict:
        """Collect technology stack information"""
        return {
            'frontend': ['React', 'TypeScript', 'Shadcn UI', 'Tailwind CSS'],
            'backend': ['Supabase', 'Edge Functions', 'PostgreSQL'],
            'database': ['PostgreSQL', 'Supabase'],
            'ai_models': ['OpenAI GPT-4', 'Claude', 'DALL-E']
        }
    
    # ========== COMPLIANCE COLLECTORS ==========
    
    def _collect_supported_standards(self) -> List[Dict]:
        """Collect all supported compliance standards"""
        standards = []
        
        for standard_id, standard_name in self.COMPLIANCE_STANDARDS.items():
            # Extract category from standard name
            category = self._categorize_standard(standard_id)
            
            standards.append({
                'standard_id': standard_id,
                'standard_name': standard_name,
                'version': self._get_standard_version(standard_id),
                'category': category,
                'total_controls': 0,  # Would be populated from compliance library
                'mapped_controls': 0,
                'coverage_percentage': 0.0
            })
        
        return standards
    
    def _categorize_standard(self, standard_id: str) -> str:
        """Categorize compliance standard"""
        if 'ISO_27001' in standard_id or 'NIST' in standard_id:
            return 'information_security'
        elif 'ISO_31000' in standard_id or 'ISO_27005' in standard_id:
            return 'risk_management'
        elif 'ISO_22301' in standard_id:
            return 'business_continuity'
        elif 'GDPR' in standard_id or 'POPIA' in standard_id:
            return 'data_privacy'
        elif 'OWASP' in standard_id:
            return 'application_security'
        elif 'COBIT' in standard_id:
            return 'governance'
        return 'other'
    
    def _get_standard_version(self, standard_id: str) -> str:
        """Get version of compliance standard"""
        versions = {
            'ISO_27001': '2022',
            'ISO_27005': '2022',
            'ISO_31000': '2018',
            'ISO_22301': '2019',
            'COBIT': '2019'
        }
        return versions.get(standard_id, 'latest')
    
    def _collect_control_mappings(self) -> List[Dict]:
        """Collect control mappings"""
        # Read from compliance control library
        control_library_file = self.foreman_path / 'compliance' / 'compliance-control-library.json'
        
        if control_library_file.exists():
            try:
                with open(control_library_file, 'r') as f:
                    library = json.load(f)
                # Extract mappings from library
                # This is simplified - actual implementation would parse the library structure
                return []
            except json.JSONDecodeError:
                self.warnings.append("Could not parse compliance control library")
        
        return []
    
    def _collect_compliance_coverage(self) -> List[Dict]:
        """Collect compliance coverage by module"""
        coverage = []
        
        for module_id in self.MODULES:
            coverage.append({
                'module_id': module_id,
                'module_name': module_id.replace('_', ' ').title(),
                'standards_supported': [],
                'total_controls_implemented': 0
            })
        
        return coverage
    
    def _collect_watchdog_rules(self) -> List[Dict]:
        """Collect compliance watchdog rules"""
        rules = []
        
        # Read from watchdog spec
        watchdog_file = self.foreman_path / 'compliance' / 'compliance-watchdog-spec.md'
        if watchdog_file.exists():
            # Extract watchdog rules
            # Simplified for now
            rules.append({
                'rule_id': 'WD-001',
                'standard': 'ISO_27001',
                'rule_description': 'Monitor compliance control coverage',
                'monitoring_frequency': 'daily',
                'alert_threshold': 'coverage < 85%',
                'remediation_action': 'Alert admin to review missing controls'
            })
        
        return rules
    
    def _collect_audit_requirements(self) -> Dict:
        """Collect audit requirements"""
        return {
            'evidence_retention_days': 2555,  # 7 years
            'audit_trail_enabled': True,
            'required_documentation': [
                'Compliance control library',
                'Control implementation evidence',
                'QA test results',
                'Architecture documentation',
                'Change management logs'
            ],
            'certification_status': {}
        }
    
    # ========== RUNTIME PROFILE COLLECTORS ==========
    
    def _collect_runtime_identity(self) -> Dict:
        """Collect runtime identity from profile spec"""
        return {
            'name': 'Maturion',
            'role': 'Runtime Platform Intelligence Agent',
            'lifecycle_phase': 'Production / Live System Operation',
            'core_responsibilities': [
                'Continuous monitoring and anomaly detection',
                'Tenant support and guidance',
                'Compliance watchdog and enforcement',
                'Architecture drift detection',
                'Learning and self-improvement',
                'Escalation and human-in-the-loop safety'
            ],
            'communication_style': {
                'tenant_user': 'Friendly, helpful, clear',
                'tenant_admin': 'Professional, strategic, governance-focused',
                'johan_admin': 'Technical, architectural, system-level'
            }
        }
    
    def _collect_tenant_isolation_rules(self) -> Dict:
        """Collect tenant isolation rules"""
        return {
            'isolation_enabled': True,
            'organisation_id_required': True,
            'cross_tenant_queries_blocked': True,
            'anonymization_required_for_aggregation': True,
            'pii_logging_prohibited': True
        }
    
    def _collect_monitoring_configuration(self) -> Dict:
        """Collect monitoring configuration"""
        return {
            'performance_monitoring': {
                'enabled': True,
                'frequency_minutes': 5,
                'alert_thresholds': {
                    'response_time_ms': 1000,
                    'error_rate_percentage': 1.0
                }
            },
            'compliance_monitoring': {
                'enabled': True,
                'frequency': 'daily',
                'drift_detection_enabled': True
            },
            'security_monitoring': {
                'enabled': True,
                'anomaly_detection_enabled': True,
                'failed_auth_threshold': 5
            },
            'architecture_drift_monitoring': {
                'enabled': True,
                'validation_frequency': 'on_deployment'
            }
        }
    
    def _collect_autonomous_actions(self) -> Dict:
        """Collect autonomous actions configuration"""
        return {
            'allowed_actions': [
                {
                    'action': 'Fix minor configuration errors',
                    'conditions': 'Error severity is low and fix is pre-approved',
                    'approval_required': False
                },
                {
                    'action': 'Generate compliance reports',
                    'conditions': 'On demand or scheduled',
                    'approval_required': False
                },
                {
                    'action': 'Create AI Change Requests',
                    'conditions': 'Issue detected requiring code/architecture change',
                    'approval_required': True
                }
            ],
            'prohibited_actions': [
                'Modify production database schema',
                'Change user permissions or roles',
                'Alter compliance control mappings',
                'Deploy code changes',
                'Access tenant data content',
                'Make governance policy changes',
                'Override human decisions'
            ]
        }
    
    def _collect_escalation_configuration(self) -> Dict:
        """Collect escalation configuration"""
        return {
            'escalation_levels': [
                {
                    'level': 'informational',
                    'description': 'Log only, no action required',
                    'escalation_target': 'log_only',
                    'response_time_sla_minutes': 0
                },
                {
                    'level': 'advisory',
                    'description': 'Notify Johan, proactive action recommended',
                    'escalation_target': 'notify_johan',
                    'response_time_sla_minutes': 1440  # 24 hours
                },
                {
                    'level': 'warning',
                    'description': 'Escalate for decision',
                    'escalation_target': 'notify_johan',
                    'response_time_sla_minutes': 240  # 4 hours
                },
                {
                    'level': 'critical',
                    'description': 'Immediate escalation required',
                    'escalation_target': 'immediate_alert',
                    'response_time_sla_minutes': 30
                }
            ],
            'auto_escalation_rules': []
        }
    
    def _collect_learning_configuration(self) -> Dict:
        """Collect learning configuration"""
        return {
            'learning_enabled': True,
            'anonymization_required': True,
            'feedback_export_frequency': 'weekly',
            'model_drift_monitoring_enabled': True,
            'drift_detection_frequency': 'weekly'
        }
    
    def _collect_module_awareness(self) -> List[Dict]:
        """Collect module awareness configuration"""
        modules = []
        
        for module_id in self.MODULES:
            modules.append({
                'module_id': module_id,
                'module_name': module_id.replace('_', ' ').title(),
                'status': 'active',
                'support_enabled': True
            })
        
        return modules
    
    def _collect_guardrails(self) -> Dict:
        """Collect runtime guardrails"""
        return {
            'cannot_modify_governance': True,
            'cannot_deploy_code': True,
            'cannot_modify_schema': True,
            'cannot_access_tenant_data_content': True,
            'cannot_grant_permissions': True,
            'cannot_override_human_decisions': True
        }
    
    def _collect_integration_points(self) -> Dict:
        """Collect integration points"""
        return {
            'watchdog_integration': True,
            'dashboard_integration': True,
            'chat_interface_enabled': True,
            'api_monitoring_integration': True
        }
    
    # ========== VALIDATION ==========
    
    def _validate_architecture_schema(self, data: Dict) -> bool:
        """Validate architecture summary against schema"""
        required_keys = ['metadata', 'modules', 'integration_contracts', 'architecture_principles']
        return all(key in data for key in required_keys)
    
    def _validate_compliance_schema(self, data: Dict) -> bool:
        """Validate compliance summary against schema"""
        required_keys = ['metadata', 'supported_standards', 'control_mappings', 'compliance_coverage_by_module', 'watchdog_rules', 'audit_requirements']
        return all(key in data for key in required_keys)
    
    def _validate_runtime_profile_schema(self, data: Dict) -> bool:
        """Validate runtime profile against schema"""
        required_keys = ['metadata', 'identity', 'tenant_isolation_rules', 'monitoring_configuration', 'autonomous_actions', 'escalation_configuration', 'learning_configuration', 'compliance_frameworks_active', 'module_awareness', 'guardrails']
        return all(key in data for key in required_keys)
    
    def generate_summary_report(self, results: Dict) -> str:
        """Generate summary report of export"""
        report_lines = [
            "=" * 80,
            "RUNTIME CONTEXT EXPORT SUMMARY",
            "=" * 80,
            "",
            f"Export Timestamp: {self.export_timestamp}",
            "",
            "EXPORTS GENERATED:",
            ""
        ]
        
        if results['architecture']:
            report_lines.append(f"✅ Architecture Summary: {results['architecture']}")
        else:
            report_lines.append("❌ Architecture Summary: FAILED")
        
        if results['compliance']:
            report_lines.append(f"✅ Compliance Summary: {results['compliance']}")
        else:
            report_lines.append("❌ Compliance Summary: FAILED")
        
        if results['runtime_profile']:
            report_lines.append(f"✅ Runtime Profile: {results['runtime_profile']}")
        else:
            report_lines.append("❌ Runtime Profile: FAILED")
        
        report_lines.append("")
        
        if self.errors:
            report_lines.append("ERRORS:")
            for error in self.errors:
                report_lines.append(f"  ❌ {error}")
            report_lines.append("")
        
        if self.warnings:
            report_lines.append("WARNINGS:")
            for warning in self.warnings:
                report_lines.append(f"  ⚠️  {warning}")
            report_lines.append("")
        
        report_lines.extend([
            "=" * 80,
            "EXPORT COMPLETE",
            "=" * 80,
            ""
        ])
        
        return "\n".join(report_lines)


def main():
    parser = argparse.ArgumentParser(
        description='Export build-time context to runtime-ready JSON bundles'
    )
    
    parser.add_argument(
        '--architecture-only',
        action='store_true',
        help='Export only architecture summary'
    )
    
    parser.add_argument(
        '--compliance-only',
        action='store_true',
        help='Export only compliance summary'
    )
    
    parser.add_argument(
        '--profile-only',
        action='store_true',
        help='Export only runtime profile'
    )
    
    parser.add_argument(
        '--full-export',
        action='store_true',
        help='Export all summaries (default if no flags specified)'
    )
    
    parser.add_argument(
        '--repo-root',
        type=str,
        default='.',
        help='Path to repository root (default: current directory)'
    )
    
    args = parser.parse_args()
    
    # If no specific export flag is set, do full export
    if not (args.architecture_only or args.compliance_only or args.profile_only):
        args.full_export = True
    
    # Initialize exporter
    repo_root = Path(args.repo_root).resolve()
    exporter = RuntimeContextExporter(str(repo_root))
    
    results = {
        'export_timestamp': exporter.export_timestamp,
        'architecture': None,
        'compliance': None,
        'runtime_profile': None,
        'errors': [],
        'warnings': []
    }
    
    # Perform requested exports
    try:
        if args.architecture_only or args.full_export:
            results['architecture'] = exporter.export_architecture_summary()
            print("✅ Architecture summary exported\n")
        
        if args.compliance_only or args.full_export:
            results['compliance'] = exporter.export_compliance_summary()
            print("✅ Compliance summary exported\n")
        
        if args.profile_only or args.full_export:
            results['runtime_profile'] = exporter.export_runtime_profile()
            print("✅ Runtime profile exported\n")
        
    except Exception as e:
        print(f"\n❌ Export failed: {str(e)}\n")
        sys.exit(1)
    
    # Collect errors and warnings
    results['errors'] = exporter.errors
    results['warnings'] = exporter.warnings
    
    # Generate and print summary report
    summary_report = exporter.generate_summary_report(results)
    print(summary_report)
    
    # Write summary report to file
    report_path = exporter.runtime_export_path / 'export-summary-report.txt'
    with open(report_path, 'w') as f:
        f.write(summary_report)
    
    print(f"📄 Summary report saved to: {report_path}\n")
    
    # Exit with error code if there were errors
    if results['errors']:
        sys.exit(1)
    
    sys.exit(0)


if __name__ == '__main__':
    main()
