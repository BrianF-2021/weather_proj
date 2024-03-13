# from flask_app import app
# from flask import render_template,redirect,request,session,flash
from my_app.apis import weather_api, weather_gov, wx_gov_2day_history 
from my_app import app
from flask import render_template, redirect, request, session
from my_app.models import current_weather, game, user as usr, city_state
from my_app.misc.datetime_converter import DateTime_Converter as DTC
import time



@app.route('/')
def index():
    session.clear()
    return redirect('/home_weather_page')


@app.route('/home_weather_page')
def home_weather_page():
    _city_state = "Key West FL"
    # all_games = game.Game.get_all_gamesObj()

    weather_obj = weather_api.Weather_Api(_city_state)
    current_wx = weather_obj.get_current_weather_data()
    forecast_wx = weather_obj.get_daily_forecast()
    res = weather_gov.get_forecast_graph(current_wx.lat, current_wx.lon)
    
    messages = []
    messages.append("Login to save your location...plus new features!")

    if forecast_wx == [] and current_wx.temp is None:
        messages.append("Failed to Connect to Weather Server!")
        return render_template("home_weather_page.html",
                               forecast_wx=forecast_wx,
                               current_wx=current_wx,
                               messages=messages)
    if not res:
        messages.append("Failed to Connect to Weather Server for Graph Data!")
        return render_template("home_weather_page.html",
                               forecast_wx=forecast_wx,
                               current_wx=current_wx,
                               messages=messages)

    if current_wx.temp and forecast_wx != []:
        return render_template("home_weather_page.html",
                               forecast_wx=forecast_wx,
                               current_wx=current_wx,
                               messages=messages)


@ app.route('/search_local_weather', methods=['POST'])
def local_weather():

    _city_state = request.form['city_state']
    messages = []
    messages.append("Login to save your location...plus new features!")
    if not _city_state:
        _city_state = "Key West Fl"

    weather_obj = weather_api.Weather_Api(_city_state)
    current_wx = weather_obj.get_current_weather_data()
    forecast_wx = weather_obj.get_daily_forecast()
    res = weather_gov.get_forecast_graph(current_wx.lat, current_wx.lon)
    messages = []
    if forecast_wx == [] and current_wx.temp is None:
        messages.append("Failed to Connect to Weather Server!")
        return render_template("home_weather_page.html",
                               forecast_wx=forecast_wx,
                               current_wx=current_wx,
                               messages=messages)
    if not res:
        messages.append("Failed to Connect to Weather Server for Graph Data!")
        return render_template("home_weather_page.html",
                               forecast_wx=forecast_wx,
                               current_wx=current_wx,
                               messages=messages)

    if current_wx.temp and forecast_wx != []:
        return render_template("home_weather_page.html",
                               forecast_wx=forecast_wx,
                               current_wx=current_wx,
                               messages=messages)


@ app.route('/user_search_local_weather', methods=['POST'])
def user_search_local_weather():
    if 'id' not in session:
        return redirect('/')

    user_data = {'id': session['id']}
    this_user = usr.User.get_one(user_data)
    all_games = game.Game.get_all_gamesObj()

    messages = []
    _city_state = request.form['city_state']
    if not this_user.city or not this_user.state:
        messages.append("No City and State has been saved to your profile.")

    if not _city_state:
        _city_state = "Key West FL"

    weather_obj = weather_api.Weather_Api(_city_state)
    current_wx = weather_obj.get_current_weather_data()
    forecast_wx = weather_obj.get_daily_forecast()
    res = weather_gov.get_forecast_graph(current_wx.lat, current_wx.lon)
    history_day1, history_day2 = wx_gov_2day_history.get_2day_weather_history(_city_state)
    history_date1, history_date2 = wx_gov_2day_history.get_2day_history_dates()
    no_history_day1 = wx_gov_2day_history.No_Wx_Data(history_date1)
    no_history_day2 = wx_gov_2day_history.No_Wx_Data(history_date2)

    messages = []
    if forecast_wx == [] and current_wx.temp == "":
        messages.append("Failed to Connect to Weather Server!")
        messages.append("Check City and State Spelling!")
        return render_template("user_weather_page.html",
                               forecast_wx=forecast_wx,
                               current_wx=current_wx,
                               all_games=all_games,
                               this_user=this_user,
                               history_day1=no_history_day1,
                               history_day2=no_history_day2,
                               messages=messages)
    if not res:
        messages.append("Failed to Connect to Weather Server for Graph Data!")
        return render_template("user_weather_page.html",
                               forecast_wx=forecast_wx,
                               current_wx=current_wx,
                               all_games=all_games,
                               this_user=this_user,
                               history_day1=history_day1,
                               history_day2=history_day2,
                               messages=messages)

    if current_wx.temp and forecast_wx != []:
        return render_template("user_weather_page.html",
                               forecast_wx=forecast_wx,
                               current_wx=current_wx,
                               all_games=all_games,
                               this_user=this_user,
                               history_day1=history_day1,
                               history_day2=history_day2,
                               messages=messages)


@ app.route('/user_local_weather')
def user_local_weather():
    if 'id' not in session:
        return redirect('/')

    user_data = {'id': session['id']}
    this_user = usr.User.get_one(user_data)
    # all_games = game.Game.get_all_gamesObj()

    messages = []
    _city_state = None
    if this_user.city and this_user.state:
        _city_state = f"{this_user.city} {this_user.state}"
    else:
        _city_state = "Key West FL"
        messages.append("No City and State has been saved to your profile.")

    weather_obj = weather_api.Weather_Api(_city_state)
    current_wx = weather_obj.get_current_weather_data()
    forecast_wx = weather_obj.get_daily_forecast()
    time.sleep(1)
    res = weather_gov.get_forecast_graph(current_wx.lat, current_wx.lon)
    history_day1 = wx_gov_2day_history.get_2day_weather_history(_city_state)[0]
    history_day2 = wx_gov_2day_history.get_2day_weather_history(_city_state)[1]
    messages = []
    if forecast_wx == [] and current_wx.temp is None:
        messages.append("Failed to Connect to Weather Server!")
        return render_template("user_weather_page.html",
                               forecast_wx=forecast_wx,
                               current_wx=current_wx,
                               history_day1=history_day1,
                               history_day2=history_day2,
                               this_user=this_user,
                               messages=messages)

    if current_wx.temp and forecast_wx != []:
        return render_template("user_weather_page.html",
                               forecast_wx=forecast_wx,
                               current_wx=current_wx,
                               history_day1=history_day1,
                               history_day2=history_day2,
                               this_user=this_user,
                               messages=messages)


