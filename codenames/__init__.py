from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

socketio = SocketIO(app)
db = SQLAlchemy(app)

from . import models, routes, helper, websocket

#: create database if not exists
db.create_all()

if __name__ == '__main__':
    #: start flask
    app.run()

    #: start websocket
    socketio.run(app)


