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
    n = Network()
            
    name = input()

    # Initializes py game window
    pygame.init()

    # Sets up screen size, you could use pygame.RESIZABLE or pygame.FULLSCREEN
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption('Five Card Mau')
    
    # Background Music
    mixer.music.load('music.mp3')
    mixer.music.play(-1)

    main_menu(screen, name)

def connect_server(screen, name, network):
    # Initializes connection with server
    count = 0
    while True:
        
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
        try:
            player = int(n.connect(name))
            print(player)
            break
        except:
            if count == 0:
                connectingText = f'Connecting {name} to Server'
                count = 1
            elif count == 1:
                connectingText = f'Connecting {name} to Server.'
                count = 2
            elif count == 2:
                connectingText = f'Connecting {name} to Server..'
                count = 3
            elif count == 3:
                connectingText = f'Connecting {name} to Server...'
                count = 0
            screen.fill((0,0,0))
            connectingFont = pygame.font.SysFont('arial', 29)
            connectingRender = connectingFont.render(connectingText, 1, (255, 255, 255))
            screen.blit(connectingRender, (int(WIDTH/2 - connectingRender.get_width()/2), int(HEIGHT/2 - connectingRender.get_height()/2)))
            pygame.display.update()
            pass

    # Starts game
    player = 1
    game(screen, network, player)


    


def game(screen, n, player):
    global WIDTH
    global HEIGTH
    global background
    voted = False
    hand = {}

    lobby(screen)

    #Card Placement
    text = 'Place Card(s) Here'
    tap = "TAP!"
    myFont = pygame.font.SysFont('arial', 29)
    card_placer = myFont.render(text, 1, (255, 255, 255))
    TAP = myFont.render(tap, 1, (255, 255, 255))

    #Background
    background = pygame.image.load('background.png')


    # Game
    while not game_over:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
    
        # Resets screen
        screen.fill((0,0,0))
        screen.blit(background, (0,0))
        
        #Hovering whites
        place_card(screen, card_hold)
        tapper(screen, card_hold)

        # Where to place cards
        pygame.draw.rect(screen, (0,0,0), (1604,50, Card_x, Card_y))
        screen.blit(card_placer, (1610,230))

        # Tap Button
        pygame.draw.circle(screen, (0,0,0), (500, 225), 100)
        screen.blit(TAP, (470,212))

        # Place Cards
        pygame.draw.rect(screen, (0,0,0), (1604, 500, 186, 100))

        # Reset Place Card
        pygame.draw.rect(screen, (0,0,0), (1810, 500, 100, 100))

        card_held(screen)

        pygame.display.update()

def place_card(screen, card_hold):

    # White outline on black box
    pressed = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    if (pressed[0] == 1) and (pos[0] >= 1604 and pos[0] <= 1870 and pos[1] >= 50 and pos[1] <= 450) and card_hold==True:
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
        pygame.draw.rect(screen, (0,0,0), (temp[0], temp[1], Card_x, Card_y))
        card_hold = True
        print(1)
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
        # print(4)

def tapper(screen, card_hold):
    # You might not need this
    pos = pygame.mouse.get_pos()

    if card_hold == False and (pos[0] >= 400 and pos[0] <= 600 and pos[1] >= 125 and pos[1] <= 325):
        pygame.draw.circle(screen, (255,255,255), (500, 225), 120)
    else:
        pass

# def card_move(screen, dif_x, dif_y):
#     pygame.draw.rect(screen, (0,0,0), (1604,50, Card_x, Card_y)
    
    
def lobby(screen):
    game = False

    lobby = pygame.image.load('lobby.png')

    while game == False:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()

        screen.fill((0,0,0))
        screen.blit(lobby, (0,0))

        draw_text(screen, 'Lobby', 'arial', 35, 400,400, (255,255,255))

        pygame.display.update()

# def draw_text(screen, text, font, fontsize, x, y, color, corner):
#     '''
#     screen = pygame render screen
#     text = what you would like to be said
#     font = what font you would like
#     fontsize = fontsize you would like
#     x = width location location on the screen
#     y = height location on the screen
#     color = color of the text (x,y,z)
#     corner = True if you want using the center of the text or False if you want to use top left
#     '''
#     texter = str(text)
#     fonter = pygame.font.SysFont(font, fontsize)
#     Render = fonter.render(texter, 1, color)
#     if corner == True:
#         pygame.draw.rect(screen, (0,0,0), (int(x - Render.get_width()/2), int(y - Render.get_height()/2), int(Render.get_width()) + 10, int(Render.get_height() + 10)))
#         screen.blit(Render, (int(x - Render.get_width()/2), int(y - Render.get_height()/2)))
#     elif corner == False:
#         pygame.draw.rect(screen, (0,0,0), (x, y, int(Render.get_width()) + 10, int(Render.get_height() + 10)))
#         screen.blit(Render, (x + 10, y + 10))
    
            
def main_menu(screen, name):
    join = False

    lobby = pygame.image.load('lobby.png')

    while join == False:
        for event in pygame.event.get():
            # print(event)
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
        JOIN.hover()
        # draw_text(screen, 'Main Menu', 'arial', 35, WIDTH/2,400, (255,255,255), True)
        # draw_text(screen, f'Welcome {name}', 'arial', 35, 0,0, (255,255,255), False)
        # draw_text(screen, 'Join', 'arial', 80, WIDTH/2, HEIGHT/2, (255,255,255), True)

        pygame.display.update()





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
        screen.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False
    
    def moving(self, pos, button_hold):
        pass

    def draw_text(self):
        texter = str(self.text)
        fonter = pygame.font.SysFont(self.font, self.fontsize)
        Render = fonter.render(texter, 1, self.color)
        self.render_width = Render.get_width()
        self.render_height = Render.get_height()
        if self.center == True:
            pygame.draw.rect(self.screen, (0,0,0), (int(self.x - self.render_width/2 - 10), int(self.y - self.render_height/2 - 10), int(self.render_width) + 20, int(self.render_height + 20)))
            self.screen.blit(Render, (int(self.x - self.render_width/2), int(self.y - self.render_height/2)))
        elif self.center == False:
            pygame.draw.rect(self.screen, (0,0,0), (self.x, self.y, int(self.render_width) + 20, int(self.render_height + 20)))
            self.screen.blit(Render, (self.x + 10, self.y + 10))

    def hover(self):
        pos = pygame.mouse.get_pos()
        mouse_x = pos[0]
        mouse_y = pos[1]
        print(mouse_x, mouse_y)
        if self.center == True:
            upper_x = self.x + self.render_width/2
            lower_x = self.x - self.render_width/2
            upper_y = self.y - self.render_height/2
            lower_y = self.y + self.render_height/2
            if ((mouse_x <= upper_x) and (mouse_x >= lower_x)) and ((mouse_y <= upper_y) and (mouse_y >= lower_y)):
                print(1)
                pyagme.draw.rect(self.screen, (255,255,255), (int(self.x - self.render_width/2 - 20), int(self.y - self.render_height/2 - 20), int(self.render_width) + 40, int(self.render_height + 40)))
        elif self.center == False:
            upper_x = self.x + self.render_width
            lower_x = self.x
            upper_y = self.y
            lower_y = self.y + self.render_height
            if ((mouse_x <= upper_x) and (mouse_x >= lower_x)) and ((mouse_y <= upper_y) and (mouse_y >= lower_y)):
                print(2)
                pyagme.draw.rect(self.screen, (255,255,255), (int(self.x - 20), int(self.y - 20), int(Render.get_width()) + 40, int(Render.get_height() + 40)))
        


def game_ended():
    # set values that need to be reset when the server announces it
    pass

def vote():
    pass
    # Use this function to only let the player vote once.



if __name__ == '__main__':
    main()
