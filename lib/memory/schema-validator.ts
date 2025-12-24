/**
 * Schema Validator
 * 
 * Validates memory entries against the memory-entry.json schema.
 * Checks required fields, types, and integrity.
 * 
 * @module lib/memory/schema-validator
 */

/**
 * Validation result
 */
export interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
}

/**
 * Schema Validator
 * 
 * Validates memory entries with:
 * - Required field checking
 * - Type validation
 * - Tag format validation
 * - Scope integrity checking
 */
export class SchemaValidator {
  private requiredFields: string[];

  constructor() {
    this.requiredFields = [
      'id',
      'scope',
      'content',
      'tags',
      'importance',
      'created_at',
      'updated_at'
    ];
  }

  /**
   * Validate a memory entry against schema
   */
  public validate(entry: any): ValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];

    // Check required fields
    for (const field of this.requiredFields) {
      if (!(field in entry)) {
        errors.push(`Missing required field: ${field}`);
      }
    }

    // Validate field types
    if (entry.id && typeof entry.id !== 'string') {
      errors.push('Field "id" must be a string');
    }

    if (entry.scope && typeof entry.scope !== 'string') {
      errors.push('Field "scope" must be a string');
    }

    if (entry.content && typeof entry.content !== 'string') {
      errors.push('Field "content" must be a string');
    }

    if (entry.tags && !Array.isArray(entry.tags)) {
      errors.push('Field "tags" must be an array');
    }

    if (entry.importance && typeof entry.importance !== 'number') {
      errors.push('Field "importance" must be a number');
    }

    // Validate scope
    const validScopes = ['global', 'foreman', 'platform', 'runtime'];
    if (entry.scope && !validScopes.includes(entry.scope)) {
      errors.push(`Invalid scope: ${entry.scope}. Must be one of: ${validScopes.join(', ')}`);
    }

    // Validate tags format
    if (entry.tags && Array.isArray(entry.tags)) {
      for (const tag of entry.tags) {
        if (typeof tag !== 'string') {
          errors.push(`Tag must be string, got: ${typeof tag}`);
        } else if (!/^[a-z0-9-_]+$/.test(tag)) {
          warnings.push(`Tag "${tag}" does not match recommended format: lowercase, alphanumeric, hyphens, underscores`);
        }
      }
    }

    // Validate importance range
    if (entry.importance !== undefined) {
      if (entry.importance < 0 || entry.importance > 100) {
        errors.push('Field "importance" must be between 0 and 100');
      }
    }

    // Validate timestamps
    if (entry.created_at && !this.isValidISODate(entry.created_at)) {
      errors.push('Field "created_at" must be a valid ISO 8601 date string');
    }

    if (entry.updated_at && !this.isValidISODate(entry.updated_at)) {
      errors.push('Field "updated_at" must be a valid ISO 8601 date string');
    }

    return {
      valid: errors.length === 0,
      errors,
      warnings
    };
  }

  /**
   * Validate multiple entries
   */
  public validateBatch(entries: any[]): ValidationResult {
    const allErrors: string[] = [];
    const allWarnings: string[] = [];

    for (let i = 0; i < entries.length; i++) {
      const result = this.validate(entries[i]);
      
      if (!result.valid) {
        allErrors.push(`Entry ${i}: ${result.errors.join(', ')}`);
      }
      
      if (result.warnings.length > 0) {
        allWarnings.push(`Entry ${i}: ${result.warnings.join(', ')}`);
      }
    }

    return {
      valid: allErrors.length === 0,
      errors: allErrors,
      warnings: allWarnings
    };
  }

  /**
   * Check if string is valid ISO 8601 date
   */
  private isValidISODate(dateString: string): boolean {
    const date = new Date(dateString);
    return !isNaN(date.getTime()) && dateString === date.toISOString();
  }
}
