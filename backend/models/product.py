# Product model - represents sourced products for projects
# Manages product catalog and shopping lists

from datetime import datetime

class Product:
    """Product model for product sourcing and management"""
    
    def __init__(self, connection):
        """Initialize with database connection"""
        self.connection = connection
    
    def create(self, user_id, name, price, project_id=None, description=None,
               vendor=None, product_url=None, image_url=None, category=None, 
               style=None, color=None):
        """
        Create a new product entry
        
        Args:
            user_id: ID of the designer
            name: Product name
            price: Product price
            project_id: Associated project (optional)
            description: Product description
            vendor: Vendor/brand name
            product_url: Link to product page
            image_url: Product image URL
            category: Product category
            style: Style classification
            color: Primary color
        
        Returns:
            product_id if successful, None otherwise
        """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    INSERT INTO products 
                    (user_id, project_id, name, description, price, vendor,
                     product_url, image_url, category, style, color)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (user_id, project_id, name, description, 
                                   price, vendor, product_url, image_url, 
                                   category, style, color))
                self.connection.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error creating product: {e}")
            return None
    
    def get_by_id(self, product_id):
        """
        Retrieve product by ID
        
        Args:
            product_id: The product's unique identifier
        
        Returns:
            Dictionary with product data or None if not found
        """
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM products WHERE id = %s"
            cursor.execute(sql, (product_id,))
            return cursor.fetchone()
    
    def get_by_project(self, project_id):
        """
        Get all products for a specific project
        
        Args:
            project_id: The project's ID
        
        Returns:
            List of product dictionaries
        """
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM products 
                WHERE project_id = %s
                ORDER BY created_at DESC
            """
            cursor.execute(sql, (project_id,))
            return cursor.fetchall()
    
    def get_by_user(self, user_id, limit=100):
        """
        Get all products saved by a user
        
        Args:
            user_id: The designer's ID
            limit: Maximum number of products to return
        
        Returns:
            List of product dictionaries
        """
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM products 
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT %s
            """
            cursor.execute(sql, (user_id, limit))
            return cursor.fetchall()
    
    def search(self, user_id, filters=None):
        """
        Search products with filters
        
        Args:
            user_id: The designer's ID
            filters: Dictionary with search filters (category, style, color, max_price)
        
        Returns:
            List of matching products
        """
        query = "SELECT * FROM products WHERE user_id = %s"
        params = [user_id]
        
        if filters:
            if filters.get('category'):
                query += " AND category = %s"
                params.append(filters['category'])
            
            if filters.get('style'):
                query += " AND style = %s"
                params.append(filters['style'])
            
            if filters.get('color'):
                query += " AND color = %s"
                params.append(filters['color'])
            
            if filters.get('max_price'):
                query += " AND price <= %s"
                params.append(filters['max_price'])
            
            if filters.get('vendor'):
                query += " AND vendor LIKE %s"
                params.append(f"%{filters['vendor']}%")
        
        query += " ORDER BY created_at DESC"
        
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def mark_purchased(self, product_id):
        """
        Mark product as purchased
        
        Args:
            product_id: The product's ID
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE products SET is_purchased = TRUE WHERE id = %s"
                cursor.execute(sql, (product_id,))
                self.connection.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def update(self, product_id, **kwargs):
        """
        Update product information
        
        Args:
            product_id: The product's ID
            **kwargs: Fields to update
        
        Returns:
            True if successful, False otherwise
        """
        try:
            allowed_fields = ['name', 'description', 'price', 'vendor', 
                            'product_url', 'image_url', 'category', 'style', 
                            'color', 'project_id']
            
            update_fields = []
            values = []
            
            for field, value in kwargs.items():
                if field in allowed_fields and value is not None:
                    update_fields.append(f"{field} = %s")
                    values.append(value)
            
            if not update_fields:
                return False
            
            values.append(product_id)
            
            with self.connection.cursor() as cursor:
                sql = f"UPDATE products SET {', '.join(update_fields)} WHERE id = %s"
                cursor.execute(sql, values)
                self.connection.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def delete(self, product_id):
        """
        Delete a product
        
        Args:
            product_id: The product's ID
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM products WHERE id = %s"
                cursor.execute(sql, (product_id,))
                self.connection.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def get_project_budget_summary(self, project_id):
        """
        Get budget summary for products in a project
        
        Args:
            project_id: The project's ID
        
        Returns:
            Dictionary with budget summary
        """
        with self.connection.cursor() as cursor:
            sql = """
                SELECT 
                    COUNT(*) as total_items,
                    SUM(price) as total_value,
                    SUM(CASE WHEN is_purchased = TRUE THEN price ELSE 0 END) as purchased_value,
                    SUM(CASE WHEN is_purchased = FALSE THEN price ELSE 0 END) as pending_value
                FROM products
                WHERE project_id = %s
            """
            cursor.execute(sql, (project_id,))
            result = cursor.fetchone()
            
            return {
                'total_items': result['total_items'],
                'total_value': float(result['total_value'] or 0),
                'purchased_value': float(result['purchased_value'] or 0),
                'pending_value': float(result['pending_value'] or 0)
            }

