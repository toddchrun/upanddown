###############################################################################
# Class for each player
#
###############################################################################
import pygame
from pygame.sprite import Group

class Player():
    """
    Class for every player
    """

    def __init__(self, settings, screen, player_id, player_name):
        super(Player, self).__init__()

        #Player settings
        self.id = player_id
        self.name = player_name
        self.hand = Group()
        self.dealer = False
        self.turn_active = False
        self.has_only_tricks = False
        self.score = 0
        self.bid = 0
        self.curr_round_tricks = 0

        #Visual settings
        self.x_start = 0.0
        self.y_start = 0.0
        self.x_center = 0.0
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.bg_color = settings.bg_color

        # Font settings - white for now and just default
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 16)

    def set_top_text(self, score, turn_active):
        """Sets text to be displayed at top"""

        #highlights player if it is their active turn
        if turn_active:
            self.bg_color = (0, 0, 150)
        else:
            self.bg_color = self.settings.bg_color

        top_str = self.name + " - Score: " + str(score)
        self.top_image = self.font.render(top_str, True, self.text_color,
            self.bg_color)

        # Display the player name and score at the top of position
        self.top_rect = self.top_image.get_rect()
        self.top_rect.y = self.y_start
        self.top_rect.center = (self.x_center, (self.y_start - (.02 * self.settings.screen_height)))

    def set_bottom_text(self, bid, curr_round_tricks, turn_active):
        """Sets text to be displayed at bottom"""

        bottom_str = "Bid: " + str(bid) + " - Tricks: " + str(curr_round_tricks)
        self.bottom_image = self.font.render(bottom_str, True, self.text_color,
            self.bg_color)

        # Display the current bid at the bottom of position
        self.bottom_rect = self.bottom_image.get_rect()
        self.bottom_rect.y = self.y_start + (.16 * self.settings.screen_height)
        self.bottom_rect.center = (self.x_center, self.bottom_rect.y)

    def show_player(self, score, bid, tricks, turn_active) :
        """Draw player text on the screen after updating score and bid"""

        self.set_top_text(score, turn_active)
        self.set_bottom_text(bid, tricks, turn_active)

        self.screen.blit(self.top_image, self.top_rect)
        self.screen.blit(self.bottom_image, self.bottom_rect)
