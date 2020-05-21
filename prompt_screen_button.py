"""
Prompt Screen Button Class - Contains prompt screen button object that will function for user to begin game
"""
import pygame
from pygame.sprite import Sprite

class PromptScreenButton(Sprite):

    def __init__(self, settings, screen, msg, active, pos_x, pos_y):
        """initial set of text and positioning"""

        super().__init__()

        #sets initial parameters
        self.msg = msg
        self.active = active #used to pass selected
        self.hidden = False

        #basic visual settings
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.bg_color = settings.bg_color

        #message font settings - white for now and just default
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 36)

        #initial set of button image
        self.image = self.font.render(self.msg, True, self.text_color)

        #definitions of the message image rect
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def select(self):
        """Updates whether button is active to change text color"""

        if not self.hidden:
            self.active = True

            self.text_color = (150, 0, 0)

            self.image = self.font.render(self.msg, True, self.text_color)

    def deselect(self):
        """Updates whether button is active to change text color"""

        if not self.hidden:
            self.active = False

            self.text_color = (255, 255, 255)

            self.image = self.font.render(self.msg, True, self.text_color)

    def hide(self):
        """Hides the prompt button, for when max rounds cannot be 7, 8 or 9"""
            
        self.hidden = True

        self.text_color = self.settings.bg_color

        self.image = self.font.render(self.msg, True, self.text_color)

    def unhide(self):
        """Hides the prompt button, for when max rounds cannot be 7, 8 or 9"""

        self.hidden = False

        self.text_color = (255, 255, 255)

        self.image = self.font.render(self.msg, True, self.text_color)
