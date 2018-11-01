from flask import Flask
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager

dashboard = Flask(__name__)
dashboard.config.from_object(Config)
db = SQLAlchemy(dashboard)
cache = Cache(dashboard)
login = LoginManager(dashboard)

import app.routes

if __name__ == "__main__":
    dashboard.run(host='192.168.25.20', debug=False, port=5000)