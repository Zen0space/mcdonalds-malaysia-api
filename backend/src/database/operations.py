"""
Database operations for McDonald's outlets
"""
import logging
from typing import List, Optional, Dict, Any
from .connection import get_db_client
from .models import Outlet, validate_outlet_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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