# all the imports
import sqlite3
import random
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, Markup
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


# http://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
# https://docs.python.org/2/library/sqlite3.html#sqlite3.Connection.row_factory
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def connect_db():
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = dict_factory
    return con


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource(DATABASE_FOLDER + '/schema.sql', mode='r') as f:
            print "importing schema"
            db.cursor().executescript(f.read())

        # check if there is data in the database. if so don't update
        cur = db.cursor().execute('SELECT COUNT(id) as count FROM painting')
        painting_count = cur.fetchone()['count']
        print "painting count is %s" % painting_count
        if painting_count == 0:
            with app.open_resource(DATABASE_FOLDER + '/populate.sql', mode='r') as f:
                db.cursor().executescript(f.read())
                print "populating the database"

        db.commit()


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % Markup.escape(session['username'])
    else:
        redirect(url_for('login'))
    return 'You are not logged in'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('show_entries'))
    return render_template('menu.html')


@app.route('/game', methods=['GET', 'POST'])
def show_entries():
    # initialize the points in the user session
    if 'right_guesses' not in session:
        session['right_guesses'] = 0
        session['wrong_guesses'] = 0

    # if the request is sent from a form
    if request.method == 'POST':
        if int(request.form['chosen_painter']) == session['selected_painting']['id']:
            session['right_guesses'] += 1
        else:
            session['wrong_guesses'] += 1

    # fetch 4 random paintings
    sql = 'SELECT * FROM painter ORDER BY RANDOM() LIMIT 4'
    painters = g.db.execute(sql).fetchall()

    # select the first painter (it is random because the records were selected randomly)
    selected_painter = random.choice(painters)

    # http://stackoverflow.com/questions/2279706/select-random-row-from-an-sqlite-table
    sql = 'SELECT * FROM painting WHERE fk_painter_id = ? ORDER BY RANDOM() LIMIT 1'
    cur = g.db.execute(sql, [selected_painter['id']])
    selected_painting = cur.fetchone()
    session['selected_painting'] = selected_painting
    return render_template('show_entries.html',
                           painters=painters,
                           selected_painter=selected_painter,
                           selected_painting=selected_painting,
                           right_guesses=session['right_guesses'],
                           wrong_guesses=session['wrong_guesses'])


if __name__ == '__main__':
    init_db()
    app.run()
