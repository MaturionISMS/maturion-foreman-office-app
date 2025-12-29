/**
 * Build Node Inspector Application
 * 
 * Implements BUILD_NODE_INSPECTION_MODEL.md (G-C9)
 * Enforces principle: "No status without explanation"
 */

const API_BASE_URL = 'http://localhost:5000/api';

// State management
const state = {
    currentInspection: null,
    currentDepth: 3
};

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    console.log('Build Node Inspector initialized');
    
    // Set up event listeners
    document.getElementById('inspect-btn').addEventListener('click', handleInspect);
    document.getElementById('depth-select').addEventListener('change', handleDepthChange);
    
    // Allow Enter key to trigger inspection
    document.getElementById('node-id-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleInspect();
        }
    });
    
    // Check for URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const nodeType = urlParams.get('type');
    const nodeId = urlParams.get('id');
    const depth = urlParams.get('depth');
    
    if (nodeType && nodeId) {
        document.getElementById('node-type-select').value = nodeType;
        document.getElementById('node-id-input').value = nodeId;
        if (depth) {
            document.getElementById('depth-select').value = depth;
        }
        // Auto-trigger inspection
        setTimeout(handleInspect, 100);
    }
});

/**
 * Handle inspection button click
 */
async function handleInspect() {
    const nodeType = document.getElementById('node-type-select').value;
    const nodeId = document.getElementById('node-id-input').value.trim();
    const depth = parseInt(document.getElementById('depth-select').value);
    
    if (!nodeId) {
        showError('Please enter a node ID');
        return;
    }
    
    // Hide previous results and errors
    document.getElementById('inspection-panel').style.display = 'none';
    document.getElementById('error-panel').style.display = 'none';
    
    // Show loading state
    const inspectBtn = document.getElementById('inspect-btn');
    inspectBtn.disabled = true;
    inspectBtn.textContent = '🔄 Inspecting...';
    
    try {
        // Call inspection API
        const response = await fetch(
            `${API_BASE_URL}/build-tree/inspect/${nodeType}/${nodeId}?depth=${depth}&include_children=false`
        );
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.details || errorData.error || 'Inspection failed');
        }
        
        const result = await response.json();
        
        if (result.success) {
            state.currentInspection = result.data;
            state.currentDepth = depth;
            renderInspection();
        } else {
            throw new Error(result.error || 'Inspection failed');
        }
        
    } catch (error) {
        console.error('Inspection error:', error);
        showError(`Failed to inspect node: ${error.message}`);
    } finally {
        inspectBtn.disabled = false;
        inspectBtn.textContent = '🔍 Inspect Node';
    }
}

/**
 * Handle depth change
 */
function handleDepthChange() {
    const depth = parseInt(document.getElementById('depth-select').value);
    if (state.currentInspection) {
        state.currentDepth = depth;
        updateDepthDisplay();
    }
}

/**
 * Render inspection results
 */
function renderInspection() {
    const data = state.currentInspection;
    
    // Update breadcrumb
    updateBreadcrumb(data);
    
    // Show inspection panel
    document.getElementById('inspection-panel').style.display = 'block';
    
    // Render Level 1: Quick Status (always shown)
    renderQuickStatus(data);
    
    // Update visibility based on depth
    updateDepthDisplay();
}

/**
 * Update breadcrumb navigation
 */
function updateBreadcrumb(data) {
    const breadcrumb = document.getElementById('breadcrumb');
    breadcrumb.innerHTML = `
        <span>Inspector</span> → 
        <span>${data.node_type}</span> → 
        <strong>${data.name}</strong>
    `;
}

/**
 * Update depth display based on current depth
 */
function updateDepthDisplay() {
    const depth = state.currentDepth;
    const data = state.currentInspection;
    
    // Level 1: Always visible
    document.getElementById('level-1-content').style.display = 'block';
    
    // Level 2
    if (depth >= 2) {
        document.getElementById('level-2-content').style.display = 'block';
        renderStateExplanation(data.current_state);
    } else {
        document.getElementById('level-2-content').style.display = 'none';
    }
    
    // Level 3
    if (depth >= 3) {
        document.getElementById('level-3-content').style.display = 'block';
        renderGoverningChecks(data.governing_checks);
        renderRequirements(data.requirements);
        renderEvidence(data.evidence, data.evidence_summary);
    } else {
        document.getElementById('level-3-content').style.display = 'none';
    }
    
    // Level 4
    if (depth >= 4) {
        document.getElementById('level-4-content').style.display = 'block';
        renderDecisions(data.decisions);
        renderAuditReports(data.audit_reports);
        renderSurveys(data.surveys);
    } else {
        document.getElementById('level-4-content').style.display = 'none';
    }
    
    // Level 5
    if (depth >= 5) {
        document.getElementById('level-5-content').style.display = 'block';
        renderBlockers(data.blockers);
        renderResolutionPaths(data.blocker_resolution_paths);
        renderStopConditions(data.stop_conditions);
    } else {
        document.getElementById('level-5-content').style.display = 'none';
    }
}

/**
 * Render Level 1: Quick Status
 */
function renderQuickStatus(data) {
    const container = document.getElementById('quick-status');
    
    container.innerHTML = `
        <div class="node-title">${data.name}</div>
        <div class="node-description">${data.description}</div>
        <div class="status-badges">
            <span class="status-badge execution">EXECUTION: ${data.current_state?.execution_state || 'N/A'}</span>
            <span class="status-badge activation">ACTIVATION: ${data.current_state?.activation_state || 'N/A'}</span>
            <span class="status-badge ${(data.current_state?.status || 'GREEN').toLowerCase()}">
                STATUS: ${getStatusIcon(data.current_state?.status)} ${data.current_state?.status || 'N/A'}
            </span>
            <span class="status-badge">${data.current_state?.completion_percentage || 0}% Complete</span>
        </div>
        <div style="margin-top: 1rem; font-size: 0.85rem; color: rgba(255, 255, 255, 0.5);">
            <div>Created: ${formatTimestamp(data.created_at)}</div>
            <div>Updated: ${formatTimestamp(data.updated_at)}</div>
            <div>Last Inspected: ${formatTimestamp(data.last_inspected_at)}</div>
        </div>
    `;
}

/**
 * Render Level 2: State Explanation
 */
function renderStateExplanation(state) {
    const container = document.getElementById('state-explanation');
    
    if (!state) {
        container.innerHTML = '<p>No state explanation available</p>';
        return;
    }
    
    let factorsHtml = '';
    if (state.status_contributing_factors && state.status_contributing_factors.length > 0) {
        factorsHtml = `
            <ul class="status-factors">
                ${state.status_contributing_factors.map(factor => `
                    <li class="${factor.contributing_to.toLowerCase()}">
                        <span>${getStatusIcon(factor.contributing_to)}</span>
                        <span><strong>${factor.factor_type}:</strong> ${factor.description} (${factor.severity})</span>
                    </li>
                `).join('')}
            </ul>
        `;
    }
    
    container.innerHTML = `
        <div class="explanation-section">
            <h4>Execution State: ${state.execution_state}</h4>
            <div class="reason">${state.execution_state_reason}</div>
            <div class="since">Since: ${formatTimestamp(state.execution_state_since)}</div>
        </div>
        
        <div class="explanation-section">
            <h4>Activation State: ${state.activation_state}</h4>
            <div class="reason">${state.activation_state_reason}</div>
            <div class="since">Since: ${formatTimestamp(state.activation_state_since)}</div>
        </div>
        
        <div class="explanation-section">
            <h4>Status: ${getStatusIcon(state.status)} ${state.status}</h4>
            <div class="reason">${state.status_reason}</div>
            ${factorsHtml}
        </div>
        
        <div class="explanation-section">
            <h4>Completion: ${state.completion_percentage}%</h4>
            <div class="reason">${state.completion_calculation}</div>
            <div class="since" style="margin-top: 0.5rem;">
                ${state.completion_is_authoritative ? 
                    '⚠️ This percentage is authoritative' : 
                    '✅ This percentage is informational only (not authoritative)'}
            </div>
        </div>
    `;
}

/**
 * Render governing checks
 */
function renderGoverningChecks(checks) {
    const container = document.getElementById('governing-checks');
    
    if (!checks || checks.length === 0) {
        container.innerHTML = '<h4>🔍 Governing Checks</h4><p>No governing checks defined</p>';
        return;
    }
    
    container.innerHTML = `
        <h4>🔍 Governing Checks (${checks.length})</h4>
        <ul class="checks-list">
            ${checks.map(check => `
                <li class="check-item">
                    <div class="item-header">
                        <span class="item-title">${check.check_name}</span>
                        <span class="item-status ${check.status.toLowerCase()}">${check.status}</span>
                    </div>
                    <div class="item-description">${check.description}</div>
                    <div class="item-meta">
                        Type: ${check.check_type} | Required: ${check.required ? 'Yes' : 'No'}
                        ${check.last_checked_at ? ` | Last checked: ${formatTimestamp(check.last_checked_at)}` : ''}
                        ${check.failure_reason ? `<br/>Failure reason: ${check.failure_reason}` : ''}
                    </div>
                </li>
            `).join('')}
        </ul>
    `;
}

/**
 * Render requirements
 */
function renderRequirements(requirements) {
    const container = document.getElementById('requirements');
    
    if (!requirements || requirements.length === 0) {
        container.innerHTML = '<h4>📋 Requirements</h4><p>No requirements defined</p>';
        return;
    }
    
    const satisfiedCount = requirements.filter(r => r.satisfied).length;
    
    container.innerHTML = `
        <h4>📋 Requirements (${satisfiedCount}/${requirements.length} satisfied)</h4>
        <ul class="requirements-list">
            ${requirements.map(req => `
                <li class="requirement-item">
                    <div class="item-header">
                        <span class="item-title">${req.requirement_name}</span>
                        <span class="item-status ${req.satisfied ? 'satisfied' : 'unsatisfied'}">
                            ${req.satisfied ? '✅ Satisfied' : '❌ Not Satisfied'}
                        </span>
                    </div>
                    <div class="item-description">${req.description}</div>
                    <div class="item-meta">
                        Type: ${req.requirement_type} | Mandatory: ${req.mandatory ? 'Yes' : 'No'}
                        ${req.satisfied_at ? `<br/>Satisfied: ${formatTimestamp(req.satisfied_at)} by ${req.satisfied_by}` : ''}
                        ${req.unsatisfied_reason ? `<br/>Reason: ${req.unsatisfied_reason}` : ''}
                    </div>
                </li>
            `).join('')}
        </ul>
    `;
}

/**
 * Render evidence
 */
function renderEvidence(evidence, summary) {
    const container = document.getElementById('evidence');
    
    if (!evidence || evidence.length === 0) {
        container.innerHTML = '<h4>📎 Evidence</h4><p>No evidence artifacts</p>';
        return;
    }
    
    let summaryHtml = '';
    if (summary) {
        summaryHtml = `
            <div class="evidence-summary">
                <div class="stat">
                    <div class="stat-value">${summary.total_evidence_items}</div>
                    <div class="stat-label">Total Items</div>
                </div>
                <div class="stat">
                    <div class="stat-value">${summary.validated_items}</div>
                    <div class="stat-label">Validated</div>
                </div>
                <div class="stat">
                    <div class="stat-value">${summary.pending_items}</div>
                    <div class="stat-label">Pending</div>
                </div>
                <div class="stat">
                    <div class="stat-value">${summary.by_category.ARCHITECTURE}</div>
                    <div class="stat-label">Architecture</div>
                </div>
                <div class="stat">
                    <div class="stat-value">${summary.by_category.QA}</div>
                    <div class="stat-label">QA</div>
                </div>
                <div class="stat">
                    <div class="stat-value">${summary.by_category.BUILD}</div>
                    <div class="stat-label">Build</div>
                </div>
                <div class="stat">
                    <div class="stat-value">${summary.by_category.COMPLETION}</div>
                    <div class="stat-label">Completion</div>
                </div>
            </div>
        `;
    }
    
    container.innerHTML = `
        <h4>📎 Evidence Artifacts</h4>
        ${summaryHtml}
        <ul class="evidence-list">
            ${evidence.map(ev => `
                <li class="evidence-item">
                    <div class="item-header">
                        <span class="item-title">${ev.artifact_description}</span>
                        <span class="item-status ${ev.validated ? 'validated' : 'pending'}">
                            ${ev.validated ? '✅ Validated' : '⏳ Pending'}
                        </span>
                    </div>
                    <div class="item-description">
                        Category: ${ev.category} | Type: ${ev.artifact_type}
                    </div>
                    <a href="${ev.artifact_location}" class="artifact-link" target="_blank" rel="noopener">
                        📄 View Artifact →
                    </a>
                    <div class="item-meta">
                        ${ev.validated_at ? `Validated: ${formatTimestamp(ev.validated_at)} by ${ev.validated_by}` : ''}
                        ${ev.validation_notes ? `<br/>Notes: ${ev.validation_notes}` : ''}
                    </div>
                </li>
            `).join('')}
        </ul>
    `;
}

/**
 * Render decisions
 */
function renderDecisions(decisions) {
    const container = document.getElementById('decisions');
    
    if (!decisions || decisions.length === 0) {
        container.innerHTML = '<h4>⚖️ Decisions</h4><p>No decisions recorded</p>';
        return;
    }
    
    container.innerHTML = `
        <h4>⚖️ Decisions (${decisions.length})</h4>
        <ul class="decisions-list">
            ${decisions.map(dec => `
                <li class="decision-item">
                    <div class="item-header">
                        <span class="item-title">${dec.decision_summary}</span>
                        <span class="item-status">${dec.decision_type.toUpperCase()}</span>
                    </div>
                    <div class="decision-rationale">${dec.decision_rationale}</div>
                    <div class="item-meta">
                        Authority: ${dec.decision_authority} | 
                        Decided: ${formatTimestamp(dec.decided_at)}
                    </div>
                </li>
            `).join('')}
        </ul>
    `;
}

/**
 * Render audit reports
 */
function renderAuditReports(reports) {
    const container = document.getElementById('audit-reports');
    
    if (!reports || reports.length === 0) {
        container.innerHTML = '<h4>📊 Audit Reports</h4><p>No audit reports available</p>';
        return;
    }
    
    container.innerHTML = `
        <h4>📊 Audit Reports (${reports.length})</h4>
        <ul class="audit-list">
            ${reports.map(report => `
                <li class="audit-item">
                    <div class="item-header">
                        <span class="item-title">${report.report_title}</span>
                    </div>
                    <div class="item-description">${report.findings_summary}</div>
                    <a href="${report.report_location}" class="artifact-link" target="_blank" rel="noopener">
                        📄 View Report →
                    </a>
                    <div class="item-meta">
                        Type: ${report.report_type} | 
                        Created: ${formatTimestamp(report.created_at)} by ${report.created_by}
                    </div>
                </li>
            `).join('')}
        </ul>
    `;
}

/**
 * Render surveys
 */
function renderSurveys(surveys) {
    const container = document.getElementById('surveys');
    
    if (!surveys || surveys.length === 0) {
        container.innerHTML = '<h4>📝 Surveys</h4><p>No surveys available</p>';
        return;
    }
    
    container.innerHTML = `
        <h4>📝 Surveys (${surveys.length})</h4>
        <ul class="audit-list">
            ${surveys.map(survey => `
                <li class="audit-item">
                    <div class="item-header">
                        <span class="item-title">${survey.survey_title}</span>
                    </div>
                    <div class="item-description">${survey.summary}</div>
                    <a href="${survey.survey_location}" class="artifact-link" target="_blank" rel="noopener">
                        📄 View Survey →
                    </a>
                    <div class="item-meta">
                        Type: ${survey.survey_type} | 
                        Conducted: ${formatTimestamp(survey.conducted_at)} | 
                        Respondent: ${survey.respondent}
                    </div>
                </li>
            `).join('')}
        </ul>
    `;
}

/**
 * Render blockers
 */
function renderBlockers(blockers) {
    const container = document.getElementById('blockers');
    
    if (!blockers || blockers.length === 0) {
        container.innerHTML = '<h4>⛔ Active Blockers</h4><p style="color: #22c55e;">✅ No active blockers</p>';
        return;
    }
    
    container.innerHTML = `
        <h4>⛔ Active Blockers (${blockers.length})</h4>
        <ul class="blockers-list">
            ${blockers.map(blocker => `
                <li class="blocker-item">
                    <div class="item-header">
                        <span class="item-title">${blocker.description}</span>
                        <span class="blocker-severity ${blocker.severity.toLowerCase()}">${blocker.severity}</span>
                    </div>
                    <div class="item-meta">
                        Type: ${blocker.type} | 
                        Created: ${formatTimestamp(blocker.created_at)}
                        ${blocker.resolved_at ? ` | Resolved: ${formatTimestamp(blocker.resolved_at)}` : ''}
                        ${blocker.resolution ? `<br/>Resolution: ${blocker.resolution}` : ''}
                    </div>
                </li>
            `).join('')}
        </ul>
    `;
}

/**
 * Render resolution paths
 */
function renderResolutionPaths(paths) {
    const container = document.getElementById('resolution-paths');
    
    if (!paths || paths.length === 0) {
        container.innerHTML = '<h4>🔧 Resolution Paths</h4><p>No resolution paths defined</p>';
        return;
    }
    
    container.innerHTML = `
        <h4>🔧 Resolution Paths (${paths.length})</h4>
        ${paths.map(path => `
            <div class="resolution-path">
                <h5>Resolution for: ${path.blocker_id}</h5>
                <div><strong>Strategy:</strong> ${path.resolution_strategy}</div>
                <div><strong>Owner:</strong> ${path.owner}</div>
                <div><strong>Status:</strong> ${path.status}</div>
                ${path.estimated_resolution_time ? `<div><strong>Estimated:</strong> ${path.estimated_resolution_time}</div>` : ''}
                <div style="margin-top: 0.5rem;"><strong>Unblocking Criteria:</strong></div>
                <ul class="unblocking-criteria">
                    ${path.unblocking_criteria.map(criteria => `<li>${criteria}</li>`).join('')}
                </ul>
            </div>
        `).join('')}
    `;
}

/**
 * Render STOP conditions
 */
function renderStopConditions(conditions) {
    const container = document.getElementById('stop-conditions');
    
    if (!conditions || conditions.length === 0) {
        container.innerHTML = '<h4>🛑 STOP Conditions</h4><p style="color: #22c55e;">✅ No active STOP conditions</p>';
        return;
    }
    
    container.innerHTML = `
        <h4>🛑 STOP Conditions (${conditions.length})</h4>
        ${conditions.map(stop => `
            <div class="stop-condition-item">
                <div class="item-header">
                    <span class="item-title">${stop.stop_description}</span>
                    <span class="blocker-severity ${stop.severity.toLowerCase()}">${stop.severity}</span>
                </div>
                <div class="item-meta">
                    Type: ${stop.stop_type} | 
                    Triggered: ${formatTimestamp(stop.triggered_at)} by ${stop.triggered_by} |
                    Recovery: ${stop.recovery_status}
                    ${stop.resolved_at ? ` | Resolved: ${formatTimestamp(stop.resolved_at)}` : ''}
                </div>
                ${stop.recovery_actions && stop.recovery_actions.length > 0 ? `
                    <div class="recovery-actions">
                        <h5>Recovery Actions:</h5>
                        <ul class="unblocking-criteria">
                            ${stop.recovery_actions.map(action => `<li>${action}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
            </div>
        `).join('')}
    `;
}

/**
 * Show error message
 */
function showError(message) {
    document.getElementById('inspection-panel').style.display = 'none';
    document.getElementById('error-panel').style.display = 'block';
    document.getElementById('error-message').textContent = message;
}

/**
 * Get status icon
 */
function getStatusIcon(status) {
    switch (status?.toUpperCase()) {
        case 'GREEN': return '🟢';
        case 'AMBER': return '🟡';
        case 'RED': return '🔴';
        default: return '⚪';
    }
}

/**
 * Format timestamp
 */
function formatTimestamp(timestamp) {
    if (!timestamp) return 'N/A';
    try {
        const date = new Date(timestamp);
        return date.toLocaleString();
    } catch (e) {
        return timestamp;
    }
}
