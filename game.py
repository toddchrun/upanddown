################################################
# Up and Down the River (A card game)          #
################################################

import pygame
from settings import Settings
import game_functions as gf
from pygame.sprite import Group
from scoreboard import Scoreboard
from player import Player


def run_game() :
    """Initializes the game and creates a screen object"""

    pygame.init()
    uadtr_settings = Settings()

    # screen = pygame.display.set_mode(
    #     (uadtr_settings.screen_width,uadtr_settings.screen_height))
    # pygame.display.set_caption("Up and Down the River")

    #Add active players to array
    active_players = []
    while i < uadtr_settings.number_of_players.length() :
        active_players.append("Player" + i)
        i = i + 1

    




run_game()
