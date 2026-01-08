/**
 * Startup Requirement Loader
 * 
 * CRITICAL: This module has ZERO decision authority and ZERO execution capability.
 * It is a READ-ONLY assessment tool that surfaces validation results.
 * 
 * Purpose:
 * - Load startup requirements from startup-requirements.json
 * - Validate requirements against the system state
 * - Surface validation results for consumption by commissioning system
 * - Provide read-only assessment of startup readiness
 * 
 * What This Module DOES NOT Do:
 * - Does NOT make decisions about system behavior
 * - Does NOT execute any system changes
 * - Does NOT grant or deny access
 * - Does NOT modify system state
 * - Does NOT have authority over routing or access control
 * - Does NOT activate any system components
 * - Does NOT trigger execution of any kind
 * 
 * Authority: Issue F-A2 - Batch 2 Memory & Commissioning Foundations
 */

import * as fs from 'fs';
import * as path from 'path';

/**
 * Requirement validation status
 */
export interface RequirementStatus {
  id: string;
  name: string;
  passed: boolean;
  critical: boolean;
  message: string;
}

/**
 * Startup requirement definition
 */
export interface StartupRequirement {
  id: string;
  name: string;
  category: string;
  type: string;
  check: string;
  validator: string;
  critical: boolean;
  description: string;
}

/**
 * Overall assessment result
 */
export interface StartupAssessment {
  ready: boolean;
  overallStatus: 'READY' | 'DEGRADED' | 'BLOCKED' | 'NOT_READY';
  timestamp: string;
  requirements: RequirementStatus[];
  passed: number;
  failed: number;
  criticalFailed: number;
  criticalFailures: number;
  totalRequirements: number;
  blockers: string[];
  warnings: string[];
}

/**
 * Alias for StartupAssessment for compatibility
 */
export type ValidationResult = StartupAssessment;

/**
 * Requirements configuration
 */
interface RequirementsConfig {
  version: string;
  requirements: StartupRequirement[];
}

/**
 * Load startup requirements from JSON file
 * 
 * READ-ONLY: This function only reads configuration, makes no system changes
 */
export function loadRequirements(): RequirementsConfig {
  const requirementsPath = path.join(__dirname, 'startup-requirements.json');
  const content = fs.readFileSync(requirementsPath, 'utf-8');
  return JSON.parse(content) as RequirementsConfig;
}

/**
 * Validate a single requirement
 * 
 * READ-ONLY: This function only checks state, makes no system changes
 */
function validateRequirement(requirement: StartupRequirement): RequirementStatus {
  let passed = false;
  let message = '';

  // READ-ONLY checks based on requirement type
  switch (requirement.type) {
    case 'memory':
      // Check if memory fabric exists (read-only)
      passed = fs.existsSync(path.join(process.cwd(), 'memory'));
      message = passed 
        ? 'Memory fabric directory exists' 
        : 'Memory fabric directory not found';
      break;

    case 'file':
      // Check if required files exist (read-only)
      if (requirement.check === 'governance-directory-exists') {
        passed = fs.existsSync(path.join(process.cwd(), 'governance'));
        message = passed
          ? 'Governance directory exists'
          : 'Governance directory not found';
      } else if (requirement.check === 'architecture-index-exists') {
        passed = fs.existsSync(path.join(process.cwd(), 'ARCHITECTURE_INDEX.json'));
        message = passed
          ? 'Architecture index exists'
          : 'Architecture index not found';
      }
      break;

    case 'config':
      // Check configuration validity (read-only)
      passed = fs.existsSync(path.join(process.cwd(), 'lib', 'commissioning'));
      message = passed
        ? 'Commissioning configuration directory exists'
        : 'Commissioning configuration not found';
      break;

    default:
      passed = false;
      message = `Unknown requirement type: ${requirement.type}`;
  }

  return {
    id: requirement.id,
    name: requirement.name,
    passed,
    critical: requirement.critical,
    message
  };
}

/**
 * Assess all startup requirements
 * 
 * READ-ONLY: This function only assesses state, makes no system changes
 * 
 * Returns an assessment object with validation results
 */
export function assessStartupRequirements(): StartupAssessment {
  const config = loadRequirements();
  const results: RequirementStatus[] = [];
  let criticalFailures = 0;
  let passed = 0;
  let failed = 0;
  const blockers: string[] = [];
  const warnings: string[] = [];

  for (const requirement of config.requirements) {
    const status = validateRequirement(requirement);
    results.push(status);

    if (status.passed) {
      passed++;
    } else {
      failed++;
      if (status.critical) {
        criticalFailures++;
        blockers.push(`${requirement.id}: ${status.message}`);
      } else {
        warnings.push(`${requirement.id}: ${status.message}`);
      }
    }
  }

  const ready = criticalFailures === 0;
  let overallStatus: 'READY' | 'DEGRADED' | 'BLOCKED' | 'NOT_READY';
  
  if (criticalFailures > 0) {
    overallStatus = 'BLOCKED';
  } else if (failed > 0) {
    overallStatus = 'DEGRADED';
  } else {
    overallStatus = 'READY';
  }

  return {
    ready,
    overallStatus,
    timestamp: new Date().toISOString(),
    requirements: results,
    passed,
    failed,
    criticalFailed: criticalFailures,
    criticalFailures,
    totalRequirements: config.requirements.length,
    blockers,
    warnings
  };
}

/**
 * Alias for assessStartupRequirements for compatibility
 * 
 * READ-ONLY: This function only assesses state, makes no system changes
 */
export function validateRequirements(): ValidationResult {
  return assessStartupRequirements();
}

/**
 * Get requirement validation results for a specific requirement ID
 * 
 * READ-ONLY: Returns validation state without modifying anything
 */
export function getRequirementStatus(requirementId: string): RequirementStatus | null {
  const assessment = assessStartupRequirements();
  return assessment.requirements.find(r => r.id === requirementId) || null;
}

/**
 * Get all failing requirements
 * 
 * READ-ONLY: Returns list of failed requirements without modifying anything
 */
export function getFailingRequirements(): RequirementStatus[] {
  const assessment = assessStartupRequirements();
  return assessment.requirements.filter(r => !r.passed);
}

/**
 * Get critical blockers that prevent system startup
 * 
 * READ-ONLY: Returns list of critical failures without modifying anything
 */
export function getCriticalBlockers(): RequirementStatus[] {
  const assessment = assessStartupRequirements();
  return assessment.requirements.filter(r => !r.passed && r.critical);
}

/**
 * Generate a human-readable readiness report
 * 
 * READ-ONLY: Returns formatted report without modifying anything
 */
export function generateReadinessReport(): string {
  const assessment = assessStartupRequirements();
  
  let report = '=== Startup Readiness Report ===\n\n';
  report += `Status: ${assessment.overallStatus}\n`;
  report += `Timestamp: ${assessment.timestamp}\n`;
  report += `Total Requirements: ${assessment.totalRequirements}\n`;
  report += `Passed: ${assessment.passed}\n`;
  report += `Failed: ${assessment.failed}\n`;
  report += `Critical Failures: ${assessment.criticalFailed}\n\n`;
  
  if (assessment.blockers.length > 0) {
    report += '--- Critical Blockers ---\n';
    assessment.blockers.forEach(blocker => {
      report += `  ❌ ${blocker}\n`;
    });
    report += '\n';
  }
  
  if (assessment.warnings.length > 0) {
    report += '--- Warnings ---\n';
    assessment.warnings.forEach(warning => {
      report += `  ⚠️  ${warning}\n`;
    });
    report += '\n';
  }
  
  if (assessment.ready) {
    report += '✅ System is READY for startup\n';
  } else {
    report += '❌ System is NOT READY for startup\n';
  }
  
  return report;
}
