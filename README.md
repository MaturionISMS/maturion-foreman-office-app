# Maturion AI Foreman

This is the Foreman repository that is responsible for managing all builder agents and maintaining the complete architecture documentation for the Maturion Integrated Security Management System (ISMS).

## What is the Foreman?

The Maturion Foreman is an AI-powered orchestration system that:
- Manages and coordinates builder agents for ISMS module development
- Maintains architectural integrity across all modules
- Enforces quality standards and compliance
- Provides centralized architecture documentation

## Repository Structure

### `/foreman/` - Foreman Core Systems
Builder agent management, initialization, and operational frameworks.

See:
- [Builder Initialization](foreman/BUILDER_INITIALIZATION.md)
- [Builder Registry Quick Reference](foreman/BUILDER_REGISTRY_QUICK_REFERENCE.md)
- [Implementation Summary](foreman/IMPLEMENTATION_SUMMARY.md)

### `/maturion-isms/` - Complete ISMS Architecture
All architecture documentation organized by:
- **System-level architecture** (`/architecture/`) - System-wide specifications  
- **Application modules** (`/apps/`) - Module-specific documentation

For detailed information about the organization and contents, see [ARCHITECTURE_ORGANIZATION.md](maturion-isms/ARCHITECTURE_ORGANIZATION.md).

### Architecture Indexing & Search
- [Architecture Indexing System](ARCHITECTURE_INDEXING_README.md) - Automated architecture document indexing
- [Architecture Index](ARCHITECTURE_INDEX.json) - Searchable index of all architecture files
- [Quick Start Guide](ARCHITECTURE_INDEX_QUICK_START.md) - Get started with architecture search
- [Index Report](ARCHITECTURE_INDEX_REPORT.md) - Latest indexing results

### Validation & QA Tools
- [Repository Validation Tool](VALIDATION_TOOL_README.md) - Automated repository validation
- [Validation Report](VALIDATION_REPORT.md) - Latest validation results
- [Validation Summary](VALIDATION_SUMMARY.md) - Validation overview

## Quick Navigation

### Foreman Operations
- [Builder Agent Registry](foreman/builder-registry-report.md)
- [Builder Initialization](foreman/init_builders.py)
- [Architecture Indexing](index-isms-architecture.py) - Index and search architecture documents
- [QA Engine Documentation](foreman/qa/) (if applicable)

### System Architecture
- [Integrated ISMS Architecture](maturion-isms/architecture/system-architecture/Integrated_ISMS_Architecture_v1.1.md)
- [Module Integration Map](maturion-isms/architecture/integration-maps/INTEGRATED_ISMS_MODULE_INTEGRATION_MAP_v1.0.md)
- [Control Library](maturion-isms/architecture/control-models/CONTROL_LIBRARY_v0.1.md)

### Application Modules
- [Course Crafter](maturion-isms/apps/course-crafter/) - Video course production platform
- [ERM](maturion-isms/apps/erm/) - Enterprise Risk Management
- [PIT](maturion-isms/apps/pit/) - Project Implementation Tracker
- [Risk Assessment](maturion-isms/apps/risk-assessment/) - Risk assessment module
- [Threat](maturion-isms/apps/threat/) - Threat management module
- [Vulnerability](maturion-isms/apps/vulnerability/) - Vulnerability management module
- [WRAC](maturion-isms/apps/wrac/) - Workplace Risk Assessment & Controls

## Architecture Organization

All 114 architecture documents have been organized into a structured hierarchy:
- System-level documents in `/maturion-isms/architecture/`
- Module-specific documents in `/maturion-isms/apps/{module-name}/`

Each module contains:
- Architecture (True North documents)
- Schemas (Database, APIs, Edge Functions)
- QA Plans
- Implementation Guides
- Frontend Specifications (Component Maps, Wireframes)
- Sprint Plans
- Special features (Watchdog logic, AI routing where applicable)

For complete details, see the [Architecture Organization Guide](maturion-isms/ARCHITECTURE_ORGANIZATION.md).

## Getting Started

1. **For Builder Agents**: See [Builder Initialization](foreman/BUILDER_INITIALIZATION.md)
2. **For Architecture Review**: Start with [Architecture Organization](maturion-isms/ARCHITECTURE_ORGANIZATION.md)
3. **For Architecture Search**: Use the [Architecture Indexing System](ARCHITECTURE_INDEXING_README.md) or run `python index-isms-architecture.py`
4. **For Repository Validation**: Run `python validate-repository.py`
5. **For Module Development**: Review the specific module's True North document in `maturion-isms/apps/{module}/architecture/`
