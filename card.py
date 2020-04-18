###############################################################################
# Class for each card
#
###############################################################################

class Card():
    """
    Class for every card
    """

    def __init__(self, rank, suit):
        super(Card, self).__init__()

        ranks = {2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9",
            10: "10", 11: "J", 12: "Q", 13: "K", 14: "A"}
        suits = ["c", "s", "d", "h"]

        self.rank = ranks{rank}
        self.suit = suits[suit]

        return {rank, suit}
