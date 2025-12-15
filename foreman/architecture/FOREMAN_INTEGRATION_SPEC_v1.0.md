# FOREMAN_INTEGRATION_SPEC_v1.0.md

## Johan's Foreman Office — Integration Specification

**Version**: 1.0  
**Date**: 2025-12-15

---

## 1. INBOUND INTERACTIONS

### 1.1 From Johan (Human Governor)
- **Intent Definition**: Johan provides program intent via UI
- **Plan Approval**: Johan approves or rejects execution plans
- **Decision Requests**: Johan responds to blocker escalations
- **Owner Override**: Johan invokes temporary rule overrides

### 1.2 From Builder Agents
- **Heartbeat**: Builders send heartbeat every 60s
- **Progress Updates**: Builders report task progress
- **Completion Claims**: Builders claim task completion
- **Escalations**: Builders escalate blockers

### 1.3 From GitHub
- **Repository Events**: Push events, PR events
- **Issue Comments**: (Future: real-time comment monitoring)

---

## 2. OUTBOUND INTERACTIONS

### 2.1 To Builder Agents
- **Build Instructions**: "Build to Green" instructions
- **Task Assignments**: Task assignment notifications
- **Guidance**: Mid-execution guidance (rare)

### 2.2 To GitHub
- **PR Creation**: Create PRs for completed tasks
- **PR Updates**: Update PR descriptions with progress
- **Issue Updates**: Update issue status
- **Commit Status**: Report build status

### 2.3 To Memory Fabric
- **Governance Logs**: Write governance events
- **Execution Logs**: Write execution state
- **Evidence**: Store evidence artifacts

---

## 3. EVENTS CONSUMED

- Builder heartbeat events
- Task state change events
- Blocker detection events
- Governance violation events
- QA execution completed events

---

## 4. EVENTS PRODUCED

- Program state changed
- Wave state changed
- Task state changed
- Blocker created
- Blocker resolved
- Governance violation detected

---

## 5. API CALLS MADE

### 5.1 GitHub API
- `GET /repos/:owner/:repo/issues`
- `POST /repos/:owner/:repo/pulls`
- `PATCH /repos/:owner/:repo/pulls/:number`
- `POST /repos/:owner/:repo/issues/:number/comments`

### 5.2 Builder Backends
- `POST /builder/execute` (send "Build to Green" instruction)
- `GET /builder/status` (check builder availability)

### 5.3 Memory Fabric API
- `POST /memory/store` (store governance/execution memory)
- `GET /memory/query` (query historical context)

---

## 6. API ENDPOINTS EXPOSED

### 6.1 Builder API
- `POST /api/heartbeat` - Receive builder heartbeats
- `POST /api/task/complete` - Builder claims task completion
- `POST /api/escalation` - Builder escalates blocker

### 6.2 Johan UI API
- `GET /api/programs` - List programs
- `GET /api/programs/:id` - Get program details
- `POST /api/programs/:id/approve` - Approve plan
- `POST /api/blockers/:id/resolve` - Resolve blocker

---

## 7. DATA CONTRACTS

### 7.1 "Build to Green" Instruction Contract
```json
{
  "taskId": "uuid",
  "instruction": "Build to Green",
  "architecture": {
    "location": "path/to/architecture.md",
    "summary": "Brief description"
  },
  "qaSuite": {
    "location": "path/to/qa/",
    "status": "RED",
    "totalTests": 10,
    "failing": 10
  },
  "acceptanceCriteria": ["All tests passing (100%)"]
}
```

### 7.2 Heartbeat Contract
```json
{
  "builderId": "ui-builder",
  "taskId": "uuid",
  "timestamp": "ISO 8601",
  "status": "active",
  "progressPercentage": 45
}
```

---

## 8. ERROR HANDLING

- GitHub API failures: Retry with exponential backoff
- Builder backend failures: Fallback to local builder
- Memory fabric failures: Local cache fallback

---

## 9. MODULE ISOLATION

- No direct access to other module databases
- All inter-module communication via defined APIs
- Evidence stored in Foreman's own tables

---

*Generated for Issue #2 - Architecture & QA Design (Wave 0 Completion)*
