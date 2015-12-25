# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from os.path import abspath, dirname

# configuration
DATABASE_FOLDER = abspath(dirname(__file__)) + '/database'
DATABASE = DATABASE_FOLDER + '/trivia.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource(DATABASE_FOLDER + '/schema.sql', mode='r') as f:
            print "importing schema"
            db.cursor().executescript(f.read())

        #check if there is data in the database. if so don't update
        cur = db.cursor().execute('SELECT COUNT(id) FROM painting')
        painting_count = cur.fetchall()[0][0]
        print "painting count is %s" % painting_count
        if painting_count == 0:
            with app.open_resource(DATABASE_FOLDER + '/populate.sql', mode='r') as f:
                db.cursor().executescript(f.read())
                print "populating the database"

        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_entries():
    cur = g.db.execute('SELECT title, file_name FROM painting')
    entries = [dict(title=row[0], file_name=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

if __name__ == '__main__':
    init_db()
    app.run()
