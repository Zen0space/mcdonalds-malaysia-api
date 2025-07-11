"""
McDonald's Context Provider

This module provides McDonald's specific context and knowledge base
for the chatbot to answer questions about outlets, locations, and services.
"""

import logging
from typing import Dict, List, Optional, Any
from ..database.operations import DatabaseOperations
import math

logger = logging.getLogger(__name__)

class McDonaldContext:
    """
    Provides McDonald's Malaysia specific context for the chatbot.
    
    This class handles:
    - Outlet data retrieval
    - Location-based queries
    - Operating hours information
    - Distance calculations
    - Context formatting for AI
    """
    
    def __init__(self, db_operations: DatabaseOperations):
        """
        Initialize McDonald's context provider.
        
        Args:
            db_operations: Database operations instance
        """
        self.db = db_operations
        logger.info("Initialized McDonald's context provider")
    
    async def get_outlet_context(self, query: str, user_location: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Get relevant outlet context based on user query.
        
        Args:
            query: User's query/message
            user_location: Optional user location {"lat": float, "lng": float}
            
        Returns:
            Context dictionary with relevant outlet information
        """
        context = {
            "query_type": self._classify_query(query),
            "outlets": [],
            "user_location": user_location
        }
        
        # Handle different query types
        if context["query_type"] == "nearby":
            context["outlets"] = await self._get_nearby_outlets(user_location, query)
        elif context["query_type"] == "location_search":
            context["outlets"] = await self._search_outlets_by_location(query)
        elif context["query_type"] == "hours":
            context["outlets"] = await self._get_outlets_with_hours(query)
        elif context["query_type"] == "24_hours":
            context["outlets"] = await self._get_24_hour_outlets()
        elif context["query_type"] == "general":
            context["outlets"] = await self._get_popular_outlets()
        
        # Add distance calculations if user location is provided
        if user_location and context["outlets"]:
            context["outlets"] = self._add_distances(context["outlets"], user_location)
        
        return context
    
    def _classify_query(self, query: str) -> str:
        """
        Classify the type of query to determine appropriate context.
        
        Args:
            query: User's query
            
        Returns:
            Query type classification
        """
        query_lower = query.lower()
        
        # Location-based queries
        if any(word in query_lower for word in ["near", "nearby", "close", "closest"]):
            return "nearby"
        
        # Specific location searches
        if any(word in query_lower for word in ["kl", "kuala lumpur", "klcc", "bukit bintang", "mid valley"]):
            return "location_search"
        
        # Operating hours queries
        if any(word in query_lower for word in ["hours", "open", "close", "operating", "time"]):
            return "hours"
        
        # 24-hour queries
        if any(word in query_lower for word in ["24", "twenty four", "24 hours", "24-hour"]):
            return "24_hours"
        
        # General queries
        return "general"
    
    async def _get_nearby_outlets(self, user_location: Optional[Dict], query: str) -> List[Dict]:
        """Get nearby outlets based on user location."""
        if not user_location:
            # If no location provided, return popular outlets
            return await self._get_popular_outlets()
        
        try:
            # Use existing nearby API functionality
            outlets = await self.db.get_nearby_outlets(
                latitude=user_location["lat"],
                longitude=user_location["lng"],
                radius_km=10,  # 10km radius
                limit=5
            )
            return outlets
        except Exception as e:
            logger.error(f"Error getting nearby outlets: {str(e)}")
            return []
    
    async def _search_outlets_by_location(self, query: str) -> List[Dict]:
        """Search outlets by location name."""
        try:
            # Extract location keywords
            location_keywords = self._extract_location_keywords(query)
            
            outlets = []
            for keyword in location_keywords:
                results = await self.db.search_outlets(
                    search_query=keyword,
                    limit=10
                )
                outlets.extend(results)
            
            # Remove duplicates and limit results
            unique_outlets = {outlet['id']: outlet for outlet in outlets}
            return list(unique_outlets.values())[:5]
            
        except Exception as e:
            logger.error(f"Error searching outlets by location: {str(e)}")
            return []
    
    async def _get_outlets_with_hours(self, query: str) -> List[Dict]:
        """Get outlets with operating hours information."""
        try:
            outlets = await self.db.get_all_outlets(limit=10)
            # Filter outlets that have operating hours
            return [outlet for outlet in outlets if outlet.get('operating_hours')]
        except Exception as e:
            logger.error(f"Error getting outlets with hours: {str(e)}")
            return []
    
    async def _get_24_hour_outlets(self) -> List[Dict]:
        """Get 24-hour McDonald's outlets."""
        try:
            outlets = await self.db.get_all_outlets(limit=50)
            # Filter for 24-hour outlets
            return [
                outlet for outlet in outlets 
                if outlet.get('operating_hours') and '24' in outlet['operating_hours']
            ]
        except Exception as e:
            logger.error(f"Error getting 24-hour outlets: {str(e)}")
            return []
    
    async def _get_popular_outlets(self) -> List[Dict]:
        """Get popular/featured outlets."""
        try:
            # Get first 5 outlets as popular ones
            outlets = await self.db.get_all_outlets(limit=5)
            return outlets
        except Exception as e:
            logger.error(f"Error getting popular outlets: {str(e)}")
            return []
    
    def _extract_location_keywords(self, query: str) -> List[str]:
        """Extract location keywords from query."""
        # Common KL locations
        locations = [
            "klcc", "bukit bintang", "mid valley", "kl sentral", "pavilion",
            "times square", "lot 10", "suria klcc", "avenue k", "ampang park",
            "cheras", "puchong", "petaling jaya", "subang", "shah alam"
        ]
        
        query_lower = query.lower()
        found_locations = []
        
        for location in locations:
            if location in query_lower:
                found_locations.append(location)
        
        # Also add general terms
        if "kl" in query_lower or "kuala lumpur" in query_lower:
            found_locations.append("kuala lumpur")
        
        return found_locations or ["kuala lumpur"]  # Default to KL
    
    def _add_distances(self, outlets: List[Dict], user_location: Dict) -> List[Dict]:
        """Add distance calculations to outlets."""
        for outlet in outlets:
            if outlet.get('latitude') and outlet.get('longitude'):
                distance = self._calculate_distance(
                    user_location["lat"], user_location["lng"],
                    outlet['latitude'], outlet['longitude']
                )
                outlet['distance_km'] = f"{distance:.1f}"
        
        # Sort by distance
        outlets.sort(key=lambda x: float(x.get('distance_km', '999')))
        return outlets
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two points using Haversine formula.
        
        Args:
            lat1, lon1: First point coordinates
            lat2, lon2: Second point coordinates
            
        Returns:
            Distance in kilometers
        """
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Earth's radius in kilometers
        r = 6371
        
        return r * c
    
    def get_general_info(self) -> Dict[str, Any]:
        """Get general McDonald's Malaysia information."""
        return {
            "brand": "McDonald's Malaysia",
            "coverage": "Kuala Lumpur and surrounding areas",
            "services": [
                "Dine-in",
                "Drive-Thru",
                "McDelivery",
                "24-hour locations",
                "McCafe"
            ],
            "features": [
                "GPS navigation via Waze",
                "Operating hours information",
                "Location-based search",
                "Distance calculations"
            ]
        }
    
    def get_help_text(self) -> str:
        """Get help text for users."""
        return """
I can help you with McDonald's Malaysia outlets! Here's what you can ask me:

🍟 **Find Outlets:**
- "Find nearest McDonald's"
- "McDonald's near KLCC"
- "McDonald's in Bukit Bintang"

⏰ **Operating Hours:**
- "What time does McDonald's open?"
- "24-hour McDonald's"
- "McDonald's operating hours"

📍 **Directions:**
- "How to get to McDonald's?"
- "Directions to nearest McDonald's"

🗺️ **General Info:**
- "McDonald's locations in KL"
- "McDonald's services"

Just ask me anything about McDonald's Malaysia outlets!
""" 