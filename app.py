from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables (override=True ensures .env values take precedence)
load_dotenv(override=True)

def create_app():
    app = Flask(__name__)
    CORS(app) # Enable CORS for frontend requests

    # App Configuration from .env
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')
    app.config['MONGO_DB_NAME'] = os.getenv('MONGO_DB_NAME')
    app.config['JWT_SECRET'] = os.getenv('JWT_SECRET')
    app.config['GOOGLE_CLIENT_ID'] = os.getenv('GOOGLE_CLIENT_ID')

    # Initialize MongoDB Client
    client = MongoClient(app.config['MONGO_URI'])
    db = client[app.config['MONGO_DB_NAME']]
    app.config['DB'] = db # Store db in app config to pass to routes

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.workspace import workspace_bp
    from routes.artifact import artifact_bp
    from routes.chat import chat_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(workspace_bp, url_prefix='/api/workspace')
    app.register_blueprint(artifact_bp, url_prefix='/api/artifacts')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')

    @app.route('/')
    def index():
        return "RepoMind Space Backend is running."

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') == 'development')
