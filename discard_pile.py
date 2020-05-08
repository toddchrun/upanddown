"""
Discard Pile Class
"""
from pygame.sprite import Group

class Pile():

    def __init__(self, settings, screen):
        """
        Initializes empty discard pile sprite Group
        The pile will not have it's own rect, it will rely on sprites for their rects
        """

        self.discards = Group()
        self.x = settings.screen_width / 2 #set for half point of table
        self.y = (settings.screen_height / 2) - (.071875 * settings.screen_height) #Set for card to be centered
