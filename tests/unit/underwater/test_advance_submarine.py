from app.models.user import User
from battlefield import app
from tests.unit.underwater.test_generate_game import generate_game


def test_crash_submarine_and_live():
    with app.app_context():

        #         0    1    2    3    4    5
        #      -------------------------------
        #   0  |    |    | s0 | s1 |    |    |
        #   1  |    |    |    | s2 |    |    |
        #   2  |    |    |    | s0 |    |    |
        #   3  |    |    |    | s0 |    |    |
        #   4  |    |    |    | s0 |    |    |
        #   5  |    |    |    |    |    |    |
        #      -------------------------------

        # GENERATE GAME
        host = User("player1", "player1", "player1@mail.com")
        visitor = User("player2", "player2", "player2@mail.com")
        players = {"host": host, "visitor": visitor}
        sub_list = [
            {
                "player": host,
                "chosen_id": 0,
                "health": 10,
                "x_coord": 0,
                "y_coord": 3,
                "direction": 2,
            },
            {
                "player": visitor,
                "chosen_id": 3,
                "health": 50,
                "x_coord": 1,
                "y_coord": 3,
                "direction": 0,
            },
        ]  # size = 4
        tor_list = []
        game = generate_game(6, 6, players, sub_list, tor_list)
        sub1 = game.submarines[0]
        sub2 = game.submarines[1]

        # ACTION TO TEST
        game.advance_object(sub2, 1)

        # ASSERT
        expected_board = [
            [None, None, None, sub2, None, None],
            [None, None, None, sub2, None, None],
            [None, None, None, sub2, None, None],
            [None, None, None, sub2, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
        ]

        assert game.board.matrix == expected_board
        assert sub2.health == 40
        assert len(game.submarines) == 1
        assert game.is_finished()


def test_crash_submarine_and_die():
    with app.app_context():

        #         0    1    2    3    4    5
        #      -------------------------------
        #   0  |    |    | s0 | s1 |    |    |
        #   1  |    |    |    | s2 |    |    |
        #   2  |    |    |    | s0 |    |    |
        #   3  |    |    |    | s0 |    |    |
        #   4  |    |    |    | s0 |    |    |
        #   5  |    |    |    |    |    |    |
        #      -------------------------------

        # GENERATE GAME
        host = User("player1", "player1", "player1@mail.com")
        visitor = User("player2", "player2", "player2@mail.com")
        players = {"host": host, "visitor": visitor}
        sub_list = [
            {
                "player": host,
                "chosen_id": 0,
                "health": 10,
                "x_coord": 0,
                "y_coord": 3,
                "direction": 2,
            },
            {
                "player": visitor,
                "chosen_id": 3,
                "health": 10,
                "x_coord": 1,
                "y_coord": 3,
                "direction": 0,
            },
        ]  # size = 4
        tor_list = []
        game = generate_game(6, 6, players, sub_list, tor_list)
        sub1 = game.submarines[0]
        sub2 = game.submarines[1]

        # ACTION TO TEST
        game.advance_object(sub2, 1)

        # ASSERT
        expected_board = [
            [None, None, sub1, sub1, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
        ]

        assert game.board.matrix == expected_board
        assert sub1.health == 0
        assert len(game.submarines) == 1
        assert game.is_finished()


def test_advance_submarine_crash_tail_of_submarine_and_live():
    with app.app_context():

        #         0    1    2    3    4    5
        #      -------------------------------
        #   0  |    |    |    | s0 | s1 |    |
        #   1  |    |    |    | s2 |    |    |
        #   2  |    |    |    | s0 |    |    |
        #   3  |    |    |    | s0 |    |    |
        #   4  |    |    |    | s0 |    |    |
        #   5  |    |    |    |    |    |    |
        #      -------------------------------

        # GENERATE GAME
        host = User("player1", "player1", "player1@mail.com")
        visitor = User("player2", "player2", "player2@mail.com")
        players = {"host": host, "visitor": visitor}
        sub_list = [
            {
                "player": host,
                "chosen_id": 0,
                "health": 10,
                "x_coord": 0,
                "y_coord": 4,
                "direction": 2,
            },
            {
                "player": visitor,
                "chosen_id": 3,
                "health": 50,
                "x_coord": 1,
                "y_coord": 3,
                "direction": 0,
            },
        ]  # size = 4
        tor_list = []
        game = generate_game(6, 6, players, sub_list, tor_list)
        sub1 = game.submarines[0]
        sub2 = game.submarines[1]

        # ACTION TO TEST
        game.advance_object(sub2, 1)

        # ASSERT
        expected_board = [
            [None, None, None, sub2, None, None],
            [None, None, None, sub2, None, None],
            [None, None, None, sub2, None, None],
            [None, None, None, sub2, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
        ]

        assert game.board.matrix == expected_board
        assert sub2.health == 40
        assert len(game.submarines) == 1
        assert game.is_finished()


def test_advance_submarine_crash_tail_of_submarine_and_die():
    with app.app_context():

        #         0    1    2    3    4    5
        #      -------------------------------
        #   0  |    |    |    | s0 | s1 |    |
        #   1  |    |    |    | s2 |    |    |
        #   2  |    |    |    | s0 |    |    |
        #   3  |    |    |    | s0 |    |    |
        #   4  |    |    |    | s0 |    |    |
        #   5  |    |    |    |    |    |    |
        #      -------------------------------

        # GENERATE GAME
        host = User("player1", "player1", "player1@mail.com")
        visitor = User("player2", "player2", "player2@mail.com")
        players = {"host": host, "visitor": visitor}
        sub_list = [
            {
                "player": host,
                "chosen_id": 0,
                "health": 10,
                "x_coord": 0,
                "y_coord": 4,
                "direction": 2,
            },
            {
                "player": visitor,
                "chosen_id": 3,
                "health": 10,
                "x_coord": 1,
                "y_coord": 3,
                "direction": 0,
            },
        ]  # size = 4
        tor_list = []
        game = generate_game(6, 6, players, sub_list, tor_list)
        sub1 = game.submarines[0]
        sub2 = game.submarines[1]

        # ACTION TO TEST
        game.advance_object(sub2, 1)

        # ASSERT
        expected_board = [
            [None, None, None, sub1, sub1, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
        ]

        assert game.board.matrix == expected_board
        assert sub1.health == 0
        assert len(game.submarines) == 1
        assert game.is_finished()


def test_advance_submarine_crash_wall():
    with app.app_context():

        #         0    1    2    3    4    5
        #      -------------------------------
        #   0  | s0 | s1 |    | s2 |    |    |
        #   1  |    |    |    | s0 |    |    |
        #   2  |    |    |    | s0 |    |    |
        #   3  |    |    |    | s0 |    |    |
        #   4  |    |    |    |    |    |    |
        #   5  |    |    |    |    |    |    |
        #      -------------------------------

        # GENERATE GAME
        host = User("player1", "player1", "player1@mail.com")
        visitor = User("player2", "player2", "player2@mail.com")
        players = {"host": host, "visitor": visitor}
        sub_list = [
            {
                "player": host,
                "chosen_id": 0,
                "health": 10,
                "x_coord": 0,
                "y_coord": 1,
                "direction": 2,
            },
            {
                "player": visitor,
                "chosen_id": 3,
                "health": 50,
                "x_coord": 0,
                "y_coord": 3,
                "direction": 0,
            },
        ]  # size = 4
        tor_list = []
        game = generate_game(6, 6, players, sub_list, tor_list)
        sub1 = game.submarines[0]
        sub2 = game.submarines[1]

        # ACTION TO TEST
        game.advance_object(sub2, 1)

        # ASSERT
        expected_board = [
            [sub1, sub1, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
        ]

        assert game.board.matrix == expected_board
        assert game.is_finished
        assert len(game.submarines) == 1


def test_advance_submarine_crash_torpedo_and_live():
    with app.app_context():

        #         0    1    2    3    4    5
        #      -------------------------------
        #   0  | s0 | s1 |    | *1 |    |    |
        #   1  |    |    |    | s2 |    |    |
        #   2  |    |    |    | s0 |    |    |
        #   3  |    |    |    | s0 |    |    |
        #   4  |    |    |    | s0 |    |    |
        #   5  |    |    |    |    |    |    |
        #      -------------------------------

        # GENERATE GAME
        host = User("player1", "player1", "player1@mail.com")
        visitor = User("player2", "player2", "player2@mail.com")
        players = {"host": host, "visitor": visitor}
        sub_list = [
            {
                "player": host,
                "chosen_id": 0,
                "health": 10,
                "x_coord": 0,
                "y_coord": 1,
                "direction": 2,
            },
            {
                "player": visitor,
                "chosen_id": 3,
                "health": 50,
                "x_coord": 1,
                "y_coord": 3,
                "direction": 0,
            },
        ]  # size = 4
        tor_list = [{"player": host, "x_coord": 0, "y_coord": 3, "direction": 2}]
        game = generate_game(6, 6, players, sub_list, tor_list)
        sub1 = game.submarines[0]
        sub2 = game.submarines[1]

        # ACTION TO TEST
        game.advance_object(sub2, 1)

        # ASSERT
        expected_board = [
            [sub1, sub1, None, sub2, None, None],
            [None, None, None, sub2, None, None],
            [None, None, None, sub2, None, None],
            [None, None, None, sub2, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
        ]

        assert game.board.matrix == expected_board
        assert game.is_ongoing()
        assert len(game.submarines) == 2
        assert sub2.health == 45


def test_advance_submarine_crash_torpedo_and_die():
    with app.app_context():

        #         0    1    2    3    4    5
        #      -------------------------------
        #   0  | s0 | s1 |    | *1 |    |    |
        #   1  |    |    |    | s2 |    |    |
        #   2  |    |    |    | s0 |    |    |
        #   3  |    |    |    | s0 |    |    |
        #   4  |    |    |    | s0 |    |    |
        #   5  |    |    |    |    |    |    |
        #      -------------------------------

        # GENERATE GAME
        host = User("player1", "player1", "player1@mail.com")
        visitor = User("player2", "player2", "player2@mail.com")
        players = {"host": host, "visitor": visitor}
        sub_list = [
            {
                "player": host,
                "chosen_id": 0,
                "health": 10,
                "x_coord": 0,
                "y_coord": 1,
                "direction": 2,
            },
            {
                "player": visitor,
                "chosen_id": 3,
                "health": 5,
                "x_coord": 1,
                "y_coord": 3,
                "direction": 0,
            },
        ]  # size = 4
        tor_list = [{"player": host, "x_coord": 0, "y_coord": 3, "direction": 2}]
        game = generate_game(6, 6, players, sub_list, tor_list)
        sub1 = game.submarines[0]
        sub2 = game.submarines[1]

        # ACTION TO TEST
        game.advance_object(sub2, 1)

        # ASSERT
        expected_board = [
            [sub1, sub1, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
        ]

        assert game.board.matrix == expected_board
        assert game.is_finished()
        assert len(game.submarines) == 1
        assert len(game.torpedos) == 0
