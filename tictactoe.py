"""
Tic Tac Toe Player
"""

import math

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
    """
    Returns player who has the next turn on a board.
    """
    cnt = 0

    # Count the number of moves by all players
    for i in board:
        for j in i:
            if j != EMPTY:
                cnt += 1

    # If the moves is even then it is X's Turn if it is Odd then it is O's Turn
    return "O" if ((cnt % 2) == 1) else "X"
    

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i, row in enumerate(board):
        for j, value in enumerate(row):

            # If there is a empty state then a move should be possible.
            if value == EMPTY:
                moves.add((i, j))

    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    new_board = [row[:] for row in board]
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    lines = board + list(zip(*board)) + [[board[i][i]
                                          for i in range(3)], [board[i][2-i] for i in range(3)]]

    for line in lines:
        if line[0] != EMPTY and all(x == line[0] for x in line):
            return line[0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or not any(EMPTY in row for row in board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    return {"X": 1, "O": -1}.get(winner(board), 0)


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # Find the Maximum Value for the Maxplayer to minimize the loss
    def maxval(state):
        if terminal(state):
            return utility(state), None
        
        val = -math.inf
        best_action = None

        for action in actions(state):
            new_val, _ = minval(result(state, action))
            if new_val > val:
                val = new_val
                best_action = action
        return val, best_action
    
    # Find the Minimum Value for the Max player to minimize the loss
    def minval(state):
        if terminal(state):
            return utility(state), None
        
        val = math.inf
        best_action = None

        for action in actions(state):
            new_val, _ = maxval(result(state, action))
            if new_val < val:
                val = new_val
                best_action = action
        return val, best_action
    
    # If the board is in terminal state then there should be no move to calculate.
    if terminal(board):
        return None

    _, action = maxval(board) if player(board) == "X" else minval(board)
    return action

