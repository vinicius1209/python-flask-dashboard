from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

dashboard = Flask(__name__)
dashboard.config.from_object(Config)
db = SQLAlchemy(dashboard)

from app import routes

if __name__ == "__main__":
    dashboard.run(host='0.0.0.0', debug=False, port=5000)