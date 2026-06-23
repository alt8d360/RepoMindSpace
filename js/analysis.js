// analysis.js - Handles repository analysis data fetching and display

document.addEventListener('DOMContentLoaded', () => {
    
    // Function to animate the circular progress indicator
    function animateProgress() {
        const circle = document.getElementById('progressCircle');
        const value = document.getElementById('progressValue');
        if (!circle || !value) return;

        // The circle's stroke-dasharray is 339.292 (2 * pi * 54)
        const circumference = 339.292;
        
        // Define animation steps
        const steps = [
            { percent: 0, delay: 0 },
            { percent: 40, delay: 500 },
            { percent: 75, delay: 1500 },
            { percent: 100, delay: 2200 }
        ];

        steps.forEach(step => {
            setTimeout(() => {
                const offset = circumference - (step.percent / 100) * circumference;
                circle.style.strokeDashoffset = offset;
                
                // Animate text counter
                let currentVal = parseInt(value.innerText) || 0;
                const targetVal = step.percent;
                const diff = targetVal - currentVal;
                const stepTime = Math.max(20, 500 / (diff || 1));
                
                if (diff > 0) {
                    let counter = currentVal;
                    const timer = setInterval(() => {
                        counter += 1;
                        value.innerText = `${counter}%`;
                        if (counter >= targetVal) clearInterval(timer);
                    }, stepTime);
                }
            }, step.delay);
        });
    }

    // Function to fetch repository analysis data
    function loadAnalysisData() {
        console.log('Fetching analysis data for the current workspace...');
        
        const workspaceName = localStorage.getItem('lastWorkspaceName') || 'siya';

        // Update Repo Name Badges/Headers
        const metaRepoName = document.getElementById('metaRepoName');
        if (metaRepoName) metaRepoName.innerText = workspaceName;

        // Trigger the progress animation
        animateProgress();
    }

    // Only run if we are on the workspace detail page
    if (document.getElementById('metaRepoName') || document.getElementById('progressCircle')) {
        loadAnalysisData();
    }
});
