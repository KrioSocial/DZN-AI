#!/usr/bin/env python3
"""
Simple test server for AI Studio authentication
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import generate_password_hash, check_password_hash
import sqlite3
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # No expiration for testing

# Enable CORS
CORS(app)

# Initialize JWT
jwt = JWTManager(app)

# Database path
DB_PATH = 'ai_studio.db'

def get_db_connection():
    """Get SQLite database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'AI Studio API is running',
        'version': '1.0.0'
    }), 200

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        if not data.get('name') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Name, email, and password are required'}), 400
        
        # Hash password
        password_hash = generate_password_hash(data['password']).decode('utf-8')
        
        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Insert new user
            cursor.execute("""
                INSERT INTO users (name, email, password_hash, role, subscription_tier, ai_generations_limit)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (data['name'], data['email'], password_hash, 'designer', 'free', 5))
            
            user_id = cursor.lastrowid
            conn.commit()
            
            return jsonify({
                'message': 'Registration successful',
                'user_id': user_id
            }), 201
            
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Email already exists'}), 409
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({'error': 'Registration failed', 'message': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get user by email
        cursor.execute("SELECT * FROM users WHERE email = ?", (data['email'],))
        user = cursor.fetchone()
        
        if not user or not check_password_hash(user['password_hash'], data['password']):
            conn.close()
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Create JWT token
        access_token = create_access_token(identity=user['id'])
        
        conn.close()
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'role': user['role'],
                'subscription_tier': user['subscription_tier']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Login failed', 'message': str(e)}), 500

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        user_id = get_jwt_identity()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        
        conn.close()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'role': user['role'],
                'subscription_tier': user['subscription_tier']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch profile', 'message': str(e)}), 500

if __name__ == '__main__':
    print("🚀 AI Studio Test Server Starting...")
    print("📍 Server: http://localhost:5001")
    print("🔧 Testing authentication endpoints")
    print("\n✨ Ready for testing!\n")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
