import random
from flask import request, session, render_template, Markup, redirect, url_for, Flask, flash
from sqlalchemy.sql.functions import func
from models.painter import Painter
from models.painting import Painting
from models.user import User
from settings import app
from database import users
from settings import db


def layout_buttons(request):
    print request.form.values(), request.__dict__.keys()
    print request.form
    if 'Login' in request.form.values():
        return redirect(url_for('login'))
    if 'Register' in request.form.values():
        return redirect(url_for('register'))
    if 'Logout' in request.form.values():
        return redirect(url_for('logout'))


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
        print 'Hey'
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
        if not (username_aux == '' or password_aux == ''):
            # Check if the username exists
            retrieved_users = User.query.filter(User.name == username_aux).order_by(func.random()).all()
            if retrieved_users:
                # Check if the password is correct
                if retrieved_users[0].password == password_aux:
                    session['username'] = username_aux
                    session['password'] = password_aux
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
        if not (username_aux == '' or password_aux == ''):
            session['username'] = username_aux
            session['password'] = password_aux
            retrieved_users = User.query.filter(User.name == username_aux).order_by(func.random()).all()
            if retrieved_users:
                # Check if the password is correct
                flash('User already exists', 'error')
            else:
                # Add the user
                session['username'] = username_aux
                session['password'] = password_aux
                users.add_user(username_aux, password_aux)
                db.session.commit()
                return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('password', None)
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
