# Cross-Repo Tracking Update Instructions

**For**: Governance Administrator or Johan Ras  
**Date**: 2026-01-11  
**Subject**: Register foreman-office-app in Cross-Repo Governance Tracking

---

## Background

The FPC (First Point of Contact) Repository Layer-Down has been completed for the `maturion-foreman-office-app` repository. This document provides instructions for updating the cross-repo tracking in the `maturion-foreman-governance` repository.

---

## Required Update

### Target File
`maturion-foreman-governance/cross-repo/GOVERNANCE_VERSION_MATRIX.md`

(Or equivalent cross-repo tracking file - if this file doesn't exist, it should be created based on the CROSS_REPOSITORY_LAYER_DOWN_PROTOCOL.md)

### Entry to Add

```markdown
| foreman-office-app | APGI-cmy/maturion-foreman-office-app | v1.0 | COMPLETE | 2026-01-11T07:15:00Z |
```

### Full Entry Details

If a more detailed entry format is required:

```markdown
## foreman-office-app

- **Repository**: APGI-cmy/maturion-foreman-office-app
- **URL**: https://github.com/APGI-cmy/maturion-foreman-office-app
- **Repo Key**: foreman-office-app
- **Governance Version**: v1.0
- **Layer-Down Status**: COMPLETE
- **Layer-Down Method**: FPC (Retroactive)
- **Completion Date**: 2026-01-11T07:15:00Z
- **Canonical Documents**: 30+ governance documents referenced
- **Special Notes**: Canonical FM repository; retroactive initialization completed
```

---

## Context

### Repository Role
This is the **canonical Foreman Office Application repository** - the primary FM repository that defines:
- FM identity, roles, and governance model
- Architecture enforcement standards
- QA governance and QA-of-QA
- Builder agent orchestration
- Compliance mapping (ISO/NIST/COBIT/OWASP/GDPR)
- Runtime platform agent behavior
- Innovation engine and survey specifications

### Initialization Type
**Retroactive FPC Layer-Down** - The repository pre-existed with extensive governance scaffolding but lacked formal canonical tracking. The layer-down completed the missing elements:
- Created `.architecture/REPOSITORY_INITIALIZATION_EVIDENCE.md`
- Created `governance/GOVERNANCE_VERSION.md`
- Created `.qa/` directory

### Evidence Location
All evidence is documented in the repository:
- `.architecture/REPOSITORY_INITIALIZATION_EVIDENCE.md` - Complete initialization evidence
- `governance/GOVERNANCE_VERSION.md` - Governance version and canon tracking
- `FPC_LAYER_DOWN_COMPLETION_SUMMARY.md` - Executive summary of work completed

---

## Verification

To verify the layer-down was completed correctly, check:

1. **governance/GOVERNANCE_VERSION.md exists** - Contains governance version v1.0 and lists 30+ canonical documents
2. **.architecture/REPOSITORY_INITIALIZATION_EVIDENCE.md exists** - Contains complete initialization checklist and evidence
3. **.qa/ directory exists** - QA evidence root directory created
4. **All canonical requirements satisfied** - See FPC_LAYER_DOWN_COMPLETION_SUMMARY.md for full validation checklist

---

## Next Steps

1. Review this document
2. Navigate to `maturion-foreman-governance` repository
3. Locate or create `cross-repo/GOVERNANCE_VERSION_MATRIX.md`
4. Add the entry for `foreman-office-app` as specified above
5. Commit with message: `Register foreman-office-app in cross-repo tracking (FPC layer-down complete)`
6. (Optional) Add a note in the governance repository changelog

---

## Alternative: Create Cross-Repo Tracking File

If `cross-repo/GOVERNANCE_VERSION_MATRIX.md` doesn't exist yet, create it with this structure:

```markdown
# Cross-Repository Governance Version Matrix

This file tracks governance alignment status across all Maturion repositories.

## Matrix

| Repo Key | Repository URL | Governance Version | Status | Last Sync |
|----------|---------------|-------------------|--------|-----------|
| foreman-office-app | APGI-cmy/maturion-foreman-office-app | v1.0 | COMPLETE | 2026-01-11T07:15:00Z |

## Status Definitions

- **NOT_STARTED**: No governance structure present
- **PARTIAL**: Some governance elements present, not fully aligned
- **COMPLETE**: Full FPC layer-down completed, canonical compliance achieved

## Notes

- Governance Version refers to the version of canonical governance from maturion-foreman-governance
- Last Sync is the timestamp of the most recent governance alignment or layer-down
- Repo Key is the canonical key used to identify the repository in governance contexts

---

*This file is maintained by the Governance Administrator as part of cross-repository governance tracking.*
```

---

## Questions?

If you have questions about this update or need clarification on the layer-down process, refer to:
- `.architecture/REPOSITORY_INITIALIZATION_EVIDENCE.md` in the foreman-office-app repository
- `FPC_LAYER_DOWN_COMPLETION_SUMMARY.md` in the foreman-office-app repository
- `CROSS_REPOSITORY_LAYER_DOWN_PROTOCOL.md` in the maturion-foreman-governance repository

---

**Document Created**: 2026-01-11T07:15:00Z  
**Authority**: Governance Liaison Agent  
**Purpose**: Cross-repo tracking update instructions
