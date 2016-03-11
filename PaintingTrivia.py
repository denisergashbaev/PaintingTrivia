import pickle

from flask import request, session, render_template, redirect, url_for, flash
from flask.ext.login import login_required, login_user, logout_user

from models.painter import Painter
from models.user import User
from quiz import PainterQuiz, SaintQuiz
from settings import app, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.get_user_by_id(user_id)


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
    session['quiz'] = None


@app.route('/main', methods=['GET', 'POST'])
@login_required
def menu():
    if request.method == 'POST':
        x = layout_buttons()
        if x:
            return x
    initialize_quiz()
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
            # Check if the password is correct
            user = User.get_user(username_aux, password_aux)
            if user:
                login_user(user)
                return redirect(url_for('main_menu'))
            else:
                flash('Invalid username/password', 'error')
                return redirect(url_for('register'))
    initialize_quiz()
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
            # try to add the user to the database
            user = User.add_user(username_aux, password_aux)
            if user:
                login_user(user)
                return redirect(url_for('main_menu'))
            else:
                # Check if the password is correct
                flash('User already exists', 'error')
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_menu'))


@app.route('/', methods=['GET', 'POST'])
@app.route('/main_menu', methods=['GET', 'POST'])
@login_required
def main_menu():
    if request.method == 'POST':
        x = layout_buttons()
        if x:
            return x
    initialize_quiz()
    return render_template('main_menu.html')


@app.route('/results', methods=['GET', 'POST'])
@login_required
def show_quiz_results():
    if request.method == 'POST':
        # Clear session
        session.pop('quiz')
        x = layout_buttons()
        if x:
            initialize_quiz()
            return x
    quiz = pickle.loads(session['quiz'])
    redirect_to = request.args['redirect_to']
    return render_template('show_quiz_results.html',
                           quiz=quiz,
                           redirect_to=redirect_to)


@app.route('/guessthepainter', methods=['GET', 'POST'])
@login_required
def guess_the_painter():
    # if the request is sent from a form
    if request.method == 'POST':
        x = layout_buttons()
        if x:
            return x

        try:
            quiz = pickle.loads(session['quiz'])
            chosen_painter_id = int(request.form['chosen_painter'])
            quiz.process_answer(chosen_painter_id)
        except KeyError:
            quiz = PainterQuiz()
        session['quiz'] = pickle.dumps(quiz)

        # http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#using-exists

    # the instructions below correspond to the following sql statement:
    #  SELECT painter.id AS painter_id, painter.name AS painter_name FROM painter
    # WHERE EXISTS (SELECT * FROM painting WHERE painter.id = painting.painter_id)
    # ORDER BY random() LIMIT 4
    if session['quiz'] is None:
        # Obtain the painters and the paintings randomly
        quiz = PainterQuiz()
        session['quiz'] = pickle.dumps(quiz)
    else:
        quiz = pickle.loads(session['quiz'])

    # If all of the images have been seen, show again, the incorrect ones
    question = quiz.next_question()

    session['quiz'] = pickle.dumps(quiz)
    if not question:
        return redirect(url_for('show_quiz_results', redirect_to='guess_the_painter'))
    return render_template('guess_the_painter.html',
                           quiz=quiz)


@app.route('/guessthesaint', methods=['GET', 'POST'])
@login_required
def guess_the_saint():
    # if the request is sent from a form
    if request.method == 'POST':
        x = layout_buttons()
        if x:
            return x

        quiz = pickle.loads(session['quiz'])
        chosen_saint_id = int(request.form['chosen_saint'])
        quiz.process_answer(chosen_saint_id)
        session['quiz'] = pickle.dumps(quiz)

    if session['quiz'] is None:
        # Obtain the saints and the paintings randomly
        quiz = SaintQuiz()
        session['quiz'] = pickle.dumps(quiz)
    else:
        quiz = pickle.loads(session['quiz'])

    # If all of the images have been seen, show again, the incorrect ones
    question = quiz.next_question()

    session['quiz'] = pickle.dumps(quiz)
    if not question:
        return redirect(url_for('show_quiz_results', redirect_to='guess_the_saint'))

    chosen_painting = question.element

    return render_template('guess_the_saint.html',
                           quiz=quiz,
                           selected_painter=Painter.query.filter(Painter.id == chosen_painting.painter_id).first())


# http://stackoverflow.com/a/13161594
@app.route("/all-links")
def site_map():
    def has_no_empty_params(rule):
        defaults = rule.defaults if rule.defaults is not None else ()
        arguments = rule.arguments if rule.arguments is not None else ()
        return len(defaults) >= len(arguments)

    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return render_template("all_links.html", links=links)

if __name__ == '__main__':
    app.run()
