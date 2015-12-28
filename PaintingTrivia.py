import random
from flask import request, session, render_template, Markup, redirect, url_for, Flask
from sqlalchemy.sql.functions import func
from models.painter import Painter
from models.painting import Painting
from settings import app
from database import users


@app.before_request
def set_session():
    # initialize the points in the user session
    if 'right_guesses' not in session:
        session['right_guesses'] = 0
        session['wrong_guesses'] = 0


@app.route('/')
def index():
    if 'username' in session:
        # return 'Logged in as %s' % Markup.escape(session['username'])
        print 'index to show entries'
        return redirect(url_for('show_entries'))
    else:
        print 'index to login'
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_aux = request.form['username']
        password_aux = request.form['password']
        if not(username_aux == '' or password_aux == ''):
            print username_aux, password_aux
            session['username'] = username_aux
            session['password'] = password_aux
            user_bool = users.add_user(username_aux, password_aux)
            if user_bool:
                return redirect(url_for('index'))
    return render_template('menu.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/play', methods=['GET', 'POST'])
def show_entries():
    # if the request is sent from a form
    if request.method == 'POST':
        key = 'right_guesses' if int(request.form['chosen_painter']) == session['selected_painter_id'] \
            else 'wrong_guesses'
        session[key] += 1

    painters = Painter.query.order_by(func.random()).limit(4).all()

    selected_painter = random.choice(painters)

    selected_painting = Painting.query.filter(Painting.painter == selected_painter).order_by(func.random()).limit(
        1).one()
    session['selected_painter_id'] = selected_painting.painter.id
    return render_template('show_entries.html',
                           painters=painters,
                           selected_painter=selected_painter,
                           selected_painting=selected_painting,
                           right_guesses=session['right_guesses'],
                           wrong_guesses=session['wrong_guesses'])


if __name__ == '__main__':
    app.run()
