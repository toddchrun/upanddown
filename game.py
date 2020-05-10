################################################
# Up and Down the River (A card game)          #
################################################

import pygame
import time
from random import randint
from settings import Settings
from pygame.sprite import Group
from player import Player
from deck import Deck
from table import Table
from discard_pile import Pile
from scoreboard import Scoreboard
from settings import Settings
from action_message import Message
import game_functions as gf
import screen_functions as sf


def run_game() :
    """Initializes the game and creates a screen object"""

################Screen Setting################
    pygame.init()
    settings = Settings()

    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Up and Down the River")

################Screen Setting################


################Initial Sets################

    #Add active players to array NEED MAJOR UPDATES HERE
    active_players = []
    i = 0
    while i < settings.number_of_players:
        new_player_name = "Player " + str(i+1)
        player_id = i
        active_players.append(Player(settings, screen, player_id, new_player_name))
        i += 1

    #Set dealer
    active_players[0].dealer = True

    #Set player position on screen
    sf.set_player_position(settings, screen, active_players)

    #setting up new deck
    deck = Deck(settings, screen)

    #scoreboard
    score = Scoreboard()

    #table instance
    table = Table(settings, screen)

    #active message instance
    message = Message(settings, screen)

################Initial Sets################

################Testing################

    # curr_round = 6
    #
    # #Beginning each round
    # shuffled_deck = deck.shuffle() #fresh shuffle
    #
    # #Refreshes the discard pile
    # pile = Pile(settings, screen)
    #
    # gf.deal_round(shuffled_deck, curr_round, active_players)
    # trick_card = gf.get_trick(shuffled_deck)
    # trick_card.update_card_position(settings.trick_x, settings.trick_y)
    # trick_card.flip_card()
    #
    # for card in active_players[0].hand:
    #     card.flip_card()
    #
    # #Sets each card's position to be displayed
    # sf.sort_cards(active_players, trick_card)
    # sf.set_card_pos(settings, screen, active_players)
    #
    # while True:
    #     sf.update_screen(settings, screen, table, active_players, pile, trick_card)
    #     sf.check_events(settings, screen, table, active_players, pile)

################Gameplay####################

    for idx in range(0, len(settings.round_array)):

        #cycles through round array to get number of cards to deal
        curr_round = settings.round_array[idx]

        #Beginning each round with a fresh deck
        shuffled_deck = deck.shuffle(settings, screen)

        #Refreshes the discard pile
        pile = Pile(settings, screen)

        #start of each round - deal out cards to every player and then flip a trick card
        gf.deal_round(shuffled_deck, curr_round, active_players)
        trick_card = gf.get_trick(shuffled_deck)
        trick_card.update_card_position(settings.trick_x, settings.trick_y)
        # trick_card.flip_card()

        #sorts the fresh hand for everyone and updates screen positions
        sf.sort_cards(active_players, trick_card)
        sf.set_card_pos(settings, screen, active_players)

        #Bid round - pass around each turn until
        gf.bid_round(settings, screen, table, curr_round, active_players, pile, trick_card, message)

        #Play round
        gf.play_round(settings, screen, table, curr_round, active_players, pile, trick_card, message)


################Gameplay####################

run_game()
