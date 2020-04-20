################################################
# Up and Down the River (A card game)          #
################################################

import pygame
from settings import Settings
from pygame.sprite import Group
from player import Player
from deck import Deck
from settings import Settings
import game_functions as gf


def run_game() :
    """Initializes the game and creates a screen object"""

    pygame.init()
    settings = Settings()

    # screen = pygame.display.set_mode(
    #     (uadtr_settings.screen_width,uadtr_settings.screen_height))
    # pygame.display.set_caption("Up and Down the River")


    #TESTING#
###################################

    #Add active players to array
    active_players = []
    i = 0
    while i < settings.number_of_players:
        new_player_name = "Player " + str(i+1)
        new_player = Player(new_player_name)
        active_players.append(new_player.player)
        i = i + 1

    #setting up new
    deck = Deck()

    #Current round - shuffle up a new deck
    shuffled_deck = deck.shuffle()
    curr_round = settings.round

    gf.deal_round(shuffled_deck, curr_round, active_players)

    print(active_players)


run_game()
