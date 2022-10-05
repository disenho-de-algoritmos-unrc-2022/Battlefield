import json
from flask import jsonify

import app.daos.underwater.submarine_dao as sub_dao
from app import db
from app.models.underwater.under_dtos import UnderGameSchema
from app.models.underwater.under_models import UnderGame, UnderBoard, boards
from app.models.user import User


class UnderGameDao:

    def __init__(self, game):
        self.game = game

    @staticmethod
    def create(host_id, height=10, width=20):
        if db.session.query(User).where(User.id == host_id) == None:
            return None

        game = UnderGame(host_id=host_id)
        db.session.add(game)
        db.session.commit()
        boards.update({game.id: UnderBoard(game.id, height, width)})
        return UnderGameDao(game)


    @staticmethod
    def get(game_id):
        game = db.session.query(UnderGame).where(UnderGame.id == game_id).one_or_none()
        if not game:
            raise ValueError("no game found with id %s" % game_id)
        return UnderGameDao(game)


    def update(self, host_id=None, visitor_id=None):
        if host_id != None:
            self.game.host_id = host_id
        if visitor_id != None:
            self.game.visitor_id = visitor_id

        db.session.commit()


    @staticmethod
    def get_options():
        options_json = open("app/models/underwater/options.json")
        options = json.load(options_json)
        return options


    def add_submarine(self, player_id, option_id):
        options = UnderGameDao.get_options()
        choosen = options[str(option_id)]

        if not self.has_user(player_id):
            raise Exception("the game does not have the specified player")

        for sub in self.game.submarines:
            if sub.player_id == player_id:
                raise Exception("Player already has a submarine")

        sub = sub_dao.create_submarine(
            self.game.id,
            player_id,
            choosen["name"],
            int(choosen["size"]),
            int(choosen["speed"]),
            int(choosen["visibility"]),
            int(choosen["radar_scope"]),
            float(choosen["health"]),
            int(choosen["torpedo_speed"]),
            float(choosen["torpedo_damage"]),
        )
        self.game.submarines.append(sub)
        db.session.commit()
        return sub


    def has_user(self, player_id):
        return self.game.host_id == player_id or self.game.visitor_id == player_id


    def place(self, obj, x_coord, y_coord, direction):
        if obj.is_placed():
            raise Exception("submarine is already placed")

        board = boards[obj.game.id]

        # if not board.segment_is_empty(x_coord, y_coord, direction, submarine.size):
        #     raise Exception("Given position is not available")
        try:
            board.place(obj, x_coord, y_coord, direction, obj.size)
        except Exception as e:
            raise Exception("%s" % str(e))

        obj.update_position(x_coord, y_coord, direction)

        db.session.commit()


    def contains_submarine(self, submarine_id):
        for sub in self.game.submarines:
            if sub.id == submarine_id:
                return True
        return False

    def jsonify(self):
        under_game_schema = UnderGameSchema()
        return jsonify(under_game_schema.drop(self.game))

    def get_visitor(self):
        return self.game.visitor

    def get_host(self):
        return self.game.host