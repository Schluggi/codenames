from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, AnyOf

from . import app


class IndexForm(FlaskForm):
    game_name = StringField(validators=[DataRequired()], render_kw={"placeholder": "Give your game a name"})
    username = StringField(validators=[DataRequired()], render_kw={"placeholder": "Whats your name?"})
    game_mode = SelectField(validators=[DataRequired(), AnyOf(app.config['GAME_MODES'])], choices=app.game_modes)
    submit = SubmitField('Go!')


class GameForm(FlaskForm):
    game_mode = SelectField(validators=[AnyOf(app.config['GAME_MODES'])], choices=app.game_modes)
    submit = SubmitField('New Game')
