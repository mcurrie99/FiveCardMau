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
    gameID = 0

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
        
        self.gameID += 1 # LOOK INTO THIS FOR THE SUMMER

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
        # Removes a player from the game variables
        new_host = False # Initializes a temporary variable to need to new host
        temp = [] # Initializes list that will be used to transfer cards back to deck
        try:
            if self.players[Name][1] == True: # Checks if the player is the host
                new_host = True # Sets variable to true so computer knows to find new host
            del self.players[Name] # Deletes player from player list
            del self.points[Name] # Deletes player from points list
            if self.votes[Name][0] == True: # Checks if the person is true
                self.voters -=  1 # Removes a total vote if the person has voted
            del self.votes[Name] # Deletes players name from the vote dictionary
            self.order.remove(Name) # Removes the name from the order list
            if self.started == True: # Proccesses that only will be done if the game has started
                try:  # Won't always work so this makes sure the game does not crash
                    for i in self.hand[Name]: # Runs through the entire hand of the player
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
                pass # Otherwise pass and do nothing
        except:
            # return game back preparing state
            pass
        
    def end_game(self):
        # Ends the game when someone has won or there is no one in the game
        print(self.order) # Print the order of the game
        print('Ending Game') # Prints to the server console that the game is ending
        print(self.points['Dealer'][0]) # Prints to the server console the points that the Dealer had
        for i, j in enumerate(self.hand): # Runs through the players in the hand dictionary if there are any
            for k in range(0, len(self.hand[j])):  # Runs through the hand of each player
                self.cards['Cards'].append(self.hand[j][0]) # Adds the card back to the deck
                self.hand[j].pop(0) # Removes the card from the players deck
        for i, j in enumerate(self.votes): # Runs through the players in the vote dictionary
            self.votes[j][0] = False # Sets each players vote to be False so that they can vote again
        self.started = False # Has stated that game is not running and should not be started
        self.voters = 0 # Sets the game to have 0 votes
        self.round = 1 # Changes the round of the game back to 1
        self.turn = 0 # Changes the turn of which player back to 0
        self.dealer_play = False # Changes the variable so that game knows that the Dealer has not gone
        print('Game Ended') # Prints to the server console that the game has not ended
        print(len(self.cards['Cards'])) # Prints to the server console the length of the card deck
        print(self.hand) # Prints to the server console the hand dictionary
        return self.started # Returns that the game should not be started

    def start_game(self):
        # Starts the game
        if len(self.order) > 1: # If the length of order is greater than 1
            random.shuffle(self.order) # Shuffles the order of the players so it changed
        self.started = True # Sets the game to be started
        self.init_deal() # Initializes the deals
        self.over = False # The game is set to not end
        self.winner_name = '' # Chanes the winners name back to nothing
        self.round = 1 # The round is onece again set to one
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
        if self.voters == len(self.votes) and self.voters > 0: # Runs if there are more than 0 people in the lobby and everyone has voted
            self.start_game() # The game is started

    def empty_lobby(self):
        # Checks if the loby is empty
        if len(self.players) == 0 and self.started == True: # Runs if there is no one in the lobby
            print('Empty Lobby') # Prints to the server console that the lobby is empty
            self.end_game() # Ends the game

    def change_turn(self):
        # Changes the turn of the player
        self.player_length = len(self.order) - 1 # Defines index of the last player
        if self.turn == self.player_length: # Runs if the turn is equal to the index of the last player
            self.round += 1 # Adds one to the round length
            self.stands = 0 # Sets the number of stands to 0
            self.turn = 0 # Sets the turn to 0
            print(f'Round Changed to {self.round}') # Prints to the server console what round the game is now
        else: # If the turn is not equal to the index of the last player
            turn += 1 # Adds one to the turn counter

        if self.round == 2 and self.dealer_play == False: # Runs if the round is equal 2 and the dealer has not played
            self.play_dealer() # Has the dealer play
        elif self.round == 4: # If the round is equal to 4
            self.over = True # The game is set to end
            self.end_game() # Ends the game

    def check_points(self):
        # Checks the points of all the players
        for i, j in enumerate(self.points): # Runs through all the players in the points dictionary
            number = False # Is the first term in the card a number is automatically set to False
            count_low = 0 # Low count is initialized to 0
            count_high = 0 # High count is initialized to 0
            Ace = False # Is there an Ace is automatically set to False
            check = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] # Set the terms to be compared to temporarily
            for k in self.hand[j]: # Runs through the hand of the player
                count_add = k.split('_') # Splits the card title by underscores
                for l in check: # Runs through the check list
                    if count_add[0] == l: # Runs if the first term of the split string is equal to the check
                        add = int(count_add[0]) # Converts the number to an integer
                        count_low += add # Adds the number to the high count
                        count_high += add # Adds the number to the low count
                        break # Breaks the current for loop of running through the check list
                
                if count_add[0] == 'king' or count_add[0] == 'queen' or count_add[0] == 'jack': # Checks to see if the term is equal to any of the name cards
                    count_low += 10 # Adds 10 to the high count
                    count_high += 10 # Adds 10 to the low count
                elif count_add[0] == 'ace': # Runs if the first term is an ace
                    if Ace == False: # Runs if there has not already been an ace counted
                        count_low += 1 # Adds 1 to the low count
                        count_high += 11 # Adds 11 to the high count
                        Ace = True # Sets the variable to True so the game knows there is an Ace in the deck
                    elif Ace == True: # Runs if the game has already counted an Ace
                        count_low += 1 # Adds one to the low count
                        count_high += 1 # Adds one to the high count
            diff1 = 21 - count_low # Finds the difference between 21 and the low count
            diff2 = 21 - count_high # Finds the difference between 21 and the high count

            if diff1 <= diff2 and diff1 >= 0: # Runs if the difference 1 is smaller and difference 1 is greater than 0
                self.points[j][0] = count_low # Sets the low count to be points for that person
            elif diff2 <= diff1 and diff2 >= 0: # Runs if the difference 2 is smaller and difference 1 is greater than 0
                self.points[j][0] = count_high # Sets the players points to be the high count
            elif diff1 < 0 and diff2 < 0: # Runs if the difference 1 and 2 are less than 0
                self.points[j][0] = 'Over 21' # Set the players count to be "Over 21"
            elif diff1 < 0 and diff2 >= 0: # Runs if difference 1 is less than 0 and difference 2 is greater than 0
                self.points[j][0] = count_high # Sets the player's points to be the high count
            elif diff2 < 0 and diff1 >= 0: # Runs if difference 2 is less than 0 and difference 1 is greater than 0
                self.points[j][0] = count_low # Sets the player's points to be the low count
            else: # If none of the cases are met
                print('Stats') # Prints "Stats" to the server console
                print(diff1) # Print the first difference
                print(diff2) # Print the second difference
                print(count_low) # Print the low count
                print(count_high) # Print the high count
                print() # Adds a couple of spaces so that the stats can be seen
                print()
                print()
                print()

                self.points[j][0] = 'Error' # Sets the player's points to be "Error" telling the player that there is a problem

            if self.started == True: # Runs if the game has started
                if self.round != 1: # Runs if the round is not 1
                    # print('setting display points 1')
                    self.dealer_display_points = self.points['Dealer'][0] # Displays the total points for the dealer
                else: # If the game is on round 1
                    # print('setting display points 2')
                    dealer_add = self.hand['Dealer'][0].split('_')[0] # Splits the first card of the dealer's hand
                    # print(dealer_add)
                    for i in check: # Runs through the check list variables
                        if dealer_add == i: # If the first term of the card is equal a variable in the checklist
                            self.dealer_display_points = int(dealer_add) # The dealer's display points are equal to 0

                    if dealer_add == 'king' or dealer_add == 'queen' or dealer_add == 'jack': # Runs if the first term corresponds to a name card
                        self.dealer_display_points = 10 # Sets the display points to 10
                    elif dealer_add == 'ace': # Runs if the first term indicates the card is an ace
                        self.dealer_display_points = 11 # Sets the display points to be 11
                        
    def play_dealer(self):
        # Plays the dealer when it is his turn
        if self.started == True: # Runs if the game has started
            print('Dealer Playing') # Prints to the server console that it is playing the dealer
            while True: # Runs a while loop for the dealer
                if self.points['Dealer'][0] == 'Over 21' or self.points['Dealer'][0] >= 17: # Runs if the dealers cards are over 21
                    break # Breaks the while loop
                else:
                    print('Dealing Dealer') # Prints to the server console that the dealer is being dealt a card
                    self.deal('Dealer') # Deals the dealer a card

                self.check_points() # Checks the points of the players
            self.dealer_play = True # Tells the game that the dealer has played
            print('Dealer Standing') # Prints to the server console that the dealer is standing
            self.stand('Dealer') # Tells the game that the Dealer is standing
            self.winners() # Checks the game for winners

    def winners(self):
        winner_num = 0 # Initializes the number of winners to 0
        for i, j in enumerate(self.points): # Runs through all the players points
            if i == 0: # If the index is 0, which is the dealer
                if self.points[j][0] == 'Over 21': # Runs if the Dealers Cards are over 21
                    for k, l in enumerate(self.players): # Runs through the players
                        if k == 0: # Runs if it is the first iteration
                            self.winner_name += l # Adds the players name to the string of winners
                        else: # Runs if it is not the first iteration of the for loop
                            self.winner_name += f', {l}'  # Adds a comma and space before players name for correct grammar
                    winner_num += 1 # Adds 1 the number of winners
                    break # Breaks the for loop running through the points
                continue # Continues to next iteration of the loop
            if self.points[j][0] != 'Over 21': # Runs if the player's points is not over 21
                if self.points[j][0] >= self.points['Dealer'][0]: # Runs if the player's points is greater than the Dealer's points
                    if winner_num == 0: # Runs if the number of winners is 0
                        self.winner_name += j # Adds the players name to the strings of winners
                        winner_num += 1 # Adds 1 to the number of winners
                    else: # If the number of winners is more than 0
                        self.winner_name += f', {j}' # Adds the player's name to the string of winner name with a comma and a space for proper grammar
        if winner_num == 0: # Runs if there are no winners
            self.winner_name = 'None' # Sets the winner name to 0
        # self.over = True
        # self.end_game()
        
        


class Blackjack:
    '''
    Client side of Blackjack
    screen, network, name, WIDTH, HEIGHT
    voted to be the next game that is used
    '''
    def __init__(self, screen, network, name, WIDTH, HEIGHT):
        # Initializes game renderer 
        self.screen = screen # Sets window to use
        self.network = network # Sets the network object to use
        self.name = name # Sets the name of the player
        self. WIDTH = WIDTH # Sets the Width of the window
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

            if self.server.winner_name == '': # Runs if there are no winners
                pass # Does not render any text
            elif self.server.winner_name == 'None': # Runs if there were no winners in the last game
                WINNER_NAME = Button(self.screen, f'Winner(s): {self.server.winner_name}', 'arial', 50, self.WIDTH/2, 200, (255,0,0), False, True) # Renders the winners names in red text
            else:
                WINNER_NAME = Button(self.screen, f'Winner(s): {self.server.winner_name}', 'arial', 50, self.WIDTH/2, 200, (0,255,0), False, True)  # Renders the winners names in green text

            pygame.display.update() # Updates the game display with the new frame

            if self.server.started == True: # Runs if the game has started
                self.game() # Starts the game rendering
                self.voted = False # Sets the user's voting status back to false

    def game(self):
        # Runs the game rendering
        self.voted = False # Sets voting status to False
        self.Stand = False # Sets the Stands Status to False

        counter = 0 # Initializes counter to 0

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
                
            # Resets screen
            self.screen.fill((0,0,0)) # Renders in a black screen
            self.screen.blit(background, (0,0)) # Renders in the background

            # Creates and draws cards that the player holds
            
            try: # Tries rendering in the cards
                # There should always be an initial card
                CARD1 = Card(self.screen, self.server.hand[self.name][0], .5, 105, 680) # Renders in Card 1

                try:
                    CARD2 = Card(self.screen, self.server.hand[self.name][1], .5, 470, 680) # Tries to render in Card 2
                except:
                    pass
                try:
                    CARD3 = Card(self.screen, self.server.hand[self.name][2], .5, 835, 680) # Tries to render in Card 3
                except:
                    pass
                try:
                    CARD4 = Card(self.screen, self.server.hand[self.name][3], .5, 1200, 680) # Tries to render in Card 4
                except:
                    pass
                try:
                    CARD5 = Card(self.screen, self.server.hand[self.name][4], .5, 1565, 680) # Tries to render in Card 5
                except:
                    pass
            except:
                print('Error at printing cards') # Prints in player's console that the cards has failed to render


            # Shows the dealer first card and second card
            try:
                # There should always be an initial card
                # Should start at 617.5
                CARD1_DEALER = Card(self.screen, self.server.hand['Dealer'][0], .25, 617, 170) # Tries to render in Dealer Card 1

                try:
                    if self.server.round < 3: # Runs if the round is less than 3
                        CARD2_DEALER = Button(self.screen, '?', 'arial', 90, 819.5, 260.75, (255, 255, 255), True, False) # Renders in a question mark where the second dealt card is
                    else:
                        CARD2_DEALER = Card(self.screen, self.server.hand['Dealer'][1], .25, 757, 170) # Tries to render in Dealer Card 2
                except:
                    pass
                try:
                    CARD3_DEALER = Card(self.screen, self.server.hand['Dealer'][2], .25, 897, 170) # Tries to render in Dealer Card 3
                except:
                    pass
                try:
                    CARD4_DEALER = Card(self.screen, self.server.hand['Dealer'][3], .25, 1037, 170) # Tries to render in Dealer Card 4
                except:
                    pass
                try:
                    CARD5_DEALER = Card(self.screen, self.server.hand['Dealer'][4], .25, 1177, 170) # Tries to render in Dealer Card 5
                except:
                    pass
            except:
                print('Error at printing cards') # Prints in player's console that the cards has failed to render
            try:
                WAITING = Card(self.screen, self.server.hand[self.name]['Waiting'][0], 1570, 100)
            except:
                WAITING = False

            # Playable Buttons
            if self.Stand == False: # If the player hasn't Stood
                HIT = Button(self.screen, 'Hit', 'arial', 90, 150, 150, (255,255,255), False, False) # Render in Hit button
                self.STAND = Button(self.screen, 'Stand', 'arial', 90, (200 + HIT.render_width), 150, (255, 255, 255), False, False) # Render in Stand button

            # Shows the calculated amount of points that you have at the moment
            POINTS = Button(self.screen, f'Points: {self.server.points[self.name][0]}', 'arial', 90, 105, (680 - (self.STAND.render_height + 50)), (255, 255, 255), False, False)
            # Shows the calculated amount of points that the dealer has
            DEALER_POINTS = Button(self.screen, f'Points: {self.server.dealer_display_points}', 'arial', 50, self.WIDTH/2, 400, (0, 0, 255), False, True)

            if self.server.points[self.name][0] == 'Over 21': # Runs if the players points is over 21
                self.Stand = True # Automatically has the person stand

            # Draws the Hit or Stand Buttons to Hit and allows you to click them
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
            if self.server.turn == self.server.order.index(self.name): # Runs if it is the player's turn
                TURN = Button(self.screen, 'It is your turn', 'arial', 90, self.WIDTH/2, 100, (0, 255, 0), False, True) # Renders in that it is your turn in green text
            elif self.Stand == True:
                TURN = Button(self.screen, 'Your are standing', 'arial', 90, self.WIDTH/2, 100, (0,0,255), False, True) # Renders in that you are standing in Blue text
            else: # Runs if it is not your turn and you have not stood
                current_turn = self.server.order[self.server.turn]
                TURN = Button(self.screen, f'It is {current_turn}\'s turn', 'arial', 90, self.WIDTH/2, 100, (255, 0, 0), False, True) # Renders in that it not is your turn in red text

            
            # Shows players that are in the lobby
            player_y = 100
            for i, j in enumerate(self.server.players): # Runs through players names
                PLAYER = Button(self.screen, j, 'arial', 60, 1500, player_y, (255,255,255), False, False) # Renders in players text name
                player_y += PLAYER.render_height + 50 # Adds 50 pixles after name is rendered


            if WAIT < 100: # Run's if the click count is less than 100
                WAIT += 10 # Adds 5 to the WAIT variable

            
            if self.server.over == True: # Runs if the game has ended
                time.sleep(3) # Pauses the game for 3 seconds
                print('End Game') # Prints in the player's console that the game has ended
                break

            pygame.display.update() # Shows the new rendered frame in the window