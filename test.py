# test = [5,5,5,5,5]
# test2 = [6,6,6,6,6,6,6]
# test3 = [test, test2]
# test4 = [9,9,9,9,9]

# print(test3)

# test3.append(test4)

# print(test3)

# import pygame
# from pygame.locals import *

# RED = (255, 0, 0)
# GRAY = (150, 150, 150)

# pygame.init()
# w, h = 1920, 1080
# screen = pygame.display.set_mode((w, h))
# running = True

# img = pygame.image.load('Playing Cards/2_of_clubs.png')
# img.convert()
# rect = img.get_rect()
# rect.center = 800, 600
# img = pygame.transform.rotozoom(img, 0, .5)
# screen.blit(img, rect)
# moving = False

# while running:
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             running = False

#         elif event.type == MOUSEBUTTONDOWN:
#             if rect.collidepoint(event.pos):
#                 moving = True

#         elif event.type == MOUSEBUTTONUP:
#             moving = False

#         elif event.type == MOUSEMOTION and moving:
#             rect.move_ip(event.rel)
    
#     screen.fill(GRAY)
#     screen.blit(img, rect)
#     pygame.draw.rect(screen, RED, rect, 1)
#     pygame.display.update()

# pygame.quit()

# import json

# data = {}
# with open ('Cards.txt') as json_file:
#     data = json.load(json_file)
# for i in range(0, len(data["Cards"])):
#     print(data["Cards"][i])
# print(len(data["Cards"]))

import json

names = {'Matt': [0, True]}
del names['Matt']
print(names)
# , 'Dean':[1, False], 'Shea':[1, False], 'Patrick':[1, False]}

# try:
#     for i, j in enumerate(names):
#         # print(j)
#         del names[j]
#         print(names)
#         # for k in range(0, len(names[j])):
#         #     del names[j]
#         #     print(names)
#     print(names)
# except:
#     print('All names deleted')
#     print(names)


# try:
#     del names['Matt']
#     try:
#         for i, j in enumerate(names):
#             if names[j][1] == False:
#                 names[j][1] = True
#                 break
#     except:
#         # return game back preparing state
#         pass
# except:
#     pass

# print(names)

# del names['Matt']

# print(names
# {"Cards": ["2_of_clubs", "2_of_diamonds", "2_of_hearts", "2_of_spades", "3_of_clubs", "3_of_diamonds", "3_of_hearts", "3_of_spades","4_of_clubs", "4_of_diamonds", "4_of_hearts", "4_of_spades","5_of_clubs", "5_of_diamonds", "5_of_hearts", "5_of_spades","6_of_clubs", "6_of_diamonds", "6_of_hearts", "6_of_spades","7_of_clubs", "7_of_diamonds", "7_of_hearts", "7_of_spades","8_of_clubs", "8_of_diamonds", "8_of_hearts", "8_of_spades","9_of_clubs", "9_of_diamonds", "9_of_hearts", "9_of_spades","10_of_clubs", "10_of_diamonds", "10_of_hearts", "10_of_spades","ace_of_clubs", "ace_of_diamonds", "ace_of_hearts", "ace_of_spades","jack_of_clubs", "jack_of_diamonds", "jack_of_hearts", "jack_of_spades","queen_of_clubs", "queen_of_diamonds", "queen_of_hearts", "queen_of_spades","king_of_clubs", "king_of_diamonds", "king_of_hearts", "king_of_spades", "red_joker", "black_joker"]}

# with open('Cards.json', 'r') as json_file:
#     test = json.load(json_file)

# print(test)