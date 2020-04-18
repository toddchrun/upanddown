import pygame
from pygame.sprite import Sprite

class Alien(Sprite) :
    """Class to represent each alien in the game"""

    def __init__(self, ai_settings, screen) :
        """Initialies an alien and sets starting position"""

        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #load the alien image
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #start each alien at the top left position
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def check_edges(self) :
        """Return true if alien hits edge of the screen"""

        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right :
            return True
        elif self.rect.left <= 0 :
            return True

    def update(self) :
        """Move alien right or left"""

        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

    def blitme(self) :
        """Draw alien at current location"""

        self.screen.blit(self.image, self.rect)
