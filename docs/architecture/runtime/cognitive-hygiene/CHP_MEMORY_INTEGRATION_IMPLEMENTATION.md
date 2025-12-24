# CHP Memory Integration - Implementation Guide

## Overview

This implementation provides the **Cognitive Hygiene Protocol (CHP) Memory Integration** as specified in:
```
docs/architecture/runtime/cognitive-hygiene/CHP_MEMORY_INTEGRATION_ARCHITECTURE.md
```

## Core Principle

**CHP Proposes, Never Decides**

- CHP is a **detection and advisory system**, not a decision-making authority
- CHP reads memory to understand governance, architecture, and patterns
- CHP detects drift and proposes corrections
- CHP **never** auto-applies changes without approval
- CHP **never** accesses tenant data

## Implementation Components

### 1. CHP Authorization Service
**Location:** `lib/memory/chp-authorization.ts`

Enforces scope-based read authorization for CHP:

- ✅ **Allowed Read Scopes:** `global`, `foreman`, `experience`
- ❌ **Denied Read Scopes:** `runtime`, `platform` (contain tenant data)
- ❌ **Write Operations:** All writes denied (must use proposals)

```typescript
import { chpAuthorization, ActorType } from '@/lib/memory/chp-authorization';

// Check authorization
const result = chpAuthorization.authorize({
  actor: 'CHP',
  actorType: ActorType.CHP,
  action: 'read',
  scopes: ['global', 'foreman', 'experience'],
  reason: 'Analyzing agent behavior'
});

// result.authorized === true
// result.allowedScopes === ['global', 'foreman', 'experience']
```

**Authorization Matrix:**

| Actor Type | Read Scopes | Write Scopes | Requires Proposal |
|-----------|-------------|--------------|-------------------|
| CHP | global, foreman, experience | (none) | Yes |
| FOREMAN | (all) | global, foreman, experience | No |
| RUNTIME_AGENT | global, foreman, runtime, platform | runtime | Yes (for non-runtime) |
| BUILDER | global, foreman | (none) | Yes |
| HUMAN | (all) | (all) | No |
| WATCHDOG | (all) | (none) | No |

### 2. CHP Proposal Generator
**Location:** `lib/memory/chp-proposal-generator.ts`

Generates well-structured CHP proposals with:

- Unique proposal IDs (`CHP-YYYY-NNNNNN` format)
- Evidence and context
- Recommended actions
- Precedent references
- Automatic approval routing

```typescript
import { chpProposalGenerator, ProposalCategory, ProposalSeverity } from '@/lib/memory/chp-proposal-generator';

// Generate architecture drift proposal
const proposal = chpProposalGenerator.generateArchitectureDriftProposal(
  'ui-builder',
  'add_database_import',
  'ARCH-2024-089: All modules must use API layer',
  'Asset',
  [
    'Revert database import',
    'Update UI Builder context with module boundary rules',
    'Re-attempt via API layer'
  ],
  'chp-session-123'
);

// Proposal routing
const routing = chpProposalGenerator.getRoutingTarget(proposal);
// routing.approver === 'Foreman' (for architecture_drift)
// routing.notificationMethod === 'dashboard' (for medium severity)
```

**Proposal Categories:**

| Category | Severity Levels | Approver | Auto-Apply Allowed |
|----------|----------------|----------|--------------------|
| `architecture_drift` | Low-Critical | Foreman | ❌ Never |
| `governance_violation` | Any | Johan | ❌ Never |
| `qa_gap` | Low-High | Foreman | ❌ Never |
| `documentation_gap` | Low-Medium | Foreman | ⚠️ Only if pre-authorized |
| `pattern_improvement` | Low | Foreman | ⚠️ Only if pre-authorized |
| `privacy_violation` | Any | Johan | ❌ Never (immediate escalation) |

### 3. CHP Client
**Location:** `lib/memory/chp-client.ts`

Unified client integrating authorization, audit logging, and proposals:

```typescript
import { chpClient, CHPMode } from '@/lib/memory/chp-client';

// Initialize CHP
await chpClient.initialize();

// Read memory with authorization
const result = await chpClient.readMemory({
  scopes: ['global', 'foreman'],
  tags: ['architecture', 'governance'],
  importanceMin: 'high',
  reason: 'Analyzing agent deviation from module boundary rules',
  sessionId: 'chp-session-123'
});

// result.authorized === true
// result.entries === [...memory entries...]
// result.scopesRead === ['global', 'foreman']
// result.scopesDenied === []

// Submit a proposal
const proposal = await chpClient.submitProposal({
  category: ProposalCategory.ARCHITECTURE_DRIFT,
  severity: ProposalSeverity.MEDIUM,
  title: 'Agent violated module boundary rule',
  description: 'UI Builder attempted direct database access...',
  evidence: {
    drift_detected_at: new Date().toISOString(),
    agent: 'ui-builder',
    action: 'add_database_import',
    module: 'Asset',
    violated_rule: 'ARCH-2024-089'
  },
  recommendedAction: {
    type: 'revert_and_educate',
    steps: ['Revert change', 'Update context', 'Re-attempt via API']
  }
});

// Convenience methods
const proposal = await chpClient.reportArchitectureDrift(
  'ui-builder',
  'add_database_import',
  'ARCH-2024-089',
  'Asset',
  ['Revert change', 'Update context', 'Re-attempt via API'],
  'chp-session-123'
);

const proposal = await chpClient.reportPrivacyViolation(
  'global',
  'entry-123',
  'PII detected in summary field',
  ['Redact PII', 'Update entry', 'Notify privacy officer'],
  'chp-session-123'
);
```

### 4. CHP Modes

CHP adapts to memory lifecycle state:

| Memory State | CHP Mode | Behavior |
|--------------|----------|----------|
| USABLE | NORMAL | Full functionality |
| DEGRADED | DEGRADED | Limited context (e.g., experience scope unavailable) |
| FAILED | CONSERVATIVE | Detects drift but cannot generate proposals |
| UNINITIALIZED, LOADING, VALIDATING | CONSERVATIVE | Waiting for memory to be ready |

```typescript
// Check CHP health
const health = chpClient.getHealthStatus();
// health.mode === CHPMode.NORMAL
// health.memoryState === MemoryLifecycleState.USABLE
// health.canRead === true
// health.canGenerateProposals === true
```

## Audit Trail

Every CHP memory read is audited:

```json
{
  "timestamp": "2025-12-24T14:30:00Z",
  "actor": "CHP",
  "actorType": "CHP",
  "action": "read_memory",
  "scopesAccessed": ["global", "foreman"],
  "tagsQueried": ["architecture", "governance"],
  "importanceMin": "high",
  "entriesReturned": 15,
  "reason": "Analyzing agent deviation from module boundary rules",
  "sessionId": "chp-session-789",
  "authorized": true
}
```

**Audit Storage:** `runtime/audit/chp-memory-reads.json` (append-only, immutable)  
**Retention:** 7 years (compliance requirement)

Access audit trail:

```typescript
const auditTrail = chpClient.getAuditTrail({
  since: new Date('2025-12-24'),
  limit: 100
});
```

## Proposal Workflow

### Submission

1. CHP detects drift or issue
2. CHP queries memory for context and precedent
3. CHP generates proposal
4. CHP writes proposal to `runtime/proposals/pending/{proposal_id}.json`
5. CHP emits `proposal-generated` event
6. Routing system notifies approver

### Approval

```
runtime/proposals/pending/CHP-2025-000001.json
  ↓ (Foreman/Johan reviews and approves)
runtime/proposals/approved/CHP-2025-000001.json
  ↓ (Action executed)
experience scope updated with outcome
```

### Rejection

```
runtime/proposals/pending/CHP-2025-000001.json
  ↓ (Foreman/Johan reviews and rejects with reason)
runtime/proposals/rejected/CHP-2025-000001.json
  ↓ (CHP learns from rejection)
experience scope updated with lesson
```

## No Auto-Promotion Enforcement

**Core Rule:** CHP proposals **MUST NOT** be auto-applied without explicit approval.

**Enforcement Mechanisms:**

1. **Code-Level:** CHP cannot call execution functions directly
2. **Approval Token:** Execution requires approval token (generated only by Foreman/Johan)
3. **Audit:** All CHP actions logged with `requires_approval: true/false`
4. **Watchdog:** Monitors for CHP actions without approval tokens

**Auto-Apply Policy:**

- ❌ **Never auto-apply:** Architecture, governance, code, privacy, security changes
- ⚠️ **May auto-apply (if pre-authorized):** Documentation corrections, logging additions
- ✅ **Pre-authorization:** Defined in `governance/chp-auto-apply-policy.json`

## Testing

Run CHP integration tests:

```bash
pytest tests/test_chp_memory_integration.py -v
```

**Test Coverage:**

- ✅ CHP authorization (7 tests)
- ✅ CHP audit logging (5 tests)
- ✅ CHP proposal generation (7 tests)
- ✅ CHP proposal workflow (5 tests)
- ✅ No auto-promotion (6 tests)
- ✅ CHP failure handling (4 tests)
- ✅ CHP integration (4 tests)

**Total: 38 tests, all passing**

## Directory Structure

```
lib/memory/
├── chp-authorization.ts      # Authorization service
├── chp-proposal-generator.ts # Proposal generator
├── chp-client.ts             # Unified CHP client
├── audit-logger.ts           # Audit logging (enhanced)
├── lifecycle-manager.ts      # Memory lifecycle (existing)
└── index.ts                  # Exports

runtime/
├── proposals/
│   ├── pending/              # Pending proposals
│   ├── approved/             # Approved proposals
│   ├── rejected/             # Rejected proposals
│   └── under_review/         # Under review (optional)
└── audit/
    └── chp-memory-reads.json # CHP audit log

tests/
└── test_chp_memory_integration.py  # CHP tests
```

## Integration Points

### With Memory Fabric

- CHP uses `MemoryClient` to read authorized scopes
- CHP respects `MemoryLifecycleManager` states
- CHP integrates with `PrivacyChecker` (defense-in-depth)

### With Existing Proposals

- CHP proposals compatible with existing proposal structure
- CHP proposals stored alongside other proposals
- CHP proposals use same approval workflow

### With Foreman

- CHP proposals routed to Foreman dashboard
- Foreman reviews and approves/rejects
- Foreman can query CHP audit trail

### With Watchdog

- Watchdog monitors CHP access patterns
- Watchdog alerts on unauthorized attempts
- Watchdog verifies proposal approval tokens

## Security Guarantees

1. **No Tenant Data Access:** CHP cannot read `runtime` or `platform` scopes
2. **No Direct Writes:** CHP must use proposal workflow
3. **Audit Trail:** All CHP reads logged immutably
4. **Authorization Enforcement:** Multi-layer authorization checks
5. **Privacy Protection:** Privacy checker filters CHP reads
6. **No Auto-Promotion:** Proposals require explicit approval

## Future Enhancements

- **Adaptive Learning:** CHP learns from approval/rejection patterns
- **Proactive Hygiene:** CHP predicts drift before it occurs
- **Cross-Tenant Patterns:** CHP analyzes anonymized patterns (if authorized)
- **Auto-Apply Policy:** Implement pre-authorization policy for low-risk actions

## Related Documentation

- **Architecture Spec:** `docs/architecture/runtime/cognitive-hygiene/CHP_MEMORY_INTEGRATION_ARCHITECTURE.md`
- **Memory Lifecycle:** `docs/architecture/runtime/memory/MEMORY_LIFECYCLE_STATE_MACHINE.md`
- **Memory Proposals:** `MEMORY_WRITE_PROPOSALS_README.md`
- **Privacy Guardrails:** `governance/policies/privacy-guardrails.md`

## Support

For questions or issues:
- Review architecture spec
- Check test suite for examples
- Escalate to Johan for governance questions
