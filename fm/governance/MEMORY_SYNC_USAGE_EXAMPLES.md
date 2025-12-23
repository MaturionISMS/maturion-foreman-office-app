# Governance Memory Sync & Invalidation — Usage Examples

## PURPOSE

This document provides practical usage examples for the Governance Memory Sync & Invalidation Contract implementation.

---

## QUICK START

### 1. Basic Initialization with Sync Check

```typescript
import { createGlobalMemoryRuntime } from '@/lib/memory/runtime-loader';

async function initializeMemory() {
  // Create and initialize runtime loader
  const loader = await createGlobalMemoryRuntime();
  
  // Check initialization state
  const state = loader.getMemoryState();
  console.log('Memory State:', state); // Should be 'LOADED'
  
  // Get loaded version
  const version = loader.getLoadedVersion();
  console.log('Governance Version:', version?.version);
  
  return loader;
}
```

### 2. Check for Stale Memory

```typescript
async function checkMemoryFreshness(loader) {
  const isStale = await loader.isMemoryStale();
  
  if (isStale) {
    console.warn('⚠️  Governance memory is stale!');
    
    // Get current version
    const currentVersion = await loader.getGovernanceVersion();
    const loadedVersion = loader.getLoadedVersion();
    
    console.log(`Loaded: ${loadedVersion?.version}`);
    console.log(`Current: ${currentVersion.version}`);
    
    return true;
  }
  
  console.log('✅ Memory is current');
  return false;
}
```

### 3. Reload If Stale

```typescript
async function syncMemoryIfNeeded(loader) {
  const reloaded = await loader.reloadIfStale();
  
  if (reloaded) {
    console.log('✅ Memory reloaded successfully');
    
    // Get new version
    const newVersion = loader.getLoadedVersion();
    console.log('New version:', newVersion?.version);
  } else {
    console.log('ℹ️  Memory already current, no reload needed');
  }
  
  return reloaded;
}
```

---

## INTEGRATION PATTERNS

### Pattern 1: Application Startup

```typescript
// In your FM App startup routine
async function startupMemoryCheck() {
  try {
    const loader = await createGlobalMemoryRuntime();
    
    // Verify state
    const state = loader.getMemoryState();
    if (state !== 'LOADED') {
      throw new Error(`Memory initialization failed: ${state}`);
    }
    
    // Get version info
    const version = loader.getLoadedVersion();
    console.log(`📚 Governance Memory v${version?.version} loaded`);
    
    // Check health
    const health = await loader.healthCheck();
    console.log(`Memory Health:`, health);
    
    if (health.is_stale) {
      console.warn('Memory is stale, consider reload');
    }
    
    return loader;
  } catch (error) {
    console.error('❌ Memory initialization failed:', error);
    // Escalate to admin
    throw error;
  }
}
```

### Pattern 2: Background Sync Task

```typescript
// Run this periodically (e.g., every 5 minutes)
class MemorySyncService {
  private loader: GlobalMemoryRuntimeLoader;
  private checkInterval: number = 5 * 60 * 1000; // 5 minutes
  
  async start() {
    this.loader = await createGlobalMemoryRuntime();
    
    // Check immediately
    await this.checkAndSync();
    
    // Set up periodic check
    setInterval(() => this.checkAndSync(), this.checkInterval);
  }
  
  private async checkAndSync() {
    try {
      const isStale = await this.loader.isMemoryStale();
      
      if (isStale) {
        console.log('🔄 Governance memory version changed, reloading...');
        
        const success = await this.loader.reloadIfStale();
        
        if (success) {
          const version = this.loader.getLoadedVersion();
          console.log(`✅ Reloaded to v${version?.version}`);
          
          // Log invalidation
          const lastInvalidation = this.loader.getLastInvalidation();
          console.log('Invalidation:', lastInvalidation);
        } else {
          console.error('❌ Reload failed');
          // Escalate
        }
      }
    } catch (error) {
      console.error('Memory sync check failed:', error);
    }
  }
}
```

### Pattern 3: UI State Display Component

```typescript
// React component example
import { useEffect, useState } from 'react';

interface MemoryStatus {
  state: string;
  version: string;
  timestamp: string | null;
  isStale: boolean;
}

export function MemoryStatusIndicator() {
  const [status, setStatus] = useState<MemoryStatus | null>(null);
  
  useEffect(() => {
    async function loadStatus() {
      const loader = await createGlobalMemoryRuntime();
      
      const health = await loader.healthCheck();
      const version = loader.getLoadedVersion();
      
      setStatus({
        state: health.memory_state,
        version: health.governance_version,
        timestamp: health.last_reload,
        isStale: health.is_stale,
      });
    }
    
    loadStatus();
    
    // Refresh every minute
    const interval = setInterval(loadStatus, 60000);
    return () => clearInterval(interval);
  }, []);
  
  if (!status) return <div>Loading...</div>;
  
  return (
    <div className="memory-status">
      <StatusBadge state={status.state} />
      <span>v{status.version}</span>
      {status.isStale && <WarningIcon />}
    </div>
  );
}

function StatusBadge({ state }: { state: string }) {
  const colors = {
    LOADED: 'green',
    STALE: 'yellow',
    INVALID: 'red',
    LOADING: 'blue',
    UNINITIALIZED: 'gray',
  };
  
  return (
    <span 
      className="badge" 
      style={{ backgroundColor: colors[state] || 'gray' }}
    >
      {state}
    </span>
  );
}
```

### Pattern 4: Pre-Governance Action Guard

```typescript
// Before any governance decision
async function performGovernanceAction(action: string) {
  const loader = await createGlobalMemoryRuntime();
  
  // Guard: Ensure memory is not stale
  const state = loader.getMemoryState();
  if (state === 'STALE') {
    throw new Error(
      'Cannot perform governance action: Memory is stale. Reload required.'
    );
  }
  
  if (state !== 'LOADED') {
    throw new Error(
      `Cannot perform governance action: Memory state is ${state}`
    );
  }
  
  // Check for staleness
  const isStale = await loader.isMemoryStale();
  if (isStale) {
    throw new Error(
      'Governance memory has changed. Reload before proceeding.'
    );
  }
  
  // Load required governance context
  const memories = await loader.loadProcessGuidance();
  
  // Proceed with action using current context
  console.log(`Performing ${action} with ${memories.length} governance memories`);
  
  return { action, memories };
}
```

### Pattern 5: Force Reload on Demand

```typescript
// Admin action: Force memory reload
async function adminForceReload() {
  const loader = await createGlobalMemoryRuntime();
  
  try {
    console.log('🔄 Forcing memory reload...');
    
    const oldVersion = loader.getLoadedVersion();
    console.log(`Old version: ${oldVersion?.version}`);
    
    await loader.forceReload();
    
    const newVersion = loader.getLoadedVersion();
    console.log(`✅ Reloaded to: ${newVersion?.version}`);
    
    // Check invalidation history
    const history = loader.getInvalidationHistory();
    console.log(`Total invalidations: ${history.length}`);
    
    return true;
  } catch (error) {
    console.error('❌ Force reload failed:', error);
    return false;
  }
}
```

---

## ERROR HANDLING

### Handling Stale State

```typescript
async function handleStaleMemory() {
  const loader = await createGlobalMemoryRuntime();
  
  if (loader.getMemoryState() === 'STALE') {
    console.warn('Memory is stale, attempting reload...');
    
    try {
      await loader.forceReload();
      console.log('✅ Memory reloaded successfully');
    } catch (error) {
      console.error('Reload failed:', error);
      
      // Get error details
      const initError = loader.getInitializationError();
      console.error('Initialization error:', initError);
      
      // Escalate to admin
      await escalateToAdmin({
        issue: 'Memory reload failed',
        error: error.message,
        state: loader.getMemoryState(),
      });
      
      throw error;
    }
  }
}
```

### Handling Invalid State

```typescript
async function handleInvalidMemory() {
  const loader = await createGlobalMemoryRuntime();
  
  if (loader.getMemoryState() === 'INVALID') {
    console.error('❌ Memory is in INVALID state');
    
    const error = loader.getInitializationError();
    console.error('Error:', error);
    
    // Check health for diagnostics
    const health = await loader.healthCheck();
    console.error('Health:', health);
    
    // Soft stop: Cannot proceed with governance actions
    throw new Error(
      'Memory is invalid. Manual intervention required. ' +
      `Error: ${error}`
    );
  }
}
```

---

## MONITORING & OBSERVABILITY

### Memory Health Check

```typescript
async function monitorMemoryHealth() {
  const loader = await createGlobalMemoryRuntime();
  
  const health = await loader.healthCheck();
  
  return {
    status: health.status,
    state: health.memory_state,
    version: health.governance_version,
    lastReload: health.last_reload,
    isStale: health.is_stale,
    invalidationCount: health.invalidation_count,
    rootExists: health.memory_root_exists,
    schemaExists: health.schema_exists,
    totalEntries: health.total_entries,
  };
}
```

### Invalidation Audit Log

```typescript
async function getInvalidationAuditLog() {
  const loader = await createGlobalMemoryRuntime();
  
  const history = loader.getInvalidationHistory();
  
  console.log('Invalidation History:');
  console.log('='.repeat(60));
  
  for (const event of history) {
    console.log(`
Timestamp: ${event.timestamp}
Old Version: ${event.old_version || 'N/A'}
New Version: ${event.new_version}
Reason: ${event.reason}
Triggered Reload: ${event.triggered_reload ? 'Yes' : 'No'}
${'='.repeat(60)}
    `);
  }
  
  return history;
}
```

---

## TESTING SCENARIOS

### Test: Version Change Detection

```typescript
async function testVersionChangeDetection() {
  const loader = await createGlobalMemoryRuntime();
  
  // Get current version
  const v1 = loader.getLoadedVersion();
  console.log('Initial version:', v1?.version);
  
  // Simulate governance version change
  // (In real scenario, this would be external update)
  console.log('Simulating version change...');
  
  // Check if stale
  const isStale = await loader.isMemoryStale();
  
  if (isStale) {
    console.log('✅ Stale detection works');
    
    // Reload
    await loader.reloadIfStale();
    
    const v2 = loader.getLoadedVersion();
    console.log('New version:', v2?.version);
  } else {
    console.log('ℹ️  No version change detected');
  }
}
```

### Test: Atomic Reload

```typescript
async function testAtomicReload() {
  const loader = await createGlobalMemoryRuntime();
  
  const stateBefore = loader.getMemoryState();
  const versionBefore = loader.getLoadedVersion();
  
  console.log('Before reload:', { stateBefore, versionBefore: versionBefore?.version });
  
  try {
    await loader.forceReload();
    
    const stateAfter = loader.getMemoryState();
    const versionAfter = loader.getLoadedVersion();
    
    console.log('After reload:', { stateAfter, versionAfter: versionAfter?.version });
    
    // Verify state is LOADED (atomic success)
    if (stateAfter === 'LOADED') {
      console.log('✅ Atomic reload successful');
    }
  } catch (error) {
    // On failure, state should be unchanged (atomic rollback)
    const stateAfter = loader.getMemoryState();
    const versionAfter = loader.getLoadedVersion();
    
    console.log('Rollback:', { stateAfter, versionAfter: versionAfter?.version });
    console.log('✅ Atomic rollback on failure');
  }
}
```

---

## TROUBLESHOOTING

### Issue: Memory Always Reports Stale

**Symptom:** `isMemoryStale()` always returns true

**Resolution:**
```typescript
async function diagnoseStaleIssue() {
  const loader = await createGlobalMemoryRuntime();
  
  // Get both versions
  const loaded = loader.getLoadedVersion();
  const current = await loader.getGovernanceVersion();
  
  console.log('Loaded version:', loaded?.version);
  console.log('Loaded checksum:', loaded?.checksum);
  
  console.log('Current version:', current.version);
  console.log('Current checksum:', current.checksum);
  
  // Compare
  if (loaded?.version !== current.version) {
    console.log('❌ Version mismatch');
  }
  
  if (loaded?.checksum !== current.checksum) {
    console.log('❌ Checksum mismatch');
  }
  
  // Fix: Force reload
  await loader.forceReload();
}
```

### Issue: Reload Fails Repeatedly

**Symptom:** `forceReload()` throws error

**Resolution:**
```typescript
async function diagnoseReloadFailure() {
  const loader = await createGlobalMemoryRuntime();
  
  try {
    await loader.forceReload();
  } catch (error) {
    console.error('Reload failed:', error.message);
    
    // Check file access
    const health = await loader.healthCheck();
    console.log('Root exists:', health.memory_root_exists);
    console.log('Schema exists:', health.schema_exists);
    
    // Check initialization error
    const initError = loader.getInitializationError();
    console.log('Init error:', initError);
    
    // Manual intervention required
    console.log('❌ Escalate to admin for manual fix');
  }
}
```

---

## REFERENCES

- **Contract:** `/fm/governance/MEMORY_SYNC_CONTRACT.md`
- **Schema:** `/memory/schema/governance-version.json`
- **Runtime Loader:** `/lib/memory/runtime-loader.ts`
- **Tests:** `/tests/test_governance_memory_sync.py`

---

**End of Usage Examples**
