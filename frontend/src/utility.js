export const getCoordinates = async (address) => {
    const apiUrl = process.env.REACT_APP_GEOCODE_API;

    const geocodingUrl = `https://geocode.maps.co/search?q=${encodeURIComponent(address)}&api_key=${apiUrl}`;

    try {
      const response = await fetch(geocodingUrl);
      const data = await response.json();
      if (data.length === 0) {
        return [NaN, NaN];
      } else {
        return [data[0].lat, data[0].lon];
      }
    } catch (error) {
      console.error('Error:', error);
        return [NaN, NaN]
    }
  };
