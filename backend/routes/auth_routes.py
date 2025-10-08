# Authentication Routes
# Handles user registration, login, and authentication

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from models.user import User
from models.activity import ActivityLog
from utils.db import get_db_connection, close_db_connection
from utils.auth import get_current_user

# Create blueprint for auth routes
bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user account
    
    Expected JSON:
        {
            "name": "Designer Name",
            "email": "email@example.com",
            "password": "password123"
        }
    
    Returns:
        Success message with user ID
    """
    try:
        # Get registration data from request
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Name, email, and password are required'}), 400
        
        # Connect to database
        connection = get_db_connection()
        user_model = User(connection)
        
        # Create new user
        user_id = user_model.create(
            name=data['name'],
            email=data['email'],
            password=data['password'],
            role='designer',  # Default role
            subscription_tier='free'  # Default tier
        )
        
        if not user_id:
            close_db_connection(connection)
            return jsonify({'error': 'Email already exists'}), 409
        
        # Log activity
        activity_model = ActivityLog(connection)
        activity_model.log(user_id, 'user_registered', 'user', user_id)
        
        close_db_connection(connection)
        
        return jsonify({
            'message': 'Registration successful',
            'user_id': user_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Registration failed', 'message': str(e)}), 500


@bp.route('/login', methods=['POST'])
def login():
    """
    Login with email and password
    
    Expected JSON:
        {
            "email": "email@example.com",
            "password": "password123"
        }
    
    Returns:
        JWT access token and user information
    """
    try:
        # Get login credentials from request
        data = request.get_json()
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Connect to database
        connection = get_db_connection()
        user_model = User(connection)
        
        # Verify credentials
        user = user_model.verify_password(data['email'], data['password'])
        
        if not user:
            close_db_connection(connection)
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Log login activity
        activity_model = ActivityLog(connection)
        activity_model.log(user['id'], 'user_login', 'user', user['id'])
        
        close_db_connection(connection)
        
        # Create JWT tokens
        access_token = create_access_token(identity=user['id'])
        refresh_token = create_refresh_token(identity=user['id'])
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'role': user['role'],
                'subscription_tier': user['subscription_tier']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Login failed', 'message': str(e)}), 500


@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token using refresh token
    
    Returns:
        New JWT access token
    """
    try:
        # Get user ID from refresh token
        user_id = get_jwt_identity()
        
        # Create new access token
        access_token = create_access_token(identity=user_id)
        
        return jsonify({
            'access_token': access_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Token refresh failed', 'message': str(e)}), 500


@bp.route('/me', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Get current user's profile information
    
    Returns:
        User profile data
    """
    try:
        # Get current user
        user = get_current_user()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get user statistics
        connection = get_db_connection()
        user_model = User(connection)
        stats = user_model.get_stats(user['id'])
        close_db_connection(connection)
        
        # Remove sensitive data
        user_data = dict(user)
        if 'password_hash' in user_data:
            del user_data['password_hash']
        
        return jsonify({
            'user': user_data,
            'stats': stats
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch profile', 'message': str(e)}), 500


@bp.route('/update-subscription', methods=['PUT'])
@jwt_required()
def update_subscription():
    """
    Update user's subscription tier
    
    Expected JSON:
        {
            "tier": "pro"  // or "agency"
        }
    
    Returns:
        Success message
    """
    try:
        data = request.get_json()
        new_tier = data.get('tier')
        
        # Validate tier
        if new_tier not in ['free', 'pro', 'agency']:
            return jsonify({'error': 'Invalid subscription tier'}), 400
        
        # Get current user
        user_id = get_jwt_identity()
        
        # Update subscription
        connection = get_db_connection()
        user_model = User(connection)
        success = user_model.update_subscription(user_id, new_tier)
        
        if success:
            # Log activity
            activity_model = ActivityLog(connection)
            activity_model.log(user_id, 'subscription_updated', 'user', user_id, 
                             {'new_tier': new_tier})
        
        close_db_connection(connection)
        
        if not success:
            return jsonify({'error': 'Failed to update subscription'}), 500
        
        return jsonify({
            'message': 'Subscription updated successfully',
            'new_tier': new_tier
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Subscription update failed', 'message': str(e)}), 500

