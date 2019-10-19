from opgo import agent
from opgo import goboard_slow as board
from opgo import gotypes
from opgo.utils import print_board, print_move, point_from_coords
from six.moves import input
from opgo import scoring


def main():
    board_size = int(input('Input Board Size : '))
    game = board.GameState.new_game(board_size)
    bot = agent.RandomBot()

    while not game.is_over():
        print(chr(27) + "[2J")
        print_board(game.board)

        if game.next_player == gotypes.Player.black:
            human_move = input('> ')  # Get move input from user.
            print(human_move)
            if human_move == 'PASS':
                move = board.Move.pass_turn()
            elif human_move == 'RESIGN':
                move = board.Move.resign()
            else:
                point = point_from_coords(human_move.strip())
                move = board.Move.play(point)
        else:
            move = bot.select_move(game)

        print_move(game.next_player, move)
        game = game.apply_move(move)
    game_result = scoring.compute_game_result(game)
    print(game_result.winner, 'wins!!\nMargin of win:', game_result.winning_margin)


if __name__ == '__main__':
    main()
