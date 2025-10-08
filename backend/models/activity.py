# Activity model - tracks user actions for AI insights and analytics
# Logs all user activities for pattern analysis and recommendations

import json
from datetime import datetime

class ActivityLog:
    """Activity log model for tracking user actions"""
    
    def __init__(self, connection):
        """Initialize with database connection"""
        self.connection = connection
    
    def log(self, user_id, action, entity_type=None, entity_id=None, details=None):
        """
        Log a user activity
        
        Args:
            user_id: ID of the user performing the action
            action: Action description (e.g., 'created_project', 'generated_design')
            entity_type: Type of entity affected (project, client, design, etc.)
            entity_id: ID of the affected entity
            details: Additional details as dictionary
        
        Returns:
            log_id if successful, None otherwise
        """
        try:
            # Convert details dict to JSON string
            details_json = json.dumps(details) if details else None
            
            with self.connection.cursor() as cursor:
                sql = """
                    INSERT INTO activity_log 
                    (user_id, action, entity_type, entity_id, details)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (user_id, action, entity_type, entity_id, details_json))
                self.connection.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error logging activity: {e}")
            return None
    
    def get_by_user(self, user_id, limit=100, offset=0):
        """
        Get activity log for a specific user
        
        Args:
            user_id: The user's ID
            limit: Maximum number of entries to return
            offset: Number of entries to skip (for pagination)
        
        Returns:
            List of activity log entries
        """
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM activity_log 
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
            """
            cursor.execute(sql, (user_id, limit, offset))
            logs = cursor.fetchall()
            
            # Parse JSON details for each log entry
            for log in logs:
                if log.get('details'):
                    try:
                        log['details'] = json.loads(log['details'])
                    except:
                        log['details'] = {}
            
            return logs
    
    def get_by_entity(self, entity_type, entity_id, limit=50):
        """
        Get activity log for a specific entity
        
        Args:
            entity_type: Type of entity (project, client, etc.)
            entity_id: The entity's ID
            limit: Maximum number of entries to return
        
        Returns:
            List of activity log entries
        """
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM activity_log 
                WHERE entity_type = %s AND entity_id = %s
                ORDER BY created_at DESC
                LIMIT %s
            """
            cursor.execute(sql, (entity_type, entity_id, limit))
            logs = cursor.fetchall()
            
            # Parse JSON details
            for log in logs:
                if log.get('details'):
                    try:
                        log['details'] = json.loads(log['details'])
                    except:
                        log['details'] = {}
            
            return logs
    
    def get_recent(self, user_id, hours=24, limit=50):
        """
        Get recent activity within specified hours
        
        Args:
            user_id: The user's ID
            hours: Number of hours to look back
            limit: Maximum number of entries to return
        
        Returns:
            List of recent activity entries
        """
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM activity_log 
                WHERE user_id = %s 
                AND created_at >= DATE_SUB(NOW(), INTERVAL %s HOUR)
                ORDER BY created_at DESC
                LIMIT %s
            """
            cursor.execute(sql, (user_id, hours, limit))
            logs = cursor.fetchall()
            
            # Parse JSON details
            for log in logs:
                if log.get('details'):
                    try:
                        log['details'] = json.loads(log['details'])
                    except:
                        log['details'] = {}
            
            return logs
    
    def get_action_count(self, user_id, action, days=30):
        """
        Count how many times a user performed a specific action
        
        Args:
            user_id: The user's ID
            action: Action to count
            days: Number of days to look back
        
        Returns:
            Count of actions
        """
        with self.connection.cursor() as cursor:
            sql = """
                SELECT COUNT(*) as count FROM activity_log 
                WHERE user_id = %s 
                AND action = %s
                AND created_at >= DATE_SUB(NOW(), INTERVAL %s DAY)
            """
            cursor.execute(sql, (user_id, action, days))
            result = cursor.fetchone()
            return result['count'] if result else 0
    
    def get_activity_summary(self, user_id, days=7):
        """
        Get summary of user activity for dashboard insights
        
        Args:
            user_id: The user's ID
            days: Number of days to analyze
        
        Returns:
            Dictionary with activity statistics
        """
        with self.connection.cursor() as cursor:
            # Total actions
            cursor.execute("""
                SELECT COUNT(*) as count FROM activity_log 
                WHERE user_id = %s 
                AND created_at >= DATE_SUB(NOW(), INTERVAL %s DAY)
            """, (user_id, days))
            total_actions = cursor.fetchone()['count']
            
            # Most common actions
            cursor.execute("""
                SELECT action, COUNT(*) as count FROM activity_log 
                WHERE user_id = %s 
                AND created_at >= DATE_SUB(NOW(), INTERVAL %s DAY)
                GROUP BY action
                ORDER BY count DESC
                LIMIT 5
            """, (user_id, days))
            top_actions = cursor.fetchall()
            
            # Daily activity trend
            cursor.execute("""
                SELECT DATE(created_at) as date, COUNT(*) as count 
                FROM activity_log 
                WHERE user_id = %s 
                AND created_at >= DATE_SUB(NOW(), INTERVAL %s DAY)
                GROUP BY DATE(created_at)
                ORDER BY date DESC
            """, (user_id, days))
            daily_trend = cursor.fetchall()
            
            return {
                'total_actions': total_actions,
                'top_actions': top_actions,
                'daily_trend': daily_trend
            }
    
    def delete_old_logs(self, days=90):
        """
        Delete activity logs older than specified days (for cleanup)
        
        Args:
            days: Delete logs older than this many days
        
        Returns:
            Number of deleted logs
        """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    DELETE FROM activity_log 
                    WHERE created_at < DATE_SUB(NOW(), INTERVAL %s DAY)
                """
                cursor.execute(sql, (days,))
                self.connection.commit()
                return cursor.rowcount
        except:
            return 0

