###############################################################################
#   Card Class
#   Inherits Pygame Sprites, used to display for each player and given hand!
###############################################################################
import pygame
from pygame.sprite import Sprite

class Card(Sprite):

    def __init__(self, settings, screen, suit, value, display, sort_index):
        """
        Initalizes each card to be displayed
        """

        super().__init__()

        #Visual Settings
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        #Card settings
        self.suit = suit
        self.value = value
        self.display = display
        self.sort_index = sort_index
        self.face_up = False
        self.selected = False
        self.play = False #set to true if the computer is to play card
        self.trick_broken = False
        self.valid = False #processed each turn, needs to be True to be able to play
        self.played_id = int()  #tracks the person that played the card

        #Set card face down image
        self.image = pygame.image.load('images/card.png')
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (int(self.rect.width / 2), int(self.rect.height / 2)))
        self.rect = self.image.get_rect()

    def blitme(self) :
        """Draw card at current location"""

        self.screen.blit(self.image, self.rect)


    def update_card_position(self, pos_x, pos_y):
        """Sets specfic location of each card based on screen object"""

        self.rect.x = pos_x
        self.rect.y = pos_y

    def flip_card(self):
        """Flips display"""

        self.face_up = not self.face_up

        if self.face_up:
            self.image = pygame.image.load('images/' + self.display + '.png')
            self.image = pygame.transform.scale(self.image, (int(self.rect.width), int(self.rect.height)))
        else:
            self.image = pygame.image.load('images/card.png')
            self.image = pygame.transform.scale(self.image, (int(self.rect.width), int(self.rect.height)))

    def select_card(self):
        """Switches card as candidate for selection, needs double click feature"""

        self.selected = True
        self.rect.y -= (.01 * self.settings.screen_height)

    def deselect_card(self):
        """Switches card back to not being a play candidate"""

        self.selected = False
        self.rect.y += (.01 * self.settings.screen_height)
