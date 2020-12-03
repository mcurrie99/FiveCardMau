import pygame
import sys
import random
import json
import random
import time
from pygame import mixer
from Network import Network
from Buttons import *
    

class Spoons:
    '''
    Server side of Spoons
    '''
    def __init__(self, id):
        with open('Cards.json') as json_file:
            self.cards = json.load(json_file)# Imports all card names
        self.players = {} # Contains the names of all the players and ids that are joining
        self.hand = {} # Contains the hand of each person that is playing
        self.started = False # Boolean for whether the game has starated or not
        self.votes = {} # Contains players names and whether they have voted to start the game or not yet
        self.voters = 0 # How many people have voted to start the game
        self.order = [] # Contains the order of who is going to go
        self.winner = False # Boolean to decide whether the game should end or not
        self.winner_name = '' # Name of the person who won last

    def deal(self):
        for i, j in enumerate(self.hand):
            for k in range(0,4):
                r = random.randint(0, len(self.cards['Cards']) - 1) # Creates a random integer
                self.hand[j]['Hand'].append(self.cards['Cards'][r]) # Adds the random card to the deck
                self.cards['Cards'].pop(r) # Removes the card from the deck
        self.rotate_cards() # Calls to give a card to person first in turn
        print(self.hand) # Prints the hand dictionary
        print('Dealt Cards') # Prins that all the cards have been dealt

    def rotate_cards(self):
        # Gives a card to the first person in order
        if len(self.hand[self.order[0]]['Waiting']) == 0: # Runs if the player does not have another card waiting
            r = random.randint(0, len(self.cards['Cards']) - 1) # Creates a random integer
            self.hand[self.order[0]]['Waiting'].append(self.cards['Cards'][r]) # Adds the random card to the deck
            self.cards['Cards'].pop(r) # Removes the card from the deck


    def add_player(self, Name, playerid):
        # Ran when a new player joins the game
        self.players.update({Name:[playerid, False]}) # Adds name to the list of players
        self.hand.update({Name:{'Hand':[],'Waiting':[]}}) # Adds player to the list of hands for the game
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
        # Removes a player from the game variables
        new_host = False # Initializes a temporary variable to need to new host
        temp = [] # Initializes list that will be used to transfer cards back to deck
        try:
            if self.players[Name][1] == True: # Checks if the player is the host
                new_host = True # Sets variable to true so computer knows to find new host
            del self.players[Name] # Deletes player from player list
            if self.votes[Name][0] == True: # Checks if the person is true
                self.voters -=  1 # Removes a total vote if the person has voted
            del self.votes[Name] # Deletes players name from the vote dictionary
            self.order.remove(Name) # Removes the name from the order list
            if self.started == True: # Proccesses that only will be done if the game has started
                try:  # Won't always work so this makes sure the game does not crash
                    for i in self.hand[Name]['Hand']: # Runs through the entire hand of the player
                        temp.append(i) # Appends the had to the temporary list
                    for i in self.hand[Name]['Waiting']: # Runs through the entire hand of the player
                        temp.append(i) # Appends the had to the temporary list
                    for i in temp: # Runs through all the cards in the temporary list
                        self.cards['Cards'].append(i) # Adds the card back to the deck
                    del self.hand[Name] # Deletes the player from the hand and his characters
                    self.empty_lobby() # Checks to see if the lobby's empty
                except:
                    pass
            elif self.started == False: # Only runs the processes if the game has not started
                self.check_votes() # Checks how many people have voted to start the game
            if new_host == True: # If the game needs to find a new host
                self.find_new_host() # Calls function to start a new host
            for i in range(0, len(temp)): # Runs through the temporary list, will not run if empty
                temp.pop(0) # Removes the first element of the list
            print(f'{Name} was removed from the game') # Prints to the server console that the player has been removed
        except:
            print(f'Could not delete player: {Name}') # Prints to the server console that the game could not remove the player

    def find_new_host(self):
        # Function to find new host
        try: # Prevents server from crashing
            if len(self.players) > 0: # Only runs if there is more than 1 person in the lobby
                for i, j in enumerate(self.players): # Runs through the players in the player dictionary
                    if self.players[j][1] == False: # The first person that the server finds in the dictionary that's not host
                        self.players[j][1] = True # Sets the person to be the host of the game
                        break # Ends the for loop so no one else becomes the host of the game
            else:
                pass
        except:
            # return game back preparing state
            pass

    def change_winner(self, name):
        print(f'Changing winner to {name}') # Prints to the server console the winner's name
        self.winner = True # Tells the game that there is a winner
        self.winner_name = name # Sets the winners name
        self.end_game() # Calls to end the game
        
    
    def end_game(self):
        # Ends the game when someone has won or there is no one in the game
        print('Ending Game') # Print the order of the game
        for i, j in enumerate(self.hand): # Runs through the players in the hand dictionary if there are any
            for k in range(0, len(self.hand[j]['Hand'])):  # Runs through the hand of each player
                self.cards['Cards'].append(self.hand[j]['Hand'][0]) # Adds the card back to the deck
                self.hand[j]['Hand'].pop(0) # Removes the card from the players deck
            try:
                for k in range(0, len(self.hand[j]['Waiting'])):  # Runs through the hand of each player
                    self.cards['Cards'].append(self.hand[j]['Waiting'][0]) # Adds the card back to the deck
                    self.hand[j]['Waiting'].pop(0) # Removes the card from the players deck
            except:
                print('No Cards Waiting or Error') # Prints to the server console that the player had no waiting cards
        for i, j in enumerate(self.votes): # Runs through the players in the vote dictionary
            self.votes[j][0] = False # Sets each players vote to be False so that they can vote again
        self.started = False # Has stated that game is not running and should not be started
        self.voters = 0 # Sets the game to have 0 votes
        print('Game Ended') # Prints to the server console that the game has not ended
        return self.started # Returns that the game should not be started

    def start_game(self):
        # Starts the game
        if len(self.order) > 1: # If the length of order is greater than 1
            random.shuffle(self.order) # Shuffles the order of the players so it changed
        self.started = True # Sets the game to be started
        self.deal() # Initializes the deals
        self.winner = False # The game is set to not end
        print('\n\n\n\nStarting Game') # Prints to the server console that the game is starting
        return self.started # Returns that the game has started

    def vote(self, Name):
        # Ran when a player has voted to start the game
        self.votes[Name][0] = True # Tells the game that the player hs voted
        print(f'{Name} has voted') # Prints on the server console that the palyer has voted
        self.check_votes() # Checks who and how many people have voted

    def get_host_name(self):
        # Gets the host name
        for i, j in enumerate(self.players): # Runs through the players dictionary
            if self.players[j][1] == True: # If the person is the host
                return j # Returns the players name

    def check_votes(self):
        # Checks who and how many people have voted
        self.voters = 0 # Initializes the vote count at 0
        if len(self.players) > 0: # If the length of players is greater than 0
            for i, j in enumerate(self.votes): # Runs through all the votes
                if self.votes[j][0] == True: # If the specific player has voted the process is ran
                    self.voters += 1 # The total vote counted is added to by 1
        else:
            self.empty_lobby() # If the lobby is empty the proccess is ran
        if self.voters == len(self.votes) and self.voters > 1: # Runs if there are more than 0 people in the lobby and everyone has voted
            self.start_game() # The game is started

    def empty_lobby(self):
        # Checks if the loby is empty
        if len(self.players) == 0 and self.started == True: # Runs if there is no one in the lobby and the game has started
            self.end_game() # Prints to the server console that the lobby is empty
        elif len(self.players) == 0 and self.started == False: # Runs if there is one in the lobby and the game hasn't started
            self.winner_name == '' # Set there to be no winner

    def change_hand(self, name, new_wait, new_hand):
        # Changes the player's hands
        if new_wait != 'Pass': # Runs if the cards is not being passed
            spot_hand = self.hand[name]['Hand'].index(new_wait) # Finds the index of the card in the deck
            spot_wait = self.hand[name]['Waiting'].index(new_hand) # Finds the index of hte card in the deck
            self.hand[name]['Waiting'][spot_wait] = new_wait # Swaps out the waiting card
            self.hand[name]['Hand'][spot_hand] = new_hand # Swaps out the card in the hand
        else: # Runs in the person has passed
            self.hand[name]['Waiting'].remove(new_hand) # Removes the card from the player's waiting hand
            on_deck = self.order.index(name) # Gets the position that the player is in
            on_deck += 1 # Adds one to get index of person taht is up next
            try: # Will work if there is a player that comes enext
                on_deck_person = self.order[on_deck] # Gets name of person that is up next
                self.hand[on_deck_person]['Waiting'].append(new_hand) # Appends the card to their waiting deck
                print('Transferred to next player') # Prints to the server console that a card has been passed
            except: # Will run if the player is last in order
                self.cards['Cards'].append(new_hand) # Adds the card back to the deck
                # print('Added to Deck')
        if self.order.index(name) == 0: # Runs if the person if the person is first in line
            self.rotate_cards() # Calls for a new card to go to first players

class Spoon:    
    '''
    Spoons game that will be supported
    Hopefully the first of modular parts of the game
    screen, network, name, WIDTH, HEIGHT
    '''
    def __init__(self, screen, network, name, WIDTH, HEIGHT):
        # Initializes game renderer 
        self.screen = screen # Sets window to use
        self.network = network # Sets the network object to use
        self.name = name # Sets the name of the player
        self.WIDTH = WIDTH # Sets the Width of the window
        self.HEIGHT = HEIGHT # Sets the Height to the window
        self.game_over = False # Sets the game to not be over

    def lobby(self):
        global close_game # Makes close_game a global variable
        gamer = False # Sets gamer to be False
        close_game = True # Sets close_game to True so that the game closes when the game is exited
        self.voted = False # Sets if the player has voted to false 
        lob = pygame.image.load('background.png') # Loads in the background texture
        # game_over = True
        # network.change_hand('this', 'works')
        while gamer == False: # Sets up a while loop for game
            self.server = self.network.get_game() # Requests and get the game data
            player_y = 0 # Pixel location for where to render names
            for event in pygame.event.get(): # Reads for inputs from user
                if event.type == pygame.QUIT: # Runs if input is to hit the exit button
                    sys.exit() # Quits the game

                if event.type == pygame.KEYDOWN: # Runs if the input is a keyboard press
                    if event.key == pygame.K_q: # Runs if the input is the press of the q button
                        sys.exit() # Exits the game
            self.screen.fill((0,0,0)) # Fills the background of the game with black
            self.screen.blit(lob, (0,0)) # Renders the lobby texture onto the screen

            LOBBY = Button(self.screen, 'Lobby', 'arial', 35, 0, 0, (255,255,255), False, False) # Rends the text that says "Lobby"
            for i, j in enumerate(self.server.players): # Runs through the players of the game
                PLAYER = Button(self.screen, j, 'arial', 40, 1500, player_y, (255,255,255), False, False) # Renders in the players name as text onto screen
                player_y += PLAYER.render_height + 50 # Adds 50 to the pixel location of the person

            if self.voted == False: # Runs if the person has voted
                VOTE = Button(self.screen, 'Vote to Start Game', 'arial', 35, 50, 880, (0,255,0), False, False) # Renders in a button to vote
                clicked = VOTE.hover() # Checks if the player has clicked to vote
                if clicked == True: # If the person has clicked
                    self.network.send('voted') # Sends the information to the server that the player has voted
                    self.voted = True # Tell the user's computer that the user has voted
            elif self.voted == True: # Runs if the player has voted
                VOTE = Button(self.screen, 'You Have Voted', 'arial', 35, 50, 880, (255,0,0), False, False) # Renders in a vote button that says you have voted
            
            TOTAL_VOTES = Button(self.screen, f'Total Votes: {self.server.voters}', 'arial', 35, 50, 980, (255,0,0), False, False) # Renders in text of how many people have voted

            if self.server.winner_name != '': # Runs if there are winners
                WINNER_NAME = Button(self.screen, f'{self.server.winner_name} won the last game', 'arial', 50, self.WIDTH/2, 200, (0,255,0), False, True) # Renders the winner of the last game

            pygame.display.update() # Updates the game display with the new frame

            if self.server.started == True: # Runs if the game has started
                self.game() # Starts the game rendering
                self.voted = False # Sets the user's voting status back to false

    def game(self):
        # Runs the game rendering
        self.voted = False # Sets voting status to False

        #Background
        background = pygame.image.load('background.png') # Loads in the background texture

        WAIT = 0 # Initializes variable for how long for game to wait in between clicks
        # Game
        while not self.game_over: # While loop to run game
            for event in pygame.event.get(): # Reads for inputs from user
                if event.type == pygame.QUIT: # Runs if input is to hit the exit button
                    sys.exit() # Quits the game

                if event.type == pygame.KEYDOWN: # Runs if the input is a keyboard press
                    if event.key == pygame.K_q: # Runs if the input is the press of the q button
                        sys.exit() # Exits the game
            self.server = self.network.get_game() # Requests and gets game data from server
            if self.server.winner == True:
                break
            # Resets screen
            self.screen.fill((0,0,0)) # Renders in a black screen
            self.screen.blit(background, (0,0)) # Renders in the background

            # Creates and draws cards that the player holds
            
            try: # Tries rendering in the cards
                CARD1 = Card(self.screen, self.server.hand[self.name]['Hand'][0], .5, 100, 680)
                CARD2 = Card(self.screen, self.server.hand[self.name]['Hand'][1], .5, 590, 680)
                CARD3 = Card(self.screen, self.server.hand[self.name]['Hand'][2], .5, 1080, 680)
                CARD4 = Card(self.screen, self.server.hand[self.name]['Hand'][3], .5, 1570, 680)
            except:
                print('Error at printing cards') # Prints in player's console that the cards has failed to render
            try: # Tries rendering in the cards
                WAITING = Card(self.screen, self.server.hand[self.name]['Waiting'][0], .5,  1570, 100)
            except:
                print('Error printing Card') # Prints in player's console that the cards has failed to render
                WAITING = False # There is no waiting card

            PASS = Button(self.screen, 'Pass', 'arial', 90, 150, 150, (255,255,255), False, False) # Reenders in a pass button

            # Draws square under the card the player is hovering over and sends data to server if clicked
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

            
            # Shows players that are in the lobby
            player_y = 100
            for i, j in enumerate(self.server.players): # Runs through players names
                PLAYER = Button(self.screen, j, 'arial', 60, 960, player_y, (255,255,255), False, True) # Renders in players text name
                player_y += PLAYER.render_height + 50 # Adds 50 pixles after name is rendered

            self.check_winner() # Checks to see if you are winning

            if WAIT < 100: # Run's if the click count is less than 100
                WAIT += 10 # Adds 5 to the WAIT variable

            pygame.display.update() # Shows the new rendered frame in the window

    


    # Decides if person is elgible to win
    def check_winner(self):
        # Checks if player can win

        # Grabs the first term of every card in the player's hand
        Card1 = self.server.hand[self.name]['Hand'][0].split('_')
        Card2 = self.server.hand[self.name]['Hand'][1].split('_')
        Card3 = self.server.hand[self.name]['Hand'][2].split('_')
        Card4 = self.server.hand[self.name]['Hand'][3].split('_')

        if (Card1[0] == Card2[0]) and (Card1[0] == Card3[0]) and (Card1[0] == Card4[0]): # If are the cards are equal to each other
            WINNER = Button(self.screen, 'Press to Win', 'arial', 60, self.WIDTH/2, 730, (0,255,0), False, True) # ALlows player to click button to win
            if WINNER.hover() == True: # See if the person clicks it
                self.network.send('Winner') # Tells the server that the player has one
