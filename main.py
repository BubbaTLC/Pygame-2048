import pygame
from pygame.locals import *
import numpy as np
# pylint: disable=no-member

class Board:
    """Board Object for storing the position of tiles."""
    def __init__(self, width=4, height=4, score=0, choice=[2,4], endTile=2048):
        self.tiles = np.zeros(width*height, dtype=int)
        for i in range(len(choice)-1):
            self.tiles[i] = choice[i]
        np.random.shuffle(self.tiles)

        self.width = width
        self.height = height
        self.choice = choice
        self.score = score
        self.highScore = self.read_highscore()
        self.endTile = endTile

    def place_tile(self):
        """
        This function will randomly place a tile on an open space.
        """
        tile = np.random.choice(self.choice)

        possiblePos = np.where(self.tiles == 0)
        if len(possiblePos[0]) == 0:
            return
        
        pos = np.random.choice(possiblePos[0])
        self.tiles[pos] = tile

    def can_move(self):
        """
        """
        # if there are empty tiles we can move.
        if len(np.where(self.tiles == 0)[0]) > 0:
            return True

        # Check if the tile bellow is the same
        for r in range(len(self.tiles) - self.width):
            if self.tiles[r] == self.tiles[r+self.width]:
                return True
        
        # Check if the tile to the side is the same
        for r in range(0, len(self.tiles)-1, self.width):
            for c in range(0, self.tiles-1, 1):
                if self.tiles[r+(c)] == self.tiles[r+(c+1)]:
                    return True
        
        return False

    def print_board(self):
        """
        This functions prints the self.tiles and the score to the console.
        """
        print(f"Score: {self.score}")
        print(self.tiles.copy().reshape(self.width,self.height))

    def is_game_over(self):
        """
            This function returns if the game is over.
        """
        if len(np.where(self.tiles == self.endTile)[0]):
            return True

        if self.can_move():
            return False
        
        return True

    def move_left(self):
        """
        This function will shift the tiles to the left.
        """
        tempB = self.tiles.copy()

        for i in range(self.width-1):
            for r in range(0, len(self.tiles)-1, 4):
                for c in range(0, self.width-1, 1):
                    if self.tiles[r+(c)] == 0:
                        self.tiles[r+(c)] = self.tiles[r+(c+1)]
                        self.tiles[r+(c+1)] = 0

        for r in range(0, len(self.tiles)-1, 4):
            for c in range(0, self.width-1, 1):
                if self.tiles[r+(c)] == self.tiles[r+(c+1)]:
                    self.tiles[r+(c)] = self.tiles[r+(c)] + self.tiles[r+(c+1)]
                    self.tiles[r+(c+1)] = 0
                    score += self.tiles[r+(c)]

        for i in range(self.width-1):
            for r in range(0, len(self.tiles)-1, 4):
                for c in range(0, self.width-1, 1):
                    if self.tiles[r+(c)] == 0:
                        self.tiles[r+(c)] = self.tiles[r+(c+1)]
                        self.tiles[r+(c+1)] = 0

        compare = tempB == self.tiles

        if not self.is_game_over() and not compare.all():
            self.place_tile()

        return score
    
    def move_right(self):
        """
        This function will shifts the tiles to the right.
        """

        tempB = self.tiles.copy()

        for i in range(self.width-1):
            for r in range(len(self.tiles)-1, 0, -4):
                for c in range(0, self.width-1, 1):
                    if self.tiles[r-(c)] == 0:
                        self.tiles[r-(c)] = self.tiles[r-(c+1)]
                        self.tiles[r-(c+1)] = 0

        for r in range(len(self.tiles)-1, 0, -4):
            for c in range(0, self.width-1, 1):
                if self.tiles[r-(c)] == self.tiles[r-(c+1)]:
                    self.tiles[r-(c)] = self.tiles[r-(c)] + self.tiles[r-(c+1)]
                    self.tiles[r-(c+1)] = 0
                    score += self.tiles[r-(c)]

        for i in range(self.width-1):
            for r in range(len(self.tiles)-1, 0, -4):
                for c in range(0, self.width-1, 1):
                    if self.tiles[r-(c)] == 0:
                        self.tiles[r-(c)] = self.tiles[r-(c+1)]
                        self.tiles[r-(c+1)] = 0

        compare = tempB == self.tiles

        if not self.is_game_over() and not compare.all():
            self.place_tile()


        return score

    def move_up(self):
        """
        This function will shifts the tiles up.
        """

        tempB = self.tiles.copy()

        for i in range(self.width-1):
            for c in range(len(self.tiles)-self.height):
                if self.tiles[c] == 0:
                    self.tiles[c] = self.tiles[c+self.height]
                    self.tiles[c+self.height] = 0

        for c in range(len(self.tiles)-self.height):
            if self.tiles[c] == self.tiles[c+self.height]:
                self.tiles[c] = self.tiles[c] + self.tiles[c+self.height]
                self.tiles[c+self.height] = 0
                score += self.tiles[c]

        for i in range(self.width-1):
            for c in range(len(self.tiles)-self.height):
                if self.tiles[c] == 0:
                    self.tiles[c] = self.tiles[c+self.height]
                    self.tiles[c+self.height] = 0

        compare = tempB == self.tiles

        if not self.is_game_over() and not compare.all():
            self.place_tile()

        return score

    def move_down(self):
        """
        This function will shifts the tiles down.
        """
        tempB = self.tiles.copy()
        for i in range(self.height-1):
            for c in range(len(self.tiles)-1, self.height-1, -1): # Move tiles
                if self.tiles[c] == 0:
                    self.tiles[c] = self.tiles[c-self.height]
                    self.tiles[c-self.height] = 0

        for c in range(len(self.tiles)-1, self.height-1, -1): # Combine tiles
            if self.tiles[c] == self.tiles[c-self.height]:
                self.tiles[c] = self.tiles[c] + self.tiles[c-self.height]
                self.tiles[c-self.height] = 0
                score += self.tiles[c]

        for i in range(self.height-1):
            for c in range(len(self.tiles)-1, self.height-1, -1): # Move tiles
                if self.tiles[c] == 0:
                    self.tiles[c] = self.tiles[c-self.height]
                    self.tiles[c-self.height] = 0

        compare = tempB == self.tiles

        if not self.is_game_over() and not compare.all():
            self.place_tile()

        return score

    def read_highscore(self, file='highscore.txt'):
        try:
            f = open(file, "rt")
            line = f.readline()
            f.close()
            self.highScore = int(line)
        except ValueError:
            self.highScore = 0

    def write_highscore(self, file='highscore.txt'):
        try:
            if self.highScore <= self.score:
                f = open(file, "wt")
                f.writelines(f"{self.score}")
                f.close()
        except:
            pass


class App:
    """Create a single-window app with multiple scenes."""

    def __init__(self):
        """Initialize pygame and the application."""
        pygame.init()
        # flags = pygame.NOFRAME
        self.TILE_SIZE = 100
        self.WIDTH = ((self.TILE_SIZE+20) * (4))-10
        self.HEIGHT = ((self.TILE_SIZE+20) * (5))-10
        self.SCREEN_SIZE = (self.WIDTH, self.HEIGHT)
        App.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        App.running = True

        self.shortcuts = {
            (pygame.K_z, pygame.KMOD_CTRL): 'print("ctl+X")',
            (pygame.K_r, pygame.KMOD_CTRL): 'print("alt+X")',
            (pygame.K_a, pygame.KMOD_CTRL + pygame.KMOD_SHIFT): 'print("ctrl+shift+A")',
        }

        self.colors = {
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
            "MAX" : (153, 0, 153)
        }

    def run(self):
        """Run the main event loop."""
        while App.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    App.running = False

                if event.type == pygame.KEYDOWN:
                    self.do_shortcut(event)
        pygame.quit()

    def do_shortcut(self, event):
        """Find the the key/mod combination in the dictionary and execute the cmd."""
        k = event.key
        m = event.mod
        if k in self.shortcuts and m == 0 :
            exec(self.shortcuts[k])
        elif (k, m) in self.shortcuts:
            exec(self.shortcuts[k, m])

    # def draw_board(self, board):
    #     """
    #     This function draws the board to the screen
    #     """
    #     pygame.draw.rect(screen, GAME_COLORS['BLACK'], (0,0,SCREEN_WIDTH, SCREEN_HEIGHT)) # Background
    #     pygame.draw.rect(screen, GAME_COLORS['DARK_GRAY'], (10,30+TILE_SIZE, SCREEN_WIDTH-20, SCREEN_HEIGHT-40-TILE_SIZE)) # Tile background
    #     tempBoard = board.copy().reshape(WIDTH,HEIGHT) 

    #     # Display the tiles
    #     for c in range(WIDTH):
    #         for r in range(HEIGHT):
    #             pygame.draw.rect(screen, GAME_COLORS[f'{tempBoard[r][c]}'], ((20)+(c*TILE_SIZE)+(c*10),(40+TILE_SIZE)+(r*TILE_SIZE)+(r*10), TILE_SIZE, TILE_SIZE))
    #             if tempBoard[r][c] > 0:
    #                 label = ariel_55.render(f'{tempBoard[r][c]}', 1, GAME_COLORS['BLACK'])
    #                 lblRect = label.get_rect(center=(((20)+(c*TILE_SIZE)+(c*10))+(TILE_SIZE//2), ((40+TILE_SIZE)+(r*TILE_SIZE)+(r*10))+(TILE_SIZE//2)))
    #                 screen.blit(label, lblRect)

    #     # Display the score
    #     if score > highScr:
    #         highScr = score

    #     lblScore = ariel_25.render(f'Score: {score}', 1, GAME_COLORS['LIGHT_GRAY'])
    #     lblHighscore = ariel_25.render(f'Highscore: {highScr}', 1, GAME_COLORS['LIGHT_GRAY'])
    #     screen.blit(lblScore, (20,TILE_SIZE))
    #     screen.blit(lblHighscore, (20,TILE_SIZE-25))

    #     # Display Controls
    #     undo = ariel_25.render(f'Undo: CTRL + Z', 1, GAME_COLORS['LIGHT_GRAY'])
    #     screen.blit(undo, ((SCREEN_WIDTH//2)+35,TILE_SIZE))
    #     undo = ariel_25.render(f'New Game: CTRL + R', 1, GAME_COLORS['LIGHT_GRAY'])
    #     screen.blit(undo, ((SCREEN_WIDTH//2)+35,TILE_SIZE-25))

    #     # Display the Game title
    #     title = ariel_55.render("2048 In Python!", 1, GAME_COLORS['LIGHT_GRAY'])
    #     screen.blit(title, (20,20))



if __name__ == '__main__':
    App().run()