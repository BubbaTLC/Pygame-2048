import pygame
from pygame.locals import *
import numpy as np
import sys
import math
import random
from ui import *
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
    "DARK_GRAY": (64,64,64),
    "LIGHT_GRAY": (176,176,176),
    "0": (88,88,88),
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
    tile1 = random.choice(CHOICE)
    tile2 = random.choice(CHOICE)
    board[2] = tile1
    board[3] = tile2
    np.random.shuffle(board)

    # board[0] = 2
    # board[4] = 2
    # board[8] = 2
    # board[12] = 2

    # tiles = [ 2, 4, 8, 4, 4, 8, 4,  2, 64,  32,  16,   4, 16,  64, 256, 512]
    # for i in range(16):
    #     board[i] = tiles[i]

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
    for r in range(0, len(board)-1, 4):
        for c in range(0, WIDTH-1, 1):
            if board[r+(c)] == board[r+(c+1)]:
                return True
    
    return False

def move_left(board, score):
    """
    This function will shift the tiles to the left.
    """
    tempB = board.copy()

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

    for i in range(WIDTH-1):
        for r in range(0, len(board)-1, 4):
            for c in range(0, WIDTH-1, 1):
                if board[r+(c)] == 0:
                    board[r+(c)] = board[r+(c+1)]
                    board[r+(c+1)] = 0

    compare = tempB == board

    if not is_game_over(board) and not compare.all():
        place_tile(board)

    return score
    
def move_right(board, score):
    """
    This function will shifts the tiles to the right.
    """

    tempB = board.copy()

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

    for i in range(WIDTH-1):
        for r in range(len(board)-1, 0, -4):
            for c in range(0, WIDTH-1, 1):
                if board[r-(c)] == 0:
                    board[r-(c)] = board[r-(c+1)]
                    board[r-(c+1)] = 0

    compare = tempB == board

    if not is_game_over(board) and not compare.all():
        place_tile(board)


    return score

def move_up(board, score):
    """
    This function will shifts the tiles up.
    """

    tempB = board.copy()

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

    for i in range(WIDTH-1):
        for c in range(len(board)-HEIGHT):
            if board[c] == 0:
                board[c] = board[c+HEIGHT]
                board[c+HEIGHT] = 0

    compare = tempB == board

    if not is_game_over(board) and not compare.all():
        place_tile(board)


    return score

def move_down(board, score):
    """
    This function will shifts the tiles down.
    """
    tempB = board.copy()
    for i in range(HEIGHT-1):
        for c in range(len(board)-1, HEIGHT-1, -1): # Move tiles
            if board[c] == 0:
                board[c] = board[c-HEIGHT]
                board[c-HEIGHT] = 0

    for c in range(len(board)-1, HEIGHT-1, -1): # Combine tiles
        if board[c] == board[c-HEIGHT]:
            board[c] = board[c] + board[c-HEIGHT]
            board[c-HEIGHT] = 0
            score += board[c]

    for i in range(HEIGHT-1):
        for c in range(len(board)-1, HEIGHT-1, -1): # Move tiles
            if board[c] == 0:
                board[c] = board[c-HEIGHT]
                board[c-HEIGHT] = 0

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

    if can_move(board):
        return False
    
    return True

def print_board(board, score):
    """
    This functions prints the board and the score to the console.
    """
    print(f"Score: {score}")
    print(board.copy().reshape(WIDTH,HEIGHT))

def draw_board(board, score, highScr):
    """
    This function draws the board to the screen
    """
    pygame.draw.rect(screen, GAME_COLORS['BLACK'], (0,0,SCREEN_WIDTH, SCREEN_HEIGHT)) # Background
    pygame.draw.rect(screen, GAME_COLORS['DARK_GRAY'], (10,30+TILE_SIZE, SCREEN_WIDTH-20, SCREEN_HEIGHT-40-TILE_SIZE)) # Tile background
    tempBoard = board.copy().reshape(WIDTH,HEIGHT) 

    # Display the tiles
    for c in range(WIDTH):
        for r in range(HEIGHT):
            pygame.draw.rect(screen, GAME_COLORS[f'{tempBoard[r][c]}'], ((20)+(c*TILE_SIZE)+(c*10),(40+TILE_SIZE)+(r*TILE_SIZE)+(r*10), TILE_SIZE, TILE_SIZE))
            if tempBoard[r][c] > 0:
                label = ariel_55.render(f'{tempBoard[r][c]}', 1, GAME_COLORS['BLACK'])
                lblRect = label.get_rect(center=(((20)+(c*TILE_SIZE)+(c*10))+(TILE_SIZE//2), ((40+TILE_SIZE)+(r*TILE_SIZE)+(r*10))+(TILE_SIZE//2)))
                screen.blit(label, lblRect)

    # Display the score
    if score > highScr:
        highScr = score

    lblScore = ariel_25.render(f'Score: {score}', 1, GAME_COLORS['LIGHT_GRAY'])
    lblHighscore = ariel_25.render(f'Highscore: {highScr}', 1, GAME_COLORS['LIGHT_GRAY'])
    screen.blit(lblScore, (20,TILE_SIZE))
    screen.blit(lblHighscore, (20,TILE_SIZE-25))

    # Display Controls
    undo = ariel_25.render(f'Undo: CTRL + Z', 1, GAME_COLORS['LIGHT_GRAY'])
    screen.blit(undo, ((SCREEN_WIDTH//2)+35,TILE_SIZE))
    undo = ariel_25.render(f'New Game: CTRL + R', 1, GAME_COLORS['LIGHT_GRAY'])
    screen.blit(undo, ((SCREEN_WIDTH//2)+35,TILE_SIZE-25))

    # Display the Game title
    title = ariel_55.render("2048 In Python!", 1, GAME_COLORS['LIGHT_GRAY'])
    screen.blit(title, (20,20))



def write_line(file, line):
    f = open(file, "wt")
    f.writelines(f"{line}")
    f.close()

def read_line(file):
    f = open(file, "rt")
    line = f.readline()
    f.close()
    return line

def read_highscore(file='highscore.txt'):
    highScore = 0
    try:
        highScore = int(read_line(file))
    except ValueError:
        highScore = 0
    return highScore

def write_highscore(highScore, score, file='highscore.txt'):
    if highScore <= score:
        write_line(file,score)

def draw_button(screen, centerX, centerY, width=50, height=25, text="button", primaryColor=(64,64,64), secondaryColor=(176,176,176)):
    # Display button
    rect1 = Rect(0,0,0,0)
    rect1.size=(width, height)
    rect1.centerx = (centerX)
    rect1.centery = (centerY)
    pygame.draw.rect(screen, secondaryColor, rect1)
    
    rect2 = Rect(0,0,0,0)
    rect2.size=(width-10, height-10)
    rect2.centerx = (centerX)
    rect2.centery = (centerY)
    pygame.draw.rect(screen, primaryColor, rect2)

    label = ariel_55.render(text,1, secondaryColor)
    lblRect = label.get_rect(center=(centerX, centerY))
    screen.blit(label, lblRect)

    return rect1
                      
if __name__ == "__main__":
    # * Initialize Game * #
    gameOver = False
    running = True
    highScore = 0
    score = 0
    oldScore = score
    board = create_board()
    initialize_game(board)
    oldBoard = board.copy()

    highScore = read_highscore()

    # * Initialize Graphics * #
    pygame.init()
    pygame.display.init()
    pygame.font.init()
    pygame.display.set_caption("2048 In Python!")
    icon = pygame.image.load('images\\2048_white.png')
    pygame.display.set_icon(icon)
    ariel_55 = pygame.font.SysFont("ariel", 55)
    ariel_25 = pygame.font.SysFont("ariel", 25)
    screen = pygame.display.set_mode(SCREEN_SIZE)
    draw_board(board, score, highScore)
    pygame.display.update()

    button = Rect(0,0,0,0)
    # * Game Loop * #
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                write_highscore(highScore, score)
                sys.exit()

            if event.type == pygame.KEYDOWN and not gameOver:
                if event.key == pygame.K_w or event.key == pygame.K_UP: # Up
                    oldBoard = board.copy()
                    oldScore = score
                    score = move_up(board, score)

                if event.key == pygame.K_s or event.key == pygame.K_DOWN: # Down
                    oldBoard = board.copy() 
                    oldScore = score
                    score = move_down(board, score)

                if event.key == pygame.K_a or event.key == pygame.K_LEFT: # Left
                    oldBoard = board.copy() 
                    oldScore = score
                    score = move_left(board, score)

                if event.key == pygame.K_d or event.key == pygame.K_RIGHT: # Right
                    oldBoard = board.copy() 
                    oldScore = score
                    score = move_right(board, score)

                if event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL: # Undo
                    board = oldBoard
                    score = oldScore

                if event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL: # New Game
                    write_highscore(highScore, score)
                    highScore = read_highscore()
                    gameOver = False
                    board = create_board()
                    score = 0
                    initialize_game(board)
                    oldBoard = board.copy()
                    oldScore = score
                    draw_board(board, score, highScore)
                    pygame.display.update()

                draw_board(board, score, highScore)
                pygame.display.update()

                if is_game_over(board):
                    gameOver = True
                
                if gameOver: # Endgame screen
                    # Tint the background
                    bg = pygame.Surface(SCREEN_SIZE)
                    bg.set_alpha(200)
                    pygame.draw.rect(bg, GAME_COLORS['BLACK'], (0,0,SCREEN_WIDTH,SCREEN_HEIGHT))
                    screen.blit(bg, (0, 0))

                    # Display game over text
                    labels = ["Game Over!", f"Your Score: {score}", f"Largest Tile: {board.max()}"]
                    for line in range(len(labels)):
                        label = ariel_55.render(labels[line],1, GAME_COLORS['LIGHT_GRAY'])
                        lblRect = label.get_rect(center=(SCREEN_WIDTH//2, (SCREEN_HEIGHT//3)+(line*45) ))
                        screen.blit(label, lblRect)

                    # Display play again button
                    button = draw_button(SCREEN_WIDTH//2, (SCREEN_HEIGHT//3)*2, TILE_SIZE*2.5, TILE_SIZE, "Play Again")

                    pygame.display.update()

                    write_highscore(highScore, score)

            # Click Play again
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button ==1) and gameOver:
                pos = pygame.mouse.get_pos()
                if button.collidepoint(pos):
                    write_highscore(highScore, score)
                    highScore = read_highscore()
                    gameOver = False
                    board = create_board()
                    score = 0
                    initialize_game(board)
                    oldBoard = board.copy()
                    oldScore = score
                    draw_board(board, score, highScore)
                    pygame.display.update()
                    
                    
    
