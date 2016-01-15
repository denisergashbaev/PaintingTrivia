import random
from flask import request, session, render_template, Markup, redirect, url_for, Flask, flash
from sqlalchemy.sql.functions import func
from models.painter import Painter
from models.painting import Painting
from models.user import User
from settings import app
from settings import db


def valid_actions():
    return [login.__name__, register.__name__, logout.__name__, guess_the_saint.__name__, guess_the_painter.__name__,  main_menu.__name__]


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

    # Select a painter who has at least a painting
    selected_painter, selected_painting = db.session.query(Painter, Painting).order_by(func.random()).filter(
        Painter.id == Painting.painter_id).limit(1).first()

    # Select three other painters
    painters_list = Painter.query.filter(Painter.id != selected_painter.id).order_by(func.random()).limit(3).all()

    painters_list.append(selected_painter)
    random.shuffle(painters_list)

    session['selected_painter_id'] = selected_painting.painter.id
    return render_template('guess_the_painter.html',
                           painters=painters_list,
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
            chosen_painter = int(request.form['chosen_painter'])
        except KeyError:
            chosen_painter = -1

        key = 'right_guesses' if chosen_painter == session[
            'selected_painter_id'] else 'wrong_guesses'
        session[key] += 1

    # Select a painter who has at least a painting
    selected_painter, selected_painting = db.session.query(Painter, Painting).order_by(func.random()).filter(
        Painter.id == Painting.painter_id).limit(1).first()

    # Select three other painters
    painters_list = Painter.query.filter(Painter.id != selected_painter.id).order_by(func.random()).limit(3).all()

    painters_list.append(selected_painter)
    random.shuffle(painters_list)

    session['selected_painter_id'] = selected_painting.painter.id
    return render_template('guess_the_saint.html',
                           painters=painters_list,
                           selected_painter=selected_painter,
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
