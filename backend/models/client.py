# Client model - represents interior designer's clients
# Manages client information, preferences, and profiles

import json
from datetime import datetime

class Client:
    """Client model for managing interior design clients"""
    
    def __init__(self, connection):
        """Initialize with database connection"""
        self.connection = connection
    
    def create(self, user_id, name, email=None, phone=None, address=None, 
               style_preferences=None, budget_range=None, notes=None):
        """
        Create a new client profile
        
        Args:
            user_id: ID of the designer who owns this client
            name: Client's full name
            email: Client's email address
            phone: Client's phone number
            address: Client's address
            style_preferences: Description of client's style preferences
            budget_range: Client's budget range
            notes: Additional notes about the client
        
        Returns:
            client_id if successful, None otherwise
        """
        try:
            # Initialize personality profile as empty JSON
            personality_profile = json.dumps({})
            
            with self.connection.cursor() as cursor:
                sql = """
                    INSERT INTO clients 
                    (user_id, name, email, phone, address, style_preferences, 
                     personality_profile, budget_range, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (user_id, name, email, phone, address, 
                                   style_preferences, personality_profile, 
                                   budget_range, notes))
                self.connection.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error creating client: {e}")
            return None
    
    def get_by_id(self, client_id, user_id):
        """
        Retrieve client by ID (ensures user owns this client)
        
        Args:
            client_id: The client's unique identifier
            user_id: The designer's ID (for authorization)
        
        Returns:
            Dictionary with client data or None if not found
        """
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM clients WHERE id = %s AND user_id = %s"
            cursor.execute(sql, (client_id, user_id))
            client = cursor.fetchone()
            
            # Parse JSON personality profile
            if client and client.get('personality_profile'):
                try:
                    client['personality_profile'] = json.loads(client['personality_profile'])
                except:
                    client['personality_profile'] = {}
            
            return client
    
    def get_all(self, user_id, limit=100, offset=0):
        """
        Get all clients for a specific designer
        
        Args:
            user_id: The designer's ID
            limit: Maximum number of clients to return
            offset: Number of clients to skip (for pagination)
        
        Returns:
            List of client dictionaries
        """
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM clients 
                WHERE user_id = %s 
                ORDER BY created_at DESC 
                LIMIT %s OFFSET %s
            """
            cursor.execute(sql, (user_id, limit, offset))
            clients = cursor.fetchall()
            
            # Parse JSON for each client
            for client in clients:
                if client.get('personality_profile'):
                    try:
                        client['personality_profile'] = json.loads(client['personality_profile'])
                    except:
                        client['personality_profile'] = {}
            
            return clients
    
    def update(self, client_id, user_id, **kwargs):
        """
        Update client information
        
        Args:
            client_id: The client's ID
            user_id: The designer's ID (for authorization)
            **kwargs: Fields to update (name, email, phone, etc.)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Build dynamic UPDATE query based on provided fields
            allowed_fields = ['name', 'email', 'phone', 'address', 
                            'style_preferences', 'budget_range', 'notes']
            
            update_fields = []
            values = []
            
            for field, value in kwargs.items():
                if field in allowed_fields and value is not None:
                    update_fields.append(f"{field} = %s")
                    values.append(value)
            
            if not update_fields:
                return False
            
            # Add user_id and client_id to values for WHERE clause
            values.extend([user_id, client_id])
            
            with self.connection.cursor() as cursor:
                sql = f"""
                    UPDATE clients 
                    SET {', '.join(update_fields)}, updated_at = NOW()
                    WHERE user_id = %s AND id = %s
                """
                cursor.execute(sql, values)
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating client: {e}")
            return False
    
    def delete(self, client_id, user_id):
        """
        Delete a client (soft delete - archives the client)
        
        Args:
            client_id: The client's ID
            user_id: The designer's ID (for authorization)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM clients WHERE id = %s AND user_id = %s"
                cursor.execute(sql, (client_id, user_id))
                self.connection.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def update_personality_profile(self, client_id, user_id, profile_data):
        """
        Update AI-generated personality profile for client
        
        Args:
            client_id: The client's ID
            user_id: The designer's ID
            profile_data: Dictionary with personality insights
        
        Returns:
            True if successful, False otherwise
        """
        try:
            profile_json = json.dumps(profile_data)
            
            with self.connection.cursor() as cursor:
                sql = """
                    UPDATE clients 
                    SET personality_profile = %s 
                    WHERE id = %s AND user_id = %s
                """
                cursor.execute(sql, (profile_json, client_id, user_id))
                self.connection.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def search(self, user_id, query):
        """
        Search clients by name or email
        
        Args:
            user_id: The designer's ID
            query: Search query string
        
        Returns:
            List of matching clients
        """
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM clients 
                WHERE user_id = %s AND (name LIKE %s OR email LIKE %s)
                ORDER BY name
            """
            search_term = f"%{query}%"
            cursor.execute(sql, (user_id, search_term, search_term))
            return cursor.fetchall()
    
    def get_with_stats(self, client_id, user_id):
        """
        Get client with additional statistics (projects, messages)
        
        Args:
            client_id: The client's ID
            user_id: The designer's ID
        
        Returns:
            Dictionary with client data and stats
        """
        client = self.get_by_id(client_id, user_id)
        if not client:
            return None
        
        with self.connection.cursor() as cursor:
            # Count active projects
            cursor.execute("""
                SELECT COUNT(*) as count FROM projects 
                WHERE client_id = %s AND status != 'completed'
            """, (client_id,))
            active_projects = cursor.fetchone()['count']
            
            # Count total messages
            cursor.execute("""
                SELECT COUNT(*) as count FROM messages WHERE client_id = %s
            """, (client_id,))
            message_count = cursor.fetchone()['count']
            
            # Get last message date
            cursor.execute("""
                SELECT MAX(created_at) as last_message FROM messages WHERE client_id = %s
            """, (client_id,))
            last_message = cursor.fetchone()['last_message']
            
            client['stats'] = {
                'active_projects': active_projects,
                'message_count': message_count,
                'last_contact': last_message
            }
            
            return client

