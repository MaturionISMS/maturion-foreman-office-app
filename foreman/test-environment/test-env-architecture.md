# Test Environment Architecture

## Purpose

Describes how the test environment mirrors production:

- Same module boundaries
- Similar configuration (minus secrets)
- Simulated or masked external dependencies
- Ability to exercise full ISMS workflows without tenant risk

---

## 1. Structure

The test environment consists of:

1. **Application Layer**
   - All ISMS modules deployed in test mode
   - Feature flags enabled for testing
   - Monitoring enabled but in test mode

2. **Data Layer**
   - Separate database instance (never production)
   - Synthetic or masked data only
   - Schema mirroring production

3. **Integration Layer**
   - Mock external services where appropriate
   - Test connectors for edge functions
   - Internal module integration paths identical to production

4. **AI Layer**
   - Same AI routing logic
   - Test-safe prompts and guardrails
   - Ability to test drift detection

---

## 2. Isolation Rules

- Test environment **MUST NOT** connect to production databases.
- Test environment **MUST NOT** send real notifications to users.
- Test environment **MUST** maintain clear visual indicators (headers, banners) that it is not production.

---

## 3. Data Policy Reference

See `foreman/test-environment/test-env-data-policy.md` for strict rules on test data.

---

## 4. Deployment Sequencing

See `foreman/test-environment/test-env-deployment-plan.md` for how builder agents deploy to test.
