###############################################################################
# Class for each player
#
###############################################################################

class Player():
    """
    Class for every player
    """

    def __init__(self, player_id, player_name):
        super(Player, self).__init__()

        #Player settings
        self.id = player_id
        self.name = player_name
        self.hand = []
        self.dealer = False
        self.score = 0
        self.bid = 0
        self.curr_round_tricks = 0
        self.screen_position = 0
