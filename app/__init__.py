from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager
from celery import Celery

dashboard = Flask(__name__)
dashboard.config.from_object(Config)

celery = Celery(dashboard.name, broker=dashboard.config['CELERY_BROKER_URL'])
celery.conf.update(dashboard.config)


db = SQLAlchemy(dashboard)
login_manager = LoginManager(dashboard)
login_manager.login_view = 'login'
login_manager.login_message = 'Credenciais invalidas. Por favor tente novamente!'

from app import routes

if __name__ == "__main__":
    dashboard.run(host='0.0.0.0', debug=False, port=5000)

