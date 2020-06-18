"""
Initial settings for Up and Down the River
"""
class Settings() :

    def __init__(self) :
        """Initializes static settings"""

        #Screen Settings
        self.screen_width = 1400
        self.screen_height = 800
        self.bg_color = (34, 139, 34)

        #Basic settings
        self.number_of_players_option = [3, 4, 5, 6, 7, 8]
        self.number_of_players = int()

        self.game_difficulty_option = ["Easy", "Intermediate", "Hard"]
        self.game_difficulty = str()

        self.starting_round = 1
        self.max_rounds_available = 9
        self.max_rounds = int()

        #trick card screen settings
        self.trick_x = self.screen_width * .35 #trick set
        self.trick_y = (self.screen_height / 2) - (.071875 * self.screen_height) #Set for card to be centered

    def set_round_array(self):
        #Sets an array for number of cards to be dealt in a given round
        self.round_array = []
        for round in range(self.starting_round, self.max_rounds+1):
            self.round_array.append(round)
        for round in range(self.starting_round, self.max_rounds+1):
            self.round_array.insert(self.max_rounds, round) #continually adds to countdown from max to 1
