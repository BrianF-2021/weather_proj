# python3 -m venv env/myenv
# source env/myenv/bin/activate
# pip install flask PyMysql flask-bcrypt

# from flask_app import app
# from flask import render_template,redirect,request,session,flash
from crypt import methods
from urllib import response
from my_app import app
from my_app.games import mine_sweeper_tkinter, tic_tac_toe_tkinter
from my_app.models import score, best_score, game
from flask import render_template, redirect, request, session, jsonify
from my_app.models import user as usr


@app.route('/game/<string:game_name>/<int:game_id>')
def games(game_name, game_id):
    if 'id' not in session:
        return redirect('/')
    gameId = {
        'id': game_id
    }
    this_game = game.Game.get_one_game(gameId)
    user_id = session['id']
    userId = {
        'id': user_id
    }
    game_data = {
        'id': this_game.id,
        'name': this_game.name
    }
    user = usr.User.get_one(userId)
    top_scores = score.Score.get_top_scoresByGameId(game_data)
    # print("game_name: ", this_game.name)
    game_best = best_score.Best_Score.get_bestScore_by_gameId(game_data)

    if game_name == "snake":
        return render_template("snake_game.html", user=user, game_best=game_best, this_game=this_game, top_scores=top_scores)
    if game_name == "minesweeper":
        mine_sweeper_tkinter.mine_sweeper()
        return redirect('/user_local_weather')
    if game_name == "tic_tac_toe":
        tic_tac_toe_tkinter.tictactoe()
        return redirect('/user_local_weather')
    return redirect('/user_local_weather')

    # snake_game = game.Game.get_one_game(gameId)
    #    all_games = my_game.My_Game.get_games()
    # return render_template("snake_game.html", snake_game_stats = snake_game_stats, top_scores = top_scores, game_best = game_best)
    # snake_game_stats = score.Score.get_all_scores_by_userId(userId)


@app.route('/updateScore/<int:game_id>', methods=["POST", "GET"])
def updateScore(game_id):
    if 'id' not in session:
        return redirect('/')
    user_id = session['id']
    userId = {
        'id': user_id
    }
    gameId = {
        'id': game_id
    }

    if request.method == "POST":
        game_data = request.get_json()
        # print("score: ", game_data['score'])
        # data = {
        #     'score':game_data['score'],
        #     'score_id':game_data['score_id'],
        #     'user_id': game_data['user_id'],
        #     'game_id': game_data['game_id'],
        #     'gameBest_id': game_data['gameBest_id']
        # }
        score_data = {
            'score': game_data['score'],
            'id': game_data['score_id'],
            'user_id': user_id,
            'game_id': game_id
        }

        bestGame_score_data = {
            'score': game_data['score'],
            'id': game_data['gameBest_id'],
            'user_id': user_id,
            'game_id': game_id
        }

        score.Score.save_update_score(score_data)
        best_score.Best_Score.save_update_gameBestScore(bestGame_score_data)
        return "Transformed!"

    if request.method == "GET":
        user = usr.User.get_one(userId)
        top_scores = score.Score.get_top_scoresByGameId(game_id)
        game_best = best_score.Best_Score.get_gameBest_by_gameId(gameId)
        data = {'user_id': user_id, 'game_id': game_id}
        user_scores = score.Score.get_score_by_userId(data)

        # stats = {'best': game_bests, 'user_best': user_scores.best, 'user_prev': user_scores.prev_score}
        stats = {}
        stats['game_id'] = game_id
        stats['user_id'] = user_id
        stats['top_scores'] = top_scores

        if user_scores is None:
            stats['user_best'] = 0
            stats['user_prev'] = 0
            stats['score_id'] = None
        else:
            stats['user_best'] = user_scores.best
            stats['user_prev'] = user_scores.prev_score
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
    # return "Transformed!"

    return redirect("/user/home")
