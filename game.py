################################################
# Up and Down the River (A card game)          #
################################################

import pygame
from settings import Settings
from pygame.sprite import Group
from player import Player
from deck import Deck
from settings import Settings


def run_game() :
    """Initializes the game and creates a screen object"""

    pygame.init()
    settings = Settings()

    # screen = pygame.display.set_mode(
    #     (uadtr_settings.screen_width,uadtr_settings.screen_height))
    # pygame.display.set_caption("Up and Down the River")


    #Add active players to array
    active_players = []
    i = 0
    while i < settings.number_of_players:
        new_player_name = "Player " + str(i+1)
        new_player = Player(new_player_name)
        active_players.append(new_player.player)
        i = i + 1

    #TESTING
    #setting up new
    deck = Deck()

    #deal out hands - SET THIS UP IN GAME FUNCTIONS
    for i in range(0, len(active_players)):
        dealt_card = deck.draw()
        active_players[i]['hand'].append(dealt_card)

    print(active_players)


run_game()
