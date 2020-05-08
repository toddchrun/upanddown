###############################################################################
#   Table Class
###############################################################################
import pygame
from pygame import gfxdraw

class Table():
    """
    Class for every deck
    """

    def __init__(self, settings, screen):

        super().__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings

        #load table image
        self.image = pygame.image.load('images/table.png')
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center

        #defines dimensions for box surrounding trick card
        self.trick_box_x = self.settings.trick_x - (.005 * self.settings.screen_width)
        self.trick_box_y = self.settings.trick_y - (.01 * self.settings.screen_height)
        self.trick_box_width = (self.settings.screen_width * (.0525 + .01))
        self.trick_box_height = (self.settings.screen_height * (.14375 + .02))

        #defines deck image to display
        self.deck_image = pygame.image.load('images/card.png')
        self.deck_rect = self.deck_image.get_rect()
        self.deck_image = pygame.transform.scale(self.deck_image, (int(self.deck_rect.width / 2), int(self.deck_rect.height / 2)))
        self.deck_rect.x = self.settings.trick_x - (self.settings.screen_width * .07)
        self.deck_rect.y = self.settings.trick_y

    def blitme(self):

        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.deck_image, self.deck_rect)
        pygame.gfxdraw.rectangle(self.screen, (self.trick_box_x, self.trick_box_y, self.trick_box_width, self.trick_box_height), (255, 255, 255))
