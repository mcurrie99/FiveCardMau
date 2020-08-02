import pygame
import sys
import random
import json
import time
from pygame import mixer
from Network import Network
import os
from Spoons import Spoon
from Buttons import *
from game import Spoons

# Initial variable for holding cards
button = False

#Screen Dimensions
WIDTH =  1920 #2560/2
HEIGHT =  1080 #1440/2

# Temporary First card location
store = [0, 680]
temp = [0, 680]
card_hold = False
dif_x = 0
dif_y = 0

name = ''

def main():
    global WIDTH
    global HEIGTH
    global background
    n = Network()
            
    connect_server(n)
    print('Connected')

    # Initializes py game window
    pygame.init()

    # Sets up screen size, you could use pygame.RESIZABLE or pygame.FULLSCREEN
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption('Cards')
    
    # Background Music
    # mixer.music.load('music.mp3')
    # mixer.music.play(-1)
    
    test = Spoon(screen, n, name, WIDTH, HEIGHT)
    test.main_menu()

def connect_server(network):
    # Initializes connection with server
    global name
    count = 0

    while True:
        print('Enter your game name here')        
        name = input()
        player = network.connect(name)
        if player == 'Good':
            launch = True
            break
        else:
            print('Name is already taken')
    # lobby(screen, player, network, name, server)
        

def place_card(screen, card_hold):

    # White outline on black box
    pressed = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    if (pressed[0] == 1) and (pos[0] >= 1604 and pos[0] <= 1870 and pos[1] >= 50 and pos[1] <= 450) and card_hold==True:
        pygame.draw.rect(screen, (255,255,255), (1584, 30, Card_x + 40, Card_y + 40))

def card_held(screen):
    global card_hold, dif_x, dif_y
    pressed = pygame.mouse.get_pressed()[0]
    pos = pygame.mouse.get_pos()
    if pressed == 1:
        button = True
    elif pressed == 0:
        button = False

    

    if button == True and (pos[0] >= temp[0] and pos[0] <= temp[0] + Card_x and pos[1] >= temp[1] and pos[1] <= temp[1] + Card_y) and card_hold == False:
        dif_x = pos[0] - temp[0]
        dif_y = pos[1] - temp[1]
        temp[0] = pos[0]-dif_x
        temp[1] = pos[1]-dif_y
        pygame.draw.rect(screen, (0,0,0), (temp[0], temp[1], Card_x, Card_y))
        card_hold = True
    elif button == True and card_hold == True:
        # and (pos[0] >= temp[0] and pos[0] <= temp[0] + Card_x and pos[1] >= temp[1] and pos[1] <= temp[1] + Card_y)
        temp[0] = pos[0]-dif_x
        temp[1] = pos[1]-dif_y
        pygame.draw.rect(screen, (0,0,0), (temp[0], temp[1], Card_x, Card_y))
        card_hold = True
    else:
        pygame.draw.rect(screen, (0,0,0), (store[0], store [1], Card_x, Card_y))
        temp[0] = store[0]
        temp[1] = store[1]
        card_hold = False

# def card_move(screen, dif_x, dif_y):
#     pygame.draw.rect(screen, (0,0,0), (1604,50, Card_x, Card_y)
    
if __name__ == '__main__':
    main()
