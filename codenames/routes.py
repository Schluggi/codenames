import flask.json
from flask import render_template, redirect, url_for

from . import app, models, helper, websocket
from .forms import IndexForm, GameForm


@app.route('/', methods=['GET', 'POST'])
def index():
    form = IndexForm()
    if form.validate_on_submit():

        #: check if the game already exists
        if not models.Game.query.filter_by(name=form.game_name.data).first():
            helper.new_game(form.game_name.data)

        return redirect(url_for('games', game_name=form.game_name.data))
    return render_template('index.html', form=form)


@app.route('/games/<game_name>', methods=['GET', 'POST'])
@app.route('/games/')
def games(game_name=None):
    form = GameForm()
    game = models.Game.query.filter_by(name=game_name).first()

    if form.validate_on_submit():
        helper.new_game(game_name, new_round=True)
        websocket.reload(game.id)

    if not game:
        return redirect(url_for('index'))

    image_chunks = flask.json.loads(game.images)

    return render_template('game.html', rows=image_chunks, game=game, form=form)
