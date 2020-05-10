###############################################################################
# Settings for Up and Down the River (a card game)
#
###############################################################################
import math

class Settings() :
    """Class to store all the settings for Up and Down the River Game"""

    def __init__(self) :
        """Initializes static settings"""

        #Screen Settings
        self.screen_width = 1400
        self.screen_height = 800
        self.bg_color = (34, 139, 34)

        #Basic options
        self.game_option = ["Single Player", "Multiplayer"]
        self.number_of_players_option = [3, 4, 5, 6, 7, 8]
        self.game_difficulty_option = ["Easy", "Intermediate", "Hard"]
        self.exact_mode_option = True

        #Basic settings
        self.game = "Multiplayer"
        self.number_of_players = 8
        self.starting_round = 1
        self.max_rounds_available = math.trunc(53 / self.number_of_players)
        self.trick_x = self.screen_width * .35 #trick set
        self.trick_y = (self.screen_height / 2) - (.071875 * self.screen_height) #Set for card to be centered

        #Make sure max rounds will have enough cards!
        self.max_rounds = 3
        try:
            self.max_rounds < self.max_rounds_available
        except:
            self.max_rounds = self.max_rounds_available

        #Sets an array for number of cards to be dealt in a given round
        self.round_array = []
        for round in range(self.starting_round, self.max_rounds+1):
            self.round_array.append(round)
        for round in range(self.starting_round, self.max_rounds+1):
            self.round_array.insert(self.max_rounds, round) #continually adds to countdown from max to 1
