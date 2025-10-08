# Marketing Routes
# API endpoints for AI-powered marketing content generation

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.marketing import MarketingContent
from backend.models.project import Project
from backend.models.activity import ActivityLog
from backend.services.ai_service import AIService
from backend.utils.db import get_db_connection, close_db_connection
from backend.utils.auth import check_subscription_limit, require_subscription_tier
from backend.config import get_config

# Create blueprint for marketing routes
bp = Blueprint('marketing', __name__)


@bp.route('', methods=['GET'])
@jwt_required()
def get_marketing_content():
    """
    Get all marketing content for the current user
    
    Query Parameters:
        type: Filter by content type (optional)
        status: Filter by status (optional)
        limit: Maximum number of items (default: 100)
    
    Returns:
        List of marketing content
    """
    try:
        user_id = get_jwt_identity()
        content_type = request.args.get('type', None)
        status = request.args.get('status', None)
        limit = request.args.get('limit', 100, type=int)
        
        connection = get_db_connection()
        marketing_model = MarketingContent(connection)
        
        # Get marketing content with optional filters
        content = marketing_model.get_all(user_id, content_type=content_type, 
                                         status=status, limit=limit)
        close_db_connection(connection)
        
        return jsonify({
            'content': content,
            'count': len(content)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch marketing content', 'message': str(e)}), 500


@bp.route('/<int:content_id>', methods=['GET'])
@jwt_required()
def get_content(content_id):
    """
    Get a specific marketing content by ID
    
    Args:
        content_id: The content's ID
    
    Returns:
        Marketing content data
    """
    try:
        user_id = get_jwt_identity()
        
        connection = get_db_connection()
        marketing_model = MarketingContent(connection)
        
        # Get content
        content = marketing_model.get_by_id(content_id, user_id)
        close_db_connection(connection)
        
        if not content:
            return jsonify({'error': 'Content not found'}), 404
        
        return jsonify({'content': content}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch content', 'message': str(e)}), 500


@bp.route('/generate', methods=['POST'])
@jwt_required()
@require_subscription_tier('pro')  # Marketing tools require Pro subscription
def generate_marketing_content():
    """
    Generate AI marketing content (caption, blog, email, post)
    
    Expected JSON:
        {
            "content_type": "caption",  // caption, blog, email, post
            "project_id": 1,
            "platform": "Instagram",
            "title": "Modern Living Room Design"
        }
    
    Returns:
        Generated marketing content
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        if not data.get('content_type'):
            return jsonify({'error': 'content_type is required'}), 400
        
        # Check AI generation limit
        if not check_subscription_limit(user_id, 'ai_generations'):
            return jsonify({
                'error': 'AI generation limit reached',
                'message': 'Please upgrade your subscription'
            }), 403
        
        connection = get_db_connection()
        
        # Get project info if provided
        project_info = {}
        if data.get('project_id'):
            project_model = Project(connection)
            project = project_model.get_by_id(data['project_id'], user_id)
            if project:
                project_info = {
                    'title': project.get('title', ''),
                    'description': project.get('description', ''),
                    'style': data.get('style', '')  # From request
                }
        
        # If no project, use title and description from request
        if not project_info:
            project_info = {
                'title': data.get('title', 'Interior Design Project'),
                'description': data.get('description', '')
            }
        
        # Initialize AI service
        config = get_config()
        ai_service = AIService(config.OPENAI_API_KEY)
        
        # Generate marketing content
        generated_content = ai_service.generate_marketing_content(
            content_type=data['content_type'],
            project_info=project_info,
            platform=data.get('platform')
        )
        
        if not generated_content:
            close_db_connection(connection)
            return jsonify({'error': 'Failed to generate content'}), 500
        
        # Save generated content
        marketing_model = MarketingContent(connection)
        content_id = marketing_model.create(
            user_id=user_id,
            content_type=data['content_type'],
            content=generated_content,
            project_id=data.get('project_id'),
            platform=data.get('platform'),
            title=project_info.get('title')
        )
        
        if content_id:
            # Log activity
            activity_model = ActivityLog(connection)
            activity_model.log(user_id, 'marketing_content_generated', 'marketing', content_id, 
                             {'content_type': data['content_type']})
        
        # Get the complete content
        content = marketing_model.get_by_id(content_id, user_id)
        close_db_connection(connection)
        
        return jsonify({
            'message': 'Marketing content generated successfully',
            'content': content
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Failed to generate marketing content', 'message': str(e)}), 500


@bp.route('/<int:content_id>', methods=['PUT'])
@jwt_required()
def update_content(content_id):
    """
    Update marketing content
    
    Args:
        content_id: The content's ID
    
    Expected JSON:
        Any content fields to update
    
    Returns:
        Success message
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        connection = get_db_connection()
        marketing_model = MarketingContent(connection)
        
        # Update content
        success = marketing_model.update(content_id, user_id, **data)
        
        if success:
            # Log activity
            activity_model = ActivityLog(connection)
            activity_model.log(user_id, 'marketing_content_updated', 'marketing', content_id)
        
        close_db_connection(connection)
        
        if not success:
            return jsonify({'error': 'Failed to update content or content not found'}), 404
        
        return jsonify({'message': 'Content updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to update content', 'message': str(e)}), 500


@bp.route('/<int:content_id>/schedule', methods=['POST'])
@jwt_required()
def schedule_content(content_id):
    """
    Schedule content for future posting
    
    Args:
        content_id: The content's ID
    
    Expected JSON:
        {
            "scheduled_date": "2024-02-15T10:00:00"
        }
    
    Returns:
        Success message
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data.get('scheduled_date'):
            return jsonify({'error': 'scheduled_date is required'}), 400
        
        connection = get_db_connection()
        marketing_model = MarketingContent(connection)
        
        # Schedule content
        success = marketing_model.schedule_post(content_id, user_id, data['scheduled_date'])
        
        if success:
            # Log activity
            activity_model = ActivityLog(connection)
            activity_model.log(user_id, 'content_scheduled', 'marketing', content_id)
        
        close_db_connection(connection)
        
        if not success:
            return jsonify({'error': 'Failed to schedule content'}), 404
        
        return jsonify({'message': 'Content scheduled successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to schedule content', 'message': str(e)}), 500


@bp.route('/<int:content_id>', methods=['DELETE'])
@jwt_required()
def delete_content(content_id):
    """
    Delete marketing content
    
    Args:
        content_id: The content's ID
    
    Returns:
        Success message
    """
    try:
        user_id = get_jwt_identity()
        
        connection = get_db_connection()
        marketing_model = MarketingContent(connection)
        
        # Delete content
        success = marketing_model.delete(content_id, user_id)
        
        if success:
            # Log activity
            activity_model = ActivityLog(connection)
            activity_model.log(user_id, 'marketing_content_deleted', 'marketing', content_id)
        
        close_db_connection(connection)
        
        if not success:
            return jsonify({'error': 'Failed to delete content or content not found'}), 404
        
        return jsonify({'message': 'Content deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to delete content', 'message': str(e)}), 500

