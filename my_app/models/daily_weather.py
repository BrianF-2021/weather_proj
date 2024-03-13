# python3 -m venv env/myenv
# source env/myenv/bin/activate
# pip install flask PyMysql flask-bcrypt
from my_app.config.mysqlconnection import connectToMySQL
from my_app import app
from my_app.misc.datetime_converter import DateTime_Converter as DTC


class Daily_Weather:

    db = "my_portfolio_db"
    forecast = []

    def __init__(self):
        # self.id = None
        # self.lat = None
        # self.lon = None
        self.dt = None
        self.sunrise = None
        self.sunset = None
        self.moonrise = None
        self.moonset = None
        self.moon_phase = None
        self.temp_max = None
        self.temp_min = None
        self.feels_like_eve = None
        self.feels_like_morn = None
        self.pressure = None
        self.humidity = None
        self.dew_point = None
        self.wind_speed = None
        self.wind_deg = None
        self.wind_gust = None
        self.weather_id = None
        self.weather_description = None
        self.clouds = None
        self.pop = None
        self.rain = None
        self.snow = None
        self.uvi = None
        self.icon = None
        Daily_Weather.forecast.append(self)
        # self.created_at = None
        # self.updated_at = None
        # self.user = None

    def set_instance_attributes(self, data):
        # self.id = data['id']
        # self.lat = data['lat']
        # self.lon = data['lon']
        self.dt = data['dt']
        self.sunrise = data['sunrise']
        self.sunset = data['sunset']
        self.moonrise = data['moonrise']
        self.moonset = data['moonset']
        self.moon_phase = data['moon_phase']
        self.temp_max = data['temp_max']
        self.temp_min = data['temp_min']
        self.feels_like_eve = data['feels_like_eve']
        self.feels_like_morn = data['feels_like_morn']
        self.pressure = data['pressure']
        self.humidity = data['humidity']
        self.dew_point = data['dew_point']
        self.wind_speed = data['wind_speed']
        self.wind_deg = data['wind_deg']
        self.wind_gust = data['wind_gust']
        self.weather_id = data['weather_id']
        self.weather_description = data['weather_description']
        self.clouds = data['clouds']
        self.pop = data['pop']
        self.rain = data['rain']
        self.snow = data['snow']
        self.uvi = data['uvi']
        self.icon = data['icon']
        # self.created_at = data['created_at']
        # self.updated_at = data['updated_at']
        # self.user = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM weather"
        weather_from_db = connectToMySQL(cls.db).query_db(query)
        this_weather = []
        for weather in weather_from_db:
            this_weather.append(weather)
        return this_weather

