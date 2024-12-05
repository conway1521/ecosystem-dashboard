import React from 'react';
import { Card, CardHeader, CardTitle, CardBody } from '@/components/ui/card';

const PillarConnections = () => {
  const [hoveredConnection, setHoveredConnection] = React.useState(null);

  // Define the connections between pillars
  const connections = [
    {
      id: 'pbc-hsc-1',
      from: { pillar: 'pbc', item: 'Institutional Infrastructure' },
      to: { pillar: 'hsc', item: 'Human Capital Development' },
      description: 'Institutional infrastructure enables educational attainment and skills development'
    },
    {
      id: 'pbc-ea-1',
      from: { pillar: 'pbc', item: 'Essential Services' },
      to: { pillar: 'ea', item: 'Economic Base' },
      description: 'Essential services enable business operations and market functioning'
    },
    // Add more connections as needed
  ];

  return (
    <div className="w-full max-w-7xl mx-auto p-4">
      <div className="relative flex justify-between items-stretch min-h-[600px]">
        {/* Place-based Conditions Pillar */}
        <Card className="w-1/3 border-primary border-2">
          <CardHeader>
            <CardTitle>Place-based Conditions</CardTitle>
          </CardHeader>
          <CardBody className="space-y-4">
            <div className="p-2 border rounded">Institutional Infrastructure</div>
            <div className="p-2 border rounded">Essential Services</div>
            <div className="p-2 border rounded">Digital Infrastructure</div>
          </CardBody>
        </Card>

        {/* Human & Social Capital Pillar */}
        <Card className="w-1/3 mx-4 border-success border-2">
          <CardHeader>
            <CardTitle>Human & Social Capital</CardTitle>
          </CardHeader>
          <CardBody className="space-y-4">
            <div className="p-2 border rounded">Human Capital Development</div>
            <div className="p-2 border rounded">Network Capital</div>
            <div className="p-2 border rounded">Social Engagement</div>
          </CardBody>
        </Card>

        {/* Economic Activity Pillar */}
        <Card className="w-1/3 border-danger border-2">
          <CardHeader>
            <CardTitle>Economic Activity</CardTitle>
          </CardHeader>
          <CardBody className="space-y-4">
            <div className="p-2 border rounded">Economic Base</div>
            <div className="p-2 border rounded">Labour Market</div>
            <div className="p-2 border rounded">Household Resources</div>
          </CardBody>
        </Card>

        {/* SVG Overlay for Arrows */}
        <svg 
          className="absolute top-0 left-0 w-full h-full pointer-events-none"
          style={{ zIndex: 10 }}
        >
          {connections.map((connection) => (
            <g key={connection.id}>
              <path
                d="M100 100 L300 150"
                stroke={hoveredConnection === connection.id ? '#000' : '#666'}
                strokeWidth={hoveredConnection === connection.id ? 2 : 1}
                fill="none"
                className="cursor-pointer"
                onMouseEnter={() => setHoveredConnection(connection.id)}
                onMouseLeave={() => setHoveredConnection(null)}
              />
              {hoveredConnection === connection.id && (
                <foreignObject x="150" y="75" width="200" height="100">
                  <div className="bg-white p-2 rounded shadow text-sm">
                    {connection.description}
                  </div>
                </foreignObject>
              )}
            </g>
          ))}
        </svg>
      </div>
    </div>
  );
};

export default PillarConnections;
