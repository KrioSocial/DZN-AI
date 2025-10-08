# Task model - represents project tasks and milestones
# Manages task lifecycle and progress tracking

from datetime import datetime

class Task:
    """Task model for project task management"""
    
    def __init__(self, connection):
        """Initialize with database connection"""
        self.connection = connection
    
    def create(self, project_id, title, description=None, priority='medium', due_date=None):
        """
        Create a new task
        
        Args:
            project_id: ID of the project this task belongs to
            title: Task title
            description: Task description
            priority: Task priority (low, medium, high)
            due_date: Task due date
        
        Returns:
            task_id if successful, None otherwise
        """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    INSERT INTO tasks 
                    (project_id, title, description, priority, due_date)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (project_id, title, description, priority, due_date))
                self.connection.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error creating task: {e}")
            return None
    
    def get_by_id(self, task_id):
        """
        Retrieve task by ID
        
        Args:
            task_id: The task's unique identifier
        
        Returns:
            Dictionary with task data or None if not found
        """
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM tasks WHERE id = %s"
            cursor.execute(sql, (task_id,))
            return cursor.fetchone()
    
    def get_by_project(self, project_id, status=None):
        """
        Get all tasks for a specific project
        
        Args:
            project_id: The project's ID
            status: Filter by status (optional)
        
        Returns:
            List of task dictionaries
        """
        with self.connection.cursor() as cursor:
            if status:
                sql = """
                    SELECT * FROM tasks 
                    WHERE project_id = %s AND status = %s
                    ORDER BY priority DESC, due_date ASC
                """
                cursor.execute(sql, (project_id, status))
            else:
                sql = """
                    SELECT * FROM tasks 
                    WHERE project_id = %s
                    ORDER BY priority DESC, due_date ASC
                """
                cursor.execute(sql, (project_id,))
            
            return cursor.fetchall()
    
    def update(self, task_id, **kwargs):
        """
        Update task information
        
        Args:
            task_id: The task's ID
            **kwargs: Fields to update
        
        Returns:
            True if successful, False otherwise
        """
        try:
            allowed_fields = ['title', 'description', 'status', 'priority', 'due_date']
            
            update_fields = []
            values = []
            
            for field, value in kwargs.items():
                if field in allowed_fields and value is not None:
                    update_fields.append(f"{field} = %s")
                    values.append(value)
            
            if not update_fields:
                return False
            
            values.append(task_id)
            
            with self.connection.cursor() as cursor:
                sql = f"""
                    UPDATE tasks 
                    SET {', '.join(update_fields)}, updated_at = NOW()
                    WHERE id = %s
                """
                cursor.execute(sql, values)
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating task: {e}")
            return False
    
    def mark_completed(self, task_id):
        """
        Mark task as completed
        
        Args:
            task_id: The task's ID
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    UPDATE tasks 
                    SET status = 'completed', completed_at = NOW()
                    WHERE id = %s
                """
                cursor.execute(sql, (task_id,))
                self.connection.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def delete(self, task_id):
        """
        Delete a task
        
        Args:
            task_id: The task's ID
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM tasks WHERE id = %s"
                cursor.execute(sql, (task_id,))
                self.connection.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def get_overdue_tasks(self, project_id):
        """
        Get overdue tasks for a project
        
        Args:
            project_id: The project's ID
        
        Returns:
            List of overdue tasks
        """
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM tasks 
                WHERE project_id = %s 
                AND due_date < CURDATE() 
                AND status != 'completed'
                ORDER BY due_date ASC
            """
            cursor.execute(sql, (project_id,))
            return cursor.fetchall()

