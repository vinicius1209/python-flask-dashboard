import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cout << "Vinicius" << endl;'
    CACHE_TYPE = 'simple'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://vinicius:vinicius@192.168.100.2/Finan?driver=SQL+Server+Native+Client+10.0"
    SCHEDULER_API_ENABLED = True