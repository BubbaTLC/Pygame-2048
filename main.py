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
        mainMenu = MenuScene(self.screen)
        gameScene = GameScene(self.board,self.screen)
        endScene = EndScene(self.board,self.screen)
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
            activeScene.Render()
            activeScene = activeScene.next
            pygame.display.flip()

        pygame.quit()



if __name__ == '__main__':
    App().run()