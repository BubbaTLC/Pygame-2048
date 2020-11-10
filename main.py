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
    board[0] = tile1
    board[1] = tile2
    np.random.shuffle(board)

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
    
    for r in range(len(board)-1):
        if board[r] == board[r+1]:
            return True
    
    return False

            

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
    print(is_game_over(board))
    print(can_move(board))

