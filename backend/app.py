# Main Flask Application
# This is the entry point for the AI Studio backend server

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import get_config
from utils.db import init_db
import os

# Initialize Flask app
app = Flask(__name__, 
           static_folder='../frontend',
           template_folder='../frontend')

# Load configuration
config = get_config()
app.config.from_object(config)

# Enable CORS for frontend communication
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize JWT for authentication
jwt = JWTManager(app)

# Initialize database connection
print("Initializing database connection...")
if init_db():
    print("✓ Database connected successfully")
else:
    print("✗ Database connection failed - check your configuration")

# Import and register route blueprints
from routes import auth_routes, client_routes, project_routes, design_routes
from routes import product_routes, invoice_routes, marketing_routes, calendar_routes
from routes import dashboard_routes

# Register all API route blueprints with /api prefix
app.register_blueprint(auth_routes.bp, url_prefix='/api/auth')
app.register_blueprint(client_routes.bp, url_prefix='/api/clients')
app.register_blueprint(project_routes.bp, url_prefix='/api/projects')
app.register_blueprint(design_routes.bp, url_prefix='/api/designs')
app.register_blueprint(product_routes.bp, url_prefix='/api/products')
app.register_blueprint(invoice_routes.bp, url_prefix='/api/invoices')
app.register_blueprint(marketing_routes.bp, url_prefix='/api/marketing')
app.register_blueprint(calendar_routes.bp, url_prefix='/api/calendar')
app.register_blueprint(dashboard_routes.bp, url_prefix='/api/dashboard')


# Root route - serves landing page
@app.route('/')
def index():
    """Serve the landing page"""
    return send_from_directory('../frontend/landing', 'index.html')


# Serve static frontend files
@app.route('/<path:path>')
def serve_frontend(path):
    """Serve frontend static files (CSS, JS, images)"""
    try:
        return send_from_directory('../frontend', path)
    except:
        # If file not found, return 404
        return jsonify({'error': 'File not found'}), 404


# Health check endpoint
@app.route('/api/health')
def health_check():
    """
    Health check endpoint to verify server is running
    Returns server status and version information
    """
    return jsonify({
        'status': 'healthy',
        'message': 'AI Studio API is running',
        'version': '1.0.0',
        'environment': app.config['FLASK_ENV']
    }), 200


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error', 'message': str(error)}), 500


@app.errorhandler(401)
def unauthorized(error):
    """Handle 401 authentication errors"""
    return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401


@app.errorhandler(403)
def forbidden(error):
    """Handle 403 authorization errors"""
    return jsonify({'error': 'Forbidden', 'message': 'Insufficient permissions'}), 403


# JWT error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """Handle expired JWT tokens"""
    return jsonify({
        'error': 'Token expired',
        'message': 'Your session has expired. Please log in again.'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    """Handle invalid JWT tokens"""
    return jsonify({
        'error': 'Invalid token',
        'message': 'Authentication token is invalid.'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    """Handle missing JWT tokens"""
    return jsonify({
        'error': 'Token required',
        'message': 'Authentication token is missing.'
    }), 401


# Run the application
if __name__ == '__main__':
    # Get port from environment or use default (5001 to avoid macOS AirPlay conflict)
    port = int(os.environ.get('PORT', 5001))
    
    # Run Flask development server
    print(f"\n🚀 AI Studio Server Starting...")
    print(f"📍 Server: http://localhost:{port}")
    print(f"🔧 Environment: {app.config['FLASK_ENV']}")
    print(f"📊 Dashboard: http://localhost:{port}/dashboard")
    print(f"\n✨ Ready to help interior designers!\n")
    
    app.run(
        host='0.0.0.0',  # Listen on all interfaces
        port=port,
        debug=app.config['DEBUG']
    )

