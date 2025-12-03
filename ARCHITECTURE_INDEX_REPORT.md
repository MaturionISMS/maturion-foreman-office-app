====================================================================================================
MATURION ISMS - ARCHITECTURE INDEX REPORT
====================================================================================================
Generated: 2025-12-03T14:25:13.050913
Repository: /home/runner/work/maturion-ai-foreman/maturion-ai-foreman

📊 EXECUTIVE SUMMARY
----------------------------------------------------------------------------------------------------
Total Modules Indexed: 9
Total Architecture Files: 87
True North Documents: 8
Overall Compliance Coverage: 3.0%
Missing Critical Elements: 27
Detected Inconsistencies: 14

📊 MODULE MAP
----------------------------------------------------------------------------------------------------

⚠ COURSE_CRAFTER
   Completeness: 78.6% (11/14 specs)
   Files: 11
   • TRUE_NORTH: v1.0
   • DATABASE_SCHEMA: v1.0

⚠ ERM
   Completeness: 71.4% (10/14 specs)
   Files: 10
   • TRUE_NORTH: v1.0
   • DATABASE_SCHEMA: v1.1

✓ PIT
   Completeness: 100.0% (14/14 specs)
   Files: 14
   • TRUE_NORTH: v1.0
   • DATABASE_SCHEMA: v1.1
   • INTEGRATION_MAP: v1.0

✗ RISK_ASSESSMENT
   Completeness: 42.9% (6/14 specs)
   Files: 6
   • TRUE_NORTH: v1.1
   • DATABASE_SCHEMA: v1.1

✗ RISK_THREAT
   Completeness: 35.7% (5/14 specs)
   Files: 5
   • TRUE_NORTH: v0.1
   • DATABASE_SCHEMA: v0.1

✗ RISK_VULNERABILITY
   Completeness: 35.7% (5/14 specs)
   Files: 5
   ⚠️  Missing Critical: TRUE_NORTH
   • DATABASE_SCHEMA: v0.1

✓ THREAT
   Completeness: 92.9% (13/14 specs)
   Files: 13
   • TRUE_NORTH: v1.0
   • DATABASE_SCHEMA: v1.1
   • INTEGRATION_MAP: v1.0

✓ VULNERABILITY
   Completeness: 92.9% (13/14 specs)
   Files: 13
   • TRUE_NORTH: v1.0
   • DATABASE_SCHEMA: v1.1
   • INTEGRATION_MAP: v1.0

⚠ WRAC
   Completeness: 71.4% (10/14 specs)
   Files: 10
   • TRUE_NORTH: v0.1
   • DATABASE_SCHEMA: v0.1

🧭 TRUE NORTH INDEX
----------------------------------------------------------------------------------------------------
✓ COURSE_CRAFTER
  Version: 1.0
  Path: COURSE_CRAFTER_TRUE_NORTH_v1.0.md
  Sections: 0
  Contains: Purpose, Architecture, Integration

✓ ERM
  Version: 1.0
  Path: ERM_TRUE_NORTH_v1.0.md
  Sections: 0
  Contains: Purpose, Architecture, Data Model, Integration

✓ PIT
  Version: 1.0
  Path: PIT_TRUE_NORTH_v1.0.md
  Sections: 0
  Contains: Purpose, Architecture, Data Model, Integration

✓ RISK_ASSESSMENT
  Version: 0.1
  Path: RISK_ASSESSMENT_TRUE_NORTH_v0.1.md
  Sections: 23
  Contains: Purpose, Architecture, Integration

✓ RISK_THREAT
  Version: 0.1
  Path: RISK_THREAT_MODULE_TRUE_NORTH_v0.1.md
  Sections: 0
  Contains: Purpose, Data Model, Integration

✓ THREAT
  Version: 1.0
  Path: THREAT_TRUE_NORTH_v1.0.md
  Sections: 0
  Contains: Purpose, Architecture, Data Model, Integration

✓ VULNERABILITY
  Version: 0.1
  Path: VULNERABILITY_MODULE_TRUE_NORTH_ARCHITECTURE_v0.1.md
  Sections: 0
  Contains: Architecture, Data Model, Integration

✓ WRAC
  Version: 0.1
  Path: WRAC_TRUE_NORTH_v0.1.md
  Sections: 0
  Contains: Purpose, Architecture, Data Model, Integration

🔗 ARCHITECTURE DEPENDENCY MAP
----------------------------------------------------------------------------------------------------
Master Integration Map:
  ✓ INTEGRATED_ISMS_MODULE_INTEGRATION_MAP_v1.0.md
  • Contains Hub-and-Spoke architecture diagram
  • Contains workflow map

Module Dependencies:
  COURSE_CRAFTER → WRAC
  ERM → PIT, WRAC
  PIT → WRAC
  RISK_ASSESSMENT → ERM, PIT, THREAT, WRAC
  RISK_THREAT → PIT, THREAT
  RISK_VULNERABILITY → PIT, VULNERABILITY
  THREAT → ERM, PIT, RISK_ASSESSMENT, VULNERABILITY, WRAC
  VULNERABILITY → ERM, PIT, THREAT, WRAC
  WRAC → ERM, PIT, RISK_ASSESSMENT, THREAT, VULNERABILITY

Dependency Statistics:
  Total Dependencies: 26
  Average per Module: 2.89
  Most Dependent Module: THREAT
  Most Referenced Module: PIT

📜 COMPLIANCE COVERAGE
----------------------------------------------------------------------------------------------------
Overall Coverage: 3.0%
Standards Tracked: 11
Fully Covered Standards: 0

Coverage by Standard:
  COBIT                ░░░░░░░░░░░░░░░░░░░░   0.0% (0/9 modules)
  GDPR                 ██░░░░░░░░░░░░░░░░░░  11.1% (1/9 modules)
  ISO 22301            ░░░░░░░░░░░░░░░░░░░░   0.0% (0/9 modules)
  ISO 27001            ░░░░░░░░░░░░░░░░░░░░   0.0% (0/9 modules)
  ISO 27005            ░░░░░░░░░░░░░░░░░░░░   0.0% (0/9 modules)
  ISO 31000            ██░░░░░░░░░░░░░░░░░░  11.1% (1/9 modules)
  NIST 800-53          ░░░░░░░░░░░░░░░░░░░░   0.0% (0/9 modules)
  NIST CSF             ░░░░░░░░░░░░░░░░░░░░   0.0% (0/9 modules)
  OWASP ASVS           ░░░░░░░░░░░░░░░░░░░░   0.0% (0/9 modules)
  OWASP Top 10         ░░░░░░░░░░░░░░░░░░░░   0.0% (0/9 modules)
  POPIA                ██░░░░░░░░░░░░░░░░░░  11.1% (1/9 modules)

⚠️  MISSING ARCHITECTURE ELEMENTS
----------------------------------------------------------------------------------------------------
Critical Missing Elements:
  🔴 RISK_VULNERABILITY: Missing TRUE_NORTH
  🔴 RISK_VULNERABILITY: Missing True North document

Medium Priority Missing Elements:
  🟡 RISK_ASSESSMENT: Missing ARCHITECTURE
  🟡 RISK_ASSESSMENT: Missing INTEGRATION_MAP
  🟡 RISK_ASSESSMENT: Missing EXPORT_SPEC
  🟡 RISK_ASSESSMENT: Missing QA_IMPLEMENTATION_PLAN
  🟡 RISK_ASSESSMENT: Missing IMPLEMENTATION_GUIDE
  🟡 RISK_ASSESSMENT: Missing CHANGELOG
  🟡 RISK_ASSESSMENT: Missing WATCHDOG_LOGIC
  🟡 RISK_ASSESSMENT: Missing MODEL_ROUTING_SPEC
  🟡 RISK_THREAT: Missing ARCHITECTURE
  🟡 RISK_THREAT: Missing WIREFRAMES
  ... and 15 more

🔍 DEPENDENCY INCONSISTENCIES
----------------------------------------------------------------------------------------------------
High Severity:
  🔴 Circular dependency: ERM ↔ WRAC
  🔴 Circular dependency: PIT ↔ WRAC
  🔴 Circular dependency: THREAT ↔ RISK_ASSESSMENT
  🔴 Circular dependency: THREAT ↔ VULNERABILITY
  🔴 Circular dependency: THREAT ↔ WRAC
  🔴 Circular dependency: VULNERABILITY ↔ THREAT
  🔴 Circular dependency: VULNERABILITY ↔ WRAC
  🔴 Circular dependency: RISK_ASSESSMENT ↔ THREAT
  🔴 Circular dependency: RISK_ASSESSMENT ↔ WRAC
  🔴 Circular dependency: WRAC ↔ ERM
  🔴 Circular dependency: WRAC ↔ PIT
  🔴 Circular dependency: WRAC ↔ RISK_ASSESSMENT
  🔴 Circular dependency: WRAC ↔ THREAT
  🔴 Circular dependency: WRAC ↔ VULNERABILITY

💡 RECOMMENDATIONS
----------------------------------------------------------------------------------------------------
🔹 Complete architecture specifications for: COURSE_CRAFTER, ERM, RISK_ASSESSMENT, WRAC, RISK_THREAT, RISK_VULNERABILITY
🔹 Create True North documents for: RISK_VULNERABILITY
🔹 Improve compliance coverage for: ISO 27001, ISO 27005, ISO 31000, ISO 22301, NIST CSF, NIST 800-53, COBIT, GDPR, POPIA, OWASP ASVS, OWASP Top 10
🔹 Resolve 14 circular dependencies

====================================================================================================
ARCHITECTURE HEALTH SCORE: 0.0/100
Status: REQUIRES ATTENTION ❌
====================================================================================================