###############################################################################
#   Deck Class
#   Used to build initial deck of 52 cards (plus insertion of Joker)
#   Function to draw - returns random card while keeping track of its index
###############################################################################
import pygame
from card import Card

class Deck():
    """
    Class for every deck
    """

    def __init__(self, settings, screen):
        super(Deck, self).__init__()

        #Visual Settings
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        #Set deck image
        self.image = pygame.image.load('images/card.png')
        self.rect = self.image.get_rect()

        #Scales the original card to half its size and places it on left side of table
        self.image = pygame.transform.scale(self.image, (int(self.rect.width / 2), int(self.rect.height / 2)))
        self.rect = self.image.get_rect()
        self.rect.x = self.settings.trick_x - (self.settings.screen_width * .07)
        self.rect.y = self.settings.trick_y

        #initialize indices
        self.suit_index = ["s", "c", "d", "h"]
        self.value_index = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
            '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

        #initialize a full deck array
        self.full_deck = []
        self.dealt = False

    def build_deck(self, settings, screen):

        sort_index = 0
        #build a deck of 52 cards, Ace through King, 4 suits
        for suit in self.suit_index:
            for key, value in self.value_index.items():
                self.display = key + suit
                card = Card(settings, screen, suit, value, self.display, sort_index)
                self.full_deck.append(card)
                sort_index += 1

        #Add the Joker! (It trumps everything)
        joker = Card(settings, screen, "joker", 15, "JK", sort_index)
        self.full_deck.append(joker)

    def shuffle(self, settings, screen):
        """Resets the list and builds a fresh deck"""

        self.full_deck = []
        self.build_deck(settings, screen)
        return self.full_deck


    def show_deck(self):
        """Shows the back of the card to represent the deck"""

        self.screen.blit(self.image, self.rect)
