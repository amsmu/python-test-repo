from flask import Flask, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db
from api_routes import api
import os

# SECURITY ISSUE: Debug mode enabled in production
app = Flask(__name__)
app.config.from_object(Config)

# SECURITY ISSUE: Weak secret key
app.secret_key = Config.SECRET_KEY

# SECURITY ISSUE: No CSRF protection
# SECURITY ISSUE: No security headers
# SECURITY ISSUE: No rate limiting

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(api, url_prefix='/api')

@app.before_request
def log_request():
    # SECURITY ISSUE: Logging sensitive request data
    print(f"Request: {request.method} {request.url}")
    print(f"Headers: {dict(request.headers)}")
    if request.data:
        print(f"Body: {request.data.decode()}")

@app.after_request
def after_request(response):
    # SECURITY ISSUE: No security headers
    # SECURITY ISSUE: CORS misconfiguration
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = '*'
    
    # SECURITY ISSUE: Exposing server information
    response.headers['Server'] = 'VulnerableApp/1.0'
    
    return response

@app.route('/')
def index():
    # SECURITY ISSUE: Information disclosure
    return jsonify({
        'message': 'Welcome to Vulnerable App',
        'version': '1.0',
        'debug': app.debug,
        'secret_key': app.secret_key,  # SECURITY ISSUE: Exposing secret key
        'database_url': Config.DATABASE_URL  # SECURITY ISSUE: Exposing DB credentials
    })

@app.route('/health')
def health():
    # SECURITY ISSUE: Exposing sensitive system information
    import psutil
    return jsonify({
        'status': 'healthy',
        'cpu_percent': psutil.cpu_percent(),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent,
        'processes': len(psutil.pids()),
        'environment': dict(os.environ)  # SECURITY ISSUE: Exposing environment variables
    })

@app.errorhandler(500)
def internal_error(error):
    # SECURITY ISSUE: Exposing stack traces
    import traceback
    return jsonify({
        'error': 'Internal Server Error',
        'traceback': traceback.format_exc(),  # SECURITY ISSUE: Stack trace exposure
        'locals': str(error.__dict__)  # SECURITY ISSUE: Variable exposure
    }), 500

if __name__ == '__main__':
    # SECURITY ISSUE: Running with debug=True in production
    # SECURITY ISSUE: Binding to all interfaces (0.0.0.0)
    # SECURITY ISSUE: No SSL/HTTPS
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True) 