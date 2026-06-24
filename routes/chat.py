from flask import Blueprint, request, jsonify, current_app
import os
import time
import datetime
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from dotenv import load_dotenv
from utils.parser import LocalParser
from routes.workspace import token_required

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/ask', methods=['POST'])
@token_required
def ask_question():
    data = request.get_json()
    if not data or 'workspace_id' not in data or 'message' not in data:
        return jsonify({'error': 'Missing workspace_id or message'}), 400

    workspace_id = data['workspace_id']
    message = data['message']

    # 1. Get workspace info
    db = current_app.config['DB']
    user_id = request.user_id
    try:
        workspace = db.workspaces.find_one({'_id': workspace_id, 'user_id': user_id})
    except Exception:
        return jsonify({'error': 'Invalid workspace ID'}), 400

    if not workspace:
        return jsonify({'error': 'Workspace not found'}), 404

    local_path = workspace.get('local_path')
    if not local_path or not os.path.exists(local_path):
        return jsonify({'error': 'Local repository path not found. Please sync again.'}), 404

    try:
        # 2. Parse repository content
        parser = LocalParser(local_path)
        parsed_data = parser.parse()
        
        # Limit context to avoid token limits
        MAX_CHARS = 100000 
        context_string = ""
        
        for file_obj in parsed_data:
            if len(context_string) >= MAX_CHARS:
                context_string += "\n... (context truncated due to token limits) ...\n"
                break
                
            file_content = file_obj['content']
            if len(context_string) + len(file_content) > MAX_CHARS:
                allowed_chars = MAX_CHARS - len(context_string)
                context_string += f"\n--- {file_obj['path']} ---\n{file_content[:allowed_chars]}\n... (file truncated) ...\n"
                break
            else:
                context_string += f"\n--- {file_obj['path']} ---\n{file_content}\n"
            
        # 3. Setup Gemini (force load env)
        load_dotenv(override=True)
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not gemini_api_key:
            return jsonify({'error': 'Gemini API key is not configured.'}), 500
            
        genai.configure(api_key=gemini_api_key)
        # Using gemma-4-26b-a4b-it to avoid hitting the gemini-* daily free tier limits
        model = genai.GenerativeModel('gemma-4-26b-a4b-it')
            
        # 4. Build Prompt
        prompt = f"You are an expert AI pair programmer. Answer the user's question about their codebase.\n\n"
        prompt += f"User Question: {message}\n\n"
        prompt += f"Here is the codebase context:\n{context_string}"
        
        # 5. Generate Content with retry
        max_retries = 2
        retry_delay = 60 # seconds
        
        for attempt in range(max_retries):
            try:
                response = model.generate_content(prompt)
                generated_text = response.text
                
                # Save chat record for tracking/recent
                db.chats.insert_one({
                    'workspace_id': workspace_id,
                    'user_id': user_id,
                    'question': message,
                    'created_at': datetime.datetime.utcnow()
                })
                
                return jsonify({'answer': generated_text}), 200
            except ResourceExhausted as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    return jsonify({'error': f'Google API Rate Limit exceeded. Details: {str(e)}'}), 429

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/recent/<workspace_id>', methods=['GET'])
@token_required
def get_recent_chats(workspace_id):
    db = current_app.config['DB']
    user_id = request.user_id
    
    # Fetch top 5 recent questions for this workspace
    recent_chats = list(db.chats.find({'workspace_id': workspace_id, 'user_id': user_id}).sort('created_at', -1).limit(5))
    
    # Serialize ObjectId and datetime
    serialized_chats = []
    for chat in recent_chats:
        serialized_chats.append({
            'id': str(chat['_id']),
            'question': chat['question'],
            'created_at': chat['created_at'].isoformat()
        })
        
    return jsonify({'recent_questions': serialized_chats}), 200

