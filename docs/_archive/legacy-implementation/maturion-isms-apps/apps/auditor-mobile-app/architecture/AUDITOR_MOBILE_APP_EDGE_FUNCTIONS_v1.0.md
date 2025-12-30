# AUDITOR_MOBILE_APP_EDGE_FUNCTIONS_v1.0.md

## Auditor Mobile App - Edge Functions Specification
**Version**: 1.0  
**Date**: 2025-12-04

## Function Catalog
- `auditor-mobile-app-create`: Create new entity (POST)
- `auditor-mobile-app-update`: Update entity (PUT)
- `auditor-mobile-app-delete`: Delete entity (DELETE)
- `auditor-mobile-app-list`: List entities (GET)
- `auditor-mobile-app-get`: Get entity by ID (GET)

## Authentication
All functions require:
- Valid JWT token in Authorization header
- User must belong to an organisation
- RLS policies enforce data isolation

## Request/Response Pattern
```typescript
// Request
interface Request {
  headers: { Authorization: string };
  body: unknown;
}

// Response
interface Response {
  success: boolean;
  data?: unknown;
  error?: string;
}
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
