# FiveCardMau
 Creating the Card Game in Python

This game took a lot of time to work, thank you to all that find this to play.

Thanks to the following website for the textures of the cards.
https://opengameart.org/content/playing-cards-vector-png



Resources for later (Im just lazy and dont wanna store them anywhere else):
def game(screen, network, player, server, name):
    global WIDTH
    global HEIGTH
    global background
    voted = False
    hand = {}

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
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
        server = network.get_game()
        print(server.hand[name])
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