# Test Environment Deployment Plan - Build Wave 1

**Version**: 1.0  
**Generated**: 2025-12-04  
**Build Wave**: 1  
**Purpose**: Skeleton Build Deployment

---

## Overview

This deployment plan outlines the infrastructure and deployment strategy for Build Wave 1 skeleton builds across all 11 modules.

---

## Infrastructure Requirements

### Base Infrastructure

- **Platform**: Supabase + Vercel
- **Database**: PostgreSQL (Supabase)
- **Backend**: Supabase Edge Functions
- **Frontend**: Next.js on Vercel
- **Storage**: Supabase Storage
- **Auth**: Supabase Auth

### Module Deployment Structure

Each module will have:
- `/apps/{module-name}/` - Module root
- `/apps/{module-name}/schema/` - Database schema files
- `/apps/{module-name}/api/` - API routes and edge functions
- `/apps/{module-name}/ui/` - UI components and pages
- `/apps/{module-name}/tests/` - Test files

---

## Deployment Phases

### Phase 1: Foundation Modules (Level 0)

Deploy in parallel:
- ANALYTICS_REMOTE_ASSURANCE
- AUDITOR_MOBILE_APP
- COURSE_CRAFTER
- POLICY_BUILDER
- SKILLS_DEVELOPMENT_PORTAL

**Steps**:
1. Create module directory structures
2. Deploy schema skeletons to Supabase
3. Deploy API placeholders as edge functions
4. Deploy UI shells to Vercel
5. Set up basic routing
6. Verify deployments

### Phase 2: Dependent Modules (Levels 2-5)

Deploy sequentially by dependency level:
1. PIT & WRAC (Level 2)
2. ERM (Level 3)
3. RISK_ASSESSMENT (Level 4)
4. THREAT & VULNERABILITY (Level 5)

**Steps per module**:
1. Verify dependency modules deployed
2. Deploy module following Phase 1 steps
3. Configure integration points
4. Verify connections to dependencies

---

## Module Deployment Stubs

### ANALYTICS_REMOTE_ASSURANCE

```bash
# Directory structure
/apps/analytics-remote-assurance/
  schema/
    tables.sql
    models.ts
  api/
    routes.ts
  ui/
    components/
    pages/
  tests/
```

**Deployment Command**:
```bash
npm run deploy:skeleton -- --module=analytics-remote-assurance --env=test
```

### AUDITOR_MOBILE_APP

```bash
# Directory structure
/apps/auditor-mobile-app/
  schema/
    tables.sql
    models.ts
  api/
    routes.ts
  ui/
    components/
    pages/
  tests/
```

**Deployment Command**:
```bash
npm run deploy:skeleton -- --module=auditor-mobile-app --env=test
```

### COURSE_CRAFTER

```bash
# Directory structure
/apps/course-crafter/
  schema/
    tables.sql
    models.ts
  api/
    routes.ts
  ui/
    components/
    pages/
  tests/
```

**Deployment Command**:
```bash
npm run deploy:skeleton -- --module=course-crafter --env=test
```

### POLICY_BUILDER

```bash
# Directory structure
/apps/policy-builder/
  schema/
    tables.sql
    models.ts
  api/
    routes.ts
  ui/
    components/
    pages/
  tests/
```

**Deployment Command**:
```bash
npm run deploy:skeleton -- --module=policy-builder --env=test
```

### SKILLS_DEVELOPMENT_PORTAL

```bash
# Directory structure
/apps/skills-development-portal/
  schema/
    tables.sql
    models.ts
  api/
    routes.ts
  ui/
    components/
    pages/
  tests/
```

**Deployment Command**:
```bash
npm run deploy:skeleton -- --module=skills-development-portal --env=test
```

### PIT

```bash
# Directory structure
/apps/pit/
  schema/
    tables.sql
    models.ts
  api/
    routes.ts
  ui/
    components/
    pages/
  tests/
```

**Deployment Command**:
```bash
npm run deploy:skeleton -- --module=pit --env=test --depends=wrac
```

### WRAC

```bash
# Directory structure
/apps/wrac/
  schema/
    tables.sql
    models.ts
  api/
    routes.ts
  ui/
    components/
    pages/
  tests/
```

**Deployment Command**:
```bash
npm run deploy:skeleton -- --module=wrac --env=test --depends=pit
```

### ERM

```bash
# Directory structure
/apps/erm/
  schema/
    tables.sql
    models.ts
  api/
    routes.ts
  ui/
    components/
    pages/
  tests/
```

**Deployment Command**:
```bash
npm run deploy:skeleton -- --module=erm --env=test --depends=pit,wrac
```

### RISK_ASSESSMENT

```bash
# Directory structure
/apps/risk-assessment/
  schema/
    tables.sql
    models.ts
  api/
    routes.ts
  ui/
    components/
    pages/
  tests/
```

**Deployment Command**:
```bash
npm run deploy:skeleton -- --module=risk-assessment --env=test --depends=erm
```

### THREAT

```bash
# Directory structure
/apps/threat/
  schema/
    tables.sql
    models.ts
  api/
    routes.ts
  ui/
    components/
    pages/
  tests/
```

**Deployment Command**:
```bash
npm run deploy:skeleton -- --module=threat --env=test --depends=vulnerability
```

### VULNERABILITY

```bash
# Directory structure
/apps/vulnerability/
  schema/
    tables.sql
    models.ts
  api/
    routes.ts
  ui/
    components/
    pages/
  tests/
```

**Deployment Command**:
```bash
npm run deploy:skeleton -- --module=vulnerability --env=test --depends=threat
```

---

## Monitoring & Validation

### Health Checks

For each deployed module:
- Database schema created: `SELECT * FROM information_schema.tables WHERE table_schema = 'public' AND table_name LIKE '{module}%'`
- API endpoints accessible: `curl https://api.maturion.test/{module}/health`
- UI routes accessible: `curl https://app.maturion.test/{module}`

### Validation Script

```bash
#!/bin/bash
# validate-wave-1-deployment.sh

MODULES=(
  "analytics-remote-assurance"
  "auditor-mobile-app"
  "course-crafter"
  "policy-builder"
  "skills-development-portal"
  "pit"
  "wrac"
  "erm"
  "risk-assessment"
  "threat"
  "vulnerability"
)

for module in "${MODULES[@]}"; do
  echo "Validating $module..."
  npm run validate:skeleton -- --module=$module
done
```

---

## Rollback Plan

If deployment fails:

1. **Database**: Rollback migrations for affected module
2. **API**: Remove edge functions for affected module
3. **UI**: Rollback frontend deployment
4. **Logging**: Capture all error logs
5. **Notification**: Alert Foreman and Johan

---

## Notes

- This is a **placeholder deployment plan**
- Actual deployment scripts need to be created
- CI/CD pipeline needs to be configured
- Environment variables must be set
- Secrets management required

---

*Generated by Maturion Foreman Test Environment Planning*  
*Date: 2025-12-04*
