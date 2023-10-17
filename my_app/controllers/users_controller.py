from my_app.apis import geo_locator_api, weather_api
from my_app.config.mysqlconnection import connectToMySQL
from my_app import app
from flask import render_template, redirect, request, session
from my_app.models import user as usr, game
from my_app.misc import datetime_converter


@app.route('/')
def index():
    session.clear()
    return redirect('/main')


@app.route('/main')
def user_main():
    session.clear()
    return render_template("login_and_registration.html")


@app.route('/create')
def user_create():
    return render_template("login_and_registration.html")


@app.route("/users/creating", methods=["POST"])
def user_creating():
    if not usr.User.validate_registration(request.form):
        return redirect('/create')
    session['id'] = usr.User.save_new_user(request.form)
    return redirect('/user/home')


@app.route('/user/home')
def user_home():
    if 'id' not in session:
        return redirect('/')
    user_id = session['id']
    data = {
        'id': user_id
    }
    all_games = game.Game.get_all_gamesObj()
    this_user = usr.User.get_one(data)

    return render_template("user_home_page.html", this_user=this_user, all_games=all_games)


@app.route('/logout')
def logout():
    if 'id' not in session:
        return redirect('/')
    session.clear()
    return redirect('/main')


@app.route('/users/validation', methods=['POST'])
def login_validation():
    data = {
        'email': request.form['email'],
        'password': request.form['password']
    }
    result = usr.User.validate_login(data)
    if result == False:
        return redirect('/create')

    user = usr.User.get_one_by_email(data)
    session['id'] = user.id
    return redirect('/user/home')


@app.route("/users/edit/<int:user_id>")
def user_edit(user_id):
    if 'id' not in session:
        return redirect('/')
    data = {
        'id': user_id
    }
    this_user = usr.User.get_one(data)
    return render_template('user_edit_form.html', this_user=this_user)


@app.route("/users/editing/<int:user_id>", methods=['POST'])
def user_editing(user_id):
    if 'id' not in session:
        return redirect('/')
    data = {
        'id': user_id,
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'city': request.form['city'],
        'state': request.form['state']
    }
    if not usr.User.user_edit_validation(data):
        return redirect(f'/users/edit/{user_id}')
    usr.User.update_user(data)
    return redirect(f'/user/edit/complete')


@app.route("/users/edit_pw/<int:user_id>")
def edit_user_password(user_id):
    if 'id' not in session:
        return redirect('/')
    data = {
        'id': user_id
    }
    this_user = usr.User.get_one(data)

    return render_template('user_edit_pw_form.html', this_user=this_user)


@app.route("/user/editing/password/<int:id>", methods=['POST'])
def editing_user_password(id):
    if 'id' not in session:
        return redirect('/')
    validation_data = {
        'id': id,
        'password': request.form['password'],
        'confirm_password': request.form['confirm_password'],
        'new_password': request.form['new_password'],
        'confirm_new_pw': request.form['confirm_new_pw']
    }
    update_data = {
        'id': id,
        'password': request.form['new_password']
    }
    if not usr.User.user_edit_password_validation(validation_data):
        return redirect(f'/users/edit_pw/{id}')
    usr.User.update_password(update_data)
    # return redirect(f'/users/edit_pw/{id}')
    return redirect(f'/user/edit/complete')


@app.route('/user/edit/complete')
def edit_complete():
    if 'id' not in session:
        return redirect('/')
    user_id = session['id']
    data = {
        'id': user_id
    }
    this_user = usr.User.get_one(data)
    message = 'You have successfully updated your profile'
    # return render_template('user_profile_edit_complete.html', message=message, this_user=this_user)
    return render_template('user_profile_edit_complete.html', message=message, this_user=this_user)


@app.route("/users/delete/<int:user_id>")
def user_destroy(user_id):
    if 'id' not in session:
        return redirect('/')
    data = {
        'id': user_id
    }
    session.pop('id')
    usr.User.delete(data)
    return redirect('/main')


@app.route('/confirm/delete/<int:user_id>')
def confirm_delete(user_id):
    if 'id' not in session:
        return redirect('/')

    return render_template('user_confirm_acct_delete.html', user_id=user_id)
