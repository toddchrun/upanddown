"""
Game functions for Up and Down the River
"""
import sys
import pygame
from random import randint

#Deal round based on current deck, round and overall number of players
def deal_round(curr_deck, curr_round, active_players):
    #Total cards
    max_index = 52

    #Deal out cards (number based on current round) to each player
    while curr_round > 0:
        for i in range(0, len(active_players)):
            index = randint(0, max_index)
            dealt_card = curr_deck[index]
            active_players[i]['hand'].append(dealt_card)
            curr_deck.pop(index)
            max_index = max_index - 1
        curr_round = curr_round - 1

    #Deal out trick_card for last step
    trick_index = randint(0, max_index)
    trick_card = curr_deck[trick_index]

def get_trick(curr_deck):
    #Deal out trick_card for last step
    trick_index = randint(0, len(curr_deck))
    trick_card = curr_deck[trick_index]
    return trick_card
