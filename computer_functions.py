"""
Computer AI functions for Up and Down the River
For now, this will be an 'easy' or 'intermediate' setting
"""

import sys
import pygame
import math
from table import Table
from random import randint
from discard_pile import Pile
from pygame.sprite import Group
import screen_functions as sf

def bid(settings, player, trick_card, active_players, curr_round):
    """Sets computer controlled bid based on current hand"""

    if player.difficulty == settings.game_difficulty_option[0]:
        determine_bid_easy(player, trick_card)
    elif player.difficulty == settings.game_difficulty_option[1]:
        determine_bid_intermediate(player, trick_card, active_players, curr_round)
    elif player.difficulty == settings.game_difficulty_option[2]:
        determine_bid_hard(player, trick_card, active_players, curr_round)

def determine_bid_easy(player, trick_card):
    """For easy mode, increments bid if player has an ace or trick"""

    bid = 0

    #increments bid if computer has a trick suit or Ace
    for card in player.hand:
        if (card.suit == trick_card.suit) or (card.display in ['Ac', 'As', 'Ad', 'Ah']):
            bid += 1

    player.bid = bid

def determine_bid_intermediate(player, trick_card, active_players, curr_round):
    """For intermediate mode"""

    player_bid = 0
    curr_bids = 0
    total_cards_left = 0
    open_bid = True #if there is still a trick to take, sets to true

    #set total cards to play
    curr_index = active_players.index(player) #gets current position within round
    tot_players = len(active_players)
    remaining_players = len(active_players[curr_index:]) #number of remaining players
    total_cards_left = curr_round * remaining_players #total cards left in play

    #loops through hand, increments bid based on card value and if there are open bids
    for card in player.hand:
        curr_bids = get_curr_bids(active_players)
        open_bid = get_open_bid(curr_bids, curr_round)

        if open_bid:
            if (card.suit == trick_card.suit): #bid one if you have a trick
                player_bid += 1

        else:
            if (card.suit == trick_card.suit) and (card.value >= (max(0, math.trunc(tot_players - curr_round) / tot_players) * 15)):
                player_bid += 1

    player.bid = player_bid

def determine_bid_hard(player, trick_card, active_players, curr_round):
    """For hard mode"""

    #variables needed
    player_bid = 0
    curr_bids = 0
    total_cards_left = 0
    player_tricks = 0
    player_non_tricks = 0
    tricks_remaining_avg = 0.0 #total number of expected remaining tricks based on where bidding is
    trick_value_avg = 8.5 #average value of trick
    open_bid = True #if there is still a trick to take, sets to true

    #set total cards to play
    curr_index = active_players.index(player) #gets current position within round
    tot_players = len(active_players)
    remaining_players = len(active_players[curr_index:]) #number of remaining players
    total_cards_left = curr_round * remaining_players - 1 #total cards left in play NOT INCLUDING CURR PLAYER

    #set player tricks and non tricks
    for card in player.hand:
        if card.suit == trick_card.suit:
            player_tricks += 1
        else:
            player_non_tricks += 1

    #set average number of tricks remaining
    tricks_remaining_avg = (14 - player_tricks) / (53 - player_non_tricks) * total_cards_left

    #loops through hand, increments bid based on card value and if there are open bids
    for card in player.hand:
        trick_target_value = 8.5 #shifted expected value based on number of tricks remaining
        curr_bids = get_curr_bids(active_players)
        open_bid = get_open_bid(curr_bids, curr_round)
        trick_factor = tricks_remaining_avg - (curr_round - curr_bids)

        if open_bid:
            if trick_factor <= 1:
                #less expected tricks than open bids, scale trick target value multiplicatively
                trick_target_value *= trick_factor
            else:
                #more expected tricks than open bids, add to target value to be more conservative
                trick_target_value += trick_factor

            if (card.suit == trick_card.suit):
                #increase/decrease how big the trick needed, but ace or higher is a bid no matter what
                if (card.value >= min(math.trunc(trick_target_value), 14)):
                    player_bid += 1
            elif card.value > 14 - max(((curr_round - curr_bids) - tricks_remaining_avg), 0):
                #if not a trick, if remaining average is less than open bids, bid if high
                player_bid += 1

        else:
            trick_target_value += tricks_remaining_avg - ((curr_round - curr_bids) * 2) #only if over-bid
            if (card.suit == trick_card.suit):
                #increase/decrease how big the trick needed, but ace or higher is a bid no matter what
                if (card.value >= min(math.trunc(trick_target_value), 14)):
                    player_bid += 1

    player.bid = player_bid

def get_curr_bids(active_players):
    """Returns count of total bids at the moment"""
    curr_bids = 0
    for player in active_players:
        curr_bids += player.bid

    return curr_bids

def get_open_bid(curr_bids, curr_round):
    """Returns true if there is an open trick card to take"""

    if curr_bids >= curr_round:
        return False
    else:
        return True

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

    if player.difficulty == settings.game_difficulty_option[0]:
        determine_play_easy(settings, screen, pile, player, trick_card)
    elif player.difficulty == settings.game_difficulty_option[1]:
        determine_play_intermediate(settings, screen, pile, player, trick_card)
    elif player.difficulty == settings.game_difficulty_option[2]:
        determine_play_hard(settings, screen, pile, player, trick_card)


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
                    #if has a trick in valid hand and needs trick, only play if player has only tricks

                    if only_tricks_valid(player, trick_card):
                        value = determine_highest_trickvalue(player, trick_card)
                        for card in reversed(player.hand.sprites()): #reverse sort to find the highest value (making sure a trick)
                            if card.value == value:
                                play_card(settings, screen, player, pile, card)
                                break
                    else:
                        value = determine_lowest_value(player, trick_card)
                        for card in player.hand:
                            if card.value == value:
                                play_card(settings, screen, player, pile, card)
                                break

                else:
                    #if has a trick, needs a trick, but not valid, play lowest card
                    value = determine_lowest_value(player, trick_card)
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
            value = determine_lowest_value(player, trick_card)
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
                    #needs trick and has one in valid hand, play highest if it beats current winner

                    winning_card = pile.current_winning_card(trick_card)
                    if can_beat(player, needs_trick, has_trick, trick_valid, winning_card, trick_card):
                        #if the trick will beat current winning card, then play it
                        value = determine_highest_trickvalue(player, trick_card)
                        for card in reversed(player.hand.sprites()): #reversed order to make sure it's a trick
                            if card.value == value:
                                play_card(settings, screen, player, pile, card)
                                break
                    else:
                        #can't beat current leader, so play lowest nontrick (if they have others) to save trick card
                        value = determine_lowest_value(player, trick_card)
                        for card in player.hand:
                            if card.value == value:
                                play_card(settings, screen, player, pile, card)
                                break

                else:
                    #needs a trick and has one, but not valid, so play lowest
                    value = determine_lowest_value(player, trick_card)
                    for card in player.hand:
                        if card.value == value:
                            play_card(settings, screen, player, pile, card)
                            break

            else:
                #needs a trick but doesn't have one, play highest hoping to take
                winning_card = pile.current_winning_card(trick_card)
                if can_beat(player, needs_trick, has_trick, trick_valid, winning_card, trick_card):
                    value = determine_highest_nontrickvalue(player, trick_card)
                else:
                    value = determine_lowest_value(player, trick_card)
                for card in player.hand:
                    if card.value == value:
                        play_card(settings, screen, player, pile, card)
                        break

        else:
            #doesn't have a trick and doesn't need one, play lowest card
            value = determine_lowest_value(player, trick_card)
            for card in player.hand:
                if card.value == value:
                    play_card(settings, screen, player, pile, card)
                    break

####################PLAY DETERMINATION TREE#####################################

    set_card_validity(player)

def determine_play_hard(settings, screen, pile, player, trick_card):
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
                    #if has a trick in valid hand and needs trick, only play if player has only tricks

                    if only_tricks_valid(player, trick_card):
                        value = determine_highest_trickvalue(player, trick_card)
                        for card in reversed(player.hand.sprites()): #reverse sort to find the highest value (making sure a trick)
                            if card.value == value:
                                play_card(settings, screen, player, pile, card)
                                break
                    else:
                        value = determine_lowest_value(player, trick_card)
                        for card in player.hand:
                            if card.value == value:
                                play_card(settings, screen, player, pile, card)
                                break

                else:
                    #if has a trick, needs a trick, but not valid, play lowest card
                    value = determine_lowest_value(player, trick_card)
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
            value = determine_lowest_value(player, trick_card)
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
                    #needs trick and has one in valid hand, play highest if it beats current winner

                    winning_card = pile.current_winning_card(trick_card)
                    if can_beat(player, needs_trick, has_trick, trick_valid, winning_card, trick_card):
                        #if the trick will beat current winning card, then play it
                        value = determine_highest_trickvalue(player, trick_card)
                        for card in reversed(player.hand.sprites()): #reversed order to make sure it's a trick
                            if card.value == value:
                                play_card(settings, screen, player, pile, card)
                                break
                    else:
                        #can't beat current leader, so play lowest nontrick (if they have others) to save trick card
                        value = determine_lowest_value(player, trick_card)
                        for card in player.hand:
                            if card.value == value:
                                play_card(settings, screen, player, pile, card)
                                break

                else:
                    #needs a trick and has one, but not valid, so play lowest
                    value = determine_lowest_value(player, trick_card)
                    for card in player.hand:
                        if card.value == value:
                            play_card(settings, screen, player, pile, card)
                            break

            else:
                #needs a trick but doesn't have one, play highest hoping to take
                winning_card = pile.current_winning_card(trick_card)
                if can_beat(player, needs_trick, has_trick, trick_valid, winning_card, trick_card):
                    value = determine_highest_nontrickvalue(player, trick_card)
                else:
                    value = determine_lowest_value(player, trick_card)
                for card in player.hand:
                    if card.value == value:
                        play_card(settings, screen, player, pile, card)
                        break

        else:
            #doesn't have a trick and doesn't need one, play lowest card
            value = determine_lowest_value(player, trick_card)
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

def can_beat(player, needs_trick, has_trick, trick_valid, winning_card, trick_card):
    """Determines if player can beat current leading card"""

    if winning_card.suit == trick_card.suit:
        #current winner is a trick card
        for card in player.hand:
            if card.suit == trick_card.suit and card.value > winning_card.value and card.valid:
                return True #can beat the current leader

        return False #can't beat current leader

    else:
        #current winner not a trick
        if needs_trick and has_trick and trick_valid:
            return True #can trump in, so do so
        else:
            #can't play a trick, determine if they can beat first suit
            for card in player.hand:
                if card.suit == trick_card.suit and card.value > winning_card.value and card.valid:
                    return True #can beat the nontrick highest

            return False #can't beat nontrick current leader

def determine_lowest_value(player, trick_card):
    """Determines lowest value in the player's valid hand"""
    has_only_tricks = True
    low_value = 15 #highest possible value

    for card in player.hand:
        if card.valid and card.suit != trick_card.suit:
            has_only_tricks = False
            break

    if has_only_tricks:
        #if they have only tricks, forced to play lowest value
        for card in player.hand:
            if (card.value < low_value) and (card.valid):
                low_value = card.value
    else:
        #player may have a trick, but we want the lowest non-trick value
        for card in player.hand:
            if (card.value < low_value) and (card.valid) and (card.suit != trick_card.suit):
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

def only_tricks_valid(player, trick_card):
    """Determines if a player only has trick cards that are valid"""

    has_only_tricks = True

    for card in player.hand:
        if card.valid and card.suit != trick_card.suit:
            has_only_tricks = False
            break

    return has_only_tricks
