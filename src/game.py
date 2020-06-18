################################################
# Up and Down the River (A card game)
# Copyright Todd Chrun 2020
# Version 1.0.0
################################################

import pygame
import time
from random import randint
from pygame.sprite import Group

from settings import Settings
from player import Player
from deck import Deck
from table import Table
from discard_pile import Pile
from scoreboard import Scoreboard
from action_message import Message
from prompt_screen import PromptScreen

import game_functions as gf
import screen_functions as sf


def run_game() :
    """Initializes the game and creates a screen object"""

################Initial Sets and Prompt Screen ################
    pygame.init()
    settings = Settings()

    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Up and Down the River")

    prompt_screen = PromptScreen(settings, screen)
    active_players = []

    while not prompt_screen.play_button.game_active:
        sf.prompt_screen(settings, screen, prompt_screen)
        sf.check_for_prompts(settings, screen, prompt_screen, active_players)

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

    #set the round array
    settings.set_round_array()

################Initial Sets and Prompt Screen ################

################Testing################
################Testing################

################Gameplay####################
    counter = 0
    for round in settings.round_array:
        counter += 1
        curr_round = round

        #cycles through round array to get number of cards to deal
        message.update_title("Round " + str(counter))

        #Beginning each round with a fresh deck
        shuffled_deck = deck.shuffle(settings, screen)

        #Refreshes the discard pile
        pile = Pile(settings, screen)

        #start of each round - deal out cards to every player and then flip a trick card
        gf.deal_round(settings, screen, table, active_players, pile, message, deck, shuffled_deck, curr_round)
        trick_card = gf.get_trick(shuffled_deck)
        trick_card.update_card_position(settings.trick_x, settings.trick_y)

        #sorts the fresh hand for everyone and updates screen positions
        sf.sort_cards(active_players, trick_card)
        sf.set_card_pos(settings, screen, active_players)

        #Bid round - pass around each turn until
        gf.bid_round(settings, screen, table, curr_round, active_players, pile, trick_card, message, deck)

        #Play round
        gf.play_round(settings, screen, table, curr_round, active_players, pile, trick_card, message, deck)

    #End of game, display the winner
    final_score = score.get_score(active_players)
    message.update_message(final_score[0][0] + " wins the game!", 0)
    while True:
        sf.clear_screen(settings, screen, table, active_players, message)
        sf.check_for_exit()

################Gameplay####################

run_game()
