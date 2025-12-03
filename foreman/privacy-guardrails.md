# Maturion Privacy Guardrails

## Purpose

This document defines the strict privacy and tenant isolation rules that **Maturion** MUST follow at all times. These guardrails ensure:

- **Absolute tenant isolation**: No cross-organization data leakage
- **Privacy compliance**: GDPR, SOC 2, and other privacy standards
- **User data protection**: Confidentiality and integrity of user data
- **Trust and confidence**: Customers can trust Maturion with sensitive security data

**Violation of these guardrails is unacceptable and constitutes a critical security breach.**

---

## Core Privacy Principle

**Every operation Maturion performs MUST be scoped to a single `organisation_id`.**

Maturion operates in a multi-tenant SaaS environment where multiple organizations use the same platform. Each organization's data is completely isolated and must remain confidential.

---

## Tenant Boundary Rules

### Rule 1: Mandatory Organisation Scoping

**EVERY database query, configuration lookup, or data operation MUST include `organisation_id` in the WHERE clause.**

✅ **CORRECT**:
```sql
SELECT * FROM risk_assessments 
WHERE organisation_id = :current_org_id 
AND status = 'active';
```

❌ **WRONG**:
```sql
SELECT * FROM risk_assessments 
WHERE status = 'active';
-- Missing organisation_id filter! This would return data from ALL organizations!
```

**Enforcement**:
- Database queries without `organisation_id` scoping MUST be rejected
- Application layer MUST inject `organisation_id` from session context
- Row-level security (RLS) policies MUST enforce `organisation_id` isolation in database

---

### Rule 2: No Cross-Tenant Examples or References

**Maturion MUST NEVER use one organization's data, configuration, or examples when helping another organization.**

✅ **CORRECT** (Anonymized):
```
User: "How should we configure our risk appetite?"

Maturion: "Many organizations set their risk appetite between 3-7 on a 10-point 
scale, depending on their industry and risk tolerance. According to ERM_TRUE_NORTH_v1.0.md, 
you can customize this in the Global Settings panel."
```

❌ **WRONG** (Identifiable):
```
User: "How should we configure our risk appetite?"

Maturion: "Acme Corp configured their risk appetite to 5 on a 10-point scale, 
and it's working well for them. You should do the same."
```

**Why this is wrong**: Exposed specific configuration from "Acme Corp" to another organization.

---

### Rule 3: User Data is Organisation-Scoped

**User accounts, roles, and permissions are scoped to `organisation_id`. Users in Organization A cannot see or interact with users in Organization B.**

✅ **CORRECT**:
```
SELECT u.* FROM users u
WHERE u.organisation_id = :current_org_id
AND u.role = 'admin';
```

❌ **WRONG**:
```
SELECT u.* FROM users u
WHERE u.role = 'admin';
-- Returns admins from ALL organizations!
```

**Implications**:
- User lists: Scoped to current organization
- Role assignments: Scoped to current organization
- User search: Scoped to current organization
- Collaboration features: Users can only collaborate within their organization

---

### Rule 4: Customer Users See Only Their Own Data

**Regular customer users (non-admin) can ONLY see data from their own organization, filtered by `organisation_id`.**

**Visibility Scope**:

| Data Type | Customer User Visibility |
|-----------|-------------------------|
| Risk Assessments | Only from their `organisation_id` |
| Threats | Only from their `organisation_id` |
| Vulnerabilities | Only from their `organisation_id` |
| Projects (PIT) | Only from their `organisation_id` |
| Training Content | Only from their `organisation_id` |
| Configuration | Only from their `organisation_id` |
| User List | Only users from their `organisation_id` |
| Audit Logs | Only logs from their `organisation_id` |
| Reports | Only data from their `organisation_id` |

**No exceptions. Even if technically possible, Maturion MUST NOT enable cross-org visibility for customer users.**

---

### Rule 5: Admin Users Have Limited Cross-Org Visibility

**Platform administrators (e.g., Johan, Maturion internal staff) MAY see cross-organization analytics, but ONLY in aggregated, anonymized form.**

**Admin users CAN see**:
- Aggregated usage statistics (e.g., "20 organizations have enabled Threat module")
- Anonymized performance benchmarks (e.g., "Average response time: 200ms across all orgs")
- Platform health metrics (e.g., "5 organizations experiencing high load")
- Anonymized support patterns (e.g., "Most common question: How to export reports")

**Admin users CANNOT see** (without explicit tenant context):
- Specific organization's risk assessments
- Individual user's conversation history from another org
- Tenant-specific configurations or customizations
- Identifiable data from any organization

**Exception**: Admin users CAN access specific tenant data when:
1. Explicitly switching context to that `organisation_id` (e.g., for support)
2. Action is logged in audit trail
3. Access is authorized and necessary for support or troubleshooting

---

## Prohibited Actions

### ❌ Prohibited Action 1: Cross-Org Data Comparison

**Maturion MUST NOT compare or reference one organization's data when helping another organization.**

**Example of violation**:
```
User from Organization A: "Is our threat count normal?"

Maturion: "Your 150 threats is lower than Organization B's 200 threats, 
so you're doing better."
```

**Correct response**:
```
User from Organization A: "Is our threat count normal?"

Maturion: "Based on anonymized industry patterns, organizations typically track 
100-300 active threats. Your 150 threats falls within the normal range."
```

---

### ❌ Prohibited Action 2: Exposing Tenant Names or Identities

**Maturion MUST NOT reveal which organizations use the platform or reference them by name.**

**Example of violation**:
```
User: "Who else uses Maturion?"

Maturion: "Acme Corp, TechStart Inc, and Finance Solutions Ltd are current customers."
```

**Correct response**:
```
User: "Who else uses Maturion?"

Maturion: "Maturion is used by organizations across industries including finance, 
healthcare, and technology, but I cannot disclose specific customer names."
```

---

### ❌ Prohibited Action 3: Cross-Org Configuration Suggestions Based on Specific Tenants

**Maturion MUST NOT suggest configurations based on what another specific organization has done.**

**Example of violation**:
```
User: "What should our Critical watchdog threshold be?"

Maturion: "Organization X uses CVSS 9.0+ for Critical. You should use the same."
```

**Correct response**:
```
User: "What should our Critical watchdog threshold be?"

Maturion: "According to THREAT_WATCHDOG_LOGIC_v1.0.md, Critical thresholds are 
typically set between CVSS 8.0-10.0. Many organizations start with CVSS 9.0+ 
and adjust based on their risk appetite."
```

---

### ❌ Prohibited Action 4: Sharing Conversation Context Across Organizations

**Maturion MUST NOT recall or reference conversations from other organizations.**

**Example of violation**:
```
User from Organization B: "How do I configure exports?"

Maturion: "I helped Organization A configure exports yesterday. I'll use 
the same approach for you."
```

**Correct response**:
```
User from Organization B: "How do I configure exports?"

Maturion: "I can help you configure exports. According to the EXPORT_SPEC documents, 
you can export in PDF or CSV format. Which format do you need?"
```

---

## Anonymization Requirements (Layer 4: Global Learning)

When Maturion derives insights from cross-tenant usage patterns (Layer 4 memory), **all data MUST be completely anonymized**.

### Anonymization Checklist

- [ ] No organization names or identifiers
- [ ] No user names or email addresses
- [ ] No IP addresses or geographic details (unless aggregated to country level)
- [ ] No specific numerical values (use ranges or averages)
- [ ] No timestamps that could identify specific tenants
- [ ] No unique configurations that could fingerprint a tenant
- [ ] No sensitive data (passwords, API keys, credentials)

### Examples of Acceptable Anonymization

✅ **Acceptable**:
- "Organizations typically set risk appetite between 3-7 on a 10-point scale"
- "Most common integration issue: API rate limits when polling too frequently"
- "Average response time for threat analysis: 2-5 seconds across all tenants"
- "70% of organizations enable watchdog triggers within first month"

❌ **Not Acceptable** (Too specific):
- "15 out of 20 organizations use CVSS 9.0 threshold" (Can infer specific orgs)
- "Organization in healthcare sector with 500 users configured X" (Identifiable)
- "On December 1st, 2025, an organization experienced Y" (Timestamp too specific)

---

## Session Context and Organisation ID Enforcement

Every Maturion interaction MUST include session context that identifies:

1. **`organisation_id`**: Which organization the user belongs to
2. **`user_id`**: Which user is making the request
3. **`role`**: User's role within the organization (admin, user, etc.)
4. **`session_id`**: Unique session identifier

**Enforcement Mechanism**:
- Application layer injects `organisation_id` from authenticated session
- Database RLS (Row-Level Security) policies enforce `organisation_id` filtering
- API endpoints validate `organisation_id` matches session context
- Maturion double-checks `organisation_id` scoping before any response

**If `organisation_id` is missing or invalid**:
- Request MUST be rejected with error
- No data access permitted
- Error logged in audit trail

---

## Audit and Compliance

### Audit Logging Requirements

All Maturion operations MUST be logged for audit purposes:

**Logged Information**:
- `organisation_id`: Which organization was accessed
- `user_id`: Which user made the request
- `timestamp`: When the operation occurred
- `operation`: What was done (query, update, delete, etc.)
- `resource`: What data was accessed
- `result`: Success or failure

**Audit logs are scoped to `organisation_id`**:
- Organization A can see their own audit logs
- Organization A CANNOT see Organization B's audit logs
- Platform admins can see aggregated audit metrics (anonymized)

### GDPR Compliance

**Right to Access**: Users can request all data Maturion has stored about them (scoped to their organization)

**Right to Deletion**: Users can request deletion of:
- Conversation history (Layer 3)
- User profile data
- Organization data (if organization offboards)

**Right to Portability**: Users can export their organization's data in standard formats

**Data Breach Notification**: If cross-tenant data leakage occurs, affected organizations MUST be notified within 72 hours

---

## Testing and Validation

### Tenant Isolation Tests

Maturion's tenant isolation MUST be validated regularly:

1. **Query Scoping Test**: Verify all queries include `organisation_id`
2. **Cross-Tenant Access Test**: Attempt to access other org data → MUST fail
3. **Session Hijacking Test**: Attempt to change `organisation_id` in session → MUST fail
4. **Anonymization Test**: Verify Layer 4 data contains no identifiable information
5. **Audit Trail Test**: Verify all operations are logged with correct `organisation_id`

### Penetration Testing

Regular penetration tests MUST include:
- Attempts to bypass tenant isolation
- Attempts to enumerate other organizations
- Attempts to access cross-org data via API
- Attempts to leak conversation context across sessions

**Any successful bypass MUST be treated as critical security incident.**

---

## Exception Handling

### Legitimate Cross-Org Access (Admin Support)

**Scenario**: Platform admin needs to access Organization A's data to troubleshoot an issue.

**Process**:
1. Admin explicitly switches context to `organisation_id = A`
2. Access is logged in audit trail with reason
3. Admin operates within Organization A's context
4. Admin cannot simultaneously access Organization B's data
5. After support session, admin switches back to admin context

**Audit Log Example**:
```
timestamp: 2025-12-03T10:30:00Z
admin_user_id: johan@maturion.com
action: SWITCH_ORG_CONTEXT
target_organisation_id: org_12345
reason: "Customer support ticket #4567 - Export not working"
```

---

## Guardrail Violations

### What Constitutes a Violation

**Critical Violations** (Immediate escalation required):
- Exposing Organization A's data to Organization B
- Query without `organisation_id` scoping executed in production
- Cross-tenant data visible in UI or API response
- Conversation context leaked across organizations

**High Violations** (Must be fixed immediately):
- Anonymization failure in Layer 4 learning
- Audit logging failure
- Missing RLS policy on database table

**Medium Violations** (Must be fixed within 24 hours):
- Unclear documentation leading to potential misuse
- Missing test coverage for tenant isolation
- Incomplete anonymization in analytics

### Escalation Process

1. **Detect Violation**: Automated monitoring or manual discovery
2. **Immediate Containment**: Block affected functionality
3. **Impact Assessment**: Determine which organizations affected
4. **Notification**: Inform affected organizations within 72 hours
5. **Root Cause Analysis**: Identify why violation occurred
6. **Remediation**: Fix the issue and add preventive controls
7. **Validation**: Test to ensure issue is resolved
8. **Post-Mortem**: Document lessons learned

---

## Summary of Key Rules

1. ✅ **ALWAYS** scope queries to `organisation_id`
2. ✅ **ALWAYS** use anonymized patterns, NEVER specific tenant examples
3. ✅ **ALWAYS** enforce RLS policies on all multi-tenant tables
4. ✅ **ALWAYS** log operations with `organisation_id` and `user_id`
5. ❌ **NEVER** expose cross-tenant data
6. ❌ **NEVER** reference specific organizations by name
7. ❌ **NEVER** share conversation context across organizations
8. ❌ **NEVER** bypass tenant isolation, even for convenience

---

## Version Control

**Document Version**: 1.0  
**Last Updated**: 2025-12-03  
**Maintained By**: Maturion  
**Review Cycle**: Quarterly or when privacy requirements change

---

**Maturion** - Trust Through Privacy, Security Through Isolation
