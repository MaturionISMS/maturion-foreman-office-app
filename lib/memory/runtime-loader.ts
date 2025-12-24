/**
 * Global Memory Runtime Loader (READ-ONLY)
 * 
 * This module provides read-only runtime access to Global Experience Memory.
 * 
 * GOVERNANCE COMPLIANCE:
 * - Implements /memory/README.md requirements (governance authority)
 * - Follows /foreman/behaviours/memory-rules.md mandatory load points
 * - Validates against /memory/schema/memory-entry.json
 * 
 * READ-ONLY ENFORCEMENT:
 * - NO write methods exposed
 * - NO memory modification capability
 * - NO learning automation
 * - NO tenant memory access
 * 
 * This is Phase 1: Read-only access only.
 * Write capabilities are explicitly out of scope.
 */

import fs from 'fs/promises';
import path from 'path';
import crypto from 'crypto';
import { MemoryEntry, MemoryClient } from './client';
import { MemoryLifecycleManager, MemoryLifecycleState } from './lifecycle-manager';
import { HealthMonitor } from './health-monitor';

/**
 * Memory state enum (Legacy - use MemoryLifecycleState for new code)
 */
export type MemoryState = 
  | 'UNINITIALIZED' 
  | 'LOADING' 
  | 'LOADED' 
  | 'STALE' 
  | 'INVALID';

/**
 * Governance version structure
 */
export interface GovernanceVersion {
  version: string;
  timestamp: string;
  commit_sha?: string;
  checksum: string;
  schema_version: string;
  files: Array<{
    path: string;
    checksum: string;
  }>;
  description?: string;
}

/**
 * Invalidation event
 */
export interface InvalidationEvent {
  timestamp: string;
  old_version: string | null;
  new_version: string;
  reason: 'version_mismatch' | 'checksum_mismatch' | 'manual' | 'initialization';
  triggered_reload: boolean;
}

/**
 * Runtime memory configuration
 */
interface RuntimeMemoryConfig {
  memoryRoot: string;
  validateOnLoad: boolean;
  failOnInvalid: boolean;
}

/**
 * Memory validation result
 */
interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
}

/**
 * Global Memory Runtime Loader
 * 
 * READ-ONLY: This class provides immutable access to global memory.
 * No write operations are permitted or implemented.
 */
export class GlobalMemoryRuntimeLoader {
  private client: MemoryClient;
  private config: RuntimeMemoryConfig;
  private schemaPath: string;
  private schema: any = null;
  private initializationError: string | null = null;
  
  // Lifecycle management
  private lifecycleManager: MemoryLifecycleManager;
  private healthMonitor: HealthMonitor;
  
  // Governance sync state (legacy)
  private memoryState: MemoryState = 'UNINITIALIZED';
  private loadedVersion: GovernanceVersion | null = null;
  private governanceVersionPath: string;
  private invalidationHistory: InvalidationEvent[] = [];
  private lastReloadTimestamp: string | null = null;

  /**
   * Create a new read-only memory runtime loader
   * 
   * @param config - Runtime configuration
   */
  constructor(config?: Partial<RuntimeMemoryConfig>) {
    this.config = {
      memoryRoot: config?.memoryRoot || path.join(process.cwd(), 'memory'),
      validateOnLoad: config?.validateOnLoad !== false, // Default to true
      failOnInvalid: config?.failOnInvalid !== false,   // Default to true
    };

    this.client = new MemoryClient(this.config.memoryRoot);
    this.schemaPath = path.join(this.config.memoryRoot, 'schema', 'memory-entry.json');
    this.governanceVersionPath = path.join(this.config.memoryRoot, '.governance-version.json');
    
    // Initialize lifecycle components
    this.lifecycleManager = new MemoryLifecycleManager({
      memoryRoot: this.config.memoryRoot,
      failOnCritical: this.config.failOnInvalid, // Maps to fail on critical failures
      enablePrivacyChecks: true
    });
    
    this.healthMonitor = new HealthMonitor();
    
    // Wire up lifecycle events to health monitor
    this.lifecycleManager.on('memory.lifecycle.loading.complete', (event) => {
      if (event.loadTimeSec) {
        this.healthMonitor.trackLoadTime(event.loadTimeSec);
      }
    });
    
    this.lifecycleManager.on('memory.lifecycle.validating.complete', (event) => {
      if (event.validationTimeSec) {
        this.healthMonitor.trackValidationTime(event.validationTimeSec);
      }
      if (event.validationErrors && event.validationErrors > 0) {
        // Track each error individually
        for (let i = 0; i < event.validationErrors; i++) {
          this.healthMonitor.trackValidationError();
        }
      }
      if (event.privacyViolations && event.privacyViolations > 0) {
        // Track each privacy violation individually
        for (let i = 0; i < event.privacyViolations; i++) {
          this.healthMonitor.trackPrivacyViolation();
        }
      }
    });
  }

  /**
   * Initialize the runtime loader
   * 
   * Validates that:
   * - Memory root exists
   * - Schema exists and is valid
   * - Global memory is present
   * - Governance version is loadable
   * 
   * FAIL-FAST: If initialization fails and failOnInvalid is true,
   * this will throw an error requiring immediate escalation.
   * 
   * Now uses MemoryLifecycleManager for full state machine.
   */
  async initialize(): Promise<void> {
    try {
      // Use lifecycle manager for initialization
      await this.lifecycleManager.initialize();
      
      // Update legacy state for backward compatibility
      const lifecycleState = this.lifecycleManager.getState();
      this.memoryState = this.mapLifecycleStateToLegacy(lifecycleState);
      
      // Load governance version (legacy)
      try {
        const version = await this.loadGovernanceVersionFile();
        this.loadedVersion = version;
        this.recordInvalidation(null, version.version, 'initialization', true);
        this.lastReloadTimestamp = new Date().toISOString();
      } catch (error) {
        console.warn('Warning: Could not load governance version:', error);
      }
      
      // If lifecycle manager succeeded, clear any initialization error
      if (this.lifecycleManager.isUsable() || this.lifecycleManager.isDegraded()) {
        this.initializationError = null;
      }
    } catch (error) {
      const message = `Memory lifecycle initialization failed: ${error instanceof Error ? error.message : error}`;
      this.initializationError = message;
      this.memoryState = 'INVALID';
      
      if (this.config.failOnInvalid) {
        throw new Error(`GOVERNANCE FAILURE: ${message}`);
      }
    }
  }
  
  /**
   * Map lifecycle state to legacy state enum
   */
  private mapLifecycleStateToLegacy(lifecycleState: MemoryLifecycleState): MemoryState {
    switch (lifecycleState) {
      case MemoryLifecycleState.UNINITIALIZED:
        return 'UNINITIALIZED';
      case MemoryLifecycleState.LOADING:
        return 'LOADING';
      case MemoryLifecycleState.VALIDATING:
        return 'LOADING';
      case MemoryLifecycleState.USABLE:
        return 'LOADED';
      case MemoryLifecycleState.DEGRADED:
        return 'LOADED'; // Still usable, just degraded
      case MemoryLifecycleState.FAILED:
        return 'INVALID';
      default:
        return 'INVALID';
    }
  }

  /**
   * Get initialization status
   * 
   * @returns true if initialized successfully, false otherwise
   */
  isInitialized(): boolean {
    return this.initializationError === null;
  }

  /**
   * Get initialization error if any
   * 
   * @returns Error message or null
   */
  getInitializationError(): string | null {
    return this.initializationError;
  }

  /**
   * Load global memory entries (READ-ONLY)
   * 
   * This method provides read-only access to global memory.
   * Memory entries are loaded from the filesystem but are immutable at runtime.
   * 
   * @param tags - Optional tags to filter by
   * @param importanceMin - Minimum importance level
   * @returns Array of memory entries (immutable)
   */
  async loadGlobalMemory(
    tags?: string[],
    importanceMin?: 'low' | 'medium' | 'high' | 'critical'
  ): Promise<Readonly<MemoryEntry>[]> {
    // Fail fast if not initialized
    if (!this.isInitialized()) {
      if (this.config.failOnInvalid) {
        throw new Error(`Cannot load memory: ${this.initializationError}`);
      }
      return [];
    }

    // Load from global scope only
    const memories = await this.client.loadMemory(['global'], tags, importanceMin);

    // Validate if configured
    if (this.config.validateOnLoad) {
      const validation = this.validateMemories(memories);
      
      if (!validation.valid && this.config.failOnInvalid) {
        throw new Error(
          `Memory validation failed: ${validation.errors.join(', ')}`
        );
      }
    }

    // Return as readonly to enforce immutability
    return memories as Readonly<MemoryEntry>[];
  }

  /**
   * Load memory for process guidance (READ-ONLY)
   * 
   * Loads memories tagged with process-related information
   * to guide runtime behavior.
   */
  async loadProcessGuidance(): Promise<Readonly<MemoryEntry>[]> {
    return this.loadGlobalMemory(
      ['governance', 'architecture', 'philosophy'],
      'high'
    );
  }

  /**
   * Load memory for escalation heuristics (READ-ONLY)
   * 
   * Loads memories that help determine when to escalate issues.
   */
  async loadEscalationHeuristics(): Promise<Readonly<MemoryEntry>[]> {
    return this.loadGlobalMemory(
      ['governance', 'escalation', 'incidents'],
      'medium'
    );
  }

  /**
   * Load memory for pattern recognition (READ-ONLY)
   * 
   * Loads memories that contain learned patterns for decision-making.
   */
  async loadPatternMemories(): Promise<Readonly<MemoryEntry>[]> {
    return this.loadGlobalMemory(
      ['build', 'architecture', 'qa'],
      'medium'
    );
  }

  /**
   * Validate memory entries against governance schema
   * 
   * @param memories - Memories to validate
   * @returns Validation result
   */
  private validateMemories(memories: MemoryEntry[]): ValidationResult {
    const result: ValidationResult = {
      valid: true,
      errors: [],
      warnings: []
    };

    if (!this.schema) {
      result.valid = false;
      result.errors.push('Schema not loaded');
      return result;
    }

    for (const memory of memories) {
      // Validate required fields
      const requiredFields = ['id', 'scope', 'title', 'summary', 'importance', 'tags'];
      for (const field of requiredFields) {
        if (!(field in memory) || memory[field as keyof MemoryEntry] === undefined) {
          result.valid = false;
          result.errors.push(`Memory ${memory.id || 'unknown'} missing required field: ${field}`);
        }
      }

      // Validate scope is 'global'
      if (memory.scope !== 'global') {
        result.warnings.push(`Memory ${memory.id} has non-global scope: ${memory.scope}`);
      }

      // Validate importance level
      const validImportance = ['low', 'medium', 'high', 'critical'];
      if (!validImportance.includes(memory.importance)) {
        result.valid = false;
        result.errors.push(
          `Memory ${memory.id} has invalid importance: ${memory.importance}`
        );
      }

      // Validate tags is array
      if (!Array.isArray(memory.tags)) {
        result.valid = false;
        result.errors.push(`Memory ${memory.id} tags must be an array`);
      }
    }

    return result;
  }

  /**
   * Format memories for AI agent prompt (READ-ONLY)
   * 
   * @param memories - Memories to format
   * @param maxMemories - Maximum number of memories to include
   * @returns Formatted string for prompt injection
   */
  formatForPrompt(
    memories: Readonly<MemoryEntry>[],
    maxMemories: number = 20
  ): string {
    return this.client.formatMemoriesForPrompt(
      memories as MemoryEntry[],
      maxMemories
    );
  }

  /**
   * Get current memory state
   * 
   * @returns Current state (UNINITIALIZED, LOADING, LOADED, STALE, INVALID)
   */
  getMemoryState(): MemoryState {
    return this.memoryState;
  }

  /**
   * Get loaded governance version
   * 
   * @returns Loaded version or null if not loaded
   */
  getLoadedVersion(): GovernanceVersion | null {
    return this.loadedVersion;
  }

  /**
   * Load governance version from file
   * 
   * @returns Governance version object
   */
  private async loadGovernanceVersionFile(): Promise<GovernanceVersion> {
    try {
      const content = await fs.readFile(this.governanceVersionPath, 'utf-8');
      return JSON.parse(content) as GovernanceVersion;
    } catch (error) {
      throw new Error(`Failed to load governance version file: ${error}`);
    }
  }

  /**
   * Get current governance version from filesystem
   * 
   * @returns Current governance version
   */
  async getGovernanceVersion(): Promise<GovernanceVersion> {
    return this.loadGovernanceVersionFile();
  }

  /**
   * Check if memory is stale (version mismatch)
   * 
   * @returns True if governance version has changed since load
   */
  async isMemoryStale(): Promise<boolean> {
    if (this.memoryState !== 'LOADED' && this.memoryState !== 'STALE') {
      return false;
    }

    try {
      const currentVersion = await this.getGovernanceVersion();
      
      if (!this.loadedVersion) {
        return true;
      }

      // Check version number
      if (currentVersion.version !== this.loadedVersion.version) {
        this.memoryState = 'STALE';
        return true;
      }

      // Check checksum
      if (currentVersion.checksum !== this.loadedVersion.checksum) {
        this.memoryState = 'STALE';
        return true;
      }

      return false;
    } catch (error) {
      // If we can't check, assume stale to be safe
      this.memoryState = 'STALE';
      return true;
    }
  }

  /**
   * Reload memory if stale
   * 
   * @returns True if reload was performed, false if not needed or failed
   */
  async reloadIfStale(): Promise<boolean> {
    const isStale = await this.isMemoryStale();
    
    if (!isStale) {
      return false;
    }

    try {
      await this.forceReload();
      return true;
    } catch (error) {
      console.error('Memory reload failed:', error);
      return false;
    }
  }

  /**
   * Force memory reload (atomic)
   * 
   * Reloads all governance memory atomically.
   * If any validation fails, rollback to previous state.
   */
  async forceReload(): Promise<void> {
    const previousState = this.memoryState;
    const previousVersion = this.loadedVersion;
    
    this.memoryState = 'LOADING';

    try {
      // Load new governance version
      const newVersion = await this.loadGovernanceVersionFile();

      // Validate we can load global memory with new version
      // This is a dry-run to ensure atomicity
      const testMemories = await this.client.loadMemory(['global']);
      
      if (this.config.validateOnLoad) {
        const validation = this.validateMemories(testMemories);
        if (!validation.valid) {
          throw new Error(`Memory validation failed: ${validation.errors.join(', ')}`);
        }
      }

      // Atomic swap: Update loaded version
      const oldVersion = this.loadedVersion?.version || null;
      this.loadedVersion = newVersion;
      this.memoryState = 'LOADED';
      this.lastReloadTimestamp = new Date().toISOString();

      // Record invalidation
      const reason = oldVersion && oldVersion !== newVersion.version 
        ? 'version_mismatch' 
        : 'checksum_mismatch';
      this.recordInvalidation(oldVersion, newVersion.version, reason, true);

      console.log(`Memory reloaded: ${oldVersion} → ${newVersion.version}`);
    } catch (error) {
      // Rollback on failure
      this.memoryState = previousState;
      this.loadedVersion = previousVersion;
      
      throw new Error(`Atomic reload failed: ${error}`);
    }
  }

  /**
   * Record invalidation event
   * 
   * @param oldVersion - Previous version
   * @param newVersion - New version
   * @param reason - Reason for invalidation
   * @param triggeredReload - Whether reload was triggered
   */
  private recordInvalidation(
    oldVersion: string | null,
    newVersion: string,
    reason: InvalidationEvent['reason'],
    triggeredReload: boolean
  ): void {
    const event: InvalidationEvent = {
      timestamp: new Date().toISOString(),
      old_version: oldVersion,
      new_version: newVersion,
      reason,
      triggered_reload: triggeredReload,
    };

    this.invalidationHistory.push(event);

    // Keep only last 50 events
    if (this.invalidationHistory.length > 50) {
      this.invalidationHistory = this.invalidationHistory.slice(-50);
    }
  }

  /**
   * Get last invalidation event
   * 
   * @returns Last invalidation event or null
   */
  getLastInvalidation(): InvalidationEvent | null {
    return this.invalidationHistory.length > 0
      ? this.invalidationHistory[this.invalidationHistory.length - 1]
      : null;
  }

  /**
   * Get invalidation history
   * 
   * @returns Array of invalidation events
   */
  getInvalidationHistory(): InvalidationEvent[] {
    return [...this.invalidationHistory];
  }

  /**
   * Perform health check on memory fabric
   * 
   * @returns Health check result with sync status and lifecycle state
   */
  async healthCheck() {
    const baseHealth = await this.client.memoryHealthCheck();
    const lifecycleHealth = await this.lifecycleManager.healthCheck();
    const healthStatus = this.healthMonitor.getHealthStatus();
    const performanceMetrics = this.healthMonitor.getPerformanceMetrics();
    
    return {
      ...baseHealth,
      governance_version: this.loadedVersion?.version || 'unknown',
      memory_state: this.memoryState,
      lifecycle_state: this.lifecycleManager.getState(),
      lifecycle_health: lifecycleHealth,
      health_status: healthStatus,
      performance_metrics: performanceMetrics,
      last_reload: this.lastReloadTimestamp,
      is_stale: await this.isMemoryStale(),
      invalidation_count: this.invalidationHistory.length,
    };
  }
  
  /**
   * Get lifecycle manager (for advanced usage)
   */
  getLifecycleManager(): MemoryLifecycleManager {
    return this.lifecycleManager;
  }
  
  /**
   * Get health monitor (for advanced usage)
   */
  getHealthMonitor(): HealthMonitor {
    return this.healthMonitor;
  }
  
  /**
   * Check if memory is in a usable state
   */
  isMemoryUsable(): boolean {
    return this.lifecycleManager.isUsable() || this.lifecycleManager.isDegraded();
  }
  
  /**
   * Check if memory has failed critically
   */
  isMemoryFailed(): boolean {
    return this.lifecycleManager.isFailed();
  }
}

/**
 * Create and initialize a global memory runtime loader
 * 
 * This is the primary entry point for runtime memory access.
 * 
 * @param config - Optional configuration
 * @returns Initialized loader
 */
export async function createGlobalMemoryRuntime(
  config?: Partial<RuntimeMemoryConfig>
): Promise<GlobalMemoryRuntimeLoader> {
  const loader = new GlobalMemoryRuntimeLoader(config);
  await loader.initialize();
  return loader;
}

/**
 * EXPLICIT READ-ONLY ENFORCEMENT
 * 
 * The following operations are FORBIDDEN in this module:
 * 
 * ❌ appendMemory() - NO WRITE CAPABILITY
 * ❌ writeMemory() - NO WRITE CAPABILITY
 * ❌ modifyMemory() - NO WRITE CAPABILITY
 * ❌ deleteMemory() - NO WRITE CAPABILITY
 * ❌ Learning automation - OUT OF SCOPE
 * ❌ Tenant memory access - OUT OF SCOPE
 * ❌ Cross-project memory - OUT OF SCOPE
 * 
 * This module provides READ-ONLY access to GLOBAL memory ONLY.
 * All other memory operations are explicitly prohibited.
 */

// Type guard to prevent accidental writes
export type ReadOnlyMemoryEntry = Readonly<MemoryEntry>;
export type ReadOnlyMemoryArray = ReadonlyArray<ReadOnlyMemoryEntry>;
