"""
Screen functions for Up and Down the River
"""

import sys
import pygame
import time
import math
from player import Player
from table import Table
from discard_pile import Pile
from pygame.sprite import Group

#Make this a general check events?  Need a separate one to test each player's turn

def check_for_exit():
    """Loops until deck is clicked and cards can be dealt"""

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            sys.exit()

def check_for_prompts(settings, screen, prompt_screen, active_players):
    """Loops until deck is clicked and cards can be dealt"""

    events = pygame.event.get()
    for event in events :
        if event.type == pygame.QUIT :
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN :
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_prompts_clicked(settings, screen, prompt_screen, mouse_x, mouse_y) #check for prompt button clicks
            check_play_button(settings, screen, prompt_screen, active_players, mouse_x, mouse_y) #check to see if play button clicked)

    #feeds text input box events for constant refresh
    prompt_screen.update_text(events)

def player_pause(settings, screen, player):
    """Loops until deck is clicked and cards can be dealt"""

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            sys.exit()

    pygame.time.delay(1500) #current pause set at 1.5 seconds, pause between computer plays
    player.turn_active = False

def check_for_deal(settings, screen, deck):
    """Loops until deck is clicked and cards can be dealt"""

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN :
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_deck_click(deck, mouse_x, mouse_y)

def check_play(settings, screen, table, player, pile, trick_card, curr_round, message):
    """Responses to mouse actions"""

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN :
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_card_clicked(settings, screen, player, pile, trick_card, message, mouse_x, mouse_y)

def check_bids(settings, screen, table, player, pile, curr_round, message):
    """Waits for valid bid"""

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            sys.exit()
        elif event.type == pygame.KEYDOWN :
            check_keydown_events(settings, screen, event, player, curr_round, message)

def update_screen(settings, screen, table, active_players, pile, trick_card, message, deck) :
    """Updates the images on the screen"""

    #Basic display drawing/fill
    screen.fill(settings.bg_color)
    table.blitme()
    deck.show_deck()

    #Display all hands
    for player in active_players:
        display_cards(screen, player)
        player.show_player(player.score, player.bid, player.curr_round_tricks, player.turn_active)

    #Display Trick Card if deck is dealt
    if deck.dealt:
        trick_card.blitme()

    #Display current action
    message.show_message()

    #Display discard pile
    pile.discards.draw(screen)

    pygame.display.flip()

def prompt_screen(settings, screen, prompt_screen) :
    """Updates the prompt images on the screen"""

    #Basic display drawing/fill
    screen.fill(settings.bg_color)
    prompt_screen.show_prompt_screen()

    pygame.display.update()

def clear_screen(settings, screen, table, active_players, message) :
    """Updates the images on the screen"""

    #Basic display drawing/fill
    screen.fill(settings.bg_color)
    table.blitme()

    #Display all hands
    for player in active_players:
        player.show_player(player.score, player.bid, player.curr_round_tricks, player.turn_active)

    #Display current action
    message.show_message()

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

def show_user_cards(active_players):
    """Passes all players, shows cards for any player controlled by user"""

    for player in active_players:
        if player.user_control:
            for card in player.hand:
                card.flip_card()

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


def check_card_clicked(settings, screen, player, pile, trick_card, message, mouse_x, mouse_y):

    for card in reversed(player.hand.sprites()):
        if (card.rect.collidepoint(mouse_x, mouse_y) and card.selected):
            valid_play = False

            if len(pile.discards) == 0:
                valid_play = validate_first_play(player, card, trick_card, message)
            else:
                valid_play = validate_play(player, card, pile, message)

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

def check_prompts_clicked(settings, screen, prompt_screen, mouse_x, mouse_y):
    """Checks collidepoint of all the prompt buttons, updates if needed"""

    #check the level prompts
    for level in prompt_screen.levels:
        if level.rect.collidepoint(mouse_x, mouse_y):
            level.select()
            for other in prompt_screen.levels: #deslect all others
                if (other != level):
                    other.deselect()

    #check the player number prompts
    for number in prompt_screen.players:
        if number.rect.collidepoint(mouse_x, mouse_y):
            number.select()
            for other in prompt_screen.players: #deslect all others
                if (other != number):
                    other.deselect()
            #hides number of round options if there aren't enough cards!
            for round in prompt_screen.rounds:
                if (int(round.msg) * int(number.msg) > 53):
                    if round.active:
                        #if the round you are hiding was active, reset to the first option to be active
                        round.active = False
                        number_of_rounds_auto_update(prompt_screen, int(number.msg))
                    round.hide()
                elif round.hidden:
                    round.unhide()

    #check the rounds prompts
    for round in prompt_screen.rounds:
        if round.rect.collidepoint(mouse_x, mouse_y):
            round.select()
            for other in prompt_screen.rounds: #deslect all others
                if (other != round):
                    other.deselect()

def number_of_rounds_auto_update(prompt_screen, num_players):
    """Called upon when previous active selection is hidden, targets highest next available selection"""

    target_level = math.trunc(53 / num_players)
    for round in prompt_screen.rounds:
        if int(round.msg) == target_level:
            round.select()

def check_play_button(settings, screen, prompt_screen, active_players, mouse_x, mouse_y):
    """Checks collidepoint of all the prompt buttons, updates if needed"""

    if prompt_screen.play_button.rect.collidepoint(mouse_x, mouse_y): #play time!

        #set game difficulty
        for level in prompt_screen.levels:
            if level.active:
                settings.game_difficulty = level.msg

        #set number of players
        for number in prompt_screen.players:
            if number.active:
                settings.number_of_players = int(number.msg)

        #set number of rounds
        for round in prompt_screen.rounds:
            if round.active:
                settings.max_rounds = int(round.msg)

        #set player name
        user_name = prompt_screen.text_input.get_text()
        active_players.append(Player(settings, screen, 0, user_name, None)) #sets first player instance as the user

        #set computer players (should clean this up)
        i = 1
        while i < settings.number_of_players:
            new_player_name = "Player " + str(i+1)
            player_id = i
            active_players.append(Player(settings, screen, player_id, new_player_name, settings.game_difficulty))
            i += 1

        #Set dealer and user player as the first player
        active_players[0].dealer = True
        active_players[0].user_control = True

        #finally, set game active to true
        prompt_screen.play_button.game_active = True

def check_deck_click(deck, mouse_x, mouse_y):
    """If deck image clicked, deal the round"""

    #If the deck image is clicked, set dealt status to True to begin dealing
    if (deck.rect.collidepoint(mouse_x, mouse_y)):
        deck.dealt = True

def add_to_discard_pile(settings, screen, pile, card):
    """Adds played card to discard pile"""

    #if face down, flip the card
    if not card.face_up:
        card.flip_card()

    x_pos = pile.x + (len(pile.discards) * settings.screen_width * .014)
    y_pos = pile.y
    card.update_card_position(x_pos, y_pos)
    pile.discards.add(card)

def check_keydown_events(settings, screen, event, player, curr_round, message):
    """Checks for key presses for bidding round"""

    bid = event.key - 48 #48 is key for 0

    if (bid >= 0) and (bid <= curr_round):
        player.bid = bid
        player.turn_active = False
    else:
        message.update_message("Incorrect bid! Your bid must be between 0 and " + str(curr_round) + ".", .5)


def validate_first_play(player, card, trick_card, message):
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
    else:
        message.update_message("Trick suit not broken!", .50)

    return valid_play

def validate_play(player, card, pile, message):
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
    else:
        message.update_message("You must play the first suit played!", .50)

    return valid_play
