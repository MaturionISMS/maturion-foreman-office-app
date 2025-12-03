# Quick Reference Guide - Maturion ISMS Architecture

## 🚀 Getting Started

### I want to understand the overall system
Start here:
1. [Integrated ISMS Architecture](architecture/system-architecture/Integrated_ISMS_Architecture_v1.1.md) - The big picture
2. [Module Integration Map](architecture/integration-maps/INTEGRATED_ISMS_MODULE_INTEGRATION_MAP_v1.0.md) - How modules connect
3. [Complete Document Index](DOCUMENT_INDEX.md) - All 114 documents organized

### I want to work on a specific module
Navigate to `/apps/{module-name}/` and start with:
- **Architecture folder** - Read the True North document first
- **Implementation folder** - Implementation guide for building
- **Schemas folder** - Database and API specifications
- **QA Plans folder** - Testing requirements

## 📚 Document Type Quick Guide

| Document Type | What It Contains | Where to Find It |
|--------------|------------------|------------------|
| **True North** | Module vision, domain model, core principles | `architecture/` folder |
| **Database Schema** | Tables, relationships, indexes | `schemas/` folder |
| **Edge Functions** | API specifications, endpoints | `schemas/` folder |
| **Frontend Component Map** | UI component hierarchy | `frontend/` folder |
| **Wireframes** | ASCII UI layouts | `frontend/` folder |
| **QA Plan** | Testing procedures, quality gates | `qa-plans/` folder |
| **Implementation Guide** | Build instructions, governance | `implementation/` folder |
| **Sprint Plan** | Development roadmap, timelines | `sprints/` folder |
| **Watchdog Logic** | Automated governance rules | `watchdog/` folder (PIT, Threat, Vulnerability only) |
| **Routing Spec** | AI model orchestration | `routing/` folder (PIT, Threat, Vulnerability only) |

## 🎯 Common Tasks

### Building a New Module Feature
1. Read the True North (in `architecture/`)
2. Review the Database Schema (in `schemas/`)
3. Check the Edge Functions spec (in `schemas/`)
4. Review the Frontend Component Map (in `frontend/`)
5. Follow the Implementation Guide (in `implementation/`)
6. Run tests per the QA Plan (in `qa-plans/`)

### Understanding Module Integration
1. Read the system-level [Integration Map](architecture/integration-maps/INTEGRATED_ISMS_MODULE_INTEGRATION_MAP_v1.0.md)
2. Check module-specific Integration Spec (in module's `schemas/` folder if it exists)
3. Review the SRMF Master Build Reference for framework context

### Setting Up Quality Assurance
1. Review the module's QA Plan (in `qa-plans/`)
2. For modules with Watchdog: Review watchdog logic (in `watchdog/`)
3. Check the Implementation Guide for governance rules

### Working with AI Features
For modules with AI capabilities (PIT, Threat, Vulnerability):
1. Review the Model Routing Spec (in `routing/`)
2. Check the Watchdog Logic for AI oversight rules
3. Review Edge Functions for AI gateway endpoints

## 📍 Module Overview

### System-Level (`/architecture/`)
- **Purpose**: Cross-module architecture and models
- **5 documents** covering system architecture, integration, and controls

### Course Crafter (`/apps/course-crafter/`)
- **Purpose**: Video course production platform
- **12 documents** - Full E1-E4 engine suite
- **Key Feature**: Multi-engine content factory

### ERM (`/apps/erm/`)
- **Purpose**: Enterprise risk management
- **18 documents** - Most comprehensive module
- **Key Feature**: Risk matrices, scales, and heatmaps

### PIT (`/apps/pit/`)
- **Purpose**: Project implementation tracking
- **20 documents** including watchdog and routing
- **Key Features**: Automated governance, AI-driven corrections

### Risk Assessment (`/apps/risk-assessment/`)
- **Purpose**: Risk assessment workflows
- **11 documents** - Assessment methodology and tools

### Threat (`/apps/threat/`)
- **Purpose**: Threat identification and management
- **19 documents** including watchdog and routing
- **Key Features**: Threat intelligence, AI analysis

### Vulnerability (`/apps/vulnerability/`)
- **Purpose**: Vulnerability tracking and remediation
- **19 documents** including watchdog and routing
- **Key Features**: Vulnerability scanning, remediation tracking

### WRAC (`/apps/wrac/`)
- **Purpose**: Workplace risk and controls
- **10 documents** - Safety and workplace controls
- **Key Feature**: Physical safety and control management

## 🔍 Finding Specific Information

### Database Changes
Look in: `{module}/schemas/{MODULE}_DATABASE_SCHEMA_v*.md`

### API Endpoints
Look in: `{module}/schemas/{MODULE}_EDGE_FUNCTIONS_v*.md`

### UI Changes
Look in:
- `{module}/frontend/{MODULE}_FRONTEND_COMPONENT_MAP_v*.md` (component structure)
- `{module}/frontend/{MODULE}_WIREFRAMES_v*.md` (layouts)

### Testing Requirements
Look in: `{module}/qa-plans/{MODULE}_QA_IMPLEMENTATION_PLAN_v*.md`

### Development Timeline
Look in: `{module}/sprints/{MODULE}_SPRINT_PLAN_v*.md`

### AI Model Selection
Look in: `{module}/routing/{MODULE}_MODEL_ROUTING_SPEC_v*.md` (PIT, Threat, Vulnerability only)

### Automated Checks
Look in: `{module}/watchdog/{MODULE}_WATCHDOG_LOGIC_v*.md` (PIT, Threat, Vulnerability only)

## 📋 Version Guide

- **v0.1** = Initial draft/early version
- **v1.0** = First stable release
- **v1.1** = Refined/updated stable version

When multiple versions exist, generally prefer the highest version number, but check changelog for context.

## 🤝 Contributing

Before making changes:
1. Review the relevant True North document
2. Check the Implementation Guide for governance rules
3. Verify against the QA Plan
4. Update corresponding architecture documents

All implementations must align with architecture documents. No deviation without updating the docs first.

## 📞 Support & Questions

For questions about:
- **System Architecture** → Review [Integrated ISMS Architecture](architecture/system-architecture/Integrated_ISMS_Architecture_v1.1.md)
- **Module Integration** → Review [Integration Map](architecture/integration-maps/INTEGRATED_ISMS_MODULE_INTEGRATION_MAP_v1.0.md)
- **Specific Module** → Start with that module's True North in `apps/{module}/architecture/`
- **Controls & Models** → Review [Control Library](architecture/control-models/CONTROL_LIBRARY_v0.1.md)

---

**Quick Access:**
- [Full Document Index](DOCUMENT_INDEX.md) - All 114 documents
- [Organization Guide](ARCHITECTURE_ORGANIZATION.md) - Detailed structure explanation
- [Main README](../README.md) - Repository overview
