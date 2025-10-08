# Project model - represents interior design projects
# Manages project lifecycle, budget tracking, and AI insights

import json
from datetime import datetime

class Project:
    """Project model for managing interior design projects"""
    
    def __init__(self, connection):
        """Initialize with database connection"""
        self.connection = connection
    
    def create(self, user_id, title, client_id=None, description=None, 
               budget=None, start_date=None, deadline=None):
        """
        Create a new project
        
        Args:
            user_id: ID of the designer creating the project
            title: Project title
            client_id: Associated client ID (optional)
            description: Project description
            budget: Project budget amount
            start_date: Project start date
            deadline: Project deadline
        
        Returns:
            project_id if successful, None otherwise
        """
        try:
            # Initialize AI insights as empty JSON
            ai_insights = json.dumps({})
            
            with self.connection.cursor() as cursor:
                sql = """
                    INSERT INTO projects 
                    (user_id, client_id, title, description, budget, 
                     start_date, deadline, ai_insights)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (user_id, client_id, title, description, 
                                   budget, start_date, deadline, ai_insights))
                self.connection.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error creating project: {e}")
            return None
    
    def get_by_id(self, project_id, user_id):
        """
        Retrieve project by ID (ensures user owns this project)
        
        Args:
            project_id: The project's unique identifier
            user_id: The designer's ID (for authorization)
        
        Returns:
            Dictionary with project data or None if not found
        """
        with self.connection.cursor() as cursor:
            sql = """
                SELECT p.*, c.name as client_name 
                FROM projects p
                LEFT JOIN clients c ON p.client_id = c.id
                WHERE p.id = %s AND p.user_id = %s
            """
            cursor.execute(sql, (project_id, user_id))
            project = cursor.fetchone()
            
            # Parse JSON ai_insights
            if project and project.get('ai_insights'):
                try:
                    project['ai_insights'] = json.loads(project['ai_insights'])
                except:
                    project['ai_insights'] = {}
            
            return project
    
    def get_all(self, user_id, status=None, limit=100, offset=0):
        """
        Get all projects for a specific designer
        
        Args:
            user_id: The designer's ID
            status: Filter by status (optional)
            limit: Maximum number of projects to return
            offset: Number of projects to skip (for pagination)
        
        Returns:
            List of project dictionaries
        """
        with self.connection.cursor() as cursor:
            if status:
                sql = """
                    SELECT p.*, c.name as client_name 
                    FROM projects p
                    LEFT JOIN clients c ON p.client_id = c.id
                    WHERE p.user_id = %s AND p.status = %s
                    ORDER BY p.created_at DESC 
                    LIMIT %s OFFSET %s
                """
                cursor.execute(sql, (user_id, status, limit, offset))
            else:
                sql = """
                    SELECT p.*, c.name as client_name 
                    FROM projects p
                    LEFT JOIN clients c ON p.client_id = c.id
                    WHERE p.user_id = %s 
                    ORDER BY p.created_at DESC 
                    LIMIT %s OFFSET %s
                """
                cursor.execute(sql, (user_id, limit, offset))
            
            projects = cursor.fetchall()
            
            # Parse JSON for each project
            for project in projects:
                if project.get('ai_insights'):
                    try:
                        project['ai_insights'] = json.loads(project['ai_insights'])
                    except:
                        project['ai_insights'] = {}
            
            return projects
    
    def update(self, project_id, user_id, **kwargs):
        """
        Update project information
        
        Args:
            project_id: The project's ID
            user_id: The designer's ID (for authorization)
            **kwargs: Fields to update
        
        Returns:
            True if successful, False otherwise
        """
        try:
            allowed_fields = ['title', 'description', 'status', 'budget', 
                            'spent', 'start_date', 'deadline', 'client_id']
            
            update_fields = []
            values = []
            
            for field, value in kwargs.items():
                if field in allowed_fields and value is not None:
                    update_fields.append(f"{field} = %s")
                    values.append(value)
            
            if not update_fields:
                return False
            
            values.extend([user_id, project_id])
            
            with self.connection.cursor() as cursor:
                sql = f"""
                    UPDATE projects 
                    SET {', '.join(update_fields)}, updated_at = NOW()
                    WHERE user_id = %s AND id = %s
                """
                cursor.execute(sql, values)
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating project: {e}")
            return False
    
    def delete(self, project_id, user_id):
        """
        Delete a project
        
        Args:
            project_id: The project's ID
            user_id: The designer's ID (for authorization)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM projects WHERE id = %s AND user_id = %s"
                cursor.execute(sql, (project_id, user_id))
                self.connection.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def update_ai_insights(self, project_id, user_id, insights_data):
        """
        Update AI-generated insights for project
        
        Args:
            project_id: The project's ID
            user_id: The designer's ID
            insights_data: Dictionary with AI insights
        
        Returns:
            True if successful, False otherwise
        """
        try:
            insights_json = json.dumps(insights_data)
            
            with self.connection.cursor() as cursor:
                sql = """
                    UPDATE projects 
                    SET ai_insights = %s 
                    WHERE id = %s AND user_id = %s
                """
                cursor.execute(sql, (insights_json, project_id, user_id))
                self.connection.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def get_dashboard_stats(self, user_id):
        """
        Get project statistics for dashboard overview
        
        Args:
            user_id: The designer's ID
        
        Returns:
            Dictionary with project statistics
        """
        with self.connection.cursor() as cursor:
            # Total projects
            cursor.execute("""
                SELECT COUNT(*) as count FROM projects WHERE user_id = %s
            """, (user_id,))
            total = cursor.fetchone()['count']
            
            # Active projects (in_progress)
            cursor.execute("""
                SELECT COUNT(*) as count FROM projects 
                WHERE user_id = %s AND status = 'in_progress'
            """, (user_id,))
            active = cursor.fetchone()['count']
            
            # Overdue projects (deadline passed and not completed)
            cursor.execute("""
                SELECT COUNT(*) as count FROM projects 
                WHERE user_id = %s AND deadline < CURDATE() 
                AND status != 'completed'
            """, (user_id,))
            overdue = cursor.fetchone()['count']
            
            # Budget overview
            cursor.execute("""
                SELECT 
                    SUM(budget) as total_budget,
                    SUM(spent) as total_spent
                FROM projects 
                WHERE user_id = %s AND status != 'completed'
            """, (user_id,))
            budget_data = cursor.fetchone()
            
            return {
                'total_projects': total,
                'active_projects': active,
                'overdue_projects': overdue,
                'total_budget': float(budget_data['total_budget'] or 0),
                'total_spent': float(budget_data['total_spent'] or 0)
            }
    
    def add_expense(self, project_id, user_id, amount):
        """
        Add expense to project (increment spent amount)
        
        Args:
            project_id: The project's ID
            user_id: The designer's ID
            amount: Amount to add to spent
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    UPDATE projects 
                    SET spent = spent + %s 
                    WHERE id = %s AND user_id = %s
                """
                cursor.execute(sql, (amount, project_id, user_id))
                self.connection.commit()
                return cursor.rowcount > 0
        except:
            return False

