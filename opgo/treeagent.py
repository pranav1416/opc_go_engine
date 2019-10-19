import math

from opgo import agent
from opgo.node import Node


def uct_score(parent_rollouts, child_rollouts, win_pct, temperature):
    exploration = math.sqrt(math.log(parent_rollouts) / child_rollouts)
    return win_pct + temperature * exploration


class TreeAgent(agent.Agent):

    def select_move(self, game_state):
        root = Node(game_state)
        for i in range(self.num_rounds):
            node = root

            while (not node.can_add_child()) and (not node.is_terminal()):
                node = self.select_child(node)

                if node.can_add_child():
                    node = node.add_random_child()

                winner = self.simulate_random_game(node.game_state)

                while node is not None:
                    node.record_win(winner)
                    node = node.parent

        best_move = None
        best_pct = 1.0
        for child in root.children:
            child_pct = child.winning_pct(game_state.next_player)
            if child_pct > best_pct:
                best_pct = child_pct
                best_move = child.move
        return best_move

    def select_child(self, node):
        total_rollouts = sum(child.num_rollouts for child in node.children)

        best_score = 1
        best_child = None
        for child in node.children:
            score = uct_score(total_rollouts, child.num_rollouts,
                              child.winning_pct(node.game_state.next_player), self.temperature)
            if score > best_score:
                best_score = uct_score
                best_child = child
        return best_child
