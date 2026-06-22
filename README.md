# RepoMind Space

RepoMind Space is an AI-powered repository intelligence platform designed to help developers understand, analyze, document, and manage software repositories.

This document outlines the recent architectural changes, specifically the introduction of the Flask backend, MongoDB integration, and the implementation of Google Identity Services for authentication.

---

## Recent Updates & Changes

### 1. Backend Infrastructure Introduced
A Python Flask backend has been established to handle API requests securely, decoupling the database logic from the frontend.
*   **`app.py`**: The main Flask entry point. It handles CORS, connects to the MongoDB cluster via connection strings in the `.env` file, and registers all API blueprints.
*   **`requirements.txt`**: Added to manage backend dependencies (`Flask`, `pymongo`, `bcrypt`, `PyJWT`, `google-auth`, etc.).
*   **`models/user.py`**: Contains the MongoDB schema helper functions (`create_user`, `get_user_by_email`). It safely hashes passwords using `bcrypt` before storing them.
*   **`routes/auth.py`**: Implements the core authentication API endpoints:
    *   `POST /api/auth/register`
    *   `POST /api/auth/login`
    *   `POST /api/auth/google`

### 2. Google OAuth 2.0 Integration (Identity Services)
We implemented a highly secure Google Sign-In flow where Google acts strictly as the Identity Provider (IdP), and our MongoDB handles the actual user records and sessions.
*   **Frontend**: Utilizes the official Google Identity Services (GIS) library to render the Google button and fetch an ID Token.
*   **Backend**: The Flask server receives the ID Token, verifies its cryptographic signature using the `google-auth` library, auto-creates the user in MongoDB if they don't exist, and returns a custom JWT session token.

### 3. Frontend UI Modifications
To support the new authentication flow, the following UI changes were made:
*   **Apple Sign-In Removed**: The Apple sign-in buttons were removed from both `login.html` and `register.html` as requested.
*   **`js/auth.js` Rewritten**:
    *   The placeholder login/register logic was replaced with actual `fetch()` calls pointing to the new Flask endpoints (`http://localhost:5000/api/auth/...`).
    *   Added logic to load the Google GIS library asynchronously.
    *   Replaced the custom Google SVG buttons with the official `google.accounts.id.renderButton` to bypass browser popup blockers and Google's cooldown periods, ensuring guaranteed reliable popups.
*   **Script Tags Added**: Injected `<script src="https://accounts.google.com/gsi/client?onload=initGoogleAuth" async defer></script>` into the HTML heads.

---

## Getting Started (Development Setup)

### Prerequisites
*   Python 3.10+
*   MongoDB Atlas Account
*   Google Cloud Console Account (for the Client ID)

### 1. Environment Setup
Create a `.env` file in the root directory and ensure it contains the following variables. **Never commit this file to version control.**

```env
# MongoDB Connection
MONGO_URI=mongodb+srv://<username>:<password>@<cluster-url>/?appName=RepoMindCluster
MONGO_DB_NAME=repomind_space

# Application Secrets
JWT_SECRET=your_super_secret_jwt_key_here
GOOGLE_CLIENT_ID=your_google_client_id_here
PORT=5000
FLASK_ENV=development
```

### 2. Running the Backend (Flask)
Open a terminal in the root directory:
```bash
# Install required Python dependencies
pip install -r requirements.txt

# Start the Flask server
python app.py
```
*The backend API will be available at `http://localhost:5000`.*

### 3. Running the Frontend
Open a separate terminal in the root directory:
```bash
# Serve the static HTML/JS files
python -m http.server 8000
```
*Access the application at `http://localhost:8000`.*
