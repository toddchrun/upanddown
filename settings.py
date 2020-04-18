class Settings() :
    """Class to store all the settings for alien_invasion.py"""

    def __init__(self) :
        """Initializes static settings"""

        #Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #Score settings
        self.score_height = 20
        self.score_right = 20

        #Ship settings
        self.ship_limit = 3

        #Bullet settings
        self.bullet_width = 3
        self.bullet_height = 20
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 4

        #Alien settings
        self.alien_drop_speed = 10
        self.alien_points = 50

        # Game speed up factor
        self.speedup_scale = 1.5

        # Alien point speed up
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self) :
        """Initialize settings that change throughout the game"""

        self.ship_speed_factor = 2
        self.bullet_speed_factor = 4
        self.alien_speed_factor = 1
        self.fleet_direction = 1

    def increase_speed(self) :
        """Increases the speed settings"""

        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        
