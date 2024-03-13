# from rsa import PrivateKey
from my_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from my_app import app
from my_app.models import user as usr
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PRICE_REGEX = re.compile(
    '^[-]?([1-9]{1}[0-9]{0,}(\.[0-9]{0,2})?|0(\.[0-9]{0,2})?|\.[0-9]{1,2})$')
# https://regexlib.com/(X(1)A(fH_1Zt9K-8cpSgQTkrRifgmQGG9_C-Q_nLDDM0bZ_HAJyCPjikPUVkFmyDSRfXHd0y0l-1fub1ngpEjEmN6CdLADFL85f4_7YNGUIdhRrF7Fmy5NFeACH6yBudcBPgI9IhxXaIm_en0YE53IcuWaDHWQdi6uGqzLzoxxwJyHkOo0Xvq3grGx5WVaa4hXAj_E0))/Search.aspx?k=currency&AspxAutoDetectCookieSupport=1


class Game:
    db = "my_portfolio_db"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        # self.best_score_id = data['best_score_id']
        self.all_games = []

    @classmethod
    def games(cls):
        all_games = []
        games = ["snake", "minesweeper", "tic_tac_toe"]
        for game in games:
            data = {
                'name': game,
            }
            Game.save_game(data)
        return

    @classmethod
    def get_gameNames_listJson(cls):
        all_games = []
        games = ["snake", "minesweeper", "tic_tac_toe"]
        for game in games:
            data = {
                'name': game,
            }
            all_games.append(data)
        return all_games

    @classmethod
    def save_game(cls, data):
        # print("data:", data)
        query = "INSERT INTO games(name) VALUES(%(name)s);"

        data = {
            'name': data['name'],
            # 'best_score_id':data['best_score_id'],
        }
        # returns id of object created/inserted
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_one_game(cls, data):
        query = "SELECT * FROM games WHERE games.id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_all_gamesObj(cls):
        query = "SELECT * FROM games"
        games_from_db = connectToMySQL(cls.db).query_db(query)

        if not games_from_db:
            print("NO RESULTS FROM QUERY")
            return False
        all = []
        for this_game in games_from_db:
            all.append(cls(this_game))
        return all


