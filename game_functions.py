import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
    bullets) :
    """Responses to key and mouse actions"""

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            sys.exit()
        elif event.type == pygame.KEYDOWN :
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP :
            check_keyup_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.MOUSEBUTTONDOWN :
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
    bullets, mouse_x, mouse_y) :
    """Starts game when player clicks the play button"""

    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active :

        ai_settings.initialize_dynamic_settings()

        # Hide mouse cursor
        pygame.mouse.set_visible(False)

        # Reset game stats
        stats.reset_stats()
        stats.game_active = True

        # Empty list of aliens and bullet
        aliens.empty()
        bullets.empty()

        # Reset scoreboard
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_ship_level()
        sb.prep_ships()

        # Create a new fleet and move ship back to center
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def check_keydown_events(event, ai_settings, screen, ship, bullets) :
            if event.key == pygame.K_RIGHT :
                # moves ship to the right
                ship.moving_right = True
            elif event.key == pygame.K_LEFT :
                #moves ship to the left
                ship.moving_left = True
            elif event.key == pygame.K_UP :
                #moves ship up
                ship.moving_up = True
            elif event.key == pygame.K_DOWN :
                #moves ship down
                ship.moving_down = True
            elif event.key == pygame.K_SPACE :
                #create a new bullet
                fire_bullet(ai_settings, screen, ship, bullets)
            elif event.key == pygame.K_q :
                #exits the game upon pressing q
                sys.exit()

def check_keyup_events(event, ai_settings, screen, ship, bullets) :
            if event.key == pygame.K_RIGHT :
                ship.moving_right = False
            elif event.key == pygame.K_LEFT :
                ship.moving_left = False
            elif event.key == pygame.K_UP :
                ship.moving_up = False
            elif event.key == pygame.K_DOWN :
                ship.moving_down = False

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
    aliens, bullets) :
    """Check to see if bullets have hit aliens, removing both objects"""

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions :
        for aliens in collisions.values() :
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_scores(stats, sb)

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets) :
    """Updating position of bullets and removing old"""

    #updates position of each bullet and removes if reaching top of screen
    bullets.update()
    for bullet in bullets.copy() :
        if bullet.rect.bottom <= 0 :
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
        aliens, bullets)

    # Check to see if a fleet of aliens is depleted, and if so, create new one
    if len(aliens) == 0 :
        # Destroy existing bullets and creat new fleet
        bullets.empty()
        ai_settings.increase_speed()
        stats.ship_level += 1
        sb.prep_ship_level()
        create_fleet(ai_settings, screen, ship, aliens)

def check_fleet_edges(ai_settings, aliens) :
    """Response if aliens have hit screen edge"""

    for alien in aliens.sprites() :
        if alien.check_edges() :
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens) :
    """Drop the entire fleet and change directions"""

    for alien in aliens.sprites() :
        alien.rect.y += ai_settings.alien_drop_speed

    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets) :
    """Respond to ship being hit by alien"""

    # updates ships left, resets the screen and pauses
    if stats.ships_left > 0 :
        stats.ships_left -= 1
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sb.prep_ships()
        sleep(0.5)
    else :
        stats.game_active = False
        pygame.mouse.set_visible(True)
        stats.reset_stats()

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets) :
    """Check if any aliens have hit the bottom, then reset if so"""

    screen_rect = screen.get_rect()
    for alien in aliens.sprites() :
        if alien.rect.bottom >= screen_rect.bottom :
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets) :
    """Updates the position of all aliens"""

    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens) :
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

    # Look for aliens hitting the bottom
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)

def fire_bullet(ai_settings, screen, ship, bullets) :
    """Fires a bullet if the maximum not reached"""

    if len(bullets) < ai_settings.bullets_allowed :
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens(ai_settings, alien_width) :
    """Determine number of aliens in a given row"""

    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height) :
    """Determine number of rows that will fit aliens"""

    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number) :
    """Create an alien and place it in the row"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens) :
    """Creat a full fleet of aliens"""

    #create alien and determine total number to be added
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    #create fleet of aliens
    for row_number in range(number_rows) :
        for alien_number in range(number_aliens_x) :
        #create alien and place in row
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_high_scores(stats, sb) :
    """Check to see if there is a new high score"""

    if stats.score > stats.high_score :
        stats.high_score = stats.score
        sb.prep_high_score()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
    play_button) :
    """Updates the images on the screen"""

    screen.fill(ai_settings.bg_color)

    #drawing of all the bullets
    for bullet in bullets.sprites() :
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # Draw score information
    sb.show_score()

    # Draw play button if game is inactive
    if not stats.game_active :
        play_button.draw_button()

    pygame.display.flip()
