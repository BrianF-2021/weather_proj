# python3 -m venv env/myenv
# source env/myenv/bin/activate
# pip install flask PyMysql flask-bcrypt

# from flask_app import app
# from flask import render_template,redirect,request,session,flash

from my_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re  # the regex module
from my_app import app


class Current_Weather:

    db = "my_portfolio_db"

    def __init__(self, data):
        # self.user_id = data['user_id']
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
        self.forecast = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM weather"
        weather_from_db = connectToMySQL(cls.db).query_db(query)
        this_weather = []
        for weather in weather_from_db:
            this_weather.append(weather)
        return cls(this_weather)

    # @classmethod
    # def get_one(cls, data):
    #     query = "SELECT * FROM users WHERE users.id = %(id)s;"
    #     result = connectToMySQL(cls.db).query_db(query, data)
    #     return result

    # @classmethod
    # def get_one(cls, data):
    #     query = "SELECT * FROM users WHERE users.id = %(id)s;"
    #     result = connectToMySQL(cls.db).query_db(query, data)
    #     return cls(result[0])

    # @classmethod
    # def get_email(cls,data):
    #     query = "SELECT * FROM users WHERE email = %(email)s;"
    #     result = connectToMySQL("mydb").query_db(query,data)
    #     if len(result) < 1:
    #         return False
    #     return cls(result[0])

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

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def save_new_user(cls, data):
        pw_hash = bcrypt.generate_password_hash(data['password'])
        print("pw_hash", pw_hash)
        data = {
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "email": data['email'],
            "password": pw_hash,
        }
        query = "INSERT INTO users(first_name, last_name, email, password, created_at, updated_at) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def save_new_password(cls, data):
        pw_hash = bcrypt.generate_password_hash(data['password'])
        print("pw_hash", pw_hash)
        data = {
            "password": pw_hash,
        }
        query = "INSERT INTO users(password, updated_at) VALUES(%(password)s, NOW());"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_registration(data):
        is_valid = True  # we assume this is true
        if (len(data['first_name']) < 2) or (len(data['last_name']) < 2):
            flash("First and Last Name  must be at least 2 characters.")
            is_valid = False

        if not data['first_name'].isalpha() or not data['last_name'].isalpha():
            flash("First and Last Name can not contain numbers")
            is_valid = False

        if len(data['password']) < 8 or len(data['confirm_password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid = False

        if data['password'] != data['confirm_password']:
            flash("Password and Confirm Password do not match")
            is_valid = False

        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!")
            is_valid = False

        email = {'email': data['email']}
        user = User.get_one_by_email(email)
        if user:
            flash("The email you entered is already associated with an account.")
            is_valid = False
        return is_valid

    @classmethod
    def get_one_by_email(cls, data):
        #        print('get_one_by_email  email:', data)
        query = "SELECT * FROM users WHERE email = %(email)s;"
#        print(connectToMySQL(cls.db).query_db(query, data))
        result = (connectToMySQL(cls.db).query_db(query, data))
        if result:
            return cls(result[0])
        return False

    @staticmethod
    def validate_login(data):
        email = {'email': data['email']}
        # print(email)
        is_valid = True
        user = User.get_one_by_email(email)
        # print('DATA PASSWORD', data['password'])
        # print('USER: ', user)
        # print('PASSWORD', user.password)
        if user:
            print('True', user)
            print('USER NAME', user.first_name)
            if data['email'] == "":
                flash("An email address is required")
                is_valid = False
            if data['email'] != user.email:
                is_valid = False
            if data['password'] == "":
                flash("A password is required")
                is_valid = False
            if not bcrypt.check_password_hash(user.password, data['password']):
                is_valid = False

            flash('Invalid Login Credentials')
            return is_valid
        else:
            flash('Invalid Login Credentials')
            is_valid = False
            return is_valid

    @staticmethod
    def user_edit_validation(data):
        is_valid = True  # we assume this is true
        if len(data['first_name']) < 2 or len(data['last_name']) < 2:
            flash("First and Last Name  must be at least 2 characters.")
            is_valid = False

        if not data['first_name'].isalpha() or not data['last_name'].isalpha():
            flash("First and Last Name can not contain numbers")
            is_valid = False

        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!")
            is_valid = False

        email = {'email': data['email']}
        user = User.get_one_by_email(email)
        if user:
            if (data['id'] != user.id) and (data['email'] == user.email):
                flash(
                    "The email you entered is already associated with another account.")
                is_valid = False

        return is_valid

    @staticmethod
    def user_edit_password_validation(data):
        is_valid = True
        user_id = {'id':  data['id']}
        pw = data['password']
        confirm_pw = data['confirm_password']
        new_pw = data['new_password']
        new_confirm_pw = data['confirm_new_pw']

        user = User.get_one(user_id)
        if not bcrypt.check_password_hash(user.password, data['password']):
            flash("Invalid Password")
            is_valid = False
        if pw != confirm_pw:
            flash("Confirm password must match password")
            is_valid = False
        if len(new_pw) < 8 or len(new_confirm_pw) < 8:
            flash("Password must be at least 8 characters")
            is_valid = False
        if new_pw != new_confirm_pw:
            flash("Confirm new password must match new password")
            is_valid = False
        return is_valid

    @classmethod
    def update_name_email(cls, data):
        data = {
            'id': data['id'],
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "email": data['email']
        }
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = NOW() WHERE users.id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update_password(cls, data):
        pw_hash = bcrypt.generate_password_hash(data['password'])
        data = {
            "id": data['id'],
            "password": pw_hash
        }
        query = "UPDATE users SET password = %(password)s, updated_at = NOW() WHERE users.id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    # @classmethod
    # def get_all_complete(cls):
    #     # query = "SELECT * FROM recipes JOIN sasquatches ON sasquatches.id = recipes.sasquatch_id WHERE sasquatches.id = recipes.sasquatch_id;"
    #     query = "SELECT * FROM users JOIN sasquatches ON sasquatches.user_id = users.id WHERE sasquatches.user_id = users.id;"
    #     sasquatches_from_db = connectToMySQL(cls.db).query_db(query)
    #     all = []
    #     print("JOIN QUERY", sasquatches_from_db)
    #     #sasquatch_instance = cls(sasquatches_from_db[0])
    #     if not sasquatches_from_db:
    #         print("NO RESULTS FROM JOIN QUERY")
    #         return False
    #         # print("USER_INSTANCE:", sasquatch_instance)
    #         # print("USERS_FROM_DB:", sasquatches_from_db)
    #         # return sasquatch_instance
    #     for sasquatch in sasquatches_from_db:

    #         user_data= {
    #             'id':sasquatch['id'],
    #             'first_name':sasquatch['first_name'],
    #             'last_name':sasquatch['last_name'],
    #             'email':sasquatch['email'],
    #             'password':sasquatch['password'],
    #             'created_at':sasquatch['created_at'],
    #             'updated_at':sasquatch['updated_at']
    #         }

    #         sasquatch_data = {
    #             'id' : sasquatch['sasquatches.id'],
    #             'location' : sasquatch['location'],
    #             'what_happened' : sasquatch['what_happened'],
    #             'date' : sasquatch['date'],
    #             'number' : sasquatch['number'],
    #             'user_id' : sasquatch['user_id'],
    #             'created_at' : sasquatch['sasquatches.created_at'],
    #             'updated_at' : sasquatch['sasquatches.updated_at']
    #         }

    #         user_inst = cls(user_data)
    #         user_inst.sasquatches = sas.Sasquatch(sasquatch_data)
    #         all.append(user_inst)
    #         print('ALL: ', all)
    #     return all

    # @classmethod
    # def get_all_with_recipes(cls):
    #     # query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id WHERE users.id = recipes.user_id;"
    #     query = "SELECT * FROM users JOIN recipes ON users.id = recipes.user_id WHERE users.id = recipes.user_id;"
    #     users_from_db = connectToMySQL(cls.db).query_db(query)
    #     all = []
    #     print("JOIN QUERY", users_from_db)
    #     #user_instance = cls(users_from_db[0])
    #     if not users_from_db:
    #         print("NO RESULTS FROM JOIN QUERY")
    #         return False
    #         # print("USER_INSTANCE:", user_instance)
    #         # print("USERS_FROM_DB:", users_from_db)
    #         # return user_instance
    #     for usr in users_from_db:
    #         recipe_data = {
    #             'id':usr['recipes.id'],
    #             'name':usr['name'],
    #             'date':usr['date'],
    #             'time':usr['time'],
    #             'description':usr['description'],
    #             'instructions':usr['instructions'],
    #             'user_id':usr['user_id'],
    #             'created_at':usr['recipes.created_at'],
    #             'updated_at':usr['recipes.updated_at']
    #         }

    #         user_data= {
    #             'id':usr['id'],
    #             'first_name':usr['first_name'],
    #             'last_name':usr['last_name'],
    #             'email':usr['email'],
    #             'password':usr['password'],
    #             'created_at':usr['created_at'],
    #             'updated_at':usr['updated_at']
    #         }
    #         user_inst = cls(user_data)
    #         user_inst.recipes = recipe.Recipe(recipe_data)
    #         all.append(user_inst)
    #     return all

    # @classmethod
    # def get_user(cls, data):
    #     query = "SELECT * FROM users WHERE id = %(id)s"
    #     user_from_db = connectToMySQL(cls.db).query_db(query,data)
    #     return cls(user_from_db[0])

    # # @classmethod
    # # def save(cls, data):
    # #     query = "INSERT INTO users(first_name, last_name, email) VALUES(%(first_name)s, %(last_name)s,%(email)s);"
    # #     return connectToMySQL(cls.db).query_db(query,data)

    # @classmethod
    # def edit_user(cls, data):
    #     query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s;"
    #     data = {
    #         'first_name' : data['first_name'],
    #         'last_name' : data['last_name'],
    #         'email' : data['email']
    #     }
    #     return connectToMySQL(cls.db).query_db(query,data)

    # @classmethod
    # def delete_user(cls, data):
    #     query = "DELETE FROM users WHERE id = %()s"
    #     return connectToMySQL(cls.db).query_db(query,data)

    # @classmethod
    # def delete_users(cls, data):
    #     query = "TRUNCATE TABLE users"
    #     return connectToMySQL(cls.db).query_db(query, data)
