from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class IndexForm(FlaskForm):
    game_name = StringField(validators=[DataRequired()], render_kw={"placeholder": "Give your game a name"})
    username = StringField(validators=[DataRequired()], render_kw={"placeholder": "Whats your name?"})
    submit = SubmitField('Go!')


class GameForm(FlaskForm):
    submit = SubmitField('New Game')
