import pygame
from pygame.locals import *
import draw

import UI
from game_project import Character, Near_Enemy, GROUND_HEIGHT
from collision import collide_list_to_list
import unit

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
painter.append_bg('image/MapSunny.png')

units = {'enemy':[], 'items':[]} #각각의 유닛을 종류별로 리스트에 담고, 리스트를 하나의 딕셔너리에 넣어 관리.
                                 #플레이어는 단 하나의 값만 가지므로 리스트에 쓰기는 부담스럽고, 따라서 units딕셔너리엔 넣지 않았다.

#트리 형태로 보면 다음과 같다.
#units(Dict)->enemy(list)->nearenemySet->Near_Enemy
#                                       ->UI
#           ->items(list)->itemSet(아직까진 아이템을 쓸 지도 미확정이지만.)

player = unit.characterSet(Character()) #캐릭터와 그 캐릭터에 해당하는 인터페이스까지 한번에 생성한다.
units['enemy'].append(unit.nearenemySet(Near_Enemy()))
units['enemy'].append(unit.nearenemySet(Near_Enemy(position=(550,GROUND_HEIGHT))))
painter.append(player)

for items in units.values(): #units['player'], units['enemy'], units['items']
    for item in items: #각각의 리스트에 있는 플레이어들, 적들, 아이템들을 불러온다.
        painter.append(item) #unit.unitSet을 통째로 등록한다.


hitbox_layer = {'player':       [player.character.hitbox],
                'player_attack':[player.character.atk_hitbox],
                'enemy' :       [i.character.hitbox for i in units['enemy']],
                'enemy_attack': [i.character.atk_hitbox  for i in units['enemy']],
                'item':         [],
                'throwable':    []
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

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
   
    player.control(pygame.key.get_pressed())
    player.update()

    for enemy in units['enemy']:
        enemy.ai(player.character)
        enemy.update()

    painter.image_update()
    painter.draw()

    collide_list_to_list(hitbox_layer['player'], hitbox_layer['enemy'])

    
    fps = clock.get_fps()
    fpsmsg = gulim.render('fps: ' + str(int(fps)), 1, BLACK, WHITE)
    DISP.blit(fpsmsg, (650, 10))

    pygame.display.update()

    frame += 1
pygame.quit()
