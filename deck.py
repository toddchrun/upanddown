###############################################################################
# Class for each card
#
###############################################################################
from card import Card

class Deck():
    """
    Class for every deck
    """

    def __init__(self):
        super(Deck, self).__init__()
        suit_index = ["c", "s", "d", "h"]
        value_index = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

        full_deck = []

        for s_index, v_index in suit_index, value_index:
            full_deck.insert(Card{v_index, s_index})
            
