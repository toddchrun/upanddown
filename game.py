################################################
# Up and Down the River (A card game)          #
################################################

import pygame
from settings import Settings
from pygame.sprite import Group
from player import Player
from deck import Deck
from scoreboard import Scoreboard
from settings import Settings
import game_functions as gf


def run_game() :
    """Initializes the game and creates a screen object"""

    # pygame.init()


    # screen = pygame.display.set_mode(
    #     (uadtr_settings.screen_width,uadtr_settings.screen_height))
    # pygame.display.set_caption("Up and Down the River")


    #TESTING#
###################################

################Initial Sets################

    settings = Settings()

    #Add active players to array NEED MAJOR UPDATES HERE
    active_players = []
    i = 0
    while i < settings.number_of_players:
        new_player_name = "Player " + str(i+1)
        new_player = Player(new_player_name)
        active_players.append(new_player.player)
        i = i + 1

    #Set dealer
    active_players[0]['dealer'] = True

    #setting up new
    deck = Deck()

    #scoreboard
    score = Scoreboard()

################Initial Sets################


################Gameplay####################

    for idx in range(0, len(settings.round_array)):

        curr_round = settings.round_array[idx]

        #Beginning each round
        shuffled_deck = deck.shuffle() #fresh shuffle

        gf.deal_round(shuffled_deck, curr_round, active_players)
        trick_card = gf.get_trick(shuffled_deck)
        trick_suit = trick_card['suit']

        #Bid round
        gf.bid_round(curr_round, active_players, trick_card)

        #Play round
        gf.play_round(curr_round, active_players, trick_suit)

        #Display score
        score.get_score(active_players)

################Gameplay####################

run_game()
