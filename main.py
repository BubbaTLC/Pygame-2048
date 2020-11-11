import pygame
import numpy as np
import sys
import math
import random
# pylint: disable=no-member

# * Global Variables * #
HEIGHT = 4
WIDTH = 4

CHOICE = [2,4]

END_TILE = 2048

TILE_SIZE = 100
SCREEN_WIDTH = ((TILE_SIZE+20) * (WIDTH))-10
SCREEN_HEIGHT = ((TILE_SIZE+20) * (HEIGHT + 1))-10

SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

GAME_COLORS = {
    "BLACK" : (0,0,0),
    "WHITE" : (255,255,255),
    "BLACK_LIGHT": (64,64,64),
    "0": (204, 0, 0),
    "2": (204, 102, 0),
    "4": (204, 153, 0),
    "8": (204, 204, 0),
    "16": (102, 204, 0),
    "32": (0, 204, 0),
    "64": (0, 204, 102),
    "128": (0, 204, 204),
    "256": (0, 102, 204),
    "512": (0, 0, 204),
    "1024": (102, 0, 204),
    "2048": (204, 0, 204),
}


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
    # tile1 = random.choice(CHOICE)
    # tile2 = random.choice(CHOICE)
    # board[2] = tile1
    # board[3] = tile2
    # np.random.shuffle(board)
    board[3] = 8
    board[7] = 8
    board[11] = 8
    board[15] = 8

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
    for c in range(len(board)-HEIGHT):
        if board[c] == board[c+HEIGHT]:
            return True
    
    return False

def move_left(board, score):
    """
    This function will shift the tiles to the left.
    """
    tempB = board.copy()

    for r in range(0, len(board)-1, 4):
        for c in range(0, WIDTH-1, 1):
            if board[r+(c)] == board[r+(c+1)]:
                board[r+(c)] = board[r+(c)] + board[r+(c+1)]
                board[r+(c+1)] = 0
                score += board[r+(c)]

    for i in range(WIDTH-1):
        for r in range(0, len(board)-1, 4):
            for c in range(0, WIDTH-1, 1):
                if board[r+(c)] == 0:
                    board[r+(c)] = board[r+(c+1)]
                    board[r+(c+1)] = 0

    for r in range(0, len(board)-1, 4):
        for c in range(0, WIDTH-1, 1):
            if board[r+(c)] == board[r+(c+1)]:
                board[r+(c)] = board[r+(c)] + board[r+(c+1)]
                board[r+(c+1)] = 0
                score += board[r+(c)]

    compare = tempB == board

    if not is_game_over(board) and not compare.all():
        place_tile(board)


    return score
    
def move_right(board, score):
    """
    This function will shifts the tiles to the right.
    """

    tempB = board.copy()

    for r in range(len(board)-1, 0, -4):
        for c in range(0, WIDTH-1, 1):
            if board[r-(c)] == board[r-(c+1)]:
                board[r-(c)] = board[r-(c)] + board[r-(c+1)]
                board[r-(c+1)] = 0
                score += board[r-(c)]

    for i in range(WIDTH-1):
        for r in range(len(board)-1, 0, -4):
            for c in range(0, WIDTH-1, 1):
                if board[r-(c)] == 0:
                    board[r-(c)] = board[r-(c+1)]
                    board[r-(c+1)] = 0


    for r in range(len(board)-1, 0, -4):
        for c in range(0, WIDTH-1, 1):
            if board[r-(c)] == board[r-(c+1)]:
                board[r-(c)] = board[r-(c)] + board[r-(c+1)]
                board[r-(c+1)] = 0
                score += board[r-(c)]

    compare = tempB == board

    if not is_game_over(board) and not compare.all():
        place_tile(board)


    return score

def move_up(board, score):
    """
    This function will shifts the tiles up.
    """

    tempB = board.copy()

    for c in range(len(board)-HEIGHT):
        if board[c] == board[c+HEIGHT]:
            board[c] = board[c] + board[c+HEIGHT]
            board[c+HEIGHT] = 0
            score += board[c]

    for i in range(WIDTH-1):
        for c in range(len(board)-HEIGHT):
            if board[c] == 0:
                board[c] = board[c+HEIGHT]
                board[c+HEIGHT] = 0

    for c in range(len(board)-HEIGHT):
        if board[c] == board[c+HEIGHT]:
            board[c] = board[c] + board[c+HEIGHT]
            board[c+HEIGHT] = 0
            score += board[c]

    compare = tempB == board

    if not is_game_over(board) and not compare.all():
        place_tile(board)


    return score

def move_down(board, score):
    """
    This function will shifts the tiles down.
    """
    tempB = board.copy()

    for c in range(len(board)-1, HEIGHT-1, -1):
        if board[c] == board[c-HEIGHT]:
            board[c] = board[c] + board[c-HEIGHT]
            board[c-HEIGHT] = 0
            score += board[c]

    for i in range(HEIGHT-1):
        for c in range(len(board)-1, HEIGHT-1, -1):
            if board[c] == 0:
                board[c] = board[c-HEIGHT]
                board[c-HEIGHT] = 0

    for c in range(len(board)-1, HEIGHT-1, -1):
        if board[c] == board[c-HEIGHT]:
            board[c] = board[c] + board[c-HEIGHT]
            board[c-HEIGHT] = 0
            score += board[c]

    compare = tempB == board

    if not is_game_over(board) and not compare.all():
        place_tile(board)

    return score

def is_game_over(board):
    """
        This function returns if the game is over.
    """
    if len(np.where(board == END_TILE)[0]):
        return True
    return not can_move(board)

def print_board(board, score):
    """
    This functions prints the board and the score to the console.
    """
    print(f"Score: {score}")
    print(board.copy().reshape(WIDTH,HEIGHT))


def draw_board(board, score):
    pygame.draw.rect(screen, GAME_COLORS['BLACK'], (0,0,SCREEN_WIDTH, SCREEN_HEIGHT)) # Background
    # pygame.draw.rect(screen, GAME_COLORS['BLACK_LIGHT'], (10,30+TILE_SIZE, SCREEN_WIDTH-20, SCREEN_HEIGHT-40-TILE_SIZE))
    tempBoard = board.copy().reshape(WIDTH,HEIGHT)
    for c in range(WIDTH):
        for r in range(HEIGHT):
            pygame.draw.rect(screen, GAME_COLORS['BLACK_LIGHT'], ((15)+(c*TILE_SIZE)+(c*10),(35+TILE_SIZE)+(r*TILE_SIZE)+(r*10), TILE_SIZE+5, TILE_SIZE+5))
    for c in range(WIDTH):
        for r in range(HEIGHT):
            if tempBoard[r][c] != 0:
                label = myFont.render(f'{tempBoard[r][c]}', 1, GAME_COLORS['BLACK'])
                lblRect = label.get_rect(center=(((20)+(c*TILE_SIZE)+(c*10))+(TILE_SIZE//2), ((40+TILE_SIZE)+(r*TILE_SIZE)+(r*10))+(TILE_SIZE//2)))
                pygame.draw.rect(screen, GAME_COLORS[f'{tempBoard[r][c]}'], ((20)+(c*TILE_SIZE)+(c*10),(40+TILE_SIZE)+(r*TILE_SIZE)+(r*10), TILE_SIZE, TILE_SIZE))
                screen.blit(label, lblRect)

            
            
if __name__ == "__main__":
    # * Initialize Game * #
    gameOver = False
    score = 0
    board = create_board()
    initialize_game(board)
    print_board(board, score)

    # * Initialize Graphics * #
    pygame.init()
    pygame.display.init()
    pygame.font.init()
    myFont = pygame.font.SysFont("ariel", 75)
    screen = pygame.display.set_mode(SCREEN_SIZE)
    draw_board(board, score)
    pygame.display.update()

    # TODO: Fix bug where 4 in a row combine into one tile. Could be considered as a feature.
    
    # * Game Loop * #
    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP: 
                    score = move_up(board, score)

                if event.key == pygame.K_s or event.key == pygame.K_DOWN: 
                    score = move_down(board, score)

                if event.key == pygame.K_a or event.key == pygame.K_LEFT: 
                    score = move_left(board, score)

                if event.key == pygame.K_d or event.key == pygame.K_RIGHT: 
                    score = move_right(board, score)
                    
                print_board(board, score)
                draw_board(board, score)
                pygame.display.update()

                if not is_game_over(board):
                    gameOver = False
                else:
                    gameOver = True

                if gameOver:
                    print(f"Game Over\nYour Score Was: {score}\nHighest Tile Created: {board.max()}")
                    pygame.time.wait(3000)
    
