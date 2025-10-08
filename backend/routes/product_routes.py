# Product Routes
# API endpoints for product sourcing and management

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.product import Product
from backend.models.activity import ActivityLog
from backend.utils.db import get_db_connection, close_db_connection

# Create blueprint for product routes
bp = Blueprint('products', __name__)


@bp.route('', methods=['GET'])
@jwt_required()
def get_products():
    """
    Get products for the current user
    
    Query Parameters:
        project_id: Filter by project (optional)
        category: Filter by category (optional)
        style: Filter by style (optional)
        max_price: Maximum price filter (optional)
        limit: Maximum number of products (default: 100)
    
    Returns:
        List of products
    """
    try:
        user_id = get_jwt_identity()
        project_id = request.args.get('project_id', None, type=int)
        limit = request.args.get('limit', 100, type=int)
        
        connection = get_db_connection()
        product_model = Product(connection)
        
        if project_id:
            # Get products for specific project
            products = product_model.get_by_project(project_id)
        else:
            # Build filters from query parameters
            filters = {}
            if request.args.get('category'):
                filters['category'] = request.args.get('category')
            if request.args.get('style'):
                filters['style'] = request.args.get('style')
            if request.args.get('max_price'):
                filters['max_price'] = float(request.args.get('max_price'))
            if request.args.get('vendor'):
                filters['vendor'] = request.args.get('vendor')
            
            # Search with filters if provided, otherwise get all
            if filters:
                products = product_model.search(user_id, filters)
            else:
                products = product_model.get_by_user(user_id, limit=limit)
        
        close_db_connection(connection)
        
        return jsonify({
            'products': products,
            'count': len(products)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch products', 'message': str(e)}), 500


@bp.route('/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    """
    Get a specific product by ID
    
    Args:
        product_id: The product's ID
    
    Returns:
        Product data
    """
    try:
        connection = get_db_connection()
        product_model = Product(connection)
        
        # Get product
        product = product_model.get_by_id(product_id)
        close_db_connection(connection)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        return jsonify({'product': product}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch product', 'message': str(e)}), 500


@bp.route('', methods=['POST'])
@jwt_required()
def create_product():
    """
    Add a new product to collection
    
    Expected JSON:
        {
            "project_id": 1,
            "name": "Modern Sofa",
            "price": 1200,
            "vendor": "IKEA",
            "product_url": "https://...",
            "image_url": "https://...",
            "category": "furniture",
            "style": "modern",
            "color": "grey"
        }
    
    Returns:
        Created product data
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name') or not data.get('price'):
            return jsonify({'error': 'Product name and price are required'}), 400
        
        connection = get_db_connection()
        product_model = Product(connection)
        
        # Create product
        product_id = product_model.create(
            user_id=user_id,
            name=data['name'],
            price=data['price'],
            project_id=data.get('project_id'),
            description=data.get('description'),
            vendor=data.get('vendor'),
            product_url=data.get('product_url'),
            image_url=data.get('image_url'),
            category=data.get('category'),
            style=data.get('style'),
            color=data.get('color')
        )
        
        if not product_id:
            close_db_connection(connection)
            return jsonify({'error': 'Failed to create product'}), 500
        
        # Log activity
        activity_model = ActivityLog(connection)
        activity_model.log(user_id, 'product_added', 'product', product_id, 
                          {'product_name': data['name'], 'price': data['price']})
        
        # Get the created product
        product = product_model.get_by_id(product_id)
        close_db_connection(connection)
        
        return jsonify({
            'message': 'Product added successfully',
            'product': product
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Failed to create product', 'message': str(e)}), 500


@bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    """
    Update an existing product
    
    Args:
        product_id: The product's ID
    
    Expected JSON:
        Any product fields to update
    
    Returns:
        Success message
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        connection = get_db_connection()
        product_model = Product(connection)
        
        # Update product
        success = product_model.update(product_id, **data)
        
        if success:
            # Log activity
            activity_model = ActivityLog(connection)
            activity_model.log(user_id, 'product_updated', 'product', product_id)
        
        close_db_connection(connection)
        
        if not success:
            return jsonify({'error': 'Failed to update product or product not found'}), 404
        
        return jsonify({'message': 'Product updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to update product', 'message': str(e)}), 500


@bp.route('/<int:product_id>/purchase', methods=['POST'])
@jwt_required()
def mark_purchased(product_id):
    """
    Mark a product as purchased
    
    Args:
        product_id: The product's ID
    
    Returns:
        Success message
    """
    try:
        user_id = get_jwt_identity()
        
        connection = get_db_connection()
        product_model = Product(connection)
        
        # Mark as purchased
        success = product_model.mark_purchased(product_id)
        
        if success:
            # Log activity
            activity_model = ActivityLog(connection)
            activity_model.log(user_id, 'product_purchased', 'product', product_id)
        
        close_db_connection(connection)
        
        if not success:
            return jsonify({'error': 'Failed to mark product as purchased'}), 404
        
        return jsonify({'message': 'Product marked as purchased'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to update product', 'message': str(e)}), 500


@bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    """
    Delete a product
    
    Args:
        product_id: The product's ID
    
    Returns:
        Success message
    """
    try:
        user_id = get_jwt_identity()
        
        connection = get_db_connection()
        product_model = Product(connection)
        
        # Delete product
        success = product_model.delete(product_id)
        
        if success:
            # Log activity
            activity_model = ActivityLog(connection)
            activity_model.log(user_id, 'product_deleted', 'product', product_id)
        
        close_db_connection(connection)
        
        if not success:
            return jsonify({'error': 'Failed to delete product or product not found'}), 404
        
        return jsonify({'message': 'Product deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to delete product', 'message': str(e)}), 500


@bp.route('/project/<int:project_id>/budget-summary', methods=['GET'])
@jwt_required()
def get_budget_summary(project_id):
    """
    Get budget summary for products in a project
    
    Args:
        project_id: The project's ID
    
    Returns:
        Budget summary with totals
    """
    try:
        connection = get_db_connection()
        product_model = Product(connection)
        
        # Get budget summary
        summary = product_model.get_project_budget_summary(project_id)
        close_db_connection(connection)
        
        return jsonify({'summary': summary}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch budget summary', 'message': str(e)}), 500

