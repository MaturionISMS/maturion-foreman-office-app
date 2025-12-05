/**
 * Maturion Foreman - TypeScript Memory Client
 * 
 * This module provides memory fabric integration for TypeScript/JavaScript-based
 * agents and applications (e.g., Vercel-hosted Foreman app).
 * 
 * Usage:
 * ```typescript
 * import { loadMemory, appendMemory, memoryHealthCheck } from '@/lib/memory/client';
 * 
 * // Load memories before reasoning
 * const memories = await loadMemory(['global', 'foreman'], ['architecture']);
 * 
 * // Write memory after significant events
 * await appendMemory({
 *   scope: 'foreman',
 *   title: 'Build Wave Completed',
 *   summary: 'Successfully completed build wave 1.2',
 *   importance: 'high',
 *   tags: ['build', 'governance']
 * });
 * ```
 */

import fs from 'fs/promises';
import path from 'path';
import { v4 as uuidv4 } from 'uuid';

/**
 * Memory entry structure based on the Unified Memory Fabric schema
 */
export interface MemoryEntry {
  id: string;
  scope: 'global' | 'foreman' | 'isms' | 'partpulse' | 'runtime' | 'platform';
  title: string;
  summary: string;
  created_at: string;
  author: 'foreman' | 'runtime' | 'builder' | 'human';
  importance: 'low' | 'medium' | 'high' | 'critical';
  tags: string[];
  details?: {
    rationale?: string;
    context?: string;
    constraints?: string[];
    examples?: string[];
    related_decisions?: string[];
    [key: string]: any;
  };
  links?: Array<{
    type: 'architecture_doc' | 'governance_doc' | 'issue' | 'pr' | 'module' | 'related_memory';
    path: string;
    description: string;
  }>;
}

/**
 * Memory collection structure (used in JSON files)
 */
interface MemoryCollection {
  memory_collection: string;
  version: string;
  description: string;
  entries: MemoryEntry[];
}

/**
 * Health check response structure
 */
export interface MemoryHealth {
  status: 'healthy' | 'warning' | 'error';
  memory_root_exists: boolean;
  schema_exists: boolean;
  scopes: Record<string, {
    exists: boolean;
    file_count: number;
    entry_count: number;
  }>;
  total_entries: number;
  issues: string[];
}

/**
 * Memory client class for interacting with the Unified Memory Fabric
 */
export class MemoryClient {
  private memoryRoot: string;
  private schemaPath: string;

  constructor(memoryRoot?: string) {
    // Default to ./memory or use provided path
    this.memoryRoot = memoryRoot || path.join(process.cwd(), 'memory');
    this.schemaPath = path.join(this.memoryRoot, 'schema', 'memory-entry.json');
  }

  /**
   * Load memory entries matching the specified criteria
   */
  async loadMemory(
    scopes: string[],
    tags?: string[],
    importanceMin?: 'low' | 'medium' | 'high' | 'critical'
  ): Promise<MemoryEntry[]> {
    const memories: MemoryEntry[] = [];
    const importanceOrder = { low: 0, medium: 1, high: 2, critical: 3 };
    const minImportanceVal = importanceOrder[importanceMin || 'low'] || 0;

    // Load from each scope directory
    for (const scope of scopes) {
      const scopeDir = path.join(this.memoryRoot, scope);
      
      try {
        const files = await fs.readdir(scopeDir);
        
        for (const file of files) {
          if (!file.endsWith('.json')) continue;
          
          const filePath = path.join(scopeDir, file);
          
          try {
            const content = await fs.readFile(filePath, 'utf-8');
            const data = JSON.parse(content);
            
            // Check if this is a collection or single entry
            let entries: MemoryEntry[] = [];
            if ('entries' in data && Array.isArray(data.entries)) {
              entries = data.entries;
            } else if ('id' in data && 'scope' in data) {
              entries = [data];
            } else {
              continue; // Unknown format
            }
            
            // Filter entries
            for (const entry of entries) {
              // Check scope match
              if (!scopes.includes(entry.scope)) continue;
              
              // Check importance
              const entryImportance = importanceOrder[entry.importance] || 0;
              if (entryImportance < minImportanceVal) continue;
              
              // Check tags if specified
              if (tags && tags.length > 0) {
                const entryTags = entry.tags || [];
                const hasMatchingTag = tags.some(tag => entryTags.includes(tag));
                if (!hasMatchingTag) continue;
              }
              
              memories.push(entry);
            }
          } catch (error) {
            console.warn(`Warning: Could not load memory file ${filePath}:`, error);
          }
        }
      } catch (error) {
        // Scope directory doesn't exist or is not readable
        continue;
      }
    }

    // Sort by importance (critical first) and then by created_at (newest first)
    memories.sort((a, b) => {
      const importanceA = importanceOrder[a.importance] || 0;
      const importanceB = importanceOrder[b.importance] || 0;
      
      if (importanceA !== importanceB) {
        return importanceB - importanceA; // Higher importance first
      }
      
      return (b.created_at || '').localeCompare(a.created_at || '');
    });

    return memories;
  }

  /**
   * Write a new memory entry to the fabric
   */
  async appendMemory(entry: Partial<MemoryEntry>, scopeOverride?: string): Promise<string> {
    // Determine scope
    const entryScope = scopeOverride || entry.scope;
    if (!entryScope) {
      throw new Error('Scope must be specified either in entry or as parameter');
    }

    // Generate ID if not provided
    if (!entry.id) {
      const timestamp = new Date().toISOString().split('T')[0];
      const uniqueId = uuidv4().split('-')[0];
      entry.id = `mem-${entryScope}-${timestamp}-${uniqueId}`;
    }

    // Set created_at if not provided
    if (!entry.created_at) {
      entry.created_at = new Date().toISOString();
    }

    // Set author if not provided
    if (!entry.author) {
      entry.author = 'foreman';
    }

    // Ensure scope is set
    entry.scope = entryScope as any;

    // Validate required fields
    const required = ['id', 'scope', 'title', 'summary', 'importance', 'tags'];
    const missing = required.filter(field => !(field in entry));
    if (missing.length > 0) {
      throw new Error(`Missing required fields: ${missing.join(', ')}`);
    }

    // Create scope directory if needed
    const scopeDir = path.join(this.memoryRoot, entryScope);
    await fs.mkdir(scopeDir, { recursive: true });

    // Determine filename (use date-based naming)
    const dateStr = new Date().toISOString().split('T')[0];
    const filename = `events-${dateStr}.json`;
    const filePath = path.join(scopeDir, filename);

    // Load existing entries or create new collection
    let data: MemoryCollection;
    try {
      const content = await fs.readFile(filePath, 'utf-8');
      data = JSON.parse(content);
    } catch {
      data = {
        memory_collection: `${entryScope.charAt(0).toUpperCase() + entryScope.slice(1)} Events - ${dateStr}`,
        version: '1.0.0',
        description: `Memory entries for ${entryScope} scope on ${dateStr}`,
        entries: []
      };
    }

    // Append new entry
    data.entries.push(entry as MemoryEntry);

    // Write back to file
    await fs.writeFile(filePath, JSON.stringify(data, null, 2));

    return entry.id!;
  }

  /**
   * Perform a health check on the memory fabric
   */
  async memoryHealthCheck(): Promise<MemoryHealth> {
    const health: MemoryHealth = {
      status: 'healthy',
      memory_root_exists: false,
      schema_exists: false,
      scopes: {},
      total_entries: 0,
      issues: []
    };

    // Check memory root exists
    try {
      await fs.access(this.memoryRoot);
      health.memory_root_exists = true;
    } catch {
      health.status = 'error';
      health.issues.push('Memory root directory does not exist');
      return health;
    }

    // Check schema exists
    try {
      await fs.access(this.schemaPath);
      health.schema_exists = true;
    } catch {
      health.status = 'warning';
      health.issues.push('Memory schema not found');
    }

    // Check each standard scope
    const standardScopes = ['global', 'foreman', 'platform', 'runtime'];
    for (const scope of standardScopes) {
      const scopeDir = path.join(this.memoryRoot, scope);
      
      try {
        const files = await fs.readdir(scopeDir);
        const jsonFiles = files.filter(f => f.endsWith('.json'));
        let entryCount = 0;

        for (const file of jsonFiles) {
          try {
            const content = await fs.readFile(path.join(scopeDir, file), 'utf-8');
            const data = JSON.parse(content);

            if ('entries' in data && Array.isArray(data.entries)) {
              entryCount += data.entries.length;
            } else if ('id' in data) {
              entryCount += 1;
            }
          } catch (error) {
            health.issues.push(`Error reading ${file}: ${error}`);
          }
        }

        health.scopes[scope] = {
          exists: true,
          file_count: jsonFiles.length,
          entry_count: entryCount
        };
        health.total_entries += entryCount;
      } catch {
        health.scopes[scope] = {
          exists: false,
          file_count: 0,
          entry_count: 0
        };
      }
    }

    if (health.total_entries === 0) {
      health.status = 'warning';
      health.issues.push('No memory entries found');
    }

    return health;
  }

  /**
   * Format loaded memories for inclusion in an AI agent prompt
   */
  formatMemoriesForPrompt(memories: MemoryEntry[], maxMemories: number = 20): string {
    if (memories.length === 0) {
      return 'No relevant memories loaded.';
    }

    // Limit to maxMemories
    const limitedMemories = memories.slice(0, maxMemories);

    const output: string[] = [];
    output.push('=== MEMORY CONTEXT ===\n');
    output.push('The following memories are critical context for your reasoning:\n');

    limitedMemories.forEach((memory, i) => {
      output.push(`\n--- Memory ${i + 1}: ${memory.title || 'Untitled'} ---`);
      output.push(`Scope: ${memory.scope || 'unknown'}`);
      output.push(`Importance: ${(memory.importance || 'unknown').toUpperCase()}`);
      output.push(`Tags: ${(memory.tags || []).join(', ')}`);
      output.push(`\nSummary: ${memory.summary || 'No summary'}`);

      // Include key details if present
      if (memory.details) {
        if (memory.details.rationale) {
          output.push(`\nRationale: ${memory.details.rationale}`);
        }
        if (memory.details.constraints && Array.isArray(memory.details.constraints)) {
          output.push('\nConstraints:');
          memory.details.constraints.forEach(constraint => {
            output.push(`  - ${constraint}`);
          });
        }
      }

      output.push(''); // Blank line separator
    });

    output.push('=== END MEMORY CONTEXT ===\n');
    return output.join('\n');
  }
}

// Default client instance
let defaultClient: MemoryClient | null = null;

/**
 * Get or create the default memory client instance
 */
export function getClient(): MemoryClient {
  if (!defaultClient) {
    defaultClient = new MemoryClient();
  }
  return defaultClient;
}

/**
 * Load memory entries (convenience function)
 */
export async function loadMemory(
  scopes: string[],
  tags?: string[],
  importanceMin?: 'low' | 'medium' | 'high' | 'critical'
): Promise<MemoryEntry[]> {
  return getClient().loadMemory(scopes, tags, importanceMin);
}

/**
 * Write a memory entry (convenience function)
 */
export async function appendMemory(
  entry: Partial<MemoryEntry>,
  scopeOverride?: string
): Promise<string> {
  return getClient().appendMemory(entry, scopeOverride);
}

/**
 * Check memory fabric health (convenience function)
 */
export async function memoryHealthCheck(): Promise<MemoryHealth> {
  return getClient().memoryHealthCheck();
}

/**
 * Format memories for AI prompt (convenience function)
 */
export function formatMemoriesForPrompt(
  memories: MemoryEntry[],
  maxMemories: number = 20
): string {
  return getClient().formatMemoriesForPrompt(memories, maxMemories);
}
