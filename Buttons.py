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
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 150
        self.button_hold = False
        self.card = card
        self.screen = screen
        self.font = font
        self.fontsize = fontsize
        self.center = center
        self.draw_text()

    def draw(self, win):
        # Might not need this either, see draw_tect()
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont('arial', 40)
        text = font.render(self.text, 1, (255, 255, 255))
        text_height = int(text.get_height())
        text_width = int(text.get_width())
        self.screen.blit(text, (self.x + round(self.width/2) - round(text_width/2), self.y + round(self.height/2) - round(text_height/2)))

    def click(self):
        pressed = pygame.mouse.get_pressed()[0]
        if pressed == True:
            return True
        else:
            return False
    
    def moving(self, pos, button_hold):
        pass

    def draw_text(self):
        texter = str(self.text)
        fonter = pygame.font.SysFont(self.font, self.fontsize)
        Render = fonter.render(texter, 1, self.color)
        self.render_width = int(Render.get_width())
        self.render_height = int(Render.get_height())
        if self.center == True:
            pygame.draw.rect(self.screen, (0,0,0), (int(self.x - self.render_width/2 - 10), int(self.y - self.render_height/2 - 10), int(self.render_width + 20), int(self.render_height + 20)))
            self.screen.blit(Render, (int(self.x - self.render_width/2), int(self.y - self.render_height/2)))
        elif self.center == False:
            pygame.draw.rect(self.screen, (0,0,0), (self.x, self.y, int(self.render_width + 20), int(self.render_height + 20)))
            self.screen.blit(Render, (self.x + 10, self.y + 10))

    def hover(self):
        pos = pygame.mouse.get_pos()
        mouse_x = pos[0]
        mouse_y = pos[1]
        clicked = False
        if self.center == True:
            upper_x = self.x + self.render_width/2 + 10
            lower_x = self.x - self.render_width/2 - 10
            upper_y = self.y - self.render_height/2 - 10
            lower_y = self.y + self.render_height/2 + 10
            if ((mouse_x <= upper_x) and (mouse_x >= lower_x)) and ((mouse_y >= upper_y) and (mouse_y <= lower_y)):
                pygame.draw.rect(self.screen, (255,255,255), (int(self.x - self.render_width/2 - 20), int(self.y - self.render_height/2 - 20), int(self.render_width + 40), int(self.render_height + 40)))
                self.draw_text()
                return self.click()
            else:
                return False
        elif self.center == False:
            upper_x = self.x + self.render_width + 10
            lower_x = self.x
            upper_y = self.y
            lower_y = self.y + self.render_height + 10
            if ((mouse_x <= upper_x) and (mouse_x >= lower_x)) and ((mouse_y >= upper_y) and (mouse_y <= lower_y)):
                pygame.draw.rect(self.screen, (255,255,255), (self.x - 10, self.y - 10, int(self.render_width + 40), int(self.render_height + 40)))
                self.draw_text()
                return self.click()
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
        self.screen = screen
        self.card = card
        self.x = x
        self.y = y
        self.scale = scale
        self.draw()

    def draw(self):
        self.location = pygame.image.load(f'Playing_Cards/{self.card}.png')
        self.location = pygame.transform.rotozoom(self.location, 0, self.scale)
        self.screen.blit(self.location, (self.x, self.y))

    def hover(self):
        pos = pygame.mouse.get_pos()
        mouse_x = pos[0]
        mouse_y = pos[1]
        clicked = False
        upper_x = self.x + 250
        lower_x = self.x
        upper_y = self.y
        lower_y = self.y + 363
        if ((mouse_x <= upper_x) and (mouse_x >= lower_x)) and ((mouse_y >= upper_y) and (mouse_y <= lower_y)):
            pygame.draw.rect(self.screen, (0,0,0), (self.x - 10, self.y - 10, int(270), int(383)))
            self.draw()
            return self.click()
        else:
            return False
    def click(self):
        pressed = pygame.mouse.get_pressed()[0]
        if pressed == True:
            return True
        else:
            return False