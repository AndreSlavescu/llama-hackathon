import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';

const MapComponent = ({ markerData }) => {
  const defaultPosition = [43.650515, -79.392287]; // center of Toronto

  return (
    <div className="relative w-full h-full" style={{ zIndex: 0 }}>
      <MapContainer 
        center={defaultPosition} 
        zoom={10} 
        className="w-full h-full"
        style={{ height: '100vh' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
          url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
        />  

        {markerData.map((marker, index) => (
          <Marker key={index} position={marker.position}>
            <Popup>{marker.popup}</Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};

export default MapComponent;