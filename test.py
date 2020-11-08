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

# import json

# names = {'Matt': [0, True], 'Dean':[1, False], 'Shea':[1, False], 'Patrick':[1, False]}
# test = {'Matt': {'Hand': ['four_there', 'five', 'eight'], 'Waiting':['nine','twelve','thirteen']}, 'Dean':{'Hand': ['four', 'five', 'eight'], 'Waiting':['nine','twelve','thirteen']}}
# tester = test['Matt']['Hand'][0].split('_')
# print(tester)
# print(test)


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

# import random
# import json

# with open('Cards.json') as json_file:
#             cards = json.load(json_file)

# hand = {'Matt':{'Hand':[],'Waiting':[]}}

# for i, j in enumerate(hand):
#             for k in range(0,4):
#                 r = random.randint(0, len(cards['Cards']))
#                 print(r)
#                 hand[j]['Hand'].append(cards['Cards'][r])
#                 cards['Cards'].pop(r)
# print('Dealt Cards')

# if len(hand['Matt']['Waiting']) == 0:
#             r = random.randint(0, len(cards['Cards']) - 1)
#             hand['Matt']['Waiting'].append(cards['Cards'][r])
#             cards['Cards'].pop(r)

# print('Ending Game')
# for i, j in enumerate(hand):
#     print(j)
#     for k in range(0, len(hand[j]['Hand'])):
#         cards['Cards'].append(hand[j]['Hand'][0])
#         hand[j]['Hand'].pop(0)
#     try:
#         for k in range(0, len(hand[j]['Waiting'])):
#             print(hand['Matt']['Waiting'][0])
#             cards['Cards'].append(hand[j]['Waiting'][0])
#             hand[j]['Waiting'].pop(0)
#     except:
#         print('No Cards Waiting or Error')
# print(len(cards['Cards']))

# import socket

# print(socket.gethostname())

# hand = ['matt', 'patt']
# print(hand.index('patt'))
# for i in hand:
#     print(i)
# hand = f.read()
# print(hand)
# hand = bytes(hand, 'utf-8')
# print(hand)
# hand = pickle.loads(hand)
# print(hand)



# count_low = 0
# count_high = 0
# Ace = False
# hello = input()
# count_add = hello.split('_')
# print(count_add)
# check = ['1','2','3','4','5','6','7','8','9','10']

# for j in check:
#     if count_add[0] == j:
#         bruh = int(count_add[0])
#         count_low += bruh
#         count_high += bruh
#         break
# if count_add[0] == 'king' or count_add[0] == 'queen' or count_add[0] == 'jack':
#     count_low += 10
#     count_high += 10
# elif count_add[0] == 'ace':
#     if Ace == False:
#         count_low += 1
#         count_high += 11
#         Ace = True
#     elif Ace == True:
#         count_low += 1
#         count_high += 1

# print(count_low)
# print(count_high)
# print(Ace)

# tester = ''
# test = ('Five', 'Nine', 'Eight')
# for i in range(0, len(test)):
#     if i == 0:
#         tester += test[i]
#     else:
#         tester += f', {test[i]}'
# print(f'Winner(s): {tester}')

# print('What does "by the skin oflkjasdf" even  mean?')

# L_value = float(input('Input the value of your loan: '))
# i_rate = float(input('Input the monthly interest rate on the loan: '))
# n_mo = int(input('Input the number of months: '))
# m_pay = float(input('Input the amount you are paying per month: '))

# cl_val = L_value
# for i in range(1, n_mo+1):
#     cl_val = cl_val*(1+(i_rate/100))-m_pay
#     print(f'Loan value after {i} months is ${cl_val:.2f}.')


# mat_a = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]

# for i in range(0,len(mat_a)):
#     mat_a[i][3] = 0
# mat_a[1][1] = 66
# mat_a[3][0:3] = [4,4,4]

temp = float(input('What is the temperature in degrees Celcius: '))
press = float(input('What is the pressure in atmospheres: '))

high_t = 100
high_p = 2.0

if temp <= high_t and press <= high_p:
    print('Good Combination')
elif temp > high_t and press > high_p:
    print('too hot')
    print('too much pressure')
elif temp > high_t and press <= high_p:
    print('too hot')
elif temp <= high_t and press > high_p:
    print('too much pressure')