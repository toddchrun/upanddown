"""
Screen functions for Up and Down the River
"""

import sys
import pygame
from table import Table
from discard_pile import Pile
from pygame.sprite import Group

#Make this a general check events?  Need a separate one to test each player's turn
def check_play(settings, screen, table, player, pile, trick_card, curr_round):
    """Responses to mouse actions"""

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN :
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_card_clicked(settings, screen, player, pile, trick_card, mouse_x, mouse_y)

def check_bids(settings, screen, table, player, pile, curr_round):
    """Waits for valid bid"""

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            sys.exit()
        elif event.type == pygame.KEYDOWN :
            check_keydown_events(settings, screen, event, player, curr_round)

def update_screen(settings, screen, table, active_players, pile, trick_card) :
    """Updates the images on the screen"""

    #Basic display drawing/fill
    screen.fill(settings.bg_color)
    table.blitme()

    #Display all hands
    for player in active_players:
        display_cards(screen, player)
        player.show_player(player.score, player.bid, player.curr_round_tricks, player.turn_active)

    #Display Trick Card
    trick_card.blitme()

    #Display discard pile
    pile.discards.draw(screen)

    pygame.display.flip()

def set_player_position(settings, screen, active_players):
    """Sets player position display based on number of players"""

    screen_rect = screen.get_rect()

    #Positions relative to screen
    pos1 = [screen_rect.width*.20, screen_rect.height*.13, screen_rect.width*.29]
    pos2 = [screen_rect.width*.41, screen_rect.height*.13, screen_rect.width*.50]
    pos3 = [screen_rect.width*.62, screen_rect.height*.13, screen_rect.width*.71]
    pos4 = [screen_rect.width*.82, screen_rect.height*.415, screen_rect.width*.91]
    pos5 = [screen_rect.width*.62, screen_rect.height*.70, screen_rect.width*.71]
    pos6 = [screen_rect.width*.41, screen_rect.height*.70, screen_rect.width*.50]
    pos7 = [screen_rect.width*.20, screen_rect.height*.70, screen_rect.width*.29]
    pos8 = [0, screen_rect.height*.415, screen_rect.width*.09]

    #Array of positional configuration based on total number of players
    player_positions = [
        {'total': 3, 'positions': [pos2,pos5,pos7]},
        {'total': 4, 'positions': [pos1,pos3,pos5,pos7]},
        {'total': 5, 'positions': [pos1,pos2,pos3,pos5,pos7]},
        {'total': 6, 'positions': [pos1,pos2,pos3,pos5,pos6,pos7]},
        {'total': 7, 'positions': [pos1,pos2,pos3,pos4,pos5,pos7,pos8]},
        {'total': 8, 'positions': [pos1,pos2,pos3,pos4,pos5,pos6,pos7,pos8]}
    ]

    #Set the position index array
    for positions in player_positions:
        if positions['total'] == settings.number_of_players:
            position_index = positions['positions']
            break

    #Assign screen position for each player
    for index in range(0, len(active_players)):
        active_players[index].x_start = position_index[index][0]
        active_players[index].y_start = position_index[index][1]
        active_players[index].x_center = position_index[index][2]

    for player in active_players:
        player.set_top_text(player.score, player.turn_active)
        player.set_bottom_text(player.bid, player.curr_round_tricks, player.turn_active)


def set_card_pos(settings, screen, active_players):
    """Centers the player's hand based on total number of cards and card image dimensions"""

    for player in active_players:
        hand_length = len(player.hand)
        x_pos = player.x_center - ((.0525 + ((hand_length - 1) * .014)) / 2 * settings.screen_width)
        y_pos = player.y_start
        x_incr = .014 * settings.screen_width
        for card in player.hand:
            card.update_card_position(x_pos, y_pos)
            x_pos += x_incr

def display_cards(screen, player):
    """Centers the player's hand based on total number of cards and card image dimensions"""

    player.hand.draw(screen)


def sort_cards(active_players, trick_card):
    """Sorts each player's hand based on the card object's sort_index"""

    #First sorts based on regular index Spades -> Clubs -> Diamonds -> Hearts
    for player in active_players:
        unsorted_sprites = player.hand.sprites()
        player.hand.empty()
        player.hand.add(sorted(unsorted_sprites, key=lambda card: card.sort_index))

    #Next auto sorts to put trick cards at the end
    for player in active_players:
        tricks = []
        for card in player.hand:
            if card.suit == trick_card.suit:
                tricks.append(card)
                player.hand.remove(card)
        for trick in tricks:
            player.hand.add(trick)


def check_card_clicked(settings, screen, player, pile, trick_card, mouse_x, mouse_y):

    for card in reversed(player.hand.sprites()):
        if (card.rect.collidepoint(mouse_x, mouse_y) and card.selected):
            valid_play = False

            if len(pile.discards) == 0:
                valid_play = validate_first_play(player, card, trick_card)
            else:
                valid_play = validate_play(player, card, pile)

            if valid_play: #if this is valid, card will be officially played
                card.played_id = player.id
                add_to_discard_pile(settings, screen, pile, card)
                player.hand.remove(card)
                player.turn_active = False
                break
            else:
                card.deselect_card()
                break
        elif card.rect.collidepoint(mouse_x, mouse_y):
            card.select_card()
            break

def add_to_discard_pile(settings, screen, pile, card):
    """Adds played card to discard pile"""

    x_pos = pile.x + (len(pile.discards) * settings.screen_width * .014)
    y_pos = pile.y
    card.update_card_position(x_pos, y_pos)
    pile.discards.add(card)

def check_keydown_events(settings, screen, event, player, curr_round):
    """Checks for key presses for bidding round"""

    bid = event.key - 48 #48 is key for 0

    if (bid >= 0) and (bid <= curr_round):
        player.bid = bid
        player.turn_active = False

def validate_first_play(player, card, trick_card):
    """
    Validates the first play of each hand.
    """
    valid_play = False

    if player.has_only_tricks:
        valid_play = True
    elif trick_card.trick_broken:
        valid_play = True
    elif card.suit != trick_card.suit:
        valid_play = True

    return valid_play

def validate_play(player, card, pile):
    """
    Validates each subsequent play in the round, first play will dictate what can be played
    """
    valid_play = False

    #if player has the first suit played, they can only play that suit
    has_suit = False

    #gets the suit of the first card played, which dictates play for the round
    round_hand = pile.discards.sprites()
    starting_suit = round_hand[0].suit

    #cycles through player hand to see if they have first play suit
    for i in player.hand:
        if i.suit == starting_suit:
            has_suit = True
            break

    #validate play based on having first suit played or not
    if has_suit == False:
        valid_play = True
    elif card.suit == starting_suit:
        valid_play = True

    return valid_play