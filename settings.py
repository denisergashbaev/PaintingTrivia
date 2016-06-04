from flask.app import Flask
from os.path import abspath, dirname

from flask.ext.login import LoginManager
from flask.ext.session import Session
from flask.ext.sqlalchemy import SQLAlchemy

DATABASE_FOLDER = abspath(dirname(__file__)) + '/database'
DATABASE = DATABASE_FOLDER + '/trivia.db'
SQLALCHEMY_DATABASE_URI = 'sqlite:////' + DATABASE
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

#use Flask-Session because we had problems storing session in cookies (default mechanism in Flask)
#bug: https://github.com/denisergashbaev/PaintingTrivia/issues/25
#https://pythonhosted.org/Flask-Session/
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

salt = 'asdfas213540808ljl(df'
login_manager = LoginManager(app)
login_manager.login_view = "login"

