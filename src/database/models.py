"""
Data models and validation for McDonald's outlets
"""
from dataclasses import dataclass
from typing import Optional, Dict, Any
import re
from datetime import datetime

@dataclass
class Outlet:
    """McDonald's outlet data model"""
    name: str
    address: str
    operating_hours: Optional[str] = None
    waze_link: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate data after initialization"""
        self.validate()
    
    def validate(self):
        """Validate outlet data"""
        if not self.name or not self.name.strip():
            raise ValueError("Outlet name cannot be empty")
        
        if not self.address or not self.address.strip():
            raise ValueError("Outlet address cannot be empty")
        
        # Clean and validate name
        self.name = self.name.strip()
        if not self.name.startswith("McDonald's"):
            # Add McDonald's prefix if not present
            if "McDonald's" not in self.name:
                self.name = f"McDonald's {self.name}"
        
        # Clean address
        self.address = self.address.strip()
        
        # Validate coordinates if provided
        if self.latitude is not None:
            if not (-90 <= self.latitude <= 90):
                raise ValueError(f"Invalid latitude: {self.latitude}")
        
        if self.longitude is not None:
            if not (-180 <= self.longitude <= 180):
                raise ValueError(f"Invalid longitude: {self.longitude}")
        
        # Validate Malaysian coordinates (rough bounds)
        if self.latitude is not None and self.longitude is not None:
            # Malaysia bounds approximately: 1°N to 7°N, 99°E to 119°E
            if not (1 <= self.latitude <= 7):
                print(f"Warning: Latitude {self.latitude} seems outside Malaysia bounds")
            if not (99 <= self.longitude <= 119):
                print(f"Warning: Longitude {self.longitude} seems outside Malaysia bounds")
        
        # Validate Waze link format
        if self.waze_link:
            if not (self.waze_link.startswith("https://waze.com") or 
                   self.waze_link.startswith("https://www.waze.com")):
                print(f"Warning: Waze link format may be invalid: {self.waze_link}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert outlet to dictionary for database insertion"""
        return {
            'name': self.name,
            'address': self.address,
            'operating_hours': self.operating_hours,
            'waze_link': self.waze_link,
            'latitude': self.latitude,
            'longitude': self.longitude
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Outlet':
        """Create outlet from dictionary"""
        return cls(
            id=data.get('id'),
            name=data['name'],
            address=data['address'],
            operating_hours=data.get('operating_hours'),
            waze_link=data.get('waze_link'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

def validate_outlet_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate raw outlet data and return cleaned version"""
    try:
        outlet = Outlet(
            name=data.get('name', ''),
            address=data.get('address', ''),
            operating_hours=data.get('operating_hours'),
            waze_link=data.get('waze_link'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude')
        )
        return outlet.to_dict()
    except ValueError as e:
        raise ValueError(f"Invalid outlet data: {str(e)}")

def clean_operating_hours(hours_text: str) -> str:
    """Clean and standardize operating hours text"""
    if not hours_text:
        return ""
    
    # Remove extra whitespace
    hours_text = re.sub(r'\s+', ' ', hours_text.strip())
    
    # Common cleaning patterns
    hours_text = hours_text.replace('–', '-')  # Replace em dash with hyphen
    hours_text = hours_text.replace('—', '-')  # Replace em dash with hyphen
    
    return hours_text

def extract_coordinates_from_waze_link(waze_link: str) -> tuple[Optional[float], Optional[float]]:
    """Extract latitude and longitude from Waze link"""
    if not waze_link:
        return None, None
    
    # Pattern for Waze coordinates: ll=latitude,longitude
    pattern = r'll=([+-]?\d+\.?\d*),([+-]?\d+\.?\d*)'
    match = re.search(pattern, waze_link)
    
    if match:
        try:
            lat = float(match.group(1))
            lon = float(match.group(2))
            return lat, lon
        except ValueError:
            return None, None
    
    return None, None 