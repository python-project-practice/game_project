import pygame
from pygame.locals import *
import draw

import UI
from game_project import Character, Near_Enemy
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
pygame.display.set_caption("연습")
painter = draw.painter(DISP)
painter.append_bg('image/MapSunny.png')


player = Character()
playerHPbar = UI.Character_stat(player, (5, 5))
painter.append(player)
painter.append(playerHPbar)

enemy_1 = Near_Enemy()
enemyHPbar = UI.Enemy_stat(enemy_1, (0, 180))
painter.append(enemy_1)
painter.append(enemyHPbar)

hitbox_layer = {'player':[player.hitbox],            'enemy':[enemy_1.hitbox],          'item': [],
                'player_attack':[player.atk_hitbox], 'enemy_attack':[enemy_1.atk_hitbox], 'throwable':[]
               }
# 일단은 임시로 만들어두었음.
# 매 프레임이 끝날 때 쯤 어디에 collision 모듈을 이용해서 충돌처리를 할 생각이다.
# collision.collide_list_to_list(hitbox_layer['player'], hitbox_layer['enemy_attack'])
    # 그러면 안쪽에서 hitbox_layer['player'][0].get_hit(hitbox_layer['enemy_attack'][0])를 불러서 충돌시 자율적으로 행동하게 하는거지.
# 이렇게 하면 되겠지?? hitbox_layer에 적 공격과 적 자체, 캐릭터의 공격과 캐릭터 자체를 따로 넣고 싶음.
# 히트박스 레이어로 만들 것들은, 플레이어, 적, 플레이어 공격, 적 공격, (아이템...은 아직은 생각 안하고 있고)
# 벽도 히트박스를 만들까 싶긴 한데, 굳이 지금은 할 필요가 있을까 싶네. 좌우 화면 벗어나는건 각각의 .update()에서 담당하게 했다.
# 이걸 바꿀 필요가 있을까? 이것도 hitbox로 처리하는게 나을까?


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
            pygame.quit()
            running = False
   
    player.control(pygame.key.get_pressed())
    player.update()
    enemy_1.near_ai(player)
    enemy_1.update()
    painter.image_update()
    painter.draw()

    collide_list_to_list(hitbox_layer['player'], hitbox_layer['enemy'])
    #pygame.draw.rect(DISP, WHITE, [0, 0, 400, 75])
    #if frame < 150: 
    #    pygame.draw.rect(DISP, RED, [5, 5, 150 - frame, 30])
    #pygame.draw.rect(DISP, BLUE, [5, 40, 150, 30])    
    
    fps = clock.get_fps()
    fpsmsg = gulim.render('fps: ' + str(int(fps)), 1, BLACK, WHITE)
    DISP.blit(fpsmsg, (650, 10))

    pygame.display.update()

    frame += 1
    
