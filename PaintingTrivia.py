import pickle

from flask import request, session, render_template, redirect, url_for, flash

from Quiz import PainterQuiz, SaintQuiz
from models.painter import Painter
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


def initialize_quiz():
    if 'quiz' not in session:
        session['quiz'] = None


@app.before_request
def set_session():
    # initialize the points in the user session
    initialize_quiz()


@app.route('/')
def index():
    if 'username' in session:
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


@app.route('/results', methods=['GET', 'POST'])
def show_quiz_results():
    if request.method == 'POST':
        # Clear session
        session.pop('quiz')
        x = layout_buttons()
        if x:
            return x
    quiz = pickle.loads(session['quiz'])
    return render_template('show_quiz_results.html',
                           right_guesses=sum(quiz.score),
                           wrong_guesses=len(quiz.score) - sum(quiz.score),
                           username=session['username'])


@app.route('/guessthepainter', methods=['GET', 'POST'])
def guess_the_painter():
    # if the request is sent from a form
    if request.method == 'POST':
        x = layout_buttons()
        if x:
            return x

        try:
            quiz = pickle.loads(session['quiz'])
            chosen_painter_id = int(request.form['chosen_painter'])
            question = quiz.current_question
            quiz.process_answer(question, chosen_painter_id == question.correct_option.id)
            session['quiz'] = pickle.dumps(quiz)
        except KeyError:
            print "Something failed"

            # http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#using-exists

    # the instructions below correspond to the following sql statement:
    #  SELECT painter.id AS painter_id, painter.name AS painter_name FROM painter
    # WHERE EXISTS (SELECT * FROM painting WHERE painter.id = painting.painter_id)
    # ORDER BY random() LIMIT 4
    if session['quiz'] is None:
        # Obtain the painters and the paintings randomly
        selected_painters, selected_paintings = initialize_images(num_painters=10)
        quiz = PainterQuiz(selected_paintings, selected_painters)
        session['quiz'] = pickle.dumps(quiz)
    else:
        quiz = pickle.loads(session['quiz'])

    # If all of the images have been seen, show again, the incorrect ones
    question = quiz.next_question()

    session['quiz'] = pickle.dumps(quiz)
    if not question:
        return redirect(url_for('show_quiz_results'))
    return render_template('guess_the_painter.html',
                           quiz=quiz,
                           username=session['username'])


@app.route('/guessthesaint', methods=['GET', 'POST'])
def guess_the_saint():
    # if the request is sent from a form
    if request.method == 'POST':
        x = layout_buttons()
        if x:
            return x

        try:
            quiz = pickle.loads(session['quiz'])
            chosen_saint_id = int(request.form['chosen_saint'])
            question = quiz.current_question
            quiz.process_answer(question, chosen_saint_id == question.correct_option.id)
            session['quiz'] = pickle.dumps(quiz)
        except KeyError:
            print "Something failed"

    if session['quiz'] is None:
        # Obtain the saints and the paintings randomly
        selected_saints, selected_paintings = initialize_saint_images(num_saints=10)
        quiz = SaintQuiz(selected_paintings, selected_saints)
        session['quiz'] = pickle.dumps(quiz)
    else:
        quiz = pickle.loads(session['quiz'])

    # If all of the images have been seen, show again, the incorrect ones
    question = quiz.next_question()

    session['quiz'] = pickle.dumps(quiz)
    if not question:
        return redirect(url_for('show_quiz_results'))

    chosen_painting = question.element.values()[0]

    return render_template('guess_the_saint.html',
                           quiz=quiz,
                           selected_painter=Painter.query.filter(Painter.id == chosen_painting.painter_id).first(),
                           username=session['username'])


if __name__ == '__main__':
    app.run()
