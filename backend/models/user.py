# User model - represents interior designer accounts
# Handles user authentication and subscription management

from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash
import sqlite3

class User:
    """User model for interior designers using the platform"""
    
    def __init__(self, connection):
        """Initialize with database connection"""
        self.connection = connection
    
    def create(self, name, email, password, role='designer', subscription_tier='free'):
        """
        Create a new user account
        
        Args:
            name: User's full name
            email: User's email address (must be unique)
            password: Plain text password (will be hashed)
            role: User role (designer or admin)
            subscription_tier: Subscription level (free, pro, agency)
        
        Returns:
            user_id if successful, None if email already exists
        """
        try:
            # Hash the password for security
            password_hash = generate_password_hash(password).decode('utf-8')
            
            # Set AI generation limits based on tier
            limits = {
                'free': 5,
                'pro': 999999,  # Effectively unlimited
                'agency': 999999
            }
            ai_limit = limits.get(subscription_tier, 5)
            
            with self.connection.cursor() as cursor:
                # SQL query to insert new user
                sql = """
                    INSERT INTO users (name, email, password_hash, role, subscription_tier, ai_generations_limit)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (name, email, password_hash, role, subscription_tier, ai_limit))
                self.connection.commit()
                
                # Return the newly created user ID
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Email already exists
            return None
    
    def get_by_id(self, user_id):
        """
        Retrieve user by their ID
        
        Args:
            user_id: The user's unique identifier
        
        Returns:
            Dictionary with user data or None if not found
        """
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE id = %s"
            cursor.execute(sql, (user_id,))
            return cursor.fetchone()
    
    def get_by_email(self, email):
        """
        Retrieve user by their email address
        
        Args:
            email: The user's email
        
        Returns:
            Dictionary with user data or None if not found
        """
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE email = %s"
            cursor.execute(sql, (email,))
            return cursor.fetchone()
    
    def verify_password(self, email, password):
        """
        Verify user's password during login
        
        Args:
            email: User's email
            password: Plain text password to verify
        
        Returns:
            User data if password is correct, None otherwise
        """
        user = self.get_by_email(email)
        if user and check_password_hash(user['password_hash'], password):
            # Remove password hash from returned data for security
            user_data = dict(user)
            del user_data['password_hash']
            return user_data
        return None
    
    def update_subscription(self, user_id, new_tier):
        """
        Update user's subscription tier
        
        Args:
            user_id: The user's ID
            new_tier: New subscription tier (free, pro, agency)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Update AI generation limits based on new tier
            limits = {
                'free': 5,
                'pro': 999999,
                'agency': 999999
            }
            ai_limit = limits.get(new_tier, 5)
            
            with self.connection.cursor() as cursor:
                sql = """
                    UPDATE users 
                    SET subscription_tier = %s, ai_generations_limit = %s, ai_generations_used = 0
                    WHERE id = %s
                """
                cursor.execute(sql, (new_tier, ai_limit, user_id))
                self.connection.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def increment_ai_usage(self, user_id):
        """
        Increment the AI generations counter for usage tracking
        
        Args:
            user_id: The user's ID
        
        Returns:
            True if successful and under limit, False if limit reached
        """
        user = self.get_by_id(user_id)
        if not user:
            return False
        
        # Check if user has reached their limit
        if user['ai_generations_used'] >= user['ai_generations_limit']:
            return False
        
        with self.connection.cursor() as cursor:
            sql = "UPDATE users SET ai_generations_used = ai_generations_used + 1 WHERE id = %s"
            cursor.execute(sql, (user_id,))
            self.connection.commit()
            return True
    
    def get_stats(self, user_id):
        """
        Get user's usage statistics
        
        Args:
            user_id: The user's ID
        
        Returns:
            Dictionary with usage stats
        """
        with self.connection.cursor() as cursor:
            # Count projects
            cursor.execute("SELECT COUNT(*) as count FROM projects WHERE user_id = %s", (user_id,))
            projects_count = cursor.fetchone()['count']
            
            # Count clients
            cursor.execute("SELECT COUNT(*) as count FROM clients WHERE user_id = %s", (user_id,))
            clients_count = cursor.fetchone()['count']
            
            # Get AI usage
            user = self.get_by_id(user_id)
            
            return {
                'projects_count': projects_count,
                'clients_count': clients_count,
                'ai_generations_used': user['ai_generations_used'],
                'ai_generations_limit': user['ai_generations_limit'],
                'subscription_tier': user['subscription_tier']
            }

