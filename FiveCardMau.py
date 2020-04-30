import pygame
import sys
import random
import json
import time
import Rules

# Initial variable for holding cards
button = False

#Screen Dimensions
WIDTH =  1920 #2560/2
HEIGHT =  1080 #1440/2

#Card Dimensions
Card_x = 266
Card_y = 400

# Temporary First card location
store = [0, 680]
temp = [0, 680]
card_hold = False
dif_x = 0
dif_y = 0

game_over = False

def main():
    global WIDTH
    global HEIGTH
    global background

    # Initializes py game window
    pygame.init()

    # Sets up screen size
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    game(screen)


def game(screen):
    global WIDTH
    global HEIGTH
    global background

    #Card Placement
    text = 'Place Card(s) Here'
    myFont = pygame.font.SysFont('arial', 36)
    card_placer = myFont.render(text, 1, (255,255,255))

    #Background
    background = pygame.image.load('background.png')

    # Game
    while not game_over:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                sys.exit()
    
        # Resets screen
        screen.fill((0,0,0))
        screen.blit(background, (0,0))
        
        place_card(screen, card_hold)

        # Where to place cards
        pygame.draw.rect(screen, (0,0,0), (1604,50, Card_x, Card_y))
        screen.blit(card_placer, (1610,230))

        # Tap Button
        pygame.draw.

        card_held(screen)

        pygame.display.update()

def place_card(screen, card_hold):

    # White outline on black box
    pressed = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    if (pressed[0] == 1) and (pos[0] >= 1604 and pos[1] >= 50) and card_hold==True:
        pygame.draw.rect(screen, (255,255,255), (1584, 30, Card_x + 40, Card_y + 40))

    # print(pos[0])
    # print (pressed)

def card_held(screen):
    global card_hold, dif_x, dif_y
    pressed = pygame.mouse.get_pressed()[0]
    pos = pygame.mouse.get_pos()
    # print(pressed)
    if pressed == 1:
        button = True
    elif pressed == 0:
        button = False

    

    if button == True and (pos[0] >= temp[0] and pos[0] <= temp[0] + Card_x and pos[1] >= temp[1] and pos[1] <= temp[1] + Card_y) and card_hold == False:
        dif_x = pos[0] - temp[0]
        dif_y = pos[1] - temp[1]
        temp[0] = pos[0]-dif_x
        temp[1] = pos[1]-dif_y
        pygame.draw.rect(screen, (0,0,0), (pos[0]+dif_x, pos[1]+dif_y, Card_x, Card_y))
        card_hold = True
        print(1)
    elif button == True and (pos[0] >= temp[0] and pos[0] <= temp[0] + Card_x and pos[1] >= temp[1] and pos[1] <= temp[1] + Card_y) and card_hold == True:
        temp[0] = pos[0]-dif_x
        temp[1] = pos[1]-dif_y
        pygame.draw.rect(screen, (0,0,0), (temp[0], temp[1], Card_x, Card_y))
        card_hold = True
        # print(temp)
        # print(pos)
        # print(dif_x)
        # print(dif_y)
        print(2)
    elif (button == False) and (card_hold == True):
        pygame.draw.rect(screen, (0,0,0), (store[0], store [1], Card_x, Card_y))
        temp[0] = store[0]
        temp[1] = store[1]
        card_hold = False
        print(3)
    else:
        pygame.draw.rect(screen, (0,0,0), (store[0], store [1], Card_x, Card_y))
        temp[0] = store[0]
        temp[1] = store[1]
        card_hold = False
        print(4)

    

# def card_move(screen, dif_x, dif_y):
#     pygame.draw.rect(screen, (0,0,0), (1604,50, Card_x, Card_y)
    
    



if __name__ == '__main__':
    main()
