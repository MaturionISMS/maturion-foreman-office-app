/**
 * Memory Module Exports
 * 
 * Exports all memory-related components:
 * - Lifecycle Manager
 * - Memory Store
 * - Schema Validator
 * - Privacy Checker
 * - Health Monitor
 * - Memory Client
 * 
 * @module lib/memory
 */

// Lifecycle Manager
export {
  MemoryLifecycleManager,
  MemoryLifecycleState,
  FailureSeverity,
  StateTransition,
  HealthStatus
} from './lifecycle-manager';

// Memory Store
export {
  MemoryStore,
  MemoryEntry
} from './store';

// Schema Validator
export {
  SchemaValidator,
  ValidationResult
} from './schema-validator';

// Privacy Checker
export {
  PrivacyChecker,
  ViolationSeverity,
  PrivacyViolation,
  PrivacyCheckResult
} from './privacy-checker';

// Health Monitor
export {
  HealthMonitor,
  HealthMetrics,
  AnomalyThresholds,
  HealthAlert
} from './health-monitor';

// Memory Client (existing)
export { MemoryClient } from './client';
