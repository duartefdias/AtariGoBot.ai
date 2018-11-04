# Copied from:
# https://github.com/aimacode/aima-python/blob/master/games.py

from collections import namedtuple
import random
import itertools
import copy
from tqdm import tqdm

infinity = float('inf')
GameState = namedtuple('GameState', 'to_move, utility, board, moves')
StochasticGameState = namedtuple('StochasticGameState', 'to_move, utility, board, moves, chance')

def alphabeta_cutoff_search(state, game, d=6, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    # The position of the game variable in the state
    game_pos_in_state = 2 + game.boardSize * game.boardSize

    player = game.to_move(state)

    # Functions used by alphabeta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for a in game.actions(state):

            ############# Debug #####################################
            # Print board
            # game.print_board(state, print_ids=True)
            # print(state)
            # if state == [5, 2, 4, 0, 7, 7, 0, 4, 4, 4, 4, 9, 4, 4, 3, 4, 0, 3, 3, 3, 0, 0, 0, 3, 0, 5, 0, state[game_pos_in_state]]:
            #     print("\nOh oh spaghettiohs\n")
            #########################################################

            v = max(v, min_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for a in game.actions(state):

            ############# Debug #####################################
            # Print board
            # game.print_board(state, print_ids=True)
            # print(state)
            # if state == [5, 2, 4, 0, 7, 7, 0, 4, 4, 4, 4, 9, 4, 4, 3, 4, 0, 3, 3, 3, 0, 0, 0, 3, 0, 5, 0, state[game_pos_in_state]]:
            #     print("\nOh oh spaghettiohs\n")
            #########################################################

            v = min(v, max_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state, depth: depth > d or
                    game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in tqdm(game.actions(state)):

        ############# Debug #####################################
        # Print board
        # game.print_board(state, print_ids=True)
        # print(state)
        # if state == [5, 2, 4, 0, 7, 7, 0, 4, 4, 4, 4, 9, 4, 4, 3, 4, 0, 3, 3, 3, 0, 0, 0, 3, 0, 5, 0, state[game_pos_in_state]]:
        #     print("\nOh oh spaghettiohs\n")
        #########################################################

        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action