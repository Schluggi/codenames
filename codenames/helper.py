import random
from os import listdir
from os.path import join as join_path

import flask

from . import models, db, app


def get_playground(game_id, spymaster=False):  #: Todo optimize
    game = models.Game.query.filter_by(id=game_id).first()
    if not game:
        print('[INFO] Game is unavailable')
        return

    fields = game.fields.all()

    all_fields_blue = [f.id for f in fields if f.type == 'blue']
    all_fields_red = [f.id for f in fields if f.type == 'red']

    shown_fields_blue = [f.id for f in fields if f.type == 'blue' and f.hidden is False]
    shown_fields_red = [f.id for f in fields if f.type == 'red' and f.hidden is False]

    if spymaster:
        fields_blue = all_fields_blue
        fields_red = all_fields_red
        fields_neutral = [f.id for f in fields if f.type == 'neutral']
        fields_assassin = [f.id for f in fields if f.type == 'assassin']
    else:
        fields_blue = shown_fields_blue
        fields_red = shown_fields_red
        fields_neutral = [f.id for f in fields if f.type == 'neutral' and f.hidden is False]
        fields_assassin = [f.id for f in fields if f.type == 'assassin' and f.hidden is False]

    playground = {
        'spymaster': spymaster,
        'fields': {
            'blue': fields_blue,
            'red': fields_red,
            'neutral': fields_neutral,
            'assassin': fields_assassin
        },
        'score': {
            'red': len(all_fields_red) - len(shown_fields_red),
            'blue': len(all_fields_blue) - len(shown_fields_blue)
        },
        'img': flask.json.loads(game.cards)
        }
    return playground


def new_game(game_name, new_round=False):  #: Todo: optimize
    #: select random images and create chunks
    images_codes = [img for img in listdir(join_path(app.root_path, 'static/img/codes/'))
                    if img.endswith(('.jpeg', '.jpg'))]
    if len(images_codes) < 20:
        print('[ERROR] Number of code images is less than 20')
        return

    images_codes = random.sample(images_codes, 20)
    images_codes = list(zip(images_codes, range(1, 21)))
    image_chunks = [images_codes[i:i + 5] for i in range(0, 20, 5)]

    cards = {}
    for card_type in ['red', 'blue', 'neutral', 'assassin']:
        card_list = [img for img in listdir(join_path(app.root_path, 'static/img/cards/{}'.format(card_type)))
                     if img.endswith(('.jpeg', '.jpg'))]
        random.shuffle(card_list)
        cards[card_type] = card_list

    if new_round:
        #: delete all fields
        game = models.Game.query.filter_by(name=game_name).first()
        game.images = flask.json.dumps(image_chunks)
        game.cards = flask.json.dumps(cards)
        for field in game.fields:
            db.session.delete(field)
    else:
        #: create a new game
        game = models.Game(name=game_name, images=flask.json.dumps(image_chunks), cards=flask.json.dumps(cards))
        db.session.add(game)

    db.session.commit()

    #: generate fields
    fields = list(range(1, 21))

    #: select red fields
    fields_red = random.sample(fields, random.choice([7, 8]))
    for field_id in fields_red:
        fields.pop(fields.index(field_id))
        db.session.add(models.Field(game_id=game.id, id=field_id, type='red'))

    #: select blue fields
    fields_blue = random.sample(fields, 15 - len(fields_red))
    for field_id in fields_blue:
        fields.pop(fields.index(field_id))
        db.session.add(models.Field(game_id=game.id, id=field_id, type='blue'))

    #: select assassin
    assassin = random.choice(fields)
    db.session.add(models.Field(game_id=game.id, id=assassin, type='assassin'))
    fields.pop(fields.index(assassin))

    #: everything else is neutral
    for field_id in fields:
        db.session.add(models.Field(game_id=game.id, id=field_id, type='neutral'))

    db.session.commit()
