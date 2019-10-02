from opgo import agent
from opgo import goboard_slow as board
from opgo import gotypes
from opgo.utils import print_board, print_move, point_from_coords
from six.moves import input


def main():
    board_size = 9
    game = board.GameState.new_game(board_size)
    bot = agent.RandomBot()

    while not game.is_over():
        print(chr(27) + "[2J")
        print_board(game.board)

        if game.next_player == gotypes.Player.black:
            human_move = input('> ')  # Get move input from user.
            point = point_from_coords(human_move.strip())
            move = board.Move.play(point)
        else:
            move = bot.select_move(game)

        print_move(game.next_player, move)
        game = game.apply_move(move)


if __name__ == '__main__':
    main()
