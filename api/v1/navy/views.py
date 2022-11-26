from flask import jsonify, request
from marshmallow import ValidationError

from api import token_auth
from app.navy.daos.missile_type_dao import missile_type_dao
from app.navy.daos.ship_type_dao import ship_type_dao
from app.navy.dtos.navy_game_dto import NavyGameDTO
from app.navy.dtos.navy_game_state_dto import NavyGameStateDTO
from app.navy.services.action_service import action_service
from app.navy.services.navy_game_service import navy_game_service
from app.navy.services.ship_service import ship_service
from app.navy.utils.navy_response import NavyResponse
from app.navy.utils.navy_utils import utils
from app import io
from flask_socketio import join_room, leave_room
from . import navy


@io.on('action2')
def handle_action(data):
    print('received json: ' + str(data))

@io.on('join')
def on_join(data):
    room = data['room']
    join_room(room)

@io.on('message')
def handle_message(data):
    print('received message: ' + str(data))
    response ={
        "body": data['body'],
        "user": data['user']
    }
    io.send(response, broadcast=True,to=data['room'])


    

@navy.post("/actions")
@token_auth.login_required
def action():
    try:
        request.json["user_id"] = utils.get_user_id_from_header(
            request.headers["Authorization"]
        )
        validated_data = action_service.validate_request(request.json)
        action_service.add(validated_data)
        return (
            NavyResponse(201, data=request.json, message="Action added").to_json(),
            201,
        )
    except ValidationError as err:
        return NavyResponse(400, message=err.messages).to_json(), 400
    


@navy.post("/ships")
@token_auth.login_required
def new_ship():
    try:
        request.json["user_id"] = utils.get_user_id_from_header(
            request.headers["Authorization"]
        )
        validated_data = ship_service.validate_request(request.json)
        ship_service.add(validated_data)
        return (
            NavyResponse(201, data=validated_data, message="Ship added").to_json(),
            201,
        )
    except ValidationError as err:
        return NavyResponse(400, message=err.messages).to_json(), 400


@navy.post("/navy_games")
@token_auth.login_required
def new_navy_game():
    try:
        user1_id = utils.get_user_id_from_header(request.headers["Authorization"])
        created_game = navy_game_service.add({"user1_id": user1_id})
        return (
            NavyResponse(
                201, data=NavyGameDTO().dump(created_game), message="Game created."
            ).to_json(),
            201,
        )
    except ValidationError as err:
        return NavyResponse(400, message=err.messages).to_json(), 400


@navy.get("/navy_games")
@token_auth.login_required
def get_navy_games():
    games = navy_game_service.get_all()
    json_games = list(map(lambda game: NavyGameDTO().dump(game), games))
    return NavyResponse(status=200, data=json_games, message="Ok").to_json(), 200


@navy.get("/navy_games/<int:id>")
@token_auth.login_required
def get_navy_game(id):
    user_id = utils.get_user_id_from_header(request.headers["Authorization"])
    game = navy_game_service.get_by_id(id)
    return (
        NavyResponse(
            status=200, data=NavyGameStateDTO(game.id, user_id).dump(), message="Ok"
        ).to_json(),
        200,
    )


@navy.patch("/navy_games/<int:id>")
@token_auth.login_required
def update_navy_game(id):
    try:
        user2_id = utils.get_user_id_from_header(request.headers["Authorization"])
        validated_data = navy_game_service.validate_patch_request(
            {"user2_id": user2_id, "game_id": id}
        )
        game = navy_game_service.join(validated_data, id)
        return (
            NavyResponse(
                200, data=NavyGameDTO().dump(game), message="Game updated."
            ).to_json(),
            200,
        )
    except ValidationError as err:
        return NavyResponse(400, message=err.messages).to_json(), 400


@navy.delete("/navy_games/<int:id>")
@token_auth.login_required
def delete_navy_game(id):
    try:
        from app.navy.validators.delete_game_validator import DeleteGameValidator

        user_id = utils.get_user_id_from_header(request.headers["Authorization"])
        validated_data = DeleteGameValidator().load({"game_id": id, "user_id": user_id})
        deleted_game = navy_game_service.delete(validated_data["game_id"])
        return (
            NavyResponse(
                200, data=NavyGameDTO().dump(deleted_game), message="Game deleted."
            ).to_json(),
            200,
        )
    except ValidationError as err:
        return NavyResponse(400, message=err.messages).to_json(), 400


@navy.get("/ship_types")
@token_auth.login_required
def ship_types():
    ships = ship_type_dao.SHIP_TYPES
    return NavyResponse(status=200, data=ships, message="Ok").to_json(), 200


@navy.get("/missile_types")
@token_auth.login_required
def missile_types():
    missiles = missile_type_dao.MISSILE_TYPES
    return NavyResponse(status=200, data=missiles, message="Ok").to_json(), 200
