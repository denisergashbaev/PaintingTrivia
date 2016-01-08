import random
from flask import request, session, render_template, Markup, redirect, url_for, Flask, flash
from sqlalchemy.sql.functions import func
from models.painter import Painter
from models.painting import Painting
from models.user import User
from settings import app
from database import users
from settings import db


def button_to_address(value):
    d = {
        'Login': login,
        'Register': register,
        'Logout': logout
    }
    return d[value] if value in d.keys() else None


def layout_buttons(request):
    if 'navigate_to' in request.form.keys():
        assert request.form['navigate_to'] in ['Login', 'Register', 'Logout']
        value = request.form['navigate_to']
        func = button_to_address(value)
        redirect_fun_name = func.__name__
        return redirect(url_for(redirect_fun_name))


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
        return redirect(url_for('show_entries'))
    else:
        return redirect(url_for('menu'))


@app.route('/main', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        x = layout_buttons(request)
        if x:
            return x
    return render_template('menu.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        x = layout_buttons(request)
        if x:
            return x
        username_aux = request.form['username']
        password_aux = request.form['password']
        if username_aux and password_aux:
            # Check if the username exists
            retrieved_users = User.query.filter(User.name == username_aux).all()
            if retrieved_users:
                # Check if the password is correct
                if users.check_user_password(username_aux, password_aux):
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
        x = layout_buttons(request)
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
                users.add_user(username_aux, password_aux)
                db.session.commit()
                return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.clear()
    return redirect(url_for('index'))


@app.route('/play', methods=['GET', 'POST'])
def show_entries():
    # if the request is sent from a form
    if request.method == 'POST':
        x = layout_buttons(request)
        if x:
            return x
        key = 'right_guesses' if int(request.form['chosen_painter']) == session[
            'selected_painter_id'] else 'wrong_guesses'
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
