/**
 * Distance calculation utilities for geolocation
 */

/**
 * Calculate the distance between two coordinates using the Haversine formula
 * @param lat1 - Latitude of first point
 * @param lon1 - Longitude of first point
 * @param lat2 - Latitude of second point
 * @param lon2 - Longitude of second point
 * @returns Distance in meters
 */
export function calculateDistance(lat1: number, lon1: number, lat2: number, lon2: number): number {
  const R = 6371e3; // Earth's radius in meters
  const φ1 = lat1 * Math.PI / 180; // φ, λ in radians
  const φ2 = lat2 * Math.PI / 180;
  const Δφ = (lat2 - lat1) * Math.PI / 180;
  const Δλ = (lon2 - lon1) * Math.PI / 180;

  const a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
            Math.cos(φ1) * Math.cos(φ2) *
            Math.sin(Δλ/2) * Math.sin(Δλ/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

  return R * c; // Distance in meters
}

/**
 * Convert kilometers to meters
 * @param km - Distance in kilometers
 * @returns Distance in meters
 */
export function kmToMeters(km: number): number {
  return km * 1000;
}

/**
 * Convert meters to kilometers
 * @param meters - Distance in meters
 * @returns Distance in kilometers
 */
export function metersToKm(meters: number): number {
  return meters / 1000;
}

/**
 * Check if two coordinates are within a certain radius
 * @param lat1 - Latitude of first point
 * @param lon1 - Longitude of first point
 * @param lat2 - Latitude of second point
 * @param lon2 - Longitude of second point
 * @param radiusMeters - Radius in meters
 * @returns True if points are within radius
 */
export function isWithinRadius(
  lat1: number, 
  lon1: number, 
  lat2: number, 
  lon2: number, 
  radiusMeters: number
): boolean {
  const distance = calculateDistance(lat1, lon1, lat2, lon2);
  return distance <= radiusMeters;
}

/**
 * Format distance for display
 * @param meters - Distance in meters
 * @returns Formatted distance string
 */
export function formatDistance(meters: number): string {
  if (meters < 1000) {
    return `${Math.round(meters)}m`;
  } else {
    return `${(meters / 1000).toFixed(1)}km`;
  }
}

/**
 * Map configuration constants
 */
export const MAP_CONFIG = {
  center: [3.139, 101.6869] as [number, number], // Kuala Lumpur center
  zoom: 11,
  minZoom: 10,
  maxZoom: 18,
  radius: 5000, // 5KM in meters
}; 