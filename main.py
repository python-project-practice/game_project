import pygame
from pygame.locals import *
import draw

import UI
from game_project import Character, Near_Enemy, GROUND_HEIGHT
from collision import collide_list_to_list


'''
800*600 크기. 카메라 무브 없이 한 맵에서 1:1 내지는 1:3 정도의 전투를 한다.
좌표계는 pygame과 동일하게 사용한다.
1 = 1px.
y는 아래 방향이 크게, x는 오른 쪽이 크게.
원점은 가장 왼쪽 위.

'''
WIDTH, HEIGHT = 800, 600

pygame.init()
DISP = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("액션 게임")
painter = draw.painter(DISP)
painter.append_bg('image/MapSunny.png')



player = Character()
playerHPbar = UI.Character_stat(player, (5, 5))
painter.append(player)
painter.append(playerHPbar)
player.hitbox.debugColor = (0, 0, 255)
player.atk_hitbox.debugColor = (0, 255, 255)

enemy_1 = Near_Enemy()
enemyHPbar = UI.Enemy_stat(enemy_1, (0, 180))
painter.append(enemy_1)
painter.append(enemyHPbar)
enemy_1.hitbox.debugColor = (255, 0, 0)
enemy_1.atk_hitbox.debugColor = (255, 255, 0)
'''
enemy_2 = Near_Enemy(position=(550, GROUND_HEIGHT))
enemy2HPbar = UI.Enemy_stat(enemy_2, (0, 180))
painter.append(enemy_2)
painter.append(enemy2HPbar)
'''
hitbox_layer = {'player':[player.hitbox],            'enemy':[enemy_1.hitbox],          'item': [],
                'player_attack':[player.atk_hitbox], 'enemy_attack':[enemy_1.atk_hitbox], 'throwable':[]
               }

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

frame = 0
frame_hp = 0
clock = pygame.time.Clock()

gulim = pygame.font.SysFont('Gulim', 36)
running = True

gulim_dead = pygame.font.SysFont('Gulim', 70)
gulim_choose = pygame.font.SysFont('Gulim', 50)
retry = gulim_dead.render('Retry?', 1, BLACK)
choose = gulim_choose.render('Y / N', 1, BLACK)
retryrect = retry.get_rect()
chooserect = choose.get_rect()
retryrect.center = (WIDTH / 2, HEIGHT / 4)
chooserect.center = (WIDTH / 2 , HEIGHT * (35 / 100))

while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
   
    player.control(pygame.key.get_pressed())
    player.update()
    
    enemy_1.near_ai(player)

    enemy_1.update()
    '''
    enemy_2.near_ai(player)
    enemy_2.update()
    '''
    painter.image_update()
    painter.draw()

    collide_list_to_list(hitbox_layer['player'], hitbox_layer['enemy'])
    collide_list_to_list(hitbox_layer['player_attack'], hitbox_layer['enemy'])
    collide_list_to_list(hitbox_layer['player'], hitbox_layer['enemy_attack'])

    if player.hp == 0:
        DISP.blit(retry, retryrect)
        DISP.blit(choose, chooserect)
    
    fps = clock.get_fps()
    fpsmsg = gulim.render('fps: ' + str(int(fps)), 1, BLACK, WHITE)
    DISP.blit(fpsmsg, (650, 10))

    pygame.display.update()

    frame += 1
pygame.quit()

