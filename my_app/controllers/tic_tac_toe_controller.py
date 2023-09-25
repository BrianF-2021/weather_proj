# from flask_app import app
# from flask import render_template,redirect,request,session,flash
from my_app.config.mysqlconnection import connectToMySQL
# from flask_app.models.user import User
from my_app import app
from flask import render_template, redirect, request, session
from my_app.games import tic_tac_toe_tkinter
from my_app.models import user as usr, painting


@app.route('/t3')
def t3():
    if 'id' not in session:
        return redirect('/')
    user_id = session['id']
    data = {
        'id': user_id
    }
    user = usr.User.get_one(data)
    tic_tac_toe_tkinter.tictactoe()
    return redirect('/user/home')


# @app.route('/t3')
# def t3():
#     user_id = session['id']
#     # for i in range(9):
#     #     session['i'] = i
#     data ={
#         'id': user_id
#         }
#     user = usr.User.get_one(data)
#     return render_template("tic_tac_toe.html", user = user)

# @app.route('/update_board/<string:pos>')
# def board_update(pos):
#    # game(pos)
#     user_id = session['id']
#     data ={
#         'id': user_id
#         }
#     user = usr.User.get_one(data)
#     return render_template("tic_tac_toe.html", user = user)
