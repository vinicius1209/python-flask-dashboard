from flask import Flask
from config import Config

dashboard = Flask(__name__)
dashboard.config.from_object(Config)

import app.routes

if __name__ == "__main__":
    dashboard.run(host= '192.168.25.24', debug=False, port=5000)