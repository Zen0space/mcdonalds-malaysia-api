"""
Database initialization script
"""
import logging
from .connection import get_db_client
from .schema import get_schema_queries

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_database():
    """Initialize database with schema"""
    try:
        client = get_db_client()
        
        # Execute schema queries
        schema_queries = get_schema_queries()
        
        for query in schema_queries:
            logger.info(f"Executing: {query[:50]}...")
            client.execute(query)
        
        logger.info("Database initialization completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        return False

def check_database_connection():
    """Check if database connection is working"""
    try:
        client = get_db_client()
        result = client.execute("SELECT 1 as test")
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Checking database connection...")
    if check_database_connection():
        print("✓ Database connection successful")
        
        print("Initializing database schema...")
        if initialize_database():
            print("✓ Database initialization completed")
        else:
            print("✗ Database initialization failed")
    else:
        print("✗ Database connection failed") 