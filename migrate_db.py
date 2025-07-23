#!/usr/bin/env python3
"""
Database migration script to add missing features column
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database.connection import get_db_client

def migrate_database():
    """Add features column to existing database"""
    try:
        client = get_db_client()
        
        # Check if features column exists
        try:
            result = client.execute("SELECT features FROM outlets LIMIT 1")
            print("✅ Features column already exists")
            return True
        except Exception:
            print("📦 Features column missing, adding it...")
        
        # Add features column
        client.execute("ALTER TABLE outlets ADD COLUMN features TEXT")
        print("✅ Added features column to outlets table")
        
        # Update existing records with empty features array
        client.execute("UPDATE outlets SET features = '[]' WHERE features IS NULL")
        print("✅ Updated existing records with empty features")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Running database migration...")
    if migrate_database():
        print("✅ Migration completed successfully")
    else:
        print("❌ Migration failed")
        sys.exit(1) 