"""
Game functions for Up and Down the River - coordinates gameplay events
"""
import sys
import pygame
import time
from pygame.sprite import Group
from random import randint
from card import Card
from player import Player
import screen_functions as sf
import computer_functions as cf


def deal_round(settings, screen, table, active_players, pile, message, deck, curr_deck, curr_round):
    """
    Deals cards to every player, total cards equals the current round.
    Cards are dealt to the left of the dealer and continually removed from the Deck
    object
    """

    deck.dealt = False #Boolean to activate deal function

    while not deck.dealt:
        message.update_message("Click the deck to deal!", 0)
        sf.update_screen(settings, screen, table, active_players, pile, None, message, deck)
        sf.check_for_deal(settings, screen, deck)

    #Deal out cards (number based on current round) to each player
    counter = curr_round
    while counter > 0:
        for i in range(0, len(active_players)):
            idx = randint(0, len(curr_deck)-1)
            active_players[i].hand.add(curr_deck[idx])
            curr_deck.pop(idx)
        counter -= 1

def get_trick(curr_deck):
    """Returns random card from remaining deck to be the trick"""

    return curr_deck[randint(0, len(curr_deck)-1)]

def bid_round(settings, screen, table, curr_round, active_players, pile, trick_card, message, deck):
    """
    Cycles through each player to determine number of cards they wish to bid for the current round.
    """

    #check to see if any player has the joker, if so, set suit to be trick_suit
    check_joker(active_players, trick_card.suit)

    #Show user controlled player's hand
    sf.show_user_cards(active_players)

    #Show the trick card
    trick_card.flip_card()

    #Sets order of bidding, dealer is last
    active_players.append(active_players.pop(0))

    #main loop to continue through until all bids have been validated
    for player in active_players:

        #sets player's turn status to active
        player.turn_active = True
        message.update_message(player.name + ", it's your bid!", 0)

        if not player.user_control:
            while player.turn_active:
                #for any computer controlled player, gets their bid, pauses for turn
                sf.update_screen(settings, screen, table, active_players, pile, trick_card, message, deck)
                cf.bid(settings, player, trick_card, active_players, curr_round)
                sf.player_pause(settings, screen, player)
        else:
            while player.turn_active:
                #prompt for user controlled player to bid
                sf.update_screen(settings, screen, table, active_players, pile, trick_card, message, deck)
                sf.check_bids(settings, screen, table, player, pile, curr_round, message)

def play_round(settings, screen, table, curr_round, active_players, pile, trick_card, message, deck):
    """Plays the round based on current number of cards and trick."""

    #will loop until each player has played all cards
    count = 0
    while count < curr_round:

        #Prompts player to play after showing hand
        for player in active_players:
            player.turn_active = True
            message.update_message(player.name + ", it's your turn!", 0)

            #For each turn checks to see if a player has only tricks, if so, they can lead with a trick
            check_for_only_tricks(player, trick_card.suit)

            if not player.user_control:
                while player.turn_active:
                    #Loop for computer controlled players
                    sf.update_screen(settings, screen, table, active_players, pile, trick_card, message, deck)
                    cf.play(settings, screen, player, trick_card, pile, curr_round, active_players)
                    sf.player_pause(settings, screen, player)
            else:
                while player.turn_active:
                    #prompt for user controlled play
                    sf.update_screen(settings, screen, table, active_players, pile, trick_card, message, deck)
                    sf.check_play(settings, screen, table, player, pile, trick_card, curr_round, message)

            #Resets any card that may have been selected
            for card in player.hand:
                if card.selected:
                    card.deselect_card()

        #After a given hand, check to see if the trick was broken.  If so, the next hand can be led with trick
        check_for_trick_broken(pile, trick_card)

        count += 1

        #Passes the whole turn into trick determining function
        trick_winner(settings, screen, table, active_players, pile, trick_card, message, deck)

        #Clears out the discard pile
        clear_discards(pile)

    #tally up points, reset bids/tricks/order
    score_round(active_players)
    clear_bids_tricks(active_players)
    trick_card.trick_broken = False
    set_dealer(active_players)

def trick_winner(settings, screen, table, active_players, pile, trick_card, message, deck):
    """Determines trick winner by passing all played hands and trick suit"""

    #Need a false bool for each hand, even if trick broken, one may have not been played
    trick_played = False

    max_value = 0

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
            player.turn_active = True
            player.curr_round_tricks += 1
            message.update_message(player.name + " wins the hand!", 0)

            #Pauses the screen to show hand winner and scores
            while player.turn_active:
                sf.update_screen(settings, screen, table, active_players, pile, trick_card, message, deck)
                sf.player_pause(settings, screen, player)


    #Need to re-sort list based on winner, winner starts the next hand
    while active_players[0].id != winning_card.played_id:
        active_players.append(active_players.pop(0))

def clear_discards(pile):
    """Clears out the discard pile, resets each cards played_id as well"""

    for card in pile.discards:
        card.played_id = int()
        pile.discards.remove(card)

def score_round(active_players):
    """
    Simple determination of scores based on tricks taken and bid
    """

    #10 points for making total bid, plus bonus point for each bid
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
