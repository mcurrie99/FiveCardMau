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

import json

data = {}
with open ('Cards.txt') as json_file:
    data = json.load(json_file)
for i in range(0, len(data["Cards"])):
    print(data["Cards"][i])
print(len(data["Cards"]))