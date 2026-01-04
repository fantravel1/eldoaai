/**
 * ELDOA Geolocation Module
 * Provides "near me" functionality for practitioners and classes
 */

window.ELDOAGeolocation = (function() {
  // Major city coordinates for practitioners without precise coordinates
  const cityCoordinates = {
    // USA
    'New York': { lat: 40.7128, lng: -74.0060 },
    'Los Angeles': { lat: 34.0522, lng: -118.2437 },
    'Chicago': { lat: 41.8781, lng: -87.6298 },
    'Houston': { lat: 29.7604, lng: -95.3698 },
    'Phoenix': { lat: 33.4484, lng: -112.0740 },
    'San Diego': { lat: 32.7157, lng: -117.1611 },
    'San Francisco': { lat: 37.7749, lng: -122.4194 },
    'Austin': { lat: 30.2672, lng: -97.7431 },
    'Denver': { lat: 39.7392, lng: -104.9903 },
    'Miami': { lat: 25.7617, lng: -80.1918 },
    'Atlanta': { lat: 33.7490, lng: -84.3880 },
    'Seattle': { lat: 47.6062, lng: -122.3321 },
    'Boston': { lat: 42.3601, lng: -71.0589 },
    'Nashville': { lat: 36.1627, lng: -86.7816 },
    'Portland': { lat: 45.5155, lng: -122.6789 },
    'Dallas': { lat: 32.7767, lng: -96.7970 },
    'Philadelphia': { lat: 39.9526, lng: -75.1652 },
    'San Antonio': { lat: 29.4241, lng: -98.4936 },
    'Las Vegas': { lat: 36.1699, lng: -115.1398 },
    'Minneapolis': { lat: 44.9778, lng: -93.2650 },
    'Tampa': { lat: 27.9506, lng: -82.4572 },
    'Charlotte': { lat: 35.2271, lng: -80.8431 },
    'Orlando': { lat: 28.5383, lng: -81.3792 },
    'Detroit': { lat: 42.3314, lng: -83.0458 },
    'Columbus': { lat: 39.9612, lng: -82.9988 },
    'Indianapolis': { lat: 39.7684, lng: -86.1581 },
    'Jacksonville': { lat: 30.3322, lng: -81.6557 },
    'Salt Lake City': { lat: 40.7608, lng: -111.8910 },
    'Kansas City': { lat: 39.0997, lng: -94.5786 },
    'Raleigh': { lat: 35.7796, lng: -78.6382 },
    'Cleveland': { lat: 41.4993, lng: -81.6944 },
    'Pittsburgh': { lat: 40.4406, lng: -79.9959 },
    'Sacramento': { lat: 38.5816, lng: -121.4944 },
    'St. Louis': { lat: 38.6270, lng: -90.1994 },
    'San Jose': { lat: 37.3382, lng: -121.8863 },
    'Oklahoma City': { lat: 35.4676, lng: -97.5164 },
    'Tucson': { lat: 32.2226, lng: -110.9747 },
    'New Orleans': { lat: 29.9511, lng: -90.0715 },
    'Baltimore': { lat: 39.2904, lng: -76.6122 },
    'Milwaukee': { lat: 43.0389, lng: -87.9065 },
    // Canada
    'Toronto': { lat: 43.6532, lng: -79.3832 },
    'Vancouver': { lat: 49.2827, lng: -123.1207 },
    'Montreal': { lat: 45.5017, lng: -73.5673 },
    'Calgary': { lat: 51.0447, lng: -114.0719 },
    'Edmonton': { lat: 53.5461, lng: -113.4938 },
    'Ottawa': { lat: 45.4215, lng: -75.6972 },
    'Winnipeg': { lat: 49.8951, lng: -97.1384 },
    'Quebec City': { lat: 46.8139, lng: -71.2080 },
    'Victoria': { lat: 48.4284, lng: -123.3656 },
    'Halifax': { lat: 44.6488, lng: -63.5752 },
    // France
    'Paris': { lat: 48.8566, lng: 2.3522 },
    'Lyon': { lat: 45.7640, lng: 4.8357 },
    'Marseille': { lat: 43.2965, lng: 5.3698 },
    'Toulouse': { lat: 43.6047, lng: 1.4442 },
    'Nice': { lat: 43.7102, lng: 7.2620 },
    'Bordeaux': { lat: 44.8378, lng: -0.5792 },
    'Nantes': { lat: 47.2184, lng: -1.5536 },
    'Strasbourg': { lat: 48.5734, lng: 7.7521 },
    'Montpellier': { lat: 43.6108, lng: 3.8767 },
    'Lille': { lat: 50.6292, lng: 3.0573 },
    // UK
    'London': { lat: 51.5074, lng: -0.1278 },
    'Manchester': { lat: 53.4808, lng: -2.2426 },
    'Birmingham': { lat: 52.4862, lng: -1.8904 },
    'Edinburgh': { lat: 55.9533, lng: -3.1883 },
    'Glasgow': { lat: 55.8642, lng: -4.2518 },
    'Liverpool': { lat: 53.4084, lng: -2.9916 },
    'Bristol': { lat: 51.4545, lng: -2.5879 },
    'Leeds': { lat: 53.8008, lng: -1.5491 },
    'Sheffield': { lat: 53.3811, lng: -1.4701 },
    'Newcastle': { lat: 54.9783, lng: -1.6178 },
    // Germany
    'Berlin': { lat: 52.5200, lng: 13.4050 },
    'Munich': { lat: 48.1351, lng: 11.5820 },
    'Hamburg': { lat: 53.5511, lng: 9.9937 },
    'Frankfurt': { lat: 50.1109, lng: 8.6821 },
    'Cologne': { lat: 50.9375, lng: 6.9603 },
    'Stuttgart': { lat: 48.7758, lng: 9.1829 },
    'Dusseldorf': { lat: 51.2277, lng: 6.7735 },
    // Italy
    'Rome': { lat: 41.9028, lng: 12.4964 },
    'Milan': { lat: 45.4642, lng: 9.1900 },
    'Naples': { lat: 40.8518, lng: 14.2681 },
    'Turin': { lat: 45.0703, lng: 7.6869 },
    'Florence': { lat: 43.7696, lng: 11.2558 },
    'Venice': { lat: 45.4408, lng: 12.3155 },
    'Bologna': { lat: 44.4949, lng: 11.3426 },
    // Australia
    'Sydney': { lat: -33.8688, lng: 151.2093 },
    'Melbourne': { lat: -37.8136, lng: 144.9631 },
    'Brisbane': { lat: -27.4698, lng: 153.0251 },
    'Perth': { lat: -31.9505, lng: 115.8605 },
    'Adelaide': { lat: -34.9285, lng: 138.6007 },
    // New Zealand
    'Auckland': { lat: -36.8485, lng: 174.7633 },
    'Wellington': { lat: -41.2865, lng: 174.7762 },
    'Christchurch': { lat: -43.5321, lng: 172.6362 },
    // Other
    'Dubai': { lat: 25.2048, lng: 55.2708 },
    'Johannesburg': { lat: -26.2041, lng: 28.0473 },
    'Cape Town': { lat: -33.9249, lng: 18.4241 },
    'Vienna': { lat: 48.2082, lng: 16.3738 },
    'Zurich': { lat: 47.3769, lng: 8.5417 },
    'Geneva': { lat: 46.2044, lng: 6.1432 },
    'Amsterdam': { lat: 52.3676, lng: 4.9041 },
    'Brussels': { lat: 50.8503, lng: 4.3517 },
    'Madrid': { lat: 40.4168, lng: -3.7038 },
    'Barcelona': { lat: 41.3851, lng: 2.1734 },
    'Lisbon': { lat: 38.7223, lng: -9.1393 }
  };

  // Country center coordinates (fallback)
  const countryCoordinates = {
    'USA': { lat: 39.8283, lng: -98.5795 },
    'United States': { lat: 39.8283, lng: -98.5795 },
    'Canada': { lat: 56.1304, lng: -106.3468 },
    'France': { lat: 46.2276, lng: 2.2137 },
    'United Kingdom': { lat: 55.3781, lng: -3.4360 },
    'UK': { lat: 55.3781, lng: -3.4360 },
    'Germany': { lat: 51.1657, lng: 10.4515 },
    'Italy': { lat: 41.8719, lng: 12.5674 },
    'Australia': { lat: -25.2744, lng: 133.7751 },
    'New Zealand': { lat: -40.9006, lng: 174.8860 },
    'South Africa': { lat: -30.5595, lng: 22.9375 },
    'UAE': { lat: 23.4241, lng: 53.8478 },
    'Austria': { lat: 47.5162, lng: 14.5501 },
    'Switzerland': { lat: 46.8182, lng: 8.2275 },
    'Netherlands': { lat: 52.1326, lng: 5.2913 },
    'Belgium': { lat: 50.5039, lng: 4.4699 },
    'Spain': { lat: 40.4637, lng: -3.7492 },
    'Portugal': { lat: 39.3999, lng: -8.2245 }
  };

  /**
   * Get user's current location using browser geolocation API
   */
  function getUserLocation() {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject(new Error('Geolocation is not supported by your browser'));
        return;
      }

      navigator.geolocation.getCurrentPosition(
        (position) => {
          resolve({
            lat: position.coords.latitude,
            lng: position.coords.longitude,
            accuracy: position.coords.accuracy
          });
        },
        (error) => {
          let message = 'Unable to get your location';
          switch (error.code) {
            case error.PERMISSION_DENIED:
              message = 'Location permission denied. Please enable location access.';
              break;
            case error.POSITION_UNAVAILABLE:
              message = 'Location information is unavailable.';
              break;
            case error.TIMEOUT:
              message = 'Location request timed out.';
              break;
          }
          reject(new Error(message));
        },
        {
          enableHighAccuracy: false,
          timeout: 10000,
          maximumAge: 300000 // Cache for 5 minutes
        }
      );
    });
  }

  /**
   * Estimate coordinates for a practitioner based on city/country
   */
  function estimateCoordinates(practitioner) {
    // Check if practitioner has coordinates
    if (practitioner.latitude && practitioner.longitude) {
      return { lat: practitioner.latitude, lng: practitioner.longitude };
    }

    // Try city first
    if (practitioner.city) {
      const cityKey = Object.keys(cityCoordinates).find(
        city => practitioner.city.toLowerCase().includes(city.toLowerCase()) ||
                city.toLowerCase().includes(practitioner.city.toLowerCase())
      );
      if (cityKey) {
        return cityCoordinates[cityKey];
      }
    }

    // Fallback to country
    if (practitioner.country) {
      const countryKey = Object.keys(countryCoordinates).find(
        country => practitioner.country.toLowerCase() === country.toLowerCase()
      );
      if (countryKey) {
        return countryCoordinates[countryKey];
      }
    }

    return null;
  }

  /**
   * Calculate distance between two points using Haversine formula
   * Returns distance in miles
   */
  function calculateDistance(lat1, lng1, lat2, lng2) {
    const R = 3959; // Earth's radius in miles
    const dLat = toRad(lat2 - lat1);
    const dLng = toRad(lng2 - lng1);
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
      Math.sin(dLng / 2) * Math.sin(dLng / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  }

  function toRad(deg) {
    return deg * (Math.PI / 180);
  }

  /**
   * Format distance for display
   */
  function formatDistance(miles) {
    if (miles < 1) {
      return 'Less than 1 mile';
    } else if (miles < 10) {
      return `${miles.toFixed(1)} miles`;
    } else if (miles < 100) {
      return `${Math.round(miles)} miles`;
    } else if (miles < 500) {
      return `~${Math.round(miles / 10) * 10} miles`;
    } else {
      return `${Math.round(miles)} miles`;
    }
  }

  /**
   * Add distance to practitioners based on user location
   */
  function addDistancesToPractitioners(practitioners, userLat, userLng) {
    return practitioners.map(p => {
      const coords = estimateCoordinates(p);
      if (coords) {
        const distance = calculateDistance(userLat, userLng, coords.lat, coords.lng);
        return {
          ...p,
          distance: distance,
          distanceText: formatDistance(distance),
          hasCoordinates: true
        };
      }
      return {
        ...p,
        distance: Infinity,
        distanceText: 'Distance unknown',
        hasCoordinates: false
      };
    });
  }

  /**
   * Sort practitioners by distance
   */
  function sortByDistance(practitioners) {
    return [...practitioners].sort((a, b) => {
      // Prioritize practitioners with known coordinates
      if (a.hasCoordinates && !b.hasCoordinates) return -1;
      if (!a.hasCoordinates && b.hasCoordinates) return 1;
      return (a.distance || Infinity) - (b.distance || Infinity);
    });
  }

  /**
   * Filter practitioners within a radius
   */
  function filterByRadius(practitioners, radiusMiles) {
    return practitioners.filter(p => p.distance && p.distance <= radiusMiles);
  }

  /**
   * Check if geolocation is available
   */
  function isGeolocationAvailable() {
    return 'geolocation' in navigator;
  }

  /**
   * Get saved location from localStorage
   */
  function getSavedLocation() {
    try {
      const saved = localStorage.getItem('eldoa_user_location');
      if (saved) {
        const parsed = JSON.parse(saved);
        // Check if saved within last 24 hours
        if (Date.now() - parsed.timestamp < 24 * 60 * 60 * 1000) {
          return { lat: parsed.lat, lng: parsed.lng };
        }
      }
    } catch (e) {
      console.warn('Could not retrieve saved location:', e);
    }
    return null;
  }

  /**
   * Save location to localStorage
   */
  function saveLocation(lat, lng) {
    try {
      localStorage.setItem('eldoa_user_location', JSON.stringify({
        lat,
        lng,
        timestamp: Date.now()
      }));
    } catch (e) {
      console.warn('Could not save location:', e);
    }
  }

  /**
   * Clear saved location
   */
  function clearSavedLocation() {
    try {
      localStorage.removeItem('eldoa_user_location');
    } catch (e) {
      console.warn('Could not clear location:', e);
    }
  }

  // Public API
  return {
    getUserLocation,
    estimateCoordinates,
    calculateDistance,
    formatDistance,
    addDistancesToPractitioners,
    sortByDistance,
    filterByRadius,
    isGeolocationAvailable,
    getSavedLocation,
    saveLocation,
    clearSavedLocation,
    cityCoordinates,
    countryCoordinates
  };
})();
