# Global Memory Runtime (Read-Only) — Implementation Guide

## Purpose

This document describes the **read-only runtime capability** for the FM App to load and use Global Experience Memory as defined by governance.

This is **Phase 1** of memory integration: **Read-only access only**.

---

## Governance Authority

This implementation strictly complies with governance definitions in:

- `/memory/schema/memory-entry.json` — Memory entry structure
- `/foreman/behaviours/memory-rules.md` — When and how to use memory
- `/memory/global/*.json` — Global seed memory files
- `/MEMORY_WAVE_2_README.md` — Memory fabric overview

**Governance is the source of truth. Runtime must conform.**

---

## What Is Global Memory?

Global memory contains:

- **Build philosophy** — One-Time Build Correctness, Zero Regression
- **Governance rules** — Mandatory architecture, QA, compliance requirements
- **Architecture patterns** — Module boundaries, integration contracts
- **Autonomy rules** — Builder permissions, escalation policies
- **Runtime agent behavior** — Monitoring, incident response patterns

Global memory is **immutable at runtime** and serves as permanent institutional knowledge.

---

## Scope (Strict)

### IN SCOPE ✅

- Load global memory structures at runtime
- Validate memory against governance schemas
- Allow **read access only** for:
  - Process guidance
  - Escalation heuristics
  - Pattern recognition
- Fail fast if governance memory is invalid or missing
- Document read-only enforcement explicitly

### OUT OF SCOPE ❌

- ❌ Writing memory
- ❌ Modifying memory
- ❌ Learning automation
- ❌ Tenant memory
- ❌ Cross-project memory
- ❌ CI/CD changes (beyond testing)

---

## Architecture

### Components

```
lib/memory/
├── client.ts              # Base memory client (read + write)
└── runtime-loader.ts      # Runtime loader (read-only) ← NEW
```

### Class: `GlobalMemoryRuntimeLoader`

**Purpose:** Provides read-only access to global memory at runtime.

**Key Methods:**

```typescript
// Initialize and validate memory fabric
await loader.initialize();

// Check initialization status
loader.isInitialized();
loader.getInitializationError();

// Load global memory with filters
await loader.loadGlobalMemory(tags?, importanceMin?);

// Specialized loaders
await loader.loadProcessGuidance();
await loader.loadEscalationHeuristics();
await loader.loadPatternMemories();

// Format for AI prompt
loader.formatForPrompt(memories, maxMemories);

// Health check
await loader.healthCheck();
```

**Read-Only Enforcement:**

- No `appendMemory()` method
- No `writeMemory()` method
- No `modifyMemory()` method
- No `deleteMemory()` method
- Returns `Readonly<MemoryEntry>[]` types
- Explicitly documented as read-only

---

## Runtime Behavior

### Initialization

When `initialize()` is called:

1. **Verify memory root exists** (`/memory`)
2. **Load and validate schema** (`/memory/schema/memory-entry.json`)
3. **Check global memory present** (`/memory/global/*.json`)
4. **Fail fast if any check fails** (when `failOnInvalid: true`)

If initialization fails:

- `isInitialized()` returns `false`
- `getInitializationError()` returns error message
- Memory loading operations throw error (soft stop)
- Escalation required (governance failure)

### Loading Memory

Memory loading follows governance rules from `/foreman/behaviours/memory-rules.md`:

**Before any governance action:**

```typescript
const loader = await createGlobalMemoryRuntime();
const memories = await loader.loadProcessGuidance();
const context = loader.formatForPrompt(memories);
// Inject into system prompt
```

**Filtering:**

- **By scope:** Always `['global']` for this phase
- **By tags:** `['governance', 'architecture', 'philosophy']`
- **By importance:** `'high'` or `'critical'` for critical decisions

**Validation:**

- All memories validated against schema
- Missing required fields → error
- Invalid importance value → error
- Non-array tags → error
- Fail fast if validation fails (when `validateOnLoad: true`)

### Fail-Fast Behavior

The runtime loader is **strict by default**:

```typescript
// Default: Fail on invalid memory
const loader = await createGlobalMemoryRuntime();

// Lenient mode (for development/testing only)
const loader = await createGlobalMemoryRuntime({
  failOnInvalid: false,
  validateOnLoad: false
});
```

When fail-fast is enabled (default):

- Missing memory root → throw error
- Missing schema → throw error
- No global memories → throw error
- Invalid memory structure → throw error
- Schema validation failure → throw error

**This enforces governance: Memory is mandatory.**

---

## Usage Patterns

### Pattern 1: Governance Decision

```typescript
import { createGlobalMemoryRuntime } from '@/lib/memory/runtime-loader';

// Before processing governance decision
const loader = await createGlobalMemoryRuntime();

const memories = await loader.loadGlobalMemory(
  ['governance', 'architecture'],
  'high'
);

const context = loader.formatForPrompt(memories, 10);

// Use context in system prompt
const systemPrompt = `${basePrompt}\n\n${context}`;
```

### Pattern 2: Build Planning

```typescript
const loader = await createGlobalMemoryRuntime();

const memories = await loader.loadGlobalMemory(
  ['build', 'sequence', 'governance'],
  'medium'
);

// Extract patterns from memories
for (const memory of memories) {
  if (memory.tags.includes('sequence')) {
    applySequencingPattern(memory);
  }
}
```

### Pattern 3: QA Validation

```typescript
const loader = await createGlobalMemoryRuntime();

const memories = await loader.loadGlobalMemory(
  ['qa', 'testing', 'coverage'],
  'medium'
);

// Use memories to validate coverage requirements
const requirements = extractQARequirements(memories);
validateCoverage(coverageReport, requirements);
```

### Pattern 4: Health Check (Startup)

```typescript
// On application startup
const loader = await createGlobalMemoryRuntime();

const health = await loader.healthCheck();

if (health.status !== 'healthy') {
  console.error('Memory fabric unhealthy:', health.issues);
  // Escalate to Johan
}
```

---

## Testing

### Test Suite: `tests/test_global_memory_runtime.py`

**Coverage:**

- ✅ Memory loading functionality
- ✅ Filtering by importance and tags
- ✅ Schema validation
- ✅ Fail-fast behavior
- ✅ Read-only enforcement (no write methods)
- ✅ Memory immutability at runtime
- ✅ Health check integration

**Run Tests:**

```bash
# Run memory tests only
pytest tests/test_global_memory_runtime.py -v

# Run with markers
pytest -m memory -v
```

**Expected Results:**

All tests should pass, validating:

1. Global memory can be loaded
2. Memories match schema requirements
3. Filtering works correctly
4. Fail-fast triggers on invalid memory
5. No write operations exist in runtime loader
6. Loaded memories are immutable

---

## Failure Scenarios

### Scenario 1: Memory Root Missing

**Symptom:**

```
GOVERNANCE FAILURE: Memory root directory does not exist: /memory
```

**Resolution:**

1. Run `python3 init-memory-fabric.py` to initialize memory
2. Verify `/memory` directory exists
3. Restart application

### Scenario 2: Schema Missing

**Symptom:**

```
GOVERNANCE FAILURE: Failed to load memory schema
```

**Resolution:**

1. Verify `/memory/schema/memory-entry.json` exists
2. Validate JSON syntax
3. Restore from governance repository if corrupted

### Scenario 3: No Global Memories

**Symptom:**

```
GOVERNANCE FAILURE: No global memory files found
```

**Resolution:**

1. Verify `/memory/global/*.json` files exist
2. Check seed files present:
   - `seed-governance-memory.json`
   - `seed-build-philosophy-memory.json`
   - `seed-architecture-memory.json`
3. Re-run `init-memory-fabric.py` if missing

### Scenario 4: Invalid Memory Structure

**Symptom:**

```
Memory validation failed: Memory mem-xxx missing required field: importance
```

**Resolution:**

1. Open the problematic memory file
2. Add missing required fields:
   - `id`, `scope`, `title`, `summary`, `importance`, `tags`
3. Validate against schema
4. Restart application

---

## Read-Only Enforcement

### Why Read-Only?

Phase 1 focuses on:

- **Safety:** No risk of corrupting governance memory
- **Validation:** Prove memory loading works correctly
- **Alignment:** Ensure governance compliance
- **Foundation:** Build confidence before write operations

### What's Prohibited?

The runtime loader **explicitly does NOT provide**:

- ❌ `appendMemory()` — No writing
- ❌ `writeMemory()` — No writing
- ❌ `modifyMemory()` — No modification
- ❌ `deleteMemory()` — No deletion
- ❌ Learning loops — No automation
- ❌ Tenant memory — Out of scope
- ❌ Cross-project memory — Out of scope

### Code Enforcement

```typescript
// TypeScript type system enforces read-only
export type ReadOnlyMemoryEntry = Readonly<MemoryEntry>;
export type ReadOnlyMemoryArray = ReadonlyArray<ReadOnlyMemoryEntry>;

// Methods return Readonly types
async loadGlobalMemory(): Promise<Readonly<MemoryEntry>[]>
```

### Test Enforcement

Test suite validates:

```python
def test_no_append_memory_in_runtime_loader():
    """Runtime loader must NOT contain write operations"""
    prohibited_patterns = [
        'appendMemory(',
        'writeMemory(',
        'modifyMemory(',
        'deleteMemory(',
    ]
    
    for pattern in prohibited_patterns:
        assert pattern not in runtime_loader_code
```

---

## Next Steps (Out of Scope for This PR)

Future phases (not in this PR):

1. **Phase 2:** Memory write capability (controlled)
2. **Phase 3:** Tenant-specific memory (isolated)
3. **Phase 4:** Learning automation (safe patterns)
4. **Phase 5:** Cross-project memory (governance-controlled)

**This PR stops after Phase 1: Read-only access.**

---

## Integration Checklist

When integrating memory runtime into FM App:

- [ ] Import `createGlobalMemoryRuntime` from `lib/memory/runtime-loader`
- [ ] Call `initialize()` on application startup
- [ ] Check `isInitialized()` before using memory
- [ ] Load memories before governance decisions
- [ ] Format memories for AI prompt injection
- [ ] Handle initialization failures with escalation
- [ ] Monitor memory health with `healthCheck()`
- [ ] Document usage in application code
- [ ] Add integration tests
- [ ] Verify no write operations used

---

## References

- **Memory Schema:** `/memory/schema/memory-entry.json`
- **Memory Rules:** `/foreman/behaviours/memory-rules.md`
- **Memory Overview:** `/MEMORY_WAVE_2_README.md`
- **Client Implementation:** `/lib/memory/client.ts`
- **Runtime Loader:** `/lib/memory/runtime-loader.ts`
- **Test Suite:** `/tests/test_global_memory_runtime.py`

---

## Compliance Statement

This implementation:

✅ Complies with `/memory/schema/memory-entry.json`  
✅ Follows `/foreman/behaviours/memory-rules.md`  
✅ Uses governance-defined memory structure  
✅ Enforces read-only access  
✅ Validates memory against schema  
✅ Fails fast on invalid memory  
✅ Documents all behavior explicitly  
✅ Provides comprehensive test coverage  

**No governance rules were bypassed or weakened.**

---

**End of Global Memory Runtime (Read-Only) Implementation Guide**
