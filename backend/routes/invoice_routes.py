# Invoice Routes
# API endpoints for financial management (invoices and quotes)

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.invoice import Invoice
from backend.models.activity import ActivityLog
from backend.utils.db import get_db_connection, close_db_connection

# Create blueprint for invoice routes
bp = Blueprint('invoices', __name__)


@bp.route('', methods=['GET'])
@jwt_required()
def get_invoices():
    """
    Get all invoices/quotes for the current user
    
    Query Parameters:
        status: Filter by status (optional)
        type: Filter by type (invoice/quote) (optional)
        limit: Maximum number of invoices (default: 100)
    
    Returns:
        List of invoices
    """
    try:
        user_id = get_jwt_identity()
        status = request.args.get('status', None)
        invoice_type = request.args.get('type', None)
        limit = request.args.get('limit', 100, type=int)
        
        connection = get_db_connection()
        invoice_model = Invoice(connection)
        
        # Get invoices with optional filters
        invoices = invoice_model.get_all(user_id, status=status, 
                                        invoice_type=invoice_type, limit=limit)
        
        # Check for overdue invoices
        invoice_model.check_overdue(user_id)
        
        close_db_connection(connection)
        
        return jsonify({
            'invoices': invoices,
            'count': len(invoices)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch invoices', 'message': str(e)}), 500


@bp.route('/<int:invoice_id>', methods=['GET'])
@jwt_required()
def get_invoice(invoice_id):
    """
    Get a specific invoice by ID
    
    Args:
        invoice_id: The invoice's ID
    
    Returns:
        Invoice data with client and project info
    """
    try:
        user_id = get_jwt_identity()
        
        connection = get_db_connection()
        invoice_model = Invoice(connection)
        
        # Get invoice
        invoice = invoice_model.get_by_id(invoice_id, user_id)
        close_db_connection(connection)
        
        if not invoice:
            return jsonify({'error': 'Invoice not found'}), 404
        
        return jsonify({'invoice': invoice}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch invoice', 'message': str(e)}), 500


@bp.route('', methods=['POST'])
@jwt_required()
def create_invoice():
    """
    Create a new invoice or quote
    
    Expected JSON:
        {
            "type": "invoice",  // or "quote"
            "project_id": 1,
            "client_id": 1,
            "amount": 5000,
            "due_date": "2024-02-28",
            "notes": "Payment terms: Net 30"
        }
    
    Returns:
        Created invoice data
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        if not data.get('amount'):
            return jsonify({'error': 'Amount is required'}), 400
        
        connection = get_db_connection()
        invoice_model = Invoice(connection)
        
        # Create invoice
        invoice_id = invoice_model.create(
            user_id=user_id,
            amount=data['amount'],
            invoice_type=data.get('type', 'invoice'),
            project_id=data.get('project_id'),
            client_id=data.get('client_id'),
            issue_date=data.get('issue_date'),
            due_date=data.get('due_date'),
            notes=data.get('notes')
        )
        
        if not invoice_id:
            close_db_connection(connection)
            return jsonify({'error': 'Failed to create invoice'}), 500
        
        # Log activity
        activity_model = ActivityLog(connection)
        activity_model.log(user_id, f'{data.get("type", "invoice")}_created', 
                          'invoice', invoice_id, {'amount': data['amount']})
        
        # Get the created invoice
        invoice = invoice_model.get_by_id(invoice_id, user_id)
        close_db_connection(connection)
        
        return jsonify({
            'message': f'{data.get("type", "invoice").capitalize()} created successfully',
            'invoice': invoice
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Failed to create invoice', 'message': str(e)}), 500


@bp.route('/<int:invoice_id>', methods=['PUT'])
@jwt_required()
def update_invoice(invoice_id):
    """
    Update an existing invoice
    
    Args:
        invoice_id: The invoice's ID
    
    Expected JSON:
        Any invoice fields to update
    
    Returns:
        Success message
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        connection = get_db_connection()
        invoice_model = Invoice(connection)
        
        # Update invoice
        success = invoice_model.update(invoice_id, user_id, **data)
        
        if success:
            # Log activity
            activity_model = ActivityLog(connection)
            activity_model.log(user_id, 'invoice_updated', 'invoice', invoice_id)
        
        close_db_connection(connection)
        
        if not success:
            return jsonify({'error': 'Failed to update invoice or invoice not found'}), 404
        
        return jsonify({'message': 'Invoice updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to update invoice', 'message': str(e)}), 500


@bp.route('/<int:invoice_id>/status', methods=['PUT'])
@jwt_required()
def update_invoice_status(invoice_id):
    """
    Update invoice status
    
    Args:
        invoice_id: The invoice's ID
    
    Expected JSON:
        {
            "status": "paid"  // draft, sent, paid, overdue, cancelled
        }
    
    Returns:
        Success message
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate status
        valid_statuses = ['draft', 'sent', 'paid', 'overdue', 'cancelled']
        if data.get('status') not in valid_statuses:
            return jsonify({'error': 'Invalid status'}), 400
        
        connection = get_db_connection()
        invoice_model = Invoice(connection)
        
        # Update status
        success = invoice_model.update_status(invoice_id, user_id, data['status'])
        
        if success:
            # Log activity
            activity_model = ActivityLog(connection)
            activity_model.log(user_id, 'invoice_status_updated', 'invoice', invoice_id, 
                             {'new_status': data['status']})
        
        close_db_connection(connection)
        
        if not success:
            return jsonify({'error': 'Failed to update status or invoice not found'}), 404
        
        return jsonify({'message': 'Invoice status updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to update status', 'message': str(e)}), 500


@bp.route('/<int:invoice_id>', methods=['DELETE'])
@jwt_required()
def delete_invoice(invoice_id):
    """
    Delete an invoice
    
    Args:
        invoice_id: The invoice's ID
    
    Returns:
        Success message
    """
    try:
        user_id = get_jwt_identity()
        
        connection = get_db_connection()
        invoice_model = Invoice(connection)
        
        # Delete invoice
        success = invoice_model.delete(invoice_id, user_id)
        
        if success:
            # Log activity
            activity_model = ActivityLog(connection)
            activity_model.log(user_id, 'invoice_deleted', 'invoice', invoice_id)
        
        close_db_connection(connection)
        
        if not success:
            return jsonify({'error': 'Failed to delete invoice or invoice not found'}), 404
        
        return jsonify({'message': 'Invoice deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to delete invoice', 'message': str(e)}), 500


@bp.route('/summary', methods=['GET'])
@jwt_required()
def get_financial_summary():
    """
    Get financial summary for the current user
    
    Returns:
        Financial statistics (revenue, pending, overdue, etc.)
    """
    try:
        user_id = get_jwt_identity()
        
        connection = get_db_connection()
        invoice_model = Invoice(connection)
        
        # Get summary
        summary = invoice_model.get_financial_summary(user_id)
        close_db_connection(connection)
        
        return jsonify({'summary': summary}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch financial summary', 'message': str(e)}), 500

