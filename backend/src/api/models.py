"""
Pydantic models for McDonald's Malaysia API responses.
Clean, comprehensive models for all API endpoints.
"""

from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, Field, validator


class OutletBase(BaseModel):
    """Base outlet model with common fields."""
    
    id: int = Field(..., description="Unique outlet identifier")
    name: str = Field(..., description="Outlet name")
    address: str = Field(..., description="Full address")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class OutletResponse(OutletBase):
    """Complete outlet response model."""
    
    operating_hours: Optional[str] = Field(None, description="Operating hours")
    waze_link: Optional[str] = Field(None, description="Waze navigation link")
    latitude: Optional[float] = Field(None, description="Latitude coordinate")
    longitude: Optional[float] = Field(None, description="Longitude coordinate")
    features: List[str] = Field(default_factory=list, description="Outlet features")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime = Field(..., description="Record update timestamp")
    
    @validator('latitude')
    def validate_latitude(cls, v):
        if v is not None and not (1.0 <= v <= 7.0):
            raise ValueError('Latitude must be within Malaysia bounds (1.0 to 7.0)')
        return v
    
    @validator('longitude')
    def validate_longitude(cls, v):
        if v is not None and not (99.0 <= v <= 119.0):
            raise ValueError('Longitude must be within Malaysia bounds (99.0 to 119.0)')
        return v

    class Config:
        """Pydantic configuration."""
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class OutletListResponse(BaseModel):
    """Response model for outlet list with pagination."""
    
    outlets: List[OutletResponse] = Field(..., description="List of outlets")
    total: int = Field(..., description="Total number of outlets")
    limit: int = Field(..., description="Number of outlets per page")
    offset: int = Field(..., description="Offset for pagination")
    has_more: bool = Field(..., description="Whether more outlets are available")


class NearbyOutletResponse(OutletResponse):
    """Response model for nearby outlet with distance."""
    
    distance_km: float = Field(..., description="Distance from search point in kilometers")


class NearbySearchResponse(BaseModel):
    """Response model for nearby outlet search."""
    
    outlets: List[NearbyOutletResponse] = Field(..., description="List of nearby outlets")
    center: dict = Field(..., description="Search center coordinates")
    radius_km: float = Field(..., description="Search radius in kilometers")
    total_found: int = Field(..., description="Number of outlets found")


class StatsResponse(BaseModel):
    """Response model for database statistics."""
    
    total_outlets: int = Field(..., description="Total number of outlets")
    outlets_with_coordinates: int = Field(..., description="Outlets with GPS coordinates")
    outlets_with_waze_links: int = Field(..., description="Outlets with Waze links")
    last_updated: Optional[datetime] = Field(None, description="Last database update")
    coverage_areas: List[str] = Field(default_factory=list, description="Covered areas")
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class HealthResponse(BaseModel):
    """Response model for health check."""
    
    status: str = Field(..., description="API status")
    database_connected: bool = Field(..., description="Database connection status")
    total_outlets: int = Field(..., description="Total outlets in database")
    timestamp: datetime = Field(..., description="Current timestamp")
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class APIInfoResponse(BaseModel):
    """Response model for API information."""
    
    name: str = Field(..., description="API name")
    version: str = Field(..., description="API version")
    description: str = Field(..., description="API description")
    docs_url: str = Field(..., description="Documentation URL")
    total_outlets: int = Field(..., description="Total outlets available")
    coverage: str = Field(..., description="Geographic coverage")


class ErrorResponse(BaseModel):
    """Response model for API errors."""
    
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Any] = Field(None, description="Additional error details")
    timestamp: datetime = Field(..., description="Error timestamp")
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 