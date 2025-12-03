# Maturion Memory Model

## Purpose

This document defines how **Maturion** stores, retrieves, and manages knowledge across four distinct memory layers. This memory model ensures:

- **Persistent architectural knowledge** across all interactions
- **Tenant isolation** to prevent cross-organization data leakage
- **User-specific context** for personalized assistance
- **Global learning** from anonymized patterns without exposing secrets

---

## The Four Memory Layers

### Layer 1: Static Architecture & Rules (GitHub Repository)

**Source**: Version-controlled files in this repository  
**Scope**: Global, applies to all tenants  
**Persistence**: Permanent via Git  
**Access**: Read by Maturion, updated via governance process

**Contains**:
- SRMF Master Build Reference
- Module True North documents
- Integration maps and boundaries
- QA implementation plans
- Watchdog logic specifications
- Builder agent manifests
- Governance rules and policies

**Characteristics**:
- Immutable during runtime (changes require commits and approvals)
- Single source of truth for architectural decisions
- Version-controlled for audit trail
- Accessible to all tenants (architectural patterns are not tenant-specific)

**Examples**:
- `SRMF_MASTER_BUILD_REFERENCE_v1.0.md`
- `foreman/identity.md`
- `THREAT_TRUE_NORTH_v1.0.md`
- `builder-manifest.json`

---

### Layer 2: Per-Tenant Configuration and State

**Source**: Tenant-specific database tables (scoped by `organisation_id`)  
**Scope**: Single organization only  
**Persistence**: Permanent in tenant database  
**Access**: Strict tenant isolation enforced

**Contains**:
- Organization-specific configurations
- Tenant customizations and settings
- Module enablement flags
- Custom workflows and approval processes
- Tenant-specific integrations
- Organization policies and thresholds

**Characteristics**:
- **Strict tenant boundary enforcement**: Every query MUST include `organisation_id`
- Isolated per customer organization
- Cannot be accessed by other tenants
- Persists across user sessions within the same organization
- Backed up per tenant

**Examples**:
- ERM risk appetite settings for Organization A
- Threat watchdog thresholds customized for Organization B
- Custom risk assessment templates for Organization C
- Integration API keys for Organization D (encrypted)

**Security Rules**:
- ✅ Maturion CAN read/write tenant config scoped to the current `organisation_id`
- ❌ Maturion CANNOT read tenant config from other organizations
- ❌ Maturion CANNOT use one tenant's data as an example for another tenant
- ✅ Maturion CAN use anonymized patterns (Layer 4) across tenants

---

### Layer 3: Per-User & Per-Org Conversation Memory

**Source**: Session storage, conversation context database  
**Scope**: User session or cross-session user profile  
**Persistence**: Session-based or short-term (e.g., 30-90 days)  
**Access**: User-specific or org-specific, scoped by `user_id` and `organisation_id`

**Contains**:
- User conversation history (within current session or recent sessions)
- User preferences and interaction patterns
- Contextual state for ongoing tasks
- User-specific shortcuts or favorites
- Recent queries and responses
- Organization-level conversation context (for admin users)

**Characteristics**:
- Tied to both `user_id` AND `organisation_id`
- Enables continuity across conversations
- Automatically purged after expiration period
- User can request conversation history deletion (GDPR compliance)
- NOT shared across organizations

**Examples**:
- User Johan recently asked about PIT module integration → Maturion remembers context
- Organization A's admin team discussed changing risk appetite → Maturion recalls this in next admin session
- User Sarah from Organization B asked for export help → Maturion remembers Sarah's preferences for next session

**Security Rules**:
- ✅ Maturion CAN recall user conversation history within the same organization
- ❌ Maturion CANNOT recall Organization A's conversations when helping Organization B
- ✅ Maturion CAN recall user preferences across sessions (with user consent)
- ✅ Users and admins can delete their conversation memory on request

---

### Layer 4: Global Anonymized Learning

**Source**: Aggregated, anonymized patterns from all tenants  
**Scope**: Global knowledge base  
**Persistence**: Long-term, continuously updated  
**Access**: Available to all tenants, no identifiable information

**Contains**:
- Common architectural patterns observed across deployments
- Frequently asked questions (anonymized)
- Best practices derived from usage patterns
- Performance optimization insights
- Common configuration pitfalls
- Effective quality assurance strategies

**Characteristics**:
- **Completely anonymized**: No tenant names, user names, or specific data
- Derived from aggregated behavior across ALL tenants
- Improves Maturion's ability to provide guidance
- No secrets, credentials, or sensitive data
- Cannot be reverse-engineered to identify specific tenants

**Examples** (Anonymized):
- "Organizations often set ERM risk appetite thresholds between 3-7 out of 10"
- "Common integration issue: Threat module API rate limits when polling too frequently"
- "Best practice observed: Enable watchdog triggers in PIT before Threat module"
- "Users frequently ask how to export risk assessments in CSV format"

**Security Rules**:
- ✅ Maturion CAN use anonymized patterns to improve responses for all tenants
- ❌ Maturion CANNOT expose which organizations contributed to a pattern
- ❌ Maturion CANNOT include tenant-specific examples or data
- ✅ Maturion CAN say "Many organizations configure X this way" (anonymized)
- ❌ Maturion CANNOT say "Organization Y configured X this way" (identifiable)

---

## Cross-Layer Rules and Guardrails

### Tenant Isolation (Critical)

**Maturion MUST never leak data from one organization to another.**

1. **Layer 1** (Architecture): Shared globally → Safe to reference for any tenant
2. **Layer 2** (Tenant Config): Strictly isolated → Never cross-reference between tenants
3. **Layer 3** (Conversation Memory): Scoped to user + org → Never share across organizations
4. **Layer 4** (Global Learning): Anonymized → Safe to share patterns, NOT specific data

### Example Scenarios

#### ✅ **CORRECT: Using Layer 1 + Layer 4**
```
User from Organization A: "How should we configure our Threat watchdog?"

Maturion: "According to THREAT_WATCHDOG_LOGIC_v1.0.md [Layer 1], you can configure 
four severity levels. Many organizations [Layer 4, anonymized] start with Critical 
and High triggers enabled, then add Medium triggers as they mature."
```

#### ❌ **WRONG: Leaking Layer 2 across tenants**
```
User from Organization A: "How should we configure our Threat watchdog?"

Maturion: "Organization B configured their Critical threshold to 90 CVSS score 
and High to 70. You might want to use similar settings."
```
**Problem**: Exposed Organization B's specific configuration (Layer 2) to Organization A.

#### ✅ **CORRECT: Using Layer 3 within same org**
```
User Johan from Organization A (2nd conversation): "Continue from where we left off."

Maturion: "In our last conversation, we discussed enabling Medium watchdog triggers 
for your Threat module. Would you like to proceed with that configuration?"
```

#### ❌ **WRONG: Using Layer 3 across organizations**
```
User from Organization B: "What did Johan configure?"

Maturion: "Johan from Organization A configured Critical threshold to 85 CVSS."
```
**Problem**: Leaked Organization A's conversation and configuration to Organization B.

---

## Memory Lifecycle

### Layer 1: Architecture (Git-based)
- **Creation**: Via pull requests and governance approval
- **Updates**: Version-controlled commits reviewed by Maturion Foreman
- **Deletion**: Never deleted, only superseded by newer versions
- **Access**: Always available, read by Maturion on every interaction

### Layer 2: Tenant Configuration
- **Creation**: When organization is onboarded
- **Updates**: As organization customizes settings
- **Deletion**: When organization offboards (with grace period)
- **Access**: Queried on-demand scoped to `organisation_id`

### Layer 3: Conversation Memory
- **Creation**: Start of user session or conversation
- **Updates**: Throughout conversation
- **Deletion**: After expiration period (30-90 days) or on user request
- **Access**: Retrieved at conversation start, updated during session

### Layer 4: Global Learning
- **Creation**: Continuous aggregation from anonymized usage patterns
- **Updates**: Periodic batch processing (daily/weekly)
- **Deletion**: Outdated patterns replaced as platform evolves
- **Access**: Integrated into Maturion's knowledge base

---

## Privacy and Security Commitments

1. **No Cross-Tenant Data Exposure**: Maturion will never share Organization A's data with Organization B
2. **Anonymization in Global Learning**: Layer 4 contains zero identifiable information
3. **User Control**: Users can request deletion of conversation history (Layer 3)
4. **Audit Trail**: All tenant configuration changes (Layer 2) are logged with `user_id` and timestamp
5. **Encryption**: Sensitive tenant data (API keys, credentials) encrypted at rest and in transit
6. **Role-Based Access**: Admin users may see org-wide context; regular users see only their own

---

## Admin and Customer User Boundaries

### Customer Users (Regular Users)

**Can see**:
- Layer 1: Architecture and governance docs (public knowledge)
- Layer 2: Their organization's configuration (scoped to `organisation_id`)
- Layer 3: Their own conversation history (scoped to `user_id` + `organisation_id`)
- Layer 4: Anonymized global patterns

**Cannot see**:
- Other organizations' configurations
- Other users' conversations (unless admin)
- Identifiable data from other tenants

### Admin Users (e.g., Johan)

**Can see**:
- Layer 1: Architecture and governance docs
- Layer 2: All tenant configurations (for admin purposes only, NOT shared with tenants)
- Layer 3: Cross-org analytics (aggregated, anonymized)
- Layer 4: Anonymized global patterns
- **Admin-specific analytics**: Cross-org performance metrics, usage patterns

**Cannot expose to individual tenants**:
- Other tenants' specific configurations
- Identifiable cross-org data

**Use case example**:
- Johan (admin) can see "15 organizations have enabled Threat module, average 200 threats tracked per month"
- Johan CANNOT tell Organization A what Organization B's specific threat count is
- Johan CAN share anonymized benchmarks: "Organizations typically track 100-300 threats per month"

---

## Maturion's Memory Access Pattern

When Maturion responds to a query, it follows this priority:

1. **Identify tenant scope**: Extract `organisation_id` from session context
2. **Load Layer 1**: Reference applicable architecture documents
3. **Load Layer 2**: Retrieve tenant-specific configuration (scoped to `organisation_id`)
4. **Load Layer 3**: Retrieve user's conversation context (scoped to `user_id` + `organisation_id`)
5. **Apply Layer 4**: Augment response with anonymized global learning
6. **Enforce boundaries**: Double-check no cross-tenant data leakage before responding

---

## Version Control

**Document Version**: 1.0  
**Last Updated**: 2025-12-03  
**Maintained By**: Maturion  
**Review Cycle**: Quarterly or when memory model changes

---

**Maturion** - Intelligent Memory, Absolute Privacy, Global Learning
