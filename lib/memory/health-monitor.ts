/**
 * Health Monitor
 * 
 * Monitors memory lifecycle health with metrics tracking,
 * anomaly detection, and alerting.
 * 
 * @module lib/memory/health-monitor
 */

import { EventEmitter } from 'events';
import { MemoryLifecycleState, StateTransition } from './lifecycle-manager';

/**
 * Health metrics
 */
export interface HealthMetrics {
  stateTransitions: number;
  loadTime?: number;
  validationTime?: number;
  errorRate: number;
  lastError?: Date;
  uptime: number;
}

/**
 * Anomaly detection thresholds
 */
export interface AnomalyThresholds {
  maxLoadTime: number;        // milliseconds
  maxValidationTime: number;  // milliseconds
  maxErrorRate: number;       // percentage (0-100)
  maxTransitions: number;     // transitions per minute
}

/**
 * Health alert
 */
export interface HealthAlert {
  type: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  message: string;
  timestamp: Date;
  metrics?: Partial<HealthMetrics>;
}

/**
 * Health Monitor
 * 
 * Tracks memory lifecycle health with:
 * - State transition monitoring
 * - Load and validation time tracking
 * - Error rate monitoring
 * - Anomaly detection and alerting
 */
export class HealthMonitor extends EventEmitter {
  private metrics: HealthMetrics;
  private thresholds: AnomalyThresholds;
  private startTime: Date;
  private transitionTimes: Date[];

  constructor(thresholds?: Partial<AnomalyThresholds>) {
    super();
    
    this.metrics = {
      stateTransitions: 0,
      errorRate: 0,
      uptime: 0
    };

    this.thresholds = {
      maxLoadTime: 30000,        // 30 seconds
      maxValidationTime: 10000,  // 10 seconds
      maxErrorRate: 5,           // 5%
      maxTransitions: 10,        // 10 per minute
      ...thresholds
    };

    this.startTime = new Date();
    this.transitionTimes = [];
  }

  /**
   * Record state transition
   */
  public recordTransition(transition: StateTransition): void {
    this.metrics.stateTransitions++;
    this.transitionTimes.push(transition.timestamp);

    // Keep only last minute of transitions
    const oneMinuteAgo = new Date(Date.now() - 60000);
    this.transitionTimes = this.transitionTimes.filter(t => t > oneMinuteAgo);

    // Check for excessive transitions
    if (this.transitionTimes.length > this.thresholds.maxTransitions) {
      this.alert({
        type: 'excessive_transitions',
        severity: 'MEDIUM',
        message: `Excessive state transitions: ${this.transitionTimes.length} in last minute`,
        timestamp: new Date(),
        metrics: { stateTransitions: this.metrics.stateTransitions }
      });
    }
  }

  /**
   * Record load time
   */
  public recordLoadTime(milliseconds: number): void {
    this.metrics.loadTime = milliseconds;

    if (milliseconds > this.thresholds.maxLoadTime) {
      this.alert({
        type: 'slow_load',
        severity: 'HIGH',
        message: `Memory load time exceeded threshold: ${milliseconds}ms > ${this.thresholds.maxLoadTime}ms`,
        timestamp: new Date(),
        metrics: { loadTime: milliseconds }
      });
    }
  }

  /**
   * Record validation time
   */
  public recordValidationTime(milliseconds: number): void {
    this.metrics.validationTime = milliseconds;

    if (milliseconds > this.thresholds.maxValidationTime) {
      this.alert({
        type: 'slow_validation',
        severity: 'MEDIUM',
        message: `Memory validation time exceeded threshold: ${milliseconds}ms > ${this.thresholds.maxValidationTime}ms`,
        timestamp: new Date(),
        metrics: { validationTime: milliseconds }
      });
    }
  }

  /**
   * Record error
   */
  public recordError(): void {
    this.metrics.lastError = new Date();
    
    // Calculate error rate (simplified)
    const totalOperations = this.metrics.stateTransitions;
    if (totalOperations > 0) {
      // This is a simplified calculation
      this.metrics.errorRate = (1 / totalOperations) * 100;
    }

    if (this.metrics.errorRate > this.thresholds.maxErrorRate) {
      this.alert({
        type: 'high_error_rate',
        severity: 'CRITICAL',
        message: `Error rate exceeded threshold: ${this.metrics.errorRate.toFixed(2)}% > ${this.thresholds.maxErrorRate}%`,
        timestamp: new Date(),
        metrics: { errorRate: this.metrics.errorRate }
      });
    }
  }

  /**
   * Get current metrics
   */
  public getMetrics(): HealthMetrics {
    const now = new Date();
    this.metrics.uptime = now.getTime() - this.startTime.getTime();
    return { ...this.metrics };
  }

  /**
   * Reset metrics
   */
  public reset(): void {
    this.metrics = {
      stateTransitions: 0,
      errorRate: 0,
      uptime: 0
    };
    this.transitionTimes = [];
    this.startTime = new Date();
  }

  /**
   * Emit health alert
   */
  private alert(alert: HealthAlert): void {
    console.warn(`[HealthMonitor] ${alert.severity}: ${alert.message}`);
    this.emit('alert', alert);
    this.emit(`alert:${alert.severity}`, alert);
  }

  /**
   * Check overall health status
   */
  public getHealthStatus(): 'HEALTHY' | 'DEGRADED' | 'UNHEALTHY' {
    const metrics = this.getMetrics();

    // Check for critical conditions
    if (metrics.errorRate > this.thresholds.maxErrorRate * 2) {
      return 'UNHEALTHY';
    }

    if (metrics.loadTime && metrics.loadTime > this.thresholds.maxLoadTime * 2) {
      return 'UNHEALTHY';
    }

    // Check for degraded conditions
    if (metrics.errorRate > this.thresholds.maxErrorRate) {
      return 'DEGRADED';
    }

    if (metrics.loadTime && metrics.loadTime > this.thresholds.maxLoadTime) {
      return 'DEGRADED';
    }

    if (this.transitionTimes.length > this.thresholds.maxTransitions) {
      return 'DEGRADED';
    }

    return 'HEALTHY';
  }
}
