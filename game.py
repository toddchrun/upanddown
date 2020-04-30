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
import screen_functions as sf


def run_game() :
    """Initializes the game and creates a screen object"""

################Screen Setting################
    pygame.init()
    settings = Settings()

    screen = pygame.display.set_mode(
        (settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Up and Down the River")

    #Inital scren
    sf.update_screen(settings, screen)
################Screen Setting################


################Initial Sets################

    #Add active players to array NEED MAJOR UPDATES HERE
    active_players = []
    i = 0
    while i < settings.number_of_players:
        new_player_name = "Player " + str(i+1)
        player_id = i
        active_players.append(Player(player_id, new_player_name))
        i += 1

    #Set dealer
    active_players[0].dealer = True

    #Set player position on screen
    sf.set_player_position(settings, screen, active_players)

    #setting up new
    deck = Deck(settings, screen)

    #scoreboard
    score = Scoreboard()

################Initial Sets################

################Testing################
    # shuffled_deck = deck.shuffle()
    #
    # for card in shuffled_deck:
    #     print(card.display)


################Gameplay####################

    for idx in range(0, len(settings.round_array)):

        curr_round = settings.round_array[idx]

        #Beginning each round
        shuffled_deck = deck.shuffle() #fresh shuffle

        gf.deal_round(shuffled_deck, curr_round, active_players)
        trick_card = gf.get_trick(shuffled_deck)

        #Bid round
        gf.bid_round(curr_round, active_players, trick_card)

        #Play round
        gf.play_round(curr_round, active_players, trick_card.suit)

        #Display score
        score.get_score(active_players)

################Gameplay####################

run_game()
