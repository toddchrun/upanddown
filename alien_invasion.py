import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game() :
    """Initializes the game and creates a screen object"""

    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make the play button
    play_button = Button(ai_settings, screen, "Play")

    # Create instance for game stats
    stats = GameStats(ai_settings)

    # Create a scoreboard instance
    sb = Scoreboard(ai_settings, screen, stats)

    #creates the ship
    ship = Ship(ai_settings, screen)

    #makes group of aliens
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    #creates a grouping of bullets
    bullets = Group()

    while True :

        # watches for events from the game_functions module
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
            aliens, bullets)

        if stats.game_active :
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,
                bullets)

        # updates the screen each pass
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
            play_button)

run_game()
