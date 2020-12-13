from flask import request, json, session
from flask_socketio import join_room, emit

from . import socketio, helper, db, models


def reload(game_id):
    socketio.emit('page reload', room=game_id)


@socketio.on('join game')
def join_game(data):
    join_room(data['game_id'])
    emit('playground update', helper.get_playground(data['game_id']), room=request.sid)


@socketio.on('player join')
def join_game(data):
    game = models.Game.query.filter_by(id=data['game_id']).first()
    session['team'] = data['team']

    if data['team'] == 'red':
        members_red = json.loads(game.members_red)
        members_red.append(data['username'])
        game.members_red = json.dumps(members_red)
    else:
        members_blue = json.loads(game.members_blue)
        members_blue.append(data['username'])
        game.members_blue = json.dumps(members_blue)
    db.session.commit()
    emit('playground update', helper.get_playground(data['game_id']), room=data['game_id'])


@socketio.on('get playground')
def push_playground(data):
    emit('playground update', helper.get_playground(data['game_id']), room=data['game_id'])


@socketio.on('get spymaster')
def push_spymaster(data):
    emit('post spymaster', helper.get_playground(data['game_id'], spymaster=True), room=request.sid)


@socketio.on('field update')
def update_playground(data):
    field_id = data['field_id'].split('field-', 1)[1]

    game = models.Game.query.filter_by(id=data['game_id']).first()
    field = game.fields.filter_by(id=field_id).first()
    field.hidden = False

    if field.type == 'red':
        game.score_red -= 1
    elif field.type == 'blue':
        game.score_blue -= 1

    db.session.commit()

    if field.type == 'assassin':
        if session['team'] == 'red':
            emit('game won', 'blue', room=data['game_id'])
        else:
            emit('game won', 'red', room=data['game_id'])
    elif game.score_red == 0:
        emit('game won', 'red', room=data['game_id'])
    elif game.score_blue == 0:
        emit('game won', 'blue', room=data['game_id'])

    emit('playground update', helper.get_playground(data['game_id']), room=data['game_id'])
