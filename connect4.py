import numpy as np
import matplotlib.pyplot as plt

import collections
State = collections.namedtuple('State', ['board', 'player'])

def init_state(rows=6, columns=7, player=1):
    """
    Returns the initial state given the hyperparameters and the first player.
    """
    board = np.zeros((rows, columns), dtype=np.int8)
    return State(board, player)

def get_actions(state):
    """
    Returns possible actions from a state as an array.
    """
    return np.where((state.board==0).any(axis=0))[0]

def render(state, mode='img'):
    """
    Renders the state in either 'img' or 'txt' mode.
    """
    if mode=='img':
        plt.imshow(state.board*2./3., vmin=-1, vmax=1, cmap='seismic')
        plt.title(f'{state.player} to move')
        plt.colorbar()
        plt.ylim(-0.5, 5.5)
        plt.xticks(np.arange(7)+.5)
        plt.yticks(np.arange(6)+.5)
        plt.grid()
    else:
        print(f'{state.player} to move')
        for r in range(5, -1, -1):
            print('|',end='')
            for c in range(6):
                print('X|' if state.board[r, c]==1 else ('O|' if state.board[r,c]==-1 else ' |'), end='')
            print()


def take_action(state, action):
    """
    Takes the given action from the state and returns the new state.
    """
    row = np.where(state.board[:, action]==0)[0].min()
    ns = State(state.board.copy(), -state.player)
    ns.board[row, action] = state.player
    return ns

def calc_winner(state):
    """
    Calculate the winner of the game from the state.
    Will return either 1, -1, or 0 (draw).
    """
    win = state.board[:, :-3]+state.board[:, 1:-2]+state.board[:, 2:-1]+state.board[:, 3:]
    if (np.abs(win)==4).any():
        return np.sign(win[np.where(np.abs(win)==4)])[0]

    win = state.board[:-3, :]+state.board[1:-2, :]+state.board[2:-1, :]+state.board[3:, :]
    if (np.abs(win)==4).any():
        return np.sign(win[np.where(np.abs(win)==4)])[0]

    win = state.board[:-3, :-3]+state.board[1:-2, 1:-2]+state.board[2:-1, 2:-1]+state.board[3:, 3:]
    if (np.abs(win)==4).any():
        return np.sign(win[np.where(np.abs(win)==4)])[0]

    win = state.board[3:, :-3]+state.board[2:-1, 1:-2]+state.board[1:-2, 2:-1]+state.board[:-3, 3:]
    if (np.abs(win)==4).any():
        return np.sign(win[np.where(np.abs(win)==4)])[0]
    return 0

def is_draw(state):
    """
    Returns boolean if the game is a draw.
    """
    return (state.board!=0).all()

def is_done(state):
    """
    Returns a tuple (done, winner) for the state.
    `done` is true if the game is over.
    `winner` marks the winner by player 1, -1, or 0 (draw)
    """
    winner = calc_winner(state)
    return is_draw(state) or winner != 0, winner



