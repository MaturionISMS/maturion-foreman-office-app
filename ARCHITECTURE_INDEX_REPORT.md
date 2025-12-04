====================================================================================================
MATURION ISMS - ARCHITECTURE INDEX REPORT
====================================================================================================
Generated: 2025-12-04T07:27:58.619405
Repository: /home/runner/work/maturion-ai-foreman/maturion-ai-foreman

📊 EXECUTIVE SUMMARY
----------------------------------------------------------------------------------------------------
Total Modules Indexed: 12
Total Architecture Files: 132
True North Documents: 12
Overall Compliance Coverage: 11.4%
Missing Critical Elements: 17
Detected Inconsistencies: 11

📊 MODULE MAP
----------------------------------------------------------------------------------------------------

✓ ANALYTICS_REMOTE_ASSURANCE
   Completeness: 80.0% (12/15 specs)
   Files: 12
   • TRUE_NORTH: v1.0
   • DATABASE_SCHEMA: v1.0

⚠ AUDITOR_MOBILE_APP
   Completeness: 73.3% (11/15 specs)
   Files: 11
   • TRUE_NORTH: v1.0
   • DATABASE_SCHEMA: v1.0

✓ COURSE_CRAFTER
   Completeness: 80.0% (12/15 specs)
   Files: 12
   • TRUE_NORTH: v1.0
   • DATABASE_SCHEMA: v1.0

✓ ERM
   Completeness: 80.0% (12/15 specs)
   Files: 12
   • TRUE_NORTH: v1.0
   • DATABASE_SCHEMA: v1.0

✓ PIT
   Completeness: 86.7% (13/15 specs)
   Files: 13
   • TRUE_NORTH: v1.0
   • DATABASE_SCHEMA: v1.0

✓ POLICY_BUILDER
   Completeness: 86.7% (13/15 specs)
   Files: 13
   • TRUE_NORTH: v1.0
   • DATABASE_SCHEMA: v1.0

⚠ RISK_ASSESSMENT
   Completeness: 73.3% (11/15 specs)
   Files: 11
   • TRUE_NORTH: v1.1
   • DATABASE_SCHEMA: v1.0

✗ RISK_THREAT
   Completeness: 13.3% (2/15 specs)
   Files: 2
   ⚠️  Missing Critical: DATABASE_SCHEMA
   • TRUE_NORTH: v0.1

⚠ SKILLS_DEVELOPMENT_PORTAL
   Completeness: 73.3% (11/15 specs)
   Files: 11
   • TRUE_NORTH: v1.0
   • DATABASE_SCHEMA: v1.0

✓ THREAT
   Completeness: 86.7% (13/15 specs)
   Files: 13
   • TRUE_NORTH: v1.0
   • DATABASE_SCHEMA: v1.0

✓ VULNERABILITY
   Completeness: 86.7% (13/15 specs)
   Files: 13
   • TRUE_NORTH: v1.0
   • DATABASE_SCHEMA: v1.0

⚠ WRAC
   Completeness: 60.0% (9/15 specs)
   Files: 9
   • TRUE_NORTH: v0.1
   • DATABASE_SCHEMA: v1.0

🧭 TRUE NORTH INDEX
----------------------------------------------------------------------------------------------------
✓ ANALYTICS_REMOTE_ASSURANCE
  Version: 1.0
  Path: maturion-isms/apps/analytics-remote-assurance/architecture/ANALYTICS_REMOTE_ASSURANCE_TRUE_NORTH_v1.0.md
  Sections: 9
  Contains: Purpose, Architecture

✓ AUDITOR_MOBILE_APP
  Version: 1.0
  Path: maturion-isms/apps/auditor-mobile-app/architecture/AUDITOR_MOBILE_APP_TRUE_NORTH_v1.0.md
  Sections: 9
  Contains: Purpose, Architecture

✓ COURSE_CRAFTER
  Version: 1.0
  Path: maturion-isms/apps/course-crafter/architecture/COURSE_CRAFTER_TRUE_NORTH_v1.0.md
  Sections: 0
  Contains: Purpose, Architecture, Integration

✓ ERM
  Version: 1.0
  Path: maturion-isms/apps/erm/architecture/ERM_TRUE_NORTH_v1.0.md
  Sections: 0
  Contains: Purpose, Architecture, Data Model, Integration

✓ PIT
  Version: 1.0
  Path: maturion-isms/apps/pit/architecture/PIT_TRUE_NORTH_v1.0.md
  Sections: 0
  Contains: Purpose, Architecture, Data Model, Integration

✓ POLICY_BUILDER
  Version: 1.0
  Path: maturion-isms/apps/policy-builder/architecture/POLICY_BUILDER_TRUE_NORTH_v1.0.md
  Sections: 9
  Contains: Purpose, Architecture

✓ RISK_ASSESSMENT
  Version: 0.1
  Path: maturion-isms/apps/risk-assessment/architecture/RISK_ASSESSMENT_TRUE_NORTH_v0.1.md
  Sections: 23
  Contains: Purpose, Architecture, Integration

✓ RISK_THREAT
  Version: 0.1
  Path: maturion-isms/apps/threat/architecture/RISK_THREAT_MODULE_TRUE_NORTH_v0.1.md
  Sections: 0
  Contains: Purpose, Data Model, Integration

✓ SKILLS_DEVELOPMENT_PORTAL
  Version: 1.0
  Path: maturion-isms/apps/skills-development-portal/architecture/SKILLS_DEVELOPMENT_PORTAL_TRUE_NORTH_v1.0.md
  Sections: 9
  Contains: Purpose, Architecture

✓ THREAT
  Version: 1.0
  Path: maturion-isms/apps/threat/architecture/THREAT_TRUE_NORTH_v1.0.md
  Sections: 0
  Contains: Purpose, Architecture, Data Model, Integration

✓ VULNERABILITY
  Version: 0.1
  Path: maturion-isms/apps/vulnerability/architecture/VULNERABILITY_MODULE_TRUE_NORTH_ARCHITECTURE_v0.1.md
  Sections: 0
  Contains: Architecture, Data Model, Integration

✓ WRAC
  Version: 0.1
  Path: maturion-isms/apps/wrac/architecture/WRAC_TRUE_NORTH_v0.1.md
  Sections: 0
  Contains: Purpose, Architecture, Data Model, Integration

🔗 ARCHITECTURE DEPENDENCY MAP
----------------------------------------------------------------------------------------------------
Module Dependencies:
  ERM → PIT, WRAC
  PIT → WRAC
  RISK_ASSESSMENT → ERM, PIT, WRAC
  RISK_THREAT → PIT
  THREAT → ERM, PIT, VULNERABILITY, WRAC
  VULNERABILITY → ERM, PIT, THREAT, WRAC
  WRAC → PIT, THREAT

Dependency Statistics:
  Total Dependencies: 17
  Average per Module: 1.42
  Most Dependent Module: THREAT
  Most Referenced Module: PIT

📜 COMPLIANCE COVERAGE
----------------------------------------------------------------------------------------------------
Overall Coverage: 11.4%
Standards Tracked: 11
Fully Covered Standards: 0

Coverage by Standard:
  COBIT                ░░░░░░░░░░░░░░░░░░░░   0.0% (0/12 modules)
  GDPR                 ████████░░░░░░░░░░░░  41.7% (5/12 modules)
  ISO 22301            ░░░░░░░░░░░░░░░░░░░░   0.0% (0/12 modules)
  ISO 27001            ██████░░░░░░░░░░░░░░  33.3% (4/12 modules)
  ISO 27005            ░░░░░░░░░░░░░░░░░░░░   0.0% (0/12 modules)
  ISO 31000            █░░░░░░░░░░░░░░░░░░░   8.3% (1/12 modules)
  NIST 800-53          ░░░░░░░░░░░░░░░░░░░░   0.0% (0/12 modules)
  NIST CSF             ░░░░░░░░░░░░░░░░░░░░   0.0% (0/12 modules)
  OWASP ASVS           ░░░░░░░░░░░░░░░░░░░░   0.0% (0/12 modules)
  OWASP Top 10         ░░░░░░░░░░░░░░░░░░░░   0.0% (0/12 modules)
  POPIA                ████████░░░░░░░░░░░░  41.7% (5/12 modules)

⚠️  MISSING ARCHITECTURE ELEMENTS
----------------------------------------------------------------------------------------------------
Critical Missing Elements:
  🔴 Missing master document: SRMF_MASTER_BUILD_REFERENCE_v1.0.md
  🔴 Missing master document: Integrated_ISMS_Architecture_v1.1.md
  🔴 Missing master document: INTEGRATED_ISMS_MODULE_INTEGRATION_MAP_v1.0.md
  🔴 RISK_THREAT: Missing DATABASE_SCHEMA
  🔴 RISK_VULNERABILITY: Missing True North document

Medium Priority Missing Elements:
  🟡 RISK_THREAT: Missing ARCHITECTURE
  🟡 RISK_THREAT: Missing FRONTEND_COMPONENT_MAP
  🟡 RISK_THREAT: Missing WIREFRAMES
  🟡 RISK_THREAT: Missing EDGE_FUNCTIONS
  🟡 RISK_THREAT: Missing INTEGRATION_SPEC
  🟡 RISK_THREAT: Missing INTEGRATION_MAP
  🟡 RISK_THREAT: Missing EXPORT_SPEC
  🟡 RISK_THREAT: Missing IMPLEMENTATION_GUIDE
  🟡 RISK_THREAT: Missing SPRINT_PLAN
  🟡 RISK_THREAT: Missing CHANGELOG
  ... and 2 more

🔍 DEPENDENCY INCONSISTENCIES
----------------------------------------------------------------------------------------------------
High Severity:
  🔴 Circular dependency: PIT ↔ WRAC
  🔴 Circular dependency: THREAT ↔ VULNERABILITY
  🔴 Circular dependency: THREAT ↔ WRAC
  🔴 Circular dependency: VULNERABILITY ↔ THREAT
  🔴 Circular dependency: WRAC ↔ PIT
  🔴 Circular dependency: WRAC ↔ THREAT

Low Severity:
  🟡 Orphaned module: COURSE_CRAFTER
  🟡 Orphaned module: POLICY_BUILDER
  🟡 Orphaned module: ANALYTICS_REMOTE_ASSURANCE
  🟡 Orphaned module: AUDITOR_MOBILE_APP
  🟡 Orphaned module: SKILLS_DEVELOPMENT_PORTAL

💡 RECOMMENDATIONS
----------------------------------------------------------------------------------------------------
🔹 Complete architecture specifications for: RISK_ASSESSMENT, WRAC, RISK_THREAT, AUDITOR_MOBILE_APP, SKILLS_DEVELOPMENT_PORTAL
🔹 Create True North documents for: RISK_VULNERABILITY
🔹 Improve compliance coverage for: ISO 27001, ISO 27005, ISO 31000, ISO 22301, NIST CSF, NIST 800-53, COBIT, GDPR, POPIA, OWASP ASVS, OWASP Top 10
🔹 Resolve 6 circular dependencies

====================================================================================================
ARCHITECTURE HEALTH SCORE: 0.0/100
Status: REQUIRES ATTENTION ❌
====================================================================================================