'use client';

import React from 'react';
import LocationButton from '../LocationButton';
import { useGeolocation } from '@/hooks/useGeolocation';

interface ChatHeaderProps {
  onClose: () => void;
  onClear?: () => void;
  chatSession?: any;
}

const ChatHeader: React.FC<ChatHeaderProps> = ({ onClose, onClear, chatSession }) => {
  const { location, getCurrentLocation, isLoading, error, permission } = useGeolocation();
  const autoLocationAttempted = React.useRef(false);
  const previousLocation = React.useRef<{lat: number, lng: number} | null>(null);

  // Track component lifecycle
  React.useEffect(() => {
    const timestamp = new Date().toISOString();
    console.log(`🏗️ [${timestamp}] ChatHeader: Component MOUNTED`);
    
    return () => {
      const timestamp = new Date().toISOString();
      console.log(`💀 [${timestamp}] ChatHeader: Component UNMOUNTING`);
    };
  }, []);

  // Track re-renders
  React.useEffect(() => {
    const timestamp = new Date().toISOString();
    console.log(`🔄 [${timestamp}] ChatHeader: Component RE-RENDERED`);
    console.log(`🔄 [${timestamp}] ChatHeader: Props - onClose:`, !!onClose, 'onClear:', !!onClear, 'chatSession:', !!chatSession);
  });

  // Handle location detection and setting (with reference equality fix)
  React.useEffect(() => {
    const timestamp = new Date().toISOString();
    console.log(`🚀 [${timestamp}] ChatHeader: Location effect triggered`);
    console.log(`🚀 [${timestamp}] ChatHeader: ChatSession:`, !!chatSession, 'Location:', location, 'Permission:', permission, 'AutoAttempted:', autoLocationAttempted.current);
    
    if (!chatSession) {
      // Reset flags when chat session is not available
      autoLocationAttempted.current = false;
      previousLocation.current = null;
      return;
    }
    
    // Check if location actually changed (compare values, not object reference)
    const locationChanged = location && (
      !previousLocation.current || 
      previousLocation.current.lat !== location.lat || 
      previousLocation.current.lng !== location.lng
    );
    
    // If we have a new location that actually changed, set it in chat session
    if (locationChanged) {
      console.log(`📍 [${timestamp}] ChatHeader: Location changed, updating chat session:`, location);
      console.log(`📍 [${timestamp}] ChatHeader: Previous:`, previousLocation.current, 'New:', location);
      previousLocation.current = { lat: location.lat, lng: location.lng };
      chatSession.setUserLocation(location);
      return;
    }
    
    // Try to get location automatically (only once per session)
    if (!location && !autoLocationAttempted.current && !isLoading && permission !== 'denied') {
      autoLocationAttempted.current = true;
      console.log(`🚀 [${timestamp}] ChatHeader: Automatically requesting location...`);
      
      getCurrentLocation()
        .then((detectedLocation) => {
          const timestamp = new Date().toISOString();
          console.log(`🚀 [${timestamp}] ChatHeader: Auto-location successful:`, detectedLocation);
          // Location state will update and trigger this effect again with the new location
        })
        .catch((error) => {
          const timestamp = new Date().toISOString();
          console.log(`🚀 [${timestamp}] ChatHeader: Auto-location failed:`, error.message);
        });
    } else if (location) {
      console.log(`🚀 [${timestamp}] ChatHeader: Location already set, no action needed`);
    } else {
      console.log(`🚀 [${timestamp}] ChatHeader: Skipping auto-location - conditions not met`);
    }
  }, [chatSession, location?.lat, location?.lng, permission]); // Depend on primitive values to avoid reference equality issues

  return (
    <div className="bg-red-600 text-white px-6 py-4 rounded-t-2xl shadow-sm">
      <div className="flex items-center justify-between">
        {/* Left Section: Text Only */}
        <div>
          <h3 className="font-semibold text-lg leading-tight">
            McD Assistant
          </h3>
        </div>
        
        {/* Right Section: Location and Close Buttons */}
        <div className="flex items-center gap-2">
          {/* Location Button */}
          <LocationButton 
            variant="minimal" 
            size="small" 
            showStatus={true}
            className="text-white hover:bg-red-700 focus:ring-red-300 border border-red-500 rounded-lg transition-colors"
          />
          
          {/* Close Button */}
          <button
            onClick={onClose}
            className="p-2 hover:bg-red-700 rounded-lg transition-colors"
            title="Close chat"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatHeader; 