import pygame
from pygame.sprite import Sprite

class Bullet(Sprite) :
    """Class to manage the bullets"""

    def __init__(self, ai_settings, screen, ship) :
        """Creates a bullet object from the ship's current loc"""

        super().__init__()
        self.screen = screen

        # creating initial bullet position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        #store bullet position as decimal
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self) :
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self) :
        pygame.draw.rect(self.screen, self.color, self.rect)
