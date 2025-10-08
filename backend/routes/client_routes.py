# Client Routes
# API endpoints for managing clients

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.client import Client
from backend.models.activity import ActivityLog
from backend.utils.db import get_db_connection, close_db_connection

# Create blueprint for client routes
bp = Blueprint('clients', __name__)


@bp.route('', methods=['GET'])
@jwt_required()
def get_clients():
    """
    Get all clients for the current user
    
    Query Parameters:
        limit: Maximum number of clients to return (default: 100)
        offset: Number of clients to skip for pagination (default: 0)
        search: Search query for client name or email
    
    Returns:
        List of clients
    """
    try:
        user_id = get_jwt_identity()
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        search = request.args.get('search', None)
        
        connection = get_db_connection()
        client_model = Client(connection)
        
        if search:
            # Search clients by name or email
            clients = client_model.search(user_id, search)
        else:
            # Get all clients
            clients = client_model.get_all(user_id, limit=limit, offset=offset)
        
        close_db_connection(connection)
        
        return jsonify({
            'clients': clients,
            'count': len(clients)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch clients', 'message': str(e)}), 500


@bp.route('/<int:client_id>', methods=['GET'])
@jwt_required()
def get_client(client_id):
    """
    Get a specific client by ID with statistics
    
    Args:
        client_id: The client's ID
    
    Returns:
        Client data with statistics
    """
    try:
        user_id = get_jwt_identity()
        
        connection = get_db_connection()
        client_model = Client(connection)
        
        # Get client with stats (projects, messages, etc.)
        client = client_model.get_with_stats(client_id, user_id)
        close_db_connection(connection)
        
        if not client:
            return jsonify({'error': 'Client not found'}), 404
        
        return jsonify({'client': client}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch client', 'message': str(e)}), 500


@bp.route('', methods=['POST'])
@jwt_required()
def create_client():
    """
    Create a new client
    
    Expected JSON:
        {
            "name": "Client Name",
            "email": "client@example.com",
            "phone": "+44...",
            "address": "...",
            "style_preferences": "Modern, minimalist...",
            "budget_range": "£10,000 - £20,000",
            "notes": "..."
        }
    
    Returns:
        Created client data
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name'):
            return jsonify({'error': 'Client name is required'}), 400
        
        connection = get_db_connection()
        client_model = Client(connection)
        
        # Create client
        client_id = client_model.create(
            user_id=user_id,
            name=data['name'],
            email=data.get('email'),
            phone=data.get('phone'),
            address=data.get('address'),
            style_preferences=data.get('style_preferences'),
            budget_range=data.get('budget_range'),
            notes=data.get('notes')
        )
        
        if not client_id:
            close_db_connection(connection)
            return jsonify({'error': 'Failed to create client'}), 500
        
        # Log activity
        activity_model = ActivityLog(connection)
        activity_model.log(user_id, 'client_created', 'client', client_id, 
                          {'client_name': data['name']})
        
        # Get the created client
        client = client_model.get_by_id(client_id, user_id)
        close_db_connection(connection)
        
        return jsonify({
            'message': 'Client created successfully',
            'client': client
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Failed to create client', 'message': str(e)}), 500


@bp.route('/<int:client_id>', methods=['PUT'])
@jwt_required()
def update_client(client_id):
    """
    Update an existing client
    
    Args:
        client_id: The client's ID
    
    Expected JSON:
        Any client fields to update
    
    Returns:
        Success message
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        connection = get_db_connection()
        client_model = Client(connection)
        
        # Update client
        success = client_model.update(client_id, user_id, **data)
        
        if success:
            # Log activity
            activity_model = ActivityLog(connection)
            activity_model.log(user_id, 'client_updated', 'client', client_id)
        
        close_db_connection(connection)
        
        if not success:
            return jsonify({'error': 'Failed to update client or client not found'}), 404
        
        return jsonify({'message': 'Client updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to update client', 'message': str(e)}), 500


@bp.route('/<int:client_id>', methods=['DELETE'])
@jwt_required()
def delete_client(client_id):
    """
    Delete a client
    
    Args:
        client_id: The client's ID
    
    Returns:
        Success message
    """
    try:
        user_id = get_jwt_identity()
        
        connection = get_db_connection()
        client_model = Client(connection)
        
        # Delete client
        success = client_model.delete(client_id, user_id)
        
        if success:
            # Log activity
            activity_model = ActivityLog(connection)
            activity_model.log(user_id, 'client_deleted', 'client', client_id)
        
        close_db_connection(connection)
        
        if not success:
            return jsonify({'error': 'Failed to delete client or client not found'}), 404
        
        return jsonify({'message': 'Client deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to delete client', 'message': str(e)}), 500

