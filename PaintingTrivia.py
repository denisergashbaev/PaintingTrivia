import random

from flask import request, session, render_template

from sqlalchemy.sql.functions import func
from models.painter import Painter
from models.painting import Painting
from settings import app


@app.before_request
def set_session():
    # initialize the points in the user session
    if 'right_guesses' not in session:
        session['right_guesses'] = 0
        session['wrong_guesses'] = 0


@app.route('/', methods=['GET', 'POST'])
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
