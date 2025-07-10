"""
FastAPI routes for McDonald's Malaysia API.
Clean implementation with dependency injection and proper database connection.
"""

import json
from datetime import datetime
from typing import Optional, List
from libsql_client import ClientSync

from fastapi import APIRouter, HTTPException, Query, Path, Depends
from fastapi.responses import JSONResponse

from .models import (
    OutletBase, OutletResponse, OutletListResponse, NearbyOutletResponse, NearbySearchResponse,
    StatsResponse, HealthResponse, APIInfoResponse, ErrorResponse
)
from .dependencies import DatabaseDep

# Create router with version prefix
router = APIRouter(prefix="/api/v1", tags=["outlets"])


@router.get(
    "/",
    response_model=APIInfoResponse,
    summary="🍟 API Information",
    description="""
    Get comprehensive information about the McDonald's Malaysia API.
    
    Returns API metadata, total outlets available, and coverage information.
    Perfect for checking API status and discovering available endpoints.
    """,
    response_description="API information including name, version, description, and outlet count"
)
async def get_api_info(db: ClientSync = DatabaseDep):
    """Get API information and status."""
    try:
        # Get database stats for total outlets
        result = db.execute("SELECT COUNT(*) FROM outlets")
        total_outlets = result.rows[0][0] if result.rows else 0
        
        return APIInfoResponse(
            name="McDonald's Malaysia API",
            version="1.0.0",
            description="RESTful API providing McDonald's outlet locations, coordinates, and details for Kuala Lumpur",
            docs_url="/docs",
            total_outlets=total_outlets,
            coverage="Kuala Lumpur, Malaysia"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get API info: {str(e)}")


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="💚 Health Check",
    description="""
    Check the health status of the API and database connection.
    
    Returns:
    - API status (healthy/unhealthy)
    - Database connectivity status
    - Total number of outlets in database
    - Current timestamp
    
    Use this endpoint for monitoring and health checks.
    """,
    response_description="Health status with database connectivity and outlet count"
)
async def health_check(db: ClientSync = DatabaseDep):
    """Check API and database health."""
    try:
        result = db.execute("SELECT COUNT(*) FROM outlets")
        total_outlets = result.rows[0][0] if result.rows else 0
        
        return HealthResponse(
            status="healthy",
            database_connected=True,
            total_outlets=total_outlets,
            timestamp=datetime.now()
        )
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            database_connected=False,
            total_outlets=0,
            timestamp=datetime.now()
        )


@router.get(
    "/outlets",
    response_model=OutletListResponse,
    summary="🏪 List Outlets",
    description="""
    Get a paginated list of McDonald's outlets with advanced search and filtering capabilities.
    
    **Features:**
    - 📄 Pagination support (limit & offset)
    - 🔍 Text search across outlet names and addresses
    - 🏷️ Feature filtering (24hrs, Drive-Thru, McCafe)
    - 📊 Sorting options (name, id)
    
    **Examples:**
    - `/outlets?limit=10` - Get first 10 outlets
    - `/outlets?search=KLCC` - Search for outlets containing "KLCC"
    - `/outlets?features=24hrs,Drive-Thru` - Filter by features
    - `/outlets?sort=name&limit=5&offset=10` - Sorted with pagination
    """,
    response_description="Paginated list of outlets with metadata (total, has_more, etc.)"
)
async def get_outlets(
    db: ClientSync = DatabaseDep,
    limit: int = Query(50, ge=1, le=100, description="Number of outlets per page (1-100)"),
    offset: int = Query(0, ge=0, description="Number of outlets to skip"),
    search: Optional[str] = Query(None, description="Search term for outlet name or address"),
    sort: Optional[str] = Query("name", description="Sort by: name, id"),
    features: Optional[str] = Query(None, description="Filter by features (comma-separated): 24hrs,Drive-Thru,McCafe")
):
    """Get outlets with pagination, search, and filtering."""
    try:
        # Build query with optional search and filters
        base_query = "FROM outlets"
        where_conditions = []
        params = []
        
        # Add search condition
        if search:
            where_conditions.append("(name LIKE ? OR address LIKE ?)")
            search_term = f"%{search}%"
            params.extend([search_term, search_term])
        
        # Add features filter
        if features:
            feature_list = [f.strip() for f in features.split(",")]
            for feature in feature_list:
                where_conditions.append("features LIKE ?")
                params.append(f"%{feature}%")
        
        # Build WHERE clause
        where_clause = ""
        if where_conditions:
            where_clause = f" WHERE {' AND '.join(where_conditions)}"
        
        # Validate sort parameter
        valid_sorts = {"name": "name", "id": "id"}
        sort_column = valid_sorts.get(sort, "name")
        
        # Get total count
        count_result = db.execute(f"SELECT COUNT(*) {base_query}{where_clause}", params)
        total_count = count_result.rows[0][0] if count_result.rows else 0
        
        # Get outlets with pagination
        outlets_query = f"""
            SELECT id, name, address, operating_hours, waze_link, 
                   latitude, longitude, features, created_at, updated_at 
            {base_query}{where_clause}
            ORDER BY {sort_column} 
            LIMIT ? OFFSET ?
        """
        outlets_params = params + [limit, offset]
        outlets_result = db.execute(outlets_query, outlets_params)
        
        # Convert to response models
        outlets = []
        for row in outlets_result.rows:
            outlet = OutletResponse(
                id=row[0],
                name=row[1],
                address=row[2],
                operating_hours=row[3],
                waze_link=row[4],
                latitude=float(row[5]) if row[5] is not None else None,
                longitude=float(row[6]) if row[6] is not None else None,
                features=json.loads(row[7]) if row[7] else [],
                created_at=datetime.fromisoformat(row[8]) if row[8] else datetime.now(),
                updated_at=datetime.fromisoformat(row[9]) if row[9] else datetime.now()
            )
            outlets.append(outlet)
        
        return OutletListResponse(
            outlets=outlets,
            total=total_count,
            limit=limit,
            offset=offset,
            has_more=(offset + limit) < total_count
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get outlets: {str(e)}")


@router.get(
    "/outlets/{outlet_id}",
    response_model=OutletResponse,
    summary="🏪 Get Outlet by ID",
    description="""
    Get complete details for a specific McDonald's outlet by its unique ID.
    
    **Returns:**
    - Full outlet information (name, address, hours)
    - GPS coordinates (latitude, longitude)
    - Waze navigation link
    - Outlet features (24hrs, Drive-Thru, McCafe)
    - Creation and update timestamps
    
    **Example:** `/outlets/345` - Get details for outlet with ID 345
    """,
    response_description="Complete outlet information with all available fields",
    responses={
        404: {"description": "Outlet not found", "content": {"application/json": {"example": {"detail": "Outlet with ID 999 not found"}}}}
    }
)
async def get_outlet_by_id(
    outlet_id: int = Path(..., ge=1, description="Outlet ID"),
    db: ClientSync = DatabaseDep
):
    """Get a specific outlet by ID."""
    try:
        result = db.execute(
            """SELECT id, name, address, operating_hours, waze_link, 
                      latitude, longitude, features, created_at, updated_at 
               FROM outlets WHERE id = ?""",
            [outlet_id]
        )
        
        if not result.rows:
            raise HTTPException(status_code=404, detail=f"Outlet with ID {outlet_id} not found")
        
        row = result.rows[0]
        return OutletResponse(
            id=row[0],
            name=row[1],
            address=row[2],
            operating_hours=row[3],
            waze_link=row[4],
            latitude=float(row[5]) if row[5] is not None else None,
            longitude=float(row[6]) if row[6] is not None else None,
            features=json.loads(row[7]) if row[7] else [],
            created_at=datetime.fromisoformat(row[8]) if row[8] else datetime.now(),
            updated_at=datetime.fromisoformat(row[9]) if row[9] else datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get outlet: {str(e)}")


@router.get(
    "/outlets/nearby",
    response_model=NearbySearchResponse,
    summary="📍 Find Nearby Outlets",
    description="""
    Find McDonald's outlets within a specified radius of given GPS coordinates.
    
    **Features:**
    - 🌍 Uses Haversine formula for accurate distance calculation
    - 📏 Distance included in response (kilometers)
    - 📊 Results sorted by distance (closest first)
    - 🎯 Configurable search radius (0.1km - 5km)
    - 🔢 Configurable result limit (1-50 outlets)
    
    **Examples:**
    - `/outlets/nearby?latitude=3.1570&longitude=101.7123&radius=2` - Find outlets within 2km of KLCC
    - `/outlets/nearby?latitude=3.1481&longitude=101.7109&radius=1&limit=5` - Find 5 closest outlets within 1km
    
    **Note:** Only outlets with valid GPS coordinates are included in results.
    """,
    response_description="List of nearby outlets with distances, sorted by proximity"
)
async def find_nearby_outlets(
    latitude: float = Query(..., ge=1.0, le=7.0, description="Latitude (Malaysia bounds: 1.0 to 7.0)"),
    longitude: float = Query(..., ge=99.0, le=119.0, description="Longitude (Malaysia bounds: 99.0 to 119.0)"),
    radius: float = Query(2.0, ge=0.1, le=5.0, description="Search radius in kilometers (max 5km)"),
    limit: int = Query(20, ge=1, le=50, description="Maximum number of outlets to return"),
    db: ClientSync = DatabaseDep
):
    """Find outlets within specified radius using Haversine formula."""
    try:
        # Query all outlets with coordinates
        result = db.execute("""
            SELECT id, name, address, operating_hours, waze_link, 
                   latitude, longitude, features, created_at, updated_at 
            FROM outlets 
            WHERE latitude IS NOT NULL AND longitude IS NOT NULL
        """)
        
        nearby_outlets = []
        
        # Calculate distance for each outlet using Haversine formula
        for row in result.rows:
            outlet_lat = float(row[5])
            outlet_lng = float(row[6])
            
            # Haversine formula for distance calculation
            import math
            R = 6371  # Earth's radius in kilometers
            
            lat1, lon1 = math.radians(latitude), math.radians(longitude)
            lat2, lon2 = math.radians(outlet_lat), math.radians(outlet_lng)
            
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            c = 2 * math.asin(math.sqrt(a))
            distance = R * c
            
            # Only include outlets within radius
            if distance <= radius:
                outlet = NearbyOutletResponse(
                    id=row[0],
                    name=row[1],
                    address=row[2],
                    operating_hours=row[3],
                    waze_link=row[4],
                    latitude=outlet_lat,
                    longitude=outlet_lng,
                    features=json.loads(row[7]) if row[7] else [],
                    created_at=datetime.fromisoformat(row[8]) if row[8] else datetime.now(),
                    updated_at=datetime.fromisoformat(row[9]) if row[9] else datetime.now(),
                    distance_km=round(distance, 2)
                )
                nearby_outlets.append(outlet)
        
        # Sort by distance and apply limit
        nearby_outlets.sort(key=lambda x: x.distance_km)
        nearby_outlets = nearby_outlets[:limit]
        
        return NearbySearchResponse(
            outlets=nearby_outlets,
            center={"latitude": latitude, "longitude": longitude},
            radius_km=radius,
            total_found=len(nearby_outlets)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to find nearby outlets: {str(e)}")


@router.get(
    "/stats",
    response_model=StatsResponse,
    summary="📊 Database Statistics",
    description="""
    Get comprehensive statistics about the McDonald's outlet database.
    
    **Returns:**
    - 📈 Total number of outlets in database
    - 🗺️ Number of outlets with GPS coordinates
    - 🧭 Number of outlets with Waze navigation links
    - 📅 Last database update timestamp
    - 🌍 Coverage areas (currently Kuala Lumpur)
    
    **Use cases:**
    - Monitor data quality and completeness
    - Check when database was last updated
    - Verify geographic coverage
    - API health monitoring
    """,
    response_description="Database statistics including counts, coverage, and last update time"
)
async def get_stats(db: ClientSync = DatabaseDep):
    """Get database statistics."""
    try:
        # Total outlets
        total_result = db.execute("SELECT COUNT(*) FROM outlets")
        total_outlets = total_result.rows[0][0] if total_result.rows else 0
        
        # Outlets with coordinates
        coords_result = db.execute(
            "SELECT COUNT(*) FROM outlets WHERE latitude IS NOT NULL AND longitude IS NOT NULL"
        )
        outlets_with_coordinates = coords_result.rows[0][0] if coords_result.rows else 0
        
        # Outlets with Waze links
        waze_result = db.execute(
            "SELECT COUNT(*) FROM outlets WHERE waze_link IS NOT NULL AND waze_link != ''"
        )
        outlets_with_waze_links = waze_result.rows[0][0] if waze_result.rows else 0
        
        # Last updated (most recent updated_at)
        last_updated_result = db.execute("SELECT MAX(updated_at) FROM outlets")
        last_updated = None
        if last_updated_result.rows and last_updated_result.rows[0][0]:
            last_updated = datetime.fromisoformat(last_updated_result.rows[0][0])
        
        return StatsResponse(
            total_outlets=total_outlets,
            outlets_with_coordinates=outlets_with_coordinates,
            outlets_with_waze_links=outlets_with_waze_links,
            last_updated=last_updated,
            coverage_areas=["Kuala Lumpur"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}") 