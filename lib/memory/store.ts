/**
 * Memory Store
 * 
 * Responsible for loading and querying memory entries from the memory fabric.
 * Implements scope-based loading and indexed querying.
 * 
 * @module lib/memory/store
 */

import * as fs from 'fs';
import * as path from 'path';

/**
 * Memory entry structure
 */
export interface MemoryEntry {
  id: string;
  scope: string;
  content: string;
  tags: string[];
  importance: number;
  created_at: string;
  updated_at: string;
}

/**
 * Memory Store
 * 
 * Loads and manages memory entries from the memory fabric with:
 * - Scope-based loading (global/, foreman/, platform/, runtime/)
 * - Fast indexed querying
 * - Integration with existing MemoryClient
 */
export class MemoryStore {
  private entries: Map<string, MemoryEntry>;
  private scopeIndex: Map<string, Set<string>>;
  private tagIndex: Map<string, Set<string>>;
  private memoryRoot: string;

  constructor(memoryRoot: string = './memory') {
    this.entries = new Map();
    this.scopeIndex = new Map();
    this.tagIndex = new Map();
    this.memoryRoot = memoryRoot;
  }

  /**
   * Load memory entries from all scopes
   */
  public async loadAll(): Promise<void> {
    const scopes = ['global', 'foreman', 'platform', 'runtime'];
    
    for (const scope of scopes) {
      await this.loadScope(scope);
    }
    
    this.buildIndices();
  }

  /**
   * Load memory entries from a specific scope
   */
  public async loadScope(scope: string): Promise<void> {
    const scopePath = path.join(this.memoryRoot, scope);
    
    if (!fs.existsSync(scopePath)) {
      console.warn(`[MemoryStore] Scope directory not found: ${scope}`);
      return;
    }

    const files = this.readDirectoryRecursive(scopePath, '.json');
    
    for (const file of files) {
      try {
        const content = fs.readFileSync(file, 'utf-8');
        const entry: MemoryEntry = JSON.parse(content);
        entry.scope = scope;
        this.entries.set(entry.id, entry);
      } catch (error) {
        console.error(`[MemoryStore] Failed to load ${file}:`, error);
      }
    }
  }

  /**
   * Build search indices for fast queries
   */
  private buildIndices(): void {
    this.scopeIndex.clear();
    this.tagIndex.clear();

    for (const [id, entry] of this.entries) {
      // Scope index
      if (!this.scopeIndex.has(entry.scope)) {
        this.scopeIndex.set(entry.scope, new Set());
      }
      this.scopeIndex.get(entry.scope)!.add(id);

      // Tag index
      for (const tag of entry.tags || []) {
        if (!this.tagIndex.has(tag)) {
          this.tagIndex.set(tag, new Set());
        }
        this.tagIndex.get(tag)!.add(id);
      }
    }
  }

  /**
   * Query entries by scope
   */
  public queryByScope(scope: string): MemoryEntry[] {
    const ids = this.scopeIndex.get(scope);
    if (!ids) return [];
    
    return Array.from(ids)
      .map(id => this.entries.get(id)!)
      .filter(entry => entry !== undefined);
  }

  /**
   * Query entries by tag
   */
  public queryByTag(tag: string): MemoryEntry[] {
    const ids = this.tagIndex.get(tag);
    if (!ids) return [];
    
    return Array.from(ids)
      .map(id => this.entries.get(id)!)
      .filter(entry => entry !== undefined);
  }

  /**
   * Get entry by ID
   */
  public getById(id: string): MemoryEntry | undefined {
    return this.entries.get(id);
  }

  /**
   * Get all entries
   */
  public getAll(): MemoryEntry[] {
    return Array.from(this.entries.values());
  }

  /**
   * Get entry count
   */
  public getCount(): number {
    return this.entries.size;
  }

  /**
   * Recursively read directory and filter by extension
   */
  private readDirectoryRecursive(dir: string, extension: string): string[] {
    const files: string[] = [];
    
    if (!fs.existsSync(dir)) {
      return files;
    }

    const items = fs.readdirSync(dir);
    
    for (const item of items) {
      const fullPath = path.join(dir, item);
      const stat = fs.statSync(fullPath);
      
      if (stat.isDirectory()) {
        files.push(...this.readDirectoryRecursive(fullPath, extension));
      } else if (fullPath.endsWith(extension)) {
        files.push(fullPath);
      }
    }
    
    return files;
  }
}
