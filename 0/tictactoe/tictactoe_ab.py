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
        raise TypeError(f'invalid action {action}')

    try:
        board[i][j]
        new_board = deepcopy(board)
        new_board[i][j] = player(board)
    except IndexError:
        raise IndexError(f'invalid action {action}')
    except TypeError:
        if board is None:
            raise TypeError('board is None')
        raise
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    win_condition_ = (
        # horizontal
        ((0, 0), (0, 1), (0, 2)),
        ((1, 0), (1, 1), (1, 2)),
        ((2, 0), (2, 1), (2, 2)),

        # diagonal
        ((0, 0), (1, 1), (2, 2)),
        ((2, 0), (1, 1), (0, 2)),

        # vertical
        ((0, 0), (1, 0), (2, 0)),
        ((0, 1), (1, 1), (2, 1)),
        ((0, 2), (1, 2), (2, 2)),

    )
    for wc in win_condition_:
        candidate = tuple(board[i][j] for i, j in wc if board[i][j] != EMPTY)
        if len(candidate) == 3 and len(set(candidate)) == 1:
            return O if player(board) == X else X
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # if there is a winner, return True
    if winner(board) in (X, O):
        return True

    # if no winner and the board has empty cells, return False
    for row in board:
        for column in row:
            if column == EMPTY:
                return False

    # full board with no winner, must be draw
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    return {
        X: 1,
        O: -1
    }.get(winner(board), 0)


def max_value(board, a=-100, b=100):
    if terminal(board):
        return utility(board), None
    v = -100
    optimal_action = None
    for n, action in enumerate(actions(board)):
        candidate_value, _ = min_value(result(board, action), a=a, b=b)
        if candidate_value > v:
            v = candidate_value
            optimal_action = action
            a = v
        if b <= a:
            break
    return v, optimal_action


def min_value(board, a=-100, b=100):
    if terminal(board):
        return utility(board), None
    v = 100
    optimal_action = None
    for n, action in enumerate(actions(board)):
        candidate_value, _ = max_value(result(board, action), a=a, b=b)
        if candidate_value < v:
            v = candidate_value
            optimal_action = action
            b = v
        if b <= a:
            break
    return v, optimal_action


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        v, action = max_value(board)
    else:
        v, action = min_value(board)
    return action


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
    _ = None
    board = [
        [X, O, _],
        [X, X, O],
        [O, _, X]
    ]
    print(result(board, None))
    #print(result(board, (0, 3)))
    board = [
        [X, O, O],
        [O, X, X],
        [X, X, O]
    ]
    #print_(board)
    #print(actions(board))
    # {(0, 2), (2, 0), (2, 1), (2, 2)}
    print(player(board))
    print(winner(board))
    print(terminal(board))
