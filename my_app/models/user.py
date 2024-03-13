# python3 -m venv env/myenv
# source env/myenv/bin/activate
# pip install flask PyMysql flask-bcrypt

# from flask_app import app
# from flask import render_template,redirect,request,session,flash

from my_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re  # the regex module
from my_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:

    db = "my_portfolio_db"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.city = data['city']
        self.state = data['state']
        self.updated_at = data['updated_at']
        self.paintings = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        users_from_db = connectToMySQL(cls.db).query_db(query)
        users = []
        for user in users_from_db:
            users.append(user)
        return users

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users(first_name, last_name, email, city, state, created_at, updated_at) VALUES(%(first_name)s, %(last_name)s, %(email)s, , %(city)s, %(state)s, NOW(), NOW());"

        data = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'city': data['city'],
            'state': data['state'],
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
        data = {
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "email": data['email'],
            'city': data['city'],
            'state': data['state'],
            "password": pw_hash,
        }
        query = "INSERT INTO users(first_name, last_name, email, city, state, password, created_at, updated_at) VALUES(%(first_name)s, %(last_name)s, %(email)s,  %(city)s, %(state)s, %(password)s,NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def save_new_password(cls, data):
        pw_hash = bcrypt.generate_password_hash(data['password'])
        data = {
            "password": pw_hash,
        }
        query = "INSERT INTO users(password, updated_at) VALUES(%(password)s, NOW());"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_registration(data):
        is_valid = True
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
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = (connectToMySQL(cls.db).query_db(query, data))
        if result:
            return cls(result[0])
        return False

    @staticmethod
    def validate_login(data):
        email = {'email': data['email']}
        pw = {'password': data['password']}
        is_valid = True

        this_user = User.get_one_by_email(email)
        if not this_user:
            is_valid = False
            flash('Invalid Login Credentials')
            return is_valid

        if this_user:
            if data['email'] == "":
                flash("An email address is required")
                is_valid = False
            if data['email'] != this_user.email:
                is_valid = False
            if data['password'] == "":
                flash("A password is required")
                is_valid = False
            if not bcrypt.check_password_hash(this_user.password, data['password']):
                is_valid = False

            if not is_valid:
                flash('Invalid Login Credentials')
            return is_valid

    @staticmethod
    def user_edit_validation(data):
        is_valid = True
    # future validation for city/state
        # if len(data['city']) < 2 or len(data['city']) < 2:
        #     flash("First and Last Name  must be at least 2 characters.")
        #     is_valid = False

        # if len(data['state']) < 2 or len(data['state']) < 2:
        #     flash("First and Last Name  must be at least 2 characters.")
        #     is_valid = False

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
    def update_user(cls, data):
        data = {
            'id': data['id'],
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "email": data['email'],
            "city": data['city'],
            "state": data['state']
        }
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, city = %(city)s, state = %(state)s, updated_at = NOW() WHERE users.id = %(id)s;"
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
