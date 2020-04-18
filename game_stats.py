class GameStats() :
    """Tracking statistics for Alien Invasion"""

    def __init__(self, ai_settings) :
        """Initilizes game stats"""

        self.ai_settings = ai_settings
        self.reset_stats()

        # Start game in inactive mode
        self.game_active = False

        # High score (do not reset)
        self.high_score = 0

    def reset_stats(self) :
        """Initialize stats to change during the game"""

        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.ship_level = 1
