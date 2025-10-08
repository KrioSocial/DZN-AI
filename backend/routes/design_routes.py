# Design Routes
# API endpoints for AI design generation and moodboards

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.design import Design
from backend.models.user import User
from backend.models.activity import ActivityLog
from backend.services.ai_service import AIService
from backend.utils.db import get_db_connection, close_db_connection
from backend.utils.auth import check_subscription_limit
from backend.config import get_config

# Create blueprint for design routes
bp = Blueprint('designs', __name__)


@bp.route('', methods=['GET'])
@jwt_required()
def get_designs():
    """
    Get all designs for the current user
    
    Query Parameters:
        project_id: Filter by project (optional)
        limit: Maximum number of designs (default: 50)
    
    Returns:
        List of designs
    """
    try:
        user_id = get_jwt_identity()
        project_id = request.args.get('project_id', None, type=int)
        limit = request.args.get('limit', 50, type=int)
        
        connection = get_db_connection()
        design_model = Design(connection)
        
        if project_id:
            # Get designs for specific project
            designs = design_model.get_by_project(project_id)
        else:
            # Get all user's designs
            designs = design_model.get_by_user(user_id, limit=limit)
        
        close_db_connection(connection)
        
        return jsonify({
            'designs': designs,
            'count': len(designs)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch designs', 'message': str(e)}), 500


@bp.route('/<int:design_id>', methods=['GET'])
@jwt_required()
def get_design(design_id):
    """
    Get a specific design by ID
    
    Args:
        design_id: The design's ID
    
    Returns:
        Design data with all generated content
    """
    try:
        connection = get_db_connection()
        design_model = Design(connection)
        
        # Get design
        design = design_model.get_by_id(design_id)
        close_db_connection(connection)
        
        if not design:
            return jsonify({'error': 'Design not found'}), 404
        
        return jsonify({'design': design}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch design', 'message': str(e)}), 500


@bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_design():
    """
    Generate a new AI design/moodboard
    
    Expected JSON:
        {
            "project_id": 1,
            "room_type": "living room",
            "style": "modern minimalist",
            "budget": 5000,
            "keywords": "cozy, natural light, plants"
        }
    
    Returns:
        Generated design with images, colors, and recommendations
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        if not data.get('project_id') or not data.get('room_type') or not data.get('style'):
            return jsonify({'error': 'project_id, room_type, and style are required'}), 400
        
        # Check AI generation limit
        if not check_subscription_limit(user_id, 'ai_generations'):
            return jsonify({
                'error': 'AI generation limit reached',
                'message': 'Please upgrade your subscription to generate more designs'
            }), 403
        
        connection = get_db_connection()
        design_model = Design(connection)
        
        # Create design entry
        design_id = design_model.create(
            project_id=data['project_id'],
            user_id=user_id,
            room_type=data['room_type'],
            style=data['style'],
            budget=data.get('budget'),
            keywords=data.get('keywords')
        )
        
        if not design_id:
            close_db_connection(connection)
            return jsonify({'error': 'Failed to create design entry'}), 500
        
        # Initialize AI service
        config = get_config()
        ai_service = AIService(config.OPENAI_API_KEY)
        
        # Generate moodboard with AI
        moodboard = ai_service.generate_moodboard(
            room_type=data['room_type'],
            style=data['style'],
            budget=data.get('budget', 0),
            keywords=data.get('keywords', '')
        )
        
        if not moodboard:
            close_db_connection(connection)
            return jsonify({'error': 'Failed to generate AI design'}), 500
        
        # Update design with generated content
        design_model.update_outputs(
            design_id=design_id,
            image_urls=moodboard.get('image_urls', []),
            color_palette=moodboard.get('color_palette', []),
            description=moodboard.get('description', ''),
            product_list=moodboard.get('furniture_list', [])
        )
        
        # Increment AI usage counter
        user_model = User(connection)
        user_model.increment_ai_usage(user_id)
        
        # Log activity
        activity_model = ActivityLog(connection)
        activity_model.log(user_id, 'design_generated', 'design', design_id, 
                          {'room_type': data['room_type'], 'style': data['style']})
        
        # Get the complete design
        design = design_model.get_by_id(design_id)
        close_db_connection(connection)
        
        return jsonify({
            'message': 'Design generated successfully',
            'design': design
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Failed to generate design', 'message': str(e)}), 500


@bp.route('/<int:design_id>', methods=['DELETE'])
@jwt_required()
def delete_design(design_id):
    """
    Delete a design
    
    Args:
        design_id: The design's ID
    
    Returns:
        Success message
    """
    try:
        user_id = get_jwt_identity()
        
        connection = get_db_connection()
        design_model = Design(connection)
        
        # Delete design
        success = design_model.delete(design_id)
        
        if success:
            # Log activity
            activity_model = ActivityLog(connection)
            activity_model.log(user_id, 'design_deleted', 'design', design_id)
        
        close_db_connection(connection)
        
        if not success:
            return jsonify({'error': 'Failed to delete design or design not found'}), 404
        
        return jsonify({'message': 'Design deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to delete design', 'message': str(e)}), 500

