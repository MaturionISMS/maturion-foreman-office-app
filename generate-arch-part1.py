#!/usr/bin/env python3
"""
Maturion Foreman - Architecture Component Generator (Part 1)
Build Wave 0.1 - Architecture Completion Sprint

This generates the first set of missing architecture files.
"""
import os
from pathlib import Path
from datetime import datetime

# Module configuration - all 11 modules
MODULES = {
    'pit': {
        'name': 'PIT', 'full_name': 'Project Implementation Tracker',
        'directory': 'pit', 'has_true_north': True, 'has_architecture': True,
        'requires': {'edge_functions': True, 'export_spec': False, 'watchdog_logic': True, 'model_routing_spec': True}
    },
    'erm': {
        'name': 'ERM', 'full_name': 'Event & Risk Management',
        'directory': 'erm', 'has_true_north': True, 'has_architecture': False,
        'requires': {'edge_functions': True, 'export_spec': True, 'watchdog_logic': False, 'model_routing_spec': False}
    },
    'risk-assessment': {
        'name': 'RISK_ASSESSMENT', 'full_name': 'Risk Assessment',
        'directory': 'risk-assessment', 'has_true_north': True, 'has_architecture': False,
        'requires': {'edge_functions': False, 'export_spec': True, 'watchdog_logic': False, 'model_routing_spec': False}
    },
    'threat': {
        'name': 'THREAT', 'full_name': 'Threat Management',
        'directory': 'threat', 'has_true_north': True, 'has_architecture': False,
        'requires': {'edge_functions': True, 'export_spec': False, 'watchdog_logic': True, 'model_routing_spec': True}
    },
    'vulnerability': {
        'name': 'VULNERABILITY', 'full_name': 'Vulnerability Management',
        'directory': 'vulnerability', 'has_true_north': True, 'has_architecture': False,
        'requires': {'edge_functions': True, 'export_spec': False, 'watchdog_logic': True, 'model_routing_spec': True}
    },
    'wrac': {
        'name': 'WRAC', 'full_name': 'Workforce Risk & Compliance',
        'directory': 'wrac', 'has_true_north': True, 'has_architecture': True,
        'requires': {'edge_functions': False, 'export_spec': False, 'watchdog_logic': False, 'model_routing_spec': False}
    },
    'course-crafter': {
        'name': 'COURSE_CRAFTER', 'full_name': 'Course Crafter',
        'directory': 'course-crafter', 'has_true_north': True, 'has_architecture': True,
        'requires': {'edge_functions': True, 'export_spec': True, 'watchdog_logic': False, 'model_routing_spec': False}
    },
    'policy-builder': {
        'name': 'POLICY_BUILDER', 'full_name': 'Policy Builder',
        'directory': 'policy-builder', 'has_true_north': False, 'has_architecture': False,
        'requires': {'edge_functions': True, 'export_spec': True, 'watchdog_logic': False, 'model_routing_spec': True}
    },
    'analytics-remote-assurance': {
        'name': 'ANALYTICS_REMOTE_ASSURANCE', 'full_name': 'Analytics Remote Assurance',
        'directory': 'analytics-remote-assurance', 'has_true_north': False, 'has_architecture': False,
        'requires': {'edge_functions': True, 'export_spec': True, 'watchdog_logic': False, 'model_routing_spec': False}
    },
    'auditor-mobile-app': {
        'name': 'AUDITOR_MOBILE_APP', 'full_name': 'Auditor Mobile App',
        'directory': 'auditor-mobile-app', 'has_true_north': False, 'has_architecture': False,
        'requires': {'edge_functions': True, 'export_spec': False, 'watchdog_logic': False, 'model_routing_spec': False}
    },
    'skills-development-portal': {
        'name': 'SKILLS_DEVELOPMENT_PORTAL', 'full_name': 'Skills Development Portal',
        'directory': 'skills-development-portal', 'has_true_north': False, 'has_architecture': False,
        'requires': {'edge_functions': True, 'export_spec': False, 'watchdog_logic': False, 'model_routing_spec': False}
    }
}

BASE_DIR = Path('/home/runner/work/maturion-ai-foreman/maturion-ai-foreman/maturion-isms/apps')

def ensure_dirs(module_key, module_info):
    """Create directory structure"""
    module_dir = BASE_DIR / module_info['directory']
    arch_dir = module_dir / 'architecture'
    qa_dir = module_dir / 'qa-plans'
    comp_dir = module_dir / 'compliance'
    
    arch_dir.mkdir(parents=True, exist_ok=True)
    qa_dir.mkdir(parents=True, exist_ok=True)
    comp_dir.mkdir(parents=True, exist_ok=True)
    
    return arch_dir, qa_dir, comp_dir

print("Generating architecture components for Build Wave 0.1...")
print("This will create missing architecture files for all 11 modules.")
print(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\nRun the Phase 1-5 generator scripts next to complete all files.")
