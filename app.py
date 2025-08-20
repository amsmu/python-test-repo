from flask import Flask, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db
from api_routes import api
import os

app = Flask(__name__)
app.config.from_object(Config)

app.secret_key = Config.SECRET_KEY


# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(api, url_prefix='/api')

@app.before_request
def log_request():
    print(f"Request: {request.method} {request.url}")
    print(f"Headers: {dict(request.headers)}")
    if request.data:
        print(f"Body: {request.data.decode()}")

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = '*'
    
    response.headers['Server'] = 'VulnerableApp/1.0'
    
    return response

@app.route('/')
def index():
    return jsonify({
        'message': 'Welcome to Vulnerable App',
        'version': '1.0',
        'debug': app.debug,
    })

@app.route('/health')
def health():
    import psutil
    return jsonify({
        'status': 'healthy',
        'cpu_percent': psutil.cpu_percent(),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent,
        'processes': len(psutil.pids()),
    })

@app.errorhandler(500)
def internal_error(error):
    import traceback
    return jsonify({
        'error': 'Internal Server Error',
    }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True) 