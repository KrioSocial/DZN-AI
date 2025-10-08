# Backend configuration file for AI Studio
# This file centralizes all configuration settings for the Flask application

import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class with default settings"""
    
    # Flask core configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_APP = os.getenv('FLASK_APP', 'backend/app.py')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # JWT configuration for authentication
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)  # Tokens expire after 24 hours
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # Refresh tokens expire after 30 days
    
    # Database configuration - using SQLite for development
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_NAME = os.getenv('DB_NAME', 'ai_studio')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    # Use SQLite for development (easier setup)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///ai_studio.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking to save resources
    SQLALCHEMY_ECHO = FLASK_ENV == 'development'  # Log SQL queries in development
    
    # OpenAI API configuration for AI features
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = 'gpt-4-turbo-preview'  # Model for text generation
    OPENAI_IMAGE_MODEL = 'dall-e-3'  # Model for image generation
    
    # Email configuration using SendGrid
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.sendgrid.net')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'apikey')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@aistudio.design')
    
    # Stripe payment configuration
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
    STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', '')
    
    # File upload configuration
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB default
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}
    
    # Frontend URL for CORS
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5000')
    
    # API configuration
    API_PREFIX = '/api'
    API_VERSION = 'v1'
    
    # Subscription tier limits
    TIER_LIMITS = {
        'free': {
            'projects': 2,
            'ai_generations': 5,
            'storage_mb': 100
        },
        'pro': {
            'projects': -1,  # -1 means unlimited
            'ai_generations': -1,
            'storage_mb': 5000
        },
        'agency': {
            'projects': -1,
            'ai_generations': -1,
            'storage_mb': 20000
        }
    }
    
    # Google Calendar API (for Phase 3)
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', '')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', '')


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    TESTING = False
    
    # Override with more secure settings in production
    # Ensure SECRET_KEY and JWT_SECRET_KEY are strong random values


class TestingConfig(Config):
    """Testing environment configuration"""
    DEBUG = True
    TESTING = True
    
    # Use separate test database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# Configuration dictionary for easy access
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Returns the appropriate configuration based on FLASK_ENV"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])

