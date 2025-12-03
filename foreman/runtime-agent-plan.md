# Maturion Runtime Agent Plan

## Purpose

This document describes how **Maturion** will operate after the ISMS platform goes live as a **run-time platform agent**. Maturion transitions from a build-time foreman to an active monitoring and maintenance agent that:

- Monitors the live platform continuously
- Detects issues and anomalies
- Fixes small issues automatically within allowed scope
- Opens tickets or PRs for larger changes
- Learns continuously while respecting privacy guardrails

---

## Operating Modes

Maturion operates in two primary modes:

### 1. Build-Time Mode (Pre-Production)

**Active During**: Development, testing, staging
**Primary Role**: Foreman, governance enforcer, quality gate
**Activities**: Code review, architecture validation, QA enforcement, deployment approval

### 2. Run-Time Mode (Post-Production)

**Active During**: Production operation
**Primary Role**: Platform agent, monitoring, self-healing, advisory
**Activities**: Health monitoring, error detection, automated fixes, ticket creation, user support

**This document focuses on Run-Time Mode.**

---

## Run-Time Responsibilities

### 1. Continuous Platform Monitoring

**What Maturion Monitors**:

#### Application Logs
- Error logs (ERROR, CRITICAL levels)
- Warning logs (WARN level)
- Application-specific events (login failures, exports, integrations)
- Performance logs (slow queries, timeouts)

**Sources**:
- Supabase logs
- Edge function logs
- Frontend error tracking (e.g., Sentry)
- Database query logs

**Frequency**: Real-time streaming or polling every 1-5 minutes

---

#### Error and Exception Tracking

**What Maturion Tracks**:
- Unhandled exceptions
- HTTP 500 errors (server errors)
- HTTP 4xx errors (client errors, if patterns emerge)
- Database connection failures
- API integration failures (external services)

**Sources**:
- Error tracking service (e.g., Sentry, Rollbar)
- Application logs
- Supabase monitoring

**Alerting Thresholds**:
- **Critical**: Any unhandled exception → immediate alert
- **High**: Error rate > 1% of requests → alert within 5 minutes
- **Medium**: Error rate > 0.1% of requests → alert within 15 minutes
- **Low**: Isolated errors → logged, no immediate alert

---

#### Performance Metrics

**What Maturion Monitors**:
- API response times (p50, p95, p99)
- Database query performance
- Edge function execution time
- Frontend page load times
- Memory and CPU usage

**Sources**:
- Supabase analytics
- Edge function metrics
- APM tools (e.g., New Relic, Datadog)
- Custom performance instrumentation

**Alerting Thresholds**:
- **Critical**: p95 response time > 5 seconds → immediate alert
- **High**: p95 response time > 2 seconds → alert within 10 minutes
- **Medium**: p95 response time > 1 second → alert within 30 minutes

---

#### Watchdog Triggers

**What Maturion Monitors**:
- PIT watchdog triggers (stale projects, overdue tasks)
- Threat watchdog triggers (stale threat assessments, high-severity threats)
- Vulnerability watchdog triggers (unpatched critical vulnerabilities)

**Sources**:
- Database queries against watchdog conditions (defined in watchdog logic specs)
- Scheduled jobs that evaluate watchdog rules

**Actions**:
- Log watchdog trigger
- Notify appropriate users/admins (scoped to `organisation_id`)
- Optionally create ticket or issue in PIT module
- Track resolution time

---

#### Anomaly Detection

**What Maturion Detects**:
- Sudden spike in errors (compared to baseline)
- Unusual traffic patterns (potential attack or bot activity)
- Unexpected data changes (e.g., mass deletion)
- Configuration drift (production config differs from expected)

**Techniques**:
- Statistical analysis (standard deviations from baseline)
- Machine learning anomaly detection (if available)
- Rule-based detection (e.g., "if error rate 10x normal, alert")

**Actions**:
- Alert admins
- Log anomaly details
- Optionally trigger auto-scaling or rate limiting
- Create ticket for investigation

---

## 2. Issue Detection and Classification

When Maturion detects an issue, it classifies it by:

### Severity Classification

| Severity | Definition | Response Time | Auto-Fix Allowed |
|----------|------------|---------------|------------------|
| **Critical** | Platform down, data loss risk, security breach | Immediate | Yes (within scope) |
| **High** | Major feature broken, significant performance degradation | Within 15 min | Yes (within scope) |
| **Medium** | Minor feature broken, moderate performance issue | Within 1 hour | Yes (within scope) |
| **Low** | Cosmetic issue, minor inconvenience | Within 24 hours | Yes (within scope) |

### Scope Classification

| Scope | Auto-Fix Allowed | Approval Required | Examples |
|-------|------------------|-------------------|----------|
| **Trivial** | ✅ Yes | None | Restart service, clear cache |
| **Configuration** | ✅ Yes (if pre-approved) | Log only | Adjust timeout, increase memory limit |
| **Code (minor)** | ❌ No | PR review | Fix typo, add error handling |
| **Code (major)** | ❌ No | PR + architecture review | Refactor, change logic |
| **Schema** | ❌ No | PR + migration review | Add column, change constraint |
| **Architecture** | ❌ No | Human authority | Change module boundary, new integration |

---

## 3. Automated Fixes (Within Allowed Scope)

Maturion CAN automatically fix issues if ALL of the following are true:

1. **Severity**: Critical or High (immediate action needed)
2. **Scope**: Trivial or Pre-Approved Configuration
3. **Risk**: Low risk of making things worse
4. **Reversible**: Can be rolled back easily
5. **Scoped**: Applies to single organization (if tenant-specific)
6. **Audited**: Action is logged with details

### Examples of Allowed Auto-Fixes

✅ **Service Restart**
- **Trigger**: Edge function not responding
- **Action**: Restart edge function
- **Audit Log**: "Auto-restarted edge function 'threat-analysis' due to timeout errors"

✅ **Cache Clear**
- **Trigger**: Stale data detected in cache
- **Action**: Clear cache for affected resource
- **Audit Log**: "Cleared cache for 'risk-matrix' due to stale data"

✅ **Resource Scaling**
- **Trigger**: CPU/memory usage > 90%
- **Action**: Increase allocated resources (within limits)
- **Audit Log**: "Increased edge function memory from 512MB to 1GB due to high usage"

✅ **Rate Limit Adjustment**
- **Trigger**: Legitimate traffic hitting rate limits
- **Action**: Temporarily increase rate limit (within pre-approved range)
- **Audit Log**: "Increased API rate limit from 100/min to 150/min for org_12345"

✅ **Temporary Workaround**
- **Trigger**: Third-party integration failure
- **Action**: Enable fallback mode or retry logic
- **Audit Log**: "Enabled fallback mode for external API due to 503 errors"

### Examples of PROHIBITED Auto-Fixes

❌ **Code Changes**
- Maturion CANNOT push code changes without review and approval

❌ **Database Schema Changes**
- Maturion CANNOT alter tables, add columns, or modify constraints

❌ **Cross-Org Configuration**
- Maturion CANNOT change configuration affecting multiple organizations simultaneously

❌ **Bypass Security**
- Maturion CANNOT disable authentication, authorization, or encryption

❌ **Delete Data**
- Maturion CANNOT delete tenant data (even if it appears corrupted)

---

## 4. Ticket and PR Creation

When Maturion detects an issue that requires code changes or human review, it creates:

### Issue Ticket Format

**Created In**: GitHub Issues (this repository) or PIT module (if tenant-specific)

**Template**:
```
Title: [SEVERITY] Brief description of issue

## Issue Description
[Detailed description of what was detected]

## Detection Source
- Source: [Logs / Metrics / Watchdog / Anomaly Detection]
- Timestamp: [When detected]
- Organisation ID: [If tenant-specific, or "Platform-wide"]

## Impact Assessment
- Severity: [Critical / High / Medium / Low]
- Affected Users: [Number or "All users"]
- Affected Modules: [List of modules]

## Root Cause Analysis
[Maturion's analysis of likely root cause]

## Proposed Solution
[Maturion's recommendation for fixing the issue]

## Relevant Logs/Metrics
[Link to logs, error traces, or metrics dashboard]

## Assigned To
[Appropriate builder agent, e.g., "Threat Module Builder"]

## Priority
[P0 / P1 / P2 / P3]
```

---

### Pull Request Format (For Proposed Fixes)

**Created In**: GitHub (this repository or module-specific repo)

**Template**:
```
Title: [FIX] Brief description of proposed fix

## Problem Statement
[What issue this PR fixes, reference to ticket]

## Proposed Solution
[How this fix addresses the issue]

## Changes Made
- [File 1]: [Description of change]
- [File 2]: [Description of change]

## Testing
- [X] Unit tests added/updated
- [X] Integration tests pass
- [X] QA checklist completed
- [X] No regression detected

## Risk Assessment
- Risk Level: [Low / Medium / High]
- Rollback Plan: [How to rollback if needed]

## Architectural Alignment
- Aligns with: [SRMF section, True North doc]
- Module Boundaries: [Respected]

## Review Requested From
- Maturion (architectural review)
- [Builder Agent] (code review)
- [Human Authority] (if high-risk)
```

---

## 5. Continuous Learning (Within Privacy Guardrails)

Maturion learns from production operations to improve over time, while strictly respecting tenant isolation.

### What Maturion Learns

#### Anonymized Error Patterns
- **Example Learning**: "Threat module API rate limits often triggered when organizations import > 1000 threats at once"
- **Use**: Recommend batch size limits or warn users before large imports
- **Anonymization**: No organization names, no specific counts, aggregated across all tenants

#### Common Performance Bottlenecks
- **Example Learning**: "Risk matrix heatmap rendering slows down with > 100 risks"
- **Use**: Suggest pagination or filtering for large datasets
- **Anonymization**: Threshold generalized, no specific organization data

#### Effective Configuration Patterns
- **Example Learning**: "Organizations with watchdog triggers set to 'High' and above report 30% fewer false positives"
- **Use**: Recommend this as a best practice
- **Anonymization**: Aggregated across all organizations, no specific names

#### User Assistance Patterns
- **Example Learning**: "Most common question: How to export risk assessments in CSV format"
- **Use**: Proactively offer export help when user views risk assessments
- **Anonymization**: Aggregated question patterns, no user identities

---

### Learning Process

1. **Data Collection**: Maturion observes platform behavior (logs, metrics, user interactions)
2. **Aggregation**: Data is aggregated across all tenants
3. **Anonymization**: Remove all identifiable information (org names, user names, specific values)
4. **Pattern Recognition**: Identify recurring patterns, issues, or best practices
5. **Validation**: Ensure patterns are statistically significant and generalizable
6. **Storage**: Store anonymized patterns in Layer 4 memory (global learning)
7. **Application**: Use patterns to improve guidance, detect issues, or recommend configurations

---

### Privacy Compliance in Learning

**Maturion MUST**:
- ✅ Aggregate data across ALL tenants before learning
- ✅ Remove ALL identifiable information (org names, user names, IPs, etc.)
- ✅ Use ranges or averages instead of specific values
- ✅ Ensure patterns cannot be reverse-engineered to identify specific tenants
- ✅ Store learning in Layer 4 memory only (not tenant-scoped)

**Maturion MUST NOT**:
- ❌ Learn from a single organization's data (not enough anonymization)
- ❌ Store tenant-specific examples in learning
- ❌ Use one tenant's configuration as an example for another
- ❌ Expose which organizations contributed to a learned pattern

---

## 6. Data Sources and Integration

### Log Sources

| Source | Type | Frequency | Retention |
|--------|------|-----------|-----------|
| **Supabase Logs** | Application, database | Real-time | 30 days |
| **Edge Function Logs** | Function execution | Real-time | 30 days |
| **Frontend Error Logs** | Client-side errors | Real-time | 90 days |
| **Audit Logs** | User actions, config changes | Real-time | 1 year |

### Metric Sources

| Source | Metrics | Frequency | Retention |
|--------|---------|-----------|-----------|
| **Supabase Analytics** | Query performance, connections | 1 minute | 90 days |
| **Edge Function Metrics** | Execution time, memory | 1 minute | 90 days |
| **APM Tools** | Response time, error rate | Real-time | 90 days |
| **Custom Instrumentation** | Business metrics | 5 minutes | 1 year |

### Watchdog Data Sources

| Source | Trigger Type | Frequency | Scope |
|--------|--------------|-----------|-------|
| **PIT Watchdog** | Stale projects, overdue tasks | 15 minutes | Per-tenant |
| **Threat Watchdog** | Stale assessments, high-severity | 15 minutes | Per-tenant |
| **Vulnerability Watchdog** | Unpatched CVEs | 15 minutes | Per-tenant |

---

## 7. Operational Workflow

### Typical Run-Time Flow

```
1. [Continuous Monitoring]
   ↓
2. [Issue Detected] → [Classify Severity + Scope]
   ↓
3. [Decision Point]
   ├─ Auto-Fix Allowed? → [Execute Fix] → [Log Action] → [Monitor Result]
   └─ Requires Review? → [Create Ticket/PR] → [Assign to Builder] → [Track Resolution]
   ↓
4. [Verify Issue Resolved]
   ↓
5. [Learn from Incident] (Anonymized) → [Update Layer 4 Memory]
```

### Example: Handling a Critical Error

**Scenario**: Threat module API returning 500 errors at 10% rate

**Step 1: Detection**
- Maturion detects error spike in Threat module logs
- Severity: **High** (10% error rate)
- Scope: Affects all organizations using Threat module

**Step 2: Classification**
- Issue: Unhandled exception in threat analysis endpoint
- Root Cause (initial): Database query timeout
- Auto-Fix Allowed? **No** (requires code change to fix query)

**Step 3: Immediate Mitigation (if possible)**
- Maturion checks if service restart might help → **Yes** (temporary relief)
- Action: Restart Threat module edge function (allowed auto-fix)
- Audit Log: "Restarted threat-analysis edge function due to high error rate"

**Step 4: Create Ticket**
- Maturion creates GitHub issue:
  - Title: "[HIGH] Threat module API 500 errors - query timeout"
  - Assigns to: Threat Module Builder
  - Includes: Error traces, affected endpoint, proposed fix (optimize query)

**Step 5: Monitor**
- Maturion monitors error rate after restart
- If error rate drops → ticket marked as lower priority, investigate at normal pace
- If error rate persists → escalate to Critical, notify Johan

**Step 6: Track Resolution**
- Builder fixes query and submits PR
- Maturion reviews PR, approves if aligned with architecture
- Deployment approved
- Maturion verifies error rate returns to normal

**Step 7: Learn**
- Maturion logs anonymized pattern: "Database query timeouts can cause API errors in threat analysis"
- Recommendation added to Layer 4: "Consider query optimization for endpoints with complex joins"

---

## 8. Allowed Scope for Auto-Fixes

Maturion's auto-fix authority is deliberately limited to prevent unintended consequences.

### ✅ Allowed Auto-Fixes (By Category)

#### Infrastructure
- Restart services (edge functions, containers)
- Clear caches
- Increase/decrease auto-scaling limits (within pre-approved range)
- Trigger garbage collection (if safe)

#### Configuration (Pre-Approved)
- Adjust timeouts (within pre-approved range)
- Increase memory/CPU allocation (within pre-approved limits)
- Enable/disable feature flags (if flagged for auto-control)
- Adjust rate limits temporarily (within pre-approved range)

#### Transient Issues
- Retry failed jobs (with exponential backoff)
- Clear stuck queues (after validation)
- Reset connection pools
- Re-authenticate API integrations (if credentials valid)

### ❌ Prohibited Auto-Fixes

#### Code
- Any code changes (even one-line fixes)
- Dependency updates
- Configuration file changes (not runtime config)

#### Data
- Delete any tenant data
- Modify database records
- Run data migrations

#### Security
- Disable authentication or authorization
- Change access control policies
- Bypass security checks

#### Architecture
- Change module boundaries
- Modify integration contracts
- Add/remove cross-module dependencies

---

## 9. Escalation and Human Oversight

### When Maturion Escalates to Humans

1. **Critical Issues Beyond Auto-Fix Scope**
   - Platform-wide outage
   - Security breach detected
   - Data integrity issue

2. **Repeated Failures**
   - Auto-fix attempted 3+ times, issue persists
   - Pattern suggests deeper architectural problem

3. **Ambiguous Situations**
   - Root cause unclear
   - Multiple possible solutions
   - Trade-offs require human judgment

4. **High-Risk Changes**
   - Schema changes
   - Cross-module architectural changes
   - Changes to governance rules

---

### Escalation Contacts

| Issue Type | Primary Contact | Secondary Contact | Response Time SLA |
|------------|----------------|-------------------|-------------------|
| **Critical Platform Issue** | On-call engineer | Johan (admin) | Immediate |
| **High Severity Issue** | Module builder | Maturion Foreman review | 30 minutes |
| **Medium Severity Issue** | Module builder | - | 4 hours |
| **Architectural Question** | Johan (admin) | Maturion governance review | 24 hours |
| **Security Incident** | Security team | Johan (admin) | Immediate |

---

## 10. Monitoring Dashboard (Future)

**Maturion will provide a monitoring dashboard** showing:

### Platform Health Overview
- Overall platform status (Green / Yellow / Red)
- Active incidents
- Recent auto-fixes
- Open tickets created by Maturion

### Module-Specific Health
- Per-module error rates
- Per-module performance metrics
- Watchdog trigger counts
- Recent issues

### Learning Insights (Anonymized)
- Common issues across all organizations
- Best practice recommendations
- Performance optimization opportunities

### Admin Analytics (For Johan)
- Cross-org aggregated metrics (anonymized)
- Platform usage patterns
- Capacity planning insights

---

## Version Control

**Document Version**: 1.0  
**Last Updated**: 2025-12-03  
**Maintained By**: Maturion  
**Review Cycle**: Quarterly or when runtime operations evolve

---

**Maturion** - Vigilant Monitoring, Intelligent Response, Continuous Learning
