# POLICY_BUILDER_FRONTEND_COMPONENT_MAP_v1.0.md

## Policy Builder - Frontend Component Map
**Version**: 1.0  
**Date**: 2025-12-04

## Route Structure
```
/app/policy-builder/
  /page.tsx                 # Module landing page
  /layout.tsx               # Module layout
  /[id]/page.tsx            # Detail view
  /[id]/edit/page.tsx       # Edit view
  /new/page.tsx             # Create new
```

## Component Organization
```
/components/policy-builder/
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
