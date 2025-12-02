# Maturion AI Foreman

This is the Foreman repository that is responsible for managing all builder agents and maintaining the complete architecture documentation for the Maturion Integrated Security Management System (ISMS).

## Repository Structure

### `/maturion-isms/` - Complete ISMS Architecture
This directory contains all architecture documentation organized by:
- **System-level architecture** (`/architecture/`) - System-wide specifications
- **Application modules** (`/apps/`) - Module-specific documentation

For detailed information about the organization and contents, see [ARCHITECTURE_ORGANIZATION.md](maturion-isms/ARCHITECTURE_ORGANIZATION.md).

### Quick Navigation

#### System Architecture
- [Integrated ISMS Architecture](maturion-isms/architecture/system-architecture/Integrated_ISMS_Architecture_v1.1.md)
- [Module Integration Map](maturion-isms/architecture/integration-maps/INTEGRATED_ISMS_MODULE_INTEGRATION_MAP_v1.0.md)
- [Control Library](maturion-isms/architecture/control-models/CONTROL_LIBRARY_v0.1.md)

#### Application Modules
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
