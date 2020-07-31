import pygame
import sys
import random
import json
import time
from pygame import mixer
from Network import Network
from game import Spoons
from Buttons import *
    
    
class Spoon:    
    '''
    Spoons game that will be supported
    Hopefully the first of modular parts of the game
    screen, network, name, WIDTH, HEIGHT
    '''
    def __init__(self, screen, network, name, WIDTH, HEIGHT):
        self.screen = screen
        self.network = network
        self.name = name
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.game_over = False

    def game(self):
        voted = False

        #Background
        background = pygame.image.load('background.png')

        WAIT = 0
        # Game
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        sys.exit()
            self.server = self.network.get_game()
            if self.server.winner == True:
                break
            # Resets screen
            self.screen.fill((0,0,0))
            self.screen.blit(background, (0,0))

            # Creates and draws cards that the player holds
            
            try:
                CARD1 = Card(self.screen, self.server.hand[self.name]['Hand'][0], 100, 680)
                CARD2 = Card(self.screen, self.server.hand[self.name]['Hand'][1], 590, 680)
                CARD3 = Card(self.screen, self.server.hand[self.name]['Hand'][2], 1080, 680)
                CARD4 = Card(self.screen, self.server.hand[self.name]['Hand'][3], 1570, 680)
            except:
                print('Error at printing cards')
            try:
                WAITING = Card(self.screen, self.server.hand[self.name]['Waiting'][0], 1570, 100)
            except:
                WAITING = False

            PASS = Button(self.screen, 'Pass', 'arial', 90, 150, 150, (255,255,255), False, False)

            # Draws square under the card the player is hovering over and sends data to server
            if CARD1.hover() == True and WAITING != False and WAIT == 100:
                self.network.change_hand(self.server.hand[self.name]['Hand'][0], self.server.hand[self.name]['Waiting'][0])
                WAIT = 0
            if CARD2.hover() == True and WAITING != False and WAIT == 100:
                self.network.change_hand(self.server.hand[self.name]['Hand'][1], self.server.hand[self.name]['Waiting'][0])
                WAIT = 0
            if CARD3.hover() == True and WAITING != False and WAIT == 100:
                self.network.change_hand(self.server.hand[self.name]['Hand'][2], self.server.hand[self.name]['Waiting'][0])
                WAIT = 0
            if CARD4.hover() == True and WAITING != False and WAIT == 100:
                self.network.change_hand(self.server.hand[self.name]['Hand'][3], self.server.hand[self.name]['Waiting'][0])
                WAIT = 0
            if PASS.hover() == True and WAITING != False and WAIT == 100:
                self.network.change_hand('Pass', self.server.hand[self.name]['Waiting'][0])
                WAIT = 0

            # Might use not sure yet
            # WAITING.hover()
            

            player_y = 100
            for i, j in enumerate(self.server.players):
                PLAYER = Button(self.screen, j, 'arial', 60, 960, player_y, (255,255,255), False, True)
                player_y = PLAYER.render_height + 250

            self.check_winner()

            if WAIT < 100:
                WAIT += 5

            pygame.display.update()

    def lobby(self):
        global close_game
        gamer = False
        close_game = True
        voted = False
        lob = pygame.image.load('background.png')
        # game_over = True
        # network.change_hand('this', 'works')
        while gamer == False:
            self.server = self.network.get_game()
            player_y = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        sys.exit()
            self.screen.fill((0,0,0))
            self.screen.blit(lob, (0,0))

            LOBBY = Button(self.screen, 'Lobby', 'arial', 35, 0, 0, (255,255,255), False, False)
            for i, j in enumerate(self.server.players):
                PLAYER = Button(self.screen, j, 'arial', 40, 1500, player_y, (255,255,255), False, False)
                player_y = PLAYER.render_height + 50

            if voted == False:
                VOTE = Button(self.screen, 'Vote to Start Game', 'arial', 35, 50, 880, (0,255,0), False, False)
                clicked = VOTE.hover()
                if clicked == True:
                    self.network.send('voted')
                    voted = True
            elif voted == True:
                VOTE = Button(self.screen, 'You Have Voted', 'arial', 35, 50, 880, (255,0,0), False, False)
            
            TOTAL_VOTES = Button(self.screen, f'Total Votes: {self.server.voters}', 'arial', 35, 50, 980, (255,0,0), False, False)

            if self.server.winner_name != '':
                WINNER_NAME = Button(self.screen, f'{self.server.winner_name} won the last game', 'arial', 50, self.WIDTH/2, 200, (0,255,0), False, True)

            pygame.display.update()

            if self.server.started == True:
                self.game()
                voted = False

    def main_menu(self):
        join = False

        lob = pygame.image.load('lobby.png')

        while join == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        sys.exit()

            self.screen.fill((0,0,0))
            self.screen.blit(lob, (0,0))


            MAIN = Button(self.screen, 'Main Menu', 'arial', 35, self.WIDTH/2, 400, (255,255,255), False, True)
            WELCOME = Button(self.screen, f'Welcome {self.name}', 'arial', 35, 0, 0, (255,255,255), False, False)
            JOIN = Button(self.screen, 'Join', 'arial', 80, self.WIDTH/2, self.HEIGHT/2, (255,255,255), False, True)
            clicked = JOIN.hover()

            if clicked == True:
                self.server = self.network.send('Spoons')
                self.lobby()
            if clicked == False:
                self.network.send_only('None')

            pygame.display.update()


    # Decides if person is elgible to win
    def check_winner(self):
        Card1 = self.server.hand[self.name]['Hand'][0].split('_')
        Card2 = self.server.hand[self.name]['Hand'][1].split('_')
        Card3 = self.server.hand[self.name]['Hand'][2].split('_')
        Card4 = self.server.hand[self.name]['Hand'][3].split('_')

        if (Card1[0] == Card2[0]) and (Card1[0] == Card3[0]) and (Card1[0] == Card4[0]):
            WINNER = Button(self.screen, 'Winner', 'arial', 60, self.WIDTH/2, 730, (0,255,0), False, True)
            if WINNER.hover() == True:
                self.network.send('Winner')
