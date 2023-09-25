# from flask_app import app
# from flask import render_template,redirect,request,session,flash
from my_app.apis import weather_api
from my_app.config.mysqlconnection import connectToMySQL
# from flask_app.models.user import User
from my_app import app
from flask import render_template, redirect, request, session
from my_app.models import current_weather, user as usr, city_state
from my_app.time.datetime_converter import DateTime_Converter as DTC


@ app.route('/local_weather/<int:user_id>', methods=['POST'])
def get_local_weather(user_id):
    if 'id' not in session:
        return redirect('/')
    # data = {
    #     'id':user_id,
    #     'city_state':request.form['city_state']
    # }

    city_state = request.form['city_state']
    if not city_state:
        return redirect('/user/home')

    user_data = {'id': user_id}
    this_user = usr.User.get_one(user_data)
    weather_obj = weather_api.Weather_Api(city_state)
    current_wx = weather_obj.get_current_weather_data()
    forecast_wx = weather_obj.get_daily_forecast()
    # dt = DTC()
    # day, date, time = dt.get_datetime_formatted()
    # is_day_time = dt.is_daytime()
    if current_wx:
        return render_template("weather_page.html",
                               forecast_wx=forecast_wx,
                               current_wx=current_wx,
                               this_user=this_user)

    message = f"No Weather Data Available for city/state: ' {city_state} '"
    return render_template("weather_page.html",
                           current_wx=current_wx,
                           message=message,
                           this_user=this_user)


# @app.route('/weather')
# def get_weather():
#     if 'id' not in session:
#         return redirect('/')
#     user_data = {'id': session['id']}
#     # data = {
#     #     'id':user_id,
#     #     'city_state':request.form['city_state']}
#     # geo_locator.findCoord("MHT")
#     # geo_locator.findCoord("Milford NH")
#     location = "Nashua NH"
#     # city_state = request.form['city_state']
#     current_wx_dict = weather_api.Weather_Api(
#         location).get_current_weather_data()
#     current_wx_dict['user_id'] = session['id']
#     cityState = current_wx_dict['city_state']
#     current_wx_dict["city_state_id"] = 1
#     dt = DTC()
#     day, date, time = dt.get_datetime_formatted()
#     this_user = usr.User.get_one(user_data)

#     return render_template("weather_page.html", this_user=this_user, current_wx_dict=current_wx_dict, cityState=cityState, day=day, date=date, time=time)
