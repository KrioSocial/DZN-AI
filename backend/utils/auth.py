# Authentication utilities
# Helper functions for JWT token management and authentication

from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.user import User
from utils.db import get_db_connection

def token_required(f):
    """
    Decorator to require valid JWT token for protected routes
    
    Usage:
        @app.route('/protected')
        @token_required
        def protected_route():
            return 'This is protected'
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            # Verify JWT token is present and valid
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Invalid or missing token', 'message': str(e)}), 401
    return decorated


def get_current_user():
    """
    Get current authenticated user from JWT token
    
    Returns:
        User dictionary or None if not authenticated
    """
    try:
        # Get user ID from JWT token
        user_id = get_jwt_identity()
        
        if not user_id:
            return None
        
        # Fetch user from database
        connection = get_db_connection()
        user_model = User(connection)
        user = user_model.get_by_id(user_id)
        connection.close()
        
        return user
    except:
        return None


def check_subscription_limit(user_id, feature_type):
    """
    Check if user has reached their subscription tier limits
    
    Args:
        user_id: The user's ID
        feature_type: Type of feature to check (projects, ai_generations, etc.)
    
    Returns:
        True if user is within limits, False if limit reached
    """
    from config import get_config
    
    connection = get_db_connection()
    user_model = User(connection)
    user = user_model.get_by_id(user_id)
    connection.close()
    
    if not user:
        return False
    
    # Get tier limits from config
    config = get_config()
    tier = user['subscription_tier']
    limits = config.TIER_LIMITS.get(tier, config.TIER_LIMITS['free'])
    
    # Check specific feature limit
    if feature_type == 'ai_generations':
        limit = limits['ai_generations']
        if limit == -1:  # Unlimited
            return True
        return user['ai_generations_used'] < limit
    
    elif feature_type == 'projects':
        limit = limits['projects']
        if limit == -1:  # Unlimited
            return True
        
        # Count user's projects
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as count FROM projects WHERE user_id = %s", (user_id,))
            count = cursor.fetchone()['count']
        connection.close()
        
        return count < limit
    
    # Default to allowing
    return True


def require_subscription_tier(required_tier):
    """
    Decorator to require specific subscription tier for a route
    
    Args:
        required_tier: Minimum required tier ('pro' or 'agency')
    
    Usage:
        @app.route('/premium-feature')
        @token_required
        @require_subscription_tier('pro')
        def premium_feature():
            return 'This requires Pro subscription'
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user = get_current_user()
            
            if not user:
                return jsonify({'error': 'Authentication required'}), 401
            
            # Define tier hierarchy
            tiers = {'free': 0, 'pro': 1, 'agency': 2}
            user_tier_level = tiers.get(user['subscription_tier'], 0)
            required_tier_level = tiers.get(required_tier, 2)
            
            if user_tier_level < required_tier_level:
                return jsonify({
                    'error': 'Subscription upgrade required',
                    'message': f'This feature requires {required_tier.capitalize()} subscription',
                    'current_tier': user['subscription_tier'],
                    'required_tier': required_tier
                }), 403
            
            return f(*args, **kwargs)
        return decorated
    return decorator

