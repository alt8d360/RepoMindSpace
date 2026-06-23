from flask import Blueprint, request, jsonify, current_app
from models.user import create_user, get_user_by_email, verify_password
import jwt
import datetime
import os
from google.oauth2 import id_token
from google.auth.transport import requests

auth_bp = Blueprint('auth', __name__)

def generate_jwt(user_id):
    secret = current_app.config['JWT_SECRET']
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, secret, algorithm='HS256')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')
    password = data.get('password')

    if not all([first_name, last_name, email, password]):
        return jsonify({"error": "All fields are required"}), 400

    db = current_app.config['DB']
    user, error = create_user(db, first_name, last_name, email, password=password)
    
    if error:
        return jsonify({"error": error}), 409
    
    token = generate_jwt(user['_id'])
    return jsonify({
        "message": "User registered successfully",
        "token": token,
        "user": {"id": user['_id'], "email": user['email'], "first_name": user['first_name'], "last_name": user['last_name']}
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({"error": "Email and password are required"}), 400

    db = current_app.config['DB']
    user = get_user_by_email(db, email)
    
    if not user or not user.get('password_hash'):
        return jsonify({"error": "Invalid email or password"}), 401

    if not verify_password(password, user['password_hash']):
        return jsonify({"error": "Invalid email or password"}), 401

    token = generate_jwt(user['_id'])
    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": {"id": user['_id'], "email": user['email'], "first_name": user['first_name'], "last_name": user['last_name']}
    }), 200

@auth_bp.route('/google', methods=['POST'])
def google_auth():
    data = request.get_json()
    token = data.get('credential')

    if not token:
        return jsonify({"error": "No token provided"}), 400

    client_id = current_app.config['GOOGLE_CLIENT_ID']

    try:
        # Verify the Google token (added clock_skew_in_seconds to fix intermittent sync issues)
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), client_id, clock_skew_in_seconds=10)

        # Token is valid, extract user info
        email = idinfo['email']
        google_id = idinfo['sub']
        first_name = idinfo.get('given_name', '')
        last_name = idinfo.get('family_name', '')
        picture = idinfo.get('picture', '')

        # --- MOCK DATABASE BYPASS ---
        # Since we agreed not to touch the database until all features are on,
        # we will simply mock the user object and return a valid JWT so the UI can proceed.
        user = {
            '_id': 'mocked_user_id_12345',
            'email': email,
            'first_name': first_name,
            'last_name': last_name
        }

        # Generate our own JWT
        jwt_token = generate_jwt(user['_id'])
        
        return jsonify({
            "message": "Google Login successful",
            "token": jwt_token,
            "user": {"id": user['_id'], "email": user['email'], "first_name": user['first_name'], "last_name": user['last_name']}
        }), 200

    except ValueError as e:
        # Invalid token
        return jsonify({"error": f"Invalid token: {str(e)}"}), 401
