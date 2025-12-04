# Production to Test Switch Protocol

## Purpose

Define controlled protocols for routing scenarios between production and test environments for validation purposes.

---

## 1. Use Cases

This protocol applies when:

- Testing a critical fix before production deployment
- Validating new feature with production-like load patterns
- Comparing behaviour between versions
- Performance baseline testing

---

## 2. Switch Types

### 2.1 Shadow Testing
- Production traffic is mirrored to test (read-only)
- Test environment processes but does not respond
- Used for performance and behaviour validation

### 2.2 Canary Testing
- Small percentage of production traffic routed to new version in test
- Monitored for errors and performance
- Can be rolled back instantly

### 2.3 Blue-Green Testing
- Two identical environments (current and new version)
- Traffic can be switched between them
- Full rollback capability

---

## 3. Safety Controls

- [ ] All switches must be logged
- [ ] All switches must have rollback plan
- [ ] All switches require Foreman + Human Admin approval
- [ ] No tenant data writes in test environment
- [ ] All responses from test must be clearly marked

---

## 4. Monitoring Requirements

During any switch operation:

- Real-time error rate monitoring
- Real-time latency monitoring
- Real-time health check validation
- Automated rollback on threshold breach

---

## 5. Approval Matrix

| Switch Type | Foreman | Human Admin | Duration Limit |
|------------|---------|-------------|----------------|
| Shadow     | Required | Informed    | 24 hours       |
| Canary     | Required | Required    | 4 hours        |
| Blue-Green | Required | Required    | 1 hour         |
