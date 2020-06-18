"""
Table Class - Base image for the game
"""
import pygame
from pygame import gfxdraw

class Table():
    """
    Class for the stable table image
    """

    def __init__(self, settings, screen):

        super().__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings

        #load table image
        self.image = pygame.image.load('resources/images/table.png')
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center

        #defines dimensions for box surrounding trick card
        self.trick_box_x = self.settings.trick_x - (.005 * self.settings.screen_width)
        self.trick_box_y = self.settings.trick_y - (.01 * self.settings.screen_height)
        self.trick_box_width = (self.settings.screen_width * (.0525 + .01))
        self.trick_box_height = (self.settings.screen_height * (.14375 + .02))

    def blitme(self):

        self.screen.blit(self.image, self.rect)
        pygame.gfxdraw.rectangle(self.screen, (self.trick_box_x, self.trick_box_y, self.trick_box_width, self.trick_box_height), (255, 255, 255))
