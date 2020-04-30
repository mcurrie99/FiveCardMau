import pygame
import sys
import random

pygame.init()

delay = 0

WIDTH = 800
HEIGHT = 600

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

player_pos = [WIDTH/2, HEIGHT-100]
player_size = [50, 50]

enemy_size = [50, 50]
enemy_pos = [random.randint(0, WIDTH-50), 50]
enemy_list = [enemy_pos]

SPEED = 10

SCORE = 0
myFont = pygame.font.SysFont('monospace', 35)
last_score = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False

clock = pygame.time.Clock()

def set_level(score):
    global SPEED
    global last_score
    if score%10==0 and SCORE!=last_score:
        SPEED +=1
        last_score=SCORE

def drop_enemies(enemy_list):
    global delay
    if len(enemy_list) < 10 and delay % 10 == 0:
        x_pos = random.randint(0, WIDTH-enemy_size[0])
        y_pos = 0
        enemy_list.append([x_pos, y_pos])
    if delay > 999:
        delay = 0
    delay += 1
    # print(delay)

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size[0], enemy_size[1]))

def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size[0])) or (p_x >= e_x and p_x < (e_x + enemy_size[0])):
        if (e_y >= p_y and e_y < (p_y + player_size[0])) or (p_y >= e_y and p_y < (e_y + enemy_size[0])):
            return True
    return False

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
    return False

def updater(enemy_list):
    global SCORE
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += SPEED
        else:
            enemy_list.pop(idx)
            SCORE += 1
            # print(SCORE)
 

while not game_over:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:

            x = player_pos[0]
            y = player_pos[1]

            if event.key == pygame.K_a:
                x -= 50
            elif event.key == pygame.K_d:
                x += 50
            elif event.key == pygame.K_w:
                y -= 50
            elif event.key == pygame.K_s:
                y += 50
            
            player_pos = [x, y]

    screen.fill((0,0,0))

    # print(SPEED)
    drop_enemies(enemy_list)
    updater(enemy_list)
    if collision_check(enemy_list, player_pos):
        game_over = True
        break
    text = 'Score: ' + str(SCORE)
    label = myFont.render(text, 1, GREEN)
    screen.blit(label, (WIDTH-200, HEIGHT-40))
    collision_check(enemy_list, player_pos)
    draw_enemies(enemy_list)
    set_level(SCORE)
    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size[0], player_size[1]))

    clock.tick(30)

    pygame.display.update()
print('GAME OVER!')
print('Your final score was ' + str(SCORE))
print('Try Again!')