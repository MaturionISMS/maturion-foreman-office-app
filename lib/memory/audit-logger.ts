/**
 * Audit Logger
 * 
 * Immutable, append-only audit logging for memory operations.
 * Implements tamper-proof audit trail with cryptographic hash chain.
 * 
 * Features:
 * - Append-only logging (no updates or deletes)
 * - Cryptographic hash chain for tamper detection
 * - Access and write audit logging
 * - Privacy scan result logging
 * - Query filtering and pagination
 * 
 * @module lib/memory/audit-logger
 */

import * as crypto from 'crypto';
import { EventEmitter } from 'events';

/**
 * Access audit entry
 */
export interface AccessAuditEntry {
  timestamp: Date;
  actor: string;
  actorType: string;
  action: 'read_memory';
  scopesAccessed: string[];
  tagsQueried?: string[];
  importanceMin?: string;
  entriesReturned: number;
  queryLatencyMs: number;
  reason?: string;
  sessionId?: string;
  sourceIP?: string;
  authorized: boolean;
  hash?: string;
  previousHash?: string;
}

/**
 * Write audit entry
 */
export interface WriteAuditEntry {
  timestamp: Date;
  actor: string;
  action: 'write_memory';
  scope: string;
  entryId: string;
  title: string;
  importance: string;
  tags: string[];
  validationStatus: 'passed' | 'failed';
  privacyCheckStatus: 'passed' | 'failed';
  writeLatencyMs: number;
  reason?: string;
  sessionId?: string;
  sourceIP?: string;
  authorized: boolean;
  hash?: string;
  previousHash?: string;
}

/**
 * Privacy scan audit entry
 */
export interface PrivacyScanEntry {
  timestamp: Date;
  scanType: 'write_validation' | 'periodic_scan';
  scope: string;
  entryId: string;
  piiDetected: boolean;
  secretsDetected: boolean;
  tenantDataDetected: boolean;
  scanDurationMs: number;
  outcome: 'passed' | 'failed';
  violations?: string[];
  hash?: string;
  previousHash?: string;
}

/**
 * Audit query filter
 */
export interface AuditQueryFilter {
  actor?: string;
  scope?: string;
  since?: Date;
  limit?: number;
}

/**
 * Audit statistics
 */
export interface AuditStatistics {
  totalAccesses?: number;
  totalWrites?: number;
  byActor?: Record<string, number>;
  byScope?: Record<string, number>;
  unauthorizedAttempts?: number;
  avgQueryLatencyMs?: number;
  avgWriteLatencyMs?: number;
  validationFailures?: number;
  privacyViolations?: number;
}

/**
 * Audit Logger
 * 
 * Provides immutable audit trail for all memory operations:
 * - Access logging (who read what, when, why)
 * - Write logging (who wrote what, when, why)
 * - Privacy scan logging (violations detected)
 * - Cryptographic hash chain for tamper detection
 */
export class AuditLogger extends EventEmitter {
  private accessLog: AccessAuditEntry[];
  private writeLog: WriteAuditEntry[];
  private privacyLog: PrivacyScanEntry[];
  private lastAccessHash: string;
  private lastWriteHash: string;
  private lastPrivacyHash: string;

  constructor() {
    super();
    this.accessLog = [];
    this.writeLog = [];
    this.privacyLog = [];
    this.lastAccessHash = '';
    this.lastWriteHash = '';
    this.lastPrivacyHash = '';
  }

  /**
   * Log memory access
   */
  public logAccess(entry: Omit<AccessAuditEntry, 'hash' | 'previousHash'>): void {
    const auditEntry: AccessAuditEntry = {
      ...entry,
      timestamp: entry.timestamp || new Date(),
      previousHash: this.lastAccessHash
    };

    // Compute hash for tamper detection
    auditEntry.hash = this.computeHash(auditEntry);
    this.lastAccessHash = auditEntry.hash;

    // Append to log (immutable)
    this.accessLog.push(auditEntry);

    // Emit event for monitoring
    this.emit('access-logged', auditEntry);

    // Log unauthorized attempts
    if (!entry.authorized) {
      console.warn('[AuditLogger] Unauthorized access attempt:', {
        actor: entry.actor,
        scopes: entry.scopesAccessed,
        timestamp: entry.timestamp
      });
      this.emit('unauthorized-access', auditEntry);
    }
  }

  /**
   * Log memory write
   */
  public logWrite(entry: Omit<WriteAuditEntry, 'hash' | 'previousHash'>): void {
    const auditEntry: WriteAuditEntry = {
      ...entry,
      timestamp: entry.timestamp || new Date(),
      previousHash: this.lastWriteHash
    };

    // Compute hash for tamper detection
    auditEntry.hash = this.computeHash(auditEntry);
    this.lastWriteHash = auditEntry.hash;

    // Append to log (immutable)
    this.writeLog.push(auditEntry);

    // Emit event for monitoring
    this.emit('write-logged', auditEntry);

    // Log validation failures
    if (entry.validationStatus === 'failed' || entry.privacyCheckStatus === 'failed') {
      console.warn('[AuditLogger] Write validation/privacy check failed:', {
        actor: entry.actor,
        scope: entry.scope,
        entryId: entry.entryId,
        timestamp: entry.timestamp
      });
      this.emit('write-validation-failed', auditEntry);
    }
  }

  /**
   * Log privacy scan
   */
  public logPrivacyScan(entry: Omit<PrivacyScanEntry, 'hash' | 'previousHash'>): void {
    const auditEntry: PrivacyScanEntry = {
      ...entry,
      timestamp: entry.timestamp || new Date(),
      previousHash: this.lastPrivacyHash
    };

    // Compute hash for tamper detection
    auditEntry.hash = this.computeHash(auditEntry);
    this.lastPrivacyHash = auditEntry.hash;

    // Append to log (immutable)
    this.privacyLog.push(auditEntry);

    // Emit event for monitoring
    this.emit('privacy-scan-logged', auditEntry);

    // Log violations
    if (entry.outcome === 'failed') {
      console.warn('[AuditLogger] Privacy violation detected:', {
        scope: entry.scope,
        entryId: entry.entryId,
        violations: entry.violations,
        timestamp: entry.timestamp
      });
      this.emit('privacy-violation', auditEntry);
    }
  }

  /**
   * Query access audit log
   */
  public queryAccess(filter?: AuditQueryFilter): AccessAuditEntry[] {
    let results = [...this.accessLog];

    if (filter?.actor) {
      results = results.filter(entry => entry.actor === filter.actor);
    }

    if (filter?.since) {
      results = results.filter(entry => entry.timestamp >= filter.since!);
    }

    if (filter?.limit) {
      results = results.slice(-filter.limit);
    }

    return results;
  }

  /**
   * Query write audit log
   */
  public queryWrites(filter?: AuditQueryFilter): WriteAuditEntry[] {
    let results = [...this.writeLog];

    if (filter?.actor) {
      results = results.filter(entry => entry.actor === filter.actor);
    }

    if (filter?.scope) {
      results = results.filter(entry => entry.scope === filter.scope);
    }

    if (filter?.since) {
      results = results.filter(entry => entry.timestamp >= filter.since!);
    }

    if (filter?.limit) {
      results = results.slice(-filter.limit);
    }

    return results;
  }

  /**
   * Query privacy scan log
   */
  public queryPrivacyScans(filter?: AuditQueryFilter): PrivacyScanEntry[] {
    let results = [...this.privacyLog];

    if (filter?.scope) {
      results = results.filter(entry => entry.scope === filter.scope);
    }

    if (filter?.since) {
      results = results.filter(entry => entry.timestamp >= filter.since!);
    }

    if (filter?.limit) {
      results = results.slice(-filter.limit);
    }

    return results;
  }

  /**
   * Get access audit statistics
   */
  public getAccessStatistics(filter?: AuditQueryFilter): AuditStatistics {
    const entries = this.queryAccess(filter);

    const byActor: Record<string, number> = {};
    const byScope: Record<string, number> = {};
    let unauthorizedAttempts = 0;
    let totalLatency = 0;

    for (const entry of entries) {
      // Count by actor
      byActor[entry.actor] = (byActor[entry.actor] || 0) + 1;

      // Count by scope
      for (const scope of entry.scopesAccessed) {
        byScope[scope] = (byScope[scope] || 0) + 1;
      }

      // Count unauthorized
      if (!entry.authorized) {
        unauthorizedAttempts++;
      }

      // Sum latency
      totalLatency += entry.queryLatencyMs;
    }

    return {
      totalAccesses: entries.length,
      byActor,
      byScope,
      unauthorizedAttempts,
      avgQueryLatencyMs: entries.length > 0 ? totalLatency / entries.length : 0
    };
  }

  /**
   * Get write audit statistics
   */
  public getWriteStatistics(filter?: AuditQueryFilter): AuditStatistics {
    const entries = this.queryWrites(filter);

    const byScope: Record<string, number> = {};
    const byImportance: Record<string, number> = {};
    let validationFailures = 0;
    let privacyViolations = 0;
    let totalLatency = 0;

    for (const entry of entries) {
      // Count by scope
      byScope[entry.scope] = (byScope[entry.scope] || 0) + 1;

      // Count by importance
      byImportance[entry.importance] = (byImportance[entry.importance] || 0) + 1;

      // Count validation failures
      if (entry.validationStatus === 'failed') {
        validationFailures++;
      }

      // Count privacy violations
      if (entry.privacyCheckStatus === 'failed') {
        privacyViolations++;
      }

      // Sum latency
      totalLatency += entry.writeLatencyMs;
    }

    return {
      totalWrites: entries.length,
      byScope,
      validationFailures,
      privacyViolations,
      avgWriteLatencyMs: entries.length > 0 ? totalLatency / entries.length : 0
    };
  }

  /**
   * Verify audit log integrity (check hash chain)
   */
  public verifyIntegrity(): { valid: boolean; errors: string[] } {
    const errors: string[] = [];

    // Verify access log
    let expectedHash = '';
    for (const entry of this.accessLog) {
      if (entry.previousHash !== expectedHash) {
        errors.push(`Access log integrity breach at ${entry.timestamp}: hash mismatch`);
      }
      expectedHash = entry.hash!;
    }

    // Verify write log
    expectedHash = '';
    for (const entry of this.writeLog) {
      if (entry.previousHash !== expectedHash) {
        errors.push(`Write log integrity breach at ${entry.timestamp}: hash mismatch`);
      }
      expectedHash = entry.hash!;
    }

    // Verify privacy log
    expectedHash = '';
    for (const entry of this.privacyLog) {
      if (entry.previousHash !== expectedHash) {
        errors.push(`Privacy log integrity breach at ${entry.timestamp}: hash mismatch`);
      }
      expectedHash = entry.hash!;
    }

    return {
      valid: errors.length === 0,
      errors
    };
  }

  /**
   * Get total log counts
   */
  public getCounts(): { access: number; write: number; privacy: number } {
    return {
      access: this.accessLog.length,
      write: this.writeLog.length,
      privacy: this.privacyLog.length
    };
  }

  /**
   * Compute cryptographic hash of entry
   */
  private computeHash(entry: any): string {
    const data = JSON.stringify({
      ...entry,
      hash: undefined,
      previousHash: entry.previousHash || ''
    });
    return crypto.createHash('sha256').update(data).digest('hex');
  }

  /**
   * Clear logs (for testing only - violates immutability in production)
   */
  public clearLogs(): void {
    console.warn('[AuditLogger] Clearing audit logs - should only be used in testing');
    this.accessLog = [];
    this.writeLog = [];
    this.privacyLog = [];
    this.lastAccessHash = '';
    this.lastWriteHash = '';
    this.lastPrivacyHash = '';
  }
}
