import React, { useState } from 'react';
import Map from './Map';
import Chat from './Chat';
import HouseList from './housing_column/HouseList';

const LLMContainer = (props) => {
  const [markerData, setMarkerData] = useState([]);

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
      description:
        '',
    },
    
  ];

  return (
    <div style={styles.container}>
      <div style={styles.column}>
        <HouseList houses={sampleHouses} />
      </div>
      <div style={styles.secondary}>
        <Chat />
        <Map style={{ width: '200px' }} markerData={markerData} />
      </div>
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'row',
    padding: '20px',
    gap: '20px',
    height: '100vh',
    boxSizing: 'border-box',
  },
  column: {
    flex: '0 0 600px',
    overflowY: 'auto',
    maxHeight: '100%',
  },
  secondary: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    gap: '20px',
    overflowY: 'auto',
  },
};

export default LLMContainer;
