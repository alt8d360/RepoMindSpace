// workspace.js - Handles workspace creation and listing

document.addEventListener('DOMContentLoaded', () => {
    const ingestForm = document.getElementById('ingestForm');
    if (ingestForm) {
        ingestForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const workspaceName = document.getElementById('workspaceName').value;
            console.log(`Creating workspace: ${workspaceName}`);
            
            // Show loading state, call API, then redirect
            const btn = ingestForm.querySelector('button[type="submit"]');
            btn.innerText = 'Analyzing Repository...';
            btn.disabled = true;

            // Mark that user has a workspace for the dashboard empty state
            localStorage.setItem('hasWorkspace', 'true');
            localStorage.setItem('lastWorkspaceName', workspaceName);

            setTimeout(() => {
                window.location.href = 'workspace-detail.html';
            }, 1500); // Dummy delay
        });
    }

    // Function to fetch and render workspaces list
    function loadWorkspaces() {
        // Hide Getting Started section if workspace exists
        const gettingStarted = document.getElementById('gettingStartedSection');
        if (gettingStarted && localStorage.getItem('hasWorkspace') === 'true') {
            gettingStarted.style.display = 'none';
            
            const workspaceName = localStorage.getItem('lastWorkspaceName');

            // Update Metrics (assuming they are the first two .metric-value elements)
            const metrics = document.querySelectorAll('.metric-value');
            if (metrics.length >= 2) {
                metrics[0].innerText = '1';
                metrics[1].innerText = '1';
            }

            // Update Recent Activity
            const recentActivityList = document.getElementById('recentActivityList');
            if (recentActivityList) {
                recentActivityList.innerHTML = `
                    <div style="display: flex; align-items: flex-start; gap: 1rem; margin-bottom: 1.5rem;">
                        <div style="color: var(--success); padding: 0.25rem;"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg></div>
                        <div>
                            <p class="mb-1" style="font-weight: 500;">Workspace <strong>${workspaceName}</strong> created</p>
                            <span class="text-muted" style="font-size: 0.875rem;">Just now</span>
                        </div>
                    </div>
                    <div style="display: flex; align-items: flex-start; gap: 1rem;">
                        <div style="color: var(--success); padding: 0.25rem;"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg></div>
                        <div>
                            <p class="mb-1" style="font-weight: 500;">Repository analysis completed</p>
                            <span class="text-muted" style="font-size: 0.875rem;">Just now</span>
                        </div>
                    </div>
                `;
            }

            // Update Recent Repositories
            const recentReposList = document.getElementById('recentReposList');
            if (recentReposList) {
                recentReposList.innerHTML = `
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 0.75rem; display: flex; justify-content: space-between; align-items: center; transition: all 0.2s;">
                        <div>
                            <h4 class="mb-1" style="font-size: 1.125rem;">${workspaceName}</h4>
                            <span class="text-muted" style="font-size: 0.875rem;">JavaScript • HTML • CSS</span>
                        </div>
                        <a href="workspace-detail.html" class="btn btn-secondary" style="padding: 0.5rem 1rem; font-size: 0.875rem;">View</a>
                    </div>
                `;
            }
        }
    }

    loadWorkspaces();
});
