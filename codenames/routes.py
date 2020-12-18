from flask import render_template, redirect, url_for, flash, make_response, session, json

from . import app, models, helper, websocket
from .forms import IndexForm, GameForm


@app.route('/', methods=['GET', 'POST'])
def index():
    form = IndexForm()
    if form.validate_on_submit():
        #: check if the game already exists
        if not models.Game.query.filter_by(name=form.game_name.data).first():
            #: create a new game
            helper.new_game(form.game_name.data, form.game_mode.data)

        return redirect(url_for('games', game_name=form.game_name.data))
    return render_template('index.html', form=form)


@app.route('/g/<game_name>', methods=['GET', 'POST'])
@app.route('/g/')
def games(game_name=None):
    form = GameForm()
    game = models.Game.query.filter_by(name=game_name).first()

    if not game:
        return redirect(url_for('index'))

    session['game_id'] = game.id

    if form.validate_on_submit():
        #: create a new game
        if form.game_mode.data:
            game_mode = form.game_mode.data
        else:
            game_mode = game.mode
        helper.new_game(game_name, game_mode, new_round=True)

        #: all clients have to reload the website
        websocket.reload(game.id)

    #: get the field image chunks from database
    image_chunks = json.loads(game.images)

    return render_template('game.html', rows=image_chunks, game=game, form=form, game_modes=app.game_modes)


@app.route('/static/js/game.js')
def game():
    resp = make_response(render_template('js/game.js'))
    resp.headers['Content-type'] = 'text/javascript;charset=UTF-8'
    return resp


@app.errorhandler(500)
def error_500(_):
    flash('Game error occurred', category='error')
    return redirect(url_for('index'))


@app.errorhandler(404)
def error_404(_):
    flash('Game not found', category='error')
    return redirect(url_for('index'))
