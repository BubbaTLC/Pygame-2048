import pygame
from pygame.locals import *
import numpy as np
from ui import *
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
        self.highScore = 0
        self.read_highscore()
        self.endTile = endTile
        self.lastScore = score
        self.lastTiles = self.tiles.copy()

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
            for c in range(0, self.width-1, 1):
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
        self.lastTiles = self.tiles.copy()
        self.lastScore = self.score

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
                    self.score += self.tiles[r+(c)]

        for i in range(self.width-1):
            for r in range(0, len(self.tiles)-1, 4):
                for c in range(0, self.width-1, 1):
                    if self.tiles[r+(c)] == 0:
                        self.tiles[r+(c)] = self.tiles[r+(c+1)]
                        self.tiles[r+(c+1)] = 0

        compare = self.lastTiles == self.tiles

        if not self.is_game_over() and not compare.all():
            self.place_tile()      
    
    def move_right(self):
        """
        This function will shifts the tiles to the right.
        """

        self.lastTiles = self.tiles.copy()
        self.lastScore = self.score

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
                    self.score += self.tiles[r-(c)]

        for i in range(self.width-1):
            for r in range(len(self.tiles)-1, 0, -4):
                for c in range(0, self.width-1, 1):
                    if self.tiles[r-(c)] == 0:
                        self.tiles[r-(c)] = self.tiles[r-(c+1)]
                        self.tiles[r-(c+1)] = 0

        compare = self.lastTiles == self.tiles

        if not self.is_game_over() and not compare.all():
            self.place_tile()

    def move_up(self):
        """
        This function will shifts the tiles up.
        """

        self.lastTiles = self.tiles.copy()
        self.lastScore = self.score

        for i in range(self.width-1):
            for c in range(len(self.tiles)-self.height):
                if self.tiles[c] == 0:
                    self.tiles[c] = self.tiles[c+self.height]
                    self.tiles[c+self.height] = 0

        for c in range(len(self.tiles)-self.height):
            if self.tiles[c] == self.tiles[c+self.height]:
                self.tiles[c] = self.tiles[c] + self.tiles[c+self.height]
                self.tiles[c+self.height] = 0
                self.score += self.tiles[c]

        for i in range(self.width-1):
            for c in range(len(self.tiles)-self.height):
                if self.tiles[c] == 0:
                    self.tiles[c] = self.tiles[c+self.height]
                    self.tiles[c+self.height] = 0

        compare = self.lastTiles == self.tiles

        if not self.is_game_over() and not compare.all():
            self.place_tile()

    def move_down(self):
        """
        This function will shifts the tiles down.
        """
        self.lastTiles = self.tiles.copy()
        self.lastScore = self.score

        for i in range(self.height-1):
            for c in range(len(self.tiles)-1, self.height-1, -1): # Move tiles
                if self.tiles[c] == 0:
                    self.tiles[c] = self.tiles[c-self.height]
                    self.tiles[c-self.height] = 0

        for c in range(len(self.tiles)-1, self.height-1, -1): # Combine tiles
            if self.tiles[c] == self.tiles[c-self.height]:
                self.tiles[c] = self.tiles[c] + self.tiles[c-self.height]
                self.tiles[c-self.height] = 0
                self.score += self.tiles[c]

        for i in range(self.height-1):
            for c in range(len(self.tiles)-1, self.height-1, -1): # Move tiles
                if self.tiles[c] == 0:
                    self.tiles[c] = self.tiles[c-self.height]
                    self.tiles[c-self.height] = 0

        compare = self.lastTiles == self.tiles

        if not self.is_game_over() and not compare.all():
            self.place_tile()

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
        self.TILE_SIZE = 100
        self.WIDTH = ((self.TILE_SIZE+20) * (4))-10
        self.HEIGHT = ((self.TILE_SIZE+20) * (5))-10
        self.SCREEN_SIZE = (self.WIDTH, self.HEIGHT)
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        self.running = True
        self.board = Board()

    def run(self):
        """Run the main event loop."""
        mainMenu = MenuScene()
        gameScene = GameScene(self.board)
        endScene = EndScene(self.board)
        activeScene = mainMenu

        while activeScene != None:
            pressedKeys = pygame.key.get_pressed()
            
            # Event filtering
            filteredEvents = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_COMMA: # Switch Scene
                        activeScene = mainMenu

                    if event.key == pygame.K_PERIOD: # Switch Scene
                        activeScene = gameScene

                    if event.key == pygame.K_SLASH: # Switch Scene
                        activeScene = endScene

                if not self.running:
                    activeScene.Terminate()
                else:
                    filteredEvents.append(event)
            
            activeScene.ProcessInput(filteredEvents, pressedKeys)
            activeScene.Render(self.screen)
            activeScene = activeScene.next
            pygame.display.flip()

        pygame.quit()



if __name__ == '__main__':
    App().run()