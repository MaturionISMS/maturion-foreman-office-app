# Memory Wave 2 — Implementation Guide

## Overview

This directory contains the **Memory Wave 2** implementation for the Maturion Foreman ecosystem. Memory is now a first-class requirement for all cognitive actions across Foreman, Local Builders, and Runtime Agents.

---

## Components Delivered

### 1. Python Memory Client (`python_agent/memory_client.py`)

**Purpose:** Provides memory fabric integration for Python-based agents and scripts.

**Key Functions:**

- `load_memory(scopes, tags, importance_min)` - Load memory entries matching criteria
- `write_memory(entry, scope)` - Write new memory entry to fabric
- `memory_health_check()` - Check memory fabric health status
- `format_memories_for_prompt(memories)` - Format memories for AI prompt injection

**Usage:**

```python
from memory_client import load_memory, write_memory, memory_health_check

# Load memories before reasoning
memories = load_memory(
    scopes=['global', 'foreman'],
    tags=['governance', 'architecture'],
    importance_min='high'
)

# Format for prompt
memory_context = format_memories_for_prompt(memories, max_memories=15)

# Write memory after significant event
entry_id = write_memory({
    'scope': 'foreman',
    'title': 'Build Wave Completed',
    'summary': 'Successfully completed build wave 1.2',
    'importance': 'high',
    'tags': ['build', 'governance']
})

# Check health
health = memory_health_check()
print(f"Memory Status: {health['status']}, Total Entries: {health['total_entries']}")
```

**CLI Usage:**

```bash
# Check memory health
python3 python_agent/memory_client.py health

# Load and display critical memories
python3 python_agent/memory_client.py load

# Test write capability
python3 python_agent/memory_client.py test
```

---

### 2. TypeScript Memory Client (`lib/memory/client.ts`)

**Purpose:** Provides memory fabric integration for TypeScript/JavaScript applications (e.g., Vercel-hosted Foreman app).

**Key Functions:**

- `loadMemory(scopes, tags, importanceMin)` - Load memory entries
- `appendMemory(entry, scopeOverride)` - Write new memory entry
- `memoryHealthCheck()` - Check memory fabric health
- `formatMemoriesForPrompt(memories)` - Format memories for prompts

**Usage:**

```typescript
import { loadMemory, appendMemory, memoryHealthCheck } from '@/lib/memory/client';

// Load memories before reasoning
const memories = await loadMemory(['global', 'foreman'], ['architecture'], 'high');

// Format for prompt
const memoryContext = formatMemoriesForPrompt(memories, 15);

// Write memory after action
await appendMemory({
  scope: 'foreman',
  title: 'Architecture Decision',
  summary: 'Approved new module boundary',
  importance: 'high',
  tags: ['architecture', 'decision']
});

// Check health
const health = await memoryHealthCheck();
console.log(`Status: ${health.status}, Entries: ${health.total_entries}`);
```

**Dependencies:**

The TypeScript client requires:
- `uuid` package (for generating entry IDs)

Install with: `npm install uuid` or `yarn add uuid`

---

### 3. Python Agent Core Template (`python_agent/agent_core.py`)

**Purpose:** Reference implementation showing how to integrate memory into Python builder agents.

**Key Features:**

- Memory loading before task acceptance
- System prompt enrichment with memory context
- Task rejection if memory unavailable
- Automatic completion memory writing

**Usage:**

```python
from agent_core import AgentCore

# Create agent
agent = AgentCore(
    agent_name="schema-builder",
    task_scope="isms"
)

# Execute task (automatically loads memory and enriches prompt)
task = {
    'type': 'schema',
    'title': 'Create Asset schema',
    'importance': 'high'
}

result = agent.execute_task(task)
```

---

### 4. Memory Behavior Rules (`foreman/behaviours/memory-rules.md`)

**Purpose:** Defines when, what, and how all agents interact with memory.

**Key Rules:**

1. **Memory Before Action** - Load memory before ANY reasoning or action
2. **Mandatory Load Points** - Specific points where memory MUST be loaded
3. **Mandatory Write Points** - Events that require memory entry creation
4. **Memory Safety** - No PII, secrets, or tenant-specific data in memory
5. **Auto-Initialization** - New repos automatically get memory fabric

**Read this document to understand:**

- When to read memory
- When to write memory
- What counts as important memory
- Memory lifecycle and safety rules
- Enforcement mechanisms

---

### 5. Repository Initialization Script (`init-memory-fabric.py`)

**Purpose:** Initializes Unified Memory Fabric for new repositories.

**What it does:**

1. Creates `memory/` directory structure
2. Copies memory schema from Foreman repo
3. Copies seed memories (build philosophy, governance, etc.)
4. Creates initialization memory entry
5. Validates structure

**Usage:**

```bash
# Initialize memory in current directory
python3 init-memory-fabric.py

# Initialize memory in specific repo
python3 init-memory-fabric.py /path/to/repo

# Force re-initialization (preserves existing entries)
python3 init-memory-fabric.py --force
```

**Created Structure:**

```
memory/
  schema/
    memory-entry.json
  global/
    seed-build-philosophy-memory.json
    seed-architecture-memory.json
    seed-governance-memory.json
    seed-autonomy-memory.json
    seed-runtime-agent-memory.json
  foreman/
    (events written here)
  platform/
    (platform events here)
  runtime/
    (runtime events here)
```

---

### 6. Enhanced Self-Test (`foreman/scripts/run-self-test.py`)

**Updates:** Memory fabric test now includes:

1. ✅ **Memory Load Test** - Validates loadMemory() returns entries
2. ✅ **Memory Write Test** - Validates appendMemory() creates entries
3. ✅ **Memory Health Check** - Validates memoryHealthCheck() status
4. ✅ **Schema Compliance** - Validates entries match schema

**Run Self-Test:**

```bash
cd /home/runner/work/maturion-ai-foreman/maturion-ai-foreman
python3 foreman/scripts/run-self-test.py --verbose
```

**Memory Section Output:**

```
✅ Unified Memory Fabric
   Status: PASS
   Health Status: HEALTHY
   Total Entries: 28
   Critical Memories Loaded: 20
   Write Test: PASS
```

---

## Integration Patterns

### For Foreman (Build-Time)

**Chat Pipeline:**

```typescript
// Before processing chat input
const memories = await loadMemory(['global', 'foreman'], ['governance'], 'high');
const context = formatMemoriesForPrompt(memories);
const systemPrompt = `${basePrompt}\n\n${context}`;

// After critical action
await appendMemory({
  scope: 'foreman',
  title: 'Governance Action',
  summary: 'Rejected PR due to missing QA',
  importance: 'medium',
  tags: ['governance', 'qa', 'rejection']
});
```

**Build Wave Planning:**

```python
# Load build-related memories
memories = load_memory(
    scopes=['global', 'foreman'],
    tags=['build', 'sequence'],
    importance_min='medium'
)

# Use in planning logic
for memory in memories:
    if 'sequence' in memory['tags']:
        apply_learned_pattern(memory)
```

### For Local Builders (Python)

**Before Task Execution:**

```python
from memory_client import load_memory, format_memories_for_prompt

# Load relevant memories
memories = load_memory(
    scopes=['global', 'isms'],
    tags=['schema', 'architecture'],
    importance_min='medium'
)

# Enrich system prompt
memory_context = format_memories_for_prompt(memories)
system_prompt = f"{base_prompt}\n\n{memory_context}"
```

**After Task Completion:**

```python
from memory_client import write_memory

# Write completion memory
write_memory({
    'scope': 'isms',
    'title': 'Schema Migration Completed',
    'summary': 'Added new Asset table with proper foreign keys',
    'importance': 'low',
    'tags': ['schema', 'migration', 'asset']
})
```

### For Runtime Agent

**Before Monitoring Action:**

```typescript
const memories = await loadMemory(
  ['global', 'runtime', 'platform'],
  ['monitoring', 'incidents'],
  'medium'
);
```

**After Incident:**

```typescript
await appendMemory({
  scope: 'runtime',
  title: 'Database Connection Pool Exhausted',
  summary: 'Auto-scaled pool to handle spike',
  importance: 'high',
  tags: ['runtime', 'incident', 'auto-fix']
});
```

---

## Enforcement Rules

### Pre-Action Memory Check

**All agents MUST:**

1. Load relevant memories before ANY action
2. Format memories into system prompt
3. Validate memory fabric health on initialization
4. Reject tasks if memory cannot be loaded

### Post-Action Memory Write

**All agents MUST:**

1. Identify significant events during execution
2. Write memory entries for qualifying events
3. Validate write succeeded
4. Log write failures

### Repository Initialization Check

**Foreman MUST:**

1. Check for `memory/` directory on repo access
2. Validate structure if exists
3. Auto-initialize if missing
4. Block builds until memory readiness = PASS

---

## Testing

### Memory Client Tests

```bash
# Python memory client
cd /home/runner/work/maturion-ai-foreman/maturion-ai-foreman
python3 python_agent/memory_client.py health
python3 python_agent/memory_client.py load
python3 python_agent/memory_client.py test
```

### Agent Core Demo

```bash
python3 python_agent/agent_core.py
```

### Self-Test

```bash
python3 foreman/scripts/run-self-test.py --verbose
```

---

## Migration Guide

### For Existing Repositories

If a repository doesn't have memory fabric:

1. **Run Initialization:**
   ```bash
   python3 init-memory-fabric.py /path/to/repo
   ```

2. **Verify Structure:**
   ```bash
   cd /path/to/repo
   python3 python_agent/memory_client.py health
   ```

3. **Update Agents:**
   - Import memory client
   - Load memory before actions
   - Write memory after significant events

### For New Repositories

Foreman will automatically:

1. Create `memory/` structure on repo creation
2. Copy schema and seed files
3. Validate readiness
4. Block builds if memory missing

---

## Troubleshooting

### "Memory client not available"

**Solution:** Ensure `python_agent/memory_client.py` exists and is in Python path.

```bash
# Add to path
export PYTHONPATH="${PYTHONPATH}:/path/to/repo/python_agent"
```

### "Memory root directory does not exist"

**Solution:** Initialize memory fabric.

```bash
python3 init-memory-fabric.py
```

### "No memories loaded"

**Solution:** Check seed files exist and are valid JSON.

```bash
ls -la memory/global/
python3 -m json.tool memory/global/seed-build-philosophy-memory.json
```

### "Memory write failed"

**Solution:** Check directory permissions and disk space.

```bash
ls -la memory/foreman/
df -h
```

---

## Next Steps

1. **Integrate into Vercel App** (if applicable)
   - Install TypeScript client in Next.js app
   - Add memory loading to API routes
   - Add memory writing to critical actions

2. **Update Builder Specifications**
   - Add memory requirements to each builder spec
   - Define memory load/write points
   - Update task templates

3. **Create Memory Dashboards**
   - Memory health dashboard
   - Memory usage analytics
   - Memory growth tracking

4. **Enhanced Validation**
   - Schema validation on write
   - Duplicate detection
   - Memory compression/archival

---

## References

- **Memory Schema:** `memory/schema/memory-entry.json`
- **Memory Behavior Rules:** `foreman/behaviours/memory-rules.md`
- **Memory Model:** `foreman/memory-model.md`
- **Privacy Guardrails:** `foreman/privacy-guardrails.md`
- **Self-Test Spec:** `foreman/self-test/self-test-spec.md`

---

**End of Memory Wave 2 Implementation Guide**
