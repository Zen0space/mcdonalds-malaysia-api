"""
Database dependencies for McDonald's Malaysia API.
Uses dependency injection pattern with the existing database connection.
"""

import sys
import os
from typing import Generator
from fastapi import Depends
from libsql_client import ClientSync

# Add backend to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.database.connection import get_db_client


def get_database() -> Generator[ClientSync, None, None]:
    """
    Database dependency for FastAPI endpoints.
    
    Yields:
        ClientSync: Database client instance
    """
    try:
        client = get_db_client()
        yield client
    except Exception as e:
        raise RuntimeError(f"Database connection failed: {e}")


# Dependency for FastAPI routes
DatabaseDep = Depends(get_database) 