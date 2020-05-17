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
            for card in player.hand:
                card.valid = True
        else:
            for card in player.hand:
                if card.suit != trick_card.suit:
                    card.valid = True
    else:
        #if player has the first suit played, they can only play that suit
        has_suit = False

        #gets the suit of the first card played, which dictates play for the round
        round_hand = pile.discards.sprites()

        #cycles through player hand to see if they have first play suit
        for card in player.hand:
            if card.suit == round_hand[0].suit:
                has_suit = True
                break

        #add all cards to valid list if they don't have starting suit
        if not has_suit:
            for card in player.hand:
                card.valid = True
        else:
            for card in player.hand:
                if card.suit == round_hand[0].suit:
                    card.valid = True

    if player.difficulty == 'Easy':
        determine_play_easy(settings, screen, pile, player, trick_card)
    elif player.difficulty == 'Intermediate':
        determine_play_intermediate(settings, screen, pile, player, trick_card)


def determine_play_easy(settings, screen, pile, player, trick_card):
    """Determines what card to play based on easy mode"""

    #counts number of valid cards and adds them to dummy list
    valid_cards = 0
    valid_hand = []
    for card in player.hand:
        if card.valid:
            valid_cards += 1
            valid_hand.append(card)

    #completely random selection of any valid card - easy mode
    index = randint(0, valid_cards - 1)
    valid_card = valid_hand[index]

    #matches card to play within Grouping
    for card in player.hand:
        if card.display == valid_card.display:
            play_card(settings, screen, player, pile, card)

    set_card_validity(player)

def determine_play_intermediate(settings, screen, pile, player, trick_card):
    """Determines what card to play based on intermediate mode"""

    #determining boolean values
    needs_trick = False
    trick_valid = False
    first_play = False
    has_trick = False

    #determines if first play
    if len(pile.discards) == 0:
        first_play = True

    #determines if the player needs a trick
    if player.curr_round_tricks < player.bid:
        needs_trick = True

    #determines if player has a trick
    for crd in player.hand:
        if crd.suit == trick_card.suit:
            has_trick = True
            break

    #determines if player has a trick card that is valid
    for crd in player.hand:
        if (crd.suit == trick_card.suit) and (crd.valid):
            trick_valid = True
            break


####################PLAY DETERMINATION TREE#####################################

    if first_play:
        #covers all first play scenarios

        if needs_trick:
            #first play and needs trick, first determine if they have a trick at all

            if has_trick:
                #needs trick and has one in hand, determine if trick is an actual valid play

                if trick_valid:
                    #if has a trick in valid hand and needs trick, play the highest
                    value = determine_highest_trickvalue(player, trick_card)
                    for card in reversed(player.hand.sprites()): #reverse sort to find the highest value (making sure a trick)
                        if card.value == value:
                            play_card(settings, screen, player, pile, card)
                            break
                else:
                    #if has a trick, needs a trick, but not valid, play lowest card
                    value = determine_lowest_value(player)
                    for card in player.hand:
                        if card.value == value:
                            play_card(settings, screen, player, pile, card)
                            break

            else:
                #needs a trick but doesn't have one so play highest possible card
                value = determine_highest_nontrickvalue(player, trick_card)
                for card in player.hand:
                    if card.value == value:
                        play_card(settings, screen, player, pile, card)
                        break

        else:
            #first play and doesn't need trick so play lowest card
            value = determine_lowest_value(player)
            for card in player.hand:
                if card.value == value:
                    play_card(settings, screen, player, pile, card)
                    break

    else:
        #covers all the scenarios where it isn't the first play

        if needs_trick:
            #not the first play and covers scenarios of whether they need trick or not

            if has_trick:
                #needs and trick and has trick in whole hand

                if trick_valid:
                    #needs trick and has one in valid hand, play highest
                    value = determine_highest_trickvalue(player, trick_card)
                    for card in reversed(player.hand.sprites()): #reversed order to make sure it's a trick
                        if card.value == value:
                            play_card(settings, screen, player, pile, card)
                            break

                else:
                    #needs a trick and has one, but not valid, so play lowest
                    value = determine_lowest_value(player)
                    for card in player.hand:
                        if card.value == value:
                            play_card(settings, screen, player, pile, card)
                            break

            else:
                #needs a trick but doesn't have one, play highest hoping to take
                value = determine_highest_nontrickvalue(player, trick_card)
                for card in player.hand:
                    if card.value == value:
                        play_card(settings, screen, player, pile, card)
                        break

        else:
            #doesn't have a trick and doesn't need one, play lowest card
            value = determine_lowest_value(player)
            for card in player.hand:
                if card.value == value:
                    play_card(settings, screen, player, pile, card)
                    break

####################PLAY DETERMINATION TREE#####################################

    set_card_validity(player)

def play_card(settings, screen, player, pile, card):
    """Play the card selected and add to discard pile"""

    card.played_id = player.id
    sf.add_to_discard_pile(settings, screen, pile, card)
    card.valid = False #reset validity for future play
    player.hand.remove(card)
    player.turn_active = False

def set_card_validity(player):
    """Sets all remaining cards in a hand to be not valid"""

    for card in player.hand:
        card.valid = False

def determine_lowest_value(player):
    """Determines lowest value in the player's valid hand"""

    low_value = 15 #highest possible value

    for card in player.hand:
        if (card.value < low_value) and (card.valid):
            low_value = card.value

    return low_value

def determine_highest_nontrickvalue(player, trick_card):
    """Determines highest non-trick value in the player's valid hand"""

    high_value = 0 #lowest possible value

    for card in player.hand:
        if (card.value > high_value) and (card.valid) and (card.suit != trick_card.suit):
            high_value = card.value

    return high_value

def determine_highest_trickvalue(player, trick_card):
    """Determines highest trick value in the player's valid hand"""

    high_value = 0 #highest possible value

    for card in player.hand:
        if (card.value > high_value) and (card.valid) and (card.suit == trick_card.suit):
            high_value = card.value

    return high_value
