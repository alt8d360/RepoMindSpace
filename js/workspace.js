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
            const originalText = btn.innerText;
            btn.innerText = 'Analyzing Repository...';
            btn.disabled = true;

            setTimeout(() => {
                window.location.href = 'workspace-detail.html';
            }, 1500); // Dummy delay
        });
    }

    // Function to fetch and render workspaces list
    function loadWorkspaces() {
        const list = document.getElementById('workspacesList');
        if (list) {
            console.log('Loading workspaces from API...');
            // API call goes here
        }
    }

    loadWorkspaces();
});
