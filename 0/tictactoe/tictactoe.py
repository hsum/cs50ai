"""
Tic Tac Toe Player
"""

import math

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
    i, j = action
    new_board = board[:]
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
        ((1, 0), (1, 1), (1, 2)),
        ((2, 0), (2, 1), (2, 2)),

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



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
