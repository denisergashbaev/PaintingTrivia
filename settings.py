from flask.app import Flask
from os.path import abspath, dirname
from flask.ext.sqlalchemy import SQLAlchemy

DATABASE_FOLDER = abspath(dirname(__file__)) + '/database'
DATABASE = DATABASE_FOLDER + '/trivia.db'
SQLALCHEMY_DATABASE_URI = 'sqlite:////' + DATABASE
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)