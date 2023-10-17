# python3 -m venv env/myenv
# source env/myenv/bin/activate
# pip install flask PyMysql flask-bcrypt
from my_app.config.mysqlconnection import connectToMySQL
from flask import flash
from my_app import app
from my_app.models import best_score, user as usr


class Score:
    db = "my_portfolio_db"

    def __init__(self, data):
        self.id = data['id']
        self.prev_score = data['prev_score']
        self.best = data['best']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.game_id = data['game_id']
        self.users = None

    @classmethod
    def does_User_Score_Exist(cls, data):
        result = Score.get_score_by_userId(data)
        # query = "SELECT * FROM scores WHERE scores.id = %(id)s;"
        # result = connectToMySQL(cls.db).query_db(query, data)
        if not result:
            print("no data for this user_id")
            return (False, None)
        # saved_score = cls(result[0])
        return (True, result)

    @classmethod
    def does_Score_Exist(cls, data):
        result = Score.get_score_by_id(data)
        # query = "SELECT * FROM scores WHERE scores.id = %(id)s;"
        # result = connectToMySQL(cls.db).query_db(query, data)
        if not result:
            print("no data for this user_id")
            return (False, None)
        return (True, result)

    @classmethod
    def save_update_score(cls, data):
        doesUserScoreExist, saved_score = Score.does_User_Score_Exist(data)
        this_data = {
            'best': data['score'],
            'prev_score': data['score'],
            'user_id': data['user_id'],
            'game_id': data['game_id']
        }
        if not doesUserScoreExist:

            return Score.save(this_data)

        if saved_score.best <= data['score']:
            data = {
                'id': data['id'],
                'best': data['score'],
                'prev_score': data['score'],
                'user_id': data['user_id'],
                'game_id': data['game_id']
            }
            return Score.update_score(data)

        data = {
            'id': data['id'],
            'best': saved_score.best,
            'prev_score': data['score'],
            'user_id': data['user_id'],
            'game_id': data['game_id']
        }
        return Score.update_score(data)

    @classmethod
    def get_score_by_id(cls, data):
        query = "SELECT * FROM scores WHERE scores.id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)

        if not result:
            return None
        return cls(result[0])

    @classmethod
    def get_score_by_userId(cls, data):
        query = "SELECT * FROM scores WHERE scores.user_id = %(user_id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        if not result:
            return None
        return cls(result[0])

    @classmethod
    def get_top_scoresByGameId(cls, data):
        print("SCORE DATA: ", data)
        query = "SELECT * FROM users JOIN scores ON users.id = scores.user_id WHERE users.id = scores.user_id AND scores.game_id = %(id)s ORDER BY scores.best DESC LIMIT 5;"
        # query = "SELECT * FROM users JOIN scores ON users.id = scores.user_id WHERE users.id = scores.user_id ORDER BY scores.best DESC LIMIT 5;"
        # query = "SELECT users.first_name, scores.best FROM users JOIN scores ON users.id = scores.user_id WHERE users.id = scores.user_id ORDER BY scores.best DESC LIMIT 5;"
        scores_from_db = connectToMySQL(cls.db).query_db(query, data)

        # user_id = {'id': data['id']}
        # this_user = usr.User.get_one(user_id)
        print("TOP SCORES: ", scores_from_db)

        all = []
        # score_instance = cls(scores_from_db[0])
        if not scores_from_db:
            print("NO RESULTS FROM JOIN QUERY")
            return False
            # print("USER_INSTANCE:", score_instance)
            # print("USERS_FROM_DB:", scores_from_db)
            # return score_instance
        for score in scores_from_db:
            user_data = {
                'id': score['id'],
                'first_name': score['first_name'],
                'last_name': score['last_name'],
                'email': score['email'],
                'city': score['city'],
                'state': score['state'],
                'password': score['password'],
                'created_at': score['created_at'],
                'updated_at': score['updated_at']
            }

            score_data = {
                'id': score['scores.id'],
                'best': score['best'],
                'prev_score': score['prev_score'],
                'user_id': score['user_id'],
                'game_id': score['game_id'],
                'created_at': score['scores.created_at'],
                'updated_at': score['scores.updated_at']
            }

            score_inst = cls(score_data)
            score_inst.users = usr.User(user_data)
            all.append(score_inst)
        return all

    @classmethod
    def get_all_scores_by_userId(cls):
        query = "SELECT * FROM users JOIN scores ON users.id = scores.user_id WHERE users.id = scores.user_id;"
        scores_from_db = connectToMySQL(cls.db).query_db(query)
        all = []
        print("JOIN QUERY", scores_from_db)
        # score_instance = cls(scores_from_db[0])
        if not scores_from_db:
            print("NO RESULTS FROM JOIN QUERY")
            return False
            # print("USER_INSTANCE:", score_instance)
            # print("USERS_FROM_DB:", scores_from_db)
            # return score_instance
        for score in scores_from_db:

            user_data = {
                'id': score['id'],
                'first_name': score['first_name'],
                'last_name': score['last_name'],
                'email': score['email'],
                'password': score['password'],
                'created_at': score['created_at'],
                'updated_at': score['updated_at']
            }

            score_data = {
                'id': score['scores.id'],
                'best': score['best'],
                'prev_score': score['prev_score'],
                'user_id': score['user_id'],
                'game_id': score['game_id'],
                'created_at': score['paintings.created_at'],
                'updated_at': score['paintings.updated_at']
            }

            score_inst = cls(score_data)
            score_inst.users = usr.User(user_data)
            all.append(score_inst)
        return all

    @classmethod
    def save(cls, data):
        print("data:", data)
        # data = {
        #     'best':data['score'],
        #     'prev_score':data['score'],
        #     'user_id':data['user_id'],
        #     'game_id':data['game_id'],
        #     'id': data['id']
        # }
        query = "INSERT INTO scores(best, prev_score, user_id, game_id, created_at, updated_at) VALUES(%(best)s, %(prev_score)s,%(user_id)s,%(game_id)s, NOW(), NOW());"

        # returns id of object created/inserted
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update_score(cls, data):
        data = {
            'best': data['best'],
            'prev_score': data['prev_score'],
            'user_id': data['user_id'],
            'game_id': data['game_id'],
            'id': data['id']
        }
        query = "UPDATE scores SET best = %(best)s, prev_score = %(prev_score)s, user_id = %(user_id)s, game_id = %(game_id)s, id = %(id)s, updated_at = NOW() WHERE scores.id =  %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete_score(cls, data):
        query = "DELETE FROM scores WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
