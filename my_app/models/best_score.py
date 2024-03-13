# python3 -m venv env/myenv
# source env/myenv/bin/activate
# pip install flask PyMysql flask-bcrypt

# from flask_app import app
# from flask import render_template,redirect,request,session,flash

from my_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from my_app import app
from my_app.models import best_score, user as usr, score
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PRICE_REGEX = re.compile ('^[-]?([1-9]{1}[0-9]{0,}(\.[0-9]{0,2})?|0(\.[0-9]{0,2})?|\.[0-9]{1,2})$')
# https://regexlib.com/(X(1)A(fH_1Zt9K-8cpSgQTkrRifgmQGG9_C-Q_nLDDM0bZ_HAJyCPjikPUVkFmyDSRfXHd0y0l-1fub1ngpEjEmN6CdLADFL85f4_7YNGUIdhRrF7Fmy5NFeACH6yBudcBPgI9IhxXaIm_en0YE53IcuWaDHWQdi6uGqzLzoxxwJyHkOo0Xvq3grGx5WVaa4hXAj_E0))/Search.aspx?k=currency&AspxAutoDetectCookieSupport=1



class Best_Score:
    db = "my_portfolio_db"

    def __init__(self, data):
        self.id = data['id']
        self.best = data['best']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.game_id = data['game_id']
        self.users = None

    # @classmethod
    # def does_User_bestScore_Exist(cls, data):
    #     result = Best_Score.get_bestScore_by_userId(data)
    #     # query = "SELECT * FROM scores WHERE scores.id = %(id)s;"
    #     # result = connectToMySQL(cls.db).query_db(query, data)
    #     if not result:
    #         print("no data for this user_id")
    #         return (False, None)
    #     # saved_score = cls(result[0])
    #     return (True, result)

    @classmethod
    def does_game_bestScore_exist(cls, data):
        result = Best_Score.get_bestScore_by_gameId(data)
        # query = "SELECT * FROM scores WHERE scores.id = %(id)s;"
        # result = connectToMySQL(cls.db).query_db(query, data)
        if not result:
            print("no data for this user_id")
            return (False, None)
        return (True, result)


    @classmethod
    def save_update_gameBestScore(cls, data):
        doesGameBestScoreExist, saved_gameBestScore = Best_Score.does_game_bestScore_exist(data)
        print("SAVED_GAME_BEST_SCORE: ", saved_gameBestScore)
        if not doesGameBestScoreExist:
            bestGame_data = {
                'best':data['score'],
                'user_id':data['user_id'],
                'game_id':data['game_id']
            }
            return Best_Score.save(bestGame_data)

        # user_scores_data = {
        #         'score':data['score'],
        #         'user_id':data['user_id'],
        #         'game_id':data['game_id']
        #     }
        user_scores = score.Score.get_score_by_userId(data)
        if (saved_gameBestScore.best <= data['score']):
            gameBestData = {
                'id': data['id'],
                'best':data['score'],
                'user_id':data['user_id'],
                'game_id':data['game_id']
            }
            return Best_Score.update_bestScore(gameBestData)

        if (user_scores.best >= saved_gameBestScore.best):
            gameBestData = {
                'id': data['id'],
                'best': user_scores.best,
                'user_id':data['user_id'],
                'game_id':data['game_id']
            }
            return Best_Score.update_bestScore(gameBestData)

        gameBestData = {
            'id': data['id'],
            'best':saved_gameBestScore.best,
            'user_id':data['user_id'],
            'game_id':data['game_id']
        }
        print("Error line 91-98 in best_score.py")
        return Best_Score.update_bestScore(gameBestData)


    @classmethod
    def update_bestScore(cls, data):
        # data = {
        #     'best':data['best'],
        #     'user_id':data['user_id'],
        #     'game_id':data['game_id'],
        #     'id': data['id']
        # }
        query = "UPDATE best_scores SET best = %(best)s, user_id = %(user_id)s, game_id = %(game_id)s, id = %(id)s, updated_at = NOW() WHERE best_scores.game_id =  %(game_id)s;"
        return connectToMySQL(cls.db).query_db(query, data)



    @classmethod
    def get_game_bestScore(cls, data):
        query = "SELECT * FROM best_scores WHERE best_scores.id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)

        if not result:
            return None
        return cls(result[0])


    @classmethod
    def get_gameBest_by_gameId(cls, data):
        query = "SELECT * FROM best_scores WHERE best_scores.game_id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        if not result:
            return None
        return cls(result[0])


    @classmethod
    def get_all_bestScores(cls):
        query = "SELECT * FROM users JOIN best_scores ON users.id = best_scores.user_id WHERE users.id = best_scores.user_id;"
        scores_from_db = connectToMySQL(cls.db).query_db(query)
        all = []
        print("JOIN QUERY", scores_from_db)
        #score_instance = cls(scores_from_db[0])
        if not scores_from_db:
            print("NO RESULTS FROM JOIN QUERY")
            return False
            # print("USER_INSTANCE:", score_instance)
            # print("USERS_FROM_DB:", scores_from_db)
            # return score_instance
        for score in scores_from_db:

            user_data= {
                'id':score['id'],
                'first_name':score['first_name'],
                'last_name':score['last_name'],
                'email':score['email'],
                'password':score['password'],
                'created_at':score['created_at'],
                'updated_at':score['updated_at']
            }

            bestScore_data = {
                'id' : score['scores.id'],
                'best' : score['best'],
                'user_id' : score['user_id'],
                'game_id' : score['game_id'],
                'created_at' : score['paintings.created_at'],
                'updated_at' : score['paintings.updated_at']
            }

            bestScore_inst = cls(bestScore_data)
            bestScore_inst.users = usr.User(user_data)
            all.append(bestScore_inst)
        return all


    @classmethod
    def save(cls, data):
        print("data:", data)
        # data = {
        #     'best':data['score'],
        #     'user_id':data['user_id'],
        #     'game_id':data['game_id'],
        #     'id': data['id']
        # }
        print("right data:", data)
        query = "INSERT INTO best_scores(best, user_id, game_id, created_at, updated_at) VALUES(%(best)s,%(user_id)s,%(game_id)s, NOW(), NOW());"

        return connectToMySQL(cls.db).query_db(query, data) # returns id of object created/inserted


    @classmethod
    def delete_score(cls, data):
        query = "DELETE FROM scores WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_bestScore_by_gameId(cls, data):
        query = "SELECT * FROM best_scores WHERE %(id)s = best_scores.game_id;"
        # query = "SELECT * FROM games JOIN best_scores ON %(id)s = best_scores.game_id WHERE %(id)s = best_scores.game_id;"
        scores_from_db = connectToMySQL(cls.db).query_db(query,data)
        print("JOIN QUERY", scores_from_db)
        #score_instance = cls(scores_from_db[0])
        if not scores_from_db:
            print("NO RESULTS FROM JOIN QUERY")
            return False
            # print("USER_INSTANCE:", score_instance)
            # print("USERS_FROM_DB:", scores_from_db)
            # return score_instance
        # for score in scores_from_db:

        # user_data= {
        #     'id':scores_from_db[0]['id'],
        #     'first_name':scores_from_db[0]['first_name'],
        #     'last_name':scores_from_db[0]['last_name'],
        #     'email':scores_from_db[0]['email'],
        #     'password':scores_from_db[0]['password'],
        #     'created_at':scores_from_db[0]['created_at'],
        #     'updated_at':scores_from_db[0]['updated_at']
        # }

        bestScore_data = {
            'id' : scores_from_db[0]['id'],
            'best' : scores_from_db[0]['best'],
            'user_id' : scores_from_db[0]['user_id'],
            'game_id' : scores_from_db[0]['game_id'],
            'created_at' : scores_from_db[0]['created_at'],
            'updated_at' : scores_from_db[0]['updated_at']
        }

        bestScore_inst = cls(bestScore_data)
        # bestScore_inst.users = usr.User(user_data)
        return bestScore_inst


