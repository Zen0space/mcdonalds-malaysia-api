"""
Database operations for McDonald's outlets
"""
import logging
from typing import List, Optional, Dict, Any
from .connection import get_db_client
from .models import Outlet, validate_outlet_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseOperations:
    """
    Async database operations for chat service and API endpoints.
    
    This class provides async methods for database operations
    needed by the chat service and other components.
    """
    
    def __init__(self):
        self.client = get_db_client()
    
    async def get_nearby_outlets(self, latitude: float, longitude: float, 
                                radius_km: float = 2.0, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get nearby outlets within radius using Haversine formula.
        
        Args:
            latitude: User latitude
            longitude: User longitude
            radius_km: Search radius in kilometers
            limit: Maximum number of results
            
        Returns:
            List of outlet dictionaries with distance
        """
        try:
            # Haversine formula for distance calculation
            # Note: SQLite doesn't support HAVING with calculated columns, so we use a subquery
            query = """
            SELECT id, name, address, operating_hours, waze_link, latitude, longitude, distance
            FROM (
                SELECT id, name, address, operating_hours, waze_link, latitude, longitude,
                       (6371 * acos(cos(radians(?)) * cos(radians(latitude)) * 
                       cos(radians(longitude) - radians(?)) + sin(radians(?)) * 
                       sin(radians(latitude)))) AS distance
                FROM outlets 
                WHERE latitude IS NOT NULL AND longitude IS NOT NULL
            ) AS outlets_with_distance
            WHERE distance <= ?
            ORDER BY distance
            LIMIT ?
            """
            
            result = self.client.execute(query, (latitude, longitude, latitude, radius_km, limit))
            
            outlets = []
            for row in result.rows:
                outlet = {
                    'id': row[0],
                    'name': row[1],
                    'address': row[2],
                    'operating_hours': row[3],
                    'waze_link': row[4],
                    'latitude': row[5],
                    'longitude': row[6],
                    'distance_km': f"{row[7]:.2f}"
                }
                outlets.append(outlet)
            
            logger.info(f"Found {len(outlets)} nearby outlets within {radius_km}km")
            return outlets
            
        except Exception as e:
            logger.error(f"Failed to get nearby outlets: {str(e)}")
            return []
    
    async def search_outlets(self, search_query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search outlets by name or address.
        
        Args:
            search_query: Search term
            limit: Maximum number of results
            
        Returns:
            List of outlet dictionaries
        """
        try:
            query = """
            SELECT id, name, address, operating_hours, waze_link, latitude, longitude
            FROM outlets 
            WHERE name LIKE ? OR address LIKE ?
            ORDER BY name
            LIMIT ?
            """
            
            search_term = f"%{search_query}%"
            result = self.client.execute(query, (search_term, search_term, limit))
            
            outlets = []
            for row in result.rows:
                outlet = {
                    'id': row[0],
                    'name': row[1],
                    'address': row[2],
                    'operating_hours': row[3],
                    'waze_link': row[4],
                    'latitude': row[5],
                    'longitude': row[6]
                }
                outlets.append(outlet)
            
            logger.info(f"Found {len(outlets)} outlets matching '{search_query}'")
            return outlets
            
        except Exception as e:
            logger.error(f"Failed to search outlets: {str(e)}")
            return []
    
    async def get_all_outlets(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get all outlets with limit.
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List of outlet dictionaries
        """
        try:
            query = """
            SELECT id, name, address, operating_hours, waze_link, latitude, longitude
            FROM outlets 
            ORDER BY name
            LIMIT ?
            """
            
            result = self.client.execute(query, (limit,))
            
            outlets = []
            for row in result.rows:
                outlet = {
                    'id': row[0],
                    'name': row[1],
                    'address': row[2],
                    'operating_hours': row[3],
                    'waze_link': row[4],
                    'latitude': row[5],
                    'longitude': row[6]
                }
                outlets.append(outlet)
            
            logger.info(f"Retrieved {len(outlets)} outlets")
            return outlets
            
        except Exception as e:
            logger.error(f"Failed to get all outlets: {str(e)}")
            return []
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Check database health and connectivity.
        
        Returns:
            Health check result dictionary
        """
        try:
            # Test database connectivity
            result = self.client.execute("SELECT COUNT(*) FROM outlets")
            total_outlets = result.rows[0][0] if result.rows else 0
            
            # Test a simple query
            test_result = self.client.execute("SELECT 1")
            
            return {
                "status": "healthy",
                "database_connected": True,
                "total_outlets": total_outlets,
                "test_query_success": bool(test_result.rows)
            }
            
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "database_connected": False,
                "error": str(e),
                "total_outlets": 0
            }

class OutletDatabase:
    """Database operations for outlets"""
    
    def __init__(self):
        self.client = get_db_client()
    
    def insert_outlet(self, outlet_data: Dict[str, Any]) -> Optional[int]:
        """Insert a single outlet into the database"""
        try:
            # Validate data
            clean_data = validate_outlet_data(outlet_data)
            
            # Insert query
            query = """
            INSERT INTO outlets (name, address, operating_hours, waze_link, latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            
            params = (
                clean_data['name'],
                clean_data['address'],
                clean_data['operating_hours'],
                clean_data['waze_link'],
                clean_data['latitude'],
                clean_data['longitude']
            )
            
            result = self.client.execute(query, params)
            logger.info(f"Inserted outlet: {clean_data['name']}")
            return result.last_insert_rowid
            
        except Exception as e:
            logger.error(f"Failed to insert outlet: {str(e)}")
            return None
    
    def insert_outlets_batch(self, outlets_data: List[Dict[str, Any]]) -> List[Optional[int]]:
        """Insert multiple outlets in batch"""
        inserted_ids = []
        
        for outlet_data in outlets_data:
            outlet_id = self.insert_outlet(outlet_data)
            inserted_ids.append(outlet_id)
        
        logger.info(f"Batch insert completed: {len([id for id in inserted_ids if id])} successful")
        return inserted_ids
    
    def get_outlet_by_id(self, outlet_id: int) -> Optional[Outlet]:
        """Get outlet by ID"""
        try:
            query = "SELECT * FROM outlets WHERE id = ?"
            result = self.client.execute(query, (outlet_id,))
            
            if result.rows:
                row = result.rows[0]
                return Outlet.from_dict({
                    'id': row[0],
                    'name': row[1],
                    'address': row[2],
                    'operating_hours': row[3],
                    'waze_link': row[4],
                    'latitude': row[5],
                    'longitude': row[6],
                    'created_at': row[7],
                    'updated_at': row[8]
                })
            return None
            
        except Exception as e:
            logger.error(f"Failed to get outlet by ID {outlet_id}: {str(e)}")
            return None
    
    def get_all_outlets(self) -> List[Outlet]:
        """Get all outlets"""
        try:
            query = "SELECT * FROM outlets ORDER BY name"
            result = self.client.execute(query)
            
            outlets = []
            for row in result.rows:
                outlet = Outlet.from_dict({
                    'id': row[0],
                    'name': row[1],
                    'address': row[2],
                    'operating_hours': row[3],
                    'waze_link': row[4],
                    'latitude': row[5],
                    'longitude': row[6],
                    'created_at': row[7],
                    'updated_at': row[8]
                })
                outlets.append(outlet)
            
            logger.info(f"Retrieved {len(outlets)} outlets")
            return outlets
            
        except Exception as e:
            logger.error(f"Failed to get all outlets: {str(e)}")
            return []
    
    def search_outlets_by_name(self, name: str) -> List[Outlet]:
        """Search outlets by name"""
        try:
            query = "SELECT * FROM outlets WHERE name LIKE ? ORDER BY name"
            result = self.client.execute(query, (f"%{name}%",))
            
            outlets = []
            for row in result.rows:
                outlet = Outlet.from_dict({
                    'id': row[0],
                    'name': row[1],
                    'address': row[2],
                    'operating_hours': row[3],
                    'waze_link': row[4],
                    'latitude': row[5],
                    'longitude': row[6],
                    'created_at': row[7],
                    'updated_at': row[8]
                })
                outlets.append(outlet)
            
            logger.info(f"Found {len(outlets)} outlets matching '{name}'")
            return outlets
            
        except Exception as e:
            logger.error(f"Failed to search outlets by name '{name}': {str(e)}")
            return []
    
    def check_duplicate_outlet(self, name: str, address: str) -> bool:
        """Check if outlet already exists"""
        try:
            query = "SELECT COUNT(*) FROM outlets WHERE name = ? AND address = ?"
            result = self.client.execute(query, (name, address))
            
            count = result.rows[0][0] if result.rows else 0
            return count > 0
            
        except Exception as e:
            logger.error(f"Failed to check duplicate outlet: {str(e)}")
            return False
    
    def get_outlets_without_coordinates(self) -> List[Outlet]:
        """Get outlets that don't have coordinates"""
        try:
            query = "SELECT * FROM outlets WHERE latitude IS NULL OR longitude IS NULL"
            result = self.client.execute(query)
            
            outlets = []
            for row in result.rows:
                outlet = Outlet.from_dict({
                    'id': row[0],
                    'name': row[1],
                    'address': row[2],
                    'operating_hours': row[3],
                    'waze_link': row[4],
                    'latitude': row[5],
                    'longitude': row[6],
                    'created_at': row[7],
                    'updated_at': row[8]
                })
                outlets.append(outlet)
            
            logger.info(f"Found {len(outlets)} outlets without coordinates")
            return outlets
            
        except Exception as e:
            logger.error(f"Failed to get outlets without coordinates: {str(e)}")
            return []
    
    def update_outlet_coordinates(self, outlet_id: int, latitude: float, longitude: float) -> bool:
        """Update outlet coordinates"""
        try:
            query = "UPDATE outlets SET latitude = ?, longitude = ? WHERE id = ?"
            result = self.client.execute(query, (latitude, longitude, outlet_id))
            
            logger.info(f"Updated coordinates for outlet ID {outlet_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update coordinates for outlet ID {outlet_id}: {str(e)}")
            return False
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            stats = {}
            
            # Total outlets
            result = self.client.execute("SELECT COUNT(*) FROM outlets")
            stats['total_outlets'] = result.rows[0][0] if result.rows else 0
            
            # Outlets with coordinates
            result = self.client.execute("SELECT COUNT(*) FROM outlets WHERE latitude IS NOT NULL AND longitude IS NOT NULL")
            stats['outlets_with_coordinates'] = result.rows[0][0] if result.rows else 0
            
            # Outlets without coordinates
            stats['outlets_without_coordinates'] = stats['total_outlets'] - stats['outlets_with_coordinates']
            
            # Latest outlet
            result = self.client.execute("SELECT name, created_at FROM outlets ORDER BY created_at DESC LIMIT 1")
            if result.rows:
                stats['latest_outlet'] = {
                    'name': result.rows[0][0],
                    'created_at': result.rows[0][1]
                }
            
            logger.info(f"Database stats: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get database stats: {str(e)}")
            return {}
    
    def clear_all_outlets(self) -> bool:
        """Clear all outlets from the database"""
        try:
            query = "DELETE FROM outlets"
            result = self.client.execute(query)
            
            logger.info("All outlets cleared from database")
            return True
            
        except Exception as e:
            logger.error(f"Failed to clear all outlets: {str(e)}")
            return False

# Global instance
outlet_db = OutletDatabase()

# Convenience functions
def insert_outlet(outlet_data: Dict[str, Any]) -> Optional[int]:
    """Insert a single outlet"""
    return outlet_db.insert_outlet(outlet_data)

def insert_outlets_batch(outlets_data: List[Dict[str, Any]]) -> List[Optional[int]]:
    """Insert multiple outlets"""
    return outlet_db.insert_outlets_batch(outlets_data)

def get_all_outlets() -> List[Outlet]:
    """Get all outlets"""
    return outlet_db.get_all_outlets()

def search_outlets_by_name(name: str) -> List[Outlet]:
    """Search outlets by name"""
    return outlet_db.search_outlets_by_name(name)

def get_database_stats() -> Dict[str, Any]:
    """Get database statistics"""
    return outlet_db.get_database_stats() 