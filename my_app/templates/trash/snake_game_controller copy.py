# python3 -m venv env/myenv
# source env/myenv/bin/activate
# pip install flask PyMysql flask-bcrypt

# from flask_app import app
# from flask import render_template,redirect,request,session,flash
from crypt import methods
from urllib import response
from my_app.config.mysqlconnection import connectToMySQL
# from flask_app.models.user import User
from my_app import app
from my_app.models import my_game, score, best_score
from flask import render_template, redirect, request, session,jsonify, make_response
from my_app.models import user as usr, painting



@app.route('/snake_game/{id}')
def snake_game():
    if 'id' not in session:
        return redirect('/')
    user_id = session['id']
    data ={
        'id': user_id
        }
    user = usr.User.get_one(data)
    top_scores = score.Score.get_top_scores()
#    all_games = my_game.My_Game.get_games()
    return render_template("snake_game.html", user = user, top_scores = top_scores)

@app.route('/updateScore', methods=["POST","GET"])
def updateScore():
    if 'id' not in session:
        return redirect('/')
    user_id = session['id']

    if request.method == "POST":
        s_core = request.get_json()
        print("score: ", s_core['score'])
        data = {
            'id':3,
            'user_id': user_id,
            's_core':s_core['score'],
            'game_id': 1
        }
        score.Score.save_update_score(data)
        best_score.Best_Score.save_update_gameBestScore(data)
        return "Transformed!"
    if request.method == "GET":
        data = {'user_id': user_id, 'game_id':1}
        user_scores = score.Score.get_score_by_userId(data)
        game_best = best_score.Best_Score.get_bestScore_by_gameId(data)
        # stats = {'best': game_bests, 'user_best': user_scores.best, 'user_prev': user_scores.prev_score}
        stats = {}
        stats['game_id'] = 1
        stats['user_id'] = user_id
        if user_scores is None:
            stats['user_best'] = 0
            stats['user_prev'] = 0
            stats['score_id'] = None
        else:
            stats['user_best']= user_scores.best
            stats['user_prev']= user_scores.prev_score
            stats['score_id'] = user_scores.id
            # stats['game_id'] = user_scores.game_id



        if game_best is None:
            stats['game_best'] = 0
            stats['game_best_id'] = None
        else:
            stats['game_best'] = game_best.best
            stats['game_best_id'] = game_best.id
        print("stats: ", stats)
        return jsonify(stats)
    #return "Transformed!"

    return redirect("/user/home")


