/**
 * Memory Observability Integration
 * 
 * Factory and integration utilities for wiring together the memory observability stack:
 * - Lifecycle Manager
 * - Memory Store
 * - Audit Logger
 * - Health Monitor
 * - Observability Service
 * - Dashboard Data Builder
 * 
 * Provides a simple API to initialize and use the complete observability system.
 * 
 * @module lib/memory/observability-integration
 */

import { MemoryLifecycleManager, MemoryLifecycleState } from './lifecycle-manager';
import { MemoryStore } from './store';
import { AuditLogger } from './audit-logger';
import { HealthMonitor } from './health-monitor';
import { ObservabilityService } from './observability-service';
import { DashboardDataBuilder, ForemanMemoryPanel, WatchdogMemoryMonitor, JohanMemoryOversight } from './dashboard';

/**
 * Observability configuration
 */
export interface ObservabilityConfig {
  memoryRoot?: string;
  enableAuditLogging?: boolean;
  enableHealthMonitoring?: boolean;
  enableDashboards?: boolean;
}

/**
 * Memory Observability Integration
 * 
 * Central integration point for the complete observability stack.
 * Wires together all components and provides a unified API.
 */
export class MemoryObservabilityIntegration {
  private lifecycleManager: MemoryLifecycleManager;
  private memoryStore: MemoryStore;
  private auditLogger: AuditLogger;
  private healthMonitor: HealthMonitor;
  private observabilityService: ObservabilityService;
  private config: Required<ObservabilityConfig>;

  constructor(config?: ObservabilityConfig) {
    this.config = {
      memoryRoot: config?.memoryRoot || './memory',
      enableAuditLogging: config?.enableAuditLogging !== false,
      enableHealthMonitoring: config?.enableHealthMonitoring !== false,
      enableDashboards: config?.enableDashboards !== false
    };

    // Initialize components
    this.lifecycleManager = new MemoryLifecycleManager();
    this.memoryStore = new MemoryStore(this.config.memoryRoot);
    this.auditLogger = new AuditLogger();
    this.healthMonitor = new HealthMonitor();

    // Wire up lifecycle events to health monitor
    this.lifecycleManager.on('state-transition', (transition) => {
      this.healthMonitor.recordTransition(transition);
    });

    // Wire up audit events to health monitor
    if (this.config.enableAuditLogging) {
      this.auditLogger.on('unauthorized-access', () => {
        this.healthMonitor.recordError();
      });

      this.auditLogger.on('write-validation-failed', () => {
        this.healthMonitor.recordError();
      });

      this.auditLogger.on('privacy-violation', () => {
        this.healthMonitor.recordError();
      });
    }

    // Create observability service
    this.observabilityService = new ObservabilityService(
      this.lifecycleManager,
      this.memoryStore,
      this.auditLogger,
      this.healthMonitor
    );

    // Wire up memory client to audit logger
    this.setupMemoryClientAuditing();
  }

  /**
   * Initialize the observability system
   */
  async initialize(): Promise<void> {
    // Initialize lifecycle manager
    await this.lifecycleManager.initialize();

    // Load memory store
    await this.lifecycleManager.load(this.memoryStore);

    // Validate memory
    await this.lifecycleManager.validate();

    // Record initial performance data point
    const health = this.observabilityService.getHealth();
    this.observabilityService.recordPerformanceDataPoint({
      timestamp: new Date(),
      metrics: {
        avgQueryLatencyMs: health.metrics.avgQueryLatencyMs,
        cacheHitRate: health.metrics.cacheHitRate,
        queriesPerSec: 0,
        writesPerSec: 0
      },
      state: health.state,
      alerts: health.alerts
    });
  }

  /**
   * Setup memory client auditing
   * 
   * Wraps memory client methods to log access
   */
  private setupMemoryClientAuditing(): void {
    if (!this.config.enableAuditLogging) {
      return;
    }

    // Note: This is a placeholder for actual integration
    // In practice, memory client would need to emit events
    // or accept an audit logger as a dependency
  }

  /**
   * Get memory health status
   * Endpoint: GET /api/internal/memory/health
   */
  getHealth() {
    return this.observabilityService.getHealth();
  }

  /**
   * Get lifecycle history
   * Endpoint: GET /api/internal/memory/lifecycle/history
   */
  getLifecycleHistory(since?: Date, limit?: number) {
    return this.observabilityService.getLifecycleHistory(since, limit);
  }

  /**
   * Get access audit
   * Endpoint: GET /api/internal/memory/audit/access
   */
  getAccessAudit(actor?: string, since?: Date, limit?: number) {
    return this.observabilityService.getAccessAudit(actor, since, limit);
  }

  /**
   * Get write audit
   * Endpoint: GET /api/internal/memory/audit/write
   */
  getWriteAudit(actor?: string, scope?: string, since?: Date, limit?: number) {
    return this.observabilityService.getWriteAudit(actor, scope, since, limit);
  }

  /**
   * Get privacy compliance report
   * Endpoint: GET /api/internal/memory/compliance/privacy
   */
  getPrivacyCompliance(since?: Date) {
    return this.observabilityService.getPrivacyCompliance(since);
  }

  /**
   * Get performance metrics
   * Endpoint: GET /api/internal/memory/metrics/performance
   */
  getPerformanceMetrics(since?: Date, interval?: string) {
    return this.observabilityService.getPerformanceMetrics(since, interval);
  }

  /**
   * Log memory access
   */
  logAccess(
    actor: string,
    actorType: string,
    scopesAccessed: string[],
    entriesReturned: number,
    queryLatencyMs: number,
    options?: {
      tagsQueried?: string[];
      importanceMin?: string;
      reason?: string;
      sessionId?: string;
      sourceIP?: string;
      authorized?: boolean;
    }
  ): void {
    if (!this.config.enableAuditLogging) {
      return;
    }

    this.auditLogger.logAccess({
      timestamp: new Date(),
      actor,
      actorType,
      action: 'read_memory',
      scopesAccessed,
      tagsQueried: options?.tagsQueried,
      importanceMin: options?.importanceMin,
      entriesReturned,
      queryLatencyMs,
      reason: options?.reason,
      sessionId: options?.sessionId,
      sourceIP: options?.sourceIP,
      authorized: options?.authorized !== false
    });
  }

  /**
   * Log memory write
   */
  logWrite(
    actor: string,
    scope: string,
    entryId: string,
    title: string,
    importance: string,
    tags: string[],
    validationStatus: 'passed' | 'failed',
    privacyCheckStatus: 'passed' | 'failed',
    writeLatencyMs: number,
    options?: {
      reason?: string;
      sessionId?: string;
      sourceIP?: string;
      authorized?: boolean;
    }
  ): void {
    if (!this.config.enableAuditLogging) {
      return;
    }

    this.auditLogger.logWrite({
      timestamp: new Date(),
      actor,
      action: 'write_memory',
      scope,
      entryId,
      title,
      importance,
      tags,
      validationStatus,
      privacyCheckStatus,
      writeLatencyMs,
      reason: options?.reason,
      sessionId: options?.sessionId,
      sourceIP: options?.sourceIP,
      authorized: options?.authorized !== false
    });
  }

  /**
   * Log privacy scan
   */
  logPrivacyScan(
    scanType: 'write_validation' | 'periodic_scan',
    scope: string,
    entryId: string,
    piiDetected: boolean,
    secretsDetected: boolean,
    tenantDataDetected: boolean,
    scanDurationMs: number,
    outcome: 'passed' | 'failed',
    violations?: string[]
  ): void {
    if (!this.config.enableAuditLogging) {
      return;
    }

    this.auditLogger.logPrivacyScan({
      timestamp: new Date(),
      scanType,
      scope,
      entryId,
      piiDetected,
      secretsDetected,
      tenantDataDetected,
      scanDurationMs,
      outcome,
      violations
    });
  }

  /**
   * Get Foreman dashboard panel
   */
  getForemanPanel(): ForemanMemoryPanel {
    if (!this.config.enableDashboards) {
      throw new Error('Dashboards are disabled');
    }

    const health = this.observabilityService.getHealth();
    const auditData = this.observabilityService.getAccessAudit(undefined, undefined, 10);

    return DashboardDataBuilder.buildForemanPanel(health, auditData);
  }

  /**
   * Get Watchdog dashboard monitor
   */
  getWatchdogMonitor(): WatchdogMemoryMonitor {
    if (!this.config.enableDashboards) {
      throw new Error('Dashboards are disabled');
    }

    const health = this.observabilityService.getHealth();
    const history = this.observabilityService.getLifecycleHistory();
    const performance = this.observabilityService.getPerformanceMetrics();

    return DashboardDataBuilder.buildWatchdogMonitor(health, history, performance);
  }

  /**
   * Get Johan dashboard oversight
   */
  getJohanOversight(): JohanMemoryOversight {
    if (!this.config.enableDashboards) {
      throw new Error('Dashboards are disabled');
    }

    const foremanPanel = this.getForemanPanel();
    const watchdogMonitor = this.getWatchdogMonitor();
    const auditData = this.observabilityService.getAccessAudit();

    return DashboardDataBuilder.buildJohanOversight(foremanPanel, watchdogMonitor, auditData);
  }

  /**
   * Get current memory state
   */
  getMemoryState(): MemoryLifecycleState {
    return this.lifecycleManager.getState();
  }

  /**
   * Check if memory is usable
   */
  isMemoryUsable(): boolean {
    return this.lifecycleManager.isUsable();
  }

  /**
   * Check if memory is degraded
   */
  isMemoryDegraded(): boolean {
    return this.lifecycleManager.isDegraded();
  }

  /**
   * Check if memory has failed
   */
  isMemoryFailed(): boolean {
    return this.lifecycleManager.isFailed();
  }

  /**
   * Get lifecycle manager (for advanced usage)
   */
  getLifecycleManager(): MemoryLifecycleManager {
    return this.lifecycleManager;
  }

  /**
   * Get memory store (for advanced usage)
   */
  getMemoryStore(): MemoryStore {
    return this.memoryStore;
  }

  /**
   * Get audit logger (for advanced usage)
   */
  getAuditLogger(): AuditLogger {
    return this.auditLogger;
  }

  /**
   * Get health monitor (for advanced usage)
   */
  getHealthMonitor(): HealthMonitor {
    return this.healthMonitor;
  }

  /**
   * Get observability service (for advanced usage)
   */
  getObservabilityService(): ObservabilityService {
    return this.observabilityService;
  }
}

/**
 * Create and initialize memory observability integration
 * 
 * This is the primary entry point for using the observability system.
 * 
 * @param config - Optional configuration
 * @returns Initialized integration
 */
export async function createMemoryObservability(
  config?: ObservabilityConfig
): Promise<MemoryObservabilityIntegration> {
  const integration = new MemoryObservabilityIntegration(config);
  await integration.initialize();
  return integration;
}
