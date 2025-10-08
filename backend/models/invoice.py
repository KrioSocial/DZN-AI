# Invoice model - represents financial documents
# Manages invoices, quotes, and payment tracking

from datetime import datetime, date

class Invoice:
    """Invoice model for financial management"""
    
    def __init__(self, connection):
        """Initialize with database connection"""
        self.connection = connection
    
    def create(self, user_id, amount, invoice_type='invoice', project_id=None, 
               client_id=None, issue_date=None, due_date=None, notes=None):
        """
        Create a new invoice or quote
        
        Args:
            user_id: ID of the designer
            amount: Invoice amount
            invoice_type: Type ('invoice' or 'quote')
            project_id: Associated project (optional)
            client_id: Associated client (optional)
            issue_date: Date invoice was issued
            due_date: Payment due date
            notes: Additional notes
        
        Returns:
            invoice_id if successful, None otherwise
        """
        try:
            # Generate unique invoice number
            invoice_number = self._generate_invoice_number(user_id)
            
            # Use current date if not provided
            if not issue_date:
                issue_date = date.today()
            
            with self.connection.cursor() as cursor:
                sql = """
                    INSERT INTO invoices 
                    (user_id, project_id, client_id, invoice_number, type, 
                     amount, issue_date, due_date, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (user_id, project_id, client_id, invoice_number, 
                                   invoice_type, amount, issue_date, due_date, notes))
                self.connection.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error creating invoice: {e}")
            return None
    
    def _generate_invoice_number(self, user_id):
        """
        Generate unique invoice number
        
        Args:
            user_id: The designer's ID
        
        Returns:
            Unique invoice number string
        """
        with self.connection.cursor() as cursor:
            # Count existing invoices for this user
            cursor.execute("SELECT COUNT(*) as count FROM invoices WHERE user_id = %s", (user_id,))
            count = cursor.fetchone()['count']
            
            # Format: INV-USERID-COUNT (e.g., INV-001-00123)
            return f"INV-{user_id:03d}-{count+1:05d}"
    
    def get_by_id(self, invoice_id, user_id):
        """
        Retrieve invoice by ID (ensures user owns this invoice)
        
        Args:
            invoice_id: The invoice's unique identifier
            user_id: The designer's ID (for authorization)
        
        Returns:
            Dictionary with invoice data or None if not found
        """
        with self.connection.cursor() as cursor:
            sql = """
                SELECT i.*, c.name as client_name, p.title as project_title
                FROM invoices i
                LEFT JOIN clients c ON i.client_id = c.id
                LEFT JOIN projects p ON i.project_id = p.id
                WHERE i.id = %s AND i.user_id = %s
            """
            cursor.execute(sql, (invoice_id, user_id))
            return cursor.fetchone()
    
    def get_all(self, user_id, status=None, invoice_type=None, limit=100):
        """
        Get all invoices for a designer
        
        Args:
            user_id: The designer's ID
            status: Filter by status (optional)
            invoice_type: Filter by type (optional)
            limit: Maximum number of invoices to return
        
        Returns:
            List of invoice dictionaries
        """
        query = """
            SELECT i.*, c.name as client_name, p.title as project_title
            FROM invoices i
            LEFT JOIN clients c ON i.client_id = c.id
            LEFT JOIN projects p ON i.project_id = p.id
            WHERE i.user_id = %s
        """
        params = [user_id]
        
        if status:
            query += " AND i.status = %s"
            params.append(status)
        
        if invoice_type:
            query += " AND i.type = %s"
            params.append(invoice_type)
        
        query += " ORDER BY i.created_at DESC LIMIT %s"
        params.append(limit)
        
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def update_status(self, invoice_id, user_id, new_status):
        """
        Update invoice status
        
        Args:
            invoice_id: The invoice's ID
            user_id: The designer's ID
            new_status: New status value
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.connection.cursor() as cursor:
                # If marking as paid, set paid_date
                if new_status == 'paid':
                    sql = """
                        UPDATE invoices 
                        SET status = %s, paid_date = CURDATE()
                        WHERE id = %s AND user_id = %s
                    """
                else:
                    sql = """
                        UPDATE invoices 
                        SET status = %s
                        WHERE id = %s AND user_id = %s
                    """
                
                cursor.execute(sql, (new_status, invoice_id, user_id))
                self.connection.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def update(self, invoice_id, user_id, **kwargs):
        """
        Update invoice information
        
        Args:
            invoice_id: The invoice's ID
            user_id: The designer's ID
            **kwargs: Fields to update
        
        Returns:
            True if successful, False otherwise
        """
        try:
            allowed_fields = ['amount', 'due_date', 'notes', 'status', 'type']
            
            update_fields = []
            values = []
            
            for field, value in kwargs.items():
                if field in allowed_fields and value is not None:
                    update_fields.append(f"{field} = %s")
                    values.append(value)
            
            if not update_fields:
                return False
            
            values.extend([user_id, invoice_id])
            
            with self.connection.cursor() as cursor:
                sql = f"""
                    UPDATE invoices 
                    SET {', '.join(update_fields)}, updated_at = NOW()
                    WHERE user_id = %s AND id = %s
                """
                cursor.execute(sql, values)
                self.connection.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def delete(self, invoice_id, user_id):
        """
        Delete an invoice
        
        Args:
            invoice_id: The invoice's ID
            user_id: The designer's ID
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM invoices WHERE id = %s AND user_id = %s"
                cursor.execute(sql, (invoice_id, user_id))
                self.connection.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def get_financial_summary(self, user_id):
        """
        Get financial summary for dashboard
        
        Args:
            user_id: The designer's ID
        
        Returns:
            Dictionary with financial statistics
        """
        with self.connection.cursor() as cursor:
            # Total revenue (paid invoices)
            cursor.execute("""
                SELECT SUM(amount) as total FROM invoices 
                WHERE user_id = %s AND status = 'paid' AND type = 'invoice'
            """, (user_id,))
            revenue = cursor.fetchone()['total'] or 0
            
            # Pending payments (sent invoices not yet paid)
            cursor.execute("""
                SELECT SUM(amount) as total FROM invoices 
                WHERE user_id = %s AND status = 'sent' AND type = 'invoice'
            """, (user_id,))
            pending = cursor.fetchone()['total'] or 0
            
            # Overdue invoices
            cursor.execute("""
                SELECT COUNT(*) as count, SUM(amount) as total FROM invoices 
                WHERE user_id = %s AND status = 'overdue' AND type = 'invoice'
            """, (user_id,))
            overdue_data = cursor.fetchone()
            
            # Quotes pending
            cursor.execute("""
                SELECT COUNT(*) as count FROM invoices 
                WHERE user_id = %s AND status = 'sent' AND type = 'quote'
            """, (user_id,))
            pending_quotes = cursor.fetchone()['count']
            
            return {
                'total_revenue': float(revenue),
                'pending_payments': float(pending),
                'overdue_count': overdue_data['count'],
                'overdue_amount': float(overdue_data['total'] or 0),
                'pending_quotes': pending_quotes
            }
    
    def check_overdue(self, user_id):
        """
        Check for overdue invoices and update their status
        
        Args:
            user_id: The designer's ID
        
        Returns:
            Number of invoices marked as overdue
        """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    UPDATE invoices 
                    SET status = 'overdue'
                    WHERE user_id = %s 
                    AND status = 'sent' 
                    AND due_date < CURDATE()
                """
                cursor.execute(sql, (user_id,))
                self.connection.commit()
                return cursor.rowcount
        except:
            return 0

