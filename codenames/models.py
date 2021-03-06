from . import db


class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    mode = db.Column(db.String(255), nullable=False)
    images = db.Column(db.Text, nullable=False)
    cards = db.Column(db.Text, nullable=False)
    score_red = db.Column(db.Integer)
    score_blue = db.Column(db.Integer)
    members_red = db.Column(db.Text, nullable=False, default='[]')
    members_blue = db.Column(db.Text, nullable=False, default='[]')
    start_score_red = db.Column(db.Integer)
    start_score_blue = db.Column(db.Integer)
    fields = db.relationship('Field', backref='game', lazy='dynamic')


class Field(db.Model):
    __tablename__ = 'fields'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False, primary_key=True)
    hidden = db.Column(db.Boolean, nullable=False, default=True)
    type = db.Column(db.String(8), nullable=False)
