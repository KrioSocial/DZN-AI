#!/usr/bin/env python3
"""
Database initialization script for AI Studio
Creates SQLite database and tables from schema
"""

import sqlite3
import os
from pathlib import Path

def init_database():
    """Initialize the SQLite database with schema"""
    
    # Get the database path
    db_path = 'ai_studio.db'
    
    print(f"Creating database at: {db_path}")
    
    # Read the SQLite schema
    schema_path = Path(__file__).parent.parent / 'database' / 'schema_sqlite.sql'
    
    if not schema_path.exists():
        print(f"Schema file not found: {schema_path}")
        return False
    
    try:
        # Create database connection
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Read and execute schema
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        # Execute schema (SQLite can handle multiple statements)
        cursor.executescript(schema_sql)
        
        # Commit changes
        conn.commit()
        
        print("✓ Database created successfully!")
        print("✓ Tables created successfully!")
        
        # Verify tables were created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"✓ Created {len(tables)} tables: {[table[0] for table in tables]}")
        
        # Check if admin user was created
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
        admin_count = cursor.fetchone()[0]
        print(f"✓ Admin users: {admin_count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Initializing AI Studio Database...")
    success = init_database()
    
    if success:
        print("\n✅ Database initialization complete!")
        print("You can now start the Flask server.")
    else:
        print("\n❌ Database initialization failed!")
        exit(1)
