# Database utility functions
# Handles database connection and initialization

import sqlite3
from config import get_config

def get_db_connection():
    """
    Create and return a SQLite database connection
    
    Returns:
        Database connection object with row factory for dict-like access
    """
    config = get_config()
    
    try:
        # Extract database path from SQLAlchemy URI
        db_path = config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row  # Enable dict-like access to rows
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise


def init_db():
    """
    Initialize database connection and verify it works
    
    Returns:
        True if connection successful, False otherwise
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        connection.close()
        print("Database connection successful!")
        return True
    except Exception as e:
        print(f"Database initialization failed: {e}")
        return False


def close_db_connection(connection):
    """
    Safely close database connection
    
    Args:
        connection: Database connection to close
    """
    if connection:
        try:
            connection.close()
        except:
            pass

