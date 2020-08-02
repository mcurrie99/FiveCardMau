import pygame
import sys
import random
import json
from pygame import mixer
from Network import Network
from Spoons import *
from Buttons import *
from Blackjack import *
# from game import Spoons


# Make sure you update this when you add a new game
Game_Modes = ['Spoons', 'Blackjack']

#Screen Dimensions
WIDTH =  1920 #2560/2
HEIGHT =  1080 #1440/2



name = ''

def main():
    global WIDTH
    global HEIGTH
    global background
    n = Network()
            
    connect_server(n)
    print('Connected to server')

    # Initializes py game window
    pygame.init()

    # Sets up screen size, you could use pygame.RESIZABLE or pygame.FULLSCREEN
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption('Cards')
    
    # Background Music
    # mixer.music.load('music.mp3')
    # mixer.music.play(-1)
    
    main_menu(screen, name, n)

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
        

def main_menu(screen, name, network):
        join = False

        lob = pygame.image.load('lobby.png')

        while join == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        sys.exit()

            screen.fill((0,0,0))
            screen.blit(lob, (0,0))


            MAIN = Button(screen, 'Main Menu', 'arial', 35, WIDTH/2, 400, (255,255,255), False, True)
            WELCOME = Button(screen, f'Welcome {name}', 'arial', 35, 0, 0, (255,255,255), False, False)
            button_place = HEIGHT/2
            for i in Game_Modes:
                JOIN = Button(screen, f'Join {i}', 'arial', 80, WIDTH/2, button_place, (255,255,255), False, True)
                clicked = JOIN.hover()
                if clicked == True:
                    if i == 'Spoons':
                        spoons = Spoon(screen, network, name, WIDTH, HEIGHT)
                        server = network.send(i)
                        spoons.lobby()
                    elif i == 'Blackjack':
                        blackjack = Blackjack(screen, network, name, WIDTH, HEIGHT)
                button_place += JOIN.render_height + 50
            # if clicked == False:
            #     self.network.send_only('None')

            pygame.display.update()

    
if __name__ == '__main__':
    main()







# Initial variable for holding cards
# button = False

# Temporary First card location
# store = [0, 680]
# temp = [0, 680]
# card_hold = False
# dif_x = 0
# dif_y = 0

# def place_card(screen, card_hold):

#     # White outline on black box
#     pressed = pygame.mouse.get_pressed()
#     pos = pygame.mouse.get_pos()
#     if (pressed[0] == 1) and (pos[0] >= 1604 and pos[0] <= 1870 and pos[1] >= 50 and pos[1] <= 450) and card_hold==True:
#         pygame.draw.rect(screen, (255,255,255), (1584, 30, Card_x + 40, Card_y + 40))

# def card_held(screen):
#     global card_hold, dif_x, dif_y
#     pressed = pygame.mouse.get_pressed()[0]
#     pos = pygame.mouse.get_pos()
#     if pressed == 1:
#         button = True
#     elif pressed == 0:
#         button = False

    

#     if button == True and (pos[0] >= temp[0] and pos[0] <= temp[0] + Card_x and pos[1] >= temp[1] and pos[1] <= temp[1] + Card_y) and card_hold == False:
#         dif_x = pos[0] - temp[0]
#         dif_y = pos[1] - temp[1]
#         temp[0] = pos[0]-dif_x
#         temp[1] = pos[1]-dif_y
#         pygame.draw.rect(screen, (0,0,0), (temp[0], temp[1], Card_x, Card_y))
#         card_hold = True
#     elif button == True and card_hold == True:
#         # and (pos[0] >= temp[0] and pos[0] <= temp[0] + Card_x and pos[1] >= temp[1] and pos[1] <= temp[1] + Card_y)
#         temp[0] = pos[0]-dif_x
#         temp[1] = pos[1]-dif_y
#         pygame.draw.rect(screen, (0,0,0), (temp[0], temp[1], Card_x, Card_y))
#         card_hold = True
#     else:
#         pygame.draw.rect(screen, (0,0,0), (store[0], store [1], Card_x, Card_y))
#         temp[0] = store[0]
#         temp[1] = store[1]
#         card_hold = False

# def card_move(screen, dif_x, dif_y):
#     pygame.draw.rect(screen, (0,0,0), (1604,50, Card_x, Card_y)