# pylint: disable=import-error
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, AnyOf

from . import app


class IndexForm(FlaskForm):
    game_name = StringField(validators=[DataRequired()], render_kw={"placeholder": "Give your game a name"})
    game_mode = SelectField(validators=[DataRequired(), AnyOf(app.config['GAME_MODES'])], choices=app.game_modes)
    start_game = SubmitField('Start or join game!')


class GameForm(FlaskForm):
    game_mode = SelectField(validators=[AnyOf(app.config['GAME_MODES'])], choices=app.game_modes)
    new_round = SubmitField('New Round')
