import random

from flask import request, session, render_template

# configuration
from sqlalchemy.sql.functions import func
from models.painter import Painter
from models.painting import Painting
from settings import app


@app.route('/', methods=['GET', 'POST'])
def show_entries():
    #initialize the points in the user session
    if 'right_guesses' not in session:
        session['right_guesses'] = 0
        session['wrong_guesses'] = 0
    #if the request is sent from a form
    if request.method == 'POST':
        if int(request.form['chosen_painter']) == session['selected_painter_id']:
            session['right_guesses'] += 1
        else:
            session['wrong_guesses'] += 1

    # WAS
    # fetch 4 random paintings
    #sql = 'SELECT * FROM painter ORDER BY RANDOM() LIMIT 4'
    #painters = g.db.execute(sql).fetchall()
    painters = Painter.query.order_by(func.random()).limit(4).all()

    #select the first painter (it is random because the records were selected randomly)
    selected_painter = random.choice(painters)

    #WAS
    #http://stackoverflow.com/questions/2279706/select-random-row-from-an-sqlite-table
    #sql = 'SELECT * FROM painting WHERE fk_painter_id = ? ORDER BY RANDOM() LIMIT 1'
    #cur = g.db.execute(sql, [selected_painter['id']])
    #selected_painting = cur.fetchone()
    selected_painting = Painting.query.filter(Painting.painter == selected_painter).order_by(func.random()).limit(1).one()
    session['selected_painter_id'] = selected_painting.painter.id
    return render_template('show_entries.html',
                           painters=painters,
                           selected_painter=selected_painter,
                           selected_painting=selected_painting,
                           right_guesses=session['right_guesses'],
                           wrong_guesses=session['wrong_guesses'])

if __name__ == '__main__':
    app.run()
