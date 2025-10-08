# Calendar model - represents calendar events and automations
# Manages meetings, deadlines, reminders, and automated actions

from datetime import datetime

class CalendarEvent:
    """Calendar event model for scheduling and automations"""
    
    def __init__(self, connection):
        """Initialize with database connection"""
        self.connection = connection
    
    def create(self, user_id, title, start_time, event_type='meeting', 
               end_time=None, description=None, project_id=None, client_id=None, 
               location=None, is_automated=False):
        """
        Create a new calendar event
        
        Args:
            user_id: ID of the designer
            title: Event title
            start_time: Event start datetime
            event_type: Type of event (meeting, deadline, reminder, automation)
            end_time: Event end datetime (optional)
            description: Event description
            project_id: Associated project (optional)
            client_id: Associated client (optional)
            location: Event location
            is_automated: Whether this is an automated event
        
        Returns:
            event_id if successful, None otherwise
        """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    INSERT INTO calendar_events 
                    (user_id, project_id, client_id, title, description, 
                     event_type, start_time, end_time, location, is_automated)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (user_id, project_id, client_id, title, 
                                   description, event_type, start_time, end_time, 
                                   location, is_automated))
                self.connection.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error creating calendar event: {e}")
            return None
    
    def get_by_id(self, event_id, user_id):
        """
        Retrieve event by ID
        
        Args:
            event_id: The event's unique identifier
            user_id: The designer's ID (for authorization)
        
        Returns:
            Dictionary with event data or None if not found
        """
        with self.connection.cursor() as cursor:
            sql = """
                SELECT e.*, c.name as client_name, p.title as project_title
                FROM calendar_events e
                LEFT JOIN clients c ON e.client_id = c.id
                LEFT JOIN projects p ON e.project_id = p.id
                WHERE e.id = %s AND e.user_id = %s
            """
            cursor.execute(sql, (event_id, user_id))
            return cursor.fetchone()
    
    def get_by_date_range(self, user_id, start_date, end_date):
        """
        Get events within a date range
        
        Args:
            user_id: The designer's ID
            start_date: Range start datetime
            end_date: Range end datetime
        
        Returns:
            List of events
        """
        with self.connection.cursor() as cursor:
            sql = """
                SELECT e.*, c.name as client_name, p.title as project_title
                FROM calendar_events e
                LEFT JOIN clients c ON e.client_id = c.id
                LEFT JOIN projects p ON e.project_id = p.id
                WHERE e.user_id = %s 
                AND e.start_time BETWEEN %s AND %s
                ORDER BY e.start_time ASC
            """
            cursor.execute(sql, (user_id, start_date, end_date))
            return cursor.fetchall()
    
    def get_upcoming(self, user_id, limit=20):
        """
        Get upcoming events for a designer
        
        Args:
            user_id: The designer's ID
            limit: Maximum number of events to return
        
        Returns:
            List of upcoming events
        """
        with self.connection.cursor() as cursor:
            sql = """
                SELECT e.*, c.name as client_name, p.title as project_title
                FROM calendar_events e
                LEFT JOIN clients c ON e.client_id = c.id
                LEFT JOIN projects p ON e.project_id = p.id
                WHERE e.user_id = %s 
                AND e.start_time >= NOW()
                ORDER BY e.start_time ASC
                LIMIT %s
            """
            cursor.execute(sql, (user_id, limit))
            return cursor.fetchall()
    
    def get_by_project(self, project_id):
        """
        Get all events for a specific project
        
        Args:
            project_id: The project's ID
        
        Returns:
            List of events
        """
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM calendar_events 
                WHERE project_id = %s
                ORDER BY start_time ASC
            """
            cursor.execute(sql, (project_id,))
            return cursor.fetchall()
    
    def update(self, event_id, user_id, **kwargs):
        """
        Update event information
        
        Args:
            event_id: The event's ID
            user_id: The designer's ID
            **kwargs: Fields to update
        
        Returns:
            True if successful, False otherwise
        """
        try:
            allowed_fields = ['title', 'description', 'start_time', 'end_time', 
                            'location', 'event_type', 'project_id', 'client_id']
            
            update_fields = []
            values = []
            
            for field, value in kwargs.items():
                if field in allowed_fields and value is not None:
                    update_fields.append(f"{field} = %s")
                    values.append(value)
            
            if not update_fields:
                return False
            
            values.extend([user_id, event_id])
            
            with self.connection.cursor() as cursor:
                sql = f"""
                    UPDATE calendar_events 
                    SET {', '.join(update_fields)}
                    WHERE user_id = %s AND id = %s
                """
                cursor.execute(sql, values)
                self.connection.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def delete(self, event_id, user_id):
        """
        Delete an event
        
        Args:
            event_id: The event's ID
            user_id: The designer's ID
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM calendar_events WHERE id = %s AND user_id = %s"
                cursor.execute(sql, (event_id, user_id))
                self.connection.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def mark_reminder_sent(self, event_id):
        """
        Mark reminder as sent for an event
        
        Args:
            event_id: The event's ID
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE calendar_events SET reminder_sent = TRUE WHERE id = %s"
                cursor.execute(sql, (event_id,))
                self.connection.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def get_pending_reminders(self, user_id):
        """
        Get events that need reminders sent (24 hours before)
        
        Args:
            user_id: The designer's ID
        
        Returns:
            List of events needing reminders
        """
        with self.connection.cursor() as cursor:
            sql = """
                SELECT e.*, c.name as client_name, p.title as project_title
                FROM calendar_events e
                LEFT JOIN clients c ON e.client_id = c.id
                LEFT JOIN projects p ON e.project_id = p.id
                WHERE e.user_id = %s 
                AND e.reminder_sent = FALSE
                AND e.start_time BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 24 HOUR)
                ORDER BY e.start_time ASC
            """
            cursor.execute(sql, (user_id,))
            return cursor.fetchall()

