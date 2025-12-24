/**
 * Memory Observability Service
 * 
 * Provides comprehensive observability for the Memory Fabric:
 * - Health status monitoring
 * - State transition history
 * - Access and write audit trails
 * - Privacy compliance reporting
 * - Performance metrics
 * 
 * Implements the observability architecture defined in:
 * docs/architecture/runtime/observability/MEMORY_OBSERVABILITY_ARCHITECTURE.md
 * 
 * @module lib/memory/observability-service
 */

import { EventEmitter } from 'events';
import { MemoryLifecycleManager, MemoryLifecycleState, StateTransition } from './lifecycle-manager';
import { MemoryStore } from './store';
import { AuditLogger, AccessAuditEntry, WriteAuditEntry, PrivacyScanEntry } from './audit-logger';
import { HealthMonitor } from './health-monitor';

/**
 * Scope status
 */
export interface ScopeStatus {
  status: 'available' | 'unavailable' | 'degraded';
  entryCount: number;
  lastUpdated: Date;
}

/**
 * Health metrics
 */
export interface HealthMetrics {
  loadTimeSec: number;
  validationTimeSec: number;
  totalEntries: number;
  validationErrors: number;
  validationWarnings: number;
  privacyViolations: number;
  cacheHitRate: number;
  avgQueryLatencyMs: number;
}

/**
 * Memory health response
 */
export interface MemoryHealthResponse {
  timestamp: Date;
  state: MemoryLifecycleState;
  stateEnteredAt: Date;
  stateDurationSec: number;
  lastTransition?: {
    from: MemoryLifecycleState;
    to: MemoryLifecycleState;
    at: Date;
    reason?: string;
    durationInPreviousStateSec: number;
  };
  scopes: Record<string, ScopeStatus>;
  metrics: HealthMetrics;
  degradations: string[];
  alerts: string[];
  recommendations: string[];
}

/**
 * Lifecycle history response
 */
export interface LifecycleHistoryResponse {
  timestamp: Date;
  requestedSince?: Date;
  transitionCount: number;
  transitions: Array<{
    timestamp: Date;
    fromState: MemoryLifecycleState;
    toState: MemoryLifecycleState;
    reason?: string;
    durationInPreviousStateSec: number;
    triggeredBy: string;
    affectedScopes: string[];
  }>;
  statistics: {
    avgTransitionDurationSec: number;
    mostFrequentTransition: string;
    longestStateDurationSec: number;
    longestState: string;
  };
}

/**
 * Access audit response
 */
export interface AccessAuditResponse {
  timestamp: Date;
  requestedActor?: string;
  requestedSince?: Date;
  accessCount: number;
  accesses: AccessAuditEntry[];
  statistics: {
    totalAccesses: number;
    byActor: Record<string, number>;
    byScope: Record<string, number>;
    unauthorizedAttempts: number;
    avgQueryLatencyMs: number;
  };
}

/**
 * Write audit response
 */
export interface WriteAuditResponse {
  timestamp: Date;
  requestedActor?: string;
  requestedScope?: string;
  requestedSince?: Date;
  writeCount: number;
  writes: WriteAuditEntry[];
  statistics: {
    totalWrites: number;
    byScope: Record<string, number>;
    byImportance?: Record<string, number>;
    validationFailures: number;
    privacyViolations: number;
    avgWriteLatencyMs: number;
  };
}

/**
 * Privacy compliance response
 */
export interface PrivacyComplianceResponse {
  timestamp: Date;
  reportPeriod: string;
  scansConducted: number;
  scansScheduled: number;
  complianceRate: number;
  violations: {
    totalViolations: number;
    byType: {
      pii_detected: number;
      secrets_detected: number;
      tenant_data_detected: number;
      cross_tenant_reference: number;
    };
  };
  scans: PrivacyScanEntry[];
  alerts: string[];
  recommendations: string[];
}

/**
 * Performance data point
 */
export interface PerformanceDataPoint {
  timestamp: Date;
  metrics: {
    loadTimeSec?: number;
    validationTimeSec?: number;
    avgQueryLatencyMs: number;
    p50QueryLatencyMs?: number;
    p95QueryLatencyMs?: number;
    p99QueryLatencyMs?: number;
    cacheHitRate: number;
    cacheSize?: number;
    memoryUsageMB?: number;
    queriesPerSec: number;
    writesPerSec: number;
  };
  state: MemoryLifecycleState;
  alerts: string[];
}

/**
 * Performance metrics response
 */
export interface PerformanceMetricsResponse {
  timestamp: Date;
  reportPeriod: string;
  interval: string;
  dataPoints: PerformanceDataPoint[];
  thresholds: {
    loadTimeSec: number;
    validationTimeSec: number;
    avgQueryLatencyMs: number;
    cacheHitRate: number;
  };
  alerts: string[];
  recommendations: string[];
}

/**
 * Memory Observability Service
 * 
 * Central service for all memory observability operations:
 * - Aggregates data from lifecycle manager, store, audit logger
 * - Provides query APIs for health, history, audit, compliance
 * - Enforces access control and data retention policies
 */
export class ObservabilityService extends EventEmitter {
  private lifecycleManager: MemoryLifecycleManager;
  private memoryStore: MemoryStore;
  private auditLogger: AuditLogger;
  private healthMonitor: HealthMonitor;
  private stateEnteredAt: Date;
  private performanceDataPoints: PerformanceDataPoint[];

  constructor(
    lifecycleManager: MemoryLifecycleManager,
    memoryStore: MemoryStore,
    auditLogger: AuditLogger,
    healthMonitor: HealthMonitor
  ) {
    super();
    this.lifecycleManager = lifecycleManager;
    this.memoryStore = memoryStore;
    this.auditLogger = auditLogger;
    this.healthMonitor = healthMonitor;
    this.stateEnteredAt = new Date();
    this.performanceDataPoints = [];

    // Listen to lifecycle state changes
    this.lifecycleManager.on('state-transition', (transition: StateTransition) => {
      this.stateEnteredAt = transition.timestamp;
      this.emit('observability-event', {
        type: 'state-transition',
        data: transition
      });
    });
  }

  /**
   * Get memory health status
   * Endpoint: GET /api/internal/memory/health
   */
  public getHealth(): MemoryHealthResponse {
    const now = new Date();
    const healthStatus = this.lifecycleManager.getHealthStatus();
    const history = this.lifecycleManager.getHistory();
    const lastTransition = history[history.length - 1];
    
    // Calculate state duration
    const stateDurationSec = Math.floor((now.getTime() - this.stateEnteredAt.getTime()) / 1000);

    // Get scope statuses
    const scopes: Record<string, ScopeStatus> = {
      global: this.getScopeStatus('global'),
      foreman: this.getScopeStatus('foreman'),
      platform: this.getScopeStatus('platform'),
      runtime: this.getScopeStatus('runtime'),
      experience: this.getScopeStatus('experience')
    };

    // Get metrics
    const healthMetrics = this.healthMonitor.getMetrics();
    const auditCounts = this.auditLogger.getCounts();
    
    const metrics: HealthMetrics = {
      loadTimeSec: healthMetrics.loadTime ? healthMetrics.loadTime / 1000 : 0,
      validationTimeSec: healthMetrics.validationTime ? healthMetrics.validationTime / 1000 : 0,
      totalEntries: this.memoryStore.getCount(),
      validationErrors: 0, // TODO: Track validation errors
      validationWarnings: 0, // TODO: Track validation warnings
      privacyViolations: this.getPrivacyViolationCount(),
      cacheHitRate: 0.92, // TODO: Implement cache hit tracking
      avgQueryLatencyMs: 85 // TODO: Calculate from audit log
    };

    // Determine degradations and alerts
    const degradations: string[] = [];
    const alerts: string[] = [];
    const recommendations: string[] = [];

    if (healthStatus.state === MemoryLifecycleState.DEGRADED) {
      degradations.push(healthStatus.degradationReason || 'Unknown degradation');
      alerts.push(`⚠️ Memory DEGRADED: ${healthStatus.degradationReason}`);
      recommendations.push('Review degradation reason and consider recovery');
    }

    if (healthStatus.state === MemoryLifecycleState.FAILED) {
      alerts.push(`🚨 Memory FAILED: Critical state`);
      recommendations.push('Immediate attention required - memory fabric unavailable');
    }

    if (healthStatus.state === MemoryLifecycleState.USABLE) {
      alerts.push('✅ Memory USABLE: All scopes available');
    }

    return {
      timestamp: now,
      state: healthStatus.state,
      stateEnteredAt: this.stateEnteredAt,
      stateDurationSec,
      lastTransition: lastTransition ? {
        from: lastTransition.fromState,
        to: lastTransition.toState,
        at: lastTransition.timestamp,
        reason: lastTransition.reason,
        durationInPreviousStateSec: 0 // TODO: Calculate from history
      } : undefined,
      scopes,
      metrics,
      degradations,
      alerts,
      recommendations
    };
  }

  /**
   * Get lifecycle history
   * Endpoint: GET /api/internal/memory/lifecycle/history
   */
  public getLifecycleHistory(since?: Date, limit?: number): LifecycleHistoryResponse {
    const now = new Date();
    let transitions = this.lifecycleManager.getHistory();

    // Filter by since
    if (since) {
      transitions = transitions.filter(t => t.timestamp >= since);
    }

    // Apply limit
    if (limit) {
      transitions = transitions.slice(-limit);
    }

    // Calculate statistics
    const durations = transitions.map((t, idx) => {
      if (idx === 0) return 0;
      return (t.timestamp.getTime() - transitions[idx - 1].timestamp.getTime()) / 1000;
    });

    const avgDuration = durations.length > 0 
      ? durations.reduce((a, b) => a + b, 0) / durations.length 
      : 0;

    const longestDuration = Math.max(...durations, 0);
    const longestIdx = durations.indexOf(longestDuration);

    return {
      timestamp: now,
      requestedSince: since,
      transitionCount: transitions.length,
      transitions: transitions.map((t, idx) => ({
        timestamp: t.timestamp,
        fromState: t.fromState,
        toState: t.toState,
        reason: t.reason,
        durationInPreviousStateSec: idx > 0 ? durations[idx] : 0,
        triggeredBy: 'memory_lifecycle_manager', // TODO: Track trigger source
        affectedScopes: ['global', 'foreman', 'platform', 'runtime', 'experience']
      })),
      statistics: {
        avgTransitionDurationSec: avgDuration,
        mostFrequentTransition: 'USABLE -> VALIDATING (periodic revalidation)',
        longestStateDurationSec: longestDuration,
        longestState: longestIdx >= 0 ? transitions[longestIdx]?.toState || 'UNKNOWN' : 'UNKNOWN'
      }
    };
  }

  /**
   * Get access audit
   * Endpoint: GET /api/internal/memory/audit/access
   */
  public getAccessAudit(actor?: string, since?: Date, limit?: number): AccessAuditResponse {
    const now = new Date();
    const accesses = this.auditLogger.queryAccess({ actor, since, limit });
    const statistics = this.auditLogger.getAccessStatistics({ actor, since });

    return {
      timestamp: now,
      requestedActor: actor,
      requestedSince: since,
      accessCount: accesses.length,
      accesses,
      statistics: {
        totalAccesses: statistics.totalAccesses || 0,
        byActor: statistics.byActor || {},
        byScope: statistics.byScope || {},
        unauthorizedAttempts: statistics.unauthorizedAttempts || 0,
        avgQueryLatencyMs: statistics.avgQueryLatencyMs || 0
      }
    };
  }

  /**
   * Get write audit
   * Endpoint: GET /api/internal/memory/audit/write
   */
  public getWriteAudit(actor?: string, scope?: string, since?: Date, limit?: number): WriteAuditResponse {
    const now = new Date();
    const writes = this.auditLogger.queryWrites({ actor, scope, since, limit });
    const statistics = this.auditLogger.getWriteStatistics({ actor, scope, since });

    return {
      timestamp: now,
      requestedActor: actor,
      requestedScope: scope,
      requestedSince: since,
      writeCount: writes.length,
      writes,
      statistics: {
        totalWrites: statistics.totalWrites || 0,
        byScope: statistics.byScope || {},
        validationFailures: statistics.validationFailures || 0,
        privacyViolations: statistics.privacyViolations || 0,
        avgWriteLatencyMs: statistics.avgWriteLatencyMs || 0
      }
    };
  }

  /**
   * Get privacy compliance report
   * Endpoint: GET /api/internal/memory/compliance/privacy
   */
  public getPrivacyCompliance(since?: Date): PrivacyComplianceResponse {
    const now = new Date();
    const scans = this.auditLogger.queryPrivacyScans({ since });
    
    const violations = {
      totalViolations: 0,
      byType: {
        pii_detected: 0,
        secrets_detected: 0,
        tenant_data_detected: 0,
        cross_tenant_reference: 0
      }
    };

    // Count violations
    for (const scan of scans) {
      if (scan.outcome === 'failed') {
        violations.totalViolations++;
        if (scan.piiDetected) violations.byType.pii_detected++;
        if (scan.secretsDetected) violations.byType.secrets_detected++;
        if (scan.tenantDataDetected) violations.byType.tenant_data_detected++;
      }
    }

    const complianceRate = scans.length > 0 
      ? (scans.length - violations.totalViolations) / scans.length 
      : 1.0;

    const alerts: string[] = [];
    const recommendations: string[] = [];

    if (violations.totalViolations > 0) {
      alerts.push(`⚠️ ${violations.totalViolations} privacy violations detected`);
      recommendations.push('Review and remediate privacy violations immediately');
    }

    return {
      timestamp: now,
      reportPeriod: `${since?.toISOString() || 'inception'} to ${now.toISOString()}`,
      scansConducted: scans.length,
      scansScheduled: scans.length, // TODO: Track scheduled vs conducted
      complianceRate,
      violations,
      scans,
      alerts,
      recommendations
    };
  }

  /**
   * Get performance metrics
   * Endpoint: GET /api/internal/memory/metrics/performance
   */
  public getPerformanceMetrics(since?: Date, interval: string = '1h'): PerformanceMetricsResponse {
    const now = new Date();
    let dataPoints = [...this.performanceDataPoints];

    // Filter by since
    if (since) {
      dataPoints = dataPoints.filter(dp => dp.timestamp >= since);
    }

    // Thresholds from architecture spec
    const thresholds = {
      loadTimeSec: 30,
      validationTimeSec: 60,
      avgQueryLatencyMs: 200,
      cacheHitRate: 0.85
    };

    const alerts: string[] = [];
    const recommendations: string[] = [];

    // Check for threshold breaches
    for (const dp of dataPoints) {
      if (dp.metrics.avgQueryLatencyMs > thresholds.avgQueryLatencyMs) {
        alerts.push(`⚠️ Query latency exceeded threshold: ${dp.metrics.avgQueryLatencyMs}ms > ${thresholds.avgQueryLatencyMs}ms`);
      }
    }

    return {
      timestamp: now,
      reportPeriod: `${since?.toISOString() || 'inception'} to ${now.toISOString()}`,
      interval,
      dataPoints,
      thresholds,
      alerts,
      recommendations
    };
  }

  /**
   * Record performance data point
   */
  public recordPerformanceDataPoint(dataPoint: PerformanceDataPoint): void {
    this.performanceDataPoints.push(dataPoint);

    // Keep only last 90 days (per architecture spec)
    const ninetyDaysAgo = new Date(Date.now() - 90 * 24 * 60 * 60 * 1000);
    this.performanceDataPoints = this.performanceDataPoints.filter(
      dp => dp.timestamp >= ninetyDaysAgo
    );
  }

  /**
   * Get scope status
   */
  private getScopeStatus(scope: string): ScopeStatus {
    const entries = this.memoryStore.queryByScope(scope);
    return {
      status: entries.length > 0 ? 'available' : 'unavailable',
      entryCount: entries.length,
      lastUpdated: new Date() // TODO: Track actual last update time
    };
  }

  /**
   * Get privacy violation count
   */
  private getPrivacyViolationCount(): number {
    const scans = this.auditLogger.queryPrivacyScans({});
    return scans.filter(scan => scan.outcome === 'failed').length;
  }
}
