import pygame
import sys
import random
import json
import time
from pygame import mixer
from Network import Network

# Initial variable for holding cards

button = False

#Screen Dimensions
WIDTH =  1920 #2560/2
HEIGHT =  1080 #1440/2

#Card Dimensions (might not be needed)
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
    n = Network()
            
    name = input()

    # Initializes py game window
    pygame.init()

    # Sets up screen size, you could use pygame.RESIZABLE or pygame.FULLSCREEN
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption('Five Card Mau')
    
    # Background Music
    # mixer.music.load('music.mp3')
    # mixer.music.play(-1)

    main_menu(screen, name, n)

def connect_server(screen, name, network):
    # Initializes connection with server
    global game_over
    count = 0
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
        # if game_over == True:
        #         sys.exit()
        # try:
        player = int(network.connect(name))
        print(player)
        server = network.get_game()
        lobby(screen, player, network, name, server)
            # break
        # except:
        #     if count == 0:
        #         connectingText = f'Connecting {name} to Server'
        #         count = 1
        #     elif count == 1:
        #         connectingText = f'Connecting {name} to Server.'
        #         count = 2
        #     elif count == 2:
        #         connectingText = f'Connecting {name} to Server..'
        #         count = 3
        #     elif count == 3:
        #         connectingText = f'Connecting {name} to Server...'
        #         count = 0
            # screen.fill((0,0,0))
            # connectingFont = pygame.font.SysFont('arial', 29)
            # connectingRender = connectingFont.render(connectingText, 1, (255, 255, 255))
            # screen.blit(connectingRender, (int(WIDTH/2 - connectingRender.get_width()/2), int(HEIGHT/2 - connectingRender.get_height()/2)))
            # pygame.display.update()
            # pass

    # Starts game
    # player = 1
    # game(screen, network, player)


    


def game(screen, network, player, server, name):
    global WIDTH
    global HEIGTH
    global background
    voted = False

    #Background
    background = pygame.image.load('background.png')

    WAIT = 0
    # Game
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
        server = network.get_game()
        # Resets screen
        screen.fill((0,0,0))
        screen.blit(background, (0,0))

        if server.winner == True:
            break
        
        # Creates and draws cards that the player holds
        CARD1 = Card(screen, server.hand[name]['Hand'][0], 100, 680)
        CARD2 = Card(screen, server.hand[name]['Hand'][1], 590, 680)
        CARD3 = Card(screen, server.hand[name]['Hand'][2], 1080, 680)
        CARD4 = Card(screen, server.hand[name]['Hand'][3], 1570, 680)
        try:
            WAITING = Card(screen, server.hand[name]['Waiting'][0], 1570, 100)
        except:
            WAITING = False

        PASS = Button(screen, 'Pass', 'arial', 90, 150, 150, (255,255,255), False, False)

        # Draws square under the card the player is hovering over and sends data to server
        if CARD1.hover() == True and WAITING != False and WAIT == 100:
            network.change_hand(server.hand[name]['Hand'][0], server.hand[name]['Waiting'][0])
            WAIT = 0
        if CARD2.hover() == True and WAITING != False and WAIT == 100:
            network.change_hand(server.hand[name]['Hand'][1], server.hand[name]['Waiting'][0])
            WAIT = 0
        if CARD3.hover() == True and WAITING != False and WAIT == 100:
            network.change_hand(server.hand[name]['Hand'][2], server.hand[name]['Waiting'][0])
            WAIT = 0
        if CARD4.hover() == True and WAITING != False and WAIT == 100:
            network.change_hand(server.hand[name]['Hand'][3], server.hand[name]['Waiting'][0])
            WAIT = 0
        if PASS.hover() == True and WAITING != False and WAIT == 100:
            network.change_hand('Pass', server.hand[name]['Waiting'][0])
            WAIT = 0

        # Might use not sure yet
        # WAITING.hover()
        

        player_y = 100
        for i, j in enumerate(server.players):
            PLAYER = Button(screen, j, 'arial', 60, 960, player_y, (255,255,255), False, True)
            player_y = PLAYER.render_height + 50

        check_winner(screen, name, server, network)

        if WAIT < 100:
            WAIT += 4

        pygame.display.update()

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

def tapper(screen, card_hold):
    # You might not need this
    pos = pygame.mouse.get_pos()

    if card_hold == False and (pos[0] >= 400 and pos[0] <= 600 and pos[1] >= 125 and pos[1] <= 325):
        pygame.draw.circle(screen, (255,255,255), (500, 225), 120)
    else:
        pass

# def card_move(screen, dif_x, dif_y):
#     pygame.draw.rect(screen, (0,0,0), (1604,50, Card_x, Card_y)
    
    
def lobby(screen, player, network, name, server):
    global game_over
    gamer = False
    voted = False
    lobby = pygame.image.load('background.png')
    # game_over = True
    # network.change_hand('this', 'works')
    while gamer == False:
        server = network.get_game()
        started = server.started
        player_y = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
        screen.fill((0,0,0))
        screen.blit(lobby, (0,0))

        LOBBY = Button(screen, 'Lobby', 'arial', 35, 0, 0, (255,255,255), False, False)
        for i, j in enumerate(server.players):
            PLAYER = Button(screen, j, 'arial', 40, 1500, player_y, (255,255,255), False, False)
            player_y = PLAYER.render_height + 50

        if voted == False:
            VOTE = Button(screen, 'Vote to Start Game', 'arial', 35, 50, 880, (0,255,0), False, False)
            clicked = VOTE.hover()
            if clicked == True:
                network.send('voted')
                voted = True
        elif voted == True:
            VOTE = Button(screen, 'You Have Voted', 'arial', 35, 50, 880, (255,0,0), False, False)
        
        TOTAL_VOTES = Button(screen, f'Total Votes: {server.voters}', 'arial', 35, 50, 980, (255,0,0), False, False)

        if server.winner_name != '':
            WINNER_NAME = Button(screen, f'{server.winner_name} won the last game', 'arial', 50, WIDTH/2, 200, (0,255,0), False, True)

        pygame.display.update()

        if started == True:
            game(screen, network, player, server, name)
            voted = False

    
            
def main_menu(screen, name, network):
    join = False

    lobby = pygame.image.load('lobby.png')

    while join == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()

        screen.fill((0,0,0))
        screen.blit(lobby, (0,0))


        MAIN = Button(screen, 'Main Menu', 'arial', 35, WIDTH/2, 400, (255,255,255), False, True)
        WELCOME = Button(screen, f'Welcome {name}', 'arial', 35, 0, 0, (255,255,255), False, False)
        JOIN = Button(screen, 'Join', 'arial', 80, WIDTH/2, HEIGHT/2, (255,255,255), False, True)
        clicked = JOIN.hover()
        if clicked == True:
            connect_server(screen, name, network)

        pygame.display.update()

# Decides if person is elgible to win
def check_winner(screen, name, server, network):
    Card1 = server.hand[name]['Hand'][0].split('_')
    Card2 = server.hand[name]['Hand'][1].split('_')
    Card3 = server.hand[name]['Hand'][2].split('_')
    Card4 = server.hand[name]['Hand'][3].split('_')

    if (Card1[0] == Card2[0]) and (Card1[0] == Card3[0]) and (Card1[0] == Card4[0]):
        WINNER = Button(screen, 'Winner', 'arial', 60, WIDTH/2, 730, (0,255,0), False, True)
        if WINNER.hover() == True:
            network.send('Winner')






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
        screen.blit(text, (self.x + round(self.width/2) - round(text_width/2), self.y + round(self.height/2) - round(text_height/2)))

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
    def __init__(self, screen, card, x, y):
        self.screen = screen
        self.card = card
        self.x = x
        self.y = y
        self.draw()

    def draw(self):
        self.location = pygame.image.load(f'Playing_Cards/{self.card}.png')
        self.location = pygame.transform.rotozoom(self.location, 0, .5)
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


        


def game_ended():
    # set values that need to be reset when the server announces it
    pass

def vote():
    pass
    # Use this function to only let the player vote once.



if __name__ == '__main__':
    main()