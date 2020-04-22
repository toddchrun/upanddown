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

    # pygame.init()
    settings = Settings()

    # screen = pygame.display.set_mode(
    #     (uadtr_settings.screen_width,uadtr_settings.screen_height))
    # pygame.display.set_caption("Up and Down the River")


    #TESTING#
###################################

################Initial Sets################
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

    #Current round - shuffle up a new deck
    curr_round = settings.round
################Initial Sets################


################Gameplay####################

    #Beginning each round
    shuffled_deck = deck.shuffle() #fresh shuffle

    gf.deal_round(shuffled_deck, curr_round, active_players)
    trick_card = gf.get_trick(shuffled_deck)
    trick_suit = trick_card['suit']

    #Bid round
    gf.bid_round(curr_round, active_players, trick_card)

    #Play round
    gf.play_round(curr_round, active_players, trick_suit)














    # #PURE TESTING
    # print("The Trick Card is " + trick_card['display'])
    #
    # for i in active_players:
    #     print("\n" + i['name'] + " your hand is: ")
    #     for j in i['hand']:
    #         print(j['display'])
    #
    # print(settings.round_array)


run_game()
