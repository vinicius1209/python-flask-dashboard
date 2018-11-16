from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from apscheduler.schedulers.background import BackgroundScheduler

dashboard = Flask(__name__)
dashboard.config.from_object(Config)
db = SQLAlchemy(dashboard)

from app import routes

from app.enviaEmailAutomatico import sendEmailsInterval

# Aqui realizamos o agendamento da função de Envio de E-mail Automático
# Neste momento, estamos rodando a mesma a cada 5 minutos...
scheduler = BackgroundScheduler()
scheduler.add_job(sendEmailsInterval, 'interval', minutes=5)
scheduler.start()

if __name__ == "__main__":
    dashboard.run(host='0.0.0.0', debug=False, port=5000)