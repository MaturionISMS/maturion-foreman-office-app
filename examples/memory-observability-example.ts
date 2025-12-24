/**
 * Memory Observability Usage Examples
 * 
 * Demonstrates how to use the memory observability system:
 * - Initialize observability
 * - Query health and audit APIs
 * - Generate dashboard data
 * - Log memory operations
 * 
 * @module examples/memory-observability-example
 */

import {
  createMemoryObservability,
  MemoryObservabilityIntegration
} from '../lib/memory';

/**
 * Example 1: Basic Initialization and Health Check
 */
async function example1_BasicHealthCheck() {
  console.log('=== Example 1: Basic Health Check ===\n');

  // Create and initialize observability
  const observability = await createMemoryObservability({
    memoryRoot: './memory',
    enableAuditLogging: true,
    enableHealthMonitoring: true,
    enableDashboards: true
  });

  // Get health status
  const health = observability.getHealth();
  console.log('Memory State:', health.state);
  console.log('State Duration:', health.stateDurationSec, 'seconds');
  console.log('Scopes Available:');
  Object.entries(health.scopes).forEach(([scope, status]) => {
    console.log(`  ${scope}: ${status.status} (${status.entryCount} entries)`);
  });
  console.log('\nMetrics:');
  console.log('  Load Time:', health.metrics.loadTimeSec, 'seconds');
  console.log('  Validation Time:', health.metrics.validationTimeSec, 'seconds');
  console.log('  Total Entries:', health.metrics.totalEntries);
  console.log('  Privacy Violations:', health.metrics.privacyViolations);
  console.log('\nAlerts:');
  health.alerts.forEach(alert => console.log('  ', alert));
}

/**
 * Example 2: Query Lifecycle History
 */
async function example2_LifecycleHistory() {
  console.log('\n=== Example 2: Lifecycle History ===\n');

  const observability = await createMemoryObservability();

  // Get lifecycle history for last 24 hours
  const oneDayAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);
  const history = observability.getLifecycleHistory(oneDayAgo, 10);

  console.log('Transition Count:', history.transitionCount);
  console.log('\nRecent Transitions:');
  history.transitions.forEach(transition => {
    console.log(`  ${transition.fromState} → ${transition.toState}`);
    console.log(`    At: ${transition.timestamp}`);
    console.log(`    Reason: ${transition.reason || 'N/A'}`);
    console.log(`    Duration: ${transition.durationInPreviousStateSec}s\n`);
  });

  console.log('Statistics:');
  console.log('  Avg Transition Duration:', history.statistics.avgTransitionDurationSec, 'seconds');
  console.log('  Longest State:', history.statistics.longestState);
}

/**
 * Example 3: Access Audit Query
 */
async function example3_AccessAudit() {
  console.log('\n=== Example 3: Access Audit ===\n');

  const observability = await createMemoryObservability();

  // Query all accesses
  const allAccesses = observability.getAccessAudit();
  console.log('Total Accesses:', allAccesses.accessCount);
  console.log('\nBy Actor:');
  Object.entries(allAccesses.statistics.byActor).forEach(([actor, count]) => {
    console.log(`  ${actor}: ${count}`);
  });
  console.log('\nBy Scope:');
  Object.entries(allAccesses.statistics.byScope).forEach(([scope, count]) => {
    console.log(`  ${scope}: ${count}`);
  });
  console.log('\nUnauthorized Attempts:', allAccesses.statistics.unauthorizedAttempts);
  console.log('Avg Query Latency:', allAccesses.statistics.avgQueryLatencyMs, 'ms');

  // Query specific actor
  const chpAccesses = observability.getAccessAudit('CHP');
  console.log(`\nCHP Accesses: ${chpAccesses.accessCount}`);
}

/**
 * Example 4: Log Memory Access
 */
async function example4_LogAccess() {
  console.log('\n=== Example 4: Log Memory Access ===\n');

  const observability = await createMemoryObservability();

  // Simulate memory access
  console.log('Logging memory access...');
  observability.logAccess(
    'ui-builder',
    'builder_agent',
    ['global'],
    15,
    120,
    {
      tagsQueried: ['ui', 'patterns'],
      importanceMin: 'medium',
      reason: 'Loading UI component patterns before task execution',
      sessionId: 'ui-builder-session-456',
      authorized: true
    }
  );

  // Query to verify
  const accesses = observability.getAccessAudit('ui-builder');
  console.log('UI Builder accesses:', accesses.accessCount);
  if (accesses.accesses.length > 0) {
    const latest = accesses.accesses[accesses.accesses.length - 1];
    console.log('Latest access:');
    console.log('  Timestamp:', latest.timestamp);
    console.log('  Scopes:', latest.scopesAccessed);
    console.log('  Entries Returned:', latest.entriesReturned);
    console.log('  Reason:', latest.reason);
  }
}

/**
 * Example 5: Log Memory Write
 */
async function example5_LogWrite() {
  console.log('\n=== Example 5: Log Memory Write ===\n');

  const observability = await createMemoryObservability();

  // Simulate memory write
  console.log('Logging memory write...');
  observability.logWrite(
    'Foreman',
    'foreman',
    'foreman-2025-12-24-001234',
    'Module Boundary Decision: Asset Module API Layer',
    'high',
    ['architecture', 'decision', 'module', 'asset'],
    'passed',
    'passed',
    45,
    {
      reason: 'Approved UI Builder proposal to use API layer for Asset data access',
      sessionId: 'foreman-session-123',
      authorized: true
    }
  );

  // Query to verify
  const writes = observability.getWriteAudit('Foreman', 'foreman');
  console.log('Foreman writes to foreman scope:', writes.writeCount);
  if (writes.writes.length > 0) {
    const latest = writes.writes[writes.writes.length - 1];
    console.log('Latest write:');
    console.log('  Title:', latest.title);
    console.log('  Importance:', latest.importance);
    console.log('  Validation:', latest.validationStatus);
    console.log('  Privacy Check:', latest.privacyCheckStatus);
  }
}

/**
 * Example 6: Privacy Compliance Report
 */
async function example6_PrivacyCompliance() {
  console.log('\n=== Example 6: Privacy Compliance Report ===\n');

  const observability = await createMemoryObservability();

  // Log some privacy scans
  observability.logPrivacyScan(
    'write_validation',
    'foreman',
    'foreman-2025-12-24-001234',
    false,
    false,
    false,
    25,
    'passed'
  );

  // Get compliance report
  const compliance = observability.getPrivacyCompliance();
  console.log('Scans Conducted:', compliance.scansConducted);
  console.log('Compliance Rate:', (compliance.complianceRate * 100).toFixed(2), '%');
  console.log('\nViolations:');
  console.log('  Total:', compliance.violations.totalViolations);
  console.log('  PII Detected:', compliance.violations.byType.pii_detected);
  console.log('  Secrets Detected:', compliance.violations.byType.secrets_detected);
  console.log('  Tenant Data Detected:', compliance.violations.byType.tenant_data_detected);

  if (compliance.alerts.length > 0) {
    console.log('\nAlerts:');
    compliance.alerts.forEach(alert => console.log('  ', alert));
  }
}

/**
 * Example 7: Performance Metrics
 */
async function example7_PerformanceMetrics() {
  console.log('\n=== Example 7: Performance Metrics ===\n');

  const observability = await createMemoryObservability();

  // Get performance metrics
  const metrics = observability.getPerformanceMetrics();
  console.log('Report Period:', metrics.reportPeriod);
  console.log('Interval:', metrics.interval);
  console.log('\nThresholds:');
  console.log('  Load Time:', metrics.thresholds.loadTimeSec, 'seconds');
  console.log('  Validation Time:', metrics.thresholds.validationTimeSec, 'seconds');
  console.log('  Avg Query Latency:', metrics.thresholds.avgQueryLatencyMs, 'ms');
  console.log('  Cache Hit Rate:', metrics.thresholds.cacheHitRate);

  console.log('\nData Points:', metrics.dataPoints.length);
  if (metrics.dataPoints.length > 0) {
    const latest = metrics.dataPoints[metrics.dataPoints.length - 1];
    console.log('Latest Metrics:');
    console.log('  Query Latency:', latest.metrics.avgQueryLatencyMs, 'ms');
    console.log('  Cache Hit Rate:', latest.metrics.cacheHitRate);
    console.log('  Queries/sec:', latest.metrics.queriesPerSec);
    console.log('  Writes/sec:', latest.metrics.writesPerSec);
  }

  if (metrics.alerts.length > 0) {
    console.log('\nAlerts:');
    metrics.alerts.forEach(alert => console.log('  ', alert));
  }
}

/**
 * Example 8: Foreman Dashboard Panel
 */
async function example8_ForemanPanel() {
  console.log('\n=== Example 8: Foreman Dashboard Panel ===\n');

  const observability = await createMemoryObservability({
    enableDashboards: true
  });

  // Get Foreman panel data
  const panel = observability.getForemanPanel();
  console.log(panel.stateIndicator, panel.stateMessage);
  console.log('\nState Duration:', panel.stateDurationSec, 'seconds');
  
  console.log('\nScope Availability:');
  Object.entries(panel.scopeAvailability).forEach(([scope, available]) => {
    console.log(`  ${scope}: ${available ? '✅' : '❌'}`);
  });

  if (panel.unavailableScopes.length > 0) {
    console.log('\nUnavailable Scopes:', panel.unavailableScopes.join(', '));
  }

  console.log('\nValidation Status:');
  console.log('  Outcome:', panel.validationStatus.outcome);
  console.log('  Errors:', panel.validationStatus.errors);
  console.log('  Warnings:', panel.validationStatus.warnings);

  console.log('\nPrivacy Compliance:');
  console.log('  Status:', panel.privacyCompliance.status);
  console.log('  Violations:', panel.privacyCompliance.violations);

  console.log('\nAvailable Actions:');
  panel.actions.forEach(action => {
    const status = action.enabled ? '✅' : '❌';
    console.log(`  ${status} ${action.label}`);
  });
}

/**
 * Example 9: Watchdog Dashboard Monitor
 */
async function example9_WatchdogMonitor() {
  console.log('\n=== Example 9: Watchdog Dashboard Monitor ===\n');

  const observability = await createMemoryObservability({
    enableDashboards: true
  });

  // Get Watchdog monitor data
  const monitor = observability.getWatchdogMonitor();
  console.log('Current State:', monitor.currentState);
  console.log('State Timeline:', monitor.stateTimeline.length, 'states');

  console.log('\nPerformance:');
  console.log('  Load Time:', monitor.performance.loadTimeSec, 's');
  console.log('  Validation Time:', monitor.performance.validationTimeSec, 's');
  console.log('  Avg Query Latency:', monitor.performance.avgQueryLatencyMs, 'ms');
  console.log('  Cache Hit Rate:', monitor.performance.cacheHitRate);

  if (monitor.performance.breached.length > 0) {
    console.log('  ⚠️ Thresholds Breached:', monitor.performance.breached.join(', '));
  }

  console.log('\nAccess Patterns:');
  console.log('  Queries/min:', monitor.accessPatterns.queriesPerMinute);
  console.log('  Writes/min:', monitor.accessPatterns.writesPerMinute);

  console.log('\nPrivacy Compliance:');
  console.log('  Total Scans:', monitor.privacyCompliance.totalScans);
  console.log('  Violations:', monitor.privacyCompliance.violations);
  console.log('  Compliance Rate:', (monitor.privacyCompliance.complianceRate * 100).toFixed(2), '%');

  if (monitor.anomalies.length > 0) {
    console.log('\nAnomalies:');
    monitor.anomalies.forEach(anomaly => {
      console.log(`  [${anomaly.severity}] ${anomaly.type}: ${anomaly.message}`);
    });
  }
}

/**
 * Example 10: Johan Dashboard Oversight
 */
async function example10_JohanOversight() {
  console.log('\n=== Example 10: Johan Dashboard Oversight ===\n');

  const observability = await createMemoryObservability({
    enableDashboards: true
  });

  // Get Johan oversight data
  const oversight = observability.getJohanOversight();
  
  console.log('Audit Trail:');
  console.log('  Total Accesses:', oversight.auditTrail.totalAccesses);
  console.log('  Total Writes:', oversight.auditTrail.totalWrites);
  console.log('  Unauthorized Attempts:', oversight.auditTrail.unauthorizedAttempts);

  console.log('\nCHP Proposals:');
  console.log('  Total:', oversight.chpProposals.total);
  console.log('  Pending:', oversight.chpProposals.pending);
  console.log('  Approved:', oversight.chpProposals.approved);
  console.log('  Rejected:', oversight.chpProposals.rejected);

  console.log('\nGovernance Status:');
  console.log('  Memory Behavior Compliance:', oversight.governanceStatus.memoryBehaviorCompliance ? '✅' : '❌');
  console.log('  Privacy Guardrail Compliance:', oversight.governanceStatus.privacyGuardrailCompliance ? '✅' : '❌');
  console.log('  Compliance Rate:', (oversight.governanceStatus.complianceRate * 100).toFixed(2), '%');

  console.log('\nAvailable Queries:');
  oversight.availableQueries.forEach(query => {
    console.log(`  - ${query.name}`);
    console.log(`    ${query.description}`);
    console.log(`    Parameters: ${query.parameters.join(', ')}`);
  });

  console.log('\nAvailable Actions:');
  oversight.actions.forEach(action => {
    const status = action.enabled ? '✅' : '❌';
    const confirm = action.requiresConfirmation ? ' (requires confirmation)' : '';
    console.log(`  ${status} ${action.label}${confirm}`);
  });
}

/**
 * Run all examples
 */
async function runAllExamples() {
  try {
    await example1_BasicHealthCheck();
    await example2_LifecycleHistory();
    await example3_AccessAudit();
    await example4_LogAccess();
    await example5_LogWrite();
    await example6_PrivacyCompliance();
    await example7_PerformanceMetrics();
    await example8_ForemanPanel();
    await example9_WatchdogMonitor();
    await example10_JohanOversight();
    
    console.log('\n=== All Examples Completed ===\n');
  } catch (error) {
    console.error('Error running examples:', error);
  }
}

// Run if executed directly
if (require.main === module) {
  runAllExamples().catch(console.error);
}

export {
  example1_BasicHealthCheck,
  example2_LifecycleHistory,
  example3_AccessAudit,
  example4_LogAccess,
  example5_LogWrite,
  example6_PrivacyCompliance,
  example7_PerformanceMetrics,
  example8_ForemanPanel,
  example9_WatchdogMonitor,
  example10_JohanOversight,
  runAllExamples
};
