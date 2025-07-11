'use client';

import React from 'react';

interface OutletInfo {
  name: string;
  address: string;
  distance: string;
  operatingHours: string;
  wazeLink: string;
}

interface LocationCardProps {
  outlet: OutletInfo;
}

const LocationCard: React.FC<LocationCardProps> = ({ outlet }) => {
  // Debug logging
  console.log('🏪 LocationCard received outlet data:', outlet);
  console.log('🔗 Waze link present:', !!outlet.wazeLink, 'Value:', outlet.wazeLink);

  const handleWazeClick = () => {
    if (outlet.wazeLink) {
      window.open(outlet.wazeLink, '_blank', 'noopener,noreferrer');
    }
  };

  return (
    <div className="bg-white border border-gray-100 rounded-2xl shadow-lg hover:shadow-xl p-5 mb-3 last:mb-0 transition-all duration-300 ease-out backdrop-blur-sm hover:scale-[1.02]">
      {/* Header - Restaurant Name */}
      <div className="mb-4">
        <h3 className="font-bold text-lg text-transparent bg-gradient-to-r from-red-600 to-red-500 bg-clip-text leading-tight">
          {outlet.name}
        </h3>
      </div>

      {/* Information Grid */}
      <div className="space-y-4">
        {/* Address */}
        <div className="flex items-start gap-3">
          <div className="w-5 h-5 mt-0.5 flex-shrink-0">
            <svg className="w-5 h-5 text-red-500" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
            </svg>
          </div>
          <div className="flex-1">
            <p className="text-sm text-gray-700 leading-relaxed font-medium">
              {outlet.address}
            </p>
          </div>
        </div>

        {/* Distance and Hours Row */}
        <div className="flex items-center gap-6">
          {/* Distance */}
          {outlet.distance && (
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 flex-shrink-0">
                <svg className="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
                </svg>
              </div>
              <span className="text-sm font-semibold text-blue-600 bg-blue-50 px-2 py-1 rounded-full">
                {outlet.distance}
              </span>
            </div>
          )}

          {/* Operating Hours */}
          {outlet.operatingHours && (
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 flex-shrink-0">
                <svg className="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <span className="text-sm text-gray-600 font-medium">
                {outlet.operatingHours}
              </span>
            </div>
          )}
        </div>

        {/* Waze Button - Always show for debugging */}
        <div className="pt-2">
          {outlet.wazeLink ? (
            <button
              onClick={handleWazeClick}
              className="inline-flex items-center gap-2 px-4 py-2.5 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white text-sm font-semibold rounded-xl transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 shadow-md hover:shadow-lg transform hover:scale-105"
            >
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
              </svg>
              <span>Navigate with Waze</span>
            </button>
          ) : (
            <div className="text-xs text-red-500 bg-red-50 px-2 py-1 rounded">
              Debug: No Waze link found
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LocationCard; 