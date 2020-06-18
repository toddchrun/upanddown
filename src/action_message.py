"""
Action Message Class - Contains message object for game play text and title
"""
import pygame
import time

class Message():

    def __init__(self, settings, screen):
        """
        Initializes the action message that will be constantly updated and
        will display each action of gameplay and title
        """

        #inital title and message
        self.msg = "Let's Play!"
        self.title = "Up and Down the River"

        #passing settings and screen object
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.bg_color = settings.bg_color

        #title and message font settings
        self.text_color = (255, 255, 255)
        self.message_font = pygame.font.SysFont(None, 28)
        self.title_font = pygame.font.SysFont(None, 48)

        #initial set of images to be displayed
        self.message_image = self.message_font.render(self.msg, True, self.text_color)
        self.title_image = self.title_font.render(self.title, True, self.text_color)

        #initialize image rects
        self.message_rect = self.message_image.get_rect()
        self.message_rect.y = self.settings.screen_height * .625
        self.message_rect.center = ((self.settings.screen_width / 2), self.message_rect.y)
        self.title_rect = self.title_image.get_rect()
        self.title_rect.y = self.settings.screen_height * .05
        self.title_rect.center = ((self.settings.screen_width / 2), self.title_rect.y)

    def update_message(self, msg, pause):
        """Updated message with new text and pause if needed"""

        self.msg = msg
        self.message_image = self.message_font.render(self.msg, True, self.text_color)
        self.show_message()
        time.sleep(pause)

    def update_title(self, title):
        """Updated title with new text"""

        self.title = title
        self.title_image = self.title_font.render(self.title, True, self.text_color)
        self.show_message()

    def show_message(self):
        """Shows the current message and title"""

        #re-centers the message each time
        self.message_rect = self.message_image.get_rect()
        self.message_rect.y = self.settings.screen_height * .625
        self.message_rect.center = ((self.settings.screen_width / 2), self.message_rect.y)

        #re-centers title each time
        self.title_rect = self.title_image.get_rect()
        self.title_rect.y = self.settings.screen_height * .05
        self.title_rect.center = ((self.settings.screen_width / 2), self.title_rect.y)

        self.screen.blit(self.message_image, self.message_rect)
        self.screen.blit(self.title_image, self.title_rect)
