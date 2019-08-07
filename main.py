import os, sys
import pygame
import draw

'''
800*600 크기. 카메라 무브 없이 한 맵에서 1:1 내지는 1:3 정도의 전투를 한다.
좌표계는 pygame과 동일하게 사용한다.
1 = 1px.
y는 아래 방향이 크게, x는 오른 쪽이 크게.
원점은 가장 왼쪽 위.











'''

HEIGHT, WIDTH = 800, 600

pygame.init()
DISP = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption("연습")
painter = draw.painter(DISP)
standsprite = draw.sprite(['image/cloud.png', 'image/cloud2.png'], True, pos=(100,100))
painter.append(standsprite)


frame = 0
while True:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            pygame.quit()
            sys.exit()
    painter.draw_bg('image/MapSunny.png')
    painter.draw()
    pygame.display.update()
    frame += 1
    if frame % 5 == 0:
        painter.update()
