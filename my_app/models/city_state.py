# python3 -m venv env/myenv
# source env/myenv/bin/activate
from my_app.config.mysqlconnection import connectToMySQL
from flask import flash
from my_app import app


class City_State:

    db = "my_portfolio_db"

    def __init__(self, data):
        self.id = data['id']
        self.city_state = data['city_state']

    @classmethod
    def get_all_cities_states_list(cls):
        query = "SELECT * FROM cities_states"
        cities_states_from_db = connectToMySQL(cls.db).query_db(query)
        cities_states = []
        for city_state in cities_states_from_db:
            cities_states.append(city_state)
        return cities_states

    @classmethod
    def get_id_by_city_state(cls, data):
        query = "SELECT id FROM cities_states WHERE city_state = %(city_state)s;"
        data = {
            'city_state': data['city_state']
        }
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            print(f"result: {result}, result[0]: {result[0]}")
            return result[0]['id']
        return result

    @classmethod
    def save(cls, data):
        # print("data:", data)
        query = "INSERT INTO cities_states(city_state) VALUES(%(city_state)s);"
        data = {
            "city_state": data['city_state'],
        }
        # returns id of object created/inserted
        return connectToMySQL(cls.db).query_db(query, data)

    # @classmethod
    # def get_one(cls, data):
    #     query = "SELECT * FROM users WHERE users.id = %(id)s;"
    #     result = connectToMySQL(cls.db).query_db(query, data)
    #     return cls(result[0])
