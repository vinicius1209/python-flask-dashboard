from flask import Flask
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from config import Config

dashboard = Flask(__name__)
dashboard.config.from_object(Config)
db = SQLAlchemy(dashboard)
cache = Cache(dashboard)

import app.routes

if __name__ == "__main__":
    dashboard.run(host='192.168.100.25', debug=False, port=5000)