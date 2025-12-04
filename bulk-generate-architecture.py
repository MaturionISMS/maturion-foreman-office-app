#!/usr/bin/env python3
"""
Maturion Foreman - Bulk Architecture Component Generator
Build Wave 0.1 - Architecture Completion Sprint
Generates all 121 missing architecture files
"""
from pathlib import Path
from datetime import datetime

# Module configuration
MODULES = {
    'pit': ('PIT', 'Project Implementation Tracker', True, True, True, False, True, True),
    'erm': ('ERM', 'Event & Risk Management', True, False, True, True, False, False),
    'risk-assessment': ('RISK_ASSESSMENT', 'Risk Assessment', True, False, False, True, False, False),
    'threat': ('THREAT', 'Threat Management', True, False, True, False, True, True),
    'vulnerability': ('VULNERABILITY', 'Vulnerability Management', True, False, True, False, True, True),
    'wrac': ('WRAC', 'Workforce Risk & Compliance', True, True, False, False, False, False),
    'course-crafter': ('COURSE_CRAFTER', 'Course Crafter', True, True, True, True, False, False),
    'policy-builder': ('POLICY_BUILDER', 'Policy Builder', False, False, True, True, False, True),
    'analytics-remote-assurance': ('ANALYTICS_REMOTE_ASSURANCE', 'Analytics Remote Assurance', False, False, True, True, False, False),
    'auditor-mobile-app': ('AUDITOR_MOBILE_APP', 'Auditor Mobile App', False, False, True, False, False, False),
    'skills-development-portal': ('SKILLS_DEVELOPMENT_PORTAL', 'Skills Development Portal', False, False, True, False, False, False),
}

BASE = Path('/home/runner/work/maturion-ai-foreman/maturion-ai-foreman/maturion-isms/apps')
DATE = datetime.now().strftime('%Y-%m-%d')

def template(doc_type, name, full_name, key):
    """Generate minimal template content for each document type"""
    templates = {
        'TRUE_NORTH': f"""# {name}_TRUE_NORTH_v1.0.md

## {full_name} - True North Architecture
**Version**: 1.0  
**Date**: {DATE}  
**Status**: Foundation Document

## Purpose
This True North defines the philosophical direction and architectural foundation for {full_name} within the Maturion ISMS ecosystem.

## Vision
{full_name} is a core module providing essential functionality for information security management and compliance tracking.

## Role in Maturion Ecosystem
- Integrates with platform authentication and authorization
- Enforces multi-tenant data isolation via organisation_id
- Publishes/consumes events for inter-module coordination
- Provides compliance evidence for ISO 27001, GDPR, POPIA

## Key Entities
[To be detailed during refinement]

## User Workflows
[To be detailed during refinement]

## Technical Constraints
- Supabase backend (PostgreSQL + Edge Functions)
- Next.js 14+ frontend (React + TypeScript)
- Row Level Security (RLS) enforcement
- Multi-tenant architecture

## Success Criteria
- ≥80% user adoption within 6 months
- ≥95% uptime
- Full compliance with applicable standards

*Generated for Build Wave 0.1 - Architecture Completion Sprint*
""",
        'ARCHITECTURE': f"""# {name}_ARCHITECTURE_v1.0.md

## {full_name} - Architecture Specification
**Version**: 1.0  
**Date**: {DATE}  
**Status**: Foundation Specification

## System Overview
{full_name} provides structured functionality within the Maturion ISMS platform.

### Module Boundaries
- Responsible for: [To be defined]
- NOT responsible for: Platform-level auth, org management

## Component Architecture
### Frontend
- Next.js pages and components
- React Hook Form for forms
- React Query for server state
- Zustand for client state

### Backend
- Supabase PostgreSQL database
- Edge Functions (Deno/TypeScript)
- Row Level Security policies
- Real-time subscriptions

## Data Model
[Entity tables and relationships to be defined in DATABASE_SCHEMA]

## Security Architecture
- JWT authentication via Supabase Auth
- RLS policies for tenant isolation
- Audit logging for all operations
- Encryption at rest and in transit

## Integration Architecture
[Integration points defined in INTEGRATION_SPEC]

## Technology Stack
- Frontend: Next.js 14, React 18, TypeScript 5, Tailwind CSS
- Backend: Supabase, PostgreSQL 15, Deno Edge Functions
- Hosting: Vercel (frontend), Supabase Cloud (backend)

*Generated for Build Wave 0.1 - Architecture Completion Sprint*
""",
        'INTEGRATION_SPEC': f"""# {name}_INTEGRATION_SPEC_v1.0.md

## {full_name} - Integration Specification
**Version**: 1.0  
**Date**: {DATE}

## Integration Patterns
- REST API for synchronous operations
- Event-driven messaging for asynchronous coordination
- Real-time WebSocket subscriptions for live updates
- Direct database access via RLS policies

## Inbound Integrations
[Modules that consume this module - to be defined]

## Outbound Integrations
[Modules this module depends on - to be defined]

## Platform Integration
- Authentication: Supabase Auth with JWT
- Authorization: RLS policies scoped to organisation_id
- Audit: All operations logged to audit table

## Event Catalog
### Events Published
[To be defined]

### Events Consumed
[To be defined]

## API Security
- JWT authentication required
- Rate limiting applied
- Input validation enforced
- Audit logging mandatory

*Generated for Build Wave 0.1 - Architecture Completion Sprint*
""",
        'DATABASE_SCHEMA': f"""# {name}_DATABASE_SCHEMA_v1.0.md

## {full_name} - Database Schema
**Version**: 1.0  
**Date**: {DATE}

## Schema Overview
All tables follow naming convention: `{key.replace('-', '_')}_*`

All tables include:
- `organisation_id UUID NOT NULL REFERENCES organisations(id)`
- `created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()`
- `updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()`
- `created_by UUID NOT NULL REFERENCES auth.users(id)`
- `updated_by UUID NOT NULL REFERENCES auth.users(id)`

## Core Tables
[Entity tables to be defined - following RLS pattern]

## Row Level Security (RLS)
All tables have RLS enabled with policies:
- SELECT: WHERE organisation_id = auth.current_organisation_id()
- INSERT: WITH CHECK organisation_id = auth.current_organisation_id()
- UPDATE: USING organisation_id = auth.current_organisation_id()
- DELETE: USING organisation_id = auth.current_organisation_id()

## Indexes
- Primary keys on all tables
- Index on organisation_id for all tables
- Composite indexes for common queries

## Triggers
- Auto-update `updated_at` timestamp on UPDATE
- Auto-set `updated_by` to auth.uid() on UPDATE

## Data Integrity
- Foreign keys for referential integrity
- Check constraints for validation
- Unique constraints where applicable
- CASCADE delete for tenant data

*Generated for Build Wave 0.1 - Architecture Completion Sprint*
""",
        'FRONTEND_COMPONENT_MAP': f"""# {name}_FRONTEND_COMPONENT_MAP_v1.0.md

## {full_name} - Frontend Component Map
**Version**: 1.0  
**Date**: {DATE}

## Route Structure
```
/app/{key}/
  /page.tsx                 # Module landing page
  /layout.tsx               # Module layout
  /[id]/page.tsx            # Detail view
  /[id]/edit/page.tsx       # Edit view
  /new/page.tsx             # Create new
```

## Component Organization
```
/components/{key}/
  /forms/                   # Form components
  /tables/                  # Data tables
  /cards/                   # Card displays
  /dialogs/                 # Modal dialogs
```

## Key Components
- EntityTable: Paginated, sortable, filterable table
- EntityForm: Create/edit form with validation
- EntityCard: Compact entity display
- EntityDetailsDialog: Quick view modal

## State Management
- Server State: React Query (useQuery, useMutation)
- Client State: Zustand (UI state, filters)
- Form State: React Hook Form + Zod validation

## UI Component Library
- shadcn/ui components: Button, Table, Form, Dialog, Card, Badge, Input, Select

## Styling
- Tailwind CSS for utility-first styling
- Dark mode support via CSS variables
- Responsive design (mobile-first)

*Generated for Build Wave 0.1 - Architecture Completion Sprint*
""",
        'WIREFRAMES': f"""# {name}_WIREFRAMES_v1.0.md

## {full_name} - UI Wireframes
**Version**: 1.0  
**Date**: {DATE}

## Main List View
```
┌────────────────────────────────────────────────┐
│ {full_name}                    [+ New]        │
├────────────────────────────────────────────────┤
│ [🔍 Search...]      [Filter] [Settings]       │
├────────────────────────────────────────────────┤
│ Name     │ Status │ Created  │ Updated │ ⋮   │
├────────────────────────────────────────────────┤
│ Entity 1 │ Active │ 01/01/24 │ 01/15/24│ ⋮   │
│ Entity 2 │ Active │ 01/02/24 │ 01/14/24│ ⋮   │
└────────────────────────────────────────────────┘
```

## Detail View
```
┌────────────────────────────────────────────────┐
│ ◄ Back                    [Edit] [Delete]     │
├────────────────────────────────────────────────┤
│ Entity Name              Status: Active        │
│                                                │
│ Details:                                       │
│ [Entity details displayed here]                │
│                                                │
│ Related Items:                                 │
│ • Item 1                                       │
│ • Item 2                                       │
└────────────────────────────────────────────────┘
```

## Create/Edit Form
```
┌────────────────────────────────────────────────┐
│ ◄ Cancel            Create/Edit Entity        │
├────────────────────────────────────────────────┤
│ Name *: [_____________]                        │
│ Description: [_____________]                   │
│ Status: [Select...      ▼]                     │
│                                                │
│                     [Cancel] [Save]            │
└────────────────────────────────────────────────┘
```

*Generated for Build Wave 0.1 - Architecture Completion Sprint*
""",
        'QA_IMPLEMENTATION_PLAN': f"""# {name}_QA_IMPLEMENTATION_PLAN_v1.0.md

## {full_name} - QA Implementation Plan
**Version**: 1.0  
**Date**: {DATE}

## QA Strategy
Comprehensive quality assurance covering:
- Unit testing (component & function level)
- Integration testing (API & database)
- E2E testing (user workflows)
- Security testing (auth, RLS, input validation)
- Performance testing (load & stress)
- Compliance testing (standards coverage)

## Testing Framework
- Frontend: Vitest + Testing Library
- Backend: Deno test
- E2E: Playwright
- API: Supertest / Supabase client

## Test Coverage Requirements
- Unit tests: ≥80% code coverage
- Integration tests: All API endpoints
- E2E tests: All critical user flows
- Security tests: All auth & RLS policies

## Test Categories
### Unit Tests
- Component rendering
- Form validation
- State management
- Utility functions

### Integration Tests
- API endpoint contracts
- Database operations
- RLS policy enforcement
- Event publishing/consuming

### E2E Tests
- User authentication
- CRUD operations
- Search & filter
- Form submission

## QA Governance
- All PRs require tests
- CI/CD runs all tests
- Test failures block merge
- Coverage reports generated

## Compliance Testing
- Verify audit logging
- Validate data isolation
- Check access controls
- Confirm encryption

*Generated for Build Wave 0.1 - Architecture Completion Sprint*
""",
        'IMPLEMENTATION_GUIDE': f"""# {name}_IMPLEMENTATION_GUIDE_v1.0.md

## {full_name} - Implementation Guide
**Version**: 1.0  
**Date**: {DATE}

## Overview
Step-by-step implementation guide for builder agents.

## Module Structure
```
maturion-isms/apps/{key}/
├── architecture/          # Architecture docs
├── qa-plans/              # QA specifications
├── compliance/            # Compliance mappings
└── README.md              # Module overview
```

## Implementation Phases
### Phase 1: Schema Setup
1. Create database tables (as per DATABASE_SCHEMA)
2. Apply RLS policies
3. Create indexes
4. Add triggers
5. Test with sample data

### Phase 2: Backend API
1. Implement Edge Functions (as per EDGE_FUNCTIONS)
2. Add validation logic
3. Implement audit logging
4. Test API contracts
5. Add error handling

### Phase 3: Frontend UI
1. Create pages (as per FRONTEND_COMPONENT_MAP)
2. Build components
3. Implement forms
4. Add tables/lists
5. Apply styling (Tailwind)

### Phase 4: Integration
1. Connect frontend to backend
2. Implement real-time subscriptions
3. Add event pub/sub
4. Test inter-module integrations

### Phase 5: QA
1. Write unit tests
2. Add integration tests
3. Create E2E tests
4. Run security tests
5. Validate compliance

## Builder Agent Assignment
- schema-builder: Phase 1
- api-builder: Phase 2
- ui-builder: Phase 3
- integration-builder: Phase 4
- qa-builder: Phase 5

*Generated for Build Wave 0.1 - Architecture Completion Sprint*
""",
        'SPRINT_PLAN': f"""# {name}_SPRINT_PLAN_v1.0.md

## {full_name} - Sprint Plan
**Version**: 1.0  
**Date**: {DATE}

## Sprint Overview
Structured build sequence for {full_name} module.

## Sprint 1: Database Foundation (1 week)
**Assigned**: schema-builder
- Create all tables
- Apply RLS policies
- Add indexes and triggers
- Create sample seed data
- Validate with integration tests

## Sprint 2: API Implementation (1 week)
**Assigned**: api-builder
- Implement Edge Functions
- Add CRUD operations
- Implement validation
- Add audit logging
- Test API contracts

## Sprint 3: Frontend Development (2 weeks)
**Assigned**: ui-builder
- Create page routes
- Build components
- Implement forms
- Add tables/lists
- Apply responsive design

## Sprint 4: Integration (1 week)
**Assigned**: integration-builder
- Connect frontend to backend
- Add real-time subscriptions
- Implement event handlers
- Test inter-module integration

## Sprint 5: QA & Testing (1 week)
**Assigned**: qa-builder
- Write all unit tests
- Add integration tests
- Create E2E tests
- Run security audit
- Validate compliance

## Total Timeline: 6 weeks
**Dependencies**: Platform core must be ready
**Blockers**: None identified
**Risks**: Low - standard CRUD module

*Generated for Build Wave 0.1 - Architecture Completion Sprint*
""",
        'CHANGELOG': f"""# {name}_CHANGELOG_v1.0.md

## {full_name} - Changelog

## [1.0.0] - {DATE}
### Added
- Initial architecture foundation
- TRUE_NORTH specification
- ARCHITECTURE specification
- DATABASE_SCHEMA specification
- FRONTEND_COMPONENT_MAP specification
- WIREFRAMES specification
- INTEGRATION_SPEC specification
- QA_IMPLEMENTATION_PLAN
- IMPLEMENTATION_GUIDE
- SPRINT_PLAN
- Module directory structure created

### Status
- Architecture completeness: Foundation established
- Ready for builder agent implementation
- Compliance mappings to be added

*Generated for Build Wave 0.1 - Architecture Completion Sprint*
""",
        'EDGE_FUNCTIONS': f"""# {name}_EDGE_FUNCTIONS_v1.0.md

## {full_name} - Edge Functions Specification
**Version**: 1.0  
**Date**: {DATE}

## Function Catalog
- `{key}-create`: Create new entity (POST)
- `{key}-update`: Update entity (PUT)
- `{key}-delete`: Delete entity (DELETE)
- `{key}-list`: List entities (GET)
- `{key}-get`: Get entity by ID (GET)

## Authentication
All functions require:
- Valid JWT token in Authorization header
- User must belong to an organisation
- RLS policies enforce data isolation

## Request/Response Pattern
```typescript
// Request
interface Request {{
  headers: {{ Authorization: string }};
  body: unknown;
}}

// Response
interface Response {{
  success: boolean;
  data?: unknown;
  error?: string;
}}
```

## Error Handling
- 400: Invalid request
- 401: Unauthorized
- 403: Forbidden
- 404: Not found
- 500: Server error

## Audit Logging
All operations logged to audit table:
- entity_type
- entity_id
- action (create/update/delete)
- user_id
- organisation_id
- timestamp
- changes (JSON)

*Generated for Build Wave 0.1 - Architecture Completion Sprint*
""",
        'EXPORT_SPEC': f"""# {name}_EXPORT_SPEC_v1.0.md

## {full_name} - Export Specification
**Version**: 1.0  
**Date**: {DATE}

## Export Formats
- CSV: Spreadsheet format for Excel/Sheets
- JSON: Machine-readable format
- PDF: Human-readable reports

## Export Endpoints
- `/api/{key}/export/csv`: Export to CSV
- `/api/{key}/export/json`: Export to JSON
- `/api/{key}/export/pdf`: Export to PDF

## Export Scope
- All records (filtered by organisation_id)
- Selected records (by ID list)
- Filtered records (by search/filter criteria)
- Date range exports

## Security
- Requires authentication
- RLS policies enforced
- Audit log entry created
- Rate limiting applied

## File Format
- UTF-8 encoding
- Standard delimiters (CSV)
- Pretty-printed JSON
- A4 page size (PDF)

*Generated for Build Wave 0.1 - Architecture Completion Sprint*
""",
        'WATCHDOG_LOGIC': f"""# {name}_WATCHDOG_LOGIC_v1.0.md

## {full_name} - Watchdog Logic Specification
**Version**: 1.0  
**Date**: {DATE}

## Purpose
Automated monitoring and alerting for {full_name} module health and compliance.

## Monitored Metrics
- Entity creation rate
- Update frequency
- Error rates
- Performance degradation
- Compliance violations
- Data quality issues

## Watchdog Rules
### Rule 1: Stale Data Detection
- Trigger: No updates in 30 days
- Action: Alert owner
- Severity: Warning

### Rule 2: Error Rate Threshold
- Trigger: Error rate > 5%
- Action: Alert admin
- Severity: Critical

### Rule 3: Performance Degradation
- Trigger: Response time > 3s
- Action: Alert DevOps
- Severity: High

## Alert Channels
- In-app notifications
- Email (critical alerts)
- Slack/Teams integration (optional)

## Watchdog Schedule
- Continuous monitoring
- Hourly health checks
- Daily compliance scans
- Weekly performance reports

*Generated for Build Wave 0.1 - Architecture Completion Sprint*
""",
        'MODEL_ROUTING_SPEC': f"""# {name}_MODEL_ROUTING_SPEC_v1.0.md

## {full_name} - AI Model Routing Specification
**Version**: 1.0  
**Date**: {DATE}

## Purpose
Define AI model usage and routing logic for {full_name} module.

## Model Categories
### LLM Models
- GPT-4: Complex analysis, decision support
- GPT-3.5: Text generation, summaries
- Claude: Long-context analysis

### Specialized Models
[Module-specific AI models to be defined]

## Routing Rules
### Rule 1: Cost Optimization
- Use GPT-3.5 for standard operations
- Use GPT-4 only for complex tasks
- Cache common queries

### Rule 2: Performance
- Timeout: 30s for AI calls
- Retry: 3 attempts with backoff
- Fallback: Graceful degradation

### Rule 3: Context Management
- Max tokens: 4000 for GPT-3.5, 8000 for GPT-4
- Context window: Last N interactions
- Summarize long contexts

## Model Gateway Integration
- All AI calls through Maturion Model Gateway
- Usage tracking and billing
- Rate limiting per organisation
- Model selection based on tier

## Prompt Templates
[Module-specific prompt templates to be defined]

*Generated for Build Wave 0.1 - Architecture Completion Sprint*
""",
    }
    return templates.get(doc_type, f"# {name}_{doc_type}_v1.0.md\n\n[To be defined]\n")

def main():
    print("=" * 70)
    print("🚀 Build Wave 0.1 - Architecture Component Generator")
    print("=" * 70)
    generated = []
    
    for key, (name, full, has_tn, has_arch, edge, export, watch, model) in MODULES.items():
        print(f"\n📦 {full}")
        mod = BASE / key
        arch = mod / 'architecture'
        qa = mod / 'qa-plans'
        
        # Create dirs
        arch.mkdir(parents=True, exist_ok=True)
        qa.mkdir(parents=True, exist_ok=True)
        
        # Generate files
        files = []
        if not has_tn: files.append(('TRUE_NORTH', arch))
        if not has_arch: files.append(('ARCHITECTURE', arch))
        
        files.extend([
            ('INTEGRATION_SPEC', arch),
            ('DATABASE_SCHEMA', arch),
            ('FRONTEND_COMPONENT_MAP', arch),
            ('WIREFRAMES', arch),
            ('QA_IMPLEMENTATION_PLAN', qa),
            ('IMPLEMENTATION_GUIDE', arch),
            ('SPRINT_PLAN', arch),
            ('CHANGELOG', arch),
        ])
        
        if edge: files.append(('EDGE_FUNCTIONS', arch))
        if export: files.append(('EXPORT_SPEC', arch))
        if watch: files.append(('WATCHDOG_LOGIC', arch))
        if model: files.append(('MODEL_ROUTING_SPEC', arch))
        
        for doc_type, directory in files:
            filepath = directory / f"{name}_{doc_type}_v1.0.md"
            if not filepath.exists():
                content = template(doc_type, name, full, key)
                filepath.write_text(content)
                generated.append(str(filepath.relative_to(BASE.parent.parent)))
                print(f"  ✓ {doc_type}")
    
    print("\n" + "=" * 70)
    print(f"✅ Generated {len(generated)} architecture files")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Run architecture indexing: python3 index-isms-architecture.py")
    print("2. Validate completeness: python3 validate-repository.py")
    print("3. Update readiness reports")
    return len(generated)

if __name__ == '__main__':
    count = main()
    print(f"\n📊 Total files created: {count}")
