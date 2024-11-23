import React from 'react';

const HouseTitle = ({ title }) => {
  return (
    <h2 style={styles.title}>{title}</h2>
  );
};

const styles = {
  title: {
    fontSize: '1.2rem',
    fontWeight: '600',
    margin: '0 0 8px 0',
  },
};

export default HouseTitle;
