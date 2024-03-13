from geopy.geocoders import Nominatim
from my_app.error_logging import logger


class GeoLocator:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="my_weather_app")

    def get_coord(self, city_state):
        lat = None
        lon = None
        try:
            location = self.geolocator.geocode(city_state)
        except Exception as e:
            logger.logger.error(
                f"'geo_locator_api.py => get_coord(), line 17' error: {e}")
            return (lat, lon)
        if location:
            lat = location.latitude
            lon = location.longitude
 #           print(f"lat: {location.latitude} lon: {location.longitude}")
        return (lat, lon)
