/**
 * Privacy Checker
 * 
 * Scans memory entries for PII, secrets, and privacy violations.
 * Enforces tenant isolation and escalates violations.
 * 
 * @module lib/memory/privacy-checker
 */

/**
 * Privacy violation severity
 */
export enum ViolationSeverity {
  CRITICAL = 'CRITICAL',    // Definite secret/PII
  HIGH = 'HIGH',            // Probable PII
  MEDIUM = 'MEDIUM',        // Possible PII
  LOW = 'LOW'               // Suspicious pattern
}

/**
 * Privacy violation
 */
export interface PrivacyViolation {
  type: string;
  severity: ViolationSeverity;
  field: string;
  value: string;
  reason: string;
}

/**
 * Privacy check result
 */
export interface PrivacyCheckResult {
  passed: boolean;
  violations: PrivacyViolation[];
}

/**
 * Privacy Checker
 * 
 * Detects privacy and security issues with:
 * - PII detection (emails, phones, SSNs, credit cards)
 * - Secrets detection (API keys, tokens, passwords)
 * - Tenant isolation validation
 * - Violation reporting with escalation
 */
export class PrivacyChecker {
  private patterns: Map<string, RegExp>;

  constructor() {
    this.patterns = new Map([
      ['email', /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g],
      ['phone', /\b(\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b/g],
      ['ssn', /\b\d{3}-\d{2}-\d{4}\b/g],
      ['credit_card', /\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b/g],
      ['api_key', /\b(api[_-]?key|apikey|access[_-]?token)\s*[:=]\s*['"]?([a-zA-Z0-9_-]{20,})['"]?/gi],
      ['password', /\b(password|passwd|pwd)\s*[:=]\s*['"]?([^'"\s]{6,})['"]?/gi],
      ['jwt', /\beyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\b/g],
      ['aws_key', /\bAKIA[0-9A-Z]{16}\b/g],
    ]);
  }

  /**
   * Check entry for privacy violations
   */
  public check(entry: any): PrivacyCheckResult {
    const violations: PrivacyViolation[] = [];

    // Check content field
    if (entry.content && typeof entry.content === 'string') {
      violations.push(...this.scanText(entry.content, 'content'));
    }

    // Check all string fields
    for (const [key, value] of Object.entries(entry)) {
      if (typeof value === 'string' && key !== 'content') {
        violations.push(...this.scanText(value, key));
      }
    }

    // Check for tenant isolation violations
    if (entry.scope === 'global' && this.containsTenantSpecificData(entry)) {
      violations.push({
        type: 'tenant_isolation',
        severity: ViolationSeverity.CRITICAL,
        field: 'scope',
        value: entry.scope,
        reason: 'Global scope contains tenant-specific data'
      });
    }

    return {
      passed: violations.length === 0,
      violations
    };
  }

  /**
   * Scan text for privacy violations
   */
  private scanText(text: string, field: string): PrivacyViolation[] {
    const violations: PrivacyViolation[] = [];

    for (const [type, pattern] of this.patterns) {
      const matches = text.match(pattern);
      
      if (matches && matches.length > 0) {
        const severity = this.getSeverity(type);
        
        for (const match of matches) {
          violations.push({
            type,
            severity,
            field,
            value: this.redact(match),
            reason: `Detected ${type} pattern`
          });
        }
      }
    }

    return violations;
  }

  /**
   * Get severity for violation type
   */
  private getSeverity(type: string): ViolationSeverity {
    const criticalTypes = ['api_key', 'password', 'jwt', 'aws_key'];
    const highTypes = ['ssn', 'credit_card'];
    const mediumTypes = ['email', 'phone'];

    if (criticalTypes.includes(type)) {
      return ViolationSeverity.CRITICAL;
    } else if (highTypes.includes(type)) {
      return ViolationSeverity.HIGH;
    } else if (mediumTypes.includes(type)) {
      return ViolationSeverity.MEDIUM;
    }

    return ViolationSeverity.LOW;
  }

  /**
   * Redact sensitive value for logging
   */
  private redact(value: string): string {
    if (value.length <= 8) {
      return '***';
    }
    
    const start = value.substring(0, 4);
    const end = value.substring(value.length - 4);
    return `${start}...${end}`;
  }

  /**
   * Check if entry contains tenant-specific data
   */
  private containsTenantSpecificData(entry: any): boolean {
    const tenantIndicators = [
      /tenant[_-]?id/i,
      /org[_-]?id/i,
      /organization[_-]?id/i,
      /customer[_-]?id/i,
      /account[_-]?id/i
    ];

    const content = JSON.stringify(entry);
    
    for (const pattern of tenantIndicators) {
      if (pattern.test(content)) {
        return true;
      }
    }

    return false;
  }

  /**
   * Check batch of entries
   */
  public checkBatch(entries: any[]): PrivacyCheckResult {
    const allViolations: PrivacyViolation[] = [];

    for (const entry of entries) {
      const result = this.check(entry);
      allViolations.push(...result.violations);
    }

    return {
      passed: allViolations.length === 0,
      violations: allViolations
    };
  }

  /**
   * Escalate critical violations
   */
  public escalate(violations: PrivacyViolation[]): void {
    const criticalViolations = violations.filter(
      v => v.severity === ViolationSeverity.CRITICAL
    );

    if (criticalViolations.length > 0) {
      console.error('[PrivacyChecker] CRITICAL VIOLATIONS DETECTED:');
      for (const violation of criticalViolations) {
        console.error(`  - ${violation.type} in ${violation.field}: ${violation.reason}`);
      }
      
      throw new Error(
        `Critical privacy violations detected: ${criticalViolations.length} violations`
      );
    }
  }
}
