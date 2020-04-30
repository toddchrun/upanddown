###############################################################################
#   Card Class
#   Inherits Pygame Sprites, used to display for each player and given hand!
###############################################################################
import pygame
from pygame.sprite import Sprite

class Card(Sprite):

    def __init__(self, settings, screen, suit, value, display):
        """
        Initalizes each card to be displayed
        """

        super().__init__()

        #Visual Settings for each card
        self.settings = settings
        self.screen = screen

        self.image = pygame.image.load('images/' + display + '.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

        #Card settings
        self.suit = suit
        self.value = value
        self.display = display


    def blitme(self) :
        """Draw card at current location"""

        self.screen.blit(self.image, self.rect)
