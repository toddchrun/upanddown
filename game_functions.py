"""
Game functions for Up and Down the River
"""
import sys
import pygame
from random import randint

#Deal round based on current deck, round and overall number of players
def deal_round(curr_deck, curr_round, active_players):

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

    # #Deal out trick_card for last step
    # trick_index = randint(0, max_index)
    # trick_card = curr_deck[trick_index]

def get_trick(curr_deck):
    #Deal out trick_card for last step
    trick_index = randint(0, len(curr_deck))
    trick_card = curr_deck[trick_index]
    return trick_card

def bid_round(curr_round, active_players, trick_card):
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

        #make sure input isn't greater than max -THIS NEEDS MAJOR UPDATES: Need to try except this
        if (bid > max_bid):
            print("You can only bid the maximum idiot")

        player['bid'] = bid

    return

def play_round(curr_round, active_players, trick_suit):
        count = 0
        while count < curr_round:
            round_hand = []
            for player in active_players:
                print("\n" + player['name'] + " it's your turn.  Your hand: ")
                for card in player['hand']:
                    print(card['display'])
                play = input("\n" + player['name'] + " what card will you play?: ")
                for card in player['hand']:
                    if card['display'] == play:
                        round_hand.append({player['name']: card})
            count += 1
        print(round_hand)
#         round_score(round_hand, active_players, trick_suit)
#
# def round_score(round_hand, active_players, trick_suit):
#     for i in round_hand:
