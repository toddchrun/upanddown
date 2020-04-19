###############################################################################
#   Deck Class
#   Used to build initial deck of 52 cards (plus insertion of Joker)
#   Function to draw - returns random card while keeping track of its index
###############################################################################
from random import randint

class Deck():
    """
    Class for every deck
    """

    def __init__(self):
        super(Deck, self).__init__()

        #initialize indices
        self.suit_index = ["c", "s", "d", "h"]
        self.value_index = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
            '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

        #initialize a full deck array
        self.full_deck = []

        #initialize empty array to keep track of cards already dealt
        self.used_card_index = []

        #build full deck
        self.build_deck();

    def build_deck(self):

        #build a deck of 52 cards, Ace through King, 4 suits
        for suit in self.suit_index:
            for key, value in self.value_index.items():
                self.display = key + suit
                self.full_deck.append({'suit': suit, 'value': value, 'display': self.display})

        #Add the Joker! (It trumps everything)
        self.full_deck.append({'suit': "", 'value': 15, 'display': "JK"})

    def draw(self):
        return self.full_deck[randint(0,52)]

    
