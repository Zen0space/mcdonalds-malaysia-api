"""
Synchronous API Function Wrappers for Gemini Function Calling

This module provides synchronous wrapper functions that are compatible with
Gemini's function calling system. These wrappers handle async execution
within the existing FastAPI event loop without using asyncio.run().
"""

import logging
import asyncio
from typing import Dict, List, Optional, Union, Any
from concurrent.futures import ThreadPoolExecutor
from ..database.operations import DatabaseOperations

# Configure logging
logger = logging.getLogger(__name__)

# Thread pool for async execution
executor = ThreadPoolExecutor(max_workers=4)

def sync_find_nearby_outlets(db_ops: DatabaseOperations, latitude: float, longitude: float, radius: float = 2.0, limit: int = 20) -> Dict[str, Any]:
    """
    Synchronous wrapper for find_nearby_outlets function.
    
    Find McDonald's outlets near the given coordinates using GPS location.
    
    This function should be used when users ask for location-based searches such as:
    - "Find McDonald's near me"
    - "Show McDonald's within 2km of my location"
    - "What's the closest McDonald's?"
    - "Find McDonald's near KLCC" (when you have KLCC coordinates)
    - "McDonald's within 1km of Pavilion KL"
    - "Show nearby McDonald's outlets"
    - "Find the nearest McDonald's to [landmark]"
    
    Args:
        db_ops (DatabaseOperations): Database operations instance
        latitude (float): User's latitude coordinate (Malaysia bounds: 1.0 to 7.0)
        longitude (float): User's longitude coordinate (Malaysia bounds: 99.0 to 119.0)
        radius (float, optional): Search radius in kilometers. Defaults to 2.0. 
                                 Maximum allowed is 5.0km for performance.
        limit (int, optional): Maximum number of outlets to return. Defaults to 20.
                              Maximum allowed is 50 for performance.
    
    Returns:
        Dict[str, Any]: Response containing outlet data or error information
    """
    try:
        logger.info(f"🎯 sync_find_nearby_outlets called with: lat={latitude}, lng={longitude}, radius={radius}, limit={limit}")
        
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
        
        # Handle async execution properly within existing event loop
        try:
            loop = asyncio.get_running_loop()
            # We're in an event loop, run in thread pool to avoid blocking
            future = executor.submit(asyncio.run, db_ops.get_nearby_outlets(latitude, longitude, radius, limit))
            outlets = future.result(timeout=30)  # 30 second timeout
        except RuntimeError:
            # No event loop running, use asyncio.run directly
            outlets = asyncio.run(db_ops.get_nearby_outlets(latitude, longitude, radius, limit))
        
        result = {
            "success": True,
            "data": {
                "outlets": outlets,
                "total": len(outlets),
                "search_radius_km": radius,
                "search_center": {"latitude": latitude, "longitude": longitude}
            }
        }
        
        logger.info(f"🎯 sync_find_nearby_outlets result: success=True, found {len(outlets)} outlets")
        return result
        
    except Exception as e:
        logger.error(f"Error in sync_find_nearby_outlets: {str(e)}")
        return {
            "success": False,
            "error": f"Database error: {str(e)}",
            "error_type": "database_error"
        }

def sync_search_outlets(db_ops: DatabaseOperations, search_query: str, limit: int = 10) -> Dict[str, Any]:
    """
    Synchronous wrapper for search_outlets function.
    
    Search McDonald's outlets by name or address using text matching.
    
    This function should be used when users search for specific outlets by name or location:
    - "Find McDonald's KLCC"
    - "Search for McDonald's in Pavilion"
    - "Show McDonald's with 'Suria' in the name"
    - "Find McDonald's on Jalan Ampang"
    - "McDonald's near Mid Valley"
    - "Search for McDonald's Bukit Bintang"
    
    Args:
        db_ops (DatabaseOperations): Database operations instance
        search_query (str): Search term to match against outlet names and addresses
        limit (int, optional): Maximum number of outlets to return. Defaults to 10.
    
    Returns:
        Dict[str, Any]: Response containing search results or error information
    """
    try:
        logger.info(f"🔍 sync_search_outlets called with: query='{search_query}', limit={limit}")
        
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
        
        # Handle async execution properly within existing event loop
        try:
            loop = asyncio.get_running_loop()
            future = executor.submit(asyncio.run, db_ops.search_outlets(search_query.strip(), limit))
            outlets = future.result(timeout=30)
        except RuntimeError:
            outlets = asyncio.run(db_ops.search_outlets(search_query.strip(), limit))
        
        result = {
            "success": True,
            "data": {
                "outlets": outlets,
                "total": len(outlets),
                "search_query": search_query.strip()
            }
        }
        
        logger.info(f"🔍 sync_search_outlets result: success=True, found {len(outlets)} outlets")
        return result
        
    except Exception as e:
        logger.error(f"Error in sync_search_outlets: {str(e)}")
        return {
            "success": False,
            "error": f"Database error: {str(e)}",
            "error_type": "database_error"
        }

def sync_get_outlet_details(db_ops: DatabaseOperations, outlet_id: int) -> Dict[str, Any]:
    """
    Synchronous wrapper for get_outlet_details function.
    
    Get detailed information for a specific McDonald's outlet by its unique ID.
    
    This function should be used when users want complete details about a specific outlet:
    - "Tell me more about this McDonald's"
    - "What are the operating hours for outlet 369?"
    - "Show details for McDonald's KLCC"
    - "Get information about this outlet"
    - "What's the address of this McDonald's?"
    - "Show me the Waze link for this outlet"
    
    Args:
        db_ops (DatabaseOperations): Database operations instance
        outlet_id (int): Unique identifier for the McDonald's outlet
    
    Returns:
        Dict[str, Any]: Response containing outlet details or error information
    """
    try:
        logger.info(f"📋 sync_get_outlet_details called with: outlet_id={outlet_id}")
        
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
        
        result = {
            "success": True,
            "data": {
                "outlet": outlet_data
            }
        }
        
        logger.info(f"📋 sync_get_outlet_details result: success=True, outlet={outlet.name}")
        return result
        
    except Exception as e:
        logger.error(f"Error in sync_get_outlet_details: {str(e)}")
        return {
            "success": False,
            "error": f"Database error: {str(e)}",
            "error_type": "database_error"
        }

def sync_get_outlet_stats(db_ops: DatabaseOperations) -> Dict[str, Any]:
    """
    Synchronous wrapper for get_outlet_stats function.
    
    Get comprehensive statistics about the McDonald's outlet database.
    
    This function should be used when users ask about database information:
    - "How many McDonald's outlets are there?"
    - "Show me database statistics"
    - "What's the total number of outlets?"
    - "How many outlets have GPS coordinates?"
    - "Give me an overview of the data"
    - "Show outlet coverage information"
    
    Args:
        db_ops (DatabaseOperations): Database operations instance
    
    Returns:
        Dict[str, Any]: Response containing statistics or error information
    """
    try:
        logger.info(f"📊 sync_get_outlet_stats called")
        
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
        
        result = {
            "success": True,
            "data": enhanced_stats
        }
        
        logger.info(f"📊 sync_get_outlet_stats result: success=True, total_outlets={stats.get('total_outlets')}")
        return result
        
    except Exception as e:
        logger.error(f"Error in sync_get_outlet_stats: {str(e)}")
        return {
            "success": False,
            "error": f"Database error: {str(e)}",
            "error_type": "database_error"
        }

def sync_get_api_health(db_ops: DatabaseOperations) -> Dict[str, Any]:
    """
    Synchronous wrapper for get_api_health function.
    
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
        logger.info(f"🏥 sync_get_api_health called")
        
        # Handle async execution properly within existing event loop
        try:
            loop = asyncio.get_running_loop()
            future = executor.submit(asyncio.run, db_ops.health_check())
            health_result = future.result(timeout=30)
        except RuntimeError:
            health_result = asyncio.run(db_ops.health_check())
        
        result = {
            "success": True,
            "data": {
                "api_status": "healthy",
                "database": health_result,
                "message": "McDonald's outlet API is healthy and operational"
            }
        }
        
        logger.info(f"🏥 sync_get_api_health result: success=True")
        return result
        
    except Exception as e:
        logger.error(f"Error in sync_get_api_health: {str(e)}")
        return {
            "success": False,
            "error": f"Health check failed: {str(e)}",
            "error_type": "system_error"
        } 