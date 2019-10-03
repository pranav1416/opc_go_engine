from opgo import agent
from opgo import goboard_slow
from opgo import gotypes
from opgo.utils import print_board, print_move 
from opgo import scoring
import time

def main(): 
    board_size = int(input('Input Board Size : '))
    game = goboard_slow.GameState.new_game(board_size) 
    bots = {gotypes.Player.black: agent.naivecfg.RandomBot(), gotypes.Player.white: agent.naivecfg.RandomBot(), }
    while not game.is_over():
        time.sleep(0.3)
        print(chr(27) + "[2J")
        print_board(game.board)
        bot_move = bots[game.next_player].select_move(game) 
        print_move(game.next_player, bot_move)
        game = game.apply_move(bot_move) 
    game_result = scoring.compute_game_result(game)
    print(game_result.winner,' wins!!\nMargin of win: ',game_result.winning_margin)
if __name__ == '__main__':
        main()