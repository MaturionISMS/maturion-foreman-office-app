# FOREMAN_VERSIONING_STRATEGY_v1.0.md

## Version: 1.0  
## Date: 2025-12-15

---

## 1. VERSIONING SCHEME

**Semantic Versioning**: MAJOR.MINOR.PATCH

**Version Increment Rules**:
- **MAJOR**: Breaking changes to Foreman contract or governance rules
- **MINOR**: New features or capabilities (backward compatible)
- **PATCH**: Bug fixes, clarifications (backward compatible)

**Examples**:
- 1.0.0 → 1.0.1: Bug fix
- 1.0.1 → 1.1.0: New monitoring dashboard feature
- 1.1.0 → 2.0.0: Breaking change to Builder Agent Contract

---

## 2. BACKWARD COMPATIBILITY GUARANTEES

### 2.1 Database Schema
- MINOR/PATCH: Additive only (new columns, tables)
- MAJOR: May include breaking schema changes

### 2.2 Builder Contract
- MINOR/PATCH: No changes to "Build to Green" instruction format
- MAJOR: May change instruction format (with migration guide)

### 2.3 API Contracts
- MINOR/PATCH: New endpoints only, existing endpoints unchanged
- MAJOR: May change or remove endpoints

---

## 3. MIGRATION STRATEGY

### 3.1 Database Migrations
- Use Alembic or Supabase migrations
- All migrations reversible
- Migrations tested in staging before production

### 3.2 Data Migrations
- MAJOR version: May require data migration scripts
- Scripts provided with release notes
- Rollback scripts provided

### 3.3 Code Migrations
- Deprecation warnings in MINOR versions
- Removal in next MAJOR version
- Migration guide provided

---

## 4. DEPRECATION POLICY

### 4.1 Deprecation Timeline
1. Announce deprecation in release notes
2. Add deprecation warning (in code, logs, UI)
3. Maintain deprecated feature for at least 1 MINOR version
4. Remove in next MAJOR version

### 4.2 Deprecation Notice
```
DEPRECATED: Feature X will be removed in version 2.0.0
Use Feature Y instead.
See migration guide: docs/migrations/feature-x-to-y.md
```

---

## 5. VERSION COMPATIBILITY MATRIX

| Foreman Version | Builder Contract Version | Database Schema Version |
|-----------------|-------------------------|------------------------|
| 1.0.0           | 1.0                     | 1.0                    |
| 1.1.0           | 1.0 (compatible)        | 1.1 (additive)         |
| 2.0.0           | 2.0 (breaking)          | 2.0 (breaking)         |

---

## 6. IMPACT ANALYSIS FOR VERSION CHANGES

### 6.1 Pre-Release Checklist
- [ ] Review all changes
- [ ] Classify as MAJOR/MINOR/PATCH
- [ ] Identify breaking changes
- [ ] Write migration guide (if MAJOR)
- [ ] Update compatibility matrix
- [ ] Test migrations in staging
- [ ] Communicate changes to stakeholders

### 6.2 Release Notes Template
```
## Version X.Y.Z (YYYY-MM-DD)

### Breaking Changes (MAJOR only)
- Change 1 with migration guide

### New Features (MINOR)
- Feature 1
- Feature 2

### Bug Fixes (PATCH)
- Fix 1
- Fix 2

### Deprecations
- Deprecated feature X (will be removed in v2.0.0)

### Migration Guide
See docs/migrations/vX.Y.Z.md
```

---

## 7. VERSION NEGOTIATION

**Not applicable for Wave 0** (single-tenant, always latest version)

**Future** (multi-tenant):
- Clients specify API version in request header
- Server supports last 2 MAJOR versions
- Automatic upgrade prompts in UI

---

## 8. ROLLBACK PROCEDURE

### 8.1 Rollback Steps
1. Stop Foreman Office service
2. Restore database from backup (if MAJOR schema change)
3. Deploy previous version
4. Restart service
5. Verify functionality

### 8.2 Rollback Decision Criteria
- Critical bug affecting governance enforcement
- Data corruption detected
- Unrecoverable performance degradation

---

*Generated for Issue #2 - Architecture & QA Design (Wave 0 Completion)*
