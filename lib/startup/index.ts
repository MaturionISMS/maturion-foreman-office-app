/**
 * Startup Requirement Loader - Module Exports
 * 
 * This module provides read-only assessment of startup requirements.
 * 
 * CRITICAL: Zero execution authority, zero decision authority.
 */

export {
  loadRequirements,
  assessStartupRequirements,
  validateRequirements,
  getRequirementStatus,
  RequirementStatus,
  StartupAssessment,
  ValidationResult
} from './RequirementLoader';
