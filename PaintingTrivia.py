import random
from flask import request, session, render_template, Markup, redirect, url_for, Flask, flash
from sqlalchemy.sql.expression import exists
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.expression import exists
from models.painter import Painter
from models.painting import Painting
from models.saint import Saint
from models.user import User
from settings import app
from settings import db


def valid_actions():
    return [login.__name__, register.__name__, logout.__name__, guess_the_saint.__name__, guess_the_painter.__name__,
            main_menu.__name__]


def layout_buttons():
    try:
        navigate_to = request.form['navigate_to']
    except KeyError:
        navigate_to = None
    if navigate_to in valid_actions():
        return redirect(url_for(navigate_to))


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
        return redirect(url_for('main_menu'))
    else:
        return redirect(url_for('menu'))


@app.route('/main', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        x = layout_buttons()
        if x:
            return x
    return render_template('menu.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        x = layout_buttons()
        if x:
            return x

        username_aux = request.form['username']
        password_aux = request.form['password']
        if username_aux and password_aux:
            # Check if the username exists
            retrieved_users = User.query.filter(User.name == username_aux).all()
            if retrieved_users:
                # Check if the password is correct
                if User.check_user_password(username_aux, password_aux):
                    session['username'] = username_aux
                    return redirect(url_for('index'))
                else:
                    flash('Password is wrong!', 'error')
                    return redirect(url_for('index'))
            else:
                flash('This user is not registered!', 'error')
                return redirect(url_for('register'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        x = layout_buttons()
        if x:
            return x
        username_aux = request.form['username']
        password_aux = request.form['password']
        if username_aux and password_aux:
            retrieved_users = User.query.filter(User.name == username_aux).all()
            if retrieved_users:
                # Check if the password is correct
                flash('User already exists', 'error')
            else:
                # Add the user
                session['username'] = username_aux
                User.add_user(username_aux, password_aux)
                db.session.commit()
                return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.clear()
    return redirect(url_for('index'))


@app.route('/main_menu', methods=['GET', 'POST'])
def main_menu():
    if request.method == 'POST':
        x = layout_buttons()
        if x:
            return x
    return render_template('main_menu.html', username=session['username'])


@app.route('/guessthepainter', methods=['GET', 'POST'])
def guess_the_painter():
    # if the request is sent from a form
    if request.method == 'POST':
        x = layout_buttons()
        if x:
            return x

        try:
            chosen_painter = int(request.form['chosen_painter'])
        except KeyError:
            chosen_painter = -1
        key = 'right_guesses' if chosen_painter == session[
            'selected_painter_id'] else 'wrong_guesses'
        session[key] += 1

    #http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#using-exists
    #the instructions below correspond to the following sql statement:
    # SELECT painter.id AS painter_id, painter.name AS painter_name FROM painter
    # WHERE EXISTS (SELECT * FROM painting WHERE painter.id = painting.painter_id)
    # ORDER BY random() LIMIT 4

    stmt = exists().where(Painter.id == Painting.painter_id)
    painters = Painter.query.filter(stmt).order_by(func.random()).limit(4).all()
    selected_painter = random.choice(painters)
    selected_painting = Painting.query.filter(Painting.painter == selected_painter).order_by(func.random()).limit(
        1).first()

    session['selected_painter_id'] = selected_painting.painter.id
    return render_template('guess_the_painter.html',
                           painters=painters,
                           selected_painter=selected_painter,
                           selected_painting=selected_painting,
                           right_guesses=session['right_guesses'],
                           wrong_guesses=session['wrong_guesses'],
                           username=session['username'])


@app.route('/guessthesaint', methods=['GET', 'POST'])
def guess_the_saint():
    # if the request is sent from a form
    if request.method == 'POST':
        x = layout_buttons()
        if x:
            return x
        try:
            chosen_painting = int(request.form['chosen_saint'])
        except KeyError:
            chosen_painting = -1

        key = 'right_guesses' if chosen_painting == session[
            'selected_saint_id'] else 'wrong_guesses'
        session[key] += 1

    # Select a painter who has at least a painting
    # stmt = exists().where(Saint.paintings.any(id==Painting.id))
    # painting_list = Painting.query.filter(stmt).order_by(func.random()).limit(4).all()

    saints_list = Saint.query.filter(Saint.paintings.any()).limit(4).all()
    selected_saint = random.choice(saints_list)

    selected_painting = Painting.query.filter(Painting.saints.any(id=selected_saint.id)).first()

    session['selected_saint_id'] = selected_saint.id
    return render_template('guess_the_saint.html',
                           saints_list=saints_list,
                           selected_painter=selected_painting.painter,
                           selected_saint=selected_saint,
                           selected_painting=selected_painting,
                           right_guesses=session['right_guesses'],
                           wrong_guesses=session['wrong_guesses'],
                           username=session['username'])


if __name__ == '__main__':
    # run on the machine ip address (local network)
    # http://stackoverflow.com/questions/7023052/flask-configure-dev-server-to-be-visible-across-the-network
    # app.run(host='0.0.0.0')
    # run on localhost
    app.run()
