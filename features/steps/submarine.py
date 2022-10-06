import json

from behave import *
from flask import url_for

from app import db
from app.daos.underwater.under_game_dao import UnderGameDao
from app.daos.user_dao import add_user
from app.models.underwater.under_models import Submarine, UnderGame, boards
from app.models.user import User

# BACKGROUND


@given("there exists two users and they are logged in")
def step_impl(context):

    for row in context.table:
        add_user(row["username"], row["password"], row["email"])

    context.player1 = (
        db.session.query(User).where(User.username == "player1").one_or_none()
    )

    context.player2 = (
        db.session.query(User).where(User.username == "player2").one_or_none()
    )
    assert context.player1
    assert context.player2


# CREATE A NEW GAME


@when("the user 'player1' asks for a new underwater game")
def step_impl(context):
    context.page = context.client.get(
        url_for("underwater.new_game", host_id=context.player1.id)
    )
    assert context.page


@then("A new game is registered")
def step_impl(context):
    data = json.loads(context.page.text)
    context.game_dao = UnderGameDao.get(data["id"])
    assert context.game_dao


@then("an empty board with one player is returned")
def step_impl(context):
    board = boards[context.game_dao.get_id()]
    for row in board.matrix:
        for cell in row:
            assert cell is None
    assert context.game_dao.get_host()


# JOIN A GAME


@given("there is a game with no visitor")
def step_impl(context):
    context.game_dao = UnderGameDao.create(host_id=context.player1.id)
    assert context.game_dao


@when("the user 'player2' joins that game")
def step_impl(context):
    context.page = context.client.get(
        url_for(
            "underwater.join_game",
            game_id=context.game_dao.get_id(),
            visitor_id=context.player2.id,
        )
    )
    assert context.page.status_code is 200


@then("the game now has the new visitor")
def step_impl(context):
    assert context.game_dao.get_visitor().id == context.player2.id


# GET THE SUBMARINE OPTIONS


@when("I receive a request to show the submarine options")
def step_impl(context):
    context.page = context.client.get(url_for("underwater.get_options"))
    assert context.page


@then("the options are returned")
def step_impl(context):
    options = json.loads(context.page.text)
    assert "0" in options
    assert "1" in options
    assert "2" in options
    assert "3" in options


# CHOOSE A SUBMARINE


@given("the user 'player1' is in a game of dimension '{h:d}'x'{w:d}' with visitor")
def step_impl(context, h, w):
    context.game_dao = UnderGameDao.create(context.player1.id, context.player2.id, h, w)
    assert context.game_dao


@when("the user 'player1' chooses a submarine")
def step_impl(context):
    data = {
        "game_id": context.game_dao.get_id(),
        "player_id": context.player1.id,
        "submarine_id": 1,
    }
    context.page = context.client.post(
        url_for("underwater.choose_submarine"), data=data
    )


@then("the game bounds the user to the choosen submarine successfully")
def step_impl(context):
    # game_dao = UnderGameDao.get(context.game.id)
    # assert game_dao..submarines[0].player_id == context.player1.id
    # assert context.game
    submarines = context.game_dao.get_submarines()
    print(submarines)
    assert submarines[0].player_id == context.player1.id
    assert context.page.status_code is 200


# CHOOSE AN EXTRA SUBMARINE


@then("the system should not allow to have an extra submarine")
def step_impl(context):
    print(context.page.text)
    assert "Player already has a submarine" in context.page.text
    # assert context.page.status_code is 409


# PLACE A SUBMARINE


@given("the user '{username}' chose '{sub_name}' submarine")
def step_impl(context, username, sub_name):
    player = (
        context.player1 if (context.player1.username == username) else context.player2
    )
    submarines = json.load(open("app/models/underwater/options.json"))
    for key in submarines.keys():
        if submarines[key]["name"] == sub_name:
            chosen_id = key
    assert context.game_dao.add_submarine(player.id, chosen_id)


@when(
    "the user '{username}' chooses the position '{x:d}','{y:d}' and direction '{d:d}'"
)
def step_impl(context, username, x, y, d):
    player = (
        context.player1 if (context.player1.username == username) else context.player2
    )
    submarine = player.submarine[0]
    data = {
        "submarine_id": submarine.id,
        "x_coord": x,
        "y_coord": y,
        "direction": d,
    }
    context.page = context.client.post(url_for("underwater.place_submarine"), data=data)


@then("the submarine is successfully placed")
def step_impl(context):
    assert context.page.status_code is 200


# PLACE A SUBMARINE IN AN INVALID POSITION


@Then("the system should not allow to place the submarine in that position")
def step_impl(context):
    assert "Invalid coordinates" in context.page.text


# PLACE A SUBMARINE ALREADY PLACED


@Then("the system should not allow to place the submarine again")
def step_impl(context):
    print(context.page.text)
    assert "submarine is already placed" in context.page.text
