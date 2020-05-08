###############################################################################
#   Deck Class
#   Used to build initial deck of 52 cards (plus insertion of Joker)
#   Function to draw - returns random card while keeping track of its index
###############################################################################
from card import Card

class Deck():
    """
    Class for every deck
    """

    def __init__(self, settings, screen):
        super(Deck, self).__init__()

        #initialize indices
        self.suit_index = ["s", "c", "d", "h"]
        self.value_index = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
            '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

        #initialize a full deck array
        self.full_deck = []

        # #build full deck
        # self.build_deck(settings, screen);

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
        self.full_deck = []
        self.build_deck(settings, screen)
        return self.full_deck
