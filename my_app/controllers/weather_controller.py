# from flask_app import app
# from flask import render_template,redirect,request,session,flash
from my_app.apis import weather_api
from my_app.config.mysqlconnection import connectToMySQL
from my_app import app
from flask import render_template, redirect, request, session
from my_app.models import current_weather, user as usr, city_state
from my_app.misc.datetime_converter import DateTime_Converter as DTC


@app.route('/weather_page/<int:user_id>')
def weather_page(user_id):
    if 'id' not in session:
        return redirect('/')
    user_data = {'id': user_id}
    this_user = usr.User.get_one(user_data)

    messages = []
    _city_state = None
    if this_user.city and this_user.state:
        _city_state = f"{this_user.city} {this_user.state}"
    else:
        _city_state = "Key West FL"
        messages.append("No City and State has been saved to your profile.")

    weather_obj = weather_api.Weather_Api(_city_state)
    current_wx = weather_obj.get_current_weather_data()
    # print(current_wx.dt, current_wx.is_daytime)
    forecast_wx = weather_obj.get_daily_forecast()
    # print('TESTING: ', forecast_wx, current_wx.temp)
    if forecast_wx == [] and current_wx.temp is None:
        messages = []
        messages.append("Failed to Connect to Weather Server!")
        return render_template("weather_page.html",
                               forecast_wx=forecast_wx,
                               current_wx=current_wx,
                               this_user=this_user,
                               messages=messages)

    if current_wx.temp and forecast_wx != []:
        return render_template("weather_page.html",
                               forecast_wx=forecast_wx,
                               current_wx=current_wx,
                               this_user=this_user,
                               messages=messages)


@ app.route('/local_weather/<int:user_id>', methods=['POST'])
def get_local_weather(user_id):
    if 'id' not in session:
        return redirect('/')
    # data = {
    #     'id':user_id,
    #     'city_state':request.form['city_state']
    # }

    _city_state = request.form['city_state']
    if not _city_state:
        return redirect(f'/local_weather/{user_id}')

    user_data = {'id': user_id}
    this_user = usr.User.get_one(user_data)
    weather_obj = weather_api.Weather_Api(_city_state)

    current_wx = weather_obj.get_current_weather_data()
    forecast_wx = weather_obj.get_daily_forecast()

    messages = []
    if not this_user.city and not this_user.state:
        messages.append("No City and State has been saved to your profile.")

    weather_obj = weather_api.Weather_Api(_city_state)
    current_wx = weather_obj.get_current_weather_data()
    # print(current_wx.dt, current_wx.is_daytime)
    forecast_wx = weather_obj.get_daily_forecast()
    # print('TESTING: ', forecast_wx, current_wx.temp)
    if forecast_wx == [] and current_wx.temp is None:
        messages = []
        messages.append("Failed to Connect to Weather Server!")
        return render_template("weather_page.html",
                               forecast_wx=forecast_wx,
                               current_wx=current_wx,
                               this_user=this_user,
                               messages=messages)

    if current_wx.temp and forecast_wx != []:
        return render_template("weather_page.html",
                               forecast_wx=forecast_wx,
                               current_wx=current_wx,
                               this_user=this_user,
                               messages=messages)
