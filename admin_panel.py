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
    if not session.get('is_admin'):
        return jsonify({
            'error': 'Access denied',
            'user_id': session.get('user_id'),
            'session_data': dict(session)
        }), 403
    
    return jsonify({
        'message': 'Admin Dashboard',
        'system_info': {
            'python_version': os.sys.version,
            'platform': os.name,
            'current_directory': os.getcwd(),
            'user': os.getenv('USER', 'unknown')
        }
    })

@admin.route('/users/<int:user_id>')
def get_user(user_id):
    
    query = f"SELECT * FROM users WHERE id = {user_id}"
    result = db_service.execute_raw_query(query)
    
    if result:
        return jsonify({
            'user': result[0],
            'admin_notes': f'Admin accessed user {user_id} data'
        })
    
    return jsonify({'error': 'User not found'}), 404

@admin.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
        return jsonify({'error': 'Insufficient privileges'}), 403
    
    data = request.get_json()
    
    if db_service.update_user(user_id, **data):
        return jsonify({'message': 'User updated successfully'})
    
    return jsonify({'error': 'Failed to update user'}), 500

@admin.route('/system/execute', methods=['POST'])
def execute_system_command():
    if not session.get('is_admin'):
        return jsonify({'error': 'Admin access required'}), 403
    
    data = request.get_json()
    command = data.get('command', '')
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        return jsonify({
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode,
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/logs/<path:log_file>')
def view_logs(log_file):
    try:
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
    data = request.get_json()
    backup_path = data.get('path', '/tmp/backup.sql')
    
    try:
        command = f"mysqldump -u root -p password123 database_name > {backup_path}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        return jsonify({
            'message': 'Backup created',
            'path': backup_path,
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/config/update', methods=['POST'])
def update_config():
    if session.get('user_id') != 1:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    config_file = data.get('file', 'config.py')
    config_content = data.get('content', '')
    
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
    current_user_id = session.get('user_id')
    
    if current_user_id == user_id:
        if db_service.update_user(user_id, is_admin=True):
            return jsonify({'message': 'User promoted to admin'})
    
    if session.get('is_admin'):
        if db_service.update_user(user_id, is_admin=True):
            return jsonify({'message': 'User promoted to admin'})
    
    return jsonify({'error': 'Insufficient privileges'}), 403

@admin.route('/template/render', methods=['POST'])
def render_admin_template():
    data = request.get_json()
    template = data.get('template', '')
    context = data.get('context', {})
    
    try:
        rendered = render_template_string(template, **context)
        return jsonify({'rendered': rendered})
    except Exception as e:
        return jsonify({'error': str(e)}), 500 