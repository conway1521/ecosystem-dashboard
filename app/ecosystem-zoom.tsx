import React, { useState } from 'react';
import { ChevronDown, ChevronRight, ZoomIn, ZoomOut, ArrowLeft } from 'lucide-react';

const ZoomableEcosystem = () => {
  const [zoomedPillar, setZoomedPillar] = useState(null);
  const [expandedPillars, setExpandedPillars] = useState({
    pbc: false,
    hsc: false,
    ea: false
  });

  const handleZoom = (pillar) => {
    setZoomedPillar(pillar);
  };

  const handleZoomOut = () => {
    setZoomedPillar(null);
  };

  const getPillarPosition = (pillarKey) => {
    const positions = {
      pbc: 'translate-y-[-50%]',
      hsc: 'translate-x-[-50%] translate-y-[50%]',
      ea: 'translate-x-[50%] translate-y-[50%]'
    };
    return positions[pillarKey] || '';
  };

  const togglePillar = (pillar) => {
    setExpandedPillars(prev => ({
      ...prev,
      [pillar]: !prev[pillar]
    }));
  };

  return (
    <div className="h-screen w-full relative overflow-hidden bg-gray-50">
      {/* Navigation */}
      {zoomedPillar && (
        <button
          onClick={handleZoomOut}
          className="absolute top-4 left-4 z-50 flex items-center gap-2 px-4 py-2 bg-white rounded-lg shadow hover:bg-gray-50"
        >
          <ArrowLeft size={20} />
          Back to Overview
        </button>
      )}

      {/* Ecosystem Container */}
      <div className={`
        absolute inset-0 transition-transform duration-700 ease-in-out
        ${zoomedPillar ? 'scale-150' : 'scale-100'}
      `}>
        {/* Central Circle */}
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full border-2 border-gray-200">
          {/* Pillars */}
          {Object.entries(pillarsData).map(([key, data]) => {
            const isZoomed = zoomedPillar === key;
            const isFaded = zoomedPillar && zoomedPillar !== key;
            
            return (
              <div
                key={key}
                className={`
                  absolute top-1/2 left-1/2 transform -translate-x-1/2 
                  ${getPillarPosition(key)}
                  transition-all duration-700 ease-in-out
                  ${isFaded ? 'opacity-20 scale-75' : ''}
                  ${isZoomed ? 'scale-150' : ''}
                `}
              >
                <div 
                  className={`
                    transform transition-transform duration-700
                    ${isZoomed ? 'scale-125' : 'hover:scale-105'}
                  `}
                >
                  <div 
                    className="cursor-pointer"
                    onClick={() => !zoomedPillar && handleZoom(key)}
                  >
                    <Pillar
                      {...data}
                      expanded={expandedPillars[key]}
                      onToggle={() => togglePillar(key)}
                    />
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

// Reuse the Pillar, Subject, and Component components from before
// [Previous component definitions here]

export default ZoomableEcosystem;
