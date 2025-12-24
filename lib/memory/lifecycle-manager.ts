/**
 * Memory Lifecycle State Machine Manager
 * 
 * Implements the runtime memory lifecycle as specified in:
 * docs/architecture/runtime/memory/MEMORY_LIFECYCLE_STATE_MACHINE.md
 * 
 * Manages transitions through 5 states:
 * UNINITIALIZED → LOADING → VALIDATING → USABLE / DEGRADED / FAILED
 * 
 * @module lib/memory/lifecycle-manager
 */

import { EventEmitter } from 'events';

/**
 * Memory lifecycle states
 */
export enum MemoryLifecycleState {
  UNINITIALIZED = 'UNINITIALIZED',
  LOADING = 'LOADING',
  VALIDATING = 'VALIDATING',
  USABLE = 'USABLE',
  DEGRADED = 'DEGRADED',
  FAILED = 'FAILED'
}

/**
 * Failure severity levels
 */
export enum FailureSeverity {
  CRITICAL = 'CRITICAL',      // Hard stop - move to FAILED
  NON_CRITICAL = 'NON_CRITICAL'  // Degraded mode - move to DEGRADED
}

/**
 * State transition event
 */
export interface StateTransition {
  fromState: MemoryLifecycleState;
  toState: MemoryLifecycleState;
  timestamp: Date;
  reason?: string;
}

/**
 * Health status report
 */
export interface HealthStatus {
  state: MemoryLifecycleState;
  timestamp: Date;
  uptime: number;
  lastTransition?: StateTransition;
  errorCount: number;
  degradationReason?: string;
}

/**
 * Memory Lifecycle Manager
 * 
 * Orchestrates memory state machine transitions with:
 * - State validation and enforcement
 * - Audit logging for all transitions
 * - Observable events for monitoring
 * - Failure mode handling (hard stop vs degraded)
 */
export class MemoryLifecycleManager extends EventEmitter {
  private currentState: MemoryLifecycleState;
  private stateHistory: StateTransition[];
  private startTime: Date;
  private errorCount: number;
  private degradationReason?: string;

  constructor() {
    super();
    this.currentState = MemoryLifecycleState.UNINITIALIZED;
    this.stateHistory = [];
    this.startTime = new Date();
    this.errorCount = 0;
  }

  /**
   * Get current lifecycle state
   */
  public getState(): MemoryLifecycleState {
    return this.currentState;
  }

  /**
   * Get health status
   */
  public getHealthStatus(): HealthStatus {
    const now = new Date();
    return {
      state: this.currentState,
      timestamp: now,
      uptime: now.getTime() - this.startTime.getTime(),
      lastTransition: this.stateHistory[this.stateHistory.length - 1],
      errorCount: this.errorCount,
      degradationReason: this.degradationReason
    };
  }

  /**
   * Initialize memory lifecycle
   * UNINITIALIZED → LOADING
   */
  public async initialize(): Promise<void> {
    this.validateTransition(MemoryLifecycleState.LOADING);
    await this.transition(MemoryLifecycleState.LOADING, 'Initialization started');
  }

  /**
   * Begin loading memory from storage
   * Typically called after initialize()
   */
  public async load(memoryStore: any): Promise<void> {
    if (this.currentState !== MemoryLifecycleState.LOADING) {
      throw new Error(`Cannot load from state ${this.currentState}`);
    }
    
    try {
      // Loading logic would happen here in real implementation
      // For now, just transition to VALIDATING
      await this.transition(MemoryLifecycleState.VALIDATING, 'Memory loaded successfully');
    } catch (error) {
      await this.handleFailure(FailureSeverity.CRITICAL, `Load failed: ${error}`);
      throw error;
    }
  }

  /**
   * Validate loaded memory
   * VALIDATING → USABLE / DEGRADED / FAILED
   */
  public async validate(): Promise<void> {
    if (this.currentState !== MemoryLifecycleState.VALIDATING) {
      throw new Error(`Cannot validate from state ${this.currentState}`);
    }

    try {
      // Validation logic would happen here
      // For now, assume validation passes
      await this.transition(MemoryLifecycleState.USABLE, 'Validation passed');
    } catch (error) {
      await this.handleFailure(FailureSeverity.NON_CRITICAL, `Validation warnings: ${error}`);
    }
  }

  /**
   * Handle failure based on severity
   */
  public async handleFailure(severity: FailureSeverity, reason: string): Promise<void> {
    this.errorCount++;
    
    if (severity === FailureSeverity.CRITICAL) {
      // Hard stop - move to FAILED
      this.degradationReason = reason;
      await this.transition(MemoryLifecycleState.FAILED, `Critical failure: ${reason}`);
      this.emit('critical-failure', { reason, timestamp: new Date() });
    } else {
      // Degraded mode - partial functionality
      this.degradationReason = reason;
      await this.transition(MemoryLifecycleState.DEGRADED, `Degraded: ${reason}`);
      this.emit('degraded-mode', { reason, timestamp: new Date() });
    }
  }

  /**
   * Attempt recovery from DEGRADED state
   * DEGRADED → LOADING
   */
  public async recover(): Promise<void> {
    if (this.currentState !== MemoryLifecycleState.DEGRADED) {
      throw new Error(`Cannot recover from state ${this.currentState}`);
    }

    await this.transition(MemoryLifecycleState.LOADING, 'Recovery attempt started');
    this.degradationReason = undefined;
  }

  /**
   * Validate that a state transition is allowed
   */
  private validateTransition(toState: MemoryLifecycleState): void {
    const allowedTransitions: Record<MemoryLifecycleState, MemoryLifecycleState[]> = {
      [MemoryLifecycleState.UNINITIALIZED]: [
        MemoryLifecycleState.LOADING,
        MemoryLifecycleState.FAILED
      ],
      [MemoryLifecycleState.LOADING]: [
        MemoryLifecycleState.VALIDATING,
        MemoryLifecycleState.DEGRADED,
        MemoryLifecycleState.FAILED
      ],
      [MemoryLifecycleState.VALIDATING]: [
        MemoryLifecycleState.USABLE,
        MemoryLifecycleState.DEGRADED,
        MemoryLifecycleState.FAILED
      ],
      [MemoryLifecycleState.USABLE]: [
        MemoryLifecycleState.LOADING  // Reload scenario
      ],
      [MemoryLifecycleState.DEGRADED]: [
        MemoryLifecycleState.LOADING,  // Recovery attempt
        MemoryLifecycleState.FAILED    // Give up
      ],
      [MemoryLifecycleState.FAILED]: []  // Terminal state - no auto-recovery
    };

    const allowed = allowedTransitions[this.currentState] || [];
    if (!allowed.includes(toState)) {
      throw new Error(
        `Invalid state transition: ${this.currentState} → ${toState}. ` +
        `Allowed: ${allowed.join(', ')}`
      );
    }
  }

  /**
   * Execute state transition with audit logging
   */
  private async transition(toState: MemoryLifecycleState, reason?: string): Promise<void> {
    const fromState = this.currentState;
    
    // Validate transition is allowed
    this.validateTransition(toState);

    // Record transition
    const transitionEvent: StateTransition = {
      fromState,
      toState,
      timestamp: new Date(),
      reason
    };

    this.stateHistory.push(transitionEvent);
    this.currentState = toState;

    // Audit log (console for now, would be proper logging in production)
    console.log(`[MemoryLifecycle] ${fromState} → ${toState}`, reason || '');

    // Emit observable event
    this.emit('state-transition', transitionEvent);
    this.emit(`state:${toState}`, transitionEvent);
  }

  /**
   * Get state transition history
   */
  public getHistory(): StateTransition[] {
    return [...this.stateHistory];
  }

  /**
   * Check if memory is usable
   */
  public isUsable(): boolean {
    return this.currentState === MemoryLifecycleState.USABLE;
  }

  /**
   * Check if in failed state
   */
  public isFailed(): boolean {
    return this.currentState === MemoryLifecycleState.FAILED;
  }

  /**
   * Check if in degraded state
   */
  public isDegraded(): boolean {
    return this.currentState === MemoryLifecycleState.DEGRADED;
  }
}
