###############################################################################
# Settings for Up and Down the River (a card game)
#
###############################################################################

class Settings() :
    """Class to store all the settings for Up and Down the River Game"""

    def __init__(self) :
        """Initializes static settings"""

        # #Screen Settings
        # self.screen_width = 1200
        # self.screen_height = 800
        # self.bg_color = (230, 230, 230)

        #Basic options
        self.game_option = ["Single Player", "Multiplayer"]
        self.number_of_players_option = [3, 4, 5, 6, 7, 8]
        self.game_difficulty_option = ["Easy", "Intermediate", "Hard"]
        self.exact_mode_option = True

        #Basic Settings
        self.game = "Multiplayer"
        self.number_of_players = 3
