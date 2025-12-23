# Governance Memory Sync & Invalidation Contract

## PURPOSE

This contract ensures the FM App remains aligned with governance-defined memory by implementing a **synchronization and invalidation system** that prevents drift and silent divergence.

---

## GOVERNANCE AUTHORITY

This contract implements requirements from:

- `/foreman/behaviours/memory-rules.md` — Memory usage rules
- `/memory/schema/memory-entry.json` — Memory structure
- `/memory/schema/governance-version.json` — Version tracking schema
- Issue #2 — Governance Memory Sync & Invalidation Contract

---

## SCOPE

### IN SCOPE ✅

1. **Governance Memory Version Tracking**
   - Define version format (semver)
   - Track version in `.governance-version.json`
   - Include checksums for integrity validation
   - Track schema version compatibility

2. **Change Detection**
   - Detect governance memory version changes
   - Compare checksums to identify modifications
   - Identify stale memory conditions
   - Track last loaded version

3. **Safe Reload Mechanism**
   - Atomic memory reload on governance change
   - Prevent partial loads
   - Ensure transactional memory updates
   - Log all reload events

4. **Cache Invalidation**
   - Explicit cache invalidation on governance updates
   - Auditable invalidation events
   - Version mismatch handling
   - Stale cache detection

5. **Memory State Exposure**
   - Define state types: LOADED, STALE, INVALID, UNINITIALIZED
   - Track current memory state
   - Provide state getters for FM App UI
   - Enable runtime state monitoring

### OUT OF SCOPE ❌

- ❌ Writing governance memory (read-only only)
- ❌ Auto-learning or memory mutation
- ❌ Tenant-specific memory
- ❌ CI/CD enforcement automation
- ❌ Governance repository changes
- ❌ Automatic version bumping
- ❌ Memory content modification

---

## RUNTIME RULES

### Rule 1: Version Validation Before Load

**REQUIREMENT:** FM App MUST validate governance memory version before loading any memory.

**IMPLEMENTATION:**
- Load `.governance-version.json` first
- Compare with last loaded version (cached)
- If mismatch detected → trigger invalidation
- If checksum differs → trigger reload

**SOFT STOP:** If version mismatch detected, FM App enters STALE state and logs warning.

### Rule 2: Atomic Memory Reload

**REQUIREMENT:** Memory reload MUST be atomic — all or nothing.

**IMPLEMENTATION:**
- Load all governance memory files into temporary buffer
- Validate all entries against schema
- If any validation fails → abort reload, keep old memory
- If all succeed → atomically swap to new memory
- Log reload completion with version

**PROHIBITION:** Partial loads are forbidden. If reload fails, existing memory remains.

### Rule 3: Explicit Invalidation

**REQUIREMENT:** All cache invalidation events MUST be explicit and auditable.

**IMPLEMENTATION:**
- Log every invalidation event with:
  - Timestamp
  - Old version
  - New version
  - Reason (version mismatch / checksum mismatch / manual)
- Store invalidation log in `/fm/memory/invalidation-log.json`
- Expose invalidation count via health check

### Rule 4: State Transitions

**REQUIREMENT:** Memory state transitions MUST follow defined state machine.

**STATE MACHINE:**

```
UNINITIALIZED
    ↓ (initialize())
LOADING
    ↓ (success)
LOADED ←→ STALE (version mismatch detected)
    ↓ (validation fail)
INVALID
```

**TRANSITIONS:**
- `UNINITIALIZED → LOADING`: On first initialize()
- `LOADING → LOADED`: On successful memory load
- `LOADED → STALE`: On version mismatch detection
- `STALE → LOADING`: On reload trigger
- `LOADING → INVALID`: On validation failure
- `INVALID → LOADING`: On retry after fix

---

## VERSION SCHEMA

### File: `memory/.governance-version.json`

```json
{
  "version": "1.0.0",
  "timestamp": "2024-12-23T16:00:00Z",
  "commit_sha": "abc123...",
  "checksum": "sha256_of_all_files",
  "schema_version": "1.0.0",
  "files": [
    {
      "path": "memory/global/seed-governance-memory.json",
      "checksum": "sha256_of_file"
    }
  ]
}
```

### Version Format

- **Format:** Semantic Versioning (MAJOR.MINOR.PATCH)
- **MAJOR:** Breaking changes to memory structure
- **MINOR:** New governance memories added
- **PATCH:** Corrections to existing memories

### Checksum Calculation

- **Algorithm:** SHA-256
- **Input:** Concatenated content of all governance memory files (sorted by path)
- **Purpose:** Detect any modification to governance memory

---

## MEMORY STATES

### State Definitions

#### `UNINITIALIZED`
- **Description:** Memory runtime not yet initialized
- **Actions Allowed:** initialize()
- **Actions Forbidden:** All memory operations

#### `LOADING`
- **Description:** Memory is being loaded or reloaded
- **Actions Allowed:** Wait, health check
- **Actions Forbidden:** Memory access

#### `LOADED`
- **Description:** Memory successfully loaded and current
- **Actions Allowed:** All read operations
- **Actions Forbidden:** Write operations

#### `STALE`
- **Description:** Governance memory version has changed, current memory is outdated
- **Actions Allowed:** Read (with warning), reload
- **Actions Forbidden:** Critical decisions without reload

#### `INVALID`
- **Description:** Memory validation failed, cannot use current memory
- **Actions Allowed:** Health check, retry initialization
- **Actions Forbidden:** All memory operations

---

## API EXTENSIONS

### Enhanced Runtime Loader Interface

```typescript
interface GlobalMemoryRuntimeLoader {
  // Existing methods
  initialize(): Promise<void>;
  isInitialized(): boolean;
  loadGlobalMemory(tags?, importanceMin?): Promise<Readonly<MemoryEntry>[]>;
  
  // NEW: Version and sync methods
  getGovernanceVersion(): Promise<GovernanceVersion>;
  getLoadedVersion(): GovernanceVersion | null;
  isMemoryStale(): Promise<boolean>;
  reloadIfStale(): Promise<boolean>;
  forceReload(): Promise<void>;
  
  // NEW: State methods
  getMemoryState(): MemoryState;
  getLastInvalidation(): InvalidationEvent | null;
  getInvalidationHistory(): InvalidationEvent[];
  
  // NEW: Health check extensions
  healthCheck(): Promise<MemoryHealth & {
    governance_version: string;
    memory_state: MemoryState;
    last_reload: string | null;
    is_stale: boolean;
  }>;
}
```

### Type Definitions

```typescript
type MemoryState = 
  | 'UNINITIALIZED' 
  | 'LOADING' 
  | 'LOADED' 
  | 'STALE' 
  | 'INVALID';

interface GovernanceVersion {
  version: string;
  timestamp: string;
  checksum: string;
  schema_version: string;
  files: Array<{
    path: string;
    checksum: string;
  }>;
}

interface InvalidationEvent {
  timestamp: string;
  old_version: string | null;
  new_version: string;
  reason: 'version_mismatch' | 'checksum_mismatch' | 'manual' | 'initialization';
  triggered_reload: boolean;
}
```

---

## INTEGRATION PATTERNS

### Pattern 1: Startup Initialization

```typescript
// On FM App startup
const loader = await createGlobalMemoryRuntime();

// Check initial state
const state = loader.getMemoryState();
if (state !== 'LOADED') {
  console.error('Memory not loaded:', state);
  // Escalate to admin
}

// Check version
const version = await loader.getGovernanceVersion();
console.log('Governance memory version:', version.version);
```

### Pattern 2: Periodic Sync Check

```typescript
// In background task (every 5 minutes)
async function checkGovernanceSync() {
  const loader = await createGlobalMemoryRuntime();
  
  const isStale = await loader.isMemoryStale();
  
  if (isStale) {
    console.warn('Governance memory is stale, reloading...');
    
    const reloaded = await loader.reloadIfStale();
    
    if (reloaded) {
      console.log('Memory reloaded successfully');
    } else {
      console.error('Memory reload failed');
      // Escalate
    }
  }
}
```

### Pattern 3: UI State Display

```typescript
// In FM App UI component
async function displayMemoryStatus() {
  const loader = await createGlobalMemoryRuntime();
  
  const state = loader.getMemoryState();
  const version = loader.getLoadedVersion();
  
  return {
    state,        // LOADED / STALE / INVALID
    version: version?.version || 'unknown',
    timestamp: version?.timestamp || null,
  };
}
```

### Pattern 4: Pre-Governance Action Check

```typescript
// Before any governance decision
async function beforeGovernanceAction() {
  const loader = await createGlobalMemoryRuntime();
  
  // Ensure memory is not stale
  if (loader.getMemoryState() === 'STALE') {
    throw new Error('Cannot proceed: Governance memory is stale');
  }
  
  // Load required memories
  const memories = await loader.loadProcessGuidance();
  
  // Proceed with action using current governance context
  return memories;
}
```

---

## FAILURE SCENARIOS & RESOLUTION

### Scenario 1: Version Mismatch Detected

**Symptom:**
```
Memory state: STALE
Governance version changed from 1.0.0 to 1.1.0
```

**Resolution:**
1. Automatic: `reloadIfStale()` triggers reload
2. Manual: Call `forceReload()` if automatic fails
3. Verify: Check state transitions to `LOADED`
4. Log: Review invalidation history

### Scenario 2: Checksum Mismatch

**Symptom:**
```
Checksum validation failed
Expected: abc123...
Got: def456...
```

**Resolution:**
1. Indicates governance memory files modified
2. Trigger full reload: `forceReload()`
3. Validate all files against version manifest
4. If persistent → escalate (file corruption)

### Scenario 3: Reload Failure

**Symptom:**
```
Memory state: INVALID
Reload failed: Schema validation error
```

**Resolution:**
1. Check governance memory files for corruption
2. Validate against schema: `memory/schema/memory-entry.json`
3. Restore from governance repository if needed
4. Retry initialization
5. If unresolvable → escalate to Johan

### Scenario 4: Persistent Stale State

**Symptom:**
```
Memory remains STALE after multiple reload attempts
```

**Resolution:**
1. Check `.governance-version.json` exists and is valid
2. Verify file permissions for memory directory
3. Check network/filesystem access
4. Manual intervention required
5. Escalate with logs

---

## TESTING REQUIREMENTS

### Test Coverage

1. **Version Detection**
   - ✅ Load governance version from file
   - ✅ Parse version correctly
   - ✅ Validate version format
   - ✅ Detect version changes

2. **Checksum Validation**
   - ✅ Calculate checksums correctly
   - ✅ Compare checksums for equality
   - ✅ Detect file modifications via checksum

3. **State Transitions**
   - ✅ Initialize to LOADING → LOADED
   - ✅ Detect stale transition LOADED → STALE
   - ✅ Handle invalid transition LOADING → INVALID
   - ✅ Reload transition STALE → LOADING → LOADED

4. **Reload Mechanism**
   - ✅ Atomic reload (all or nothing)
   - ✅ Rollback on validation failure
   - ✅ Log reload events
   - ✅ Update state after reload

5. **Invalidation Tracking**
   - ✅ Log invalidation events
   - ✅ Track invalidation history
   - ✅ Expose invalidation count
   - ✅ Audit trail complete

---

## ACCEPTANCE CRITERIA

✅ **AC1: FM App detects governance memory changes**
- Implementation: Version comparison + checksum validation
- Test: Modify governance memory, verify detection

✅ **AC2: Memory reloads without restart (if supported)**
- Implementation: `reloadIfStale()` and `forceReload()`
- Test: Trigger reload, verify new version loaded

✅ **AC3: Invalidation is explicit and auditable**
- Implementation: Invalidation event logging
- Test: Check invalidation log after version change

✅ **AC4: UI shows memory state (LOADED/STALE/INVALID)**
- Implementation: `getMemoryState()` and state tracking
- Test: Query state, verify correct values

---

## COMPLIANCE STATEMENT

This contract:

✅ Implements governance memory version tracking  
✅ Provides change detection mechanism  
✅ Ensures atomic memory reloads  
✅ Tracks all invalidation events explicitly  
✅ Exposes memory state for FM App UI  
✅ Maintains read-only memory access  
✅ Does NOT modify governance memory  
✅ Does NOT implement auto-learning  
✅ Does NOT access tenant memory  

**No governance rules were bypassed or weakened.**

---

## REFERENCES

- **Memory Rules:** `/foreman/behaviours/memory-rules.md`
- **Memory Schema:** `/memory/schema/memory-entry.json`
- **Version Schema:** `/memory/schema/governance-version.json`
- **Runtime Loader:** `/lib/memory/runtime-loader.ts`
- **Tests:** `/tests/test_governance_memory_sync.py`

---

**Status:** IMPLEMENTATION READY  
**Approval Required:** Johan Ras  
**After PR:** STOP and await human review

---

**End of Governance Memory Sync & Invalidation Contract**
