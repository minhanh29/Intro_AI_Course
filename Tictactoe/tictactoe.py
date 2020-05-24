"""
Tic Tac Toe Player
"""
from typing import Any

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    # count how many x
    x_cells = 0
    o_cells = 0
    for row in board:
        for cell in row:
            if cell == X:
                x_cells += 1

            if cell == O:
                o_cells += 1

    d = x_cells - o_cells
    if d == 0:
        return X
    else:
        return O


def actions(board):
    action_set = []

    for row in board:
        for cell in row:
            if cell is None:
                action_set.append((board.index(row), row.index(cell)))

    return action_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    output = copy.deepcopy(board)

    # check valid action
    if output[action[0]][action[1]] is not None:
        raise InvalidActionError
    else:
        output[action[0]][action[1]] = player(board)

    return output


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # set number of x, o in rows, columns, and diagonal
    x_set = []
    o_set = []

    # check rows
    for row in board:
        x_cell = 0
        o_cell = 0
        for cell in row:
            if cell == X:
                x_cell += 1
            elif cell == O:
                o_cell += 1

        x_set.append(x_cell)
        o_set.append(o_cell)

    # check columns
    range = [0, 1, 2]
    for col in range:
        x_cell = 0
        o_cell = 0
        for row in range:
            cell = board[row][col]
            if cell == X:
                x_cell += 1
            elif cell == O:
                o_cell += 1

        x_set.append(x_cell)
        o_set.append(o_cell)

    # check diagonal
    x_cell = 0
    o_cell = 0
    x_cell2 = 0
    o_cell2 = 0
    for i in range:
        if board[i][i] == X:
            x_cell += 1
        elif board[i][i] == O:
            o_cell += 1

        if board[i][2-i] == X:
            x_cell2 += 1
        elif board[i][2-i] == O:
            o_cell2 += 1

    x_set.append(x_cell)
    o_set.append(o_cell)
    x_set.append(x_cell2)
    o_set.append(o_cell2)

    if x_set.__contains__(3):
        return X
    elif o_set.__contains__(3):
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    # check tie
    if len(actions(board)) == 0:
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if player(board) == X:
        maxv = max_value(board)
        for action in actions(board):
            if min_value(result(board, action)) == maxv:
                return action

    if player(board) == O:
        minv = min_value(board)
        for action in actions(board):
            if max_value(result(board, action)) == minv:
                return action


def max_value(board):
    if terminal(board):
        return utility(board)

    v = -3

    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v


def min_value(board):
    if terminal(board):
        return utility(board)

    v = 3

    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v


class Error(Exception):
    pass


class InvalidActionError(Error):
    def __init__(self, message):
        self.message = message
