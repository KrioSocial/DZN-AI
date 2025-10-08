# Message model - represents client communications
# Manages messaging between designers and clients with AI features

from datetime import datetime

class Message:
    """Message model for client communication management"""
    
    def __init__(self, connection):
        """Initialize with database connection"""
        self.connection = connection
    
    def create(self, user_id, client_id, sender, message_text, subject=None):
        """
        Create a new message
        
        Args:
            user_id: ID of the designer
            client_id: ID of the client
            sender: Who sent the message ('designer' or 'client')
            message_text: The message content
            subject: Message subject (optional)
        
        Returns:
            message_id if successful, None otherwise
        """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    INSERT INTO messages 
                    (user_id, client_id, sender, subject, message_text)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (user_id, client_id, sender, subject, message_text))
                self.connection.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error creating message: {e}")
            return None
    
    def get_by_id(self, message_id):
        """
        Retrieve message by ID
        
        Args:
            message_id: The message's unique identifier
        
        Returns:
            Dictionary with message data or None if not found
        """
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM messages WHERE id = %s"
            cursor.execute(sql, (message_id,))
            return cursor.fetchone()
    
    def get_by_client(self, client_id, limit=50):
        """
        Get all messages for a specific client
        
        Args:
            client_id: The client's ID
            limit: Maximum number of messages to return
        
        Returns:
            List of message dictionaries
        """
        with self.connection.cursor() as cursor:
            sql = """
                SELECT m.*, c.name as client_name 
                FROM messages m
                JOIN clients c ON m.client_id = c.id
                WHERE m.client_id = %s
                ORDER BY m.created_at DESC
                LIMIT %s
            """
            cursor.execute(sql, (client_id, limit))
            return cursor.fetchall()
    
    def get_recent(self, user_id, limit=20):
        """
        Get recent messages for a designer
        
        Args:
            user_id: The designer's ID
            limit: Maximum number of messages to return
        
        Returns:
            List of recent messages
        """
        with self.connection.cursor() as cursor:
            sql = """
                SELECT m.*, c.name as client_name 
                FROM messages m
                JOIN clients c ON m.client_id = c.id
                WHERE m.user_id = %s
                ORDER BY m.created_at DESC
                LIMIT %s
            """
            cursor.execute(sql, (user_id, limit))
            return cursor.fetchall()
    
    def get_unread(self, user_id):
        """
        Get unread messages for a designer
        
        Args:
            user_id: The designer's ID
        
        Returns:
            List of unread messages
        """
        with self.connection.cursor() as cursor:
            sql = """
                SELECT m.*, c.name as client_name 
                FROM messages m
                JOIN clients c ON m.client_id = c.id
                WHERE m.user_id = %s AND m.is_read = FALSE AND m.sender = 'client'
                ORDER BY m.created_at DESC
            """
            cursor.execute(sql, (user_id,))
            return cursor.fetchall()
    
    def mark_as_read(self, message_id):
        """
        Mark message as read
        
        Args:
            message_id: The message's ID
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE messages SET is_read = TRUE WHERE id = %s"
                cursor.execute(sql, (message_id,))
                self.connection.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def update_ai_summary(self, message_id, summary, sentiment=None):
        """
        Update AI-generated summary and sentiment for message
        
        Args:
            message_id: The message's ID
            summary: AI-generated summary
            sentiment: Detected sentiment (positive, neutral, negative)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    UPDATE messages 
                    SET ai_summary = %s, sentiment = %s
                    WHERE id = %s
                """
                cursor.execute(sql, (summary, sentiment, message_id))
                self.connection.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def get_conversation(self, client_id, limit=100):
        """
        Get full conversation thread with a client
        
        Args:
            client_id: The client's ID
            limit: Maximum number of messages to return
        
        Returns:
            List of messages in chronological order
        """
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM messages 
                WHERE client_id = %s
                ORDER BY created_at ASC
                LIMIT %s
            """
            cursor.execute(sql, (client_id, limit))
            return cursor.fetchall()
    
    def delete(self, message_id):
        """
        Delete a message
        
        Args:
            message_id: The message's ID
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM messages WHERE id = %s"
                cursor.execute(sql, (message_id,))
                self.connection.commit()
                return cursor.rowcount > 0
        except:
            return False

