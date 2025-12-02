# Maturion ISMS Architecture Organization

## Overview
This directory contains the complete architecture documentation for the Maturion Integrated Security Management System (ISMS) and all its application modules.

## Directory Structure

### `/architecture/` - System-Level Architecture
Contains system-wide architecture documents that span across all modules.

#### `/architecture/system-architecture/`
- **Integrated_ISMS_Architecture_v1.1.md** - The overarching ISMS ecosystem architecture
- **SRMF_MASTER_BUILD_REFERENCE_v1.0.md** - Strategic Risk Management Framework master reference

#### `/architecture/integration-maps/`
- **INTEGRATED_ISMS_MODULE_INTEGRATION_MAP_v1.0.md** - Master integration blueprint for the entire ISMS ecosystem

#### `/architecture/control-models/`
- **CONTROL_LIBRARY_v0.1.md** - Master library of controls across organizations and risks
- **CONTROL_EFFICACY_MODEL_v0.1.md** - Control efficacy calculation model

### `/apps/` - Application Modules
Contains module-specific architecture documentation for each application in the ISMS.

Each module follows a consistent structure:

#### Standard Module Directories:
- **`architecture/`** - True North documents and architectural decisions
- **`schemas/`** - Database schemas, edge functions, export specs, integration specs
- **`qa-plans/`** - QA implementation and testing plans
- **`implementation/`** - Implementation guides and changelogs
- **`frontend/`** - Frontend component maps and wireframes
- **`sprints/`** - Sprint plans and development schedules

#### Special Module Directories (where applicable):
- **`watchdog/`** - Automated watchdog logic (PIT, Threat, Vulnerability)
- **`routing/`** - AI model routing specifications (PIT, Threat, Vulnerability)

## Application Modules

### 1. Course Crafter (`/apps/course-crafter/`)
Video course production platform with multi-engine content factory.
- **Purpose**: Transform raw materials into voice-over videos, explainer videos, and e-learning modules
- **Key Documents**: 12 files across 6 categories

### 2. ERM - Enterprise Risk Management (`/apps/erm/`)
Enterprise-wide risk management platform.
- **Purpose**: Manage risks across the entire organization
- **Key Documents**: 18 files including risk matrices, scales, and configuration

### 3. PIT - Project Implementation Tracker (`/apps/pit/`)
Project tracking with automated governance and early-warning systems.
- **Purpose**: Track project implementations with AI-driven corrections
- **Key Documents**: 20 files including watchdog logic and routing specs
- **Special Features**: Watchdog logic, AI model routing

### 4. Risk Assessment (`/apps/risk-assessment/`)
Risk assessment and analysis module.
- **Purpose**: Conduct and manage risk assessments
- **Key Documents**: 11 files across assessment workflows

### 5. Threat (`/apps/threat/`)
Threat identification and management module.
- **Purpose**: Identify, track, and manage security threats
- **Key Documents**: 19 files including watchdog and routing logic
- **Special Features**: Watchdog logic, AI model routing

### 6. Vulnerability (`/apps/vulnerability/`)
Vulnerability tracking and management module.
- **Purpose**: Track and manage security vulnerabilities
- **Key Documents**: 19 files including watchdog and routing logic
- **Special Features**: Watchdog logic, AI model routing

### 7. WRAC - Workplace Risk Assessment & Controls (`/apps/wrac/`)
Workplace safety and risk control management.
- **Purpose**: Manage workplace safety risks and controls
- **Key Documents**: 10 files covering safety controls and assessments

## Document Types Classification

### Architecture Documents
- True North documents (module vision and domain models)
- Architecture specifications
- System-wide architectural blueprints

### Schema Documents
- Database schemas
- Edge functions / API specifications
- Export specifications
- Integration specifications

### QA Documents
- QA implementation plans
- Test procedures and validation rules

### Implementation Documents
- Implementation guides
- Changelogs
- Development procedures

### Frontend Documents
- Frontend component maps
- ASCII wireframes
- UI specifications

### Sprint Documents
- Sprint plans
- Development schedules
- Delivery roadmaps

### Special Documents
- Watchdog logic (automated governance)
- Model routing specs (AI orchestration)
- Integration maps (cross-module connectivity)

## File Naming Convention

Files follow the pattern: `{MODULE}_{DOCUMENT_TYPE}_v{VERSION}.md`

Examples:
- `COURSE_CRAFTER_TRUE_NORTH_v1.0.md`
- `PIT_WATCHDOG_LOGIC_v1.0.md`
- `VULNERABILITY_DATABASE_SCHEMA_v1.1.md`

## Version Management

- **v0.1** - Initial/draft versions
- **v1.0** - First stable release
- **v1.1** - Updated/refined stable version

Multiple versions of the same document may coexist to track evolution.

## Integration Points

The system follows a hub-and-spoke architecture where:
- **Hub**: Integrated ISMS Core (central risk brain)
- **Spokes**: Individual modules (Course Crafter, ERM, PIT, etc.)

Refer to `/architecture/integration-maps/INTEGRATED_ISMS_MODULE_INTEGRATION_MAP_v1.0.md` for the complete integration architecture.

## Usage Guidelines

1. **For Developers**: Refer to module-specific architecture and implementation guides
2. **For QA Teams**: Use QA plans in each module's `qa-plans/` directory
3. **For Project Managers**: Review sprint plans in `sprints/` directories
4. **For Architects**: Start with system-level architecture documents
5. **For Foreman/Builder Agents**: Follow True North and implementation guides

## Document Authority

All documents in this structure are authoritative references. No implementation may deviate from these specifications without updating the corresponding architecture document.

---

**Total Files Organized**: 114 architecture documents
**Last Updated**: December 2, 2025
