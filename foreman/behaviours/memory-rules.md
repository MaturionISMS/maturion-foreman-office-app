# Maturion Foreman – Memory Behavior Rules

## Purpose

This document defines **when**, **what**, and **how** Maturion Foreman and all builder agents interact with the Unified Memory Fabric. Memory is a first-class requirement for all cognitive actions.

---

## Core Principle

**Memory Before Action**: All agents MUST load relevant memory context before reasoning, planning, or executing ANY action.

**Absence of Memory = Governance Violation**: No builds, no reasoning, no decisions without memory.

---

## 1. When to Read Memory

### Mandatory Memory Load Points

Memory MUST be loaded at the following points:

#### 1.1 Foreman (Build-Time)

- **Before processing any chat/command input**
  - Load: `global`, `foreman` scopes
  - Tags: `governance`, `architecture`, `philosophy`
  - Minimum importance: `high`

- **Before build wave planning**
  - Load: `global`, `foreman` scopes
  - Tags: `build`, `governance`, `architecture`
  - Minimum importance: `medium`

- **Before build task dispatch**
  - Load: `global`, `foreman` scopes
  - Tags: `builder`, `governance`, `sequence`
  - Minimum importance: `medium`

- **Before QA validation**
  - Load: `global`, `foreman` scopes
  - Tags: `qa`, `governance`, `testing`
  - Minimum importance: `medium`

- **Before compliance checking**
  - Load: `global`, `foreman`, `platform` scopes
  - Tags: `compliance`, `governance`, `security`
  - Minimum importance: `high`

- **Before repository initialization**
  - Load: `global`, `foreman` scopes
  - Tags: `initialization`, `architecture`, `governance`
  - Minimum importance: `critical`

#### 1.2 Builder Agents (Local & Remote)

- **Before accepting any task**
  - Load: `global`, scope matching task domain
  - Tags: task-specific (e.g., `ui`, `api`, `schema`)
  - Minimum importance: `medium`

- **Before generating code**
  - Load: `global`, relevant module scope
  - Tags: `architecture`, `patterns`, module-specific
  - Minimum importance: `medium`

- **Before writing tests**
  - Load: `global`, `foreman` scopes
  - Tags: `qa`, `testing`, `coverage`
  - Minimum importance: `medium`

#### 1.3 Runtime Agent

- **Before processing monitoring events**
  - Load: `global`, `runtime`, `platform` scopes
  - Tags: `monitoring`, `incidents`, `health`
  - Minimum importance: `medium`

- **Before auto-fix decisions**
  - Load: `global`, `runtime`, `platform` scopes
  - Tags: `auto-fix`, `incidents`, `governance`
  - Minimum importance: `high`

- **Before escalations**
  - Load: `global`, `runtime`, `platform` scopes
  - Tags: `incidents`, `escalation`, `governance`
  - Minimum importance: `high`

---

## 2. When to Write Memory

### Mandatory Memory Write Points

Memory entries MUST be written for the following events:

#### 2.1 Governance Events

- **Architecture decisions**
  - Scope: `foreman`
  - Importance: `high` or `critical`
  - Tags: `architecture`, `decision`, `governance`

- **Governance actions** (approvals, rejections, validations)
  - Scope: `foreman`
  - Importance: `medium` or `high`
  - Tags: `governance`, `validation`, `qa`

- **Policy changes**
  - Scope: `global` or `foreman`
  - Importance: `high` or `critical`
  - Tags: `governance`, `policy`, `change`

#### 2.2 Build Events

- **Build wave completion**
  - Scope: `foreman`
  - Importance: `medium`
  - Tags: `build`, `wave`, `completion`

- **Build failures** (if pattern detected)
  - Scope: `foreman`
  - Importance: `medium` or `high`
  - Tags: `build`, `failure`, `incident`

- **Task distribution decisions**
  - Scope: `foreman`
  - Importance: `low` or `medium`
  - Tags: `build`, `task`, `sequence`

#### 2.3 QA Events

- **QA validation outcomes** (especially failures)
  - Scope: `foreman`
  - Importance: `medium`
  - Tags: `qa`, `validation`, `testing`

- **Coverage gaps discovered**
  - Scope: `foreman`
  - Importance: `medium` or `high`
  - Tags: `qa`, `coverage`, `gap`

#### 2.4 Compliance Events

- **Compliance incidents**
  - Scope: `platform` or `runtime`
  - Importance: `high` or `critical`
  - Tags: `compliance`, `incident`, `security`

- **Control mapping updates**
  - Scope: `platform`
  - Importance: `medium`
  - Tags: `compliance`, `mapping`, `control`

#### 2.5 Runtime Events

- **Platform incidents**
  - Scope: `runtime`
  - Importance: `high` or `critical`
  - Tags: `runtime`, `incident`, `platform`

- **Auto-fix actions**
  - Scope: `runtime`
  - Importance: `medium`
  - Tags: `runtime`, `auto-fix`, `incident`

- **Anomalies detected**
  - Scope: `runtime`
  - Importance: `medium` or `high`
  - Tags: `runtime`, `anomaly`, `monitoring`

---

## 3. Memory Lifecycle

### 3.1 Creation

1. Event occurs (governance action, build completion, incident, etc.)
2. Agent creates memory entry with required fields
3. Entry is written to appropriate scope directory
4. Entry is appended to date-based collection file
5. Entry is version-controlled in Git

### 3.2 Loading

1. Agent determines required scopes, tags, and importance
2. Agent calls `loadMemory()` or equivalent
3. Memory client filters and sorts entries
4. Agent formats memories into prompt context
5. Agent proceeds with reasoning/action

### 3.3 Retention

- **All memory entries are permanent** (version-controlled in Git)
- No automatic deletion or expiration
- Entries may be superseded by newer entries but are never removed
- Critical memories survive chat resets, model upgrades, repo transfers

---

## 4. Memory Safety Rules

### 4.1 Privacy Protection

**FORBIDDEN in memory entries:**

- ❌ Tenant-specific data (organisation names, user names, emails)
- ❌ User identifiable information (PII)
- ❌ Customer secrets or credentials
- ❌ Raw tenant data or logs
- ❌ Cross-tenant references

**ALLOWED in memory entries:**

- ✅ Aggregate patterns (anonymized)
- ✅ Architecture decisions
- ✅ Governance rules
- ✅ Build outcomes
- ✅ QA results
- ✅ Compliance mappings (generic)

---

## 5. Enforcement Rules

### 5.1 Pre-Action Memory Check

**All agents MUST:**

1. Load relevant memories before ANY action
2. Format memories into system prompt or context
3. Validate memory fabric health on initialization
4. Reject tasks if memory cannot be loaded

### 5.2 Post-Action Memory Write

**All agents MUST:**

1. Identify significant events during task execution
2. Write memory entries for qualifying events
3. Validate memory write succeeded
4. Log memory write failures

### 5.3 Repository Initialization Memory Check

**Foreman MUST:**

1. Check for `memory/` directory on repo access
2. Validate memory structure if exists
3. Auto-initialize memory if missing
4. Block all builds until memory readiness = PASS

---

## 6. Auto-Initialization Rules

### 6.1 When Foreman Creates a New Repo

**Automatic Actions:**

1. Create `memory/` directory structure:
   ```
   memory/
     schema/
       memory-entry.json
     global/
       seed-build-philosophy-memory.json
       seed-architecture-memory.json
       seed-governance-memory.json
     foreman/
       (empty, ready for events)
     platform/
       (empty, ready for events)
     runtime/
       (empty, ready for events)
   ```

2. Copy memory schema from Foreman repo
3. Copy seed memories from Foreman repo
4. Validate memory structure
5. Write initialization memory entry

### 6.2 When Repo Has No Memory

**Foreman Behavior:**

1. Detect missing `memory/` directory
2. Generate **Memory Initialization Wave** issue
3. Block ALL builds until memory is initialized
4. Report to Johan: "Memory fabric missing, builds blocked"

---

## 7. Integration Points

### 7.1 Chat Pipeline Integration

**Before Reasoning:**

```typescript
// Load memory context
const memories = await loadMemory(['global', 'foreman'], ['governance', 'architecture'], 'high');
const memoryContext = formatMemoriesForPrompt(memories);

// Inject into system prompt
const systemPrompt = `${baseSystemPrompt}\n\n${memoryContext}`;
```

**After Critical Actions:**

```typescript
// Write memory entry
await appendMemory({
  scope: 'foreman',
  title: 'Module Boundary Decision',
  summary: 'Approved new Asset module boundary definition',
  importance: 'high',
  tags: ['architecture', 'decision', 'module']
});
```

### 7.2 Local Builder Integration

**Agent Initialization:**

```python
# Load memories before task acceptance
from memory_client import load_memory, format_memories_for_prompt

memories = load_memory(
    scopes=['global', task_scope],
    tags=[task_type, 'patterns', 'architecture'],
    importance_min='medium'
)

# Inject into system prompt
memory_context = format_memories_for_prompt(memories, max_memories=10)
system_prompt = f"{base_system_prompt}\n\n{memory_context}"
```

**Task Completion:**

```python
# Write memory if significant
if task_outcome.is_significant():
    write_memory({
        'scope': task_scope,
        'title': f'{task_type} Task Completed',
        'summary': task_outcome.summary,
        'importance': 'low',
        'tags': [task_type, 'task', 'completion']
    })
```

---

## 8. Self-Test Requirements

### Memory-Specific Self-Tests

**Required Tests:**

1. ✅ **Memory Load Test** - Validates loadMemory() returns entries
2. ✅ **Memory Write Test** - Validates appendMemory() creates entry
3. ✅ **Memory Fabric Health Score** - Validates memoryHealthCheck() returns status
4. ✅ **Memory Schema Compliance** - Validates all entries match schema

---

## Summary

**Memory is NOT optional. It is a first-class requirement.**

- ✅ Load memory before every action
- ✅ Write memory for every significant event
- ✅ Validate memory fabric health on initialization
- ✅ Block builds if memory is missing
- ✅ Auto-initialize memory for new repos
- ✅ Respect privacy and security in memory content

**Violation of memory rules is a governance failure.**
