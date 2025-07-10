#!/usr/bin/env python3
"""
Kuala Lumpur Coordinate Validator
Validates that geocoded coordinates are within reasonable bounds for Kuala Lumpur.
"""

import logging
from typing import Optional, Dict, Any, Tuple

class KLCoordinateValidator:
    """Validator for Kuala Lumpur coordinates."""
    
    # Kuala Lumpur approximate bounds
    KL_BOUNDS = {
        'min_latitude': 2.9,      # Southern boundary
        'max_latitude': 3.4,      # Northern boundary  
        'min_longitude': 101.5,   # Western boundary
        'max_longitude': 101.9    # Eastern boundary
    }
    
    # More precise central KL bounds for higher confidence
    KL_CENTRAL_BOUNDS = {
        'min_latitude': 3.0,
        'max_latitude': 3.25,
        'min_longitude': 101.6,
        'max_longitude': 101.8
    }
    
    def __init__(self):
        """Initialize validator."""
        self.logger = logging.getLogger(__name__)
    
    def validate_coordinates(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """
        Validate coordinates are within Kuala Lumpur bounds.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Dictionary with validation results
        """
        if latitude is None or longitude is None:
            return {
                'is_valid': False,
                'confidence': 0,
                'location_type': 'invalid',
                'reason': 'Missing coordinates'
            }
        
        # Check if coordinates are within KL bounds
        within_kl = self._is_within_bounds(latitude, longitude, self.KL_BOUNDS)
        within_central_kl = self._is_within_bounds(latitude, longitude, self.KL_CENTRAL_BOUNDS)
        
        if not within_kl:
            return {
                'is_valid': False,
                'confidence': 0,
                'location_type': 'outside_kl',
                'reason': f'Coordinates ({latitude}, {longitude}) are outside Kuala Lumpur bounds'
            }
        
        # Determine location type and confidence
        if within_central_kl:
            location_type = 'central_kl'
            confidence = 0.9
        else:
            location_type = 'greater_kl'
            confidence = 0.7
        
        # Additional validation checks
        validation_issues = []
        
        # Check for obviously invalid coordinates
        if self._is_in_water(latitude, longitude):
            validation_issues.append('Coordinates may be in water')
            confidence -= 0.2
        
        if self._is_too_precise(latitude, longitude):
            validation_issues.append('Coordinates suspiciously precise')
            confidence -= 0.1
        
        # Final confidence adjustment
        confidence = max(confidence, 0.1)  # Minimum confidence
        
        return {
            'is_valid': True,
            'confidence': round(confidence, 2),
            'location_type': location_type,
            'validation_issues': validation_issues,
            'bounds_check': {
                'within_kl': within_kl,
                'within_central_kl': within_central_kl
            }
        }
    
    def _is_within_bounds(self, lat: float, lng: float, bounds: Dict[str, float]) -> bool:
        """Check if coordinates are within specified bounds."""
        return (bounds['min_latitude'] <= lat <= bounds['max_latitude'] and
                bounds['min_longitude'] <= lng <= bounds['max_longitude'])
    
    def _is_in_water(self, latitude: float, longitude: float) -> bool:
        """
        Check if coordinates are likely in water bodies.
        Basic check for major water bodies around KL.
        """
        # This is a simplified check - in production, you might use more sophisticated methods
        
        # Check if coordinates are in known water body areas
        # (These are approximate bounds for major water bodies near KL)
        
        # Klang River area (very rough approximation)
        if (3.0 <= latitude <= 3.2 and 101.65 <= longitude <= 101.75):
            # More detailed check would be needed here
            pass
        
        # For now, return False as we don't have detailed water body data
        return False
    
    def _is_too_precise(self, latitude: float, longitude: float) -> bool:
        """
        Check if coordinates are suspiciously precise.
        Nominatim usually returns coordinates with reasonable precision.
        """
        # Convert to string to check decimal places
        lat_str = str(latitude)
        lng_str = str(longitude)
        
        # Count decimal places
        lat_decimals = len(lat_str.split('.')[-1]) if '.' in lat_str else 0
        lng_decimals = len(lng_str.split('.')[-1]) if '.' in lng_str else 0
        
        # If more than 6 decimal places, it might be suspiciously precise
        return lat_decimals > 6 or lng_decimals > 6
    
    def validate_geocoding_result(self, geocoding_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate complete geocoding result.
        
        Args:
            geocoding_result: Result from geocoding service
            
        Returns:
            Enhanced result with validation information
        """
        if not geocoding_result or geocoding_result.get('status') != 'success':
            return {
                **geocoding_result,
                'validation': {
                    'is_valid': False,
                    'confidence': 0,
                    'location_type': 'failed_geocoding',
                    'reason': 'Geocoding failed'
                }
            }
        
        latitude = geocoding_result.get('latitude')
        longitude = geocoding_result.get('longitude')
        
        validation = self.validate_coordinates(latitude, longitude)
        
        # Combine geocoding confidence with validation confidence
        geocoding_confidence = geocoding_result.get('confidence', 0)
        validation_confidence = validation.get('confidence', 0)
        
        # Use weighted average (geocoding confidence is more important)
        combined_confidence = (geocoding_confidence * 0.7) + (validation_confidence * 0.3)
        
        return {
            **geocoding_result,
            'validation': validation,
            'combined_confidence': round(combined_confidence, 2)
        }
    
    def get_kl_bounds_info(self) -> Dict[str, Any]:
        """Get information about KL bounds used for validation."""
        return {
            'kl_bounds': self.KL_BOUNDS,
            'central_kl_bounds': self.KL_CENTRAL_BOUNDS,
            'description': 'Approximate bounds for Kuala Lumpur validation'
        }
    
    def is_coordinate_in_kl(self, latitude: float, longitude: float) -> bool:
        """
        Simple check if coordinate is in KL bounds.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            True if coordinate is within KL bounds
        """
        if latitude is None or longitude is None:
            return False
        
        return self._is_within_bounds(latitude, longitude, self.KL_BOUNDS) 