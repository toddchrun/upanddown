"""
Screen functions for Up and Down the River
"""

import sys
import pygame

def update_screen(settings, screen) :
    """Updates the images on the screen"""

    screen.fill(settings.bg_color)

    pygame.display.flip()

def set_player_position(settings, screen, active_players):
    """Sets player position display based on number of players"""

    #Array of positional configuration based on total number of players
    player_positions = [
        {'total': 3, 'positions': [2,7,9]},
        {'total': 4, 'positions': [1,3,7,9]},
        {'total': 5, 'positions': [1,3,6,8,10]},
        {'total': 6, 'positions': [1,3,5,7,9,11]},
        {'total': 7, 'positions': [1,3,4,6,7,9,11]},
        {'total': 8, 'positions': [1,3,4,6,7,9,10,12]}
    ]

    #Set the position index array
    for positions in player_positions:
        if positions['total'] == settings.number_of_players:
            position_index = positions['positions']
            break

    #Assign screen position for each player
    for index in range(0, len(active_players)):
        active_players[index].screen_position = position_index[index]
