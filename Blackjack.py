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
            self.cards = json.load(json_file) # Imports all card names
        self.players = {} # Contains the names of all the players and ids that are joining
        self.points = {'Dealer': [0]} # Contains all the names and points for each individual person
        self.hand = {} # Contains the hand of each person that is playing
        self.started = False # Boolean for whether the game has starated or not
        self.votes = {} # Contains players names and whether they have voted to start the game or not yet
        self.voters = 0 # How many people have voted to start the game
        self.order = [] # Contains the order of who is going to go
        self.over = False # Boolean to decide whether the game should end or not
        self.winner_name = '' # Name of the person who won last
        self.hand.update({'Dealer':[]}) # Adds the dealer to the hand dictionary since the dealer is the server
        self.points.update({'Dealer':[0]}) # Adds the Dealer to the points dictionary since the dealer is the server
        self.turn = 0 # Value to determine whos turn it is
        self.round = 1 # Value to determine the round of the game
        self.stands = 0 # How many people have stood in the game
        self.dealer_play = False # Has the dealer played
        self.dealer_display_points = 0 # The points that will be displayed on screen for the dealer

    def init_deal(self):
        # Goes through all the players and adds a random card from the deck to create their hand
        for i, j in enumerate(self.hand):
            for k in range(0,2):
                r = random.randint(0, len(self.cards['Cards']) - 1) # Creates a random integer
                self.hand[j].append(self.cards['Cards'][r]) # Adds the random card to the deck
                self.cards['Cards'].pop(r) # Removes the card from the deck
        print(self.hand)
        print('Dealt Cards')

    def deal(self, Name):
        # Deals a card to the player that has requested to be dealt
        r = random.randint(0, len(self.cards['Cards']) - 1) # Gnerages a random number
        print(r)
        self.hand[Name].append(self.cards['Cards'][r]) # Adds the random card to the deck
        print(f"{Name} was dealt {self.cards['Cards'][r]}") # Prints in console of the server what card was given to who
        self.cards['Cards'].pop(r) # Removes the card from the deck
        self.check_points() # Checks points of every player

    def stand(self,Name):
        self.check_points() # Checks points of every player
        self.change_turn() # CHanges the turn of the player

    def add_player(self, Name, playerid):
        # Ran when a new player joins the game
        self.players.update({Name:[playerid, False]}) # Adds name to the list of players
        self.points.update({Name:[0]}) # Adds the player to the points list
        self.hand.update({Name:[]}) # Adds player to the list of hands for the game
        self.votes.update({Name: [False]}) # Adds player to voting dictionary
        self.order.append(Name) # Adds them to the order list
        host = False # Identifies that they are not the host of the game
        for i, j in enumerate(self.players):
            # Determines if there is already a host
            if self.players[j][1] == True:
                host = True
        if host == False:
            # Makes player host if there is no host
            self.players[Name][1] = True

    def remove_player(self, Name):
        new_host = False
        temp = []
        try:
            if self.players[Name][1] == True:
                new_host = True
            del self.players[Name]
            del self.points[Name]
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
        
    def end_game(self):
        print(self.order)
        print('Ending Game')
        print(self.points['Dealer'][0])
        for i, j in enumerate(self.hand):
            for k in range(0, len(self.hand[j])):
                self.cards['Cards'].append(self.hand[j][0])
                self.hand[j].pop(0)
        for i, j in enumerate(self.votes):
            self.votes[j][0] = False
        self.started = False
        self.voters = 0
        self.round = 1
        self.turn = 0
        self.dealer_play = False
        print('Game Ended')
        print(len(self.cards['Cards']))
        print(self.hand)
        return self.started

    def start_game(self):
        self.started = True
        self.init_deal()
        self.over = False
        self.winner_name = ''
        self.round = 1
        print('\n\n\n\nStarting Game')
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
            print('Empty Lobby')
            self.end_game()

    def change_turn(self):
        self.player_length = len(self.order) - 1
        if self.turn == self.player_length:
            self.round += 1
            self.stands = 0
            self.turn = 0
            print(f'Round Changed to {self.round}')
        else:
            turn += 1

        if self.round == 2 and self.dealer_play == False:
            self.play_dealer()
        elif self.round == 4:
            self.over = True
            self.end_game()

    def check_points(self):
        for i, j in enumerate(self.points):
            number = False
            count_low = 0
            count_high = 0
            Ace = False
            check = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
            for k in self.hand[j]:
                count_add = k.split('_')
                for l in check:
                    if count_add[0] == l:
                        add = int(count_add[0])
                        count_low += add
                        count_high += add
                        break
                
                if count_add[0] == 'king' or count_add[0] == 'queen' or count_add[0] == 'jack':
                    count_low += 10
                    count_high += 10
                elif count_add[0] == 'ace':
                    if Ace == False:
                        count_low += 1
                        count_high += 11
                        Ace = True
                    elif Ace == True:
                        count_low += 1
                        count_high += 1
            diff1 = 21 - count_low
            diff2 = 21 - count_high

            if diff1 <= diff2 and diff1 >= 0:
                self.points[j][0] = count_low
            elif diff2 <= diff1 and diff2 >= 0:
                self.points[j][0] = count_high
            elif diff1 < 0 and diff2 < 0:
                self.points[j][0] = 'Over 21'
            elif diff1 < 0 and diff2 >= 0:
                self.points[j][0] = count_high
            elif diff2 < 0 and diff1 >= 0:
                self.points[j][0] = count_low
            else:
                print('Stats')
                print(diff1)
                print(diff2)
                print(count_low)
                print(count_high)
                print()
                print()
                print()
                print()

                self.points[j][0] = 'Error'

            if self.started == True:
                if self.round != 1:
                    # print('setting display points 1')
                    self.dealer_display_points = self.points['Dealer'][0]
                else:
                    # print('setting display points 2')
                    dealer_add = self.hand['Dealer'][0].split('_')[0]
                    # print(dealer_add)
                    for i in check:
                        if dealer_add == i:
                            self.dealer_display_points = int(dealer_add)

                    if dealer_add == 'king' or dealer_add == 'queen' or dealer_add == 'jack':
                        self.dealer_display_points = 10
                    elif dealer_add == 'ace':
                        self.dealer_display_points = 11
                        
    def play_dealer(self):
        if self.started == True:
            print('Dealer Playing')
            while True:
                if self.points['Dealer'][0] == 'Over 21' or self.points['Dealer'][0] >= 17:
                    break
                else:
                    print('Dealing Dealer')
                    self.deal('Dealer')

                self.check_points()
            self.dealer_play = True
            print('Dealer Standing')
            self.stand('Dealer')
            self.winners()

    def winners(self):
        winner_num = 0
        for i, j in enumerate(self.points):
            if i == 0:
                if self.points[j][0] == 'Over 21':
                    for k, l in enumerate(self.players):
                        if k == 0:
                            self.winner_name += l
                        else:
                            self.winner_name += f', {l}'
                        self.winner_name
                    winner_num += 1
                    break
                continue
            if self.points[j][0] != 'Over 21':
                if self.points[j][0] >= self.points['Dealer'][0]:
                    if winner_num == 0:
                        self.winner_name += j
                        winner_num += 1
                    else:
                        self.winner_name += f', {j}'
        if winner_num == 0:
            self.winner_name = 'None'
        # self.over = True
        # self.end_game()
        
        


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
        self.voted = False
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

            if self.voted == False:
                VOTE = Button(self.screen, 'Vote to Start Game', 'arial', 35, 50, 880, (0,255,0), False, False)
                clicked = VOTE.hover()
                if clicked == True:
                    self.network.send('voted')
                    self.voted = True
            elif self.voted == True:
                VOTE = Button(self.screen, 'You Have Voted', 'arial', 35, 50, 880, (255,0,0), False, False)
            
            TOTAL_VOTES = Button(self.screen, f'Total Votes: {self.server.voters}', 'arial', 35, 50, 980, (255,0,0), False, False)

            if self.server.winner_name == '':
                pass
            elif self.server.winner_name == 'None':
                WINNER_NAME = Button(self.screen, f'Winner(s): {self.server.winner_name}', 'arial', 50, self.WIDTH/2, 200, (255,0,0), False, True)
            else:
                WINNER_NAME = Button(self.screen, f'Winner(s): {self.server.winner_name}', 'arial', 50, self.WIDTH/2, 200, (0,255,0), False, True)

            pygame.display.update()

            if self.server.started == True:
                self.game()
                self.voted = False

    def game(self):
        self.voted = False
        self.Stand = False

        counter = 0

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
                
            # Resets screen
            self.screen.fill((0,0,0))
            self.screen.blit(background, (0,0))

            # Creates and draws cards that the player holds
            
            try:
                # There should always be an initial card
                CARD1 = Card(self.screen, self.server.hand[self.name][0], .5, 105, 680)

                try:
                    CARD2 = Card(self.screen, self.server.hand[self.name][1], .5, 470, 680)
                except:
                    pass
                try:
                    CARD3 = Card(self.screen, self.server.hand[self.name][2], .5, 835, 680)
                except:
                    pass
                try:
                    CARD4 = Card(self.screen, self.server.hand[self.name][3], .5, 1200, 680)
                except:
                    pass
                try:
                    CARD5 = Card(self.screen, self.server.hand[self.name][4], .5, 1565, 680)
                except:
                    pass
            except:
                print('Error at printing cards')


            # Shows the dealer first card and second card
            try:
                # There should always be an initial card
                # Should start at 617.5
                CARD1_DEALER = Card(self.screen, self.server.hand['Dealer'][0], .25, 617, 170)

                try:
                    if self.server.round < 3:
                        CARD2_DEALER = Button(self.screen, '?', 'arial', 90, 819.5, 260.75, (255, 255, 255), True, False)
                    else:
                        CARD2_DEALER = Card(self.screen, self.server.hand['Dealer'][1], .25, 757, 170)
                except:
                    pass
                try:
                    CARD3_DEALER = Card(self.screen, self.server.hand['Dealer'][2], .25, 897, 170)
                except:
                    pass
                try:
                    CARD4_DEALER = Card(self.screen, self.server.hand['Dealer'][3], .25, 1037, 170)
                except:
                    pass
                try:
                    CARD5_DEALER = Card(self.screen, self.server.hand['Dealer'][4], .25, 1177, 170)
                except:
                    pass
            except:
                print('Error at printing cards')
            try:
                WAITING = Card(self.screen, self.server.hand[self.name]['Waiting'][0], 1570, 100)
            except:
                WAITING = False

            # Playable Buttons
            if self.Stand == False:
                HIT = Button(self.screen, 'Hit', 'arial', 90, 150, 150, (255,255,255), False, False)
                self.STAND = Button(self.screen, 'Stand', 'arial', 90, (200 + HIT.render_width), 150, (255, 255, 255), False, False)

            # Shows the calculated amount of points that you have at the moment
            POINTS = Button(self.screen, f'Points: {self.server.points[self.name][0]}', 'arial', 90, 105, (680 - (self.STAND.render_height + 50)), (255, 255, 255), False, False)
            DEALER_POINTS = Button(self.screen, f'Points: {self.server.dealer_display_points}', 'arial', 50, self.WIDTH/2, 400, (0, 0, 255), False, True)

            if self.server.points[self.name][0] == 'Over 21':
                self.Stand = True

            # Draws the Hit or Stand Buttons to Hit
            if self.Stand == False and self.server.turn == self.server.order.index(self.name):
                if HIT.hover() == True and self.name == self.server.order[self.server.turn] and WAIT == 100 and self.Stand == False:
                    self.network.send('Hit')
                    WAIT = 0
                if self.STAND.hover() == True and self.name == self.server.order[self.server.turn] and WAIT == 100:
                    self.network.send('Stand')
                    self.Stand = True
                    WAIT = 0
            elif self.Stand == True:
                self.network.send('Stand')

            # Tells you if it is your turn
            if self.server.turn == self.server.order.index(self.name):
                TURN = Button(self.screen, 'It is your turn', 'arial', 90, self.WIDTH/2, 100, (0, 255, 0), False, True)
            elif self.Stand == True:
                TURN = Button(self.screen, 'Your are standing', 'arial', 90, self.WIDTH/2, 100, (0,0,255), False, True)
            else:
                current_turn = self.server.order[self.server.turn]
                TURN = Button(self.screen, f'It is {current_turn}\'s turn', 'arial', 90, self.WIDTH/2, 100, (255, 0, 0), False, True)

            
            # Shows players that are in the lobby
            player_y = 100
            for i, j in enumerate(self.server.players):
                PLAYER = Button(self.screen, j, 'arial', 60, 1500, player_y, (255,255,255), False, False)
                player_y += PLAYER.render_height + 250

            # self.check_winner()

            if WAIT < 100:
                WAIT += 5

            
            if self.server.over == True:
                time.sleep(3)
                print('End Game')
                break

            pygame.display.update()



    # Decides if person is elgible to win
    def check_winner(self):
        Card1 = self.server.hand[self.name][0].split('_')
        try:
            Card2 = self.server.hand[self.name][1].split('_')
        except:
            pass
        try:
            Card3 = self.server.hand[self.name][2].split('_')
        except:
            pass
        try:
            Card4 = self.server.hand[self.name][3].split('_')
        except:
            pass
        try:
            Card5 = self.server.hand[self.name][4].split('_')
        except:
            pass

        if (Card1[0] == Card2[0]) and (Card1[0] == Card3[0]) and (Card1[0] == Card4[0]):
            WINNER = Button(self.screen, 'Winner', 'arial', 60, self.WIDTH/2, 730, (0,255,0), False, True)
            if WINNER.hover() == True:
                self.network.send('Winner')