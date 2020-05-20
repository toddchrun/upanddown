"""
Prompt Screen Class - Contains prompt screen object that will function for user to begin game
"""
import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
from pygame_textinput import TextInput
from prompt_screen_button import PromptScreenButton
from play_button import Button

class PromptScreen():

    def __init__(self, settings, screen):
        """
        Initializes basic properties of the prompt screen
        """

        #only one message and title to be displayed at any given time
        self.title = "Welcome to Up and Down the River!"
        self.player_name_text = "Enter Player Name:"
        self.difficulty_levels_text = "Select Difficulty:"
        self.levels = Group()
        self.number_of_players_text = "Select Number of Players:"
        self.players = Group()
        self.number_of_rounds_text = "Select Number of Rounds:"
        self.rounds = Group()

        #basic visual settings
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.bg_color = settings.bg_color

        #title font settings - white for now and just default
        self.title_text_color = (255, 255, 255)
        self.title_font = pygame.font.SysFont(None, 48)

        #Set of title image
        self.title_image = self.title_font.render(self.title, True, self.title_text_color)

        #definitions of the title image rect
        self.title_rect = self.title_image.get_rect()
        self.title_rect.y = self.settings.screen_height * .05
        self.title_rect.center = ((self.settings.screen_width / 2), self.title_rect.y)

        #player name font settings - white for now and just default
        self.player_name_text_color = (255, 255, 255)
        self.player_name_font = pygame.font.SysFont(None, 36)

        #Set of player name text image
        self.player_name_image = self.player_name_font.render(self.player_name_text, True, self.player_name_text_color)

        #definitions of the player name text image rect
        self.player_name_rect = self.player_name_image.get_rect()
        self.player_name_rect.y = self.settings.screen_height * .20
        self.player_name_rect.x = self.settings.screen_width * .20

        #number of players font settings - white for now and just default
        self.player_number_text_color = (255, 255, 255)
        self.player_number_font = pygame.font.SysFont(None, 36)

        #Set of player name text image
        self.player_number_image = self.player_number_font.render(self.number_of_players_text, True, self.player_number_text_color)

        #definitions of the player name text image rect
        self.player_number_rect = self.player_number_image.get_rect()
        self.player_number_rect.y = self.settings.screen_height * .30
        self.player_number_rect.x = self.settings.screen_width * .20

        #difficulty levels font settings - white for now and just default
        self.difficulty_levels_text_color = (255, 255, 255)
        self.difficulty_levels_font = pygame.font.SysFont(None, 36)

        #Set of difficulty levels text image
        self.difficulty_levels_text_image = self.difficulty_levels_font.render(self.difficulty_levels_text, True, self.difficulty_levels_text_color)

        #definitions of the difficulty levels text image rect
        self.difficulty_levels_rect = self.difficulty_levels_text_image.get_rect()
        self.difficulty_levels_rect.y = self.settings.screen_height * .40
        self.difficulty_levels_rect.x = self.settings.screen_width * .20

        #difficulty levels font settings - white for now and just default
        self.number_of_rounds_text_color = (255, 255, 255)
        self.number_of_rounds_text_font = pygame.font.SysFont(None, 36)

        #Set of difficulty levels text image
        self.number_of_rounds_text_image = self.number_of_rounds_text_font.render(self.number_of_rounds_text, True, self.number_of_rounds_text_color)

        #definitions of the difficulty levels text image rect
        self.number_of_rounds_rect = self.number_of_rounds_text_image.get_rect()
        self.number_of_rounds_rect.y = self.settings.screen_height * .50
        self.number_of_rounds_rect.x = self.settings.screen_width * .20

        #Instance of pygame text input module
        self.text_input = TextInput()
        self.text_input_rect_x = self.settings.screen_width * .50
        self.text_input_rect_y = self.settings.screen_height * .20

        #Sprite Group of player options
        for index in range(0 , len(self.settings.number_of_players_option)):
            msg = str(self.settings.number_of_players_option[index])
            pos_x = self.settings.screen_width * (.50 + (index * .075))
            pos_y = self.player_number_rect.y
            button = PromptScreenButton(self.settings, self.screen, msg, False, pos_x, pos_y)
            self.players.add(button)

        self.players.sprites()[0].select() #sets first option as highlight

        #Sprite Group of difficulties
        for index in range(0 , len(self.settings.game_difficulty_option)):
            msg = self.settings.game_difficulty_option[index]
            pos_x = self.settings.screen_width * (.50 + (index * .15))
            pos_y = self.difficulty_levels_rect.y
            button = PromptScreenButton(self.settings, self.screen, msg, False, pos_x, pos_y)
            self.levels.add(button)

        self.levels.sprites()[0].select() #sets first option as highlight

        #Sprite Group of rounds
        for index in range(1 , self.settings.max_rounds_available+1):
            msg = str(index)
            pos_x = self.settings.screen_width * (.50 + ((index-1) * .05))
            pos_y = self.number_of_rounds_rect.y
            button = PromptScreenButton(self.settings, self.screen, msg, False, pos_x, pos_y)
            self.rounds.add(button)

        self.rounds.sprites()[0].select() #sets first option as highlight

        #Play Button instance to capture all the prompts when selected
        self.play_button = Button(self.settings, self.screen)


    def show_prompt_screen(self):
        """Blits the text images on the screen"""

        #labels
        self.screen.blit(self.title_image, self.title_rect)
        self.screen.blit(self.player_name_image, self.player_name_rect)
        self.screen.blit(self.player_number_image, self.player_number_rect)
        self.screen.blit(self.difficulty_levels_text_image, self.difficulty_levels_rect)
        self.screen.blit(self.number_of_rounds_text_image, self.number_of_rounds_rect)

        #text input area
        self.screen.blit(self.text_input.get_surface(), (self.text_input_rect_x, self.text_input_rect_y))

        #display sprite group options
        self.levels.draw(self.screen)
        self.players.draw(self.screen)
        self.rounds.draw(self.screen)

        #display the play button
        self.play_button.draw_button()

    def update_text(self, events):
        """Updates the text input box with events"""

        self.text_input.update(events)
