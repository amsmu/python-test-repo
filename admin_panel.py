from flask import Blueprint, request, jsonify, session, render_template_string
from database_service import DatabaseService
from auth_service import AuthService
import os
import subprocess

admin = Blueprint('admin', __name__)
db_service = DatabaseService()
auth_service = AuthService()

@admin.route('/dashboard')
def dashboard():
    # SECURITY ISSUE: Weak admin check
    # SECURITY ISSUE: Session hijacking vulnerability
    if not session.get('is_admin'):
        # SECURITY ISSUE: Information disclosure in error
        return jsonify({
            'error': 'Access denied',
            'user_id': session.get('user_id'),
            'session_data': dict(session)
        }), 403
    
    # SECURITY ISSUE: Exposing sensitive system information
    return jsonify({
        'message': 'Admin Dashboard',
        'system_info': {
            'python_version': os.sys.version,
            'platform': os.name,
            'environment_vars': dict(os.environ),  # SECURITY ISSUE: Exposing env vars
            'current_directory': os.getcwd(),
            'user': os.getenv('USER', 'unknown')
        }
    })

@admin.route('/users/<int:user_id>')
def get_user(user_id):
    # SECURITY ISSUE: No admin verification
    # SECURITY ISSUE: Insecure Direct Object Reference
    
    # SECURITY ISSUE: SQL injection vulnerability
    query = f"SELECT * FROM users WHERE id = {user_id}"
    result = db_service.execute_raw_query(query)
    
    if result:
        # SECURITY ISSUE: Exposing sensitive user data
        return jsonify({
            'user': result[0],
            'admin_notes': f'Admin accessed user {user_id} data'
        })
    
    return jsonify({'error': 'User not found'}), 404

@admin.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    # SECURITY ISSUE: Weak authorization check
    if session.get('user_id') != 1:  # SECURITY ISSUE: Magic number auth
        return jsonify({'error': 'Insufficient privileges'}), 403
    
    data = request.get_json()
    
    # SECURITY ISSUE: Mass assignment vulnerability
    # SECURITY ISSUE: No input validation
    if db_service.update_user(user_id, **data):
        return jsonify({'message': 'User updated successfully'})
    
    return jsonify({'error': 'Failed to update user'}), 500

@admin.route('/system/execute', methods=['POST'])
def execute_system_command():
    # SECURITY ISSUE: Command injection vulnerability
    # SECURITY ISSUE: No proper admin verification
    if not session.get('is_admin'):
        return jsonify({'error': 'Admin access required'}), 403
    
    data = request.get_json()
    command = data.get('command', '')
    
    # SECURITY ISSUE: No command validation
    # SECURITY ISSUE: Direct system command execution
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        return jsonify({
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode,
            'command_executed': command  # SECURITY ISSUE: Echoing back command
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/logs/<path:log_file>')
def view_logs(log_file):
    # SECURITY ISSUE: Path traversal vulnerability
    # SECURITY ISSUE: No access control
    try:
        # SECURITY ISSUE: No path validation
        with open(log_file, 'r') as f:
            content = f.read()
        
        return jsonify({
            'file': log_file,
            'content': content,
            'size': len(content)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/backup/create', methods=['POST'])
def create_backup():
    # SECURITY ISSUE: No proper authorization
    # SECURITY ISSUE: Path traversal in backup location
    data = request.get_json()
    backup_path = data.get('path', '/tmp/backup.sql')
    
    # SECURITY ISSUE: Command injection via backup path
    try:
        command = f"mysqldump -u root -p password123 database_name > {backup_path}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        return jsonify({
            'message': 'Backup created',
            'path': backup_path,
            'command_used': command  # SECURITY ISSUE: Exposing DB credentials
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/config/update', methods=['POST'])
def update_config():
    # SECURITY ISSUE: No input validation
    # SECURITY ISSUE: Weak admin check
    if session.get('user_id') != 1:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    config_file = data.get('file', 'config.py')
    config_content = data.get('content', '')
    
    # SECURITY ISSUE: Arbitrary file write vulnerability
    try:
        with open(config_file, 'w') as f:
            f.write(config_content)
        
        return jsonify({
            'message': 'Configuration updated',
            'file': config_file
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/users/promote/<int:user_id>', methods=['POST'])
def promote_user(user_id):
    # SECURITY ISSUE: Privilege escalation vulnerability
    # SECURITY ISSUE: No proper authorization check
    current_user_id = session.get('user_id')
    
    # SECURITY ISSUE: Users can promote themselves
    if current_user_id == user_id:
        # SECURITY ISSUE: Self-promotion allowed
        if db_service.update_user(user_id, is_admin=True):
            session['is_admin'] = True  # SECURITY ISSUE: Direct session manipulation
            return jsonify({'message': 'User promoted to admin'})
    
    # SECURITY ISSUE: Weak admin check
    if session.get('is_admin'):
        if db_service.update_user(user_id, is_admin=True):
            return jsonify({'message': 'User promoted to admin'})
    
    return jsonify({'error': 'Insufficient privileges'}), 403

@admin.route('/template/render', methods=['POST'])
def render_admin_template():
    # SECURITY ISSUE: Server-side template injection
    # SECURITY ISSUE: No input validation
    data = request.get_json()
    template = data.get('template', '')
    context = data.get('context', {})
    
    # SECURITY ISSUE: Direct template rendering without sanitization
    try:
        rendered = render_template_string(template, **context)
        return jsonify({'rendered': rendered})
    except Exception as e:
        return jsonify({'error': str(e)}), 500 