from geopy.geocoders import Nominatim


class GeoLocator:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="my_weather_app")

    def get_coord(self, city_state):
        lat = None
        lon = None
        try:
            location = self.geolocator.geocode(city_state)
        except Exception as e:
            print(f"GeoLocator 'get_coord' error: {e}")
            return (lat, lon)
        # print("GEOLOCATOR: location - ", location)
        if location:
            lat = location.latitude
            lon = location.longitude
            print(f"lat: {location.latitude} lon: {location.longitude}")
        return (lat, lon)
