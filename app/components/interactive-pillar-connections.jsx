import React, { useState } from 'react';

const InteractivePillarConnections = () => {
  const [activePillar, setActivePillar] = useState(null);
  const [activeConnection, setActiveConnection] = useState(null);

  const pillars = {
    pbc: {
      title: "Place-based Conditions",
      color: "#0d6efd",
      x: 150,
      y: 200
    },
    hsc: {
      title: "Human & Social Capital",
      color: "#198754",
      x: 400,
      y: 200
    },
    ea: {
      title: "Economic Activity",
      color: "#dc3545",
      x: 650,
      y: 200
    }
  };

  const connections = {
    "pbc-hsc": {
      from: "pbc",
      to: "hsc",
      examples: [
        "Institutional infrastructure enables skills development",
        "Digital infrastructure supports network formation",
        "Essential services access influences human capital",
        "Transport enables network building"
      ]
    },
    "hsc-pbc": {
      from: "hsc",
      to: "pbc",
      examples: [
        "Social engagement affects institutional effectiveness",
        "Network capital influences infrastructure use",
        "Human capital drives service demands",
        "Educational foundation shapes digital adoption"
      ]
    },
    "pbc-ea": {
      from: "pbc",
      to: "ea",
      examples: [
        "Infrastructure quality determines productivity",
        "Essential services enable business operations",
        "Digital infrastructure supports markets",
        "Transport affects market access"
      ]
    },
    "ea-pbc": {
      from: "ea",
      to: "pbc",
      examples: [
        "Economic base determines infrastructure investment",
        "Market dynamics influence service provision",
        "Business environment shapes institutions",
        "Labour market affects transport demand"
      ]
    },
    "hsc-ea": {
      from: "hsc",
      to: "ea",
      examples: [
        "Educational attainment affects productivity",
        "Network structure influences job matching",
        "Skills development shapes labour markets",
        "Social cohesion impacts economic resilience"
      ]
    },
    "ea-hsc": {
      from: "ea",
      to: "hsc",
      examples: [
        "Employment structure affects education choices",
        "Market dynamics shape network formation",
        "Income security influences social engagement",
        "Economic opportunity affects institutional trust"
      ]
    }
  };

  const generatePath = (fromPillar, toPillar, isTop) => {
    const offset = isTop ? -50 : 50;
    return `M ${pillars[fromPillar].x} ${pillars[fromPillar].y} 
            C ${(pillars[fromPillar].x + pillars[toPillar].x) / 2} ${pillars[fromPillar].y + offset} 
              ${(pillars[fromPillar].x + pillars[toPillar].x) / 2} ${pillars[toPillar].y + offset} 
              ${pillars[toPillar].x} ${pillars[toPillar].y}`;
  };

  return (
    <div className="w-full max-w-6xl mx-auto">
      <div className="relative">
        <svg width="800" height="400" className="mx-auto">
          {/* Connection Paths */}
          {Object.entries(connections).map(([key, connection]) => {
            const isTop = key.includes('pbc-hsc') || key.includes('hsc-ea') || key.includes('pbc-ea');
            return (
              <path
                key={key}
                d={generatePath(connection.from, connection.to, isTop)}
                stroke={activeConnection === key ? '#000' : '#ccc'}
                strokeWidth={activeConnection === key ? 3 : 2}
                fill="none"
                className="transition-all duration-300"
                onMouseEnter={() => setActiveConnection(key)}
                onMouseLeave={() => setActiveConnection(null)}
                style={{cursor: 'pointer'}}
              />
            );
          })}

          {/* Pillar Nodes */}
          {Object.entries(pillars).map(([key, pillar]) => (
            <g key={key} 
               transform={`translate(${pillar.x - 60}, ${pillar.y - 30})`}
               onMouseEnter={() => setActivePillar(key)}
               onMouseLeave={() => setActivePillar(null)}
               style={{cursor: 'pointer'}}>
              <rect
                width="120"
                height="60"
                rx="8"
                fill={pillar.color}
                className={`transition-all duration-300 ${activePillar === key ? 'opacity-100' : 'opacity-75'}`}
              />
              <text
                x="60"
                y="35"
                textAnchor="middle"
                fill="white"
                className="text-sm font-semibold">
                {pillar.title}
              </text>
            </g>
          ))}
        </svg>

        {/* Connection Details Panel */}
        {activeConnection && (
          <div className="absolute top-0 right-0 w-64 p-4 bg-white shadow-lg rounded-lg">
            <h4 className="text-lg font-semibold mb-2">Key Linkages</h4>
            <ul className="text-sm space-y-2">
              {connections[activeConnection].examples.map((example, i) => (
                <li key={i} className="text-gray-600">{example}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default InteractivePillarConnections;
