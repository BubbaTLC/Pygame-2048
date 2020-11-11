import pygame
import numpy as np
import sys
import math
import random

# * Global Variables * #
HEIGHT = 4
WIDTH = 4

CHOICE = [2,4]

def create_board():
    """
    This function creates a board matrix of 0's

    Example:
        board = create_board(4, 4)
    Returns:
        [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
    """
    return np.zeros(WIDTH*HEIGHT, dtype=int)

def initialize_game(board):
    """
    This function will randomly place the 2 tiles onto the board.
    """
    tile1 = random.choice(CHOICE)
    tile2 = random.choice(CHOICE)
    board[2] = tile1
    board[3] = tile2
    # np.random.shuffle(board)

def place_tile(board):
    """
    This function will randomly place a tile on an open space.
    """
    tile = random.choice(CHOICE)

    possiblePos = np.where(board == 0)
    if len(possiblePos[0]) == 0:
        return
    
    pos = np.random.choice(possiblePos[0])
    board[pos] = tile

def can_move(board):
    # if there are empty tiles we can move.
    if len(np.where(board == 0)[0]) > 0:
        return True

    # Check if the tile bellow is the same
    for r in range(len(board) - WIDTH):
        if board[r] == board[r+WIDTH]:
            return True
    
    # Check if the tile to the side is the same
    for r in range(len(board)-1):
        if r+1 % 4 == 0: # don't compare the right edge with next col
            continue
        if board[r] == board[r+1]:
            return True
    
    return False

def move_left(board):
    """
    This function will shift the tiles to the left.
    """
    for r in range(len(board)-1):
        if r+1 % WIDTH == 0:
            continue
        if board[r] == board[r+1]:
            board[r] = board[r] + board[r+1]
            board[r+1] = 0

    for r in range(0, len(board)-1, 4):
        for c in range(WIDTH-1, 0, -1):
            if board[r+(c-1)] == 0:
                board[r+(c-1)] = board[r+(c)]
                board[r+(c)] = 0
    
    

    
    
    
def move_right():
    pass

def move_up():
    pass

def move_down():
    pass


def is_game_over(board):
    if len(np.where(board == 0)[0]) == 0:
        return True
    
    return False

def print_board(board):
    print(board.copy().reshape(WIDTH,HEIGHT))
            

if __name__ == "__main__":
    board = create_board()
    initialize_game(board)
    print_board(board)
    move_left(board)
    print_board(board)

