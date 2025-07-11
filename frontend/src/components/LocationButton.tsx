import React from 'react';
import { useGeolocation } from '../hooks/useGeolocation';
import { useChatSession } from '../hooks/useChatSession';

interface LocationButtonProps {
  variant?: 'primary' | 'secondary' | 'minimal';
  size?: 'small' | 'medium' | 'large';
  showStatus?: boolean;
  className?: string;
}

const LocationButton: React.FC<LocationButtonProps> = ({
  variant = 'secondary',
  size = 'medium',
  showStatus = true,
  className = '',
}) => {
  const { 
    location, 
    isLoading, 
    error, 
    isSupported, 
    permission,
    getCurrentLocation,
    clearError 
  } = useGeolocation();
  
  const { setUserLocation } = useChatSession();

  const handleGetLocation = async () => {
    try {
      clearError();
      const userLocation = await getCurrentLocation();
      if (userLocation) {
        setUserLocation(userLocation);
      }
    } catch (error) {
      console.error('Failed to get location:', error);
    }
  };

  const getButtonText = () => {
    if (isLoading) return 'Getting Location...';
    if (location) return 'Location Enabled';
    if (permission === 'denied') return 'Location Denied';
    return 'Enable Location';
  };

  const getButtonIcon = () => {
    if (isLoading) {
      return (
        <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
      );
    }

    if (location) {
      return (
        <svg className="h-4 w-4 text-green-500" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" />
        </svg>
      );
    }

    if (permission === 'denied') {
      return (
        <svg className="h-4 w-4 text-red-500" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" />
          <path d="M2 2l20 20" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
        </svg>
      );
    }

    return (
      <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 24 24">
        <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" />
      </svg>
    );
  };

  const getVariantClasses = () => {
    const baseClasses = 'inline-flex items-center justify-center font-medium rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2';
    
    switch (variant) {
      case 'primary':
        return `${baseClasses} bg-red-600 text-white hover:bg-red-700 focus:ring-red-500 disabled:bg-red-300`;
      case 'secondary':
        return `${baseClasses} bg-gray-100 text-gray-900 hover:bg-gray-200 focus:ring-gray-500 disabled:bg-gray-50 disabled:text-gray-400`;
      case 'minimal':
        return `${baseClasses} text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:ring-gray-500 disabled:text-gray-400`;
      default:
        return `${baseClasses} bg-gray-100 text-gray-900 hover:bg-gray-200 focus:ring-gray-500`;
    }
  };

  const getSizeClasses = () => {
    switch (size) {
      case 'small':
        return 'px-2 py-1 text-xs gap-1';
      case 'medium':
        return 'px-3 py-2 text-sm gap-2';
      case 'large':
        return 'px-4 py-3 text-base gap-2';
      default:
        return 'px-3 py-2 text-sm gap-2';
    }
  };

  if (!isSupported) {
    return (
      <div className="text-sm text-gray-500">
        Location not supported
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-1">
      <button
        onClick={handleGetLocation}
        disabled={isLoading || permission === 'denied'}
        className={`${getVariantClasses()} ${getSizeClasses()} ${className}`}
        title={
          permission === 'denied' 
            ? 'Location access denied. Please enable location permissions in your browser settings.'
            : 'Get your current location to find nearby McDonald\'s outlets'
        }
      >
        {getButtonIcon()}
        <span>{getButtonText()}</span>
      </button>

      {showStatus && error && (
        <div className="text-xs text-red-600 max-w-xs">
          {error}
        </div>
      )}

      {/* Removed location coordinates display */}
    </div>
  );
};

export default LocationButton; 