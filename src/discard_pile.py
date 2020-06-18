"""
Discard Pile Class - container for card objects discarded during play
"""
from pygame.sprite import Group

class Pile():

    def __init__(self, settings, screen):

        #initialize as a Sprite Group and sets starting position
        self.discards = Group()
        self.x = settings.screen_width / 2 #set for half point of table
        self.y = (settings.screen_height / 2) - (.071875 * settings.screen_height) #Set for card to be centered

    def current_winning_card(self, trick_card):
        """Called upon to check on the current winning card in the discard pile"""

        #Need a false bool for each hand, even if trick broken, one may have not been played
        trick_played = False
        max_value = 0

        #Establishes sprite list
        round_hand = self.discards.sprites()

        #Goes through all cards to determine if a trick was played
        for card in self.discards:
            if (card.suit == trick_card.suit):
                trick_played = True
                trick_suit = trick_card.suit

        #If no trick is played, set trick suit to the first card played
        if not trick_played:
            trick_suit = round_hand[0].suit

        #Max value set for player playing highest value of trick suit
        for card in round_hand:
            if (card.suit == trick_suit):
                if (card.value > max_value):
                    max_value = card.value
                    winning_card = card

        return winning_card
