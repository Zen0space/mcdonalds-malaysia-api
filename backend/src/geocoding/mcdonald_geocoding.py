#!/usr/bin/env python3
"""
McDonald's Malaysia Geocoding Interface
Provides geocoding services specifically for McDonald's outlets in Kuala Lumpur.
"""

import re
import logging
from typing import Optional, Dict, Any, List
from .nominatim_service import NominatimService
from .validators import KLCoordinateValidator

class McDonaldGeocoder:
    """Main geocoding interface for McDonald's Malaysia outlets."""
    
    def __init__(self):
        """Initialize McDonald's geocoder."""
        self.nominatim = NominatimService()
        self.validator = KLCoordinateValidator()
        self.logger = logging.getLogger(__name__)
        
        # Statistics tracking
        self.stats = {
            'total_requests': 0,
            'successful_geocodes': 0,
            'failed_geocodes': 0,
            'invalid_coordinates': 0,
            'rate_limited': 0
        }
    
    def geocode_outlet(self, outlet_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Geocode a McDonald's outlet using Waze link first, then fallback to address geocoding.
        
        Args:
            outlet_data: Dictionary containing outlet information
            
        Returns:
            Enhanced outlet data with geocoding results
        """
        self.stats['total_requests'] += 1
        
        # Extract information
        name = outlet_data.get('name', '')
        address = outlet_data.get('address', '')
        waze_link = outlet_data.get('waze_link', '')
        
        self.logger.debug(f"Geocoding outlet: {name}")
        
        # Method 1: Try extracting coordinates from Waze link first (most accurate)
        if waze_link:
            self.logger.debug(f"Trying Waze link: {waze_link}")
            lat, lng = self._extract_coordinates_from_waze_link(waze_link)
            
            if lat is not None and lng is not None:
                # Success with Waze link!
                self.stats['successful_geocodes'] += 1
                
                # Create enhanced outlet data
                enhanced_outlet = {
                    **outlet_data,
                    'latitude': lat,
                    'longitude': lng,
                    'geocoding': {
                        'status': 'success',
                        'confidence': 0.95,  # High confidence for Waze links
                        'formatted_address': address,
                        'location_type': 'waze_link',
                        'validation_issues': []
                    }
                }
                
                self.logger.info(f"✅ Geocoded from Waze link {name}: {lat}, {lng}")
                return enhanced_outlet
            else:
                self.logger.debug("No coordinates found in Waze link, falling back to address geocoding")
        
        # Method 2: Fallback to address geocoding if Waze link fails
        if not address:
            self.logger.warning(f"No address found for outlet: {name}")
            return self._add_geocoding_failure(outlet_data, 'No address provided')
        
        # Clean and prepare address for geocoding
        cleaned_address = self._clean_address(address)
        
        self.logger.debug(f"Original address: {address}")
        self.logger.debug(f"Cleaned address: {cleaned_address}")
        
        # Try geocoding with different address variations
        geocoding_result = self._try_geocoding_variations(cleaned_address, name)
        
        if not geocoding_result or geocoding_result.get('status') != 'success':
            self.stats['failed_geocodes'] += 1
            return self._add_geocoding_failure(outlet_data, 'Geocoding failed')
        
        # Validate coordinates
        validated_result = self.validator.validate_geocoding_result(geocoding_result)
        
        if not validated_result.get('validation', {}).get('is_valid', False):
            self.stats['invalid_coordinates'] += 1
            self.logger.warning(f"Invalid coordinates for {name}: {validated_result.get('validation', {}).get('reason', 'Unknown')}")
            return self._add_geocoding_failure(outlet_data, 'Invalid coordinates')
        
        # Success!
        self.stats['successful_geocodes'] += 1
        
        # Add geocoding data to outlet
        enhanced_outlet = {
            **outlet_data,
            'latitude': validated_result['latitude'],
            'longitude': validated_result['longitude'],
            'geocoding': {
                'status': 'success',
                'confidence': validated_result.get('combined_confidence', 0),
                'formatted_address': validated_result.get('formatted_address', ''),
                'location_type': validated_result.get('validation', {}).get('location_type', 'unknown'),
                'validation_issues': validated_result.get('validation', {}).get('validation_issues', [])
            }
        }
        
        self.logger.info(f"✅ Geocoded from address {name}: {validated_result['latitude']}, {validated_result['longitude']}")
        
        return enhanced_outlet
    
    def _clean_address(self, address: str) -> str:
        """
        Clean and standardize Malaysian address for better geocoding.
        
        Args:
            address: Raw address string
            
        Returns:
            Cleaned address string
        """
        if not address:
            return ""
        
        # Remove extra whitespace and normalize
        cleaned = re.sub(r'\s+', ' ', address.strip())
        
        # AGGRESSIVE CLEANING: Remove phone numbers, fax numbers, and contact info
        # Remove phone patterns (Tel: 03-12345678, Fax: 03-12345678, 03-12345678)
        cleaned = re.sub(r'\b(?:Tel|Fax|Phone|Telephone):\s*[\d\s\-]+', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\b03-\d{8}\b', '', cleaned)  # Remove standalone phone numbers
        cleaned = re.sub(r'\b03-\d{4}\s*\d{4}\b', '', cleaned)  # Remove formatted phone numbers
        cleaned = re.sub(r'\b\+60\s*3-?\d{8}\b', '', cleaned)  # Remove international format
        cleaned = re.sub(r'\b\d{3}-\d{8}\b', '', cleaned)  # Remove other phone patterns
        
        # Remove email addresses
        cleaned = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', cleaned)
        
        # Remove website URLs
        cleaned = re.sub(r'https?://[^\s]+', '', cleaned)
        cleaned = re.sub(r'www\.[^\s]+', '', cleaned)
        
        # Remove extra punctuation and formatting
        cleaned = re.sub(r',\s*,', ',', cleaned)  # Remove double commas
        cleaned = re.sub(r'\s*,\s*$', '', cleaned)  # Remove trailing comma
        cleaned = re.sub(r'^\s*,\s*', '', cleaned)  # Remove leading comma
        
        # Remove standalone numbers that might be phone/fax remnants
        cleaned = re.sub(r'\b\d{8,}\b', '', cleaned)  # Remove long number sequences
        
        # Clean up multiple spaces and punctuation
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = re.sub(r'[,\s]+$', '', cleaned)  # Remove trailing punctuation
        cleaned = cleaned.strip()
        
        # Common Malaysian address abbreviations
        abbreviations = {
            'Jln': 'Jalan',
            'Jalan': 'Jalan',
            'Rd': 'Road',
            'St': 'Street',
            'Ave': 'Avenue',
            'Blvd': 'Boulevard',
            'KL': 'Kuala Lumpur',
            'W.P.': 'Wilayah Persekutuan',
            'WP': 'Wilayah Persekutuan'
        }
        
        # Apply abbreviation expansions
        for abbr, full in abbreviations.items():
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(abbr) + r'\b'
            cleaned = re.sub(pattern, full, cleaned, flags=re.IGNORECASE)
        
        # Ensure "Kuala Lumpur" is included for better geocoding
        if 'kuala lumpur' not in cleaned.lower() and 'kl' not in cleaned.lower():
            cleaned += ', Kuala Lumpur'
        
        # Ensure "Malaysia" is included
        if 'malaysia' not in cleaned.lower():
            cleaned += ', Malaysia'
        
        # Final cleanup
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = re.sub(r',\s*,', ',', cleaned)
        cleaned = cleaned.strip()
        
        return cleaned
    
    def _try_geocoding_variations(self, address: str, outlet_name: str) -> Optional[Dict[str, Any]]:
        """
        Try geocoding with different address variations.
        Based on test results, simpler addresses work better with Nominatim.
        
        Args:
            address: Cleaned address string
            outlet_name: Name of the outlet
            
        Returns:
            Geocoding result or None if all attempts fail
        """
        # Extract key location components for progressive simplification
        variations = self._generate_progressive_variations(address, outlet_name)
        
        for i, variation in enumerate(variations):
            if not variation or len(variation.strip()) < 3:
                continue
                
            self.logger.debug(f"Trying variation {i+1}: {variation}")
            
            result = self.nominatim.geocode_address(variation)
            
            if result and result.get('status') == 'success':
                self.logger.debug(f"Success with variation {i+1}")
                return result
            elif result and result.get('status') == 'rate_limited':
                self.stats['rate_limited'] += 1
                self.logger.warning("Rate limited during geocoding")
                return result
        
        return None
    
    def _generate_progressive_variations(self, address: str, outlet_name: str) -> List[str]:
        """
        Generate progressive address variations from most specific to most general.
        Based on test results showing simpler addresses work better.
        """
        variations = []
        
        # Remove Malaysia suffix as it seems to cause issues
        clean_address = re.sub(r',?\s*Malaysia\s*$', '', address, flags=re.IGNORECASE)
        
        # 1. Original cleaned address (without Malaysia)
        variations.append(clean_address)
        
        # 2. Extract main street/area name from the address
        street_match = re.search(r'Jalan\s+([^,]+)', clean_address, re.IGNORECASE)
        if street_match:
            street_name = street_match.group(1).strip()
            # Try "Street Name, Kuala Lumpur"
            variations.append(f"{street_name}, Kuala Lumpur")
            # Try "Jalan Street Name, KL"
            variations.append(f"Jalan {street_name}, KL")
        
        # 3. Extract area/district names
        area_patterns = [
            r'(Bukit\s+\w+)',
            r'(Bangsar\s*\w*)',
            r'(Mont\s+Kiara)',
            r'(TTDI|Taman\s+Tun\s+Dr\s+Ismail)',
            r'(Cheras)',
            r'(Kepong)',
            r'(Sentul)',
            r'(Ampang)',
            r'(Petaling)',
            r'(Setapak)',
            r'(Wangsa\s+Maju)',
            r'(Sri\s+Petaling)',
            r'(Danau\s+Kota)',
            r'(Desa\s+\w+)',
            r'(Taman\s+\w+)'
        ]
        
        for pattern in area_patterns:
            area_match = re.search(pattern, clean_address, re.IGNORECASE)
            if area_match:
                area_name = area_match.group(1).strip()
                # Try "Area Name, Kuala Lumpur"
                variations.append(f"{area_name}, Kuala Lumpur")
                break
        
        # 4. Try with famous landmarks if address contains mall/complex names
        landmark_patterns = [
            r'(Times\s+Square)',
            r'(Pavilion)',
            r'(KLCC|Suria\s+KLCC)',
            r'(Mid\s+Valley)',
            r'(NU\s+Sentral)',
            r'(Sunway\s+Velocity)',
            r'(MyTown)',
            r'(Intermark)',
            r'(Berjaya\s+Times\s+Square)'
        ]
        
        for pattern in landmark_patterns:
            landmark_match = re.search(pattern, clean_address, re.IGNORECASE)
            if landmark_match:
                landmark = landmark_match.group(1).strip()
                variations.append(f"{landmark}, Kuala Lumpur")
                break
        
        # 5. Try outlet name with location (sometimes works)
        if outlet_name and "McDonald's" in outlet_name:
            # Extract location from outlet name
            location_match = re.search(r"McDonald's\s+(.+)", outlet_name)
            if location_match:
                location = location_match.group(1).strip()
                # Clean up common suffixes
                location = re.sub(r'\s+(DT|SF)$', '', location)
                variations.append(f"{location}, Kuala Lumpur")
        
        # 6. Simplified address (remove unit numbers, floor info)
        simplified = self._simplify_address(clean_address)
        if simplified and simplified not in variations:
            variations.append(simplified)
        
        # 7. Last resort: just the city
        variations.extend([
            "Kuala Lumpur",
            "KL"
        ])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_variations = []
        for var in variations:
            if var and var not in seen:
                seen.add(var)
                unique_variations.append(var)
        
        return unique_variations
    
    def _extract_coordinates_from_waze_link(self, waze_link: str) -> tuple[Optional[float], Optional[float]]:
        """Extract latitude and longitude from Waze link"""
        if not waze_link:
            return None, None
        
        self.logger.debug(f"Extracting coordinates from Waze link: {waze_link}")
        
        # NEW: Handle URL-encoded coordinates in live-map format
        # Pattern: to=ll.3.146847%2C101.710931 (where %2C is URL-encoded comma)
        url_encoded_pattern = r'to=ll\.([+-]?\d+\.?\d*)%2C([+-]?\d+\.?\d*)'
        match = re.search(url_encoded_pattern, waze_link, re.IGNORECASE)
        
        if match:
            try:
                lat = float(match.group(1))
                lon = float(match.group(2))
                
                # Validate coordinates are within reasonable bounds for Malaysia
                if 1 <= lat <= 7 and 99 <= lon <= 119:
                    self.logger.debug(f"✅ Extracted coordinates from URL-encoded format: {lat}, {lon}")
                    return lat, lon
                else:
                    self.logger.warning(f"Waze coordinates outside Malaysia bounds: {lat}, {lon}")
                    return None, None
                    
            except ValueError:
                self.logger.warning(f"Invalid coordinate format in Waze link: {waze_link}")
        
        # Original pattern for Waze coordinates: ll=latitude,longitude
        pattern = r'll=([+-]?\d+\.?\d*),([+-]?\d+\.?\d*)'
        match = re.search(pattern, waze_link)
        
        if match:
            try:
                lat = float(match.group(1))
                lon = float(match.group(2))
                
                # Validate coordinates are within reasonable bounds for Malaysia
                if 1 <= lat <= 7 and 99 <= lon <= 119:
                    self.logger.debug(f"✅ Extracted coordinates from standard format: {lat}, {lon}")
                    return lat, lon
                else:
                    self.logger.warning(f"Waze coordinates outside Malaysia bounds: {lat}, {lon}")
                    return None, None
                    
            except ValueError:
                self.logger.warning(f"Invalid coordinate format in Waze link: {waze_link}")
        
        # Try alternative Waze URL patterns
        # Some Waze links use different formats
        patterns = [
            r'navigate\?lat=([+-]?\d+\.?\d*)&lon=([+-]?\d+\.?\d*)',
            r'lat=([+-]?\d+\.?\d*)&lon=([+-]?\d+\.?\d*)',
            r'q=([+-]?\d+\.?\d*),([+-]?\d+\.?\d*)',
            r'at=([+-]?\d+\.?\d*),([+-]?\d+\.?\d*)',
            # Additional patterns for live-map format
            r'to=ll\.([+-]?\d+\.?\d*),([+-]?\d+\.?\d*)',  # Non-encoded version
            r'll\.([+-]?\d+\.?\d*)%2C([+-]?\d+\.?\d*)',   # Alternative URL-encoded
            r'll\.([+-]?\d+\.?\d*),([+-]?\d+\.?\d*)'      # Alternative non-encoded
        ]
        
        for pattern in patterns:
            match = re.search(pattern, waze_link, re.IGNORECASE)
            if match:
                try:
                    lat = float(match.group(1))
                    lon = float(match.group(2))
                    
                    # Validate coordinates
                    if 1 <= lat <= 7 and 99 <= lon <= 119:
                        self.logger.debug(f"✅ Extracted coordinates from alternative pattern: {lat}, {lon}")
                        return lat, lon
                        
                except ValueError:
                    continue
        
        self.logger.warning(f"No valid coordinates found in Waze link: {waze_link}")
        return None, None
    
    def _simplify_address(self, address: str) -> str:
        """
        Create a simplified version of the address for geocoding.
        
        Args:
            address: Full address string
            
        Returns:
            Simplified address string
        """
        # Remove common problematic elements
        simplified = address
        
        # Remove floor/unit numbers
        simplified = re.sub(r'\b(?:Floor|Level|Unit|Lot)\s+\d+[A-Z]?\b', '', simplified, flags=re.IGNORECASE)
        simplified = re.sub(r'\b\d+[A-Z]?[-\s]*\d+[A-Z]?\b', '', simplified)  # Remove unit numbers like "G-01"
        
        # Remove parenthetical information
        simplified = re.sub(r'\([^)]*\)', '', simplified)
        
        # Remove extra commas and spaces
        simplified = re.sub(r',\s*,', ',', simplified)
        simplified = re.sub(r'\s+', ' ', simplified)
        simplified = simplified.strip().strip(',').strip()
        
        return simplified
    
    def _add_geocoding_failure(self, outlet_data: Dict[str, Any], reason: str) -> Dict[str, Any]:
        """
        Add geocoding failure information to outlet data.
        
        Args:
            outlet_data: Original outlet data
            reason: Reason for failure
            
        Returns:
            Enhanced outlet data with failure information
        """
        return {
            **outlet_data,
            'latitude': None,
            'longitude': None,
            'geocoding': {
                'status': 'failed',
                'confidence': 0,
                'formatted_address': '',
                'location_type': 'failed',
                'reason': reason
            }
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get geocoding statistics."""
        total = self.stats['total_requests']
        success_rate = (self.stats['successful_geocodes'] / total * 100) if total > 0 else 0
        
        return {
            **self.stats,
            'success_rate': round(success_rate, 1)
        }
    
    def reset_statistics(self):
        """Reset geocoding statistics."""
        self.stats = {
            'total_requests': 0,
            'successful_geocodes': 0,
            'failed_geocodes': 0,
            'invalid_coordinates': 0,
            'rate_limited': 0
        }
    
    def batch_geocode_outlets(self, outlets: List[Dict[str, Any]], progress_callback=None) -> List[Dict[str, Any]]:
        """
        Geocode multiple outlets with progress tracking.
        
        Args:
            outlets: List of outlet data dictionaries
            progress_callback: Optional callback for progress updates
            
        Returns:
            List of enhanced outlet data with geocoding results
        """
        results = []
        total = len(outlets)
        
        self.logger.info(f"Starting batch geocoding of {total} outlets")
        
        for i, outlet in enumerate(outlets):
            if progress_callback:
                progress_callback(i + 1, total, outlet.get('name', 'Unknown'))
            
            enhanced_outlet = self.geocode_outlet(outlet)
            results.append(enhanced_outlet)
            
            # Log progress
            if (i + 1) % 5 == 0:
                stats = self.get_statistics()
                self.logger.info(f"Progress: {i + 1}/{total} outlets processed, {stats['success_rate']}% success rate")
        
        # Final statistics
        final_stats = self.get_statistics()
        self.logger.info(f"Batch geocoding complete: {final_stats['successful_geocodes']}/{total} successful ({final_stats['success_rate']}%)")
        
        return results 