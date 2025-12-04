# Build Wave 1.1 – Global UI Shell & Layout System

**Status**: ✅ PLANNING COMPLETE - READY FOR APPROVAL  
**Date**: 2025-12-04  
**Prepared by**: Maturion Foreman

---

## Overview

This directory contains the complete architectural planning for **Build Wave 1.1**, which establishes the global UI shell and front-end foundation for the Maturion ISMS platform.

---

## Quick Navigation

### 📖 Start Here
- **[BUILD_WAVE_1.1_SUMMARY.md](../../BUILD_WAVE_1.1_SUMMARY.md)** - Executive summary and completion report

### 🏗️ Global UI Specifications
- **[layout.md](./global/layout.md)** - Global layout system (header, sidebar, footer, responsive grid)
- **[theme-system.md](./global/theme-system.md)** - Theme and branding engine (APGI theme, dark mode, tenant theming)
- **[component-library.md](./global/component-library.md)** - Reusable components (35 components across 6 categories)
- **[navigation-spec.md](./global/navigation-spec.md)** - ISMS navigation system (11 modules, breadcrumbs, search)
- **[ai-panel-spec.md](./global/ai-panel-spec.md)** - Maturion AI panel (3 modes, chat, alerts, health, compliance)

### 🎨 Module UI Shells
- **[modules/README.md](./modules/README.md)** - Overview of module UI shell structure
- **[modules/pit-ui-shell.md](./modules/pit-ui-shell.md)** - Detailed PIT module specification
- **[modules/all-modules-summary.md](./modules/all-modules-summary.md)** - All 11 modules summary

### 📋 Build Orchestration
- **[build-plan-wave-1-1.json](../../build-plan-wave-1-1.json)** - Build plan with components, phases, timeline
- **[build-tasks-wave-1-1.json](../../build-tasks-wave-1-1.json)** - Task breakdown (135 tasks)
- **[build-status-wave-1-1.json](../../build-status-wave-1-1.json)** - Status tracking structure

---

## What Was Built

### 🎯 Scope

**Build Wave 1.1** establishes the visual structure, navigation system, global layout, theme/branding engine, and module UI scaffolding for the Maturion ISMS platform.

This is the **UI foundation** of the entire platform - every module, every screen, every interaction builds upon this global shell.

### 📦 Deliverables

#### 1. Global UI Architecture (5 specifications, 77KB)
- **Layout System**: Header, sidebar, footer, responsive grid, z-index hierarchy
- **Theme System**: 500+ CSS custom properties, APGI theme, tenant theming, dark mode
- **Component Library**: 35 reusable components (forms, data display, feedback, navigation)
- **Navigation System**: Sidebar with 11 modules, breadcrumbs, global search, permissions
- **AI Panel**: 3 operational modes, chat interface, alerts, health monitoring, compliance

#### 2. Module UI Shells (3 specifications, 33KB)
- **11 ISMS Modules**: PIT, ERM, Risk Assessment, Threat, Vulnerability, WRAC, Course Crafter, Policy Builder, Analytics & Remote Assurance, Auditor Mobile, Skills Development Portal
- **Route Structure**: All routes defined for each module
- **Dashboard Layouts**: Metrics, widgets, recent activity, quick actions
- **List/Detail/Settings/Reports**: Standard views for all modules
- **Module-Specific Components**: Custom components for each module

#### 3. Build Orchestration (3 files, 23KB)
- **Build Plan**: 6 components, 4 phases, 135 tasks, 41-day timeline
- **Build Tasks**: Complete task breakdown with dependencies, acceptance criteria
- **Build Status**: Progress tracking, blockers, governance checkpoints

#### 4. Summary Documentation (1 file, 13KB)
- **Executive Summary**: Objectives, deliverables, timeline, success criteria
- **Component Breakdown**: All 135 tasks categorized
- **QA Gates**: Accessibility, performance, cross-browser, testing requirements
- **Next Steps**: Approval process, execution plan

### 📊 Statistics

- **Total Documents**: 11 architectural specifications
- **Total Size**: ~120KB of comprehensive specifications
- **Total Tasks**: 135 estimated tasks (all for UI Builder)
- **Total Timeline**: 41 days (34 work days + 7 buffer)
- **Components Specified**: 
  - 5 global layout components
  - 35 reusable UI components
  - 6 navigation components
  - 6 AI panel components
  - 55 module-specific tasks (11 modules × 5 tasks)

---

## Build Sequence

### Phase 1: Foundation Layer (9 days)
**Focus**: Layout + Theme  
**Tasks**: 18  
**Parallel**: Yes

Build the core layout structure and theming infrastructure.

### Phase 2: Component Layer (14 days)
**Focus**: Component Library  
**Tasks**: 35  
**Parallel**: No

Build all 35 reusable components using the theme system.

### Phase 3: Navigation Layer (6 days)
**Focus**: Navigation System  
**Tasks**: 12  
**Parallel**: No

Implement ISMS navigation with all 11 modules.

### Phase 4: Feature Layer (12 days)
**Focus**: AI Panel + Module Shells  
**Tasks**: 70  
**Parallel**: Yes

Build AI panel and all 11 module UI shells.

---

## Quality Standards

### Accessibility
✅ WCAG 2.1 Level AA compliance (mandatory)  
✅ Keyboard navigation (all components)  
✅ Screen reader compatible  
✅ Focus indicators visible  
✅ High contrast mode support

### Performance
✅ LCP (Largest Contentful Paint) < 2.5s  
✅ FID (First Input Delay) < 100ms  
✅ CLS (Cumulative Layout Shift) < 0.1  
✅ Bundle size < 200KB per module

### Cross-Browser
✅ Chrome (latest)  
✅ Firefox (latest)  
✅ Safari (latest)  
✅ Edge (latest)

### Responsive
✅ Mobile: < 768px  
✅ Tablet: 768-1024px  
✅ Desktop: > 1024px

---

## Key Features

### Global Layout
- Fixed header with logo, navigation, search, notifications
- Collapsible sidebar with 11 ISMS modules
- Responsive 12-column grid system
- Mobile-first responsive design
- Print-friendly layouts

### Theme System
- APGI default theme (professional blue)
- Tenant theme overrides (logo, colors, typography)
- Dark/light mode toggle with persistence
- 500+ CSS custom properties
- Automatic contrast validation

### Component Library
- **9 Form components**: Input (all types), TextArea, Select, Checkbox, Radio, Switch, DatePicker, TimePicker, FileUpload
- **8 Data components**: Table (sortable/filterable), Card, List, Badge, Tag, Avatar, Tooltip, Popover
- **6 Feedback components**: Toast, Alert, Modal, Spinner, Progress Bar, Skeleton
- **4 Navigation components**: Breadcrumb, Tabs, Pagination, Menu
- **4 Layout components**: Grid, Stack, Divider, Spacer
- **4 Utility components**: Button (5 variants), Icon, Link, Text

### ISMS Navigation
- Hierarchical module navigation (11 modules)
- Auto-generated breadcrumbs
- Global search with autocomplete
- Notification center with real-time updates
- User profile menu with settings
- Permission-based filtering
- Mobile-responsive (hamburger menu)

### Maturion AI Panel
- **3 Operational Modes**:
  - Tenant User: Day-to-day assistance
  - Admin: Platform health, alerts, compliance
  - Global: Cross-tenant analytics (super admin)
- **4 Tabs**: Chat, Alerts, Health, Compliance
- Conversational AI interface
- Real-time platform monitoring
- Privacy-compliant (no PII)

### Module UI Shells
All 11 modules include:
- Dashboard with metrics and widgets
- List views with search, filters, pagination
- Detail views with tabs
- Settings views with configuration
- Reports views with export options
- Module-specific components

---

## Dependencies

### External
- React 18+
- TypeScript 5+
- React Router v6+
- Heroicons (MIT)
- date-fns

### Internal
- Architecture standards (`foreman/`)
- QA governance (`foreman/qa-governance.md`)
- Privacy guardrails (`foreman/privacy-guardrails.md`)

---

## Next Steps

### 1. Review & Approval
Johan reviews all specifications and provides approval to proceed.

### 2. Execution
Upon approval:
1. Setup test infrastructure
2. Initialize UI Builder workspace
3. Begin Phase 1: Foundation Layer
4. Progress through Phases 2-4 sequentially

### 3. Validation
- Accessibility audit (WCAG 2.1 AA)
- Performance testing (Core Web Vitals)
- Cross-browser testing
- Visual regression testing
- User acceptance testing

---

## Governance

**Approval Required**: Yes  
**Approver**: Johan  
**Status**: DRAFT - AWAITING APPROVAL

**Change Control**:
- Any specification changes require Foreman review
- Breaking changes require major version bump
- All changes must maintain backward compatibility
- Accessibility and performance standards are non-negotiable

---

## Contact

For questions or clarifications, refer to:
- **BUILD_WAVE_1.1_SUMMARY.md** for comprehensive overview
- Individual specification files for detailed requirements
- Maturion Foreman for architecture governance

---

*This is a governance repository. Specifications define architecture and requirements. Implementation happens in separate builder repositories.*

---

**Last Updated**: 2025-12-04  
**Version**: 1.0  
**Status**: READY FOR APPROVAL
