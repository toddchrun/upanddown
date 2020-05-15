"""
Computer AI functions for Up and Down the River
For now, this will be an 'easy' or 'intermediate' setting
"""

import sys
import pygame
from table import Table
from random import randint
from discard_pile import Pile
from pygame.sprite import Group
import screen_functions as sf

def bid(player, trick_card):
    """Sets computer controlled bid based on current hand"""

    bid = 0

    #increments bid if computer has a trick suit or Ace
    for card in player.hand:
        if (card.suit == trick_card.suit) or (card.display in ['Ac', 'As', 'Ad', 'Ah']):
            bid += 1

    player.bid = bid

def play(settings, screen, player, trick_card, pile, curr_round):
    """Sets computer play based on what has been played, etc."""

    if len(pile.discards) == 0:
        if player.has_only_tricks or trick_card.trick_broken:
            for crd in player.hand:
                player.valid_cards.add(crd)
        else:
            for crd in player.hand:
                if crd.suit != trick_card.suit:
                    player.valid_cards.add(crd) #appends every other card other than tricks
    else:
        #if player has the first suit played, they can only play that suit
        has_suit = False

        #gets the suit of the first card played, which dictates play for the round
        round_hand = pile.discards.sprites()

        #cycles through player hand to see if they have first play suit
        for crd in player.hand:
            if crd.suit == round_hand[0].suit:
                has_suit = True
                break

        #add all cards to valid list if they don't have starting suit
        if not has_suit:
            for crd in player.hand:
                player.valid_cards.add(crd)
        else:
            for crd in player.hand:
                if crd.suit == round_hand[0].suit:
                    player.valid_cards.add(crd)

    determine_play(settings, screen, pile, player)


def determine_play(settings, screen, pile, player):
    """Determines what card to play based on current situation"""

    #for now, as easy as it gets, random selection
    index = randint(0, len(player.valid_cards) - 1)
    valid_hand = player.valid_cards.sprites()
    valid_card = valid_hand[index]

    for card in player.hand.sprites():
        if card.display == valid_card.display:
            card.played_id = player.id
            sf.add_to_discard_pile(settings, screen, pile, card)
            player.hand.remove(card)
            player.turn_active = False

    player.valid_cards.empty()
