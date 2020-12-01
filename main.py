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
# List of game mode names to render
Game_Modes = ['Spoons', 'Blackjack']

#Screen Dimensions
WIDTH =  1920 #2560/2
HEIGHT =  1080 #1440/2



name = ''

def main():
    global WIDTH
    global HEIGTH
    global background
    n = Network() # Creates object of network to contact server
            
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
        print('Enter your game name here') # Asks player to enter name
        name = input() # Asks to enter his name
        if count == 0:
            player = network.connect(name) # Sends player name for validation
            count += 1
        else:
            player = network.send_name(name)

        if player == 'Good':
            launch = True
            break
        elif player == 'Not':
            print('Name is already taken') # Enter name again
        else:
            print('Could not connect to Server, try launching again.')
            time.sleep(3)
            sys.exit()
        
        

def main_menu(screen, name, network):
        join = False

        lob = pygame.image.load('lobby.png')

        # Allows player to quit
        while join == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    # If q is pressed the game quits
                    if event.key == pygame.K_q:
                        sys.exit()

            screen.fill((0,0,0))
            screen.blit(lob, (0,0))


            MAIN = Button(screen, 'Main Menu', 'arial', 35, WIDTH/2, 400, (255,255,255), False, True) # Renders main menu text
            WELCOME = Button(screen, f'Welcome {name}', 'arial', 35, 0, 0, (255,255,255), False, False) # Renders welcome text
            button_place = HEIGHT/2 # Where to place button
            for i in Game_Modes: # Renders all the game modes that are accessable
                JOIN = Button(screen, f'Join {i}', 'arial', 80, WIDTH/2, button_place, (255,255,255), False, True) # Creates button for each game mode
                clicked = JOIN.hover()
                if clicked == True:
                    if i == 'Spoons':
                        spoons = Spoon(screen, network, name, WIDTH, HEIGHT)
                        server = network.send(i) # Sends the game that wants to be joined
                        spoons.lobby() # Goes to lobby
                    elif i == 'Blackjack':
                        blackjack = Blackjack(screen, network, name, WIDTH, HEIGHT)
                        server = network.send(i) # Sends the game that wants to be joined
                        blackjack.lobby() # Goes to lobby
                button_place += JOIN.render_height + 50
            # if clicked == False:
            #     self.network.send_only('None')

            pygame.display.update()

    
if __name__ == '__main__':
    main()
    # States this as main program

