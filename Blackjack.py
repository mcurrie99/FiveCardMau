import pygame
import sys
import random
import json
import random
import time
from pygame import mixer
from Network import Network
from Buttons import *


class Blackjacks:
    '''
    Server side of Blackjack
    '''
    def __init__(self, id):
        with open('Cards.json') as json_file:
            self.cards = json.load(json_file)
        self.players = {}
        self.hand = {}
        self.started = False
        self.votes = {}
        self.voters = 0
        self.order = []
        self.winner = False
        self.winner_name = ''
        self.hand.update({'Dealer':[]})
        self.turn = 0


    def init_deal(self):
        for i, j in enumerate(self.hand):
            for k in range(0,4):
                r = random.randint(0, len(self.cards['Cards']) - 1)
                print(r)
                self.hand[j].append(self.cards['Cards'][r])
                self.cards['Cards'].pop(r)
        print(self.hand)
        print('Dealt Cards')

    def deal(self, Name):
            r = random.randint(0, len(self.cards['Cards']) - 1)
            self.hand[Name].append(self.cards['Cards'][r])
            self.cards['Cards'].pop(r)


    def add_player(self, Name, playerid):
        self.players.update({Name:[playerid, False]})
        self.hand.update({Name:[]})
        self.votes.update({Name: [False]})
        self.order.append(Name)
        host = False
        for i, j in enumerate(self.players):
            if self.players[j][1] == True:
                host = True
        if host == False:
            self.players[Name][1] = True

    def remove_player(self, Name):
        new_host = False
        temp = []
        try:
            if self.players[Name][1] == True:
                new_host = True
            del self.players[Name]
            if self.votes[Name][0] == True:
                self.voters -=  1
            del self.votes[Name]
            self.order.remove(Name)
            if self.started == True:
                try:
                    for i in self.hand[Name]:
                        temp.append(i)
                    for i in temp:
                        self.cards['Cards'].append(i)
                    del self.hand[Name]
                    self.empty_lobby()
                except:
                    pass
            elif self.started == False:
                self.check_votes()

            if new_host == True:
                self.find_new_host()
            for i in range(0, len(temp)):
                temp.pop(0)
            print(f'{Name} was removed from the game')
        except:
            print(f'Could not delete player: {Name}')

    def find_new_host(self):
        try:
            if len(self.players > 1):
                for i, j in enumerate(self.players):
                    if self.players[j][1] == False:
                        self.players[j][1] = True
                        break
            else:
                pass
        except:
            # return game back preparing state
            pass

    def change_winner(self, name):
        print('changing winner')
        self.winner = True
        self.winner_name = name
        self.end_game()
        
    
    def end_game(self):
        print('Ending Game')
        for i, j in enumerate(self.hand):
            for k in range(0, len(self.hand[j])):
                self.cards['Cards'].append(self.hand[j][0])
                self.hand[j].pop(0)
        for i, j in enumerate(self.votes):
            self.votes[j][0] = False
        self.started = False
        self.voters = 0
        print('Game Ended')
        return self.started

    def start_game(self):
        self.started = True
        self.init_deal()
        self.winner = False
        print('Starting Game')
        return self.started

    def vote(self, Name):
        self.votes[Name][0] = True
        print(f'{Name} has voted')
        self.check_votes()

    def get_host_name(self):
        for i, j in enumerate(self.players):
            if self.players[j][1] == True:
                return j

    def check_votes(self):
        self.voters = 0
        if len(self.players) > 0:
            for i, j in enumerate(self.votes):
                if self.votes[j][0] == True:
                    self.voters += 1
        else:
            self.empty_lobby()
        if self.voters == len(self.votes) and self.voters > 0:
            self.start_game()

    def empty_lobby(self):
        if len(self.players) == 0 and self.started == True:
            self.end_game()


class Blackjack:
    '''
    Client side of Blackjack
    screen, network, name, WIDTH, HEIGHT
    voted to be the next game that is used
    '''
    def __init__(self, screen, network, name, WIDTH, HEIGHT):
        self.screen = screen
        self.network = network
        self.name = name
        self. WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.game_over = False

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
                player_y += PLAYER.render_height + 50

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
                # There should always be an initial card
                CARD1 = Card(self.screen, self.server.hand[self.name][0], 105, 680)

                try:
                    CARD2 = Card(self.screen, self.server.hand[self.name][1], 470, 680)
                except:
                    pass
                try:
                    CARD3 = Card(self.screen, self.server.hand[self.name][2], 835, 680)
                except:
                    pass
                try:
                    CARD4 = Card(self.screen, self.server.hand[self.name][3], 1200, 680)
                except:
                    pass
                try:
                    CARD5 = Card(self.screen, self.server.hand[self.name][4], 1565, 650)
                except:
                    pass
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
                player_y += PLAYER.render_height + 250

            self.check_winner()

            if WAIT < 100:
                WAIT += 5

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
    