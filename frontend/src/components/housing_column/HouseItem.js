import React, { useState, useEffect } from 'react';
import HouseTitle from './HouseTitle';
import { FaBed, FaBath, FaRulerCombined, FaChevronDown, FaChevronUp } from 'react-icons/fa';
import SlideshowModal from './SlideshowModal';

const HouseItem = ({ house }) => {
  const { id, address, price, sqft, description } = house;
  const [isExpanded, setIsExpanded] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [images, setImages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const fetchImages = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await fetch(`http://127.0.0.1:8000/${id}/images`);
        if (!response.ok) {
          throw new Error(`Error fetching images: ${response.statusText}`);
        }
        const data = await response.json();
        console.log(data, " debugging line for data of images")
        setImages(data); // Assuming the backend returns { images: [url1, url2, ...] }
      } catch (err) {
        console.error(err);
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchImages();
  }, [id]);

  const toggleExpand = () => {
    setIsExpanded((prev) => !prev);
  };

  const openModal = (e) => {
    e.stopPropagation();
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  return (
    <div
      style={{
        ...styles.container,
        flexDirection: 'column',
        cursor: description ? 'pointer' : 'default',
      }}
      onClick={description && !isModalOpen ? toggleExpand : null}
    >
      <div style={styles.header}>
        <img
          src={images[0]}
          alt={address}
          style={styles.thumbnail}
          onClick={openModal}
        />
        <div style={styles.details}>
          <HouseTitle title={address} />
          <p style={styles.price}>${price.toLocaleString()}</p>
          <div style={styles.info}>
            {/* <div style={styles.infoItem}>
              <FaBed style={styles.icon} />
              <span>{bedrooms} Beds</span>
            </div>
            <div style={styles.infoItem}>
              <FaBath style={styles.icon} />
              <span>{bathrooms} Baths</span>
            </div> */}
            <div style={styles.infoItem}>
              <FaRulerCombined style={styles.icon} />
              <span>{sqft} sqft</span>
            </div>
          </div>
        </div>
        {description && (
          <div
            style={styles.arrowContainer}
            onClick={(e) => {
              e.stopPropagation();
              if (!isModalOpen) toggleExpand();
            }}
          >
            {isExpanded ? (
              <FaChevronUp style={styles.arrow} />
            ) : (
              <FaChevronDown style={styles.arrow} />
            )}
          </div>
        )}
      </div>
      {isExpanded && (
        <div style={styles.expandedContent}>
          <p style={styles.description}>
  {description.split('\\n').map((line, index) => (
    <span key={index}>
      {line}
      <br />
    </span>
  ))}
</p>
        </div>
      )}
      <SlideshowModal
        isOpen={isModalOpen}
        onRequestClose={closeModal}
        images={images}
      />
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    padding: '16px',
    borderBottom: '1px solid #ddd',
    alignItems: 'center',
    transition: 'all 0.3s ease',
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    width: '100%',
  },
  thumbnail: {
    width: '120px',
    height: '90px',
    objectFit: 'cover',
    borderRadius: '8px',
    marginRight: '16px',
    cursor: 'pointer',
    transition: 'transform 0.2s',
  },
  details: {
    flex: 1,
  },
  price: {
    fontSize: '1rem',
    color: '#2ecc71',
    margin: '4px 0 12px 0',
  },
  info: {
    display: 'flex',
    gap: '16px',
  },
  infoItem: {
    display: 'flex',
    alignItems: 'center',
    fontSize: '0.9rem',
    color: '#555',
  },
  icon: {
    width: '16px',
    height: '16px',
    marginRight: '4px',
  },
  expandedContent: {
    marginTop: '12px',
    paddingTop: '12px',
    borderTop: '1px solid #eee',
    width: '100%',
    textAlign: 'left',
  },
  description: {
    fontSize: '0.95rem',
    color: '#333',
  },
  arrowContainer: {
    marginLeft: '16px',
    display: 'flex',
    alignItems: 'center',
    cursor: 'pointer',
  },
  arrow: {
    width: '20px',
    height: '20px',
    color: '#2ecc71',
  },
};

export default HouseItem;
