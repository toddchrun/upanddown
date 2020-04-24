"""
Game functions for Up and Down the River
"""

import sys
import pygame
from random import randint

def deal_round(curr_deck, curr_round, active_players):
    """
    Deals cards to every player, total cards equals the current round.  Cards
    are dealt to the left of the dealer and continually removed from the Deck
    object
    """

    max_index = len(curr_deck) #total cards

    #Deal out cards (number based on current round) to each player
    while curr_round > 0:
        for i in range(0, len(active_players)):
            index = randint(0, max_index)
            dealt_card = curr_deck[index]
            active_players[i]['hand'].append(dealt_card)
            curr_deck.pop(index)
            max_index = max_index - 1
        curr_round = curr_round - 1

def get_trick(curr_deck):
    """
    Once all the players have been dealt out for the round, deals final "trick"
    card whose suit determines trumping suit for the round
    """

    trick_index = randint(0, len(curr_deck))
    trick_card = curr_deck[trick_index]
    return trick_card

def bid_round(curr_round, active_players, trick_card):
    """
    Cycles through each player to determine number of cards they wish to bid for
    the current round.

    THINGS TO ADD: VALIDATION TO NUMBER BID
    """

    max_bid = curr_round

    print("Round " + str(curr_round))
    print("Trick Card is " + trick_card['display'])

    #Sets order of bidding, dealer is last
    dealer = active_players.pop(0)
    active_players.append(dealer)

    #Bidding round
    for player in active_players:
        print("\n" + player['name'] + " it's your turn.  Your hand: ")
        for card in player['hand']:
            print(card['display'])
        bid = int(input("\n" + player['name'] + " please bid: "))

        #make sure input isn't greater than max -THIS NEEDS MAJOR UPDATES: Need to try/except this
        if (bid > max_bid):
            print("You can only bid the maximum idiot")

        player['bid'] = bid

def play_round(curr_round, active_players, trick_suit):
    """
    Plays the round based on current number of cards and trick.

    Needs a ton of updates:
    1. Add validations to what people can play (guided by first card, trick broken, etc.)
    2. Capture what people can cannot play
    3. Think of better way to structure round_hand, passing it to trick winner works but is ugly
    """

    count = 0
    while count < curr_round:
        round_hand = []

        #Prompts player to play after showing hand
        for player in active_players:
            print("\n" + player['name'] + " it's your turn.  Your hand: ")
            for card in player['hand']:
                print(card['display'])
            play = input("\n" + player['name'] + " what card will you play?: ")

            #Captures player hand and validates
            idx = 0
            while idx < len(player['hand']):
                if player['hand'][idx]['display'] == play:
                    round_hand.append([player['name'], player['hand'][idx]['value'], player['hand'][idx]['suit']])
                    player['hand'].pop(idx)
                idx += 1
        count += 1

        #Passes the whole turn into trick determining function
        trick_winner(round_hand, active_players, trick_suit)

    score_round(active_players)
    clear_bids_tricks(active_players)

def trick_winner(round_hand, active_players, trick_suit):
    """
    Determines trick winner by passing all played hands and trick suit
    """

    trick_played = False
    max_value = 0

    #Goes through all cards to determine if a trick was played
    for i in round_hand:
        if (i[2] == trick_suit):
            trick_played = True

    #If no trick is played, set trick suit to the first card played
    if not trick_played:
        trick_suit = round_hand[0][2]

    #Max value set for player playing highest value of trick suit
    for i in round_hand:
        if (i[2] == trick_suit):
            if (i[1] > max_value):
                max_value = i[1]
                leader = i[0]

    #Increments number of tricks won for round winner
    for player in active_players:
        if player['name'] == leader:
            player['curr_round_tricks'] += 1
            print(player['name'] + " wins the hand!")

def score_round(active_players):
    """
    Simple determination of scores based on tricks taken and bid
    """
    for player in active_players:
        if player['bid'] == player['curr_round_tricks']:
            player['score'] += (10 + player['bid'])
    print(active_players)

def clear_bids_tricks(active_players):
    """
    Clears bids and tricks taken items in each player before a new hand commences
    """
    for player in active_players:
        if player['bid'] == player['curr_round_tricks']:
            player['bid'] = 0
            player['curr_round_tricks'] = 0

    print(active_players)
