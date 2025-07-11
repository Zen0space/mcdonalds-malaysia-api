"""
McDonald's Outlet API Functions for Gemini Function Calling

This module provides intelligent API function wrappers that enable Gemini 2.5 Flash
to directly call our McDonald's outlet database operations for fast responses.

Each function is designed with comprehensive docstrings and type hints to help
Gemini understand when and how to use them for different query patterns.
"""

import logging
import math
from typing import Dict, List, Optional, Union, Any
from ..database.operations import DatabaseOperations

# Configure logging
logger = logging.getLogger(__name__)

async def find_nearby_outlets(db_ops: DatabaseOperations, latitude: float, longitude: float, radius: float = 2.0, limit: int = 20) -> Dict[str, Any]:
    """
    Find McDonald's outlets near the given coordinates using GPS location.
    
    This function should be used when users ask for location-based searches such as:
    - "Find McDonald's near me"
    - "Show McDonald's within 2km of my location"
    - "What's the closest McDonald's?"
    - "Find McDonald's near KLCC" (when you have KLCC coordinates)
    - "McDonald's within 1km of Pavilion KL"
    - "Show nearby McDonald's outlets"
    - "Find the nearest McDonald's to [landmark]"
    
    The function uses GPS coordinates to calculate distances and returns outlets
    sorted by proximity (closest first).
    
    Args:
        db_ops (DatabaseOperations): Database operations instance
        latitude (float): User's latitude coordinate (Malaysia bounds: 1.0 to 7.0)
        longitude (float): User's longitude coordinate (Malaysia bounds: 99.0 to 119.0)
        radius (float, optional): Search radius in kilometers. Defaults to 2.0. 
                                 Maximum allowed is 5.0km for performance.
        limit (int, optional): Maximum number of outlets to return. Defaults to 20.
                              Maximum allowed is 50 for performance.
    
    Returns:
        Dict[str, Any]: Response containing:
            - success (bool): Whether the request was successful
            - data (dict): Response with outlets list, each containing:
                - id, name, address, operating_hours, waze_link
                - latitude, longitude, distance_km
            - error (str): Error message if unsuccessful
    
    Example usage patterns:
        - User: "Find McDonald's near me" → Use with user's current coordinates
        - User: "McDonald's within 1km" → Use with radius=1.0
        - User: "Show 5 closest McDonald's" → Use with limit=5
        - User: "Find McDonald's near KLCC" → Use with KLCC coordinates (3.1570, 101.7123)
    """
    try:
        # Validate coordinates
        if not (1.0 <= latitude <= 7.0 and 99.0 <= longitude <= 119.0):
            return {
                "success": False,
                "error": "Invalid coordinates. Please provide coordinates within Malaysia (latitude: 1.0-7.0, longitude: 99.0-119.0)",
                "error_type": "validation_error"
            }
        
        # Validate radius
        if radius <= 0 or radius > 5.0:
            return {
                "success": False,
                "error": "Radius must be between 0.1 and 5.0 kilometers",
                "error_type": "validation_error"
            }
        
        # Validate limit
        if limit <= 0 or limit > 50:
            return {
                "success": False,
                "error": "Limit must be between 1 and 50 outlets",
                "error_type": "validation_error"
            }
        
        # Use direct database operation
        outlets = await db_ops.get_nearby_outlets(latitude, longitude, radius, limit)
        
        return {
            "success": True,
            "data": {
                "outlets": outlets,
                "total": len(outlets),
                "search_radius_km": radius,
                "search_center": {"latitude": latitude, "longitude": longitude}
            }
        }
        
    except Exception as e:
        logger.error(f"Error finding nearby outlets: {str(e)}")
        return {
            "success": False,
            "error": f"Database error: {str(e)}",
            "error_type": "database_error"
        }

async def search_outlets(db_ops: DatabaseOperations, search_query: str, limit: int = 10) -> Dict[str, Any]:
    """
    Search McDonald's outlets by name or address using text matching.
    
    This function should be used when users search for specific outlets by name or location:
    - "Find McDonald's KLCC"
    - "Search for McDonald's in Pavilion"
    - "Show McDonald's with 'Suria' in the name"
    - "Find McDonald's on Jalan Ampang"
    - "McDonald's near Mid Valley"
    - "Search for McDonald's Bukit Bintang"
    
    The function performs case-insensitive text matching on outlet names and addresses.
    
    Args:
        db_ops (DatabaseOperations): Database operations instance
        search_query (str): Search term to match against outlet names and addresses
        limit (int, optional): Maximum number of outlets to return. Defaults to 10.
                              Maximum allowed is 50 for performance.
    
    Returns:
        Dict[str, Any]: Response containing:
            - success (bool): Whether the request was successful
            - data (dict): Response with outlets list matching the search query
            - error (str): Error message if unsuccessful
    
    Example usage patterns:
        - User: "Find McDonald's KLCC" → Use with search_query="KLCC"
        - User: "McDonald's in Pavilion" → Use with search_query="Pavilion"
        - User: "Show McDonald's Bukit Bintang" → Use with search_query="Bukit Bintang"
    """
    try:
        # Validate search query
        if not search_query or len(search_query.strip()) < 1:
            return {
                "success": False,
                "error": "Search query cannot be empty",
                "error_type": "validation_error"
            }
        
        # Validate limit
        if limit <= 0 or limit > 50:
            return {
                "success": False,
                "error": "Limit must be between 1 and 50 outlets",
                "error_type": "validation_error"
            }
        
        # Use direct database operation
        outlets = await db_ops.search_outlets(search_query.strip(), limit)
        
        return {
            "success": True,
            "data": {
                "outlets": outlets,
                "total": len(outlets),
                "search_query": search_query.strip()
            }
        }
        
    except Exception as e:
        logger.error(f"Error searching outlets: {str(e)}")
        return {
            "success": False,
            "error": f"Database error: {str(e)}",
            "error_type": "database_error"
        }

async def get_outlet_details(db_ops: DatabaseOperations, outlet_id: int) -> Dict[str, Any]:
    """
    Get detailed information for a specific McDonald's outlet by its unique ID.
    
    This function should be used when users want complete details about a specific outlet:
    - "Tell me more about this McDonald's"
    - "What are the operating hours for outlet 369?"
    - "Show details for McDonald's KLCC"
    - "Get information about this outlet"
    - "What's the address of this McDonald's?"
    - "Show me the Waze link for this outlet"
    
    The function returns comprehensive outlet information including location, hours, and navigation.
    
    Args:
        db_ops (DatabaseOperations): Database operations instance
        outlet_id (int): Unique identifier for the McDonald's outlet
    
    Returns:
        Dict[str, Any]: Response containing:
            - success (bool): Whether the request was successful
            - data (dict): Complete outlet information including:
                - id, name, address, operating_hours
                - latitude, longitude, waze_link
                - created_at, updated_at timestamps
            - error (str): Error message if unsuccessful
    
    Example usage patterns:
        - User: "Tell me about outlet 369" → Use with outlet_id=369
        - User: "Show details for this McDonald's" → Use with specific outlet_id
        - User: "What time does this outlet open?" → Use to get operating_hours
    """
    try:
        # Validate outlet ID
        if not isinstance(outlet_id, int) or outlet_id <= 0:
            return {
                "success": False,
                "error": "Outlet ID must be a positive integer",
                "error_type": "validation_error"
            }
        
        # Get outlet from database using OutletDatabase (sync method)
        from ..database.operations import outlet_db
        outlet = outlet_db.get_outlet_by_id(outlet_id)
        
        if not outlet:
            return {
                "success": False,
                "error": f"Outlet with ID {outlet_id} not found",
                "error_type": "not_found"
            }
        
        # Convert outlet to dictionary
        outlet_data = {
            "id": outlet.id,
            "name": outlet.name,
            "address": outlet.address,
            "operating_hours": outlet.operating_hours,
            "waze_link": outlet.waze_link,
            "latitude": outlet.latitude,
            "longitude": outlet.longitude,
            "created_at": outlet.created_at.isoformat() if outlet.created_at else None,
            "updated_at": outlet.updated_at.isoformat() if outlet.updated_at else None
        }
        
        return {
            "success": True,
            "data": {
                "outlet": outlet_data
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting outlet details: {str(e)}")
        return {
            "success": False,
            "error": f"Database error: {str(e)}",
            "error_type": "database_error"
        }

async def get_outlet_stats(db_ops: DatabaseOperations) -> Dict[str, Any]:
    """
    Get comprehensive statistics about the McDonald's outlet database.
    
    This function should be used when users ask about database information:
    - "How many McDonald's outlets are there?"
    - "Show me database statistics"
    - "What's the total number of outlets?"
    - "How many outlets have GPS coordinates?"
    - "Give me an overview of the data"
    - "Show outlet coverage information"
    
    The function returns detailed statistics about outlet counts, coverage, and data quality.
    
    Args:
        db_ops (DatabaseOperations): Database operations instance
    
    Returns:
        Dict[str, Any]: Response containing:
            - success (bool): Whether the request was successful
            - data (dict): Statistics including:
                - total_outlets: Total number of outlets in database
                - outlets_with_coordinates: Number with GPS coordinates
                - outlets_without_coordinates: Number missing coordinates
                - latest_outlet: Information about most recently added outlet
                - coverage: Geographic coverage information
            - error (str): Error message if unsuccessful
    
    Example usage patterns:
        - User: "How many McDonald's are there?" → Use to get total_outlets
        - User: "Show me database stats" → Use to get comprehensive overview
        - User: "What's the data coverage?" → Use to get coordinate statistics
    """
    try:
        # Get database statistics using OutletDatabase (sync method)
        from ..database.operations import outlet_db
        stats = outlet_db.get_database_stats()
        
        if not stats:
            return {
                "success": False,
                "error": "Unable to retrieve database statistics",
                "error_type": "database_error"
            }
        
        # Add additional metadata
        enhanced_stats = {
            **stats,
            "coverage": "Kuala Lumpur, Malaysia",
            "data_quality": {
                "coordinate_coverage_percent": round((stats.get('outlets_with_coordinates', 0) / max(stats.get('total_outlets', 1), 1)) * 100, 1),
                "has_operating_hours": "Available for most outlets",
                "has_waze_links": "Available for navigation"
            }
        }
        
        return {
            "success": True,
            "data": enhanced_stats
        }
        
    except Exception as e:
        logger.error(f"Error getting outlet stats: {str(e)}")
        return {
            "success": False,
            "error": f"Database error: {str(e)}",
            "error_type": "database_error"
        }

async def get_api_health(db_ops: DatabaseOperations) -> Dict[str, Any]:
    """
    Check the health status of the McDonald's outlet API and database.
    
    This function should be used for system monitoring and health checks:
    - "Is the API working?"
    - "Check database connectivity"
    - "Show system health status"
    - "Is everything running properly?"
    
    Args:
        db_ops (DatabaseOperations): Database operations instance
    
    Returns:
        Dict[str, Any]: Health check response
    """
    try:
        health_result = await db_ops.health_check()
        
        return {
            "success": True,
            "data": {
                "api_status": "healthy",
                "database": health_result,
                "message": "McDonald's outlet API is healthy and operational"
            }
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "success": False,
            "error": f"Health check failed: {str(e)}",
            "error_type": "system_error"
        } 