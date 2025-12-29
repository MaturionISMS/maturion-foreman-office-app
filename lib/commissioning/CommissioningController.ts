/**
 * Maturion Foreman - Commissioning Controller
 * 
 * Governs whether the Foreman application may operate.
 * The app MUST NOT function unless commissioning state >= COMMISSIONED.
 * 
 * This is an architecture-only implementation providing:
 * - Activation state persistence (read-only initially)
 * - State validation and access control logic
 * - Routing guards for unauthorized access
 * 
 * NO UI, NO automation triggers, NO memory activation (per F-A1 constraints)
 * 
 * @module lib/commissioning
 */

import fs from 'fs/promises';
import path from 'path';
import { EventEmitter } from 'events';

/**
 * Commissioning states
 * 
 * The application lifecycle progression:
 * NOT_COMMISSIONED → COMMISSIONING → COMMISSIONED → ACTIVE → SUSPENDED
 */
export enum CommissioningState {
  /**
   * Initial state - app has never been commissioned
   * No operations are permitted
   */
  NOT_COMMISSIONED = 'NOT_COMMISSIONED',
  
  /**
   * Commissioning in progress
   * Only commissioning operations are permitted
   */
  COMMISSIONING = 'COMMISSIONING',
  
  /**
   * Commissioned but not yet active
   * Basic operations permitted, full functionality requires ACTIVE
   */
  COMMISSIONED = 'COMMISSIONED',
  
  /**
   * Fully active and operational
   * All operations permitted
   */
  ACTIVE = 'ACTIVE',
  
  /**
   * Temporarily suspended
   * Only read operations and status checks permitted
   */
  SUSPENDED = 'SUSPENDED'
}

/**
 * Commissioning state persistence structure
 */
export interface CommissioningRecord {
  state: CommissioningState;
  commissioned_at?: string;
  commissioned_by?: string;
  last_updated: string;
  version: string;
  metadata?: {
    reason?: string;
    notes?: string;
    [key: string]: any;
  };
}

/**
 * State transition event
 */
export interface StateTransitionEvent {
  fromState: CommissioningState;
  toState: CommissioningState;
  timestamp: Date;
  reason?: string;
}

/**
 * Access check result
 */
export interface AccessCheckResult {
  allowed: boolean;
  currentState: CommissioningState;
  requiredState: CommissioningState;
  message: string;
}

/**
 * Commissioning Controller
 * 
 * Manages application commissioning state and enforces access control.
 * 
 * Core responsibilities:
 * - Load and persist commissioning state
 * - Validate state transitions
 * - Enforce operational boundaries
 * - Route unauthorized access to commissioning flow
 */
export class CommissioningController extends EventEmitter {
  private currentState: CommissioningState;
  private stateFilePath: string;
  private stateHistory: StateTransitionEvent[];
  private initialized: boolean;

  /**
   * Create a new Commissioning Controller
   * 
   * @param stateFilePath - Path to commissioning state persistence file
   */
  constructor(stateFilePath?: string) {
    super();
    
    // Default to runtime/commissioning/state.json
    this.stateFilePath = stateFilePath || path.join(
      process.cwd(),
      'runtime',
      'commissioning',
      'state.json'
    );
    
    this.currentState = CommissioningState.NOT_COMMISSIONED;
    this.stateHistory = [];
    this.initialized = false;
  }

  /**
   * Initialize the controller by loading persisted state
   * 
   * @throws Error if initialization fails
   */
  public async initialize(): Promise<void> {
    if (this.initialized) {
      return;
    }

    try {
      const record = await this.loadState();
      this.currentState = record.state;
      this.initialized = true;
      
      this.emit('initialized', {
        state: this.currentState,
        timestamp: new Date()
      });
    } catch (error) {
      // If state file doesn't exist, remain in NOT_COMMISSIONED
      if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
        this.currentState = CommissioningState.NOT_COMMISSIONED;
        this.initialized = true;
        
        this.emit('initialized', {
          state: this.currentState,
          timestamp: new Date()
        });
      } else {
        throw new Error(`Failed to initialize commissioning controller: ${error}`);
      }
    }
  }

  /**
   * Get current commissioning state
   * 
   * @returns Current state
   * @throws Error if controller not initialized
   */
  public getState(): CommissioningState {
    if (!this.initialized) {
      throw new Error('CommissioningController not initialized. Call initialize() first.');
    }
    return this.currentState;
  }

  /**
   * Check if the application is commissioned (state >= COMMISSIONED)
   * 
   * @returns True if commissioned or beyond
   */
  public isCommissioned(): boolean {
    if (!this.initialized) {
      return false;
    }

    return this.currentState !== CommissioningState.NOT_COMMISSIONED &&
           this.currentState !== CommissioningState.COMMISSIONING;
  }

  /**
   * Check if the application is fully operational (state >= ACTIVE)
   * 
   * @returns True if active
   */
  public isOperational(): boolean {
    if (!this.initialized) {
      return false;
    }

    return this.currentState === CommissioningState.ACTIVE;
  }

  /**
   * Check if a specific operation is allowed in current state
   * 
   * @param requiredState - Minimum state required for the operation
   * @returns Access check result with details
   */
  public checkAccess(requiredState: CommissioningState): AccessCheckResult {
    if (!this.initialized) {
      return {
        allowed: false,
        currentState: this.currentState,
        requiredState,
        message: 'Controller not initialized'
      };
    }

    const stateOrder = [
      CommissioningState.NOT_COMMISSIONED,
      CommissioningState.COMMISSIONING,
      CommissioningState.COMMISSIONED,
      CommissioningState.ACTIVE,
      CommissioningState.SUSPENDED
    ];

    const currentIndex = stateOrder.indexOf(this.currentState);
    const requiredIndex = stateOrder.indexOf(requiredState);

    // SUSPENDED is a special case - only certain operations allowed
    if (this.currentState === CommissioningState.SUSPENDED) {
      const allowed = requiredState === CommissioningState.NOT_COMMISSIONED || 
                     requiredState === CommissioningState.COMMISSIONING;
      
      return {
        allowed,
        currentState: this.currentState,
        requiredState,
        message: allowed 
          ? 'Access granted - operation permitted in SUSPENDED state'
          : 'Access denied - application is suspended'
      };
    }

    const allowed = currentIndex >= requiredIndex;

    return {
      allowed,
      currentState: this.currentState,
      requiredState,
      message: allowed
        ? 'Access granted'
        : `Access denied - requires ${requiredState}, currently ${this.currentState}`
    };
  }

  /**
   * Validate if an operation should proceed based on commissioning state
   * 
   * @param requiredState - Minimum state required
   * @throws Error if access is denied
   */
  public validateAccess(requiredState: CommissioningState): void {
    const result = this.checkAccess(requiredState);
    
    if (!result.allowed) {
      throw new Error(
        `Operation not permitted: ${result.message}. ` +
        `Please complete commissioning process.`
      );
    }
  }

  /**
   * Get the commissioning flow route for current state
   * 
   * Used to redirect unauthorized access to appropriate commissioning page
   * 
   * @returns Route path for commissioning flow
   */
  public getCommissioningRoute(): string {
    switch (this.currentState) {
      case CommissioningState.NOT_COMMISSIONED:
        return '/commissioning/welcome';
      
      case CommissioningState.COMMISSIONING:
        return '/commissioning/setup';
      
      case CommissioningState.SUSPENDED:
        return '/commissioning/suspended';
      
      default:
        return '/commissioning/status';
    }
  }

  /**
   * Load commissioning state from persistence
   * 
   * @returns Commissioning record
   * @throws Error if file cannot be read or parsed
   */
  private async loadState(): Promise<CommissioningRecord> {
    const fileContent = await fs.readFile(this.stateFilePath, 'utf-8');
    const record = JSON.parse(fileContent) as CommissioningRecord;
    
    // Validate record structure
    if (!record.state || !Object.values(CommissioningState).includes(record.state)) {
      throw new Error('Invalid commissioning state in persistence file');
    }
    
    return record;
  }

  /**
   * Get state transition history
   * 
   * @returns Array of state transitions
   */
  public getStateHistory(): StateTransitionEvent[] {
    return [...this.stateHistory];
  }

  /**
   * Get full status report
   * 
   * @returns Detailed status information
   */
  public getStatus(): {
    initialized: boolean;
    currentState: CommissioningState;
    isCommissioned: boolean;
    isOperational: boolean;
    stateFilePath: string;
    transitionCount: number;
  } {
    return {
      initialized: this.initialized,
      currentState: this.currentState,
      isCommissioned: this.isCommissioned(),
      isOperational: this.isOperational(),
      stateFilePath: this.stateFilePath,
      transitionCount: this.stateHistory.length
    };
  }
}

/**
 * Singleton instance for application-wide use
 * 
 * Usage:
 * ```typescript
 * import { commissioningController } from '@/lib/commissioning/CommissioningController';
 * 
 * await commissioningController.initialize();
 * 
 * if (!commissioningController.isCommissioned()) {
 *   // Redirect to commissioning flow
 *   router.push(commissioningController.getCommissioningRoute());
 * }
 * ```
 */
export const commissioningController = new CommissioningController();
