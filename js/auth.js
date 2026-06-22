// auth.js - Handles authentication logic

const API_BASE_URL = 'http://localhost:5000/api/auth';
const GOOGLE_CLIENT_ID = '1091939061408-1rpl2tqd6tn2iulba1oo8v1cfh94t4bs.apps.googleusercontent.com';

document.addEventListener('DOMContentLoaded', () => {
    
    // --- Traditional Login ---
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            try {
                const response = await fetch(`${API_BASE_URL}/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                
                const data = await response.json();
                if (response.ok) {
                    localStorage.setItem('token', data.token);
                    window.location.href = 'dashboard.html';
                } else {
                    alert(data.error || 'Login failed');
                }
            } catch (error) {
                console.error('Error logging in:', error);
                alert('An error occurred during login.');
            }
        });
    }

    // --- Traditional Registration ---
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const firstName = document.getElementById('firstName').value;
            const lastName = document.getElementById('lastName').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            try {
                const response = await fetch(`${API_BASE_URL}/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ firstName, lastName, email, password })
                });
                
                const data = await response.json();
                if (response.ok) {
                    localStorage.setItem('token', data.token);
                    window.location.href = 'dashboard.html';
                } else {
                    alert(data.error || 'Registration failed');
                }
            } catch (error) {
                console.error('Error registering:', error);
                alert('An error occurred during registration.');
            }
        });
    }

    // --- Google Identity Services (GIS) Logic ---
    function handleGoogleResponse(response) {
        console.log("Encoded JWT ID token: " + response.credential);
        
        fetch(`${API_BASE_URL}/google`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ credential: response.credential })
        })
        .then(res => res.json())
        .then(data => {
            if (data.token) {
                localStorage.setItem('token', data.token);
                window.location.href = 'dashboard.html';
            } else {
                alert(data.error || 'Google login failed');
            }
        })
        .catch(err => {
            console.error('Error during Google Auth:', err);
            alert('Failed to connect to authentication server.');
        });
    }

    window.initGoogleAuth = function() {
        console.log("Google library loaded, initializing...");
        google.accounts.id.initialize({
            client_id: GOOGLE_CLIENT_ID,
            callback: handleGoogleResponse
        });

        // Instead of relying on the unreliable One-Tap prompt(), we render the official Google button.
        const renderOfficialButton = (btnId) => {
            const btn = document.getElementById(btnId);
            if (btn) {
                // Clear the custom SVG and text
                btn.innerHTML = '';
                // Render the official Google button directly inside the element
                google.accounts.id.renderButton(btn, { 
                    theme: "filled_black", 
                    size: "large", 
                    width: btn.offsetWidth || 300,
                    text: "continue_with"
                });
            }
        };

        renderOfficialButton('googleSignInBtn');
        renderOfficialButton('googleSignUpBtn');
    };

    // If script loaded synchronously
    if (typeof google !== 'undefined') {
        window.initGoogleAuth();
    }

    // --- Forgot Password / Logout Placeholders ---
    const forgotPasswordForm = document.getElementById('forgotPasswordForm');
    if (forgotPasswordForm) {
        forgotPasswordForm.addEventListener('submit', (e) => {
            e.preventDefault();
            alert('Password reset link sent to your email.');
        });
    }

    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            localStorage.removeItem('token');
            window.location.href = '../index.html';
        });
    }
});
