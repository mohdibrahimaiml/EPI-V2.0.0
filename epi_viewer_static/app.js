/**
 * EPI Viewer - Static JavaScript Application
 * 
 * Renders .epi workflow timeline with zero code execution.
 * All data is loaded from embedded JSON.
 */

// Load embedded data
function loadEPIData() {
    const dataScript = document.getElementById('epi-data');
    if (!dataScript) {
        console.error('EPI data not found');
        return null;
    }
    try {
        return JSON.parse(dataScript.textContent);
    } catch (e) {
        console.error('Failed to parse EPI data:', e);
        return null;
    }
}

// Render trust badge
function renderTrustBadge(manifest) {
    const badge = document.getElementById('trust-badge');
    if (!badge) return;

    const hasSig = manifest.signature != null;
    
    let badgeHTML;
    if (hasSig) {
        badgeHTML = `
            <div class="trust-badge inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                </svg>
                Signed
            </div>
        `;
    } else {
        badgeHTML = `
            <div class="trust-badge inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-yellow-100 text-yellow-800">
                <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
                </svg>
                Unsigned
            </div>
        `;
    }
    
    badge.innerHTML = badgeHTML;
}

// Render manifest summary
function renderManifest(manifest) {
    const summary = document.getElementById('manifest-summary');
    if (!summary) return;

    const created = new Date(manifest.created_at).toLocaleString();
    const filesCount = Object.keys(manifest.file_manifest || {}).length;

    summary.innerHTML = `
        <div>
            <div class="text-gray-500 text-xs uppercase tracking-wide">Workflow ID</div>
            <div class="font-mono text-xs mt-1 break-all">${manifest.workflow_id}</div>
        </div>
        <div>
            <div class="text-gray-500 text-xs uppercase tracking-wide">Created</div>
            <div class="mt-1">${created}</div>
        </div>
        <div>
            <div class="text-gray-500 text-xs uppercase tracking-wide">Command</div>
            <div class="font-mono text-xs mt-1 break-all bg-gray-50 p-2 rounded">${manifest.cli_command || 'N/A'}</div>
        </div>
        <div>
            <div class="text-gray-500 text-xs uppercase tracking-wide">Files</div>
            <div class="mt-1">${filesCount} captured</div>
        </div>
        <div>
            <div class="text-gray-500 text-xs uppercase tracking-wide">Spec Version</div>
            <div class="mt-1 font-mono text-xs">${manifest.spec_version}</div>
        </div>
    `;
}

// Render a single step based on its kind
function renderStep(step) {
    const { index, timestamp, kind, content } = step;
    const time = new Date(timestamp).toLocaleTimeString();

    // Common wrapper
    const wrapper = document.createElement('div');
    wrapper.className = 'step-card px-6 py-4';

    // Header
    const header = document.createElement('div');
    header.className = 'flex items-center justify-between mb-2';
    header.innerHTML = `
        <div class="flex items-center space-x-2">
            <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                #${index}
            </span>
            <span class="text-sm font-medium text-gray-900">${kind}</span>
        </div>
        <span class="text-xs text-gray-500">${time}</span>
    `;
    wrapper.appendChild(header);

    // Content based on kind
    const contentDiv = document.createElement('div');
    contentDiv.className = 'mt-3';

    if (kind === 'llm.request') {
        contentDiv.innerHTML = renderLLMRequest(content);
    } else if (kind === 'llm.response') {
        contentDiv.innerHTML = renderLLMResponse(content);
    } else if (kind === 'security.redaction') {
        contentDiv.innerHTML = renderRedaction(content);
    } else {
        // Generic JSON display
        contentDiv.innerHTML = `<pre class="text-xs bg-gray-50 p-3 rounded overflow-auto">${JSON.stringify(content, null, 2)}</pre>`;
    }

    wrapper.appendChild(contentDiv);
    return wrapper;
}

// Render LLM request
function renderLLMRequest(content) {
    const messages = content.messages || [];
    let html = `
        <div class="text-xs text-gray-600 mb-2">
            <span class="font-medium">${content.provider}</span> • 
            <span class="font-mono">${content.model}</span>
        </div>
    `;

    // Render messages as chat bubbles
    if (messages.length > 0) {
        html += '<div class="space-y-2">';
        for (const msg of messages) {
            const isUser = msg.role === 'user';
            const bgColor = isUser ? 'bg-blue-100' : 'bg-gray-100';
            const textColor = isUser ? 'text-blue-900' : 'text-gray-900';
            const align = isUser ? 'ml-auto' : 'mr-auto';
            
            html += `
                <div class="chat-bubble ${align} ${bgColor} ${textColor} rounded-lg px-4 py-2 text-sm">
                    <div class="text-xs font-medium mb-1 uppercase">${msg.role}</div>
                    <div class="whitespace-pre-wrap">${escapeHTML(msg.content)}</div>
                </div>
            `;
        }
        html += '</div>';
    }

    return html;
}

// Render LLM response
function renderLLMResponse(content) {
    const choices = content.choices || [];
    let html = `
        <div class="text-xs text-gray-600 mb-2">
            <span class="font-medium">${content.provider}</span> • 
            <span class="font-mono">${content.model}</span>
        </div>
    `;

    // Render response messages
    if (choices.length > 0) {
        html += '<div class="space-y-2">';
        for (const choice of choices) {
            html += `
                <div class="chat-bubble mr-auto bg-green-100 text-green-900 rounded-lg px-4 py-2 text-sm">
                    <div class="text-xs font-medium mb-1 uppercase">Assistant</div>
                    <div class="whitespace-pre-wrap">${escapeHTML(choice.message.content)}</div>
                    ${choice.finish_reason ? `<div class="text-xs text-green-700 mt-2">• ${choice.finish_reason}</div>` : ''}
                </div>
            `;
        }
        html += '</div>';
    }

    // Usage stats
    if (content.usage) {
        html += `
            <div class="mt-3 text-xs text-gray-600 flex items-center space-x-4">
                <span>📊 ${content.usage.total_tokens} tokens</span>
                <span>⚡ ${content.latency_seconds}s</span>
            </div>
        `;
    }

    return html;
}

// Render redaction event
function renderRedaction(content) {
    return `
        <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-3 text-sm">
            <div class="flex items-center text-yellow-800">
                <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd"/>
                </svg>
                <span class="font-medium">Secrets Redacted</span>
            </div>
            <div class="mt-2 text-yellow-700">
                ${content.count} sensitive value(s) removed from <span class="font-mono text-xs">${content.target_step}</span>
            </div>
        </div>
    `;
}

// Escape HTML to prevent XSS
function escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// Render timeline
function renderTimeline(steps) {
    const timeline = document.getElementById('timeline');
    if (!timeline) return;

    if (steps.length === 0) {
        timeline.innerHTML = `
            <div class="px-6 py-12 text-center text-gray-500">
                No steps recorded
            </div>
        `;
        return;
    }

    timeline.innerHTML = '';
    for (const step of steps) {
        timeline.appendChild(renderStep(step));
    }
}

// Initialize viewer
function init() {
    const data = loadEPIData();
    if (!data) {
        document.body.innerHTML = `
            <div class="min-h-screen flex items-center justify-center">
                <div class="text-center">
                    <h1 class="text-2xl font-bold text-red-600 mb-2">Failed to load EPI data</h1>
                    <p class="text-gray-600">The embedded data could not be parsed.</p>
                </div>
            </div>
        `;
        return;
    }

    renderTrustBadge(data.manifest);
    renderManifest(data.manifest);
    renderTimeline(data.steps);
}

// Run on load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
