"""
Action Message Class
"""
import pygame
import time

class Message():

    def __init__(self, settings, screen):
        """
        Initializes the action message that will be constantly updated and
        will display each action of gameplay to make everything smooth
        """

        #only one message to be displayed at any given time
        self.msg = "Let's Play!"

        #visual settings
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.bg_color = settings.bg_color

        #font settings - white for now and just default
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 28)

        #initial set of message image
        self.message_image = self.font.render(self.msg, True, self.text_color)

        #definitions of the message image rect
        self.message_rect = self.message_image.get_rect()
        self.message_rect.y = self.settings.screen_height * .625
        self.message_rect.center = ((self.settings.screen_width / 2), self.message_rect.y)

    def update_message(self, msg, pause):
        """Updated message with new text and pause if needed"""

        self.msg = msg

        self.message_image = self.font.render(self.msg, True, self.text_color)

        self.screen.blit(self.message_image, self.message_rect)

        time.sleep(pause)

    def show_message(self):
        """Called within screen functions update screen, will always refresh to show
        current message
        """

        #re-centers the message each time
        self.message_rect = self.message_image.get_rect()
        self.message_rect.y = self.settings.screen_height * .625
        self.message_rect.center = ((self.settings.screen_width / 2), self.message_rect.y)

        self.screen.blit(self.message_image, self.message_rect)
