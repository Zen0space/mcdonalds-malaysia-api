import { useState, useCallback, useEffect } from 'react';
import { UserLocation } from '../types/chat';
import React from 'react';

export interface GeolocationState {
  location: UserLocation | null;
  isLoading: boolean;
  error: string | null;
  isSupported: boolean;
  permission: 'granted' | 'denied' | 'prompt' | 'unknown';
}

export interface GeolocationOptions {
  enableHighAccuracy?: boolean;
  timeout?: number;
  maximumAge?: number;
}

const DEFAULT_OPTIONS: GeolocationOptions = {
  enableHighAccuracy: true,
  timeout: 10000, // 10 seconds
  maximumAge: 300000, // 5 minutes
};

export const useGeolocation = (options: GeolocationOptions = DEFAULT_OPTIONS) => {
  // Track hook initialization
  const hookId = React.useRef(Math.random().toString(36).substr(2, 9));
  React.useEffect(() => {
    const timestamp = new Date().toISOString();
    console.log(`🪝 [${timestamp}] useGeolocation: Hook INITIALIZED with ID:`, hookId.current);
    
    return () => {
      const timestamp = new Date().toISOString();
      console.log(`🪝 [${timestamp}] useGeolocation: Hook DESTROYED with ID:`, hookId.current);
    };
  }, []);

  const [state, setState] = useState<GeolocationState>({
    location: null,
    isLoading: false,
    error: null,
    isSupported: 'geolocation' in navigator,
    permission: 'unknown',
  });

  // Wrapper for setState to track all state changes
  const setStateWithLogging = useCallback((newState: GeolocationState | ((prev: GeolocationState) => GeolocationState)) => {
    const timestamp = new Date().toISOString();
    const stack = new Error().stack;
    console.log(`🪝 [${timestamp}] useGeolocation [${hookId.current}]: setState called from:`, stack?.split('\n')[2]?.trim());
    console.log(`🪝 [${timestamp}] useGeolocation [${hookId.current}]: setState with:`, typeof newState === 'function' ? 'function' : newState);
    setState(newState);
  }, []);

  // Track state changes
  React.useEffect(() => {
    const timestamp = new Date().toISOString();
    console.log(`🪝 [${timestamp}] useGeolocation [${hookId.current}]: State changed:`, {
      location: state.location,
      isLoading: state.isLoading,
      error: state.error,
      permission: state.permission
    });
  }, [state]);

  // Check permission status on mount
  useEffect(() => {
    const checkPermission = async () => {
      if (!('permissions' in navigator)) {
        return;
      }

      try {
        const result = await navigator.permissions.query({ name: 'geolocation' });
        setStateWithLogging(prev => ({ ...prev, permission: result.state }));
        
        // Listen for permission changes
        result.addEventListener('change', () => {
          setStateWithLogging(prev => ({ ...prev, permission: result.state }));
        });
      } catch (error) {
        console.warn('Could not check geolocation permission:', error);
      }
    };

    checkPermission();
  }, []);

  const getCurrentLocation = useCallback(async (): Promise<UserLocation | null> => {
    const timestamp = new Date().toISOString();
    console.log(`🌍 [${timestamp}] useGeolocation: getCurrentLocation called`);
    
    if (!state.isSupported) {
      const error = 'Geolocation is not supported by this browser';
      console.log(`🌍 [${timestamp}] useGeolocation: Error - geolocation not supported`);
      setStateWithLogging(prev => ({ ...prev, error }));
      throw new Error(error);
    }

    console.log(`🌍 [${timestamp}] useGeolocation: Starting location request...`);
    setStateWithLogging(prev => ({ ...prev, isLoading: true, error: null }));

    return new Promise((resolve, reject) => {
      const successHandler = (position: GeolocationPosition) => {
        const timestamp = new Date().toISOString();
        const location: UserLocation = {
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        };

        console.log(`🌍 [${timestamp}] useGeolocation: Location detected successfully:`, location);
        console.log(`🌍 [${timestamp}] useGeolocation: Accuracy: ${position.coords.accuracy}m`);

        setStateWithLogging(prev => ({
          ...prev,
          location,
          isLoading: false,
          error: null,
          permission: 'granted',
        }));

        console.log(`🌍 [${timestamp}] useGeolocation: State updated with new location`);
        resolve(location);
      };

      const errorHandler = (error: GeolocationPositionError) => {
        let errorMessage: string;
        let permission: 'granted' | 'denied' | 'prompt' | 'unknown' = 'unknown';

        switch (error.code) {
          case error.PERMISSION_DENIED:
            errorMessage = 'Location access denied. Please enable location permissions to find nearby McDonald\'s outlets.';
            permission = 'denied';
            break;
          case error.POSITION_UNAVAILABLE:
            errorMessage = 'Location information is unavailable. Please check your device\'s location settings.';
            break;
          case error.TIMEOUT:
            errorMessage = 'Location request timed out. Please try again.';
            break;
          default:
            errorMessage = 'An unknown error occurred while retrieving location.';
            break;
        }

        setStateWithLogging(prev => ({
          ...prev,
          isLoading: false,
          error: errorMessage,
          permission,
        }));

        reject(new Error(errorMessage));
      };

      navigator.geolocation.getCurrentPosition(
        successHandler,
        errorHandler,
        {
          enableHighAccuracy: options.enableHighAccuracy,
          timeout: options.timeout,
          maximumAge: options.maximumAge,
        }
      );
    });
  }, [state.isSupported, options]);

  const clearLocation = useCallback(() => {
    setStateWithLogging(prev => ({
      ...prev,
      location: null,
      error: null,
    }));
  }, []);

  const clearError = useCallback(() => {
    setStateWithLogging(prev => ({ ...prev, error: null }));
  }, []);

  return {
    ...state,
    getCurrentLocation,
    clearLocation,
    clearError,
  };
}; 