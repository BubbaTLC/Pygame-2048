import pygame
from pygame.locals import *
# pylint: disable=no-member

class App:
    """Create a single-window app with multiple scenes."""

    def __init__(self):
        """Initialize pygame and the application."""
        pygame.init()
        flags = RESIZABLE
        App.screen = pygame.display.set_mode((500,500), flags)
        App.t = Text('Pygame App', pos=(20, 20))

        App.running = True

    def run(self):
        """Run the main event loop."""
        while App.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    App.running = False

            App.screen.fill(Color((255,255,255)))
            pygame.display.update()

        pygame.quit()

    def toggle_fullscreen(self):
        """Toggle between full screen and windowed screen."""
        self.flags ^= pygame.display.FULLSCREEN
        pygame.display.set_mode((0, 0), self.flags)

    def toggle_resizable(self):
        """Toggle between resizable and fixed-size window."""
        self.flags ^= pygame.display.RESIZABLE
        pygame.display.set_mode(self.rect.size, self.flags)

    def toggle_frame(self):
        """Toggle between frame and noframe window."""
        self.flags ^= pygame.display.NOFRAME
        pygame.display.set_mode(self.rect.size, self.flags)

class Scene:
    """Create a new scene (room, level, view)."""
    id = 0
    bg = Color((64,64,64, 200))

    def __init__(self, *args, **kwargs):
        # Append the new scene and make it the current scene
        App.scenes.append(self)
        App.scene = self
        self.id = Scene.id
        Scene.id += 1
        self.nodes = []
        self.bg = Scene.bg

    def draw(self):
        """Draw all objects in the scene."""
        App.screen.fill(self.bg)
        for node in self.nodes:
            node.draw()
        pygame.display.flip()

class Text:
    """Create a text object."""
    def __init__(self, text, pos, **options):
        self.text = text
        self.pos = pos

        self.fontname = None
        self.fontsize = 72
        self.fontcolor = Color((255,255,255))
        self.set_font()
        self.render()

    def render(self):
        """Render the text into an image."""
        self.img = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos

    def set_font(self):
        """Set the font from its name and size."""
        self.font = pygame.font.Font(self.fontname, self.fontsize)

    def draw(self):
        """Draw the text image to the screen."""
        App.screen.blit(self.img, self.rect)

class Demo(App):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    Demo().run()