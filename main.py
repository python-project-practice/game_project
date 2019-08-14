import os, sys
import pygame
from pygame.locals import *
import draw
from game_project import Character, Near_Enemy

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
pygame.display.set_caption("연습")
painter = draw.painter(DISP)
player = Character()
painter.append(player)

enemy_1 = Near_Enemy()
painter.append(enemy_1)

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

frame = 0
clock = pygame.time.Clock()
while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
   

    enemy_1.near_ai(player)
    player.control(pygame.key.get_pressed())
    painter.update()
    painter.draw_bg('image/MapSunny.png')
    pygame.draw.rect(DISP, WHITE, [0, 0, 400, 75]) 
    pygame.draw.rect(DISP, RED, [5, 5, 150, 30])
    pygame.draw.rect(DISP, BLUE, [5, 40, 150, 30])    
    painter.draw()


    pygame.display.update()

    frame += 1
    
