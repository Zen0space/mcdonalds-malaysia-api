#!/usr/bin/env python3
"""
Nominatim Service for McDonald's Malaysia Geocoding
Provides a wrapper around the OpenStreetMap Nominatim API with rate limiting.
"""

import time
import logging
from typing import Optional, Dict, Any, Tuple
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError, GeocoderRateLimited

class NominatimService:
    """Nominatim geocoding service with rate limiting and error handling."""
    
    def __init__(self, user_agent: str = "McDonald's Malaysia Scraper v1.0"):
        """Initialize Nominatim service."""
        self.geocoder = Nominatim(user_agent=user_agent)
        self.last_request_time = 0
        self.rate_limit_delay = 1.0  # 1 second between requests for free tier
        self.max_retries = 3
        self.timeout = 10
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
    def _rate_limit(self):
        """Enforce rate limiting for Nominatim API."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - time_since_last
            self.logger.debug(f"Rate limiting: sleeping {sleep_time:.2f}s")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def geocode_address(self, address: str, country_code: str = "MY") -> Optional[Dict[str, Any]]:
        """
        Geocode a single address using Nominatim.
        
        Args:
            address: Address string to geocode
            country_code: ISO country code (default: MY for Malaysia)
            
        Returns:
            Dict with geocoding results or None if failed
        """
        if not address or not address.strip():
            return None
            
        # Rate limiting
        self._rate_limit()
        
        # Build search query
        search_query = f"{address}, Malaysia"
        
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                self.logger.debug(f"Geocoding attempt {retry_count + 1}: {search_query}")
                
                # Make geocoding request
                location = self.geocoder.geocode(
                    search_query,
                    country_codes=[country_code],
                    timeout=self.timeout,
                    exactly_one=True
                )
                
                if location:
                    result = {
                        'latitude': location.latitude,
                        'longitude': location.longitude,
                        'formatted_address': location.address,
                        'raw_data': location.raw,
                        'confidence': self._calculate_confidence(location, address),
                        'status': 'success'
                    }
                    
                    self.logger.debug(f"Geocoding successful: {location.latitude}, {location.longitude}")
                    return result
                else:
                    self.logger.warning(f"No results found for: {address}")
                    return {
                        'latitude': None,
                        'longitude': None,
                        'formatted_address': None,
                        'raw_data': None,
                        'confidence': 0,
                        'status': 'no_results',
                        'error': 'No geocoding results found'
                    }
                    
            except GeocoderRateLimited as e:
                self.logger.warning(f"Rate limited, waiting longer: {e}")
                time.sleep(self.rate_limit_delay * 2)  # Wait longer on rate limit
                retry_count += 1
                
            except GeocoderTimedOut as e:
                self.logger.warning(f"Geocoding timeout: {e}")
                retry_count += 1
                time.sleep(1)  # Brief delay before retry
                
            except GeocoderServiceError as e:
                self.logger.error(f"Geocoding service error: {e}")
                return {
                    'latitude': None,
                    'longitude': None,
                    'formatted_address': None,
                    'raw_data': None,
                    'confidence': 0,
                    'status': 'service_error',
                    'error': str(e)
                }
                
            except Exception as e:
                self.logger.error(f"Unexpected geocoding error: {e}")
                return {
                    'latitude': None,
                    'longitude': None,
                    'formatted_address': None,
                    'raw_data': None,
                    'confidence': 0,
                    'status': 'error',
                    'error': str(e)
                }
        
        # All retries failed
        return {
            'latitude': None,
            'longitude': None,
            'formatted_address': None,
            'raw_data': None,
            'confidence': 0,
            'status': 'max_retries_exceeded',
            'error': f'Failed after {self.max_retries} attempts'
        }
    
    def _calculate_confidence(self, location, original_address: str) -> float:
        """
        Calculate confidence score for geocoding result.
        
        Args:
            location: Geocoding result from Nominatim
            original_address: Original address string
            
        Returns:
            Confidence score between 0 and 1
        """
        if not location or not location.raw:
            return 0.0
        
        # Base confidence from Nominatim importance score
        importance = location.raw.get('importance', 0.5)
        base_confidence = min(importance, 1.0)
        
        # Boost confidence if address contains key Malaysian/KL terms
        address_lower = original_address.lower()
        kl_terms = ['kuala lumpur', 'kl', 'malaysia', 'jalan', 'jln']
        
        term_bonus = 0.0
        for term in kl_terms:
            if term in address_lower:
                term_bonus += 0.1
        
        # Cap the bonus
        term_bonus = min(term_bonus, 0.3)
        
        # Final confidence score
        confidence = min(base_confidence + term_bonus, 1.0)
        
        return round(confidence, 2)
    
    def batch_geocode(self, addresses: list, progress_callback=None) -> Dict[str, Dict[str, Any]]:
        """
        Geocode multiple addresses with rate limiting.
        
        Args:
            addresses: List of address strings
            progress_callback: Optional callback function for progress updates
            
        Returns:
            Dictionary mapping addresses to geocoding results
        """
        results = {}
        total = len(addresses)
        
        self.logger.info(f"Starting batch geocoding of {total} addresses")
        
        for i, address in enumerate(addresses):
            if progress_callback:
                progress_callback(i + 1, total, address)
            
            result = self.geocode_address(address)
            results[address] = result
            
            # Log progress
            if (i + 1) % 10 == 0:
                self.logger.info(f"Geocoded {i + 1}/{total} addresses")
        
        self.logger.info(f"Batch geocoding complete: {total} addresses processed")
        return results 