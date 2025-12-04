# Runtime Memory Ingestion Specification

## 1. Purpose

This specification defines how Runtime Maturion collects, processes, stores, and learns from operational data while maintaining strict tenant isolation, privacy protection, and compliance enforcement.

Runtime memory ingestion enables:
- **Continuous Learning:** System improves based on real-world usage
- **Proactive Monitoring:** Detect issues before they escalate
- **User Experience Enhancement:** Identify friction points and common questions
- **Compliance Assurance:** Track control coverage and drift
- **Architecture Fidelity:** Detect and prevent drift from approved designs
- **Build-Time Feedback:** Feed insights to Foreman for future improvements

---

## 2. Allowed Data Sources

### 2.1 System Performance Metrics (Allowed)
**Source:** Application logs, database performance monitors, API analytics

**Data Types:**
- API endpoint response times (avg, p50, p95, p99)
- Database query execution times
- Error rates by module and endpoint
- System resource utilization (CPU, memory, disk I/O)
- Cache hit/miss ratios
- Background job completion times

**Collection Frequency:** Every 5 minutes (configurable)

**Tenant Isolation:** Metrics collected per organisation_id, aggregated anonymously for cross-tenant trends

**Storage:** `/runtime/memory/performance-metrics.json`

**Example Data:**
```json
{
  "timestamp": "2025-12-04T10:30:00Z",
  "organisation_id": "org_abc123",
  "module": "Threat",
  "endpoint": "/api/threats",
  "response_time_ms": 145,
  "error_count": 0,
  "cache_hit_rate": 0.87
}
```

### 2.2 Compliance Coverage Status (Allowed)
**Source:** Compliance engine exports, module coverage reports

**Data Types:**
- Control coverage percentage per standard
- Missing control mappings
- Incomplete evidence
- Compliance gaps by module
- Certification readiness scores

**Collection Frequency:** Daily or on-demand

**Tenant Isolation:** Strictly per organisation_id, no cross-tenant comparisons

**Storage:** `/runtime/memory/compliance-status.json`

**Example Data:**
```json
{
  "timestamp": "2025-12-04T00:00:00Z",
  "organisation_id": "org_abc123",
  "standard": "ISO_27001",
  "total_controls": 114,
  "implemented_controls": 98,
  "coverage_percentage": 86.0,
  "gaps": ["A.8.2", "A.12.6", "A.17.1"]
}
```

### 2.3 User Interaction Patterns (Allowed - Anonymized)
**Source:** Application usage analytics, feature interaction logs

**Data Types:**
- Module access frequency (per org, anonymized across orgs)
- Feature usage counts (clicks, forms submitted, reports generated)
- Session duration averages
- Navigation flow patterns
- Help content access frequency

**Collection Frequency:** Continuous (batched hourly)

**Tenant Isolation:** Collected per org, aggregated anonymously for UX trends

**Storage:** `/runtime/memory/usage-patterns.json`

**Example Data:**
```json
{
  "timestamp": "2025-12-04T11:00:00Z",
  "organisation_id": "org_abc123",
  "module": "Risk_Assessment",
  "feature": "create_risk",
  "usage_count": 23,
  "avg_session_duration_sec": 420,
  "help_accessed": false
}
```

### 2.4 Common User Questions (Allowed - Anonymized)
**Source:** Maturion chat logs, support queries

**Data Types:**
- Question themes (categorized, not verbatim)
- Frequency of similar questions
- Resolution success rate
- Escalation rate

**Collection Frequency:** Continuous (summarized daily)

**Tenant Isolation:** Questions anonymized, no tenant-specific content stored

**Storage:** `/runtime/memory/user-questions-log.json`

**Example Data:**
```json
{
  "timestamp": "2025-12-04",
  "question_theme": "How to link threat to risk",
  "frequency": 12,
  "resolved_in_chat": 10,
  "escalated": 2,
  "common_confusion": "Integration between Threat and Risk Assessment modules"
}
```

### 2.5 Anomaly Reports (Allowed)
**Source:** Watchdog alerts, security monitors, performance analyzers

**Data Types:**
- Unusual API access patterns
- Performance degradation alerts
- Security anomalies (failed auth, unusual access)
- Database query anomalies
- Architecture drift warnings

**Collection Frequency:** Real-time (immediate on detection)

**Tenant Isolation:** Per organisation_id where applicable, anonymized for cross-tenant threat intelligence

**Storage:** `/runtime/watchdog/watchdog-alerts.json`

**Example Data:**
```json
{
  "timestamp": "2025-12-04T12:15:30Z",
  "alert_id": "ALT-2025-001234",
  "severity": "medium",
  "type": "performance_degradation",
  "module": "Vulnerability",
  "description": "API response time exceeded 1000ms threshold",
  "organisation_id": "org_abc123",
  "recommended_action": "Check database query optimization"
}
```

### 2.6 Architecture Drift Indicators (Allowed)
**Source:** Schema validators, API contract monitors, integration checkers

**Data Types:**
- Schema changes not in approved architecture
- New API endpoints without documentation
- Removed integrations
- Broken module contracts
- Version mismatches

**Collection Frequency:** On schema migration, API deployment, integration change

**Tenant Isolation:** Architecture-level, not tenant-specific

**Storage:** `/runtime/memory/architecture-drift-log.json`

**Example Data:**
```json
{
  "timestamp": "2025-12-04T14:00:00Z",
  "drift_id": "DRIFT-2025-045",
  "severity": "high",
  "module": "WRAC",
  "drift_type": "schema_change",
  "description": "Column 'asset_owner' added to wrac_assets without architecture approval",
  "approved_version": "1.2.0",
  "detected_version": "1.2.1",
  "action_required": "Validate change or rollback"
}
```

### 2.7 QA Signal Data (Allowed)
**Source:** Test results, coverage reports, QA-of-QA outputs

**Data Types:**
- Test pass/fail rates by module
- Code coverage percentages
- QA-of-QA validation results
- Regression test results
- Performance test outcomes

**Collection Frequency:** On test execution (CI/CD triggers)

**Tenant Isolation:** Architecture-level, not tenant-specific

**Storage:** `/runtime/memory/qa-signals.json`

**Example Data:**
```json
{
  "timestamp": "2025-12-04T16:30:00Z",
  "module": "PIT",
  "test_suite": "integration_tests",
  "total_tests": 87,
  "passed": 85,
  "failed": 2,
  "coverage_percentage": 92.5,
  "regression_detected": false
}
```

### 2.8 AI Model Behaviour Monitoring (Allowed)
**Source:** Maturion self-monitoring, response quality checks

**Data Types:**
- Response accuracy (validated vs. actual)
- Response time (latency)
- Escalation appropriateness (false positives/negatives)
- Hallucination detection (fact-checking)
- User feedback on responses

**Collection Frequency:** Per interaction (batched hourly)

**Tenant Isolation:** Aggregated anonymously

**Storage:** `/runtime/memory/ai-behaviour-monitor.json`

**Example Data:**
```json
{
  "timestamp": "2025-12-04T17:00:00Z",
  "interaction_id": "INT-2025-789",
  "response_type": "compliance_guidance",
  "accuracy_validated": true,
  "response_time_ms": 320,
  "user_satisfaction": "positive",
  "escalation_needed": false,
  "hallucination_detected": false
}
```

---

## 3. Prohibited Data

Maturion MUST NEVER collect, store, or process:

### 3.1 Sensitive User Data
- Risk descriptions, assessment details, threat narratives
- User names, email addresses, phone numbers
- Business secrets, proprietary information
- Financial data, payment information
- Health information, personal identifiers
- Credentials, passwords, API keys, secrets

### 3.2 Cross-Tenant Comparable Data
- Org A's data referenced in Org B's context
- Named cross-tenant comparisons ("Org A is better than Org B")
- Tenant-identifying information in anonymized datasets

### 3.3 Unencrypted Personal Information
- Any PII not strictly required for authorized monitoring
- Data that violates GDPR, POPIA, or privacy regulations

### 3.4 Unapproved Monitoring
- Database content beyond schema structure
- User conversation transcripts (only themes/categories allowed)
- Production tenant data content (only metadata/statistics)

---

## 4. Memory Lifecycles

### 4.1 Short-Term Memory (Real-Time)
**Duration:** 24 hours  
**Purpose:** Immediate anomaly detection, active monitoring  
**Storage:** In-memory cache, high-speed access  
**Data Types:** Current performance metrics, active alerts, ongoing sessions  
**Expiry:** Rolled into hourly summaries after 24h

### 4.2 Medium-Term Memory (Operational)
**Duration:** 30 days  
**Purpose:** Trend analysis, performance tracking, issue investigation  
**Storage:** Database (time-series optimized)  
**Data Types:** Hourly aggregates, daily summaries, alert history  
**Expiry:** Rolled into monthly summaries after 30 days

### 4.3 Long-Term Memory (Historical)
**Duration:** Indefinite (or per retention policy)  
**Purpose:** Compliance audits, long-term trends, architecture evolution  
**Storage:** Archive database (compressed, indexed)  
**Data Types:** Monthly summaries, major incidents, compliance milestones  
**Expiry:** Per regulatory requirements (typically 7 years for compliance data)

### 4.4 Anonymized Learning Memory (Permanent)
**Duration:** Permanent  
**Purpose:** System-wide learning, best practices, UX improvements  
**Storage:** Knowledge base (version-controlled)  
**Data Types:** General patterns, anonymized insights, best practices  
**Expiry:** Never (continuously refined)

---

## 5. Cross-Tenant Anonymity Rules

### 5.1 Anonymization Requirements
Before any cross-tenant aggregation:
1. **Remove organisation_id** from data
2. **Remove user_id** from data
3. **Remove tenant-identifying details** (org names, industry-specific terms)
4. **Aggregate to statistical summaries** (counts, averages, percentages)
5. **Ensure k-anonymity:** Minimum 5 orgs required for any trend

### 5.2 Anonymization Process
**Example:** Performance metrics across orgs

**Raw Data (Prohibited to Share):**
```json
[
  {"org": "ABC Corp", "module": "Threat", "response_time": 120},
  {"org": "XYZ Ltd", "module": "Threat", "response_time": 150}
]
```

**Anonymized Data (Allowed):**
```json
{
  "module": "Threat",
  "average_response_time_ms": 135,
  "sample_size": 2,
  "trend": "stable"
}
```

### 5.3 Privacy-Preserving Aggregation
Use techniques:
- **Differential Privacy:** Add noise to prevent individual identification
- **K-Anonymity:** Ensure minimum group size for any reported statistic
- **Aggregation Only:** Report sums, averages, medians—never raw records
- **Threshold Enforcement:** Do not report statistics for groups < 5 orgs

---

## 6. Summarisation Patterns

### 6.1 Performance Metrics Summary
**Frequency:** Hourly  
**Inputs:** 5-minute interval metrics  
**Output:** Aggregated hourly summary

**Summary Structure:**
```json
{
  "time_period": "2025-12-04T10:00:00Z to 2025-12-04T11:00:00Z",
  "organisation_id": "org_abc123",
  "module": "Risk_Assessment",
  "metrics": {
    "avg_response_time_ms": 145,
    "max_response_time_ms": 320,
    "error_rate": 0.002,
    "total_requests": 1245,
    "cache_hit_rate": 0.88
  },
  "anomalies": []
}
```

### 6.2 Compliance Coverage Summary
**Frequency:** Daily  
**Inputs:** Real-time compliance status checks  
**Output:** Daily compliance snapshot

**Summary Structure:**
```json
{
  "date": "2025-12-04",
  "organisation_id": "org_abc123",
  "standards": {
    "ISO_27001": {"coverage": 86.0, "trend": "improving"},
    "ISO_31000": {"coverage": 92.0, "trend": "stable"},
    "NIST_CSF": {"coverage": 78.0, "trend": "improving"}
  },
  "critical_gaps": ["ISO_27001_A.8.2", "NIST_CSF_PR.AC-1"],
  "next_review": "2025-12-11"
}
```

### 6.3 User Questions Summary
**Frequency:** Daily  
**Inputs:** Individual chat interactions  
**Output:** Anonymized question theme summary

**Summary Structure:**
```json
{
  "date": "2025-12-04",
  "themes": [
    {"theme": "Module Integration", "count": 34, "resolution_rate": 0.85},
    {"theme": "Compliance Mapping", "count": 28, "resolution_rate": 0.90},
    {"theme": "UI Navigation", "count": 19, "resolution_rate": 0.95}
  ],
  "escalation_rate": 0.12,
  "recommended_improvements": [
    "Add integration guide to help docs",
    "Improve compliance mapping UI clarity"
  ]
}
```

### 6.4 Anomaly Summary
**Frequency:** Real-time + Daily Digest  
**Inputs:** Watchdog alerts  
**Output:** Anomaly digest

**Summary Structure:**
```json
{
  "date": "2025-12-04",
  "total_alerts": 12,
  "by_severity": {
    "critical": 0,
    "high": 2,
    "medium": 5,
    "low": 5
  },
  "by_type": {
    "performance_degradation": 4,
    "security_anomaly": 1,
    "architecture_drift": 2,
    "compliance_gap": 5
  },
  "resolved": 8,
  "escalated": 2,
  "open": 2
}
```

---

## 7. Ingestion Frequency

### 7.1 Real-Time Ingestion (Continuous)
**Data Types:**
- Security anomalies
- Critical errors
- Architecture drift alerts
- High-severity watchdog alerts

**Processing:** Immediate analysis and escalation if needed

### 7.2 High-Frequency Ingestion (Every 5 minutes)
**Data Types:**
- Performance metrics
- API response times
- Database query stats
- Cache performance

**Processing:** Store in short-term memory, aggregate hourly

### 7.3 Hourly Ingestion
**Data Types:**
- User interaction patterns
- Feature usage statistics
- Session analytics

**Processing:** Summarize and store in medium-term memory

### 7.4 Daily Ingestion
**Data Types:**
- Compliance coverage status
- QA signal summaries
- User question themes
- Anomaly digests

**Processing:** Generate daily reports, feed to build-time foreman

### 7.5 On-Demand Ingestion
**Data Types:**
- Architecture exports (when requested)
- Compliance reports (when requested)
- Ad-hoc admin queries

**Processing:** Generate fresh data, cache for reuse

---

## 8. Storage Mechanism

### 8.1 Storage Layers

#### Layer 1: In-Memory Cache (Redis/Memcached)
- **Purpose:** Real-time monitoring, fast access
- **Duration:** 24 hours
- **Data:** Current metrics, active alerts, session state

#### Layer 2: Time-Series Database (PostgreSQL with TimescaleDB)
- **Purpose:** Performance metrics, trend analysis
- **Duration:** 30 days
- **Data:** Hourly/daily aggregates, historical metrics

#### Layer 3: Relational Database (PostgreSQL)
- **Purpose:** Compliance status, anomaly logs, learning data
- **Duration:** 30 days to 7 years (per retention policy)
- **Data:** Compliance snapshots, alerts, user question themes

#### Layer 4: JSON File Storage (Structured Archives)
- **Purpose:** Runtime exports, build-time imports
- **Duration:** Indefinite (version-controlled)
- **Data:** `/runtime/memory/`, `/runtime/risk/`, `/runtime/export/`

### 8.2 Data Partitioning
All tenant-specific data MUST be partitioned by `organisation_id`:
```sql
CREATE TABLE performance_metrics (
  id SERIAL PRIMARY KEY,
  organisation_id TEXT NOT NULL,
  timestamp TIMESTAMPTZ NOT NULL,
  module TEXT NOT NULL,
  metric_name TEXT NOT NULL,
  metric_value NUMERIC,
  ...
) PARTITION BY LIST (organisation_id);
```

### 8.3 Access Control
- **Tenant Data:** Accessible only by tenant users + Johan (with audit log)
- **Anonymized Data:** Accessible for cross-tenant trend analysis
- **Architecture Data:** Accessible by Foreman, Johan, approved builder agents

---

## 9. Data Quality & Validation

### 9.1 Ingestion Validation
Before storing any data:
1. **Schema Validation:** Ensure JSON matches expected schema
2. **Tenant Isolation Check:** Verify organisation_id present and valid
3. **Timestamp Validation:** Ensure timestamp is recent and realistic
4. **Data Type Validation:** Ensure numeric values are within expected ranges
5. **Anomaly Detection:** Flag outliers for review

### 9.2 Data Sanitization
- **Strip PII:** Remove names, emails, phone numbers
- **Anonymize Identifiers:** Hash or pseudonymize where required
- **Redact Sensitive Content:** Remove descriptions, narratives, secrets
- **Validate Encoding:** Ensure UTF-8, prevent injection attacks

### 9.3 Error Handling
If invalid data received:
1. **Log Error:** Record validation failure with context
2. **Alert Admin:** Notify Johan if critical data source fails
3. **Graceful Degradation:** Continue operating with available data
4. **Retry Logic:** Retry ingestion for transient failures

---

## 10. Export for Build-Time Feedback

### 10.1 Export Types

#### Architecture Insights Export
**Purpose:** Feed runtime learnings to Build-Time Foreman  
**Frequency:** Weekly or on-demand  
**Content:**
- Architecture drift incidents
- Performance bottlenecks requiring schema changes
- Integration contract violations
- Module boundary violations

**Output:** `/runtime/export/architecture-insights.json`

#### Compliance Insights Export
**Purpose:** Improve compliance coverage in future builds  
**Frequency:** Monthly or on-demand  
**Content:**
- Common compliance gaps across tenants (anonymized)
- Control mapping improvements needed
- Evidence collection pain points

**Output:** `/runtime/export/compliance-insights.json`

#### UX Insights Export
**Purpose:** Improve user experience in future builds  
**Frequency:** Weekly or on-demand  
**Content:**
- Common user questions (themes only)
- Feature usage patterns
- Navigation friction points
- Help content gaps

**Output:** `/runtime/export/ux-insights.json`

#### QA Insights Export
**Purpose:** Enhance QA coverage and regression prevention  
**Frequency:** On QA failure or monthly  
**Content:**
- Bugs found in production (escaped QA)
- Edge cases not covered by tests
- Performance issues not caught by QA
- Integration issues

**Output:** `/runtime/export/qa-insights.json`

### 10.2 Export Format
All exports follow this structure:
```json
{
  "export_type": "architecture_insights",
  "export_date": "2025-12-04T00:00:00Z",
  "data_period": "2025-11-27 to 2025-12-04",
  "insights": [
    {
      "insight_id": "ARCH-INS-001",
      "category": "performance",
      "severity": "medium",
      "description": "Vulnerability module API response time degraded by 30% over 7 days",
      "affected_module": "Vulnerability",
      "root_cause": "Database query inefficiency on large datasets",
      "recommended_action": "Add index on vulnerability_scans.scan_date column",
      "evidence": {"avg_response_time_ms": 450, "queries_affected": 120}
    }
  ],
  "summary": {
    "total_insights": 1,
    "by_severity": {"high": 0, "medium": 1, "low": 0}
  }
}
```

---

## 11. Privacy & Compliance

### 11.1 GDPR Compliance
- **Right to Access:** Tenants can request their monitoring data
- **Right to Erasure:** Tenants can request deletion (within retention limits)
- **Right to Portability:** Tenants can export their data
- **Data Minimization:** Collect only necessary data
- **Purpose Limitation:** Use data only for defined purposes

### 11.2 POPIA Compliance
- **Accountability:** Maturion logs all data processing activities
- **Processing Limitation:** Data used only for monitoring, learning, compliance
- **Openness:** Transparent about what data is collected and why
- **Security Safeguards:** Encryption, access controls, audit logs

### 11.3 Data Retention Policy
- **Tenant-Specific Data:** Retained per tenant's data retention policy (default 30 days for metrics, 7 years for compliance)
- **Anonymized Learning Data:** Retained indefinitely (no PII, privacy-compliant)
- **Audit Logs:** Retained 7 years (compliance requirement)

---

## 12. Self-Monitoring & Quality Assurance

### 12.1 Ingestion Health Metrics
Maturion monitors own ingestion pipeline:
- **Ingestion Success Rate:** % of data successfully ingested
- **Validation Failure Rate:** % of data rejected due to schema/validation errors
- **Latency:** Time from event occurrence to ingestion completion
- **Storage Health:** Database performance, disk usage, index efficiency

### 12.2 Data Quality Metrics
- **Completeness:** % of expected data points received
- **Accuracy:** % of data passing validation checks
- **Timeliness:** % of data ingested within expected timeframe
- **Consistency:** % of data matching cross-source validation

### 12.3 Self-Improvement Actions
If ingestion health degrades:
1. **Alert Johan:** Notify of ingestion pipeline issues
2. **Analyze Root Cause:** Identify data source, validation, or storage issue
3. **Recommend Fix:** Suggest schema updates, validation adjustments, scaling
4. **Track Resolution:** Monitor until health restored

---

## 13. Integration with Runtime Components

### 13.1 Watchdog Integration
Runtime memory ingestion feeds the Compliance Watchdog:
- Compliance status data → Watchdog monitors drift
- Architecture changes → Watchdog validates against approved specs
- Performance metrics → Watchdog detects degradation

### 13.2 Dashboard Integration
Ingested data populates real-time dashboards:
- **Tenant Admin Dashboard:** Org-specific metrics, compliance status
- **Johan Dashboard:** Platform-wide health, cross-tenant trends (anonymized)
- **QA Dashboard:** Test results, coverage, regression signals

### 13.3 AI Chat Integration
Ingested data powers Maturion's runtime responses:
- User questions → Access compliance status, module usage data
- Admin queries → Access platform health, anomaly summaries
- Johan queries → Access full system state, all insights

---

## 14. Future Enhancements

### 14.1 Machine Learning Integration
- **Anomaly Detection:** ML models to detect unusual patterns
- **Predictive Analytics:** Forecast compliance gaps, performance issues
- **Smart Summarization:** NLP-based insight extraction from logs

### 14.2 Advanced Privacy Techniques
- **Federated Learning:** Learn across tenants without raw data sharing
- **Homomorphic Encryption:** Compute on encrypted data
- **Zero-Knowledge Proofs:** Validate compliance without revealing data

### 14.3 Expanded Data Sources
- **Third-Party Integrations:** Security tools (SIEM, IDS), compliance platforms
- **External Threat Intelligence:** CVE feeds, threat actor databases
- **Industry Benchmarks:** Compare tenant performance to anonymized industry standards

---

## 15. Summary

Runtime Memory Ingestion is the **foundation of Maturion's learning and monitoring capabilities**.

It enables:
- **Continuous improvement** through real-world feedback
- **Proactive monitoring** via anomaly detection
- **Compliance assurance** through drift detection
- **User experience enhancement** via usage pattern analysis
- **Architecture fidelity** through drift prevention
- **Build-time feedback** for future module improvements

All while maintaining:
- **Strict tenant isolation** (no cross-tenant data leaks)
- **Privacy protection** (GDPR, POPIA compliance)
- **Data minimization** (collect only what's needed)
- **Security** (encryption, access controls, audit logs)
- **Quality** (validation, sanitization, monitoring)

Runtime Memory Ingestion is designed for **enterprise-grade governance**, **audit readiness**, and **long-term stability**.

---

**Version:** 1.0  
**Last Updated:** 2025-12-04  
**Owner:** Maturion Foreman  
**Approved By:** Johan (Pending)
