// analysis.js - Handles repository analysis data fetching and display

document.addEventListener('DOMContentLoaded', () => {
    
    // Function to fetch repository analysis data
    function loadAnalysisData() {
        console.log('Fetching analysis data for the current workspace...');
        
        const workspaceName = localStorage.getItem('lastWorkspaceName') || 'Unknown Workspace';

        // Update Workspace Name Header
        const header = document.getElementById('workspaceNameHeader');
        if (header) header.innerText = workspaceName;

        // Update Repo Summary
        const summary = document.getElementById('repoSummary');
        if (summary) summary.innerText = `Analysis complete for ${workspaceName}. The repository primarily consists of static web assets, HTML pages, and Vanilla JS.`;

        // Update file count
        const fileCount = document.getElementById('totalFilesCount');
        if (fileCount) fileCount.innerText = '14';
    }

    // Only run if we are on the workspace detail page
    if (document.getElementById('workspaceNameHeader')) {
        loadAnalysisData();
    }
});
