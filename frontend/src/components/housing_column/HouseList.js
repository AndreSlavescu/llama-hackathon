import React from 'react';
import HouseItem from './HouseItem';

const HouseList = ({ houses }) => {
  return (
    <div style={styles.list}>
      {houses.map((house) => (
        <HouseItem key={house.id} house={house} />
      ))}
    </div>
  );
};

const styles = {
  list: {
    display: 'flex',
    flexDirection: 'column',
    border: '1px solid #ddd',
    borderRadius: '8px',
    overflow: 'hidden',
  },
};

export default HouseList;
