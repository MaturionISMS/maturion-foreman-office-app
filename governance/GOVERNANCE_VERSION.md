# Governance Version

**Version**: v1.0  
**Governance Repository**: https://github.com/APGI-cmy/maturion-foreman-governance  
**Last Updated**: 2026-01-11T07:10:00Z  
**Authority**: Johan Ras  
**Layer-Down Method**: FPC (First Point of Contact) Repository Layer-Down Process

## Canonical Governance Documents

This repository follows canonical governance from the Maturion Governance Centre.

### Core Governance Canon
- **GOVERNANCE_PURPOSE_AND_SCOPE.md** - Foundational governance principles
- **BUILD_PHILOSOPHY.md** - One-Time Build Correctness, Zero Regression
- **REPOSITORY_INITIALIZATION_AND_GOVERNANCE_SEEDING_PROTOCOL.md** - Repository initialization standard
- **COMPLIANCE_AND_STANDARDS_GOVERNANCE.md** - ISO/NIST/COBIT/OWASP/GDPR compliance framework
- **ARCHITECTURE_COMPLETENESS_REQUIREMENTS.md** - Architecture design and validation requirements
- **SYSTEM_COMMISSIONING_AND_PROGRESSIVE_ACTIVATION_PROTOCOL.md** - Deployment and activation governance

### Build & QA Governance
- **BUILDER_FIRST_PR_MERGE_MODEL.md** - Builder QA enforcement and PR merge model
- **PR_GATE_REQUIREMENTS_CANON.md** - PR gate semantics and requirements
- **PR_GATE_FAILURE_HANDLING_PROTOCOL.md** - Failure classifications and escalation
- **AGENT_SCOPED_QA_BOUNDARIES.md** - Agent QA separation (T0-009 Constitutional)
- **ZERO_WARNING_TEST_DEBT_IMMEDIATE_REMEDY_DOCTRINE.md** - Zero warning enforcement
- **TEST_REMOVAL_GOVERNANCE_GATE_LOCAL.md** - Test removal governance

### Agent & Authority Governance
- **AGENT_RECRUITMENT.md** - Agent recruitment and contract authority
- **AGENT_ROLE_GATE_APPLICABILITY.md** - Role-based gate applicability
- **FOREMAN_AUTHORITY_AND_SUPERVISION_MODEL.md** - FM authority and supervision
- **GOVERNANCE_LIAISON_MINIMUM_APPOINTMENT_REQUIREMENTS.md** - Governance liaison role
- **FM_PREAUTH_CHECKLIST_CANON.md** - FM pre-authorization requirements

### Cross-Repository Governance
- **CROSS_REPOSITORY_LAYER_DOWN_PROTOCOL.md** - Layer-down procedures
- **CROSS_REPOSITORY_RIPPLE_AWARENESS_MODEL.md** - Cross-repo ripple management
- **GOVERNANCE_VERSIONING_AND_SYNC_PROTOCOL.md** - Version and sync management

## Application-Specific Governance

This repository is the **Maturion Foreman Office Application** - the canonical FM repository that:
- Defines FM's identity, roles, and governance model
- Establishes architecture enforcement standards
- Implements QA governance and QA-of-QA
- Manages builder agent orchestration
- Provides compliance mapping and watchdog specifications
- Defines runtime platform agent behavior

### FM-Specific Governance Extensions
- **GOVERNANCE_AUTHORITY_MATRIX.md** - Master authority reference for FM repo
- **FM_EXECUTION_MANDATE.md** - FM's constitutional execution authority
- **RED_GATE_AUTHORITY_AND_OWNERSHIP.md** - Red gate ownership rules
- **TWO_GATEKEEPER_MODEL.md** - Dual gatekeeper authority (Governance Admin + FM Builder)
- **GOVERNANCE_POLICY_SYNC_SPECIFICATION.md** - Canon-to-FM translation workflow

## Governance Alignment Status

**Status**: COMPLETE  
**Method**: FPC Repository Layer-Down  
**Completed**: 2026-01-11  
**Alignment Level**: Full canonical compliance

This repository has completed the FPC (First Point of Contact) layer-down process and is aligned with canonical governance from `maturion-foreman-governance`.

## Compliance and Standards

Maturion governance implements:
- **ISO 27001** - Information Security Management
- **ISO 27005** - Information Security Risk Management  
- **ISO 31000** - Risk Management
- **NIST CSF** - Cybersecurity Framework
- **COBIT** - IT Governance Framework
- **GDPR** - General Data Protection Regulation
- **POPIA** - Protection of Personal Information Act
- **OWASP** - Application Security Standards

## Governance Evolution

Governance canon evolves in the `maturion-foreman-governance` repository. This repository adopts governance through:

1. **Downward Ripple** - Canon changes flow to FM repository via Governance Liaison
2. **Upward Ripple** - FM learnings and lessons promote to canon when validated
3. **Version Tracking** - This file tracks active governance version
4. **Sync Protocol** - Drift detection and prevention per GOVERNANCE_POLICY_SYNC_SPECIFICATION.md

## Notes

- Layer-down completed using REPOSITORY_INITIALIZATION_AND_GOVERNANCE_SEEDING_PROTOCOL.md
- Repository structure validated against canonical mandatory requirements
- Cross-repo tracking updated in maturion-foreman-governance
- Latest learnings from governance/memory/** reviewed and incorporated

---

*This document is the single source of truth for governance version and alignment status in this repository.*
