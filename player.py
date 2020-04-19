###############################################################################
# Class for each player
#
###############################################################################

class Player():
    """
    Class for every player
    """

    def __init__(self, player_name):
        super(Player, self).__init__()

        #Player settings
        self.player_name = player_name
        self.player_hand = []
        self.player = {'name': self.player_name, 'hand': self.player_hand}
