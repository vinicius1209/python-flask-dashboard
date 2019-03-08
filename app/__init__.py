from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler

dashboard = Flask(__name__)
dashboard.config.from_object(Config)

db = SQLAlchemy(dashboard)

login_manager = LoginManager(dashboard)
login_manager.login_view = 'login'
login_manager.login_message = 'Credenciais invalidas. Por favor tente novamente!'

from app import routes

from app.enviaEmailAutomatico import sendEmailsInterval

# Aqui realizamos o agendamento da função de Envio de E-mail Automático
# Neste momento, estamos rodando a mesma a cada 5 minutos...
scheduler = BackgroundScheduler()
scheduler.add_job(sendEmailsInterval, 'interval', minutes=5)
scheduler.start()

if __name__ == "__main__":
    dashboard.run(host='127.0.0.1', debug=False, port=5000)

