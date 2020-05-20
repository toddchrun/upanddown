"""
Play Button class
"""

import pygame.font

class Button() :

    def __init__(self, settings, screen) :
        """Initializes button attributes"""

        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.msg = "PLAY!"
        self.game_active = False #When true, start the game and pass prompts to settings

        # Set dimensions and properties of the Button
        self.width, self.height = self.settings.screen_width / 7, self.settings.screen_height / 16
        self.button_color = (0, 0, 200)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (self.settings.screen_width / 2, self.settings.screen_height * .80)

        self.prep_msg(self.msg)

    def prep_msg(self, msg) :
        """Turn msg into a rendered image and center on the button"""

        self.msg_image = self.font.render(msg, True, self.text_color,
            self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self) :
        """Draws buttons and message on the screen"""

        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
