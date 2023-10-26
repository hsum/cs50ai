"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def print_(board):
    print('\n'.join(
        ' | '.join(f'{i=} {j=} {column}' for j, column in enumerate(row))
        for i, row in enumerate(board)
    ))


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = sum(1 for row in board for column in row if column != EMPTY)
    return (X, O)[count % 2]


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return set((i, j) for i, row in enumerate(board) for j, column in enumerate(row) if column == EMPTY)


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    try:
        i, j = action
    except TypeError:
        if board is None:
            print('board is None!')
        raise

    new_board = deepcopy(board)
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if terminal(board):
        return O if player(board) == X else X
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    win_condition_ = (
        ((0, 0), (0, 1), (0, 2)),
        ((1, 0), (1, 1), (1, 2)),
        ((2, 0), (2, 1), (2, 2)),

        ((0, 0), (1, 1), (2, 2)),
        ((2, 0), (1, 1), (0, 2)),

        ((0, 0), (1, 0), (2, 0)),
        ((0, 1), (1, 1), (2, 1)),
        ((0, 2), (1, 2), (2, 2)),

    )
    for wc in win_condition_:
        candidate = tuple(board[i][j] for i, j in wc if board[i][j] != EMPTY)
        if len(candidate) == 3 and len(set(candidate)) == 1:
            return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    return {
        X: 1,
        O: -1
    }.get(winner(board), 0)



'''
def max_value(board):
    if terminal(board):
        return utility(board), None
    v, optimal_action = -100, None
    for action in actions(board):
        candidate_value, _ = min_value(result(board, action))
        if candidate_value > v:
            v = candidate_value
            optimal_action = action
    return v, optimal_action


def min_value(board):
    if terminal(board):
        return utility(board), None
    v, optimal_action = 100, None
    print(f'{v=}')
    for action in actions(board):
        candidate_value, _ = max_value(result(board, action))
        print(f'{candidate_value=}')
        if candidate_value < v:
            v = candidate_value
            optimal_action = action
            print(f'{optimal_action=} {candidate_value=} {v=}')
    return v, optimal_action
'''


def max_value(board):
    if terminal(board):
        return utility(board), None
    v, optimal_action = -100, None
    for action in actions(board):
        candidate_value, _ = min_value(result(board, action))
        if candidate_value > v:
            v = candidate_value
            optimal_action = action
    return v, optimal_action


def min_value(board):
    if terminal(board):
        return utility(board), None
    v, optimal_action = 100, None
    print(f'{v=}')
    for action in actions(board):
        candidate_value, candidate_action = max_value(result(board, action))
        print(f'{candidate_value=} {action=}')
        if candidate_value < v:
            v = candidate_value
            optimal_action = action
            print(f'{optimal_action=} {candidate_value=} {v=}')
    return v, optimal_action

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    '''
    mm = {
        X: max_value,
        O: min_value,
    }[player(board)]

    action, _ = mm(board)
    return action
    '''
    if player(board) == X:
        v, action = max_value(board)
    else:
        v, action = min_value(board)
        print(f'min player decision: {v=} {action=}')
    return action
    '''
    mm, limit_ = {
        X: (max, -100),
        O: (min, 100),
    }[player(board)]
    inverse_mm = min if mm == max else max

    v = limit_
    optimal_action = None

    for action in actions(board):
        v = mm(v, inverse_mm(utility(result(board, action))))
        optimal_action = action
    print(mm(
        (limit_, inverse_mm(utility(result(board, action)) for action in actions(board)))
    ))
    value, optimal_action = inverse_mm((utility(result(board, action)), action) for action in actions(board))[0]

    for action in actions(board):
        print(mm, action, utility(result(board, action)))
    return optimal_action
    '''
if __name__ == '__main__':
    board = [
        [X, O, None],
        [X, X, O],
        [None, None, None]
    ]
    board = [
        [None, None, None],
        [None, X, None],
        [None, None, None]
    ]
    #print(actions(board))
    # {(0, 2), (2, 0), (2, 1), (2, 2)}
    print(terminal(board))
