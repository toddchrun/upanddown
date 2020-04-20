"""
Game functions for Up and Down the River
"""
import sys
import pygame
from random import randint

#Deal round based on current deck, round and overall number of players
def deal_round(curr_deck, curr_round, active_players):
    while curr_round > 0:
        for i in range(0, len(active_players)):
            index = randint(0,52)
            dealt_card = curr_deck[index]
            active_players[i]['hand'].append(dealt_card)
            curr_deck.pop(index)
        curr_round = curr_round - 1
