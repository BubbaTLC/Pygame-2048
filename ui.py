import pygame
from pygame.locals import *
from main import Board
# pylint: disable=no-member

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
    def __init__(self, text="Button", pos=(0,0)):
        self.text = text
        self.x = pos[0]
        self.y = pos[1]

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
    def __init__(self):
        self.next = self
        self.TILE_SIZE = 100
        self.WIDTH = ((self.TILE_SIZE+20) * (4))-10
        self.HEIGHT = ((self.TILE_SIZE+20) * (5))-10
        self.SCREEN_SIZE = (self.WIDTH, self.HEIGHT)

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        pass

    def Render(self, screen):
        pass

    def SwitchToScene(self, next_scene):
        self.next = next_scene
    
    def Terminate(self):
        self.SwitchToScene(None)

class MenuScene(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.btnNewGame = Button(text="New Game")

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button ==1 ):
                if self.btnNewGame.button_clicked(event):
                    self.SwitchToScene(GameScene(Board()))
    
    def Render(self, screen):
        # Show title
        screen.fill(COLORS['BLACK'])
        title = Text('2048 in Python!', fontcolor=COLORS['LIGHT_GRAY'])
        title.center(self.WIDTH//2, self.HEIGHT//3)
        title.draw(screen)

        # Show New game Button
        self.btnNewGame.draw(screen, (self.WIDTH//2, self.HEIGHT//2), width=self.TILE_SIZE*2.5, height=75)

        

class GameScene(Scene):
    def __init__(self, board):
        Scene.__init__(self)
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
    
    def Render(self, screen):
        screen.fill(COLORS['BLACK'])

class EndScene(Scene):
    def __init__(self, board):
        Scene.__init__(self)
        self.board = board

    def ProcessInput(self, events, pressed_keys):
        pass
    
    def Render(self, screen):
        # For the sake of brevity, the title scene is a blank red screen
        screen.fill((0, 0, 255))