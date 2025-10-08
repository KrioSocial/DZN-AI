# Calendar Routes
# API endpoints for calendar events and scheduling

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.calendar import CalendarEvent
from backend.models.activity import ActivityLog
from backend.utils.db import get_db_connection, close_db_connection
from datetime import datetime, timedelta

# Create blueprint for calendar routes
bp = Blueprint('calendar', __name__)


@bp.route('/events', methods=['GET'])
@jwt_required()
def get_events():
    """
    Get calendar events for the current user
    
    Query Parameters:
        start_date: Filter from this date (optional)
        end_date: Filter to this date (optional)
        limit: Maximum number of events (default: 20)
    
    Returns:
        List of calendar events
    """
    try:
        user_id = get_jwt_identity()
        start_date = request.args.get('start_date', None)
        end_date = request.args.get('end_date', None)
        limit = request.args.get('limit', 20, type=int)
        
        connection = get_db_connection()
        calendar_model = CalendarEvent(connection)
        
        if start_date and end_date:
            # Get events within date range
            events = calendar_model.get_by_date_range(user_id, start_date, end_date)
        else:
            # Get upcoming events
            events = calendar_model.get_upcoming(user_id, limit=limit)
        
        close_db_connection(connection)
        
        return jsonify({
            'events': events,
            'count': len(events)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch events', 'message': str(e)}), 500


@bp.route('/events/<int:event_id>', methods=['GET'])
@jwt_required()
def get_event(event_id):
    """
    Get a specific event by ID
    
    Args:
        event_id: The event's ID
    
    Returns:
        Event data with client and project info
    """
    try:
        user_id = get_jwt_identity()
        
        connection = get_db_connection()
        calendar_model = CalendarEvent(connection)
        
        # Get event
        event = calendar_model.get_by_id(event_id, user_id)
        close_db_connection(connection)
        
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        return jsonify({'event': event}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch event', 'message': str(e)}), 500


@bp.route('/events', methods=['POST'])
@jwt_required()
def create_event():
    """
    Create a new calendar event
    
    Expected JSON:
        {
            "title": "Client Meeting",
            "start_time": "2024-02-15T10:00:00",
            "end_time": "2024-02-15T11:00:00",
            "event_type": "meeting",  // meeting, deadline, reminder, automation
            "description": "Discuss design concepts",
            "project_id": 1,
            "client_id": 1,
            "location": "Office"
        }
    
    Returns:
        Created event data
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        if not data.get('title') or not data.get('start_time'):
            return jsonify({'error': 'Title and start_time are required'}), 400
        
        connection = get_db_connection()
        calendar_model = CalendarEvent(connection)
        
        # Create event
        event_id = calendar_model.create(
            user_id=user_id,
            title=data['title'],
            start_time=data['start_time'],
            event_type=data.get('event_type', 'meeting'),
            end_time=data.get('end_time'),
            description=data.get('description'),
            project_id=data.get('project_id'),
            client_id=data.get('client_id'),
            location=data.get('location'),
            is_automated=data.get('is_automated', False)
        )
        
        if not event_id:
            close_db_connection(connection)
            return jsonify({'error': 'Failed to create event'}), 500
        
        # Log activity
        activity_model = ActivityLog(connection)
        activity_model.log(user_id, 'calendar_event_created', 'calendar_event', event_id, 
                          {'title': data['title']})
        
        # Get the created event
        event = calendar_model.get_by_id(event_id, user_id)
        close_db_connection(connection)
        
        return jsonify({
            'message': 'Event created successfully',
            'event': event
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Failed to create event', 'message': str(e)}), 500


@bp.route('/events/<int:event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id):
    """
    Update an existing event
    
    Args:
        event_id: The event's ID
    
    Expected JSON:
        Any event fields to update
    
    Returns:
        Success message
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        connection = get_db_connection()
        calendar_model = CalendarEvent(connection)
        
        # Update event
        success = calendar_model.update(event_id, user_id, **data)
        
        if success:
            # Log activity
            activity_model = ActivityLog(connection)
            activity_model.log(user_id, 'calendar_event_updated', 'calendar_event', event_id)
        
        close_db_connection(connection)
        
        if not success:
            return jsonify({'error': 'Failed to update event or event not found'}), 404
        
        return jsonify({'message': 'Event updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to update event', 'message': str(e)}), 500


@bp.route('/events/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    """
    Delete an event
    
    Args:
        event_id: The event's ID
    
    Returns:
        Success message
    """
    try:
        user_id = get_jwt_identity()
        
        connection = get_db_connection()
        calendar_model = CalendarEvent(connection)
        
        # Delete event
        success = calendar_model.delete(event_id, user_id)
        
        if success:
            # Log activity
            activity_model = ActivityLog(connection)
            activity_model.log(user_id, 'calendar_event_deleted', 'calendar_event', event_id)
        
        close_db_connection(connection)
        
        if not success:
            return jsonify({'error': 'Failed to delete event or event not found'}), 404
        
        return jsonify({'message': 'Event deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to delete event', 'message': str(e)}), 500


@bp.route('/upcoming', methods=['GET'])
@jwt_required()
def get_upcoming_events():
    """
    Get upcoming events for the next 7 days
    
    Returns:
        List of upcoming events grouped by date
    """
    try:
        user_id = get_jwt_identity()
        
        connection = get_db_connection()
        calendar_model = CalendarEvent(connection)
        
        # Get upcoming events
        events = calendar_model.get_upcoming(user_id, limit=50)
        close_db_connection(connection)
        
        # Group events by date
        events_by_date = {}
        for event in events:
            event_date = event['start_time'].strftime('%Y-%m-%d')
            if event_date not in events_by_date:
                events_by_date[event_date] = []
            events_by_date[event_date].append(event)
        
        return jsonify({
            'events': events,
            'events_by_date': events_by_date,
            'count': len(events)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch upcoming events', 'message': str(e)}), 500

