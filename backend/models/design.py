# Design model - represents AI-generated design concepts
# Manages moodboards, color palettes, and AI design generations

import json
from datetime import datetime

class Design:
    """Design model for AI-generated design concepts"""
    
    def __init__(self, connection):
        """Initialize with database connection"""
        self.connection = connection
    
    def create(self, project_id, user_id, room_type, style, budget=None, keywords=None):
        """
        Create a new design entry (will be populated with AI-generated content)
        
        Args:
            project_id: ID of the project this design belongs to
            user_id: ID of the designer
            room_type: Type of room (bedroom, living room, etc.)
            style: Design style (modern, minimalist, etc.)
            budget: Budget constraint
            keywords: Additional keywords for AI generation
        
        Returns:
            design_id if successful, None otherwise
        """
        try:
            # Initialize empty JSON arrays for outputs
            image_urls = json.dumps([])
            color_palette = json.dumps([])
            product_list = json.dumps([])
            
            with self.connection.cursor() as cursor:
                sql = """
                    INSERT INTO designs 
                    (project_id, user_id, room_type, style, budget, keywords,
                     image_urls, color_palette, product_list)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (project_id, user_id, room_type, style, 
                                   budget, keywords, image_urls, color_palette, product_list))
                self.connection.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error creating design: {e}")
            return None
    
    def get_by_id(self, design_id):
        """
        Retrieve design by ID
        
        Args:
            design_id: The design's unique identifier
        
        Returns:
            Dictionary with design data or None if not found
        """
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM designs WHERE id = %s"
            cursor.execute(sql, (design_id,))
            design = cursor.fetchone()
            
            # Parse JSON fields
            if design:
                try:
                    design['image_urls'] = json.loads(design['image_urls'] or '[]')
                    design['color_palette'] = json.loads(design['color_palette'] or '[]')
                    design['product_list'] = json.loads(design['product_list'] or '[]')
                except:
                    design['image_urls'] = []
                    design['color_palette'] = []
                    design['product_list'] = []
            
            return design
    
    def get_by_project(self, project_id):
        """
        Get all designs for a specific project
        
        Args:
            project_id: The project's ID
        
        Returns:
            List of design dictionaries
        """
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM designs 
                WHERE project_id = %s
                ORDER BY created_at DESC
            """
            cursor.execute(sql, (project_id,))
            designs = cursor.fetchall()
            
            # Parse JSON for each design
            for design in designs:
                try:
                    design['image_urls'] = json.loads(design['image_urls'] or '[]')
                    design['color_palette'] = json.loads(design['color_palette'] or '[]')
                    design['product_list'] = json.loads(design['product_list'] or '[]')
                except:
                    design['image_urls'] = []
                    design['color_palette'] = []
                    design['product_list'] = []
            
            return designs
    
    def get_by_user(self, user_id, limit=50):
        """
        Get all designs created by a user
        
        Args:
            user_id: The designer's ID
            limit: Maximum number of designs to return
        
        Returns:
            List of design dictionaries
        """
        with self.connection.cursor() as cursor:
            sql = """
                SELECT d.*, p.title as project_title 
                FROM designs d
                JOIN projects p ON d.project_id = p.id
                WHERE d.user_id = %s
                ORDER BY d.created_at DESC
                LIMIT %s
            """
            cursor.execute(sql, (user_id, limit))
            designs = cursor.fetchall()
            
            # Parse JSON for each design
            for design in designs:
                try:
                    design['image_urls'] = json.loads(design['image_urls'] or '[]')
                    design['color_palette'] = json.loads(design['color_palette'] or '[]')
                    design['product_list'] = json.loads(design['product_list'] or '[]')
                except:
                    design['image_urls'] = []
                    design['color_palette'] = []
                    design['product_list'] = []
            
            return designs
    
    def update_outputs(self, design_id, image_urls=None, color_palette=None, 
                      description=None, product_list=None):
        """
        Update design with AI-generated outputs
        
        Args:
            design_id: The design's ID
            image_urls: List of generated image URLs
            color_palette: List of hex color codes
            description: AI-generated description
            product_list: List of suggested products
        
        Returns:
            True if successful, False otherwise
        """
        try:
            updates = []
            values = []
            
            if image_urls is not None:
                updates.append("image_urls = %s")
                values.append(json.dumps(image_urls))
            
            if color_palette is not None:
                updates.append("color_palette = %s")
                values.append(json.dumps(color_palette))
            
            if description is not None:
                updates.append("description = %s")
                values.append(description)
            
            if product_list is not None:
                updates.append("product_list = %s")
                values.append(json.dumps(product_list))
            
            if not updates:
                return False
            
            values.append(design_id)
            
            with self.connection.cursor() as cursor:
                sql = f"UPDATE designs SET {', '.join(updates)} WHERE id = %s"
                cursor.execute(sql, values)
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating design outputs: {e}")
            return False
    
    def delete(self, design_id):
        """
        Delete a design
        
        Args:
            design_id: The design's ID
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM designs WHERE id = %s"
                cursor.execute(sql, (design_id,))
                self.connection.commit()
                return cursor.rowcount > 0
        except:
            return False

