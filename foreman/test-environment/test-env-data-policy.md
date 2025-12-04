# Test Environment Data Policy

## Purpose

Define strict rules for data usage in test environments to protect tenant privacy and maintain compliance.

---

## 1. Prohibited Data

The following **MUST NEVER** be used in test environments:

- Real tenant data
- Real user credentials
- Real customer names, emails, or identifiers
- Real business secrets or proprietary information
- Production database snapshots (unless fully anonymized and approved)

---

## 2. Allowed Data Types

1. **Synthetic Data**
   - Generated test data following realistic patterns
   - No relation to real tenants
   - Clearly marked as synthetic

2. **Masked Data**
   - Production data with all PII removed/masked
   - Requires explicit approval process
   - Must pass privacy guardrail validation

3. **Reference Data**
   - Standards, frameworks, compliance libraries
   - Public domain information
   - Architecture and QA metadata

---

## 3. Data Lifecycle

- Test data is created at deployment time
- Test data is refreshed on each test run
- Test data is purged after test completion
- No test data persists between versions

---

## 4. Validation

Before any data is used in test:

- [ ] Verified no PII present
- [ ] Verified no tenant identifiers
- [ ] Verified no production secrets
- [ ] Approved by data policy owner
- [ ] Logged in change management system

---

## 5. Emergency Protocols

If production data accidentally enters test environment:

1. Immediately halt all test activities
2. Purge affected data
3. Document incident
4. Investigate root cause
5. Update controls to prevent recurrence
