import pygame
from pygame.locals import *
import draw

import UI
import game_project
from game_project import Character, Near_Enemy, Distance_Enemy, Projectile, GROUND_HEIGHT
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
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

pygame.init()
DISP = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("액션 게임")
unit.painter = draw.painter(DISP)
painter = unit.painter
units = unit.units
############################################################################################
#게임 전반적으로 쓰이는 변수/ 폰트 등을 지정한다. 게임을 재시작해도 새로 불러올 필요가 없다.
############################################################################################ 
frame = 0
frame_hp = 0
clock = pygame.time.Clock()

gulim = pygame.font.SysFont('Gulim', 36)
gulim_dead = pygame.font.SysFont('Gulim', 70)
gulim_choose = pygame.font.SysFont('Gulim', 50)

running = True  #프로그램을 계속 돌릴 것인지 여부

retry = gulim_dead.render('Retry?', 1, BLACK)
youwin = gulim_dead.render('You Win!', 1, BLACK)
choose = gulim_choose.render('Y / N', 1, BLACK)
retryrect = retry.get_rect()
youwinrect = youwin.get_rect()
chooserect = choose.get_rect()
retryrect.center = (WIDTH / 2, HEIGHT / 4)
youwinrect.center = (WIDTH / 2, HEIGHT * 0.15)
chooserect.center = (WIDTH / 2 , HEIGHT * (35 / 100))


def gameoverEvent():
    global running # 전역변수 running을 쓴다. 명시하지 않으면 메소드에 속한 임시변수 running을 만든다.
    while True:
        DISP.blit(retry, retryrect)
        DISP.blit(choose, chooserect)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_y:
                    return
                if event.key == K_n:
                    running = False
                    return
        pygame.display.update()

def winEvent():
    global running # 전역변수 running을 쓴다. 명시하지 않으면 메소드에 속한 임시변수 running을 만든다.
    while True:
        DISP.blit(youwin, youwinrect)
        DISP.blit(retry, retryrect)
        DISP.blit(choose, chooserect)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_y:
                    return
                if event.key == K_n:
                    running = False
                    return
        pygame.display.update()


while running: #프로그램 전체를 담당하는 반복문.
#############################################################################################
#한 게임마다 초기화해야 하는 것들을 담당한다. 플레이어나, 적이나 그런 것들.
#############################################################################################
    painter.reset()
    painter.append_bg('image/MapSunny.png')
    units['enemy'] = []
    units['projectile'] = []
    
    #트리 형태로 보면 다음과 같다.
    #units(Dict)->enemy(list)->nearenemySet->Near_Enemy
    #                                       ->UI
    #           ->items(list)->itemSet(아직까진 아이템을 쓸 지도 미확정이지만.)

    player = unit.characterSet(Character()) #캐릭터와 그 캐릭터에 해당하는 인터페이스까지 한번에 생성한다.
    player.character.draw_hitbox = True
    player.character.hitbox.debugColor = (0, 0, 255)
    player.character.atk_hitbox.debugColor = (0, 255, 255)


    units['enemy'].append(unit.nearenemySet(Near_Enemy()))
    units['enemy'].append(unit.farenemySet(Distance_Enemy(position=(600, GROUND_HEIGHT))))
    units['projectile'].append(unit.projectileSet(Projectile(position=(300, 100), speed=(6, 0), damage=0, getGravity=False)))
    units['projectile'].append(unit.projectileSet(Projectile(position=(300, 100), speed=(2, 0), damage=0, getGravity=True)))
    # units['enemy'].append(unit.nearenemySet(Near_Enemy(position=(550,GROUND_HEIGHT))))


    for enemy in units['enemy']:
        enemy.character.draw_hitbox = True
        enemy.character.hitbox.debugColor = (255, 0, 0)
        enemy.character.atk_hitbox.debugColor = (255, 255 , 0)
    painter.append(player)
    
    for items in units.values(): #units['player'], units['enemy'], units['items']
        for item in items: #각각의 리스트에 있는 플레이어들, 적들, 아이템들을 불러온다.
            painter.append(item) #unit.unitSet을 통째로 등록한다.


    hitbox_layer = {'player':       [player.character.hitbox],
                    'player_attack':[player.character.atk_hitbox],
                    'enemy' :       [i.character.hitbox for i in units['enemy']],
                    'enemy_attack': [i.character.atk_hitbox  for i in units['enemy']],
                    'projectile':   [i.character.hitbox for i in units['projectile']]
                    }

    playing = True  #게임이 계속 실행중인지 여부

############################################################################################
#실제 게임을 시작한다.
############################################################################################
    while playing: # 한 게임을 담당하는 반복문
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        player.control(pygame.key.get_pressed())
        player.update()
        for enemy in units['enemy']:
            enemy.ai(player.character)
            enemy.update()

        for proj in units['projectile']:
            proj.update()
            if(not 0 < proj.character.position.x < WIDTH or proj.character.position.y > GROUND_HEIGHT):
                units['projectile'].remove(proj)
                painter.remove(proj)
                del proj

        collide_list_to_list(hitbox_layer['player_attack'], hitbox_layer['enemy'])
        collide_list_to_list(hitbox_layer['player'], hitbox_layer['enemy_attack'])

        painter.image_update()
        painter.draw()


        if player.character.hp <= 0: #게임오버. 내가 죽으면서 적을 모두 죽였어도 게임오버(승리x).
            playing = False
            gameoverEvent()

        else:
            if(all(i.character.act == 'dead' for i in units['enemy'])): #적이 모두 죽으면 승리
                playing = False
                winEvent()

    
        fps = clock.get_fps()
        fpsmsg = gulim.render('fps: ' + str(int(fps)), 1, BLACK, WHITE)
        DISP.blit(fpsmsg, (650, 10))

        pygame.display.update()

        frame += 1
################################################################################################
#사용했던 것들을 날린다.
################################################################################################
    del units
    del player
    del painter
pygame.quit()

