from flask import Flask
from flask_compress import Compress
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'LAX'
Compress(app)

app.game_modes = []

for mode in app.config['GAME_MODES']:
    if mode == 'pictures':
        DISPLAY_NAME = 'Pictures'
    elif mode.startswith('classic_'):
        lang = mode.split('classic_', 1)[1]
        DISPLAY_NAME = f'Classic ({lang})'
    else:
        continue
    app.game_modes.append((mode, DISPLAY_NAME))

socketio = SocketIO(app)
db = SQLAlchemy(app)

#from . import models, routes, helper, websocket

#: create database if not exists
db.create_all()

if __name__ == '__main__':
    #: start flask
    app.run()

    #: start websocket
    socketio.run(app)
