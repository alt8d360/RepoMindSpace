from flask import Blueprint, request, jsonify, current_app
import os
import subprocess
import uuid
import datetime
import jwt
from functools import wraps

workspace_bp = Blueprint('workspace', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Check Authorization header
        if 'Authorization' in request.headers:
            parts = request.headers['Authorization'].split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]
        
        if not token:
            return jsonify({'error': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=["HS256"])
            # Pass user_id to the route
            request.user_id = data['user_id']
        except Exception as e:
            return jsonify({'error': 'Token is invalid!'}), 401
            
        return f(*args, **kwargs)
    return decorated

@workspace_bp.route('/create', methods=['POST'])
@token_required
def create_workspace():
    data = request.get_json()
    
    workspace_name = data.get('name')
    description = data.get('description', '')
    repo_url = data.get('repoUrl')
    
    if not workspace_name or not repo_url:
        return jsonify({'error': 'Workspace name and Repository URL are required.'}), 400
        
    workspace_id = str(uuid.uuid4())
    user_id = request.user_id
    db = current_app.config['DB']
    
    # Base directory for workspaces
    workspaces_base_dir = os.path.join(os.getcwd(), 'data', 'workspaces')
    os.makedirs(workspaces_base_dir, exist_ok=True)
    
    # Specific workspace directory
    workspace_dir = os.path.join(workspaces_base_dir, workspace_id)
    
    # Try to clone the repository
    try:
        github_token = os.getenv('GITHUB_TOKEN')
        clone_url = repo_url
        if github_token and 'github.com' in repo_url:
            if repo_url.startswith('https://github.com'):
                clone_url = repo_url.replace('https://github.com', f'https://{github_token}@github.com')
            elif repo_url.startswith('http://github.com'):
                clone_url = repo_url.replace('http://github.com', f'http://{github_token}@github.com')

        # Run git clone
        process = subprocess.run(
            ['git', 'clone', clone_url, workspace_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if process.returncode != 0:
            return jsonify({'error': f'Failed to clone repository: {process.stderr}'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Exception during clone: {str(e)}'}), 500
        
    # Repository successfully cloned, save metadata to MongoDB
    new_workspace = {
        '_id': workspace_id,
        'user_id': user_id,
        'name': workspace_name,
        'description': description,
        'repo_url': repo_url,
        'local_path': workspace_dir,
        'status': 'ready',
        'created_at': datetime.datetime.utcnow()
    }
    
    try:
        db.workspaces.insert_one(new_workspace)
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
        
    return jsonify({
        'message': 'Workspace created successfully',
        'workspace': {
            'id': workspace_id,
            'name': workspace_name,
            'status': 'ready'
        }
    }), 201

@workspace_bp.route('/<workspace_id>', methods=['GET'])
@token_required
def get_workspace(workspace_id):
    db = current_app.config['DB']
    user_id = request.user_id
    
    workspace = db.workspaces.find_one({'_id': workspace_id, 'user_id': user_id})
    if not workspace:
        return jsonify({'error': 'Workspace not found or unauthorized'}), 404
        
    local_path = workspace.get('local_path')
    
    total_files = 0
    extensions_count = {}
    
    if local_path and os.path.exists(local_path):
        for root, dirs, files in os.walk(local_path):
            # Skip common unnecessary directories
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'venv', '__pycache__']]
            
            for file in files:
                total_files += 1
                _, ext = os.path.splitext(file)
                if ext:
                    ext = ext.lower()
                    extensions_count[ext] = extensions_count.get(ext, 0) + 1
                    
    # Simple mapping of extensions to technologies
    tech_mapping = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.html': 'HTML',
        '.css': 'CSS',
        '.java': 'Java',
        '.go': 'Go',
        '.rs': 'Rust',
        '.cpp': 'C++',
        '.c': 'C',
        '.md': 'Markdown',
        '.json': 'JSON'
    }
    
    technologies = []
    # Sort extensions by frequency
    sorted_exts = sorted(extensions_count.items(), key=lambda item: item[1], reverse=True)
    
    for ext, count in sorted_exts:
        if ext in tech_mapping:
            tech_name = tech_mapping[ext]
            if tech_name not in technologies:
                technologies.append(tech_name)
        if len(technologies) >= 5:
            break
            
    if not technologies:
        technologies = ['Unknown']
        
    return jsonify({
        'id': workspace['_id'],
        'name': workspace['name'],
        'description': workspace.get('description', ''),
        'repo_url': workspace.get('repo_url', ''),
        'status': workspace.get('status', 'unknown'),
        'total_files': total_files,
        'technologies': technologies
    }), 200

@workspace_bp.route('/stats', methods=['GET'])
@token_required
def get_stats():
    db = current_app.config['DB']
    user_id = request.user_id
    
    total_workspaces = db.workspaces.count_documents({'user_id': user_id})
    repos_processed = db.workspaces.count_documents({'user_id': user_id, 'status': 'completed'})
    generated_artifacts = db.artifacts.count_documents({'user_id': user_id})
    total_chats = db.chats.count_documents({'user_id': user_id})
    
    # If a workspace exists, it processes a repo, so let's just make it equal to workspaces if it's 0 but workspace is 1
    if repos_processed == 0 and total_workspaces > 0:
        repos_processed = total_workspaces
        
    return jsonify({
        'total_workspaces': total_workspaces,
        'repos_processed': repos_processed,
        'generated_artifacts': generated_artifacts,
        'total_chats': total_chats
    }), 200

