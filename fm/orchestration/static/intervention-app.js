/**
 * Build Intervention Application
 * 
 * Implements BUILD_INTERVENTION_AND_ALERT_MODEL.md (G-C10)
 * Provides UI for intervention controls and alert routing
 */

const API_BASE_URL = 'http://localhost:5000/api';

// State management
const state = {
    currentNode: null,
    currentNodeType: null,
    interventionHistory: []
};

// Authority routing mappings
const AUTHORITY_ROUTING = {
    step: {
        alert: 'Builder Agent and FM',
        stop: 'FM'
    },
    'sub-wave': {
        alert: 'FM and Governance',
        stop: 'Human Authority or FM'
    },
    wave: {
        alert: 'FM, Governance, and Human Authority',
        stop: 'Human Authority'
    },
    application: {
        alert: 'Human Authority and Johan',
        stop: 'Johan'
    }
};

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    console.log('Build Intervention Controls initialized');
    
    // Set up event listeners
    document.getElementById('load-node-btn').addEventListener('click', loadNodeContext);
    document.getElementById('alert-btn').addEventListener('click', openAlertModal);
    document.getElementById('emergency-stop-btn').addEventListener('click', openStopModal);
    
    // Modal close buttons
    document.getElementById('alert-modal-close').addEventListener('click', closeAlertModal);
    document.getElementById('stop-modal-close').addEventListener('click', closeStopModal);
    document.getElementById('alert-cancel-btn').addEventListener('click', closeAlertModal);
    document.getElementById('stop-cancel-btn').addEventListener('click', closeStopModal);
    
    // Modal action buttons
    document.getElementById('alert-send-btn').addEventListener('click', sendAlert);
    document.getElementById('stop-execute-btn').addEventListener('click', executeStop);
    
    // Input validation
    document.getElementById('alert-rationale').addEventListener('input', validateAlertInput);
    document.getElementById('stop-rationale').addEventListener('input', validateStopInput);
    document.getElementById('stop-acknowledge-checkbox').addEventListener('change', validateStopInput);
    document.getElementById('stop-confirmation-input').addEventListener('input', validateStopInput);
    
    // Scope selection handlers
    document.getElementById('alert-scope-select').addEventListener('change', updateAlertAuthority);
    document.getElementById('stop-scope-select').addEventListener('change', updateStopAuthority);
    
    // Allow Enter key in node ID input
    document.getElementById('node-id-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            loadNodeContext();
        }
    });
    
    // Check for URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const nodeType = urlParams.get('type');
    const nodeId = urlParams.get('id');
    
    if (nodeType && nodeId) {
        document.getElementById('node-type-select').value = nodeType;
        document.getElementById('node-id-input').value = nodeId;
        setTimeout(loadNodeContext, 100);
    }
});

/**
 * Load node context from inspector
 */
async function loadNodeContext() {
    const nodeType = document.getElementById('node-type-select').value;
    const nodeId = document.getElementById('node-id-input').value.trim();
    
    if (!nodeId) {
        showError('Please enter a node ID');
        return;
    }
    
    const loadBtn = document.getElementById('load-node-btn');
    loadBtn.disabled = true;
    loadBtn.classList.add('loading');
    
    hideMessages();
    
    try {
        // Call inspector API to get node context
        const response = await fetch(
            `${API_BASE_URL}/build-tree/inspect/${nodeType}/${nodeId}?depth=3`
        );
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.details || errorData.error || 'Failed to load node');
        }
        
        const result = await response.json();
        
        if (result.success) {
            state.currentNode = nodeId;
            state.currentNodeType = nodeType;
            displayNodeContext(result.data);
            showInterventionControls();
        } else {
            throw new Error(result.error || 'Failed to load node');
        }
        
    } catch (error) {
        console.error('Error loading node:', error);
        showError(`Failed to load node: ${error.message}`);
    } finally {
        loadBtn.disabled = false;
        loadBtn.classList.remove('loading');
    }
}

/**
 * Display node context
 */
function displayNodeContext(nodeData) {
    const contextDiv = document.getElementById('node-context');
    
    contextDiv.innerHTML = `
        <div class="context-item">
            <span class="context-label">Node ID:</span>
            <span class="context-value">${nodeData.node_id}</span>
        </div>
        <div class="context-item">
            <span class="context-label">Node Type:</span>
            <span class="context-value">${nodeData.node_type}</span>
        </div>
        <div class="context-item">
            <span class="context-label">Status:</span>
            <span class="context-value">${nodeData.status_indicator || 'UNKNOWN'}</span>
        </div>
        <div class="context-item">
            <span class="context-label">State:</span>
            <span class="context-value">${nodeData.execution_state || 'UNKNOWN'}</span>
        </div>
    `;
    
    document.getElementById('node-context-panel').style.display = 'block';
}

/**
 * Show intervention controls
 */
function showInterventionControls() {
    document.getElementById('intervention-controls').style.display = 'block';
}

/**
 * Open alert modal
 */
function openAlertModal() {
    if (!state.currentNode) return;
    
    document.getElementById('alert-target-node').textContent = 
        `${state.currentNodeType}/${state.currentNode}`;
    document.getElementById('alert-rationale').value = '';
    document.getElementById('alert-char-count').textContent = '0';
    document.getElementById('alert-scope-select').value = 'step';
    
    updateAlertAuthority();
    
    document.getElementById('alert-modal').style.display = 'flex';
}

/**
 * Close alert modal
 */
function closeAlertModal() {
    document.getElementById('alert-modal').style.display = 'none';
}

/**
 * Update alert authority text based on scope
 */
function updateAlertAuthority() {
    const scope = document.getElementById('alert-scope-select').value;
    const authority = AUTHORITY_ROUTING[scope].alert;
    
    document.getElementById('alert-authority-text').textContent = 
        `This alert will be routed to: ${authority}`;
}

/**
 * Validate alert input
 */
function validateAlertInput() {
    const rationale = document.getElementById('alert-rationale').value;
    const charCount = rationale.length;
    
    document.getElementById('alert-char-count').textContent = charCount;
    
    const sendBtn = document.getElementById('alert-send-btn');
    sendBtn.disabled = charCount < 20;
}

/**
 * Send alert
 */
async function sendAlert() {
    const scopeLevel = document.getElementById('alert-scope-select').value;
    const rationale = document.getElementById('alert-rationale').value;
    
    const sendBtn = document.getElementById('alert-send-btn');
    sendBtn.disabled = true;
    sendBtn.classList.add('loading');
    
    try {
        const response = await fetch(`${API_BASE_URL}/build-tree/alert`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                scope_level: scopeLevel,
                target_node_id: state.currentNode,
                rationale: rationale,
                triggered_by: 'web_user'
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.details || errorData.error || 'Failed to issue alert');
        }
        
        const result = await response.json();
        
        if (result.success) {
            closeAlertModal();
            showSuccess(`Alert ${result.alert_id} issued successfully. Routed to: ${result.routed_to.join(', ')}`);
            
            // Add to history
            state.interventionHistory.unshift({
                type: 'alert',
                id: result.alert_id,
                scope: scopeLevel,
                timestamp: result.timestamp,
                rationale: rationale
            });
        } else {
            throw new Error(result.error || 'Failed to issue alert');
        }
        
    } catch (error) {
        console.error('Error issuing alert:', error);
        showError(`Failed to issue alert: ${error.message}`);
    } finally {
        sendBtn.disabled = false;
        sendBtn.classList.remove('loading');
    }
}

/**
 * Open emergency stop modal
 */
function openStopModal() {
    if (!state.currentNode) return;
    
    document.getElementById('stop-target-node').textContent = 
        `${state.currentNodeType}/${state.currentNode}`;
    document.getElementById('stop-rationale').value = '';
    document.getElementById('stop-char-count').textContent = '0';
    document.getElementById('stop-scope-select').value = 'step';
    document.getElementById('stop-acknowledge-checkbox').checked = false;
    document.getElementById('stop-confirmation-input').value = '';
    
    updateStopAuthority();
    
    document.getElementById('stop-modal').style.display = 'flex';
}

/**
 * Close stop modal
 */
function closeStopModal() {
    document.getElementById('stop-modal').style.display = 'none';
}

/**
 * Update stop authority text based on scope
 */
function updateStopAuthority() {
    const scope = document.getElementById('stop-scope-select').value;
    const authority = AUTHORITY_ROUTING[scope].stop;
    
    document.getElementById('stop-scope-impact').textContent = scope;
    document.getElementById('stop-auth-required').textContent = authority;
    document.getElementById('stop-authority-text').textContent = 
        `Resumption requires authorization from: ${authority}`;
}

/**
 * Validate stop input
 */
function validateStopInput() {
    const rationale = document.getElementById('stop-rationale').value;
    const charCount = rationale.length;
    const acknowledged = document.getElementById('stop-acknowledge-checkbox').checked;
    const confirmation = document.getElementById('stop-confirmation-input').value;
    
    document.getElementById('stop-char-count').textContent = charCount;
    
    const executeBtn = document.getElementById('stop-execute-btn');
    executeBtn.disabled = !(charCount >= 50 && acknowledged && confirmation === 'STOP');
}

/**
 * Execute emergency stop
 */
async function executeStop() {
    const scopeLevel = document.getElementById('stop-scope-select').value;
    const rationale = document.getElementById('stop-rationale').value;
    const acknowledged = document.getElementById('stop-acknowledge-checkbox').checked;
    const confirmation = document.getElementById('stop-confirmation-input').value;
    
    const executeBtn = document.getElementById('stop-execute-btn');
    executeBtn.disabled = true;
    executeBtn.classList.add('loading');
    
    try {
        const response = await fetch(`${API_BASE_URL}/build-tree/emergency-stop`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                scope_level: scopeLevel,
                target_node_id: state.currentNode,
                critical_rationale: rationale,
                confirmation: {
                    acknowledged_impact: acknowledged,
                    typed_confirmation: confirmation
                },
                triggered_by: 'web_user'
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.details || errorData.error || 'Failed to execute stop');
        }
        
        const result = await response.json();
        
        if (result.success) {
            closeStopModal();
            showSuccess(
                `🛑 EMERGENCY STOP ${result.stop_id} EXECUTED<br><br>` +
                `Stopped at: ${result.stopped_at}<br>` +
                `Affected nodes: ${result.affected_nodes.length}<br>` +
                `Resumption requires: ${result.resumption_requires}`
            );
            
            // Add to history
            state.interventionHistory.unshift({
                type: 'stop',
                id: result.stop_id,
                scope: scopeLevel,
                timestamp: result.stopped_at,
                rationale: rationale
            });
        } else {
            throw new Error(result.error || 'Failed to execute stop');
        }
        
    } catch (error) {
        console.error('Error executing stop:', error);
        showError(`Failed to execute emergency stop: ${error.message}`);
    } finally {
        executeBtn.disabled = false;
        executeBtn.classList.remove('loading');
    }
}

/**
 * Show success message
 */
function showSuccess(message) {
    hideMessages();
    document.getElementById('success-message').innerHTML = message;
    document.getElementById('success-panel').style.display = 'block';
    
    // Scroll to success panel
    document.getElementById('success-panel').scrollIntoView({ behavior: 'smooth' });
}

/**
 * Show error message
 */
function showError(message) {
    hideMessages();
    document.getElementById('error-message').textContent = message;
    document.getElementById('error-panel').style.display = 'block';
    
    // Scroll to error panel
    document.getElementById('error-panel').scrollIntoView({ behavior: 'smooth' });
}

/**
 * Hide all messages
 */
function hideMessages() {
    document.getElementById('success-panel').style.display = 'none';
    document.getElementById('error-panel').style.display = 'none';
}

/**
 * Close modal when clicking outside
 */
window.addEventListener('click', (event) => {
    const alertModal = document.getElementById('alert-modal');
    const stopModal = document.getElementById('stop-modal');
    
    if (event.target === alertModal) {
        closeAlertModal();
    }
    
    if (event.target === stopModal) {
        closeStopModal();
    }
});
