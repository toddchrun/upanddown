"""
Game functions for Up and Down the River
"""

import sys
import pygame
from pygame.sprite import Group
from random import randint
from card import Card
from player import Player
import screen_functions as sf


def deal_round(curr_deck, curr_round, active_players):
    """
    Deals cards to every player, total cards equals the current round.  Cards
    are dealt to the left of the dealer and continually removed from the Deck
    object
    """

    counter = curr_round

    #Deal out cards (number based on current round) to each player
    while counter > 0:
        for i in range(0, len(active_players)):
            idx = randint(0, len(curr_deck)-1)
            active_players[i].hand.add(curr_deck[idx])
            curr_deck.pop(idx)
        counter -= 1

def get_trick(curr_deck):
    """Returns random card from remaining deck to be the trick"""

    return curr_deck[randint(0, len(curr_deck)-1)]

def bid_round(settings, screen, table, curr_round, active_players, pile, trick_card, message):
    """
    Cycles through each player to determine number of cards they wish to bid for
    the current round.
    """
    #Sets order of bidding, dealer is last
    active_players.append(active_players.pop(0))

    #main loop to continue through until all bids have been validated
    for player in active_players:
        player.turn_active = True
        message.update_message(player.name + ", it's your bid!", .15) #150 millisecond delay

        while player.turn_active:
            sf.update_screen(settings, screen, table, active_players, pile, trick_card, message)
            sf.check_bids(settings, screen, table, player, pile, curr_round, message)


def play_round(settings, screen, table, curr_round, active_players, pile, trick_card, message):
    """Plays the round based on current number of cards and trick."""

    count = 0
    while count < curr_round:

        #check to see if any player has the joker, if so, set suit to be trick_suit
        check_joker(active_players, trick_card.suit)

        #Prompts player to play after showing hand
        for player in active_players:
            player.turn_active = True
            message.update_message(player.name + ", it's your turn!", 0)

            #For each turn checks to see if a player has only tricks, if so, they can lead with a trick
            check_for_only_tricks(player, trick_card.suit)

            while player.turn_active:
                sf.update_screen(settings, screen, table, active_players, pile, trick_card, message)
                sf.check_play(settings, screen, table, player, pile, trick_card, curr_round)

        #After a given hand, check to see if the trick was broken.  If so, the next hand can be led with trick
        check_for_trick_broken(pile, trick_card)

        count += 1

        #Passes the whole turn into trick determining function
        trick_winner(pile, active_players, trick_card)

        #Clears out the discard pile
        clear_discards(pile)

    score_round(active_players)
    clear_bids_tricks(active_players)
    trick_card.trick_broken = False
    set_dealer(active_players)

def trick_winner(pile, active_players, trick_card):
    """Determines trick winner by passing all played hands and trick suit"""

    #Need a false bool for each hand, even if trick broken, one may have not been played
    trick_played = False
    max_value = 0

    #Establishes sprite list
    round_hand = pile.discards.sprites()

    #Goes through all cards to determine if a trick was played
    for card in pile.discards:
        if (card.suit == trick_card.suit):
            trick_played = True
            trick_suit = trick_card.suit

    #If no trick is played, set trick suit to the first card played
    if not trick_played:
        trick_suit = round_hand[0].suit

    #Max value set for player playing highest value of trick suit
    for card in round_hand:
        if (card.suit == trick_suit):
            if (card.value > max_value):
                max_value = card.value
                winning_card = card  #only one winning card, played id will determine winner

    #Increments number of tricks won for round winner
    for player in active_players:
        if player.id == winning_card.played_id:
            player.curr_round_tricks += 1

    #Need to re-sort list based on winner
    while active_players[0].id != winning_card.played_id:
        active_players.append(active_players.pop(0))

def clear_discards(pile):
    """Clears out the discard pile, resets each cards played id as well"""

    for card in pile.discards:
        card.played_id = int()
        pile.discards.remove(card)

def score_round(active_players):
    """
    Simple determination of scores based on tricks taken and bid
    """

    for player in active_players:
        if player.bid == player.curr_round_tricks:
            player.score += (10 + player.bid)

def clear_bids_tricks(active_players):
    """
    Clears bids and tricks taken items in each player before a new hand commences
    """

    for player in active_players:
        player.bid = 0
        player.curr_round_tricks = 0
        player.has_only_tricks = False

def set_dealer(active_players):
    """Called at the end of each hand, resorts the list so the next player is assigned dealer.
    This player will subsequently be popped to the end during bidding round
    """

    #will cycle through until original dealer is in position 0
    while active_players[0].dealer != True:
        active_players.append(active_players.pop(0))

    #sets original dealer to False and pops to the end of array
    active_players[0].dealer = False
    active_players.append(active_players.pop(0))

    #next player in line set to dealer
    active_players[0].dealer = True

def check_joker(active_players, trick_suit):
    """
    Checked to begin each hand, if a player has the joker, set it's suit to trick suit
    """

    for player in active_players:
        for card in player.hand:
            if card.display == "JK":
                card.suit = trick_suit

def check_for_only_tricks(player, trick_suit):
    """
    Called prior to every play, if the player only has tricks, they can play one to start
    """

    for card in player.hand:
        if (trick_suit == card.suit):
            player.has_only_tricks = True
        else:
            player.has_only_tricks = False
            break #kill loop early, if one card is not trick, no need to check others

def check_for_trick_broken(pile, trick_card):
    """
    Called prior to every play, if the player only has tricks, they can play one to start
    """

    for hand in pile.discards:
        if (hand.suit == trick_card.suit):
            trick_card.trick_broken = True
            break
