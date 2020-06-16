from flask_socketio import join_room, emit

from . import socketio, helper, db, models


def refresh(game_id):
    socketio.emit('refresh', room=game_id)


@socketio.on('join game')
def join_game(data):
    game_id = data['game_id']
    join_room(game_id)
    emit('playground update', helper.get_playground(game_id), room=game_id)


@socketio.on('get playground')
def push_playground(data):
    game_id = data['game_id']
    emit('playground update', helper.get_playground(data['game_id']), room=game_id)


@socketio.on('get spymaster')
def push_spymaster(data):
    game_id = data['game_id']
    emit('spymaster', helper.get_playground(game_id, spymaster=True), room=game_id)


@socketio.on('field update')
def update_playground(data):
    game_id = data['game_id']
    field_id = data['field_id'].split('field-', 1)[1]

    field = models.Field.query.filter_by(id=field_id, game_id=game_id).first()
    field.hidden = False

    db.session.commit()

    emit('playground update', helper.get_playground(game_id), room=game_id)
