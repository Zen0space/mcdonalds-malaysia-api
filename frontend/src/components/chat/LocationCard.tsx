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
  const handleWazeClick = () => {
    if (outlet.wazeLink) {
      window.open(outlet.wazeLink, '_blank', 'noopener,noreferrer');
    }
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg shadow-sm p-4 mb-3 last:mb-0">
      {/* Header - Restaurant Name */}
      <div className="mb-3">
        <h3 className="font-semibold text-lg text-red-600 leading-tight">
          {outlet.name}
        </h3>
      </div>

      {/* Information Grid */}
      <div className="space-y-3">
        {/* Address */}
        <div className="flex items-start gap-2">
          <div className="w-4 h-4 mt-0.5 flex-shrink-0">
            <svg className="w-4 h-4 text-gray-500" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
            </svg>
          </div>
          <div className="flex-1">
            <p className="text-sm text-gray-700 leading-relaxed">
              {outlet.address}
            </p>
          </div>
        </div>

        {/* Distance and Hours Row */}
        <div className="flex items-center gap-4">
          {/* Distance */}
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 flex-shrink-0">
              <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
              </svg>
            </div>
            <span className="text-sm font-medium text-gray-700">
              {outlet.distance}
            </span>
          </div>

          {/* Operating Hours */}
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 flex-shrink-0">
              <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <span className="text-sm text-gray-600">
              {outlet.operatingHours}
            </span>
          </div>
        </div>

        {/* Waze Button */}
        {outlet.wazeLink && (
          <div className="pt-2">
            <button
              onClick={handleWazeClick}
              className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
              </svg>
              <span>Waze</span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default LocationCard; 