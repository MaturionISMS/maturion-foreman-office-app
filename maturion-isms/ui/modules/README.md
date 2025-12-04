# Maturion ISMS – Module UI Shell Specifications

**Version**: 1.0  
**Build Wave**: 1.1  
**Owner**: Maturion Foreman  
**Status**: DRAFT - AWAITING APPROVAL

---

## Purpose

This directory contains UI shell specifications for each of the 11 ISMS modules.

UI shell specifications define the visual structure, navigation, and placeholder components for each module **without implementing full functionality**.

---

## Module UI Shells

### Completed Modules
1. [PIT](./pit-ui-shell.md) - Personnel Information Tracker
2. [ERM](./erm-ui-shell.md) - Enterprise Risk Management
3. [Risk Assessment](./risk-assessment-ui-shell.md)
4. [Threat](./threat-ui-shell.md)
5. [Vulnerability](./vulnerability-ui-shell.md)
6. [WRAC](./wrac-ui-shell.md) - Workforce Risk Assessment & Control
7. [Course Crafter](./course-crafter-ui-shell.md)
8. [Policy Builder](./policy-builder-ui-shell.md)
9. [Analytics & Remote Assurance](./analytics-remote-assurance-ui-shell.md)
10. [Auditor Mobile](./auditor-mobile-ui-shell.md)
11. [Skills Development Portal](./skills-development-portal-ui-shell.md)

---

## UI Shell Structure

Each module UI shell specification includes:

### 1. Module Overview
- Module name and purpose
- Key user personas
- Primary workflows

### 2. Route Structure
- Root route
- Sub-routes (dashboard, lists, details, settings, reports)
- Route parameters

### 3. Navigation Structure
- Sidebar menu items
- Breadcrumb patterns
- Quick actions

### 4. Dashboard Shell
- Layout structure
- Widget placeholders
- Key metrics display

### 5. List View Shells
- Table structure
- Filters and search
- Actions and bulk operations

### 6. Detail View Shells
- Form layouts
- Tab structures
- Related data displays

### 7. Settings View Shells
- Configuration options
- Preferences
- Module-specific settings

### 8. Reports View Shells
- Report types
- Export options
- Visualization placeholders

### 9. UI Components
- Module-specific components
- Reusable patterns
- Custom widgets

### 10. Responsive Behavior
- Mobile adaptations
- Tablet optimizations
- Desktop layouts

---

## Common Patterns

### Dashboard Pattern
All modules follow a consistent dashboard layout:
```
┌──────────────────────────────────────────────────────┐
│ Dashboard Header                                     │
│   [Title] [Quick Actions]                            │
├────────────┬────────────┬────────────┬───────────────┤
│ Metric 1   │ Metric 2   │ Metric 3   │ Metric 4      │
│ [Value]    │ [Value]    │ [Value]    │ [Value]       │
├────────────┴────────────┴────────────┴───────────────┤
│ Recent Activity                    │ Quick Links    │
│ • Item 1                           │ • Link 1       │
│ • Item 2                           │ • Link 2       │
│ • Item 3                           │ • Link 3       │
├────────────────────────────────────┴────────────────┤
│ Charts/Visualizations                                │
│ [Placeholder for module-specific visualizations]    │
└──────────────────────────────────────────────────────┘
```

### List View Pattern
All modules follow a consistent list view layout:
```
┌──────────────────────────────────────────────────────┐
│ [Title]                            [+ New] [Export]  │
├──────────────────────────────────────────────────────┤
│ 🔍 [Search...]  [Filter ▼] [Sort ▼] [Columns ▼]    │
├──────────────────────────────────────────────────────┤
│ ☐  Column 1   Column 2   Column 3   Status  Actions │
│ ☐  Data 1     Data 2     Data 3     Active  [···]   │
│ ☐  Data 1     Data 2     Data 3     Active  [···]   │
│ ☐  Data 1     Data 2     Data 3     Inactive [···]  │
├──────────────────────────────────────────────────────┤
│ [←] Page 1 of 10 [→]             Showing 1-25 of 234│
└──────────────────────────────────────────────────────┘
```

### Detail View Pattern
All modules follow a consistent detail view layout:
```
┌──────────────────────────────────────────────────────┐
│ [← Back] [Title]              [Edit] [Delete] [···]  │
├──────────────────────────────────────────────────────┤
│ Tab 1 │ Tab 2 │ Tab 3 │ Tab 4                        │
├──────────────────────────────────────────────────────┤
│                                                      │
│ [Tab Content]                                        │
│ • Form fields                                        │
│ • Related data                                       │
│ • Activity history                                   │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## Implementation Notes

### For UI-Builder

When implementing module UI shells:

1. **Use Global Components**: All components from `component-library.md`
2. **Follow Theme System**: All styling via `theme-system.md`
3. **Respect Layout**: All layouts follow `layout.md`
4. **Use Navigation Patterns**: All navigation follows `navigation-spec.md`
5. **Placeholder Data**: Use realistic but clearly fake placeholder data
6. **No Business Logic**: UI shells display structure, not functionality
7. **Accessibility First**: WCAG 2.1 Level AA compliance
8. **Responsive Design**: Mobile-first approach

### Testing Requirements

Each module UI shell must have:
- [ ] Component rendering tests
- [ ] Route navigation tests
- [ ] Responsive layout tests
- [ ] Accessibility tests
- [ ] Visual regression tests (screenshots)

---

## Governance

**Approval Required**: Yes  
**Approver**: Johan  
**Status**: DRAFT  

**Change Control**:
- Module shell changes require Foreman review
- Must maintain consistency across all modules
- Breaking changes require major version bump

---

*Document prepared by: Maturion Foreman*  
*Date: 2025-12-04*  
*Build Wave: 1.1*
