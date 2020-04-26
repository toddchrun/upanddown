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

    max_index = len(curr_deck)  #total cards

    #Deal out cards (number based on current round) to each player
    while curr_round > 0:
        for i in range(0, len(active_players)):
            index = randint(0, max_index)
            dealt_card = curr_deck[index]
            active_players[i]['hand'].append(dealt_card)
            curr_deck.pop(index)
            max_index -= 1
        curr_round -= 1

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
        display_hand(player)

        bid = int(input("\n" + player['name'] + " please bid: "))

        #make sure input isn't greater than max -THIS NEEDS MAJOR UPDATES: Need to try/except this
        if (bid > max_bid):
            print("You can only bid the maximum idiot, your bid remains but you will fail")

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

        #initialize empty array to capture all played cards
        round_hand = []

        #reset for each round, object to capture just the first card determining play
        first_play = {}

        #boolean logic to check and see if tricks are broken, can only lead trick when broken
        trick_broken = False

        #Prompts player to play after showing hand
        for player in active_players:

            #For each turn checks to see if a player has only tricks, if so, they can lead with a trick
            only_tricks = False
            only_tricks = check_for_only_tricks(player, trick_suit)

            display_hand(player)

            play_card(player, round_hand, trick_broken, only_tricks, trick_suit)

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

    #Need to re-sort list based on winner
    while active_players[0]['name'] != leader:
        active_players.append(active_players.pop(0))


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

def display_hand(player):
    """
    Just loops through hand to display, eventually not needed or needs major overhaul
    """

    print("\n" + player['name'] + " it's your turn.  Your hand: ")
    for card in player['hand']:
        print(card['display'])

def check_for_only_tricks(player, trick_suit):
    """
    Called prior to every play, if the player only has tricks, they can play one to start
    """

    for hand in player['hand']:
        if (trick_suit == hand['suit']):
            only_tricks = True
        else:
            only_tricks = False
            break
    return only_tricks

def play_card(player, round_hand, trick_broken, only_tricks, trick_suit):
    """
    Functionality for prompting a play from each player.  Includes validating
    each play based on what was played first, if tricks were broken, etc.
    """

    valid_play = False

    #if first play of the round, all is valid unless
    if len(round_hand) == 0:
        while valid_play == False: #this will loop until we get a valid card play

            play = input("\n" + player['name'] + " what card will you play (enter same display)?: ")
            valid_play = validate_first_play(play, player, round_hand, trick_broken, only_tricks, trick_suit, valid_play)

    #else block will cover all the other plays during the round, first play suit will dictate
    else:
        while valid_play == False: #this will loop until we get a valid card play

            play = input("\n" + player['name'] + " what card will you play (enter same display)?: ")
            valid_play = validate_play(play, player, round_hand, trick_broken, only_tricks, trick_suit, valid_play)


def validate_first_play(play, player, round_hand, trick_broken, only_tricks, trick_suit, valid_play):
    """
    Validates the first play of each hand.  Also appends the valid play to the round_hand
    and makes sure to remove the card from the player's hand
    """

    idx = 0
    while idx < len(player['hand']):
        if player['hand'][idx]['display'] == play:
            if (only_tricks == True) or (trick_broken == True):
                trick_broken = True
                valid_play = True
                round_hand.append([player['name'], player['hand'][idx]['value'], player['hand'][idx]['suit']])
                player['hand'].pop(idx)
                break
            elif player['hand'][idx]['suit'] != trick_suit:
                valid_play = True
                round_hand.append([player['name'], player['hand'][idx]['value'], player['hand'][idx]['suit']])
                player['hand'].pop(idx)
                break
        idx += 1
    return valid_play

def validate_play(play, player, round_hand, trick_broken, only_tricks, trick_suit, valid_play):
    """
    Validates each subsequent play in the round, first play will dictate what can be played
    """

    #if player has the first suit played, they can only play that suit
    has_suit = False

    #cycles through player hand to see if they have first play suit
    for card in player['hand']:
        if card['suit'] == round_hand[0][2]:
            has_suit = True
            break

    #prompt loop to grab player hand, only can play when valid
    idx = 0
    while idx < len(player['hand']):
        if player['hand'][idx]['display'] == play:
            if has_suit == False:
                if player['hand'][idx]['suit'] == trick_suit:
                    trick_played = True
                valid_play = True
                round_hand.append([player['name'], player['hand'][idx]['value'], player['hand'][idx]['suit']])
                player['hand'].pop(idx)
                break
            elif player['hand'][idx]['suit'] == round_hand[0][2]:
                valid_play = True
                round_hand.append([player['name'], player['hand'][idx]['value'], player['hand'][idx]['suit']])
                player['hand'].pop(idx)
                break
        idx += 1

    return valid_play
