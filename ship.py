import pygame
from pygame.sprite import Sprite

class Ship(Sprite) :
    """Module for the ship to be used in alien_invasion.py"""

    def __init__(self, ai_settings, screen) :

        super().__init__()

        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Set up a decimal value for the ship's center
        self.center = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)

        # Movement right flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self) :
        """Update position of the ship based on flags"""
        if self.moving_right and self.rect.right < self.screen_rect.right :
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0 :
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0 :
            self.bottom -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom <= self.screen_rect.bottom :
            self.bottom += self.ai_settings.ship_speed_factor

        # update the rect object's position
        self.rect.centerx = self.center
        self.rect.bottom = self.bottom

    def center_ship(self) :
        """Center ship on the screen"""
        self.center = self.screen_rect.centerx
        self.bottom = self.screen_rect.bottom

    def blitme(self) :

        self.screen.blit(self.image, self.rect)
