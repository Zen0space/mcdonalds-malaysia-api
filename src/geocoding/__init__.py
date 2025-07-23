"""
McDonald's Malaysia Geocoding Module
Provides geocoding services for McDonald's outlet addresses in Kuala Lumpur.
"""

from .mcdonald_geocoding import McDonaldGeocoder
from .nominatim_service import NominatimService
from .validators import KLCoordinateValidator

__version__ = "1.0.0"
__author__ = "McDonald's Scraper Project"

# Export main classes
__all__ = [
    "McDonaldGeocoder",
    "NominatimService", 
    "KLCoordinateValidator"
] 