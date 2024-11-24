import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';



const MapComponent = ({markerData}) => {
  let mean_x = 0;
  let mean_y = 0;
  for (let i =0; i < markerData.length; ++i) {
    mean_x += markerData[i].position[0]
    mean_y += markerData[i].position[1]
  }
  mean_x /= markerData.length;
  mean_y /= markerData.length;


  const defaultPosition = [43.650515, -79.392287]; // center of Toronto



  return (
    <MapContainer center={defaultPosition} zoom={10} style={{ height: '400px', width: '50%' }}>
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
  );
};

export default MapComponent;
