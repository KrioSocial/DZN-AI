# Dashboard Routes
# API endpoints for dashboard overview and statistics

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.project import Project
from backend.models.client import Client
from backend.models.invoice import Invoice
from backend.models.message import Message
from backend.models.activity import ActivityLog
from backend.models.user import User
from backend.utils.db import get_db_connection, close_db_connection

# Create blueprint for dashboard routes
bp = Blueprint('dashboard', __name__)


@bp.route('/overview', methods=['GET'])
@jwt_required()
def get_dashboard_overview():
    """
    Get complete dashboard overview with all statistics
    
    Returns:
        Comprehensive dashboard data including:
        - Project statistics
        - Financial summary
        - Recent activity
        - Upcoming events
        - AI usage stats
    """
    try:
        user_id = get_jwt_identity()
        
        connection = get_db_connection()
        
        # Get project statistics
        project_model = Project(connection)
        project_stats = project_model.get_dashboard_stats(user_id)
        
        # Get financial summary
        invoice_model = Invoice(connection)
        financial_stats = invoice_model.get_financial_summary(user_id)
        
        # Get client count
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as count FROM clients WHERE user_id = %s", (user_id,))
            client_count = cursor.fetchone()['count']
        
        # Get unread messages count
        message_model = Message(connection)
        unread_messages = message_model.get_unread(user_id)
        
        # Get recent activity
        activity_model = ActivityLog(connection)
        recent_activity = activity_model.get_recent(user_id, hours=48, limit=10)
        
        # Get user info and AI usage
        user_model = User(connection)
        user_stats = user_model.get_stats(user_id)
        
        close_db_connection(connection)
        
        # Compile dashboard data
        dashboard = {
            'projects': project_stats,
            'finances': financial_stats,
            'clients': {
                'total_count': client_count
            },
            'messages': {
                'unread_count': len(unread_messages)
            },
            'ai_usage': {
                'used': user_stats['ai_generations_used'],
                'limit': user_stats['ai_generations_limit'],
                'remaining': max(0, user_stats['ai_generations_limit'] - user_stats['ai_generations_used'])
            },
            'subscription': {
                'tier': user_stats['subscription_tier']
            },
            'recent_activity': recent_activity
        }
        
        return jsonify({'dashboard': dashboard}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch dashboard data', 'message': str(e)}), 500


@bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """
    Get detailed statistics for analytics
    
    Returns:
        Detailed statistics and metrics
    """
    try:
        user_id = get_jwt_identity()
        
        connection = get_db_connection()
        
        # Activity summary (last 30 days)
        activity_model = ActivityLog(connection)
        activity_summary = activity_model.get_activity_summary(user_id, days=30)
        
        # Project breakdown by status
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT status, COUNT(*) as count 
                FROM projects 
                WHERE user_id = %s 
                GROUP BY status
            """, (user_id,))
            project_breakdown = cursor.fetchall()
        
        # Monthly revenue trend (last 6 months)
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    DATE_FORMAT(paid_date, '%Y-%m') as month,
                    SUM(amount) as revenue
                FROM invoices 
                WHERE user_id = %s AND status = 'paid' AND type = 'invoice'
                AND paid_date >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
                GROUP BY month
                ORDER BY month DESC
            """, (user_id,))
            revenue_trend = cursor.fetchall()
        
        close_db_connection(connection)
        
        stats = {
            'activity_summary': activity_summary,
            'project_breakdown': project_breakdown,
            'revenue_trend': revenue_trend
        }
        
        return jsonify({'stats': stats}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch statistics', 'message': str(e)}), 500


@bp.route('/insights', methods=['GET'])
@jwt_required()
def get_insights():
    """
    Get AI-powered insights and recommendations for the dashboard
    
    Returns:
        AI-generated insights and actionable recommendations
    """
    try:
        user_id = get_jwt_identity()
        
        connection = get_db_connection()
        insights = []
        
        # Check for overdue projects
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as count FROM projects 
                WHERE user_id = %s AND deadline < CURDATE() AND status != 'completed'
            """, (user_id,))
            overdue_count = cursor.fetchone()['count']
            
            if overdue_count > 0:
                insights.append({
                    'type': 'warning',
                    'title': f'{overdue_count} Overdue Project{"s" if overdue_count > 1 else ""}',
                    'message': f'You have {overdue_count} project{"s" if overdue_count > 1 else ""} past their deadline.',
                    'action': 'Review overdue projects',
                    'link': '/projects?status=overdue'
                })
        
        # Check for clients not contacted recently
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.id, c.name, MAX(m.created_at) as last_contact
                FROM clients c
                LEFT JOIN messages m ON c.id = m.client_id
                WHERE c.user_id = %s
                GROUP BY c.id
                HAVING last_contact < DATE_SUB(NOW(), INTERVAL 14 DAY) OR last_contact IS NULL
                LIMIT 5
            """, (user_id,))
            inactive_clients = cursor.fetchall()
            
            if inactive_clients:
                client_names = ', '.join([c['name'] for c in inactive_clients[:3]])
                insights.append({
                    'type': 'info',
                    'title': 'Inactive Clients',
                    'message': f'{len(inactive_clients)} clients haven\'t been contacted recently: {client_names}...',
                    'action': 'Send follow-up',
                    'link': '/clients'
                })
        
        # Check budget overspend
        project_model = Project(connection)
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, title, budget, spent 
                FROM projects 
                WHERE user_id = %s AND spent > budget AND status != 'completed'
            """, (user_id,))
            overspent_projects = cursor.fetchall()
            
            if overspent_projects:
                total_over = sum(p['spent'] - p['budget'] for p in overspent_projects)
                insights.append({
                    'type': 'alert',
                    'title': 'Budget Overspend',
                    'message': f'{len(overspent_projects)} project{"s are" if len(overspent_projects) > 1 else " is"} over budget by £{total_over:.2f} total.',
                    'action': 'Review budgets',
                    'link': '/projects'
                })
        
        # Check AI usage
        user_model = User(connection)
        user = user_model.get_by_id(user_id)
        
        if user:
            usage_percent = (user['ai_generations_used'] / user['ai_generations_limit']) * 100 if user['ai_generations_limit'] > 0 else 0
            
            if usage_percent >= 80:
                insights.append({
                    'type': 'warning',
                    'title': 'AI Usage Limit',
                    'message': f'You\'ve used {user["ai_generations_used"]} of {user["ai_generations_limit"]} AI generations ({usage_percent:.0f}%).',
                    'action': 'Upgrade subscription',
                    'link': '/settings/subscription'
                })
        
        close_db_connection(connection)
        
        return jsonify({
            'insights': insights,
            'count': len(insights)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to generate insights', 'message': str(e)}), 500


@bp.route('/activity', methods=['GET'])
@jwt_required()
def get_recent_activity():
    """
    Get recent user activity for the dashboard feed
    
    Query Parameters:
        limit: Maximum number of activities (default: 20)
        hours: Hours to look back (default: 72)
    
    Returns:
        List of recent activities
    """
    try:
        user_id = get_jwt_identity()
        limit = request.args.get('limit', 20, type=int)
        hours = request.args.get('hours', 72, type=int)
        
        connection = get_db_connection()
        activity_model = ActivityLog(connection)
        
        # Get recent activity
        activities = activity_model.get_recent(user_id, hours=hours, limit=limit)
        close_db_connection(connection)
        
        return jsonify({
            'activities': activities,
            'count': len(activities)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch activity', 'message': str(e)}), 500

