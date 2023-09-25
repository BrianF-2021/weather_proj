from my_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module
from my_app import app
from my_app.models import user as usr
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PRICE_REGEX = re.compile ('^[-]?([1-9]{1}[0-9]{0,}(\.[0-9]{0,2})?|0(\.[0-9]{0,2})?|\.[0-9]{1,2})$')
# https://regexlib.com/(X(1)A(fH_1Zt9K-8cpSgQTkrRifgmQGG9_C-Q_nLDDM0bZ_HAJyCPjikPUVkFmyDSRfXHd0y0l-1fub1ngpEjEmN6CdLADFL85f4_7YNGUIdhRrF7Fmy5NFeACH6yBudcBPgI9IhxXaIm_en0YE53IcuWaDHWQdi6uGqzLzoxxwJyHkOo0Xvq3grGx5WVaa4hXAj_E0))/Search.aspx?k=currency&AspxAutoDetectCookieSupport=1



class My_Game:

    instances = []

    def __init__(self, name):
        self.name = name
        My_Game.instances.append(self)


    @classmethod
    def set_games(cls):
        games = ["snake", "mine_sweeper", "tic_tac_toe"]
        for game in games:
            My_Game(game)
        return


    @classmethod
    def get_games(cls):
        My_Game.set_games()
        return My_Game.instances


