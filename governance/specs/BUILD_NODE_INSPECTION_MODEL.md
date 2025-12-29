# Build Node Inspection Model (G-C9)

**Version**: 1.0.0  
**Status**: Active  
**Authority**: BUILD_TREE_EXECUTION_MODEL.md (G-C8)  
**Last Updated**: 2025-12-29  
**Owner**: Johan (MaturionISMS)  
**Code**: G-C9

---

## I. Purpose

This document defines the **canonical model for build node inspection and drill-down**, enforcing the principle: **"No status without explanation."**

Every build node status, state, or indicator MUST be fully explainable through inspection. No status may be displayed without the ability to drill down to its underlying evidence, decisions, and governing rules.

**Scope**: This is a governance and data model specification for read-only inspection. It defines WHAT can be inspected and HOW data is structured. It does NOT define UI implementation details.

---

## II. Core Principle: No Status Without Explanation

### 2.1 Definition

**"No status without explanation"** means:

- Every execution state has a clear reason
- Every activation state has an authorization trail
- Every status indicator (Red/Amber/Green) has supporting evidence
- Every blocker has a specific cause and resolution path
- Every decision has an authority and rationale
- Every STOP condition has clear recovery criteria

### 2.2 Enforcement

The inspection model MUST provide:

1. **Full Traceability**: From any status back to its root causes
2. **Complete Evidence**: All artifacts that support current state
3. **Decision History**: Who decided what, when, and why
4. **Governing Rules**: Which checks/requirements apply
5. **Blocking Items**: What prevents progress and how to unblock
6. **STOP Conditions**: What safety mechanisms are active

---

## III. Inspectable Node Types

### 3.1 Program Node Inspection

**Available Information**:
- Current execution and activation states
- Status indicator with explanation
- Overall completion calculation methodology
- Aggregate evidence from all waves
- Program-level decisions and approvals
- Strategic blockers and dependencies
- Program charter and goals
- Ownership and authority chain

### 3.2 Wave Node Inspection

**Available Information**:
- Current execution and activation states
- Status indicator with explanation
- Completion calculation (tasks complete / tasks total)
- Wave planning document
- Task evidence aggregation
- Wave-level blockers and dependencies
- Sequencing rules and prerequisites
- Sub-wave structure (if applicable)

### 3.3 Task Node Inspection

**Available Information**:
- Current execution and activation states
- Status indicator with explanation
- Binary completion status (0% or 100%)
- Builder assignment and history
- Complete evidence set:
  - Architecture documents
  - QA test results
  - Build artifacts (PR links)
  - Completion validation
- Task-level blockers
- PR status and merge history
- Timeline (created, started, completed)

---

## IV. Inspection Data Model

### 4.1 Node Inspection Response

```typescript
interface NodeInspectionData {
  // Core Identity
  node_id: string;
  node_type: 'program' | 'wave' | 'sub-wave' | 'task';
  name: string;
  description: string;
  
  // Current State (with explanations)
  current_state: StateExplanation;
  
  // Governing Rules
  governing_checks: GoverningCheck[];
  requirements: Requirement[];
  
  // Evidence
  evidence: Evidence[];
  evidence_summary: EvidenceSummary;
  
  // Decisions
  decisions: Decision[];
  
  // Blockers
  blockers: Blocker[];
  blocker_resolution_paths: ResolutionPath[];
  
  // STOP Conditions
  stop_conditions: StopCondition[];
  
  // Audit Trail
  audit_reports: AuditReport[];
  surveys: Survey[];
  
  // Metadata
  created_at: string;
  updated_at: string;
  last_inspected_at: string;
}
```

### 4.2 State Explanation

```typescript
interface StateExplanation {
  execution_state: string;
  execution_state_reason: string;
  execution_state_since: string;
  
  activation_state: string;
  activation_state_reason: string;
  activation_state_since: string;
  
  status: 'RED' | 'AMBER' | 'GREEN';
  status_reason: string;
  status_contributing_factors: StatusFactor[];
  
  completion_percentage: number;
  completion_calculation: string;  // Explanation of how % was calculated
  completion_is_authoritative: boolean;  // Always false for informational %
}

interface StatusFactor {
  factor_type: 'qa_failure' | 'blocker' | 'dependency' | 'evidence_missing' | 'approval_pending';
  description: string;
  severity: 'MINOR' | 'MAJOR' | 'CRITICAL';
  contributing_to: 'RED' | 'AMBER' | 'GREEN';
}
```

### 4.3 Governing Check

```typescript
interface GoverningCheck {
  check_id: string;
  check_name: string;
  check_type: 'architecture' | 'qa' | 'compliance' | 'governance' | 'build';
  description: string;
  required: boolean;
  status: 'PASS' | 'FAIL' | 'PENDING' | 'NOT_APPLICABLE';
  last_checked_at?: string;
  failure_reason?: string;
}
```

### 4.4 Requirement

```typescript
interface Requirement {
  requirement_id: string;
  requirement_name: string;
  requirement_type: 'architecture' | 'qa' | 'evidence' | 'approval' | 'dependency';
  description: string;
  mandatory: boolean;
  satisfied: boolean;
  satisfied_at?: string;
  satisfied_by?: string;
  unsatisfied_reason?: string;
}
```

### 4.5 Evidence (Extended)

```typescript
interface Evidence {
  id: string;
  category: 'ARCHITECTURE' | 'QA' | 'BUILD' | 'COMPLETION';
  artifact_type: string;
  artifact_location: string;  // URL or path (read-only link)
  artifact_description: string;
  validated: boolean;
  validated_at?: string;
  validated_by?: string;
  validation_notes?: string;
  metadata?: Record<string, any>;
}

interface EvidenceSummary {
  total_evidence_items: number;
  validated_items: number;
  pending_items: number;
  by_category: {
    ARCHITECTURE: number;
    QA: number;
    BUILD: number;
    COMPLETION: number;
  };
}
```

### 4.6 Decision

```typescript
interface Decision {
  decision_id: string;
  decision_type: 'approval' | 'rejection' | 'escalation' | 'override' | 'authorization';
  decision_summary: string;
  decision_rationale: string;
  decision_authority: string;  // Who made the decision (Johan, Foreman, etc.)
  decided_at: string;
  related_node_id?: string;
  related_evidence_ids?: string[];
}
```

### 4.7 Resolution Path

```typescript
interface ResolutionPath {
  blocker_id: string;
  resolution_strategy: string;
  unblocking_criteria: string[];
  estimated_resolution_time?: string;
  owner: string;  // Who is responsible for resolving
  status: 'PLANNED' | 'IN_PROGRESS' | 'COMPLETED' | 'BLOCKED';
}
```

### 4.8 STOP Condition

```typescript
interface StopCondition {
  stop_id: string;
  stop_type: 'qa_failure' | 'governance_violation' | 'dependency_failure' | 'escalation_required';
  stop_description: string;
  triggered_at: string;
  triggered_by: string;
  severity: 'WARNING' | 'ERROR' | 'CRITICAL';
  recovery_status: 'NOT_STARTED' | 'IN_PROGRESS' | 'RESOLVED';
  recovery_actions: string[];
  resolved_at?: string;
}
```

### 4.9 Audit Report

```typescript
interface AuditReport {
  report_id: string;
  report_type: 'evidence_validation' | 'qa_audit' | 'compliance_check' | 'governance_review';
  report_title: string;
  report_location: string;  // URL or path (read-only link)
  created_at: string;
  created_by: string;
  findings_summary: string;
}
```

### 4.10 Survey

```typescript
interface Survey {
  survey_id: string;
  survey_type: string;
  survey_title: string;
  survey_location: string;  // URL or path (read-only link)
  conducted_at: string;
  respondent: string;
  summary: string;
}
```

---

## V. Inspection Depth Hierarchy

### 5.1 Level 1: Quick Status View

**What**: Node name, current states, status indicator  
**Purpose**: At-a-glance health check  
**Depth**: Surface information only

**Example**:
```
Task: AI Panel  [IN_PROGRESS] [ACTIVE] [🟢 GREEN] [0%]
```

### 5.2 Level 2: State Explanation

**What**: Why is the node in this state?  
**Purpose**: Understand current status reasoning  
**Depth**: State explanations + status factors

**Example**:
```
Execution State: IN_PROGRESS
  Reason: Builder is actively implementing UI components
  Since: 2025-12-29T10:00:00Z

Status: GREEN
  Reason: On track, no blockers, QA plan ready
  Contributing Factors:
    - ✅ Architecture complete (MAJOR)
    - ✅ QA suite in RED status (MAJOR)
    - ✅ No blockers (MAJOR)
```

### 5.3 Level 3: Evidence & Requirements

**What**: Supporting artifacts and governing rules  
**Purpose**: Verify compliance and readiness  
**Depth**: Evidence items + governing checks + requirements

**Example**:
```
Evidence (4/4 validated):
  ✅ Architecture: ai-panel-spec.md
  ✅ QA: 15/15 tests passing
  ✅ Build: PR#145 merged
  ✅ Completion: Validated by Foreman

Governing Checks (3/3 PASS):
  ✅ Architecture Completeness Check
  ✅ QA Coverage Check (100% coverage)
  ✅ Zero Test Debt Check

Requirements (5/5 satisfied):
  ✅ Architecture document exists
  ✅ QA suite shows 100% pass
  ✅ Zero test debt confirmed
  ✅ PR merged to main
  ✅ Foreman sign-off obtained
```

### 5.4 Level 4: Decisions & Audit Trail

**What**: Who decided what, when, and why  
**Purpose**: Full accountability and traceability  
**Depth**: Decision history + audit reports + surveys

**Example**:
```
Decisions (2):
  1. Approval to proceed (Johan, 2025-12-29T09:00:00Z)
     Rationale: Architecture complete, QA plan validated
  
  2. Builder assignment: ui-builder (Foreman, 2025-12-29T09:15:00Z)
     Rationale: Task scope matches UI builder expertise

Audit Reports (1):
  - Evidence Validation Report (Foreman, 2025-12-29T09:10:00Z)
    Findings: All evidence validated, no issues found
```

### 5.5 Level 5: Blockers & STOP Conditions

**What**: What's preventing progress or requiring attention  
**Purpose**: Identify remediation actions  
**Depth**: Active blockers + STOP conditions + resolution paths

**Example**:
```
Active Blockers (1):
  ⛔ BLOCKER-001: Dependency on API endpoint
     Type: DEPENDENCY
     Severity: MAJOR
     Created: 2025-12-29T11:00:00Z
     Resolution Path:
       - Wait for API task completion (api-builder)
       - Unblocking criteria: API endpoint deployed and tested
       - Owner: api-builder
       - Status: IN_PROGRESS

STOP Conditions (0):
  No active STOP conditions
```

---

## VI. Read-Only Enforcement

### 6.1 Inspection is Observation Only

**Rules**:
- Inspection MUST NOT modify any state
- Inspection MUST NOT create or delete evidence
- Inspection MUST NOT authorize state transitions
- Inspection MUST NOT resolve blockers
- Inspection MUST NOT approve or reject nodes
- Inspection MUST NOT execute any workflows

### 6.2 Audit Logging

Every inspection access MUST be logged:

```typescript
interface InspectionAuditLog {
  log_id: string;
  node_id: string;
  node_type: string;
  inspected_by: string;  // User or system
  inspected_at: string;
  inspection_depth: 1 | 2 | 3 | 4 | 5;
  ip_address?: string;
  user_agent?: string;
}
```

### 6.3 Security

- All inspection endpoints MUST be read-only (GET requests only)
- All artifact links MUST point to read-only resources
- No mutation operations allowed via inspection interface
- Tenant isolation MUST be enforced (organisation_id filtering)

---

## VII. API Contract

### 7.1 Node Inspection Endpoint

```
GET /api/build-tree/inspect/:node_type/:node_id
```

**Parameters**:
- `node_type`: `program`, `wave`, `sub-wave`, or `task`
- `node_id`: Unique identifier for the node

**Query Parameters**:
- `depth`: `1` | `2` | `3` | `4` | `5` (inspection depth level, default: `3`)
- `include_children`: `true` | `false` (include child nodes, default: `false`)

**Response**:
```json
{
  "success": true,
  "data": {
    "node_id": "task-ai-panel",
    "node_type": "task",
    "name": "AI Panel Implementation",
    "description": "Build AI assistance panel UI component",
    "current_state": { ... },
    "governing_checks": [ ... ],
    "requirements": [ ... ],
    "evidence": [ ... ],
    "evidence_summary": { ... },
    "decisions": [ ... ],
    "blockers": [ ... ],
    "blocker_resolution_paths": [ ... ],
    "stop_conditions": [ ... ],
    "audit_reports": [ ... ],
    "surveys": [ ... ],
    "created_at": "2025-12-29T08:00:00Z",
    "updated_at": "2025-12-29T12:00:00Z",
    "last_inspected_at": "2025-12-29T13:00:00Z"
  }
}
```

### 7.2 Evidence Artifact Access

All evidence artifacts MUST be accessible via read-only URLs:

```
GET /api/evidence/:evidence_id/artifact
```

**Response**: Redirects to artifact location or returns artifact content (read-only).

---

## VIII. Governance Integration

### 8.1 GSR Enforcement

Inspection model enforces **Governance Supremacy Rule (GSR)**:

1. **100% QA Passing**: Inspection shows actual QA test results, not estimates
2. **Zero Test Debt**: Inspection exposes any skipped/incomplete tests
3. **Architecture Conformance**: Inspection shows architecture validation status
4. **Constitutional Protection**: Inspection alerts if protected paths modified

### 8.2 Build Philosophy Alignment

Inspection model supports **Five Build Philosophy Principles**:

1. **One-Time Build Correctness**: Inspection shows architecture completeness before build
2. **Zero Regression**: Inspection shows regression test evidence
3. **Full Architectural Alignment**: Inspection shows architecture validation results
4. **Zero Loss of Context**: Inspection preserves all decisions and rationales
5. **Zero Ambiguity**: Inspection shows explicit acceptance criteria and evidence

---

## IX. Explicit Exclusions

### 9.1 NOT Inspectable

The following are **explicitly excluded** from inspection:

- **Raw Cognitive Reasoning**: Internal AI agent thought processes
- **Model Internals**: Neural network weights, training data, prompts
- **Uninterpreted Logs**: Raw log dumps without structure
- **Sensitive Credentials**: API keys, passwords, tokens
- **Draft/Incomplete Analyses**: Work-in-progress without validation
- **Personal Data**: User PII beyond audit trail requirements

### 9.2 Rationale

These exclusions enforce:
- **Clarity**: Only show structured, interpreted information
- **Security**: Protect sensitive data
- **Quality**: Only show validated, complete information
- **Privacy**: Respect data protection requirements

---

## X. UI Guidelines (Informational)

While UI implementation is out of scope for this governance spec, here are recommended practices:

### 10.1 Drill-Down Navigation

- Start with Level 1 (quick status view)
- Allow progressive disclosure to deeper levels
- Provide breadcrumb navigation
- Support keyboard shortcuts
- Enable search/filter within inspection view

### 10.2 Visual Hierarchy

- Use collapsible sections for each inspection level
- Group related information (states, evidence, decisions, blockers)
- Use icons and colors for quick scanning
- Maintain consistency with build tree visualization

### 10.3 Evidence Links

- Make all evidence artifacts clickable (read-only)
- Open in new tab/window to preserve inspection context
- Show artifact type and validation status
- Provide download option for reports

### 10.4 Responsive Design

- Ensure inspection view works on all screen sizes
- Prioritize most important information on mobile
- Allow horizontal scroll for wide data tables
- Support print/export for audit purposes

---

## XI. Compliance & Audit Readiness

### 11.1 Audit Trail Requirements

All inspection data MUST support:
- **Who**: Which user or system performed inspection
- **What**: Which node was inspected and to what depth
- **When**: Timestamp of inspection
- **Why**: Context or reason for inspection (if available)

### 11.2 Data Retention

- Inspection audit logs: Retain for 7 years (ISO 27001 compliance)
- Evidence artifacts: Permanent retention (version-controlled)
- Decision records: Permanent retention
- Audit reports: Permanent retention

### 11.3 Access Control

- Inspection access MUST respect tenant isolation
- Read-only access MUST be enforced at API level
- No bypass mechanisms allowed
- Failed access attempts MUST be logged

---

## XII. For Complete Details

This document provides the canonical model for build node inspection.

**Related Specifications**:
- **BUILD_TREE_EXECUTION_MODEL.md (G-C8)**: Core data model
- **ACTIVATION_STATE_MODEL.md**: Activation state definitions
- **COMMISSIONING_EVIDENCE_MODEL.md**: Evidence categories
- **AUDIT_READINESS_MODEL.md**: Audit requirements (when created)
- **build-tree-visualization-spec.md**: UI visualization spec

---

*END OF BUILD NODE INSPECTION MODEL (G-C9)*
