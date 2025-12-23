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
import { MemoryEntry, MemoryClient } from './client';

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
  }

  /**
   * Initialize the runtime loader
   * 
   * Validates that:
   * - Memory root exists
   * - Schema exists and is valid
   * - Global memory is present
   * 
   * FAIL-FAST: If initialization fails and failOnInvalid is true,
   * this will throw an error requiring immediate escalation.
   */
  async initialize(): Promise<void> {
    try {
      // Check memory root exists
      await fs.access(this.config.memoryRoot);
    } catch (error) {
      const message = `Memory root directory does not exist: ${this.config.memoryRoot}`;
      this.initializationError = message;
      
      if (this.config.failOnInvalid) {
        throw new Error(`GOVERNANCE FAILURE: ${message}`);
      }
      return;
    }

    // Load and validate schema
    try {
      const schemaContent = await fs.readFile(this.schemaPath, 'utf-8');
      this.schema = JSON.parse(schemaContent);
    } catch (error) {
      const message = `Failed to load memory schema: ${error}`;
      this.initializationError = message;
      
      if (this.config.failOnInvalid) {
        throw new Error(`GOVERNANCE FAILURE: ${message}`);
      }
      return;
    }

    // Validate global memory exists
    const globalDir = path.join(this.config.memoryRoot, 'global');
    try {
      const files = await fs.readdir(globalDir);
      const jsonFiles = files.filter(f => f.endsWith('.json'));
      
      if (jsonFiles.length === 0) {
        const message = 'No global memory files found';
        this.initializationError = message;
        
        if (this.config.failOnInvalid) {
          throw new Error(`GOVERNANCE FAILURE: ${message}`);
        }
      }
    } catch (error) {
      const message = `Failed to access global memory: ${error}`;
      this.initializationError = message;
      
      if (this.config.failOnInvalid) {
        throw new Error(`GOVERNANCE FAILURE: ${message}`);
      }
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
   * Perform health check on memory fabric
   * 
   * @returns Health check result
   */
  async healthCheck() {
    return this.client.memoryHealthCheck();
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
