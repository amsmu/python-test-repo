from flask import Blueprint, request, jsonify, render_template_string, session
from auth_service import AuthService
from database_service import DatabaseService
from file_upload import FileUploadService
import json
import pickle
import base64
import os
import subprocess
from urllib.parse import unquote

api = Blueprint('api', __name__)
auth_service = AuthService()
db_service = DatabaseService()
file_service = FileUploadService()

@api.route('/login', methods=['POST'])
def login():
    # SECURITY ISSUE: No CSRF protection
    # SECURITY ISSUE: No rate limiting
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing credentials'}), 400
    
    username = data['username']
    password = data['password']
    
    user = auth_service.authenticate_user(username, password)
    if user:
        token = auth_service.create_token(user['id'], user['username'], user['is_admin'])
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['is_admin'] = user['is_admin']
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': user
        })
    
    return jsonify({'error': 'Invalid credentials'}), 401

@api.route('/profile', methods=['GET'])
def get_profile():
    # SECURITY ISSUE: No proper authentication check
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # SECURITY ISSUE: No authorization check
    target_user_id = request.args.get('user_id', user_id)
    
    # SECURITY ISSUE: SQL injection vulnerability
    query = f"SELECT * FROM users WHERE id = {target_user_id}"
    result = db_service.execute_raw_query(query)
    
    if result:
        return jsonify({'user': result[0]})
    
    return jsonify({'error': 'User not found'}), 404

@api.route('/search', methods=['GET'])
def search_users():
    # SECURITY ISSUE: No authentication required
    search_term = request.args.get('q', '')
    
    # SECURITY ISSUE: No input sanitization
    if not search_term:
        return jsonify({'error': 'Search term required'}), 400
    
    users = db_service.search_users(search_term)
    return jsonify({'users': users})

@api.route('/admin/execute', methods=['POST'])
def execute_query():
    # SECURITY ISSUE: Extremely dangerous - allows execution of any SQL query
    if not session.get('is_admin'):
        return jsonify({'error': 'Admin access required'}), 403
    
    data = request.get_json()
    query = data.get('query', '')
    
    # SECURITY ISSUE: No query validation
    results = db_service.execute_raw_query(query)
    return jsonify({'results': results})

@api.route('/template', methods=['POST'])
def render_template():
    # SECURITY ISSUE: Server-side template injection
    data = request.get_json()
    template = data.get('template', '')
    
    # SECURITY ISSUE: No template validation
    try:
        rendered = render_template_string(template)
        return jsonify({'rendered': rendered})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/deserialize', methods=['POST'])
def deserialize_data():
    # SECURITY ISSUE: Insecure deserialization
    data = request.get_json()
    serialized_data = data.get('data', '')
    
    try:
        # SECURITY ISSUE: Using pickle for deserialization
        decoded_data = base64.b64decode(serialized_data)
        deserialized = pickle.loads(decoded_data)
        return jsonify({'deserialized': str(deserialized)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/command', methods=['POST'])
def execute_command():
    # SECURITY ISSUE: Command injection vulnerability
    data = request.get_json()
    command = data.get('command', '')
    
    # SECURITY ISSUE: No command validation
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        return jsonify({
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/eval', methods=['POST'])
def evaluate_code():
    # SECURITY ISSUE: Code injection vulnerability
    data = request.get_json()
    code = data.get('code', '')
    
    # SECURITY ISSUE: No code validation
    try:
        result = eval(code)
        return jsonify({'result': str(result)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500 