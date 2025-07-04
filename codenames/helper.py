# pylint: disable=too-many-locals
import random
from os import listdir
from os.path import join as join_path

from flask import json

from . import models, db, app

image_types = ['red', 'blue', 'neutral', 'assassin']


def get_playground(game_id: int, spymaster: bool = False) -> dict:
    #: get the current game and get all field ids of this game
    game = models.Game.query.filter_by(id=game_id).first()
    if not game:
        return {}
    fields = game.fields.with_entities(models.Field.id)

    playground = {
        'fields': {},
        'spymaster': spymaster,
        'img': json.loads(game.cards),
        'score': {
            'red': game.score_red,
            'blue': game.score_blue
        },
        'members': {
            'red': json.loads(game.members_red),
            'blue': json.loads(game.members_blue)
        },
        'start_score': {
            'red': game.start_score_red,
            'blue': game.start_score_blue
        }
    }

    for field_type in image_types:
        if spymaster:
            #: get all fields
            playground['fields'][field_type] = [f[0] for f in fields.filter_by(type=field_type).all()]
        else:
            #: get only fields that are not hidden
            playground['fields'][field_type] = [f[0] for f in fields.filter_by(type=field_type, hidden=False).all()]

    return playground


def new_game(game_name: str, game_mode: str, new_round: bool = False):
    #: get random field images and create chunks
    mode = join_path(*game_mode.split('_', 1))
    images_codes = [join_path(mode, img) for img in listdir(join_path(app.root_path, 'static/img/codes/', mode))
                    if img.endswith(('.jpeg', '.jpg', '.png', '.webp'))]
    images_codes = random.sample(images_codes, 20)
    images_codes = list(zip(images_codes, range(1, 21)))
    image_chunks = [images_codes[i:i + 5] for i in range(0, 20, 5)]

    cards = {}

    #: get all card images grouped by type
    for card_type in image_types:
        card_list = [img for img in listdir(join_path(app.root_path, f'static/img/cards/{card_type}'))
                     if img.endswith(('.jpeg', '.jpg', '.png', '.webp'))]
        random.shuffle(card_list)
        cards[card_type] = card_list

    if new_round:
        #: get the current game and set new images for cards and fields
        game = models.Game.query.filter_by(name=game_name).first()
        game.images = json.dumps(image_chunks)
        game.cards = json.dumps(cards)
        game.mode = game_mode
        game.members_red = '[]'
        game.members_blue = '[]'

        #: delete all fields
        for field in game.fields:
            db.session.delete(field)
    else:
        #: create a new game
        game = models.Game(name=game_name, mode=game_mode, images=json.dumps(image_chunks),
                           cards=json.dumps(cards))
        db.session.add(game)

    #: commit sql changes (necessary because otherwise we have no game id)
    db.session.commit()

    #: generate fields
    fields = list(range(1, 21))

    #: select red fields
    fields_red = random.sample(fields, random.choice([7, 8]))
    game.score_red = len(fields_red)
    game.start_score_red = game.score_red
    for field_id in fields_red:
        fields.pop(fields.index(field_id))
        db.session.add(models.Field(game_id=game.id, id=field_id, type='red'))

    #: select blue fields
    fields_blue = random.sample(fields, 15 - game.score_red)
    game.score_blue = len(fields_blue)
    game.start_score_blue = game.score_blue
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

    #: commit sql changes
    db.session.commit()
