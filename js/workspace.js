// workspace.js - Handles workspace creation and listing

document.addEventListener('DOMContentLoaded', () => {
    const ingestForm = document.getElementById('ingestForm');
    if (ingestForm) {
        ingestForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const workspaceName = document.getElementById('workspaceName').value;
            const description = document.getElementById('workspaceDesc') ? document.getElementById('workspaceDesc').value : '';
            const repoUrl = document.getElementById('repoUrl').value;
            
            console.log(`Creating workspace: ${workspaceName} from ${repoUrl}`);
            
            // Show loading state
            const btn = ingestForm.querySelector('button[type="submit"]');
            btn.innerText = 'Fetching Repository (This may take a moment)...';
            btn.disabled = true;

            const token = localStorage.getItem('token');
            if (!token) {
                alert("You must be logged in to create a workspace.");
                window.location.href = 'login.html';
                return;
            }

            fetch('http://localhost:5000/api/workspace/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ name: workspaceName, description, repoUrl })
            })
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    alert(`Error creating workspace: ${data.error}`);
                    btn.innerText = 'Create & Analyze Repository';
                    btn.disabled = false;
                } else {
                    // Mark that user has a workspace for the dashboard empty state
                    localStorage.setItem('hasWorkspace', 'true');
                    localStorage.setItem('lastWorkspaceName', workspaceName);
                    localStorage.setItem('currentWorkspaceId', data.workspace.id);
                    
                    // Redirect to workspace details
                    window.location.href = 'workspace-detail.html';
                }
            })
            .catch(err => {
                console.error(err);
                alert("Failed to connect to the server.");
                btn.innerText = 'Create & Analyze Repository';
                btn.disabled = false;
            });
        });
    }

    // Function to fetch and render workspaces list
    function loadWorkspaces() {
        // Hide Getting Started section if workspace exists
        const gettingStarted = document.getElementById('gettingStartedSection');
        if (gettingStarted && localStorage.getItem('hasWorkspace') === 'true') {
            gettingStarted.style.display = 'none';
            
            const workspaceName = localStorage.getItem('lastWorkspaceName');

            // Update Metrics
            const token = localStorage.getItem('token');
            if (token) {
                fetch('http://localhost:5000/api/workspace/stats', {
                    headers: { 'Authorization': `Bearer ${token}` }
                })
                .then(res => res.json())
                .then(stats => {
                    if (!stats.error) {
                        const metrics = document.querySelectorAll('.metric-value');
                        if (metrics.length >= 4) {
                            metrics[0].innerText = stats.total_workspaces;
                            metrics[1].innerText = stats.repos_processed;
                            metrics[2].innerText = stats.generated_artifacts;
                            metrics[3].innerText = stats.total_chats;
                        }
                    }
                })
                .catch(err => console.error("Error fetching stats:", err));
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
    loadWorkspacesPage();

    // Logic for workspaces.html specific view
    function loadWorkspacesPage() {
        const emptyState = document.getElementById('workspacesEmptyState');
        const populatedState = document.getElementById('workspacesPopulatedState');
        if (!emptyState || !populatedState) return;

        const hasWorkspace = localStorage.getItem('hasWorkspace') === 'true';
        const workspaceName = localStorage.getItem('lastWorkspaceName');

        if (hasWorkspace && workspaceName) {
            emptyState.style.display = 'none';
            populatedState.style.display = 'block';

            const token = localStorage.getItem('token');
            if (token) {
                fetch('http://localhost:5000/api/workspace/stats', {
                    headers: { 'Authorization': `Bearer ${token}` }
                })
                .then(res => res.json())
                .then(stats => {
                    if (!stats.error) {
                        document.getElementById('statTotalWorkspaces').innerText = stats.total_workspaces;
                        document.getElementById('statRepositories').innerText = stats.repos_processed;
                        document.getElementById('statArtifacts').innerText = stats.generated_artifacts;
                        document.getElementById('statChats').innerText = stats.total_chats;
                    }
                })
                .catch(err => console.error("Error fetching stats:", err));
            } else {
                document.getElementById('statTotalWorkspaces').innerText = '1';
                document.getElementById('statRepositories').innerText = '1';
                document.getElementById('statArtifacts').innerText = '0';
                document.getElementById('statChats').innerText = '0';
            }

            const workspacesList = document.getElementById('workspacesList');
            workspacesList.innerHTML = `
                <div class="card glow-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                        <h3 style="margin: 0; font-size: 1.25rem;">${workspaceName}</h3>
                        <span class="text-muted" style="font-size: 0.75rem;">Active just now</span>
                    </div>
                    <div style="margin-bottom: 1.5rem;">
                        <span class="tech-badge">Python</span>
                        <span class="tech-badge">Flask</span>
                        <span class="tech-badge">MongoDB</span>
                    </div>
                    <div class="grid grid-cols-3 mb-4" style="gap: 1rem;">
                        <div>
                            <div class="text-muted" style="font-size: 0.75rem; text-transform: uppercase;">Repos</div>
                            <div style="font-weight: 600;">1</div>
                        </div>
                        <div>
                            <div class="text-muted" style="font-size: 0.75rem; text-transform: uppercase;">Artifacts</div>
                            <div style="font-weight: 600;">0</div>
                        </div>
                        <div>
                            <div class="text-muted" style="font-size: 0.75rem; text-transform: uppercase;">Chats</div>
                            <div style="font-weight: 600;">0</div>
                        </div>
                    </div>
                    <a href="workspace-detail.html" class="btn btn-secondary text-center" style="width: 100%; display: block;">Open Workspace</a>
                </div>
            `;

            const activityLog = document.getElementById('activityLog');
            activityLog.innerHTML = `
                <div class="activity-item">
                    <div class="activity-icon"></div>
                    <div class="activity-content">
                        <h4>Workspace Created</h4>
                        <p>${workspaceName} was initialized.</p>
                    </div>
                </div>
                <div class="activity-item">
                    <div class="activity-icon" style="border-color: var(--success);"></div>
                    <div class="activity-content">
                        <h4>Analysis Completed</h4>
                        <p>Repository scan finished successfully.</p>
                    </div>
                </div>
            `;
        } else {
            emptyState.style.display = 'block';
            populatedState.style.display = 'none';
        }
    }
});
