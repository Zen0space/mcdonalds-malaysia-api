"""
Database connection module for Turso database
"""
import os
from typing import Optional
from pathlib import Path
from libsql_client import ClientSync, create_client_sync
from dotenv import load_dotenv

# Load environment variables from project root
project_root = Path(__file__).parent.parent.parent.parent
load_dotenv(dotenv_path=project_root / ".env")

class DatabaseConnection:
    """Handle database connection to Turso"""
    
    def __init__(self):
        self.url = os.getenv("TURSO_DATABASE_URL")
        self.auth_token = os.getenv("TURSO_AUTH_TOKEN")
        self.client: Optional[ClientSync] = None
        
        if not self.url or not self.auth_token:
            raise ValueError(
                "Database URL and auth token must be provided via environment variables.\n"
                "Please ensure TURSO_DATABASE_URL and TURSO_AUTH_TOKEN are set in your .env file.\n"
                "See env.example for the required format."
            )
    
    def connect(self) -> ClientSync:
        """Create and return database client"""
        if self.client is None:
            self.client = create_client_sync(
                url=self.url,
                auth_token=self.auth_token
            )
        return self.client
    
    def disconnect(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            self.client = None
    
    def __enter__(self):
        """Context manager entry"""
        return self.connect()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()

# Global database instance
db_connection = DatabaseConnection()

def get_db_client() -> ClientSync:
    """Get database client instance"""
    return db_connection.connect() 