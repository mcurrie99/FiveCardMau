import pygame
import sys
import random
import json
import time
from pygame import mixer
from Network import Network
import os

class Button:
    '''
        Makes every button that can be used an object
        screen = pygame render screen
        text = what you would like to be said
        font = what font you would like
        fontsize = fontsize you would like
        x = width location location on the screen
        y = height location on the screen
        color = color of the text (x,y,z) RGB
        card = Is it a card True or False
        center = Use the center as reference
        '''
    def __init__(self, screen, text, font, fontsize, x, y, color, card, center):
        self.text = text # text = what you would like to be said
        self.x = x # x = width location location on the screen
        self.y = y # y = height location on the screen
        self.color = color # color = color of the text (x,y,z) RGB
        self.width = 150 # Width
        self.height = 150 # Height
        self.button_hold = False # Is the card Held, this will eventually allow the player to drag the card across the screen
        self.card = card # Is it going to be a card
        self.screen = screen # screen = pygame render screen
        self.font = font # font = what font you would like
        self.fontsize = fontsize # fontsize = fontsize you would like
        self.center = center # center = Use the center as reference
        self.draw_text() # Draws the text

    def draw(self, win): # Not ever used
        # Might not need this either, see draw_tect()
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height)) # Draw rectangle
        font = pygame.font.SysFont('arial', 40)
        text = font.render(self.text, 1, (255, 255, 255))
        text_height = int(text.get_height())
        text_width = int(text.get_width())
        self.screen.blit(text, (self.x + round(self.width/2) - round(text_width/2), self.y + round(self.height/2) - round(text_height/2)))

    def click(self): # Checks if the button is clicked
        pressed = pygame.mouse.get_pressed()[0] # State of what your mouse left click is
        if pressed == True: # Is the left clicked pressed
            return True
        else:
            return False
    
    def moving(self, pos, button_hold): # Will eventually be worked on
        pass

    def draw_text(self):
        texter = str(self.text) # Makes the text into a string
        fonter = pygame.font.SysFont(self.font, self.fontsize) # Creates text in the font
        Render = fonter.render(texter, 1, self.color) # Render the words
        self.render_width = int(Render.get_width()) # Width Size of text
        self.render_height = int(Render.get_height()) # Height Size of text
        if self.card == False:
            if self.center == True:
                # Centers rectangle that is rendered
                pygame.draw.rect(self.screen, (0,0,0), (int(self.x - self.render_width/2 - 10), int(self.y - self.render_height/2 - 10), int(self.render_width + 20), int(self.render_height + 20)))
                # Centers the text
                self.screen.blit(Render, (int(self.x - self.render_width/2), int(self.y - self.render_height/2)))
            elif self.center == False:
                # Renders the rectangle in reference to top left
                pygame.draw.rect(self.screen, (0,0,0), (self.x, self.y, int(self.render_width + 20), int(self.render_height + 20)))
                # Renders the text that is given
                self.screen.blit(Render, (self.x + 10, self.y + 10))
        # if self.card == True: # NOT USED

        #     # This might need to be changed in the future
        #     self.center = True

        #     if self.center == True:
        #         pygame.draw.rect(self.screen, (0,0,0), (int(self.x - 62.5), int(self.y - 90.75), 125, 181.5))
        #         self.screen.blit(Render, (int(self.x - self.render_width/2), int(self.y - self.render_height/2)))
        #     # elif self.center == False:
        #     #     pygame.draw.rect(self.screen, (0,0,0), (self.x, self.y, int(self.render_width + 20), int(self.render_height + 20)))
        #     #     self.screen.blit(Render, (self.x + 10, self.y + 10))
        

    def hover(self):
        pos = pygame.mouse.get_pos()
        mouse_x = pos[0] # X position of mouse
        mouse_y = pos[1] # Y position of mouse
        clicked = False # Is the button clicked
        if self.center == True:
            upper_x = self.x + self.render_width/2 + 10 # Right side of rectangle
            lower_x = self.x - self.render_width/2 - 10 # Left side of rectangle
            upper_y = self.y - self.render_height/2 - 10 # Top of rectangle
            lower_y = self.y + self.render_height/2 + 10 # Bottom of rectangle
            if ((mouse_x <= upper_x) and (mouse_x >= lower_x)) and ((mouse_y >= upper_y) and (mouse_y <= lower_y)):
                pygame.draw.rect(self.screen, (255,255,255), (int(self.x - self.render_width/2 - 20), int(self.y - self.render_height/2 - 20), int(self.render_width + 40), int(self.render_height + 40)))
                self.draw_text()
                return self.click() # Checks if person has clicked
            else:
                return False
        elif self.center == False:
            upper_x = self.x + self.render_width + 10 # Right side of rectangle
            lower_x = self.x # Left side of rectangle
            upper_y = self.y # Top of rectangle
            lower_y = self.y + self.render_height + 10 # Bottom of Rectangle
            if ((mouse_x <= upper_x) and (mouse_x >= lower_x)) and ((mouse_y >= upper_y) and (mouse_y <= lower_y)):
                pygame.draw.rect(self.screen, (255,255,255), (self.x - 10, self.y - 10, int(self.render_width + 40), int(self.render_height + 40)))
                self.draw_text()
                return self.click() # Checks if person clicked
            else:
                return False

class Card:
    '''
    screen = pygame screen that is being used
    card = card name that is being used
    x = the x location for where the card will be placed
    y = the y location for where the card will be placed
    '''
    def __init__(self, screen, card, scale, x, y):
        self.screen = screen # Screen to render on
        self.card = card # Card texture to render
        self.x = x #  X position
        self.y = y # Y position
        self.scale = scale # Scale down size
        self.draw()

    def draw(self):
        self.location = pygame.image.load(f'Playing_Cards/{self.card}.png') # Loads texture
        self.location = pygame.transform.rotozoom(self.location, 0, self.scale) # Scales photo
        self.screen.blit(self.location, (self.x, self.y)) # Renders photo

    def hover(self):
        pos = pygame.mouse.get_pos() # Gets position of mouse
        mouse_x = pos[0] # X position of mouse
        mouse_y = pos[1] # Y position of mouse
        clicked = False # IS the card clicked
        upper_x = self.x + 250 # Right side of rectangle
        lower_x = self.x # Left side of rectangle
        upper_y = self.y # Top of rectangle
        lower_y = self.y + 363 # Bottom of rectangle
        if ((mouse_x <= upper_x) and (mouse_x >= lower_x)) and ((mouse_y >= upper_y) and (mouse_y <= lower_y)):
            pygame.draw.rect(self.screen, (0,0,0), (self.x - 10, self.y - 10, int(270), int(383)))
            self.draw()
            return self.click() # Checks if the card is clicked
        else:
            return False
    def click(self):
        pressed = pygame.mouse.get_pressed()[0]
        if pressed == True:
            return True # Card is clicked
        else:
            return False # Card is no clicked