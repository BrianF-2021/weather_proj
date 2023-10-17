# python3 -m venv env/myenv
# source env/myenv/bin/activate
# pip install flask PyMysql flask-bcrypt
# test commit
from my_app.apis import geo_locator_api
from geopy.geocoders import Nominatim
import requests
import os
import json
from my_app.misc.datetime_converter import DateTime_Converter as DTC
from my_app.models import current_weather, daily_weather
from my_app.error_logging import logger


# change class name to Weather_Api
class Weather_Api:
    def __init__(self, city_state):
        self.geolocator = geo_locator_api.GeoLocator()
        self.city_state = city_state
        self.api_key = os.environ['OPENWX']
        self.dt = DTC()
        self.weather_data = None
        self.forecast = []

    def get_json_wx_data(self):
        try:
            geolocation = self.geolocator.get_coord(self.city_state)
        except Exception as e:
            logger.logger.error(
                f"'weather_api.py => get_json_wx_data(), line 30' geolocator error: {e}")
            # print(f"'get_json_wx_data' geolocator error: {e}")
            return

        latitude, longitude = geolocation
        api_link = f"https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&exclude=minutely,hourly,alerts&units=imperial&appid={self.api_key}"

        try:
            api_data = requests.get(api_link)
        except Exception as e:
            logger.logger.error(
                f"'weather_api.py => get_json_wx_data(), line 41' error: {e}")
            # print(f"'weather_api.py => get_json_wx_data' error: {e}")
            return

        print("API data: ", api_data)
        if api_data.status_code == 400:
            print("Check City/State Spelling")
            return
        self.weather_data = api_data.json()
        self.weather_data['lat'] = latitude
        self.weather_data['lon'] = longitude
        self.weather_data['city_state'] = self.city_state
        print('city_state: ', self.weather_data['city_state'])
        return

    def determine_icon(self, id):
        path = "/static/pics/"
        # resize image in shell $: convert myfigure.png -resize 200x100 myfigure.jpg
        if (199 < id < 233):
            return path+"scattered_thunderstorms.png"
        elif (299 < id < 322):
            return path+"scattered_showers.png"
        elif (499 < id < 532):
            return path+"showers.png"
        elif (599 < id < 623):
            return path+"snow.png"
        elif (id in [701, 721, 741]):
            return path+"fog.png"
        elif (id == 771):
            return "Squall"
        elif (id == 781):
            return "Tornado"
        elif (id in [800, 801]):
            return path+"sunny.png"
        elif (id in [802, 803]):
            return path+"partly_cloudy.png"
        elif (id == 804):
            return path+"cloudy.png"
        else:
            return "Other Odd Weather"

    def get_current_weather_data(self):
        self.get_json_wx_data()
        if not self.weather_data:
            print(
                "'weather_api.py => get_current_weather_data(), line 86' => No weather data...check error logging")
            return current_weather.Current_Weather()

        current = self.weather_data['current']
        print('CURRENT WEATHER: ', json.dumps(current, indent=4))
        _, _, sunrise = self.dt.get_datetime_formatted_from_unix(
            current['sunrise'])
        _, _, sunset = self.dt.get_datetime_formatted_from_unix(
            current['sunset'])
        _day, _date, _time = self.dt.get_datetime_formatted_from_unix(
            current['dt'])
        visibility = round(current['visibility']*.0006213712, 1)
        is_daytime = self.dt.is_daytime_from_unix(current['dt'])

        current_wx = {'city_state': self.weather_data['city_state'],
                      'lat': self.weather_data['lat'],
                      'lon': self.weather_data['lon'],
                      'timezone_offset': self.weather_data['timezone_offset'],
                      'dt': [_day, _date, _time],
                      'is_daytime': is_daytime,
                      'sunrise': sunrise,
                      'sunset': sunset,
                      'temp': current['temp'],
                      'feels_like': current['feels_like'],
                      'pressure': current['pressure'],
                      'humidity': current['humidity'],
                      'dew_point': current['dew_point'],
                      'clouds': current['clouds'],
                      'visibility': visibility,
                      'wind_speed': current['wind_speed'],
                      'wind_deg': current['wind_deg'],
                      'weather_id': current['weather'][0]['id'],
                      'description': current['weather'][0]['description'],
                      'icon': self.determine_icon(current['weather'][0]['id'])}
        # when available: ['wind_gust', 'uvi', 'rain', 'snow']
        if 'rain' in current:
            current_wx['rain'] = current['rain']['1h']
        else:
            current_wx['rain'] = 0

        if 'wind_gust' in current:
            current_wx['wind_gust'] = current['wind_gust']
        else:
            current_wx['wind_gust'] = 0

        if 'uvi' in current:
            current_wx['uvi'] = current['uvi']
        else:
            current_wx['uvi'] = 0

        if 'snow' in current:
            current_wx['snow'] = current['snow']['1h']
        else:
            current_wx['snow'] = 0
        # print(current_wx)
        current_wx_obj = current_weather.Current_Weather()
        current_wx_obj.set_instance_attributes(current_wx)
        # print(current_wx_obj)
        return current_wx_obj

    def get_daily_forecast(self):
        # print("5_DAY_FORECAST: ", self.weather_data['daily'])
        if not self.weather_data:
            print(
                "'weather_api.py => get_daily_forecast(), line 147' => No weather data...check error logging")
            return []

        for i, day in enumerate(self.weather_data['daily']):
            data = {}
            # print(f"day {i}: {day}")
            wind_gust = 0
            rain = 0
            uvi = 0
            snow = 0
            the_day, date, _ = self.dt.get_datetime_formatted_from_unix(
                day['dt'])
            _, _, sunrise = self.dt.get_datetime_formatted_from_unix(
                day['sunrise'])
            _, _, sunset = self.dt.get_datetime_formatted_from_unix(
                day['sunset'])
            _, _, moonrise = self.dt.get_datetime_formatted_from_unix(
                day['moonrise'])
            _, _, moonset = self.dt.get_datetime_formatted_from_unix(
                day['moonset'])

            if "visibility" in day:
                visibility = round(day['visibility']*.0006213712, 1)
            if 'rain' in day:
                rain = day['rain']
            if 'wind_gust' in day:
                wind_gust = day['wind_gust']
            if 'uvi' in day:
                uvi = day['uvi']
            if 'snow' in day:
                snow = day['snow']

            data['dt'] = the_day+" "+date
            data['sunrise'] = sunrise
            data['sunset'] = sunset
            data['moonrise'] = moonrise
            data['moonset'] = moonset
            data['moon_phase'] = day['moon_phase']
            data['temp_max'] = day['temp']['max']
            data['temp_min'] = day['temp']['min']
            data['feels_like_eve'] = day['feels_like']['eve']
            data['feels_like_morn'] = day['feels_like']['morn']
            data['pressure'] = day['pressure']
            data['humidity'] = day['humidity']
            data['dew_point'] = day['dew_point']
            data['wind_speed'] = day['wind_speed']
            data['wind_deg'] = day['wind_deg']
            data['wind_gust'] = wind_gust
            data['weather_id'] = day['weather'][0]['id']
            data['weather_description'] = day['weather'][0]['description']
            data['clouds'] = day['clouds']
            data['pop'] = int(day['pop']*100)
            data['rain'] = rain
            data['snow'] = snow
            data['uvi'] = uvi
            data['icon'] = self.determine_icon(day['weather'][0]['id'])
            data['created_at'] = None
            data['updated_at'] = None
            # print(f'DAY {i}: {data}')
            day_obj = daily_weather.Daily_Weather()
            day_obj.set_instance_attributes(data)
            if i <= 5:
                self.forecast.append(day_obj)
            print(f'DAY OBJECT {i}: {day_obj.icon}')
        return self.forecast

    def print_wx_data(self):
        self.get_json_wx_data()
        print(self.weather_data)
