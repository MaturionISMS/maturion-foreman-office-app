/**
 * Build Control Panel - Frontend Application
 * 
 * Handles user interactions with the Build Control Panel UI
 * and communicates with the Build Control API.
 */

const API_BASE = '/api';

// State management
const state = {
    selectedBuildId: null,
    currentResult: null,
    builds: []
};

// DOM elements
const elements = {
    buildIdInput: null,
    loadBuildsBtn: null,
    validateBtn: null,
    executeBtn: null,
    buildsContainer: null,
    buildsList: null,
    resultsPanel: null,
    statusPanel: null,
    gateResultContainer: null,
    statusContainer: null,
    blockerModal: null,
    blockerDetails: null,
    closeModalBtn: null,
    remediationBtn: null
};

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initializeElements();
    attachEventListeners();
    checkHealth();
});

function initializeElements() {
    elements.buildIdInput = document.getElementById('build-id-input');
    elements.loadBuildsBtn = document.getElementById('load-builds-btn');
    elements.validateBtn = document.getElementById('validate-btn');
    elements.executeBtn = document.getElementById('execute-btn');
    elements.buildsContainer = document.getElementById('builds-container');
    elements.buildsList = document.getElementById('builds-list');
    elements.resultsPanel = document.getElementById('results-panel');
    elements.statusPanel = document.getElementById('status-panel');
    elements.gateResultContainer = document.getElementById('gate-result-container');
    elements.statusContainer = document.getElementById('status-container');
    elements.blockerModal = document.getElementById('blocker-modal');
    elements.blockerDetails = document.getElementById('blocker-details');
    elements.closeModalBtn = document.getElementById('close-modal-btn');
    elements.remediationBtn = document.getElementById('remediation-btn');
    
    const closeSpan = document.querySelector('.close');
    closeSpan.onclick = closeModal;
}

function attachEventListeners() {
    elements.buildIdInput.addEventListener('input', onBuildIdInput);
    elements.loadBuildsBtn.addEventListener('click', loadBuilds);
    elements.validateBtn.addEventListener('click', validateBuild);
    elements.executeBtn.addEventListener('click', executeBuild);
    elements.closeModalBtn.addEventListener('click', closeModal);
    elements.remediationBtn.addEventListener('click', showRemediationActions);
    
    // Close modal on outside click
    window.onclick = (event) => {
        if (event.target === elements.blockerModal) {
            closeModal();
        }
    };
}

// Event Handlers

function onBuildIdInput(e) {
    const buildId = e.target.value.trim();
    state.selectedBuildId = buildId;
    elements.validateBtn.disabled = !buildId;
    elements.executeBtn.disabled = true;
    
    // Hide previous results when changing build
    elements.resultsPanel.style.display = 'none';
    elements.statusPanel.style.display = 'none';
}

async function loadBuilds() {
    try {
        setLoading(elements.loadBuildsBtn, true);
        
        const response = await fetch(`${API_BASE}/builds`);
        if (!response.ok) throw new Error('Failed to load builds');
        
        const data = await response.json();
        state.builds = data.builds || [];
        
        displayBuilds(state.builds);
        elements.buildsList.style.display = 'block';
    } catch (error) {
        console.error('Error loading builds:', error);
        showError('Failed to load builds: ' + error.message);
    } finally {
        setLoading(elements.loadBuildsBtn, false);
    }
}

function displayBuilds(builds) {
    if (builds.length === 0) {
        elements.buildsContainer.innerHTML = '<p>No builds found in architecture/builds/</p>';
        return;
    }
    
    elements.buildsContainer.innerHTML = builds.map(build => `
        <div class="build-item" data-build-id="${build.id}" onclick="selectBuild('${build.id}')">
            <div>
                <strong>${build.id}</strong>
            </div>
            <span class="build-status status-${build.status.toLowerCase()}">
                ${build.status}
            </span>
        </div>
    `).join('');
}

function selectBuild(buildId) {
    state.selectedBuildId = buildId;
    elements.buildIdInput.value = buildId;
    elements.validateBtn.disabled = false;
    
    // Update visual selection
    document.querySelectorAll('.build-item').forEach(item => {
        item.classList.toggle('selected', item.dataset.buildId === buildId);
    });
    
    // Load current status for this build
    loadBuildStatus(buildId);
}

async function validateBuild() {
    if (!state.selectedBuildId) {
        showError('Please enter or select a build ID');
        return;
    }
    
    try {
        setLoading(elements.validateBtn, true);
        elements.resultsPanel.style.display = 'none';
        
        const response = await fetch(`${API_BASE}/builds/${state.selectedBuildId}/validate`, {
            method: 'POST'
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.details || 'Validation failed');
        }
        
        const result = await response.json();
        state.currentResult = result;
        
        displayValidationResult(result);
        
        // Enable execute button if authorized
        elements.executeBtn.disabled = !result.can_proceed;
        
        // Show blocker modal if failed
        if (result.gate_result === 'FAIL') {
            showBlockerModal(result);
        }
    } catch (error) {
        console.error('Error validating build:', error);
        showError('Validation failed: ' + error.message);
    } finally {
        setLoading(elements.validateBtn, false);
    }
}

function displayValidationResult(result) {
    const passClass = result.gate_result === 'PASS' ? 'pass' : 'fail';
    const icon = result.gate_result === 'PASS' ? '✅' : '❌';
    
    let html = `
        <div class="gate-result ${passClass}">
            <h3>${icon} ${result.gate_result}</h3>
            <p><strong>Build ID:</strong> ${result.build_id}</p>
            <p><strong>Timestamp:</strong> ${new Date(result.timestamp).toLocaleString()}</p>
            <p>${result.summary}</p>
        </div>
        
        <div class="preconditions-list">
            <h3>Precondition Results (${result.preconditions.length})</h3>
            ${result.preconditions.map((pc, i) => renderPrecondition(pc, i + 1)).join('')}
        </div>
        
        <p style="margin-top: 1rem; color: var(--secondary-color);">
            <strong>Evidence Package:</strong> <code>${result.evidence_path}</code>
        </p>
    `;
    
    elements.gateResultContainer.innerHTML = html;
    elements.resultsPanel.style.display = 'block';
}

function renderPrecondition(pc, index) {
    const statusClass = pc.status.toLowerCase();
    const icon = pc.status === 'SATISFIED' ? '✅' : '❌';
    
    let blockersHtml = '';
    if (pc.blocking_conditions && pc.blocking_conditions.length > 0) {
        blockersHtml = `
            <div class="blocking-conditions">
                <h5>🚫 Blocking Conditions:</h5>
                <ul>
                    ${pc.blocking_conditions.map(bc => `<li>${bc}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    return `
        <div class="precondition-item ${statusClass}">
            <h4>${icon} ${index}. ${pc.name}</h4>
            <p>${pc.message}</p>
            <p style="margin-top: 0.5rem;">
                <strong>Evidence found:</strong> ${pc.evidence_count} file(s)
            </p>
            ${blockersHtml}
        </div>
    `;
}

async function executeBuild() {
    if (!state.selectedBuildId) {
        showError('Please select a build');
        return;
    }
    
    if (!confirm(`Are you sure you want to execute build: ${state.selectedBuildId}?`)) {
        return;
    }
    
    try {
        setLoading(elements.executeBtn, true);
        
        const response = await fetch(`${API_BASE}/builds/${state.selectedBuildId}/execute`, {
            method: 'POST'
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || 'Execution failed');
        }
        
        const result = await response.json();
        showSuccess(`Build execution authorized: ${result.message}`);
        
    } catch (error) {
        console.error('Error executing build:', error);
        showError('Execution failed: ' + error.message);
    } finally {
        setLoading(elements.executeBtn, false);
    }
}

async function loadBuildStatus(buildId) {
    try {
        const response = await fetch(`${API_BASE}/builds/${buildId}/status`);
        if (!response.ok) throw new Error('Failed to load status');
        
        const status = await response.json();
        displayBuildStatus(status);
        elements.statusPanel.style.display = 'block';
    } catch (error) {
        console.error('Error loading build status:', error);
        elements.statusPanel.style.display = 'none';
    }
}

function displayBuildStatus(status) {
    let html = `
        <div class="gate-result ${status.status === 'PASS' ? 'pass' : 'fail'}">
            <h3>Status: ${status.status}</h3>
            <p><strong>Build ID:</strong> ${status.build_id}</p>
    `;
    
    if (status.timestamp) {
        html += `<p><strong>Last Updated:</strong> ${new Date(status.timestamp).toLocaleString()}</p>`;
    }
    
    if (status.summary) {
        html += `<p>${status.summary}</p>`;
    } else {
        html += `<p>${status.message}</p>`;
    }
    
    html += `</div>`;
    
    elements.statusContainer.innerHTML = html;
}

// Modal Functions

function showBlockerModal(result) {
    const failedPreconditions = result.preconditions.filter(pc => pc.status === 'FAILED');
    
    let html = `
        <p>The build cannot proceed due to ${failedPreconditions.length} failed precondition(s):</p>
        <div style="margin-top: 1rem;">
    `;
    
    failedPreconditions.forEach((pc, i) => {
        html += `
            <div style="margin-bottom: 1rem; padding: 1rem; background: white; border-radius: 4px;">
                <h4>${i + 1}. ${pc.name}</h4>
                <ul>
                    ${pc.blocking_conditions.map(bc => `<li>${bc}</li>`).join('')}
                </ul>
            </div>
        `;
    });
    
    html += `</div>`;
    
    elements.blockerDetails.innerHTML = html;
    elements.blockerModal.style.display = 'block';
}

function closeModal() {
    elements.blockerModal.style.display = 'none';
}

function showRemediationActions() {
    alert('Remediation routing to FM/Governance agents is not yet implemented in this scope.\n\n' +
          'Current blocking conditions have been logged to evidence package.\n\n' +
          'Escalate to governance team for resolution.');
}

// Utility Functions

async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        if (response.ok) {
            console.log('Build Control API is healthy');
        }
    } catch (error) {
        console.error('API health check failed:', error);
        showError('Warning: Cannot connect to Build Control API');
    }
}

function setLoading(button, isLoading) {
    if (isLoading) {
        button.dataset.originalText = button.textContent;
        button.innerHTML = '<span class="loading"></span> Loading...';
        button.disabled = true;
    } else {
        button.textContent = button.dataset.originalText || button.textContent;
        button.disabled = false;
    }
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    const main = document.querySelector('main');
    main.insertBefore(errorDiv, main.firstChild);
    
    setTimeout(() => errorDiv.remove(), 5000);
}

function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = message;
    
    const main = document.querySelector('main');
    main.insertBefore(successDiv, main.firstChild);
    
    setTimeout(() => successDiv.remove(), 5000);
}
