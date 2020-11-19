import pygame
from ui import * # pylint: disable=unused-wildcard-import
# pylint: disable=no-member
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
        activeScene = MenuScene(self.screen, self.board)
        clock = pygame.time.Clock()

        while activeScene != None:
            pressedKeys = pygame.key.get_pressed()
            
            # Event filtering
            filteredEvents = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.board.write_highscore()
                    self.board.write_board()

                if not self.running:
                    activeScene.Terminate()
                else:
                    filteredEvents.append(event)
            
            activeScene.ProcessInput(filteredEvents, pressedKeys)
            activeScene.Update()
            activeScene.Render()
            activeScene = activeScene.next
            pygame.display.flip()
            clock.tick(60)
            

        pygame.quit()



if __name__ == '__main__':
    App().run()