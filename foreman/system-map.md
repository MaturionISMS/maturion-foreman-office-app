# Maturion ISMS System Map

## Purpose

This document provides a comprehensive map of the Maturion Integrated Security Management System (ISMS) ecosystem, including:
- Monorepo structure and organization
- Module boundaries and ownership
- Integration points and dependencies
- Governance and documentation hierarchy

This map serves as the authoritative reference for understanding system organization and module relationships.

---

## 1. Monorepo Structure Overview

### Root Structure

```
maturion-isms/                              # Main ISMS monorepo
├── architecture/                           # System-level architecture
│   ├── system-architecture/               # ISMS core architecture docs
│   ├── integration-maps/                  # Cross-module integration specs
│   └── control-models/                    # Control library, efficacy models
│
├── apps/                                   # Application modules
│   ├── course-crafter/                    # E1-E4 training content module
│   ├── erm/                               # Enterprise Risk Management
│   ├── pit/                               # Project & Issues Tracker
│   ├── threat/                            # Threat Intelligence
│   ├── vulnerability/                     # Vulnerability Management
│   ├── risk-assessment/                   # Risk Assessment
│   └── wrac/                              # Workplace Risk Assessment & Control
│
└── shared/                                 # Shared libraries and components
    ├── ui-components/                     # Shared UI components
    ├── api-client/                        # Shared API client
    ├── auth/                              # Shared authentication
    └── utils/                             # Shared utilities
```

### Supporting Repositories

```
maturion-ai-foreman/                        # Governance and orchestration
├── foreman/                               # Foreman system files
│   ├── identity.md                        # Foreman identity and authority
│   ├── command-grammar.md                 # Instruction formats
│   ├── builder-manifest.json              # Builder agent registry
│   └── system-map.md                      # This document
├── .github/                               # GitHub configuration
└── [Architecture Reference Files]         # SRMF, True North, Integration Maps

maturion-copilot-builders/                  # Builder agent implementations
├── builders/                              # Individual builder agents
│   ├── course-crafter-builder/
│   ├── erm-builder/
│   ├── pit-builder/
│   ├── threat-builder/
│   ├── vulnerability-builder/
│   ├── risk-assessment-builder/
│   ├── wrac-builder/
│   └── architecture-builder/
└── knowledge/                             # Builder knowledge bases
```

---

## 2. Module Boundaries and Ownership

### Course Crafter Module
**Path**: `apps/course-crafter/`  
**Owner**: Course Crafter Builder (`builder-course-crafter`)  
**Purpose**: E1-E4 training content generation and management

**Owns**:
- Course creation and editing workflows
- Training material generation
- E1-E4 content templates
- Export functionality (SCORM, PDF, etc.)
- Course Crafter UI components

**Dependencies**:
- **ERM**: Reads risk data to inform training content (via API)
- **Integration Map**: Uses INTEGRATED_ISMS_MODULE_INTEGRATION_MAP_v1.0.md

**Boundaries**:
- ✅ Can read ERM risk assessments via API
- ❌ Cannot modify ERM data
- ❌ Cannot access other module databases directly
- ✅ Can create training content based on any ISMS module data (via APIs)

---

### ERM (Enterprise Risk Management) Module
**Path**: `apps/erm/`  
**Owner**: ERM Builder (`builder-erm`)  
**Purpose**: Enterprise-wide risk management, matrices, heatmaps, and reporting

**Owns**:
- Risk matrix configuration
- Risk heatmap visualization
- Risk appetite and tolerance settings
- Impact and likelihood scales
- Risk reporting and analytics
- Global risk settings

**Dependencies**:
- **Risk Assessment**: Reads assessment results (via API)
- **Threat**: Reads threat data for risk correlation (via API)
- **Vulnerability**: Reads vulnerability data for risk correlation (via API)
- **Integration Map**: Uses INTEGRATED_ISMS_MODULE_INTEGRATION_MAP_v1.0.md

**Boundaries**:
- ✅ Can aggregate risk data from multiple modules via APIs
- ❌ Cannot modify threat or vulnerability data
- ❌ Cannot perform risk assessments (Risk Assessment module responsibility)
- ✅ Can provide risk scoring services to other modules

---

### PIT (Project & Issues Tracker) Module
**Path**: `apps/pit/`  
**Owner**: PIT Builder (`builder-pit`)  
**Purpose**: Project tracking, issue management, watchdog monitoring, AI task routing

**Owns**:
- Project management workflows
- Issue tracking and assignment
- Watchdog logic for project monitoring
- AI routing for automated task delegation
- Project reporting and dashboards

**Dependencies**:
- **Threat**: Reads threat data for project context (via API)
- **Vulnerability**: Reads vulnerability data for project context (via API)
- **AI Routing**: Uses PIT_MODEL_ROUTING_SPEC_v1.0.md
- **Watchdog**: Uses PIT_WATCHDOG_LOGIC_v1.0.md

**Boundaries**:
- ✅ Can create watchdog triggers for project milestones
- ✅ Can route AI tasks within PIT scope
- ❌ Cannot modify threat or vulnerability assessments
- ❌ Cannot modify watchdog logic in other modules
- ✅ Can integrate with threat/vulnerability data for project context

---

### Threat Module
**Path**: `apps/threat/`  
**Owner**: Threat Builder (`builder-threat`)  
**Purpose**: Threat intelligence gathering, assessment, monitoring, and AI-assisted analysis

**Owns**:
- Threat intelligence workflows
- Threat assessment and scoring
- Threat watchdog monitoring
- AI routing for threat analysis
- Threat reporting and visualization

**Dependencies**:
- **Vulnerability**: Correlates with vulnerability data (via API)
- **ERM**: Provides threat data for risk scoring (via API)
- **AI Routing**: Uses THREAT_MODEL_ROUTING_SPEC_v1.0.md
- **Watchdog**: Uses THREAT_WATCHDOG_LOGIC_v1.0.md

**Boundaries**:
- ✅ Can analyze and assess threats
- ✅ Can trigger watchdog alerts for threat conditions
- ❌ Cannot modify vulnerability data
- ❌ Cannot modify risk scoring (ERM responsibility)
- ✅ Can correlate threat-vulnerability relationships

---

### Vulnerability Module
**Path**: `apps/vulnerability/`  
**Owner**: Vulnerability Builder (`builder-vulnerability`)  
**Purpose**: Vulnerability management, scanning integration, prioritization, and AI-assisted analysis

**Owns**:
- Vulnerability scanning integration
- Vulnerability assessment and CVSS scoring
- Vulnerability prioritization
- Vulnerability watchdog monitoring
- AI routing for vulnerability analysis
- Remediation tracking

**Dependencies**:
- **Threat**: Correlates with threat data (via API)
- **ERM**: Provides vulnerability data for risk scoring (via API)
- **AI Routing**: Uses VULNERABILITY_MODEL_ROUTING_SPEC_v1.0.md
- **Watchdog**: Uses VULNERABILITY_WATCHDOG_LOGIC_v1.0.md

**Boundaries**:
- ✅ Can assess and score vulnerabilities
- ✅ Can trigger watchdog alerts for vulnerability conditions
- ❌ Cannot modify threat assessments
- ❌ Cannot modify risk scoring (ERM responsibility)
- ✅ Can correlate vulnerability-threat relationships

---

### Risk Assessment Module
**Path**: `apps/risk-assessment/`  
**Owner**: Risk Assessment Builder (`builder-risk-assessment`)  
**Purpose**: Risk assessment workflows, methodologies, templates, and scoring

**Owns**:
- Risk assessment workflows
- Assessment templates and methodologies
- Risk scoring logic
- Compliance framework alignment (ISO, NIST, etc.)
- Assessment reporting

**Dependencies**:
- **ERM**: Sends assessment results for aggregation (via API)
- **Threat**: Reads threat data for assessment context (via API)
- **Vulnerability**: Reads vulnerability data for assessment context (via API)

**Boundaries**:
- ✅ Can perform risk assessments
- ✅ Can define assessment methodologies
- ❌ Cannot modify risk matrices (ERM responsibility)
- ❌ Cannot modify threat or vulnerability data
- ✅ Can provide assessment data to ERM for visualization

---

### WRAC (Workplace Risk Assessment & Control) Module
**Path**: `apps/wrac/`  
**Owner**: WRAC Builder (`builder-wrac`)  
**Purpose**: Workplace safety assessment, control measures, incident reporting

**Owns**:
- Workplace safety assessment workflows
- Control measure tracking and effectiveness
- Workplace incident reporting
- Safety compliance tracking
- Occupational health and safety workflows

**Dependencies**:
- **Control Library**: Uses shared control models (read-only)
- **Integration Map**: Uses INTEGRATED_ISMS_MODULE_INTEGRATION_MAP_v1.0.md

**Boundaries**:
- ✅ Can assess workplace safety risks
- ✅ Can track control measure effectiveness
- ❌ Cannot modify cyber security threat/vulnerability data
- ❌ Cannot modify enterprise risk matrices (ERM responsibility)
- ✅ Can use control library for workplace controls

---

## 3. System-Level Components

### Architecture Layer
**Path**: `architecture/`  
**Owner**: Architecture Builder (`builder-architecture`)  
**Purpose**: System-level architecture, integration specifications, shared models

**Owns**:
- System architecture documentation
- Integration maps and API contracts
- Control library and efficacy models
- Cross-module integration patterns

**Responsibilities**:
- Define API contracts between modules
- Maintain integration maps
- Ensure architectural consistency
- Design cross-module workflows

**Boundaries**:
- ✅ Can design integration patterns
- ✅ Can define API contracts
- ❌ Cannot implement module-specific features
- ❌ Cannot modify module internals without approval

---

### Shared Components
**Path**: `shared/`  
**Owner**: Multiple builders (collaborative)  
**Purpose**: Shared libraries, utilities, and components used across modules

**Includes**:
- **UI Components**: Reusable UI elements
- **API Client**: Shared API communication layer
- **Authentication**: Shared auth/authorization
- **Utilities**: Common utility functions

**Governance**:
- Changes require Architecture Builder review
- Must maintain backward compatibility
- Cannot introduce module-specific logic

---

## 4. Integration Points and Data Flow

### Integration Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     API Gateway / Integration Layer             │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
    ┌─────▼─────┐      ┌─────▼─────┐      ┌─────▼─────┐
    │    ERM    │◄────►│   Threat  │◄────►│   Vuln    │
    └───────────┘      └───────────┘      └───────────┘
          │                   │                   │
          │                   │                   │
    ┌─────▼─────┐      ┌─────▼─────┐      ┌─────▼─────┐
    │   Risk    │      │    PIT    │      │  Course   │
    │Assessment │      │           │      │  Crafter  │
    └───────────┘      └───────────┘      └───────────┘
          │
    ┌─────▼─────┐
    │   WRAC    │
    └───────────┘
```

### Key Integration Patterns

1. **Risk Data Flow**: Risk Assessment → ERM → Reporting
2. **Threat-Vulnerability Correlation**: Threat ↔ Vulnerability (bidirectional)
3. **Risk Scoring**: ERM ← (Threat + Vulnerability + Risk Assessment)
4. **Training Content Generation**: Course Crafter ← ERM (reads risk data)
5. **Project Context**: PIT ← (Threat + Vulnerability) (reads context data)

### Integration Rules

✅ **Allowed**:
- API-based data access between modules
- Read-only access to other module data via APIs
- Event-based notifications between modules
- Shared component usage

❌ **Forbidden**:
- Direct database access across modules
- Modifying other module's data without API
- Bypassing integration layer
- Tight coupling between modules

---

## 5. Governance Structure

### Documentation Hierarchy

```
Level 1: Master References (Highest Authority)
├── SRMF_MASTER_BUILD_REFERENCE_v1.0.md
├── Maturion Build Philosophy
└── Integrated_ISMS_Architecture_v1.1.md

Level 2: Module True North (Module Authority)
├── COURSE_CRAFTER_TRUE_NORTH_v1.0.md
├── ERM_TRUE_NORTH_v1.0.md
├── PIT_TRUE_NORTH_v1.0.md
├── THREAT_TRUE_NORTH_v1.0.md
├── VULNERABILITY_TRUE_NORTH_v1.0.md
├── RISK_ASSESSMENT_TRUE_NORTH_v1.1.md
└── WRAC_TRUE_NORTH_v0.1.md

Level 3: Integration Specifications (Cross-Module Authority)
├── INTEGRATED_ISMS_MODULE_INTEGRATION_MAP_v1.0.md
├── [Module]_INTEGRATION_MAP_v1.0.md
└── API Contracts

Level 4: Implementation Guides (Implementation Authority)
├── [Module]_IMPLEMENTATION_GUIDE_v1.0.md
├── [Module]_DATABASE_SCHEMA_v1.x.md
├── [Module]_EDGE_FUNCTIONS_v1.x.md
└── [Module]_FRONTEND_COMPONENT_MAP_v1.x.md

Level 5: Quality Assurance (Quality Authority)
├── [Module]_QA_IMPLEMENTATION_PLAN_v1.x.md
├── [Module]_WATCHDOG_LOGIC_v1.0.md (for PIT, Threat, Vulnerability)
└── [Module]_MODEL_ROUTING_SPEC_v1.0.md (for AI-enabled modules)
```

### Governance Authority

**Maturion Foreman** enforces:
- SRMF Master Build Reference compliance
- Module boundary adherence
- Integration map accuracy
- QA checklist completion
- Zero regression principle

**Module Owners** (Builders) decide:
- Internal module design
- Implementation approaches
- Module-specific optimizations
- Feature prioritization within module

**Architecture Builder** coordinates:
- Cross-module integrations
- API contract definitions
- System-level architecture changes
- Integration pattern design

---

## 6. Module Ownership Summary

| Module | Path | Owner Builder | Key Docs | AI-Enabled |
|--------|------|---------------|----------|------------|
| Course Crafter | `apps/course-crafter/` | builder-course-crafter | COURSE_CRAFTER_TRUE_NORTH_v1.0.md | No |
| ERM | `apps/erm/` | builder-erm | ERM_TRUE_NORTH_v1.0.md | No |
| PIT | `apps/pit/` | builder-pit | PIT_TRUE_NORTH_v1.0.md, PIT_WATCHDOG_LOGIC_v1.0.md, PIT_MODEL_ROUTING_SPEC_v1.0.md | Yes |
| Threat | `apps/threat/` | builder-threat | THREAT_TRUE_NORTH_v1.0.md, THREAT_WATCHDOG_LOGIC_v1.0.md, THREAT_MODEL_ROUTING_SPEC_v1.0.md | Yes |
| Vulnerability | `apps/vulnerability/` | builder-vulnerability | VULNERABILITY_TRUE_NORTH_v1.0.md, VULNERABILITY_WATCHDOG_LOGIC_v1.0.md, VULNERABILITY_MODEL_ROUTING_SPEC_v1.0.md | Yes |
| Risk Assessment | `apps/risk-assessment/` | builder-risk-assessment | RISK_ASSESSMENT_TRUE_NORTH_v1.1.md | No |
| WRAC | `apps/wrac/` | builder-wrac | WRAC_TRUE_NORTH_v0.1.md | No |
| Architecture | `architecture/` | builder-architecture | SRMF_MASTER_BUILD_REFERENCE_v1.0.md, Integrated_ISMS_Architecture_v1.1.md | N/A |

---

## 7. Change Management Process

### Proposing Changes

1. **Module-Level Changes**:
   - Proposed by: Module owner builder
   - Reviewed by: Maturion Foreman
   - Approved by: Maturion Foreman (if aligned with governance)

2. **Cross-Module Changes**:
   - Proposed by: Architecture Builder
   - Reviewed by: Affected module builders + Maturion Foreman
   - Approved by: Maturion Foreman

3. **Governance Changes**:
   - Proposed by: Maturion Foreman or human authority
   - Reviewed by: All stakeholders
   - Approved by: Human authority

### Change Validation

All changes must:
- ✅ Align with SRMF Master Build Reference
- ✅ Respect module boundaries
- ✅ Pass module QA checklist
- ✅ Maintain zero regression
- ✅ Update relevant documentation
- ✅ Follow integration map patterns

---

## 8. Quick Reference

### Finding Module Information

**Question**: "Which module handles X?"
- **Risk matrices/heatmaps**: ERM
- **Threat intelligence**: Threat module
- **Vulnerability scanning**: Vulnerability module
- **Risk assessments**: Risk Assessment module
- **Project tracking**: PIT module
- **Training content**: Course Crafter module
- **Workplace safety**: WRAC module

**Question**: "How do modules communicate?"
- **Answer**: Via API contracts defined in INTEGRATED_ISMS_MODULE_INTEGRATION_MAP_v1.0.md

**Question**: "Who approves architectural changes?"
- **Answer**: Maturion Foreman for governance compliance, Architecture Builder for design

**Question**: "Where are watchdog rules?"
- **Answer**: PIT_WATCHDOG_LOGIC_v1.0.md, THREAT_WATCHDOG_LOGIC_v1.0.md, VULNERABILITY_WATCHDOG_LOGIC_v1.0.md

**Question**: "Where are AI routing rules?"
- **Answer**: PIT_MODEL_ROUTING_SPEC_v1.0.md, THREAT_MODEL_ROUTING_SPEC_v1.0.md, VULNERABILITY_MODEL_ROUTING_SPEC_v1.0.md

---

## Version Control

**Document Version**: 1.0  
**Last Updated**: 2025-12-03  
**Maintained By**: Maturion Foreman  
**Review Cycle**: Quarterly or when significant structural changes occur

---

**Maturion Foreman** - Mapping the ISMS Ecosystem with Precision and Clarity
