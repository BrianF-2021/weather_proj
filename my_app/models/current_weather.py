# python3 -m venv env/myenv
# source env/myenv/bin/activate
# pip install flask PyMysql flask-bcrypt

# from flask_app import app
# from flask import render_template,redirect,request,session,flash

from my_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re  # the regex module
from my_app import app
from my_app.misc.datetime_converter import DateTime_Converter as DTC


class Current_Weather:

    db = "my_portfolio_db"

    def __init__(self):
        # self.user_id = None
        self.city_state = None
        self.lat = None
        self.lon = None
        self.timezone_offset = None
        self.dt = DTC().get_datetime_formatted_from_dt_obj()
        self.is_daytime = DTC().is_daytime_from_unix()
        print(
            f'Current_Weather.py dt: {self.dt} is_daytime: {self.is_daytime}')
        self.sunrise = None
        self.sunset = None
        self.temp = None
        self.feels_like = None
        self.pressure = None
        self.humidity = None
        self.dew_point = None
        self.clouds = None
        self.visibility = None
        self.wind_speed = None
        self.wind_deg = None
        self.wind_gust = None
        self.weather_id = None
        self.description = None
        self.icon = None
        self.uvi = None
        self.rain = None
        self.snow = None
        # self.created_at = None
        # self.updated_at = None
        self.forecast = []

    def set_instance_attributes(self, data):
        # self.user_id = data['user_id']
        print(f"DATA['dt'] = {data['dt']}")
        self.city_state = data['city_state']
        self.lat = data['lat']
        self.lon = data['lon']
        self.timezone_offset = data['timezone_offset']
        self.dt = data['dt']
        self.is_daytime = data['is_daytime']
        self.sunrise = data['sunrise']
        self.sunset = data['sunset']
        self.temp = data['temp']
        self.feels_like = data['feels_like']
        self.pressure = data['pressure']
        self.humidity = data['humidity']
        self.dew_point = data['dew_point']
        self.clouds = data['clouds']
        self.visibility = data['visibility']
        self.wind_speed = data['wind_speed']
        self.wind_deg = data['wind_deg']
        self.wind_gust = data['wind_gust']
        self.weather_id = data['weather_id']
        self.description = data['description']
        self.icon = data['icon']
        self.uvi = data['uvi']
        self.rain = data['rain']
        self.snow = data['snow']
        # self.created_at = data['created_at']
        # self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM weather"
        weather_from_db = connectToMySQL(cls.db).query_db(query)
        this_weather = []
        for weather in weather_from_db:
            this_weather.append(weather)
        return cls(this_weather)

    @classmethod
    def save(cls, data):
        # print("data:", data)
        query = "INSERT INTO current_weather(user_id, city_state_id, lat, lon, timezone_offset, dt, sunrise, sunset, temp, feels_like, pressure, humidity, dew_point, uvi, clouds, visibility, wind_speed, wind_deg, wind_gust, weather_id, description, icon, rain, snow,created_at, updated_at) VALUES(%(user_id)s, %(city_state_id)s, %(lat)s, %(lat)s, %(timezone_offset)s, %(dt)s, %(sunrise)s, %(sunset)s, %(temp)s, %(feels_like)s, %(pressure)s, %(humidity)s, %(dew_point)s, %(uvi)s, %(clouds)s, %(visibility)s, %(wind_speed)s, %(wind_deg)s, %(wind_gust)s, %(weatherId)s, %(description)s, %(icon)s, %(rain)s, %(snow)s, NOW(), NOW());"

        data = {
            "user_id": data['user_id'],
            "city_state_id": data['city_state_id'],
            "lat": data['lat'],
            "lon": data['lon'],
            "timezone_offset": data['timezone_offset'],
            "dt": data['dt'],
            "sunrise": data['sunrise'],
            "sunset": data['sunset'],
            "temp": data['temp'],
            "feels_like": data['feels_like'],
            "pressure": data['pressure'],
            "humidity": data['humidity'],
            "dew_point": data['dew_point'],
            "uvi": data['uvi'],
            "clouds": data['clouds'],
            "visibility": data['visibility'],
            "wind_speed": data['wind_speed'],
            "wind_deg": data['wind_deg'],
            "wind_gust": data['wind_gust'],
            "weatherId": data['weatherId'],
            "description": data['description'],
            "icon": data['icon'],
            "rain": data['rain'],
            "snow": data['snow'],
        }
        # returns id of object created/inserted
        return connectToMySQL(cls.db).query_db(query, data)

# user_id,lat,lon,timezone_offset,dt,sunrise,sunset,temp,feels_like,pressure,humidity,dew_point,uvi,clouds,visibility,wind_speed,wind_deg,wind_gust,weatherId,description,icon,rain,snow,created_at,updated_at

# %(lat)s,%(lat)s,%(timezone_offset)s,%(dt)s,%(sunrise)s,%(sunset)s,%(temp)s,%(feels_like)s,%(pressure)s,%(humidity)s,%(dew_point)s,%(uvi)s,%(clouds)s,%(visibility)s,%(wind_speed)s,%(wind_deg)s,%(wind_gust)s,%(weatherId)s,%(description)s,%(icon)s,%(rain)s,%(snow)s,

# user_id,lat,lon,timezone_offset,dt,sunrise,sunset,temp,feels_like,pressure,humidity,dew_point,uvi,clouds,visibility,wind_speed,wind_deg,wind_gust,weatherId,description,icon,rain,snow,created_at,updated_at
