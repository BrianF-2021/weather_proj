# python3 -m venv env/myenv
# source env/myenv/bin/activate
# pip install flask PyMysql flask-bcrypt flask_cors requests geopy

from my_app import app
from my_app.controllers import game_controller, users_controller, weather_controller

if __name__ == "__main__":
    app.run(debug=True)
