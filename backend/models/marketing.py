# Marketing model - represents AI-generated marketing content
# Manages social media posts, blogs, emails, and content scheduling

from datetime import datetime

class MarketingContent:
    """Marketing content model for AI-generated marketing materials"""
    
    def __init__(self, connection):
        """Initialize with database connection"""
        self.connection = connection
    
    def create(self, user_id, content_type, content, project_id=None, 
               platform=None, title=None):
        """
        Create new marketing content
        
        Args:
            user_id: ID of the designer
            content_type: Type of content (caption, blog, email, post)
            content: The actual content text
            project_id: Associated project (optional)
            platform: Target platform (Instagram, LinkedIn, etc.)
            title: Content title
        
        Returns:
            content_id if successful, None otherwise
        """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    INSERT INTO marketing_content 
                    (user_id, project_id, content_type, platform, title, content)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (user_id, project_id, content_type, 
                                   platform, title, content))
                self.connection.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error creating marketing content: {e}")
            return None
    
    def get_by_id(self, content_id, user_id):
        """
        Retrieve marketing content by ID
        
        Args:
            content_id: The content's unique identifier
            user_id: The designer's ID (for authorization)
        
        Returns:
            Dictionary with content data or None if not found
        """
        with self.connection.cursor() as cursor:
            sql = """
                SELECT m.*, p.title as project_title
                FROM marketing_content m
                LEFT JOIN projects p ON m.project_id = p.id
                WHERE m.id = %s AND m.user_id = %s
            """
            cursor.execute(sql, (content_id, user_id))
            return cursor.fetchone()
    
    def get_all(self, user_id, content_type=None, status=None, limit=100):
        """
        Get all marketing content for a designer
        
        Args:
            user_id: The designer's ID
            content_type: Filter by content type (optional)
            status: Filter by status (optional)
            limit: Maximum number of items to return
        
        Returns:
            List of content dictionaries
        """
        query = """
            SELECT m.*, p.title as project_title
            FROM marketing_content m
            LEFT JOIN projects p ON m.project_id = p.id
            WHERE m.user_id = %s
        """
        params = [user_id]
        
        if content_type:
            query += " AND m.content_type = %s"
            params.append(content_type)
        
        if status:
            query += " AND m.status = %s"
            params.append(status)
        
        query += " ORDER BY m.created_at DESC LIMIT %s"
        params.append(limit)
        
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def update(self, content_id, user_id, **kwargs):
        """
        Update marketing content
        
        Args:
            content_id: The content's ID
            user_id: The designer's ID
            **kwargs: Fields to update
        
        Returns:
            True if successful, False otherwise
        """
        try:
            allowed_fields = ['title', 'content', 'platform', 'status', 
                            'scheduled_date']
            
            update_fields = []
            values = []
            
            for field, value in kwargs.items():
                if field in allowed_fields and value is not None:
                    update_fields.append(f"{field} = %s")
                    values.append(value)
            
            if not update_fields:
                return False
            
            values.extend([user_id, content_id])
            
            with self.connection.cursor() as cursor:
                sql = f"""
                    UPDATE marketing_content 
                    SET {', '.join(update_fields)}
                    WHERE user_id = %s AND id = %s
                """
                cursor.execute(sql, values)
                self.connection.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def schedule_post(self, content_id, user_id, scheduled_date):
        """
        Schedule content for future posting
        
        Args:
            content_id: The content's ID
            user_id: The designer's ID
            scheduled_date: Date/time to post
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    UPDATE marketing_content 
                    SET status = 'scheduled', scheduled_date = %s
                    WHERE id = %s AND user_id = %s
                """
                cursor.execute(sql, (scheduled_date, content_id, user_id))
                self.connection.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def mark_posted(self, content_id, user_id):
        """
        Mark content as posted
        
        Args:
            content_id: The content's ID
            user_id: The designer's ID
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    UPDATE marketing_content 
                    SET status = 'posted', posted_date = NOW()
                    WHERE id = %s AND user_id = %s
                """
                cursor.execute(sql, (content_id, user_id))
                self.connection.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def delete(self, content_id, user_id):
        """
        Delete marketing content
        
        Args:
            content_id: The content's ID
            user_id: The designer's ID
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM marketing_content WHERE id = %s AND user_id = %s"
                cursor.execute(sql, (content_id, user_id))
                self.connection.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def get_scheduled(self, user_id):
        """
        Get scheduled content that needs to be posted
        
        Args:
            user_id: The designer's ID
        
        Returns:
            List of scheduled content items
        """
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM marketing_content 
                WHERE user_id = %s 
                AND status = 'scheduled' 
                AND scheduled_date <= NOW()
                ORDER BY scheduled_date ASC
            """
            cursor.execute(sql, (user_id,))
            return cursor.fetchall()

