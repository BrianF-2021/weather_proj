# python3 -m venv env/myenv
# source env/myenv/bin/activate
# pip install flask PyMysql flask-bcrypt
from my_app.config.mysqlconnection import connectToMySQL
from my_app import app


class Daily_Weather:

    db = "my_portfolio_db"

    def __init__(self, data):
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


#     @classmethod
#     def get_one(cls, data):
#         query = "SELECT * FROM users WHERE users.id = %(id)s;"
#         result = connectToMySQL(cls.db).query_db(query, data)
#         return cls(result[0])

#     @classmethod
#     def save(cls, data):
#         print("data:", data)
#         query = "INSERT INTO users(first_name, last_name, email, created_at, updated_at) VALUES(%(first_name)s, %(last_name)s, %(email)s, NOW(), NOW());"

#         data = {
#             'first_name': data['first_name'],
#             'last_name': data['last_name'],
#             'email': data['email']
#         }
#         # returns id of object created/inserted
#         return connectToMySQL(cls.db).query_db(query, data)

#     @classmethod
#     def delete(cls, data):
#         query = "DELETE FROM users WHERE id = %(id)s;"
#         return connectToMySQL(cls.db).query_db(query, data)
