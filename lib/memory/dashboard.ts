/**
 * Dashboard Data Structures
 * 
 * Provides dashboard-specific data structures for:
 * - Foreman Memory Status Panel
 * - Watchdog Memory Health Monitor
 * - Johan Complete Memory Oversight
 * 
 * Based on:
 * docs/architecture/runtime/observability/MEMORY_OBSERVABILITY_ARCHITECTURE.md
 * Section 5: Dashboard Views
 * 
 * @module lib/memory/dashboard
 */

import { MemoryLifecycleState } from './lifecycle-manager';
import { AccessAuditEntry, WriteAuditEntry } from './audit-logger';

/**
 * Alert severity levels
 */
export type AlertSeverity = 'info' | 'warning' | 'error' | 'critical';

/**
 * Dashboard alert
 */
export interface DashboardAlert {
  severity: AlertSeverity;
  message: string;
  timestamp: Date;
  actionable: boolean;
  actionLabel?: string;
  actionLink?: string;
}

/**
 * Foreman Dashboard - Memory Status Panel
 * 
 * Purpose: Enable Foreman to ensure memory is ready before accepting builds.
 * 
 * Display Information:
 * - Current memory state (USABLE, DEGRADED, FAILED)
 * - State duration (how long in current state)
 * - Last state transition (when, from, to, reason)
 * - Scope availability (which scopes are available)
 * - Recent agent memory accesses (last 10)
 * - Validation status (last validation outcome)
 * - Privacy compliance status (any violations detected)
 */
export interface ForemanMemoryPanel {
  // Current State
  currentState: MemoryLifecycleState;
  stateDurationSec: number;
  stateIndicator: '✅' | '⚠️' | '🚨';
  stateMessage: string;

  // Last Transition
  lastTransition?: {
    from: MemoryLifecycleState;
    to: MemoryLifecycleState;
    at: Date;
    reason?: string;
    timeSinceTransitionSec: number;
  };

  // Scope Availability
  scopeAvailability: {
    global: boolean;
    foreman: boolean;
    platform: boolean;
    runtime: boolean;
    experience: boolean;
  };
  unavailableScopes: string[];

  // Recent Access (last 10)
  recentAccesses: Array<{
    timestamp: Date;
    actor: string;
    scopesAccessed: string[];
    entriesReturned: number;
    reason?: string;
  }>;

  // Validation Status
  validationStatus: {
    lastValidation: Date;
    outcome: 'passed' | 'failed' | 'pending';
    errors: number;
    warnings: number;
  };

  // Privacy Compliance
  privacyCompliance: {
    status: 'compliant' | 'violations_detected';
    violations: number;
    lastScan: Date;
  };

  // Alerts
  alerts: DashboardAlert[];

  // Available Actions
  actions: Array<{
    label: string;
    action: 'revalidate' | 'view_health' | 'view_audit';
    enabled: boolean;
  }>;

  // Refresh Metadata
  lastRefresh: Date;
  nextRefresh: Date;
}

/**
 * Watchdog Dashboard - Memory Health Monitor
 * 
 * Purpose: Enable Watchdog to monitor memory fabric health during runtime.
 * 
 * Display Information:
 * - Real-time memory state (with state transition timeline)
 * - Performance metrics (load time, query latency, cache hit rate)
 * - Access patterns (queries per minute, writes per minute)
 * - Privacy compliance status (scan results, violations)
 * - State transition history (last 24 hours)
 * - Anomaly alerts (unexpected state transitions, performance degradation)
 */
export interface WatchdogMemoryMonitor {
  // Real-time State
  currentState: MemoryLifecycleState;
  stateTimeline: Array<{
    state: MemoryLifecycleState;
    enteredAt: Date;
    exitedAt?: Date;
    durationSec: number;
  }>;

  // Performance Metrics
  performance: {
    loadTimeSec: number;
    validationTimeSec: number;
    avgQueryLatencyMs: number;
    p95QueryLatencyMs: number;
    p99QueryLatencyMs: number;
    cacheHitRate: number;
    threshold: {
      loadTimeSec: number;
      validationTimeSec: number;
      avgQueryLatencyMs: number;
      cacheHitRate: number;
    };
    breached: string[];
  };

  // Access Patterns
  accessPatterns: {
    queriesPerMinute: number;
    writesPerMinute: number;
    topActors: Array<{
      actor: string;
      accesses: number;
      percentage: number;
    }>;
    topScopes: Array<{
      scope: string;
      accesses: number;
      percentage: number;
    }>;
  };

  // Privacy Compliance
  privacyCompliance: {
    totalScans: number;
    violations: number;
    complianceRate: number;
    recentViolations: Array<{
      timestamp: Date;
      scope: string;
      entryId: string;
      violationType: string;
    }>;
  };

  // State Transition History (last 24h)
  transitionHistory: Array<{
    timestamp: Date;
    from: MemoryLifecycleState;
    to: MemoryLifecycleState;
    reason?: string;
  }>;

  // Anomaly Alerts
  anomalies: Array<{
    type: 'excessive_transitions' | 'slow_performance' | 'privacy_violation' | 'unauthorized_access';
    severity: AlertSeverity;
    message: string;
    timestamp: Date;
    details?: any;
  }>;

  // Charts/Graphs Data
  charts: {
    queryLatencyTrend: Array<{ timestamp: Date; latencyMs: number }>;
    accessHeatmap: Record<string, number>;
    errorRateTrend: Array<{ timestamp: Date; errorRate: number }>;
  };

  // Actions
  actions: Array<{
    label: string;
    action: 'trigger_recovery' | 'view_audit' | 'export_report';
    enabled: boolean;
  }>;

  // Refresh Metadata
  lastRefresh: Date;
  nextRefresh: Date;
}

/**
 * Johan Dashboard - Complete Memory Oversight
 * 
 * Purpose: Provide Johan with full visibility into memory fabric state and governance.
 * 
 * Display Information:
 * - All information from Foreman and Watchdog dashboards
 * - Full audit trail (all actors, all scopes, all time)
 * - Write history (who wrote what, when, why)
 * - Privacy compliance report (detailed scan results)
 * - CHP proposal audit (proposals generated, approved, rejected)
 * - Agent access patterns (which agents access memory most frequently)
 * - Governance enforcement status (compliance with memory behavior rules)
 */
export interface JohanMemoryOversight {
  // Include Foreman Panel
  foremanPanel: ForemanMemoryPanel;

  // Include Watchdog Monitor
  watchdogMonitor: WatchdogMemoryMonitor;

  // Full Audit Trail
  auditTrail: {
    totalAccesses: number;
    totalWrites: number;
    totalScans: number;
    dateRange: { from: Date; to: Date };
    
    // Access breakdown
    accessesByActor: Record<string, number>;
    accessesByScope: Record<string, number>;
    unauthorizedAttempts: number;
    
    // Write breakdown
    writesByActor: Record<string, number>;
    writesByScope: Record<string, number>;
    writesByImportance: Record<string, number>;
    
    // Recent activity
    recentAccesses: AccessAuditEntry[];
    recentWrites: WriteAuditEntry[];
  };

  // CHP Proposal Audit
  chpProposals: {
    total: number;
    pending: number;
    approved: number;
    rejected: number;
    recentProposals: Array<{
      timestamp: Date;
      proposalId: string;
      severity: string;
      status: 'pending' | 'approved' | 'rejected';
      title: string;
    }>;
  };

  // Agent Access Patterns
  agentPatterns: {
    mostActiveAgents: Array<{
      actor: string;
      actorType: string;
      totalAccesses: number;
      scopesAccessed: string[];
      avgQueryLatencyMs: number;
    }>;
    accessFrequency: Record<string, number>;
  };

  // Governance Enforcement
  governanceStatus: {
    memoryBehaviorCompliance: boolean;
    privacyGuardrailCompliance: boolean;
    violations: Array<{
      timestamp: Date;
      type: string;
      actor: string;
      details: string;
    }>;
    complianceRate: number;
  };

  // Advanced Queries Available
  availableQueries: Array<{
    name: string;
    description: string;
    parameters: string[];
  }>;

  // Actions
  actions: Array<{
    label: string;
    action: 'manual_repair' | 'forensic_audit' | 'generate_compliance_report' | 'view_query_interface';
    enabled: boolean;
    requiresConfirmation: boolean;
  }>;

  // Refresh Metadata
  lastRefresh: Date;
  nextRefresh: Date;
}

/**
 * Dashboard data builder
 * 
 * Utility class to build dashboard data structures from observability service
 */
export class DashboardDataBuilder {
  /**
   * Build Foreman memory panel
   */
  static buildForemanPanel(health: any, auditData: any): ForemanMemoryPanel {
    const currentState = health.state as MemoryLifecycleState;
    
    // Determine state indicator
    let stateIndicator: '✅' | '⚠️' | '🚨' = '✅';
    let stateMessage = 'Memory USABLE: All scopes available';
    
    if (currentState === MemoryLifecycleState.DEGRADED) {
      stateIndicator = '⚠️';
      stateMessage = `Memory DEGRADED: ${health.degradations[0] || 'Unknown reason'}`;
    } else if (currentState === MemoryLifecycleState.FAILED) {
      stateIndicator = '🚨';
      stateMessage = 'Memory FAILED: Critical state';
    }

    // Build scope availability
    const scopeAvailability = {
      global: health.scopes.global?.status === 'available',
      foreman: health.scopes.foreman?.status === 'available',
      platform: health.scopes.platform?.status === 'available',
      runtime: health.scopes.runtime?.status === 'available',
      experience: health.scopes.experience?.status === 'available'
    };

    const unavailableScopes = Object.entries(scopeAvailability)
      .filter(([_, available]) => !available)
      .map(([scope, _]) => scope);

    // Map recent accesses
    const recentAccesses = (auditData.accesses || []).slice(-10).map((access: AccessAuditEntry) => ({
      timestamp: access.timestamp,
      actor: access.actor,
      scopesAccessed: access.scopesAccessed,
      entriesReturned: access.entriesReturned,
      reason: access.reason
    }));

    // Build alerts
    const alerts: DashboardAlert[] = health.alerts.map((msg: string) => {
      let severity: AlertSeverity = 'info';
      if (msg.includes('⚠️')) severity = 'warning';
      if (msg.includes('🚨')) severity = 'critical';
      if (msg.includes('✅')) severity = 'info';

      return {
        severity,
        message: msg,
        timestamp: health.timestamp,
        actionable: severity !== 'info'
      };
    });

    return {
      currentState,
      stateDurationSec: health.stateDurationSec,
      stateIndicator,
      stateMessage,
      lastTransition: health.lastTransition ? {
        from: health.lastTransition.from,
        to: health.lastTransition.to,
        at: health.lastTransition.at,
        reason: health.lastTransition.reason,
        timeSinceTransitionSec: Math.floor((Date.now() - new Date(health.lastTransition.at).getTime()) / 1000)
      } : undefined,
      scopeAvailability,
      unavailableScopes,
      recentAccesses,
      validationStatus: {
        lastValidation: health.timestamp,
        outcome: health.metrics.validationErrors === 0 ? 'passed' : 'failed',
        errors: health.metrics.validationErrors,
        warnings: health.metrics.validationWarnings
      },
      privacyCompliance: {
        status: health.metrics.privacyViolations === 0 ? 'compliant' : 'violations_detected',
        violations: health.metrics.privacyViolations,
        lastScan: health.timestamp
      },
      alerts,
      actions: [
        { label: '🔄 Re-validate Memory', action: 'revalidate', enabled: true },
        { label: '🔍 View Full Health Report', action: 'view_health', enabled: true },
        { label: '📊 View Access Audit', action: 'view_audit', enabled: true }
      ],
      lastRefresh: health.timestamp,
      nextRefresh: new Date(Date.now() + 5000) // 5 seconds
    };
  }

  /**
   * Build Watchdog memory monitor
   */
  static buildWatchdogMonitor(health: any, history: any, performance: any): WatchdogMemoryMonitor {
    // Build state timeline
    const stateTimeline = history.transitions.map((t: any, idx: number) => ({
      state: t.toState,
      enteredAt: t.timestamp,
      exitedAt: history.transitions[idx + 1]?.timestamp,
      durationSec: t.durationInPreviousStateSec
    }));

    // Performance thresholds
    const thresholds = {
      loadTimeSec: 30,
      validationTimeSec: 60,
      avgQueryLatencyMs: 200,
      cacheHitRate: 0.85
    };

    const breached: string[] = [];
    if (health.metrics.loadTimeSec > thresholds.loadTimeSec) breached.push('load time');
    if (health.metrics.validationTimeSec > thresholds.validationTimeSec) breached.push('validation time');
    if (health.metrics.avgQueryLatencyMs > thresholds.avgQueryLatencyMs) breached.push('query latency');
    if (health.metrics.cacheHitRate < thresholds.cacheHitRate) breached.push('cache hit rate');

    return {
      currentState: health.state,
      stateTimeline,
      performance: {
        loadTimeSec: health.metrics.loadTimeSec,
        validationTimeSec: health.metrics.validationTimeSec,
        avgQueryLatencyMs: health.metrics.avgQueryLatencyMs,
        p95QueryLatencyMs: 150, // TODO: Track actual percentiles
        p99QueryLatencyMs: 200,
        cacheHitRate: health.metrics.cacheHitRate,
        threshold: thresholds,
        breached
      },
      accessPatterns: {
        queriesPerMinute: 12, // TODO: Calculate from audit log
        writesPerMinute: 0.5,
        topActors: [],
        topScopes: []
      },
      privacyCompliance: {
        totalScans: 0,
        violations: health.metrics.privacyViolations,
        complianceRate: 1.0,
        recentViolations: []
      },
      transitionHistory: history.transitions,
      anomalies: [],
      charts: {
        queryLatencyTrend: [],
        accessHeatmap: {},
        errorRateTrend: []
      },
      actions: [
        { label: '🔄 Trigger Recovery', action: 'trigger_recovery', enabled: health.state === MemoryLifecycleState.DEGRADED },
        { label: '🔍 View Audit Trail', action: 'view_audit', enabled: true },
        { label: '📊 Export Report', action: 'export_report', enabled: true }
      ],
      lastRefresh: health.timestamp,
      nextRefresh: new Date(Date.now() + 5000)
    };
  }

  /**
   * Build Johan memory oversight
   */
  static buildJohanOversight(
    foremanPanel: ForemanMemoryPanel,
    watchdogMonitor: WatchdogMemoryMonitor,
    auditData: any
  ): JohanMemoryOversight {
    return {
      foremanPanel,
      watchdogMonitor,
      auditTrail: {
        totalAccesses: auditData.statistics.totalAccesses,
        totalWrites: 0, // TODO: Add write statistics
        totalScans: 0,
        dateRange: { from: new Date(0), to: new Date() },
        accessesByActor: auditData.statistics.byActor,
        accessesByScope: auditData.statistics.byScope,
        unauthorizedAttempts: auditData.statistics.unauthorizedAttempts,
        writesByActor: {},
        writesByScope: {},
        writesByImportance: {},
        recentAccesses: auditData.accesses.slice(-10),
        recentWrites: []
      },
      chpProposals: {
        total: 0,
        pending: 0,
        approved: 0,
        rejected: 0,
        recentProposals: []
      },
      agentPatterns: {
        mostActiveAgents: [],
        accessFrequency: {}
      },
      governanceStatus: {
        memoryBehaviorCompliance: true,
        privacyGuardrailCompliance: auditData.statistics.unauthorizedAttempts === 0,
        violations: [],
        complianceRate: 1.0
      },
      availableQueries: [
        {
          name: 'Memory Accesses by Actor',
          description: 'Show all memory accesses by a specific actor',
          parameters: ['actor', 'since', 'limit']
        },
        {
          name: 'Memory Writes by Scope',
          description: 'Show all memory writes to a specific scope',
          parameters: ['scope', 'since', 'limit']
        },
        {
          name: 'Privacy Violations',
          description: 'Show all privacy violations detected',
          parameters: ['since', 'limit']
        }
      ],
      actions: [
        { label: '🔧 Manual Repair', action: 'manual_repair', enabled: false, requiresConfirmation: true },
        { label: '🔍 Forensic Audit Mode', action: 'forensic_audit', enabled: true, requiresConfirmation: true },
        { label: '📋 Generate Compliance Report', action: 'generate_compliance_report', enabled: true, requiresConfirmation: false },
        { label: '🔎 View Query Interface', action: 'view_query_interface', enabled: true, requiresConfirmation: false }
      ],
      lastRefresh: new Date(),
      nextRefresh: new Date(Date.now() + 5000)
    };
  }
}
