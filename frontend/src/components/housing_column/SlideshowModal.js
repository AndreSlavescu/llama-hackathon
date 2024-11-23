import React, { useRef, useEffect } from 'react';
import Modal from 'react-modal';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

Modal.setAppElement('#root');

const SlideshowModal = ({ isOpen, onRequestClose, images }) => {
  const sliderRef = useRef(null);

  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    accessibility: true,
    arrows: true,
    adaptiveHeight: true,
  };

  const handleKeyDown = (event) => {
    if (event.key === 'ArrowLeft') {
      sliderRef.current.slickPrev();
    } else if (event.key === 'ArrowRight') {
      sliderRef.current.slickNext();
    }
  };

  useEffect(() => {
    if (isOpen) {
      window.addEventListener('keydown', handleKeyDown);
    } else {
      window.removeEventListener('keydown', handleKeyDown);
    }

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [isOpen]);

  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={onRequestClose}
      contentLabel="House Images Slideshow"
      style={customStyles}
      shouldFocusAfterRender={true} 
      shouldCloseOnOverlayClick={true} 
      shouldCloseOnEsc={true} 
    >
      <button onClick={onRequestClose} style={styles.closeButton} aria-label="Close Slideshow">
        &times;
      </button>
      <div style={styles.sliderContainer} tabIndex={0}>
        <Slider {...settings} ref={sliderRef}>
          {images.map((img, index) => (
            <div key={index}>
              <img src={img} alt={`House Image ${index + 1}`} style={styles.image} />
            </div>
          ))}
        </Slider>
      </div>
    </Modal>
  );
};

const customStyles = {
  content: {
    top: '50%',
    left: '50%',
    right: 'auto',
    bottom: 'auto',
    marginRight: '-50%',
    transform: 'translate(-50%, -50%)',
    width: '80%',
    maxWidth: '800px',
    padding: '20px',
    position: 'relative',
    borderRadius: '10px',
    boxShadow: '0 5px 15px rgba(0,0,0,0.3)',
  },
  overlay: {
    backgroundColor: 'rgba(0, 0, 0, 0.75)',
    zIndex: 1000,
  },
};

const styles = {
  closeButton: {
    position: 'absolute',
    top: '10px',
    right: '15px',
    fontSize: '2rem',
    background: 'none',
    border: 'none',
    color: '#fff',
    cursor: 'pointer',
    zIndex: 1001,
  },
  image: {
    width: '100%',
    height: 'auto',
    borderRadius: '8px',
  },
  sliderContainer: {
    outline: 'none',
  },
};

export default SlideshowModal;
