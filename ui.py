# pylint: disable=no-member
import pygame
from pygame.locals import Color, Rect
import numpy as np


COLORS = {
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
        self.highscore = 0
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
            self.highscore = int(line)
        except ValueError:
            self.highscore = 0

    def write_highscore(self, file='highscore.txt'):
        try:
            if self.highscore <= self.score:
                f = open(file, "wt")
                f.writelines(f"{self.score}")
                f.close()
        except:
            pass

class Text:
    """Create a text object."""

    def __init__(self, text, pos=(0,0), fontcolor=Color('black'), fontsize=72, fontname='ariel'):
        self.text = text
        self.pos = pos
        self.fontname = fontname
        self.fontsize = fontsize
        self.fontcolor = fontcolor
        self.set_font()
        self.render()

    def set_font(self):
        """Set the Font object from name and size."""
        self.font = pygame.font.SysFont(self.fontname, self.fontsize)

    def render(self):
        """Render the text into an image."""
        self.img = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos

    def draw(self, screen):
        """Draw the text image to the screen."""
        screen.blit(self.img, self.rect)

    def center(self,x,y):
        self.rect = self.img.get_rect(center=(x,y))

class Button():
    def __init__(self, text="Button"):
        self.text = text

    def draw(self, screen, pos, width=50, height=25, fontSize=55, primaryColor=COLORS['DARK_GRAY'], secondaryColor=COLORS['LIGHT_GRAY']):
        # Display button
        centerX = pos[0]
        centerY = pos[1]

        rect1 = Rect(0,0,0,0)
        rect1.size=(width, height)
        rect1.centerx = centerX
        rect1.centery = centerY
        pygame.draw.rect(screen, secondaryColor, rect1)

        self.rect2 = Rect(0,0,0,0)
        self.rect2.size=(width-10, height-10)
        self.rect2.centerx = (centerX)
        self.rect2.centery = (centerY)
        pygame.draw.rect(screen, primaryColor, self.rect2)

        label = Text(self.text, fontsize=fontSize)
        label.set_font()
        label.center(centerX, centerY)
        label.draw(screen)

    def button_clicked(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect2.collidepoint(x, y):
                    return True

        return False

class Scene:
    def __init__(self, screen):
        self.next = self
        self.TILE_SIZE = 100
        self.WIDTH = ((self.TILE_SIZE+20) * (4))-10
        self.HEIGHT = ((self.TILE_SIZE+20) * (5))-10
        self.SCREEN_SIZE = (self.WIDTH, self.HEIGHT)
        self.screen = screen

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        pass

    def Render(self):
        pass

    def SwitchToScene(self, next_scene):
        self.next = next_scene
    
    def Terminate(self):
        self.SwitchToScene(None)

class MenuScene(Scene):
    def __init__(self, screen):
        Scene.__init__(self, screen)
        self.btnNewGame = Button(text="New Game")

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button ==1 ):
                if self.btnNewGame.button_clicked(event):
                    self.SwitchToScene(GameScene(Board(), self.screen))
                    
    
    def Render(self):
        # Show title
        self.screen.fill(COLORS['BLACK'])
        title = Text('2048 in Python!', fontcolor=COLORS['LIGHT_GRAY'])
        title.center(self.WIDTH//2, self.HEIGHT//3)
        title.draw(self.screen)

        # Show New game Button
        self.btnNewGame.draw(self.screen, (self.WIDTH//2, self.HEIGHT//2), width=self.TILE_SIZE*2.5, height=75)
   
class GameScene(Scene):
    def __init__(self, board, screen):
        Scene.__init__(self, screen)
        self.board = board
        self.shortcuts = {
            (pygame.K_w):       'self.board.move_up()',
            (pygame.K_s):       'self.board.move_down()',
            (pygame.K_a):       'self.board.move_left()',
            (pygame.K_d):       'self.board.move_right()',
            (pygame.K_UP):      'self.board.move_up()',
            (pygame.K_DOWN):    'self.board.move_down()',
            (pygame.K_LEFT):    'self.board.move_left()',
            (pygame.K_RIGHT):   'self.board.move_right()',
            (pygame.K_z, 4160): 'self.board.tiles = self.board.lastTiles.copy()\nself.board.score = self.board.lastScore',
            (pygame.K_r, 4160): 'self.board = Board()',
            (pygame.K_a, 4161): 'print("ctrl+shift+a")',
        }

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.do_shortcut(event)
                self.board.print_board()

            if self.board.is_game_over():
                    gameOver = True

            gameOver = True
                
            if gameOver: # Endgame screen
                self.SwitchToScene(EndScene(self.board, self.screen))
                    

    def do_shortcut(self, event):
        """Find the the key/mod combination in the dictionary and execute the cmd."""
        k = event.key
        m = event.mod
        if (k, m) in self.shortcuts:
            exec(self.shortcuts[(k , m)])
        elif (k) in self.shortcuts:
            exec(self.shortcuts[k])
    
    def Update(self):
        pass
    
    def Render(self):
        self.draw_board()

    def draw_board(self):
        """
        This function draws the board to the screen
        """
        pygame.draw.rect(self.screen, COLORS['BLACK'], (0,0, self.WIDTH, self.HEIGHT)) # Background
        pygame.draw.rect(self.screen, COLORS['DARK_GRAY'], (10,30+self.TILE_SIZE, self.WIDTH-20, self.HEIGHT-40-self.TILE_SIZE)) # Tile background
        tempBoard = self.board.tiles.copy().reshape(self.board.width,self.board.height) 

        # Display the tiles
        for c in range(self.board.width):
            for r in range(self.board.height):
                pygame.draw.rect(self.screen, COLORS[f'{tempBoard[r][c]}'], ((20)+(c*self.TILE_SIZE)+(c*10),(40+self.TILE_SIZE)+(r*self.TILE_SIZE)+(r*10), self.TILE_SIZE, self.TILE_SIZE))
                if tempBoard[r][c] > 0:
                    label = Text(f'{tempBoard[r][c]}', fontcolor=COLORS['BLACK'], fontsize=55)
                    label.center(((20)+(c*self.TILE_SIZE)+(c*10))+(self.TILE_SIZE//2), ((40+self.TILE_SIZE)+(r*self.TILE_SIZE)+(r*10))+(self.TILE_SIZE//2))
                    label.draw(self.screen)

        # Display the score
        if self.board.score > self.board.highscore:
            self.board.highscore = self.board.score

        lblScore = Text(f'Score: {self.board.score}',pos=(20, self.TILE_SIZE), fontcolor=COLORS['LIGHT_GRAY'], fontsize=25)
        lblScore.draw(self.screen)
        lblHighscore = Text(f'Highscore: {self.board.highscore}',pos=(20, self.TILE_SIZE-25), fontcolor=COLORS['LIGHT_GRAY'], fontsize=25)
        lblHighscore.draw(self.screen)

        # Display Controls
        undo = Text(f'Undo: CTRL + Z',pos=((self.WIDTH//2)+35,self.TILE_SIZE), fontcolor=COLORS['LIGHT_GRAY'], fontsize=25)
        undo.draw(self.screen)
        restart = Text(f'New Game: CTRL + R',pos=((self.WIDTH//2)+35,self.TILE_SIZE-25), fontcolor=COLORS['LIGHT_GRAY'], fontsize=25)
        restart.draw(self.screen)

        # Display the Game title
        title = Text(f'2048 in Python!',pos=(20,20), fontcolor=COLORS['LIGHT_GRAY'], fontsize=25)
        title.draw(self.screen)

class EndScene(Scene):
    def __init__(self, board, screen):
        Scene.__init__(self, screen)
        self.board = board
        self.btnPlayAgain = Button(text="Play Again")

    def ProcessInput(self, events, pressed_keys):
        pass
    
    def Render(self):
        # Tint the background
        bg = pygame.Surface(self.SCREEN_SIZE)
        bg.set_alpha(1)
        pygame.draw.rect(bg, COLORS['BLACK'], (0,0,self.WIDTH,self.HEIGHT))
        self.screen.blit(bg, (0, 0))

        # Display game over text
        labels = ["Game Over!", f"Your Score: {self.board.score}", f"Highscore: {self.board.highscore}"]
        for line in range(len(labels)):
            label = Text(labels[line], fontcolor=COLORS['LIGHT_GRAY'])
            label.center(self.WIDTH//2, (self.HEIGHT//3)+(line*50))
            label.draw(self.screen)

        # Display play again button
        self.btnPlayAgain.draw(self.screen, (self.WIDTH//2, self.HEIGHT//2+50*3), width=self.TILE_SIZE*2.5, height=75)