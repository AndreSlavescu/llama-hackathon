import React, { useState } from 'react';
import Map from './Map';
import Chat from './Chat';
import HouseList from './housing_column/HouseList';

const LLMContainer = () => {
  const [markerData, setMarkerData] = useState([]);
  const [isChatOpen, setIsChatOpen] = useState(false);

  const sampleHouses = [
    {
      id: 1,
      images: [
        'https://i.imgur.com/Vbphqpb.jpeg',
        'https://i.imgur.com/tnIsaCN.jpeg',
        'https://via.placeholder.com/600x400?text=House+1+Image+3',
      ],
      title: 'Modern Family Home',
      price: 350000,
      bedrooms: 4,
      bathrooms: 3,
      squareFeet: 2500,
      description:
        'A beautiful modern family home located in a serene neighborhood with spacious gardens and contemporary amenities.',
    },
    {
      id: 2,
      images: [
        'https://via.placeholder.com/600x400?text=House+2+Image+1',
        'https://via.placeholder.com/600x400?text=House+2+Image+2',
      ],
      title: 'Cozy Cottage',
      price: 200000,
      bedrooms: 2,
      bathrooms: 1,
      squareFeet: 1200,
      description: '',
    },
  ];

  return (
    <div className="flex h-screen bg-slate-100">
      {/* Left Sidebar - House Listings */}
      <div className="w-96 bg-white shadow-lg overflow-y-auto z-20">
        <div className="p-4 border-b border-slate-200">
          <h2 className="text-xl font-semibold text-slate-800">Available Properties</h2>
        </div>
        <div className="p-4">
          <HouseList houses={sampleHouses} />
        </div>
      </div>

      {/* Main Content Area - Full Map */}
      <div className="flex-1 relative">
        <Map markerData={markerData} />
        
        {/* Floating Chat Widget */}
        <div className="fixed bottom-6 right-6" style={{ zIndex: 1000 }}>
          <div className={`bg-white rounded-lg shadow-xl transition-all duration-300 ${
            isChatOpen ? 'w-96 h-[500px]' : 'w-14 h-14'
          }`}>
            {isChatOpen ? (
              <div className="h-full flex flex-col">
                <div className="p-3 border-b border-slate-200 flex justify-between items-center bg-white rounded-t-lg">
                  <h3 className="font-semibold">Chat Assistant</h3>
                  <button 
                    onClick={() => setIsChatOpen(false)}
                    className="p-1 hover:bg-slate-100 rounded-full"
                  >
                    ✕
                  </button>
                </div>
                <div className="flex-1 overflow-hidden bg-white">
                  <Chat />
                </div>
              </div>
            ) : (
              <button
                onClick={() => setIsChatOpen(true)}
                className="w-full h-full flex items-center justify-center bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
              >
                💬
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LLMContainer;