# Project Routes
# API endpoints for managing interior design projects

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.project import Project
from backend.models.task import Task
from backend.models.activity import ActivityLog
from backend.services.ai_service import AIService
from backend.utils.db import get_db_connection, close_db_connection
from backend.config import get_config
import os

# Create blueprint for project routes
bp = Blueprint('projects', __name__)


@bp.route('', methods=['GET'])
@jwt_required()
def get_projects():
    """
    Get all projects for the current user
    
    Query Parameters:
        status: Filter by status (optional)
        limit: Maximum number of projects (default: 100)
        offset: Pagination offset (default: 0)
    
    Returns:
        List of projects
    """
    try:
        user_id = get_jwt_identity()
        status = request.args.get('status', None)
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        connection = get_db_connection()
        project_model = Project(connection)
        
        # Get projects with optional status filter
        projects = project_model.get_all(user_id, status=status, limit=limit, offset=offset)
        close_db_connection(connection)
        
        return jsonify({
            'projects': projects,
            'count': len(projects)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch projects', 'message': str(e)}), 500


@bp.route('/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id):
    """
    Get a specific project by ID with tasks
    
    Args:
        project_id: The project's ID
    
    Returns:
        Project data with tasks
    """
    try:
        user_id = get_jwt_identity()
        
        connection = get_db_connection()
        project_model = Project(connection)
        task_model = Task(connection)
        
        # Get project
        project = project_model.get_by_id(project_id, user_id)
        
        if not project:
            close_db_connection(connection)
            return jsonify({'error': 'Project not found'}), 404
        
        # Get project tasks
        tasks = task_model.get_by_project(project_id)
        project['tasks'] = tasks
        
        close_db_connection(connection)
        
        return jsonify({'project': project}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch project', 'message': str(e)}), 500


@bp.route('', methods=['POST'])
@jwt_required()
def create_project():
    """
    Create a new project
    
    Expected JSON:
        {
            "title": "Project Name",
            "client_id": 1,
            "description": "...",
            "budget": 15000,
            "start_date": "2024-01-01",
            "deadline": "2024-03-31"
        }
    
    Returns:
        Created project data
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        if not data.get('title'):
            return jsonify({'error': 'Project title is required'}), 400
        
        connection = get_db_connection()
        project_model = Project(connection)
        
        # Create project
        project_id = project_model.create(
            user_id=user_id,
            title=data['title'],
            client_id=data.get('client_id'),
            description=data.get('description'),
            budget=data.get('budget'),
            start_date=data.get('start_date'),
            deadline=data.get('deadline')
        )
        
        if not project_id:
            close_db_connection(connection)
            return jsonify({'error': 'Failed to create project'}), 500
        
        # Log activity
        activity_model = ActivityLog(connection)
        activity_model.log(user_id, 'project_created', 'project', project_id, 
                          {'project_title': data['title']})
        
        # Get the created project
        project = project_model.get_by_id(project_id, user_id)
        close_db_connection(connection)
        
        return jsonify({
            'message': 'Project created successfully',
            'project': project
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Failed to create project', 'message': str(e)}), 500


@bp.route('/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    """
    Update an existing project
    
    Args:
        project_id: The project's ID
    
    Expected JSON:
        Any project fields to update
    
    Returns:
        Success message
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        connection = get_db_connection()
        project_model = Project(connection)
        
        # Update project
        success = project_model.update(project_id, user_id, **data)
        
        if success:
            # Log activity
            activity_model = ActivityLog(connection)
            activity_model.log(user_id, 'project_updated', 'project', project_id)
        
        close_db_connection(connection)
        
        if not success:
            return jsonify({'error': 'Failed to update project or project not found'}), 404
        
        return jsonify({'message': 'Project updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to update project', 'message': str(e)}), 500


@bp.route('/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    """
    Delete a project
    
    Args:
        project_id: The project's ID
    
    Returns:
        Success message
    """
    try:
        user_id = get_jwt_identity()
        
        connection = get_db_connection()
        project_model = Project(connection)
        
        # Delete project
        success = project_model.delete(project_id, user_id)
        
        if success:
            # Log activity
            activity_model = ActivityLog(connection)
            activity_model.log(user_id, 'project_deleted', 'project', project_id)
        
        close_db_connection(connection)
        
        if not success:
            return jsonify({'error': 'Failed to delete project or project not found'}), 404
        
        return jsonify({'message': 'Project deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to delete project', 'message': str(e)}), 500


@bp.route('/<int:project_id>/tasks', methods=['POST'])
@jwt_required()
def create_task(project_id):
    """
    Create a new task for a project
    
    Args:
        project_id: The project's ID
    
    Expected JSON:
        {
            "title": "Task name",
            "description": "...",
            "priority": "high",
            "due_date": "2024-02-01"
        }
    
    Returns:
        Created task data
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        if not data.get('title'):
            return jsonify({'error': 'Task title is required'}), 400
        
        # Verify project ownership
        connection = get_db_connection()
        project_model = Project(connection)
        project = project_model.get_by_id(project_id, user_id)
        
        if not project:
            close_db_connection(connection)
            return jsonify({'error': 'Project not found'}), 404
        
        task_model = Task(connection)
        
        # Create task
        task_id = task_model.create(
            project_id=project_id,
            title=data['title'],
            description=data.get('description'),
            priority=data.get('priority', 'medium'),
            due_date=data.get('due_date')
        )
        
        if not task_id:
            close_db_connection(connection)
            return jsonify({'error': 'Failed to create task'}), 500
        
        # Log activity
        activity_model = ActivityLog(connection)
        activity_model.log(user_id, 'task_created', 'task', task_id, 
                          {'project_id': project_id})
        
        # Get the created task
        task = task_model.get_by_id(task_id)
        close_db_connection(connection)
        
        return jsonify({
            'message': 'Task created successfully',
            'task': task
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Failed to create task', 'message': str(e)}), 500


@bp.route('/<int:project_id>/ai-insights', methods=['POST'])
@jwt_required()
def generate_insights(project_id):
    """
    Generate AI insights for a project
    
    Args:
        project_id: The project's ID
    
    Returns:
        AI-generated insights and recommendations
    """
    try:
        user_id = get_jwt_identity()
        
        connection = get_db_connection()
        project_model = Project(connection)
        
        # Get project
        project = project_model.get_by_id(project_id, user_id)
        
        if not project:
            close_db_connection(connection)
            return jsonify({'error': 'Project not found'}), 404
        
        # Initialize AI service
        config = get_config()
        ai_service = AIService(config.OPENAI_API_KEY)
        
        # Generate insights
        insights = ai_service.generate_project_insights(project)
        
        if insights:
            # Save insights to project
            project_model.update_ai_insights(project_id, user_id, insights)
            
            # Log activity
            activity_model = ActivityLog(connection)
            activity_model.log(user_id, 'ai_insights_generated', 'project', project_id)
        
        close_db_connection(connection)
        
        if not insights:
            return jsonify({'error': 'Failed to generate insights'}), 500
        
        return jsonify({
            'message': 'Insights generated successfully',
            'insights': insights
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to generate insights', 'message': str(e)}), 500

