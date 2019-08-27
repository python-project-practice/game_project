'''
몹 / 캐릭터 설계
human class -> 기본적인 요소들 정의 / 기본 스텟, 모션들을 구현함(점프, 우측, 좌측, 베기, 찌르기)
    이동속도는 가속X, 등속운동, 점프는 등가속 운동
    크리티컬은 random모듈을 활용
character class -> human class를 상속하여 여기에 조작법을 추가함
enemy class -> human class를 상속하여 여기에 ai를 추가함 / 타입에 따라 근거리, 원거리로 나뉨 -> 몹 스텟은 캐릭터 스텟보다 더 좋도록 설계
    근거리 -> 일정거리 접근하면 캐릭터 공격모션과 동일하게 공격
    원거리 -> 일정거리 벌리고 공격 / 활 쏘는 모션은 위의 human class를 상속하여 모션을 오버라이딩함
        화살은 일직선으로 -> 캐릭터들은 점프해서 회피함.
boss class -> enemy class의 모션, 스텟, ai를 오버라이딩해서 짬. 공격 형태는 근/원거리 둘다 가능하도록
    ++추후 걷는 모션 / 공격 모션 / 경직 모션 등 선딜레이, 후딜레이 개념을 정의해야 함!

맵 / 규칙 설계
벨트 스크롤 형식이 아닌 스테이지 형식(적이 모두 죽으면 다음 스테이지로 넘어감)
적들을 죽이면 점수를 쌓도록 만듦(이거는 희망사항인데, 일정시간 내에 타격을 많이 하면 점수를 쌓도록 설계(콤보 시스템))
만약 적의 hp가 0이 될 경우, 타격 판정(경직)이 사라짐.

'''
from abc import *
import random
import pygame
from pygame.locals import *
import draw
from collision import hitbox
from vector import vector
import time
import UI

#++ 히트박스 클래스 고려하여 프로그래밍 ㄱㄱ

Vleft = 'view_left'
Vright = 'view_right'

MOVE_SPEED = 6
GROUND_HEIGHT = 500
MAP_LEFT_LIMIT = 0
MAP_RIGHT_LIMIT = 800

temp_t = 60
temp_h = -150


JUMP_SPEED = 4 * temp_h / temp_t
GRAVITY_CONSTANT = vector(0, -8 * temp_h / (temp_t ** 2)) # gain speed (rightward , downward) px per frame

# human 클래스에 character, enemy가 공유함
class Human(metaclass=ABCMeta):

    def __init__(self, hp = 150, mp = 0, atk = 10, arm = 0, cri = 0.1): #기본 스텟/몹, 캐릭터의 위치 설계
        self.hp = hp
        self.mp = mp
        self.atk = atk
        self.arm = arm
        self.cri = cri

        self.position = vector(0, 0)  #위치
        self.speed = vector(0, 0) #속도, 매 프레임마다 위치+= 속도
        self.viewdir = Vright #오른쪽 방향으로 일단 고정 -> 이게 없으면 방향이 고정됨 -> 고려해봐야 함
        self.act = 'stop' #여러 프레임이 걸리는 행동이 있을 거 아냐 그럴 때 지금 무슨 행동을 실행하고 있는지
        self.actframe = 0 # 여러 프레임이 걸리는 행동일 경우 몇 프레임 후에 행동이 끝나는지
        self.onGround = True #캐릭터가 땅 위에 존재
        self.draw_hitbox = False

    def __str__(self):
        return str(self.__class__)#__class__은 클래스 이름을 str 형태로 가져온다.
                                  #이 메소드를 상속받은 클래스에서도 쓸 수 있다. 디버그용.

    @abstractmethod 
    def jump(self): #점프
        pass

    @abstractmethod
    def left(self): #좌측 방향
        pass

    @abstractmethod
    def right(self): #우측 방향
        pass

    @abstractmethod
    def walk(self): # 이동
        pass

    @abstractmethod
    def stop(self): #멈춤
        pass

    @abstractmethod
    def get_attack(self, other, memo=''): #피격 판정. other:Human에게 (memo:str)형태로
        pass

    @abstractmethod
    def rigidity(self): #경직
        pass

    @abstractmethod
    def dead(self): #사망
        pass

    @abstractmethod
    def update(self): #캐릭터 상태 업데이트: 캐릭터의 스텟이나 위치 등 상태만 업데이트 한다. 내부에서 이미지 업데이트를 부르지 말자.
        pass

    @abstractmethod
    def image_update(self): # 캐릭터 이미지 업데이트: 스프라이트 이미지만 업데이트 한다. 내부에서 상태 업데이트를 부르지 말자.
        pass

    def draw(self, surf): #캐릭터/몹 상태를 나타냄
        if(self.draw_hitbox):
            self.hitbox.draw(surf)
            self.atk_hitbox.draw(surf)
        self.sprite.draw(surf)

class Character(Human):
    def __init__(self, hp = 150, mp = 20, atk = 10, arm = 10, cri = 0.1): #기본 스텟/몹, 캐릭터의 위치 설계
        super().__init__(hp, mp, atk, arm, cri)  
        self.position = vector(60, GROUND_HEIGHT)
        self.speed = vector(0, 0) #속도. 매 프레임마다 위치+= 속도

        self.motion = 0  #모션
        self.viewdir = Vright #오른쪽
        self.onGround = True #캐릭터가 땅 위에 존재

        self.static_right_sprite = draw.sprite(['image/char/static.png'], True, 1, self.position)
        self.static_left_sprite = self.static_right_sprite.flip(True, False)
        self.walk_right_sprite = draw.sprite(['image/char/walk-' + str(i) + '.png' for i in range(1,5)], True, 6, self.position)
        self.walk_left_sprite = self.walk_right_sprite.flip(True, False)
        self.slash_right_sprite = draw.sprite(['image/char/slash_' + str(i) + '.png' for i in range(1,3)], False, 3, self.position)
        self.slash_left_sprite = self.slash_right_sprite.flip(True, False)
        self.sting_right_sprite = draw.sprite(['image/char/sting_' + str(i) + '.png' for i in range(1,3)], True, 2, self.position)
        self.sting_left_sprite = self.sting_right_sprite.flip(True, False)
        self.get_attack_right_sprite = draw.sprite(['image/char/get_attack_1.png'], True, 3, self.position)
        self.get_attack_left_sprite = self.get_attack_right_sprite.flip(True, False)
        self.dead_right_sprite = draw.sprite(['image/char/get_attack_3.png'], True, 2, self.position)
        self.dead_left_sprite = self.dead_right_sprite.flip(True, False)

        self.sprite = self.static_right_sprite
    
        self.hitbox = hitbox(self, self.position.x, self.position.y, *self.sprite.get_size(), 'static')
        self.atk_hitbox = hitbox(self, self.position.x, self.position.y, *self.sprite.get_size(), 'attack')
        self.sting_cooltime = 0
        self.default_sting_cooltime = 30
        self.slash_cooltime = 0
        self.default_slash_cooltime = 30

        self.hitbox = hitbox(self, self.position.x, self.position.y, *self.sprite.get_size(), memo="static")
        self.atk_hitbox = hitbox(self, self.position.x, self.position.y, *self.sprite.get_size(), memo="attack", check=False)
        self.stop() #stop 상태로 초기화
        
    def control(self, keys): #기본적인 조작법
        if(self.act != 'stop'):
            if(self.actframe > 0):
                return

        if keys[K_RIGHT]:
            self.right()
            self.walk()

        elif keys[K_LEFT]:
            self.left()
            self.walk()

        else:
            self.stop()
            if keys[K_z]:
                self.slash()
            elif keys[K_x]:
                self.sting()

        if keys[K_UP] and self.onGround:
            self.jump()
        
        else:
            pass

        if keys[K_ESCAPE]:
            pygame.quit()

    def jump(self): #점프
        if self.onGround:
            self.onGround = False
            self.speed.y = JUMP_SPEED
            if self.viewdir == Vright:
                self.sprite = self.static_right_sprite
            if self.viewdir == Vleft:
                self.sprite = self.static_left_sprite
            self.atk_hitbox.check = False

    def left(self): #좌측 보기?
        self.viewdir = Vleft

    def right(self): #우측 보기?
        self.viewdir = Vright

    def walk(self): #보고 있는 방향으로 이동?
        if (self.viewdir == Vleft):
            self.position.x -= MOVE_SPEED
            self.sprite = self.walk_left_sprite
            self.hitbox.move(self.position)
            self.atk_hitbox.check = False
        elif (self.viewdir == Vright):
            self.position.x += MOVE_SPEED
            self.sprite = self.walk_right_sprite
            self.hitbox.move(self.position)
            self.atk_hitbox.check = False

    def stop(self):
        self.speed.x = 0
        if self.viewdir == Vright:
            self.sprite = self.static_right_sprite
        if self.viewdir == Vleft:
            self.sprite = self.static_left_sprite
        self.atk_hitbox.check = False

    def get_attack(self, other, memo=''): #피격 판정
        if (memo == 'attack'):
            self.rigidity()
            self.hp -= (other.atk - self.arm)
            if other.cri <= random.random():
                self.hp -= (other.atk * 2 - self.arm)

            if(self.hp <= 0):
                self.dead()
        else:
            pass

    def rigidity(self): #경직
        self.act = 'stun'
        self.actframe = 10
        self.atk_hitbox.check = False
        if (self.viewdir == Vleft):
            self.sprite = self.get_attack_left_sprite
            self.position.x += 40
        elif (self.viewdir == Vright):
            self.sprite = self.get_attack_right_sprite
            self.position.x -= 40
        else:
            pass

    def slash(self):
        if (self.slash_cooltime > 0):
            pass
        else:
            self.act = 'slash'
            self.actframe = 10
            self.atk_hitbox.check = True
            self.slash_cooltime = self.default_slash_cooltime
            if (self.viewdir == Vleft):
                self.sprite = self.slash_left_sprite
            elif (self.viewdir == Vright):
                self.sprite = self.slash_right_sprite
        
    def sting(self):
        if (self.sting_cooltime > 0):
            pass
        else:
            self.act = 'sting'
            self.actframe = 6
            self.atk_hitbox.check = True
            self.sting_cooltime = self.default_sting_cooltime
            if (self.viewdir == Vleft):
                self.sprite = self.sting_left_sprite
            elif (self.viewdir == Vright):
                self.sprite = self.sting_right_sprite

    def dead(self): #사망
        self.act = 'dead'
        self.actframe = 10000
        self.hitbox.check=False
        self.atk_hitbox.check = False
        if self.hp <= 0:
            if (self.viewdir == Vleft):
                self.sprite = self.dead_left_sprite
            elif (self.viewdir == Vright):
                self.sprite = self.dead_right_sprite
        else:
            pass

    def image_update(self):
        self.sprite.move(self.position)
        self.sprite.image_update()

    def update(self):
        self.hitbox.move(self.position)
        self.hitbox.resize(*self.sprite.get_size())
        self.atk_hitbox.move(self.position)
        self.atk_hitbox.resize(*self.sprite.get_size())
        if(self.act != 'stop'):
            self.actframe -= 1
            if(self.actframe == 0):
                self.act = 'stop'
        self.sting_cooltime -= 1
        self.slash_cooltime -= 1

        self.position += self.speed
        if(self.position.x < MAP_LEFT_LIMIT): #self.position.left < MAP_LEFT_LIMIT
            self.position.x = MAP_LEFT_LIMIT
        if(self.position.x + self.sprite.get_size()[0] > MAP_RIGHT_LIMIT):
            self.position.x = MAP_RIGHT_LIMIT - self.sprite.get_size()[0]

        if not self.onGround:
            self.speed += GRAVITY_CONSTANT
        if(self.position.y + self.sprite.get_size()[1] > GROUND_HEIGHT):
            self.onGround = True
            self.position.y = GROUND_HEIGHT - self.sprite.get_size()[1]
            self.speed = vector(0, 0)


class Near_Enemy(Human): #근거리

    def __init__(self, hp = 150, mp = 0, atk = 10, arm = 0, cri = 0.1, position = (600,GROUND_HEIGHT)):
        super().__init__(hp, mp, atk, arm, cri)  
        self.position = vector(*position)
        self.speed = vector(0, 0) #속도. 매 프레임마다 위치+= 속도

        self.motion = 0  #모션
        self.viewdir = Vright #오른쪽
        self.onGround = True #캐릭터가 땅 위에 존재

        self.sting_cooltime = 0
        self.default_sting_cooltime = 60
        self.slash_cooltime = 0
        self.default_slash_cooltime = 20

        self.static_right_sprite = draw.sprite(['image/Enemy/static.png'], True, 1, self.position)
        self.static_left_sprite = self.static_right_sprite.flip(True, False) #좌우 대칭
        self.walk_right_sprite = draw.sprite(['image/Enemy/walk-' + str(i) + '.png' for i in range(1,5)], True, 6, self.position)
        self.walk_left_sprite = self.walk_right_sprite.flip(True, False)
        self.slash_right_sprite = draw.sprite(['image/Enemy/slash_' + str(i) + '.png' for i in range(1,3)], True, 2, self.position)
        self.slash_left_sprite = self.slash_right_sprite.flip(True, False)
        self.sting_right_sprite = draw.sprite(['image/Enemy/sting_' + str(i) + '.png' for i in range(1,3)], True, 2, self.position)
        self.sting_left_sprite = self.sting_right_sprite.flip(True, False)
        self.get_attack_right_sprite = draw.sprite(['image/Enemy/get_attack_1.png'], True, 3, self.position)
        self.get_attack_left_sprite = self.get_attack_right_sprite.flip(True, False)

        self.dead_right_sprite = draw.sprite(['image/Enemy/get_attack_3.png'], True, 2, self.position)
        self.dead_left_sprite = self.dead_right_sprite.flip(True, False)

        self.sprite = self.static_right_sprite

        self.hitbox = hitbox(self, self.position.x, self.position.y, *self.sprite.get_size(), 'static')
        self.atk_hitbox = hitbox(self, self.position.x, self.position.y, *self.sprite.get_size(), 'attack')
        self.stop()

    def jump(self): #점프
        self.atk_hitbox.check = False
        if self.onGround:
            self.onGround = False
            self.speed.y = JUMP_SPEED
            if self.viewdir == Vright:
                self.sprite = self.static_right_sprite
            if self.viewdir == Vleft:
                self.sprite = self.static_left_sprite

    def left(self): #좌측 보기?
        self.atk_hitbox.check = False
        self.viewdir = Vleft

    def right(self): #우측 보기?
        self.atk_hitbox.check = False
        self.viewdir = Vright

    def walk(self): #보고 있는 방향으로 이동?
        self.atk_hitbox.check = False
        if (self.viewdir == Vleft):
            self.position.x -= MOVE_SPEED
            self.sprite = self.walk_left_sprite
            self.hitbox.move(self.position)
            self.atk_hitbox.move(self.position)
        elif (self.viewdir == Vright):
            self.position.x += MOVE_SPEED
            self.sprite = self.walk_right_sprite
            self.hitbox.move(self.position)
            self.atk_hitbox.move(self.position)

    def stop(self):
        self.atk_hitbox.check = False
        self.speed.x = 0
        if self.viewdir == Vright:
            self.sprite = self.static_right_sprite
        if self.viewdir == Vleft:
            self.sprite = self.static_left_sprite

    def near_ai(self, other): #이동 메서드 추가
        if(self.act != 'stop'):
            return #다른 동작중이면 아무 것도 하지 않는다

        dist = self.position.x - other.position.x
        if -20 < dist < 20:
            if(random.random() < 0.5):
                self.slash()
            else:
                self.slash()
        elif -70 < dist < 70:
            self.stop()
            self.sting()

        elif dist >= 70:
            self.left()
            self.walk()
        else:
            self.right()
            self.walk()
        
    def sting(self):
        self.atk_hitbox.check = True
        if (self.sting_cooltime > 0):
            pass
        else:
            self.act = 'sting'
            self.actframe = 6
            self.sting_cooltime = self.default_sting_cooltime
            if (self.viewdir == Vleft):
                self.sprite = self.sting_left_sprite
            elif (self.viewdir == Vright):
                self.sprite = self.sting_right_sprite

    def slash(self):
        self.atk_hitbox.check = True
        if (self.slash_cooltime > 0):
            pass
        else:
            self.act = 'slash'
            self.actframe = 6
            self.slash_cooltime = self.default_slash_cooltime
            if (self.viewdir == Vleft):
                self.sprite = self.slash_left_sprite
            elif (self.viewdir == Vright):
                self.sprite = self.slash_right_sprite


    def get_attack(self, other, memo=''):
        if (memo == 'attack'):
            self.rigidity()
            self.hp -= (other.atk - self.arm)
            if other.cri <= random.random():
                self.hp -= (other.atk * 2 - self.arm)
            if(self.hp <= 0):
                self.dead()
        else:
            pass
        
    def rigidity(self):
        self.atk_hitbox.check = False
        self.act = 'stun'
        self.actframe = 10
        if (self.viewdir == Vleft):
            self.sprite = self.get_attack_left_sprite
            self.position.x += 40
        elif (self.viewdir == Vright):
            self.sprite = self.get_attack_right_sprite
            self.position.x -= 40
        else:
            pass

    def dead(self):
        self.act = 'dead'
        self.actframe = -1 # 1씩 감소하면 0이 될 일은 없으니까?? 테스트
        self.atk_hitbox.check = False
        self.hitbox.check = False
        if self.hp <= 0:
            if (self.viewdir == Vleft):
                self.sprite = self.dead_left_sprite
            elif (self.viewdir == Vright):
                self.sprite = self.dead_right_sprite
        else:
            pass

    def image_update(self):
        self.sprite.move(self.position)
        self.sprite.image_update()

    def update(self):
        if(self.act != 'stop'):
            self.actframe -= 1
            if(self.actframe == 0):
                self.act = 'stop'
        self.hitbox.move(self.position)
        self.hitbox.resize(*self.sprite.get_size())
        self.atk_hitbox.move(self.position)
        self.atk_hitbox.resize(*self.sprite.get_size())
        self.sting_cooltime -= 1
        self.slash_cooltime -= 1
        self.position += self.speed

        if(self.position.x < MAP_LEFT_LIMIT): #self.position.left < MAP_LEFT_LIMIT
            self.position.x = MAP_LEFT_LIMIT
        if(self.position.x + self.sprite.get_size()[0] > MAP_RIGHT_LIMIT):
            self.position.x = MAP_RIGHT_LIMIT - self.sprite.get_size()[0]

        if not self.onGround:
            self.speed += GRAVITY_CONSTANT
        if(self.position.y + self.sprite.get_size()[1] > GROUND_HEIGHT):
            self.onGround = True
            self.position.y = GROUND_HEIGHT - self.sprite.get_size()[1]
            self.speed = vector(0, 0)

        if self.hp <= 0:
            self.dead()


class Distance_Enemy(Human): #원거리

    def __init__(self, hp = 250, mp = 0, atk = 15, arm = 5, cri = 0, position = (600,GROUND_HEIGHT)):
        super().__init__(hp, mp, atk, arm, cri)
        self.position = vector(*position)
        self.speed = vector(0, 0) #속도. 매 프레임마다 위치+= 속도

        self.motion = 0  #모션
        self.viewdir = Vright #오른쪽
        self.onGround = True #캐릭터가 땅 위에 존재

        self.static_right_sprite = draw.sprite(['image/Enemy_D/static_D.png'], True, 1, self.position) #sprite 수정 필요
        self.static_left_sprite = self.static_right_sprite.flip(True, False) #좌우 대칭
        self.walk_right_sprite = draw.sprite(['image/Enemy_D/walk-' + str(i) + '_D.png' for i in range(1,5)], True, 6, self.position)
        self.walk_left_sprite = self.walk_right_sprite.flip(True, False)
        self.shoot_right_sprite = draw.sprite(['image/Enemy_D/shoot_' + str(i) + '.png' for i in range(1,3)], True, 2, self.position)
        self.shoot_left_sprite = self.shoot_right_sprite.flip(True, False)
        self.get_attack_right_sprite = draw.sprite(['image/Enemy/get_attack_1.png'], True, 3, self.position)
        self.get_attack_left_sprite = self.get_attack_right_sprite.flip(True, False)

        self.dead_right_sprite = draw.sprite(['image/Enemy/get_attack_3.png'], True, 2, self.position)
        self.dead_left_sprite = self.dead_right_sprite.flip(True, False)

        self.sprite = self.static_right_sprite
        self.shoot_cooltime = 0
        self.default_shoot_cooltime = 30

        self.act = 'stop'
        self.hitbox = hitbox(self, self.position.x, self.position.y, *self.sprite.get_size(), 'static')
        self.atk_hitbox = hitbox(self, self.position.x, self.position.y, *self.sprite.get_size(), 'attack')
        self.stop()

    def jump(self): #점프
        self.atk_hitbox.check = False
        if self.onGround:
            self.onGround = False
            self.speed.y = JUMP_SPEED
            if self.viewdir == Vright:
                self.sprite = self.static_right_sprite
            if self.viewdir == Vleft:
                self.sprite = self.static_left_sprite

    def left(self): #좌측 방향
        self.atk_hitbox.check = False
        self.viewdir = Vleft

    def right(self): #우측 방향
        self.atk_hitbox.check = False
        self.viewdir = Vright

    def walk(self): # 이동
        self.atk_hitbox.check = False
        if (self.viewdir == Vleft):
            self.position.x -= MOVE_SPEED
            self.sprite = self.walk_left_sprite
            self.hitbox.move(self.position)
            self.atk_hitbox.move(self.position)
        elif (self.viewdir == Vright):
            self.position.x += MOVE_SPEED
            self.sprite = self.walk_right_sprite
            self.hitbox.move(self.position)
            self.atk_hitbox.move(self.position)

    def stop(self): #멈춤
        self.atk_hitbox.check = False
        self.speed.x = 0
        if self.viewdir == Vright:
            self.sprite = self.static_right_sprite
        if self.viewdir == Vleft:
            self.sprite = self.static_left_sprite

    def shoot(self):
        self.atk_hitbox.check = True

        if (self.shoot_cooltime > 0):
            pass
        else:
            self.act = 'attack'
            self.actframe = 3
            self.shoot_cooltime = self.default_shoot_cooltime
            if (self.viewdir == Vleft):
                self.sprite = self.shoot_left_sprite
            elif (self.viewdir == Vright):
                self.sprite = self.shoot_right_sprite

    def get_attack(self, other, memo=''): #피격 판정. other:Human에게 (memo:str)형태로
        if (memo == 'attack'):
            self.rigidity()
            self.hp -= (other.atk - self.arm)
            if other.cri <= random.random():
                self.hp -= (other.atk * 2 - self.arm)
            if(self.hp <= 0):
                self.dead()
        else:
            pass

    def rigidity(self): #경직
        self.atk_hitbox.check = False
        self.act = 'stun'
        self.actframe = 10
        if (self.viewdir == Vleft):
            self.sprite = self.get_attack_left_sprite
            self.position.x += 40
        else:
            self.sprite = self.get_attack_right_sprite
            self.position.x -= 40

    def distance_ai(self, other): #모션은 기존의 찌르기/베기 모션을 오버라이딩함.
        if (self.act != 'stop'):
            return

        dist = self.position.x - other.position.x
        if 0 <= dist < 300:
            self.right()
            self.walk()
        elif -300 < dist <= 0:
            self.left()
            self.walk()

        elif dist >= 300 and self.position.x < MAP_RIGHT_LIMIT:
            self.left()
            self.stop()
            self.shoot()
        else:
            self.right()
            self.stop()
            self.shoot()

    def dead(self): #사망
        self.act = 'dead'
        self.actframe = -1 # 1씩 감소하면 0이 될 일은 없으니까?? 테스트
        self.atk_hitbox.check = False
        self.hitbox.check = False
        if self.hp <= 0:
            if (self.viewdir == Vleft):
                self.sprite = self.dead_left_sprite
            elif (self.viewdir == Vright):
                self.sprite = self.dead_right_sprite
        else:
            pass

    def update(self): #캐릭터 상태 업데이트: 캐릭터의 스텟이나 위치 등 상태만 업데이트 한다. 내부에서 이미지 업데이트를 부르지 말자.
        if(self.act != 'stop'):
            self.actframe -= 1
            if(self.actframe == 0):
                self.act = 'stop'
        self.hitbox.move(self.position)
        self.hitbox.resize(*self.sprite.get_size())
        self.position += self.speed

        if(self.position.x < MAP_LEFT_LIMIT): #self.position.left < MAP_LEFT_LIMIT
            self.position.x = MAP_LEFT_LIMIT
        if(self.position.x + self.sprite.get_size()[0] > MAP_RIGHT_LIMIT):
            self.position.x = MAP_RIGHT_LIMIT - self.sprite.get_size()[0]
        
        self.shoot_cooltime -= 1

        if not self.onGround:
            self.speed += GRAVITY_CONSTANT
        if(self.position.y + self.sprite.get_size()[1] > GROUND_HEIGHT):
            self.onGround = True
            self.position.y = GROUND_HEIGHT - self.sprite.get_size()[1]
            self.speed = vector(0, 0)

        if self.hp <= 0:
            self.dead()

    def image_update(self): # 캐릭터 이미지 업데이트: 스프라이트 이미지만 업데이트 한다. 내부에서 상태 업데이트를 부르지 말자.
        self.sprite.move(self.position)
        self.sprite.image_update()

class Projectile: #투사체, 원거리 적 클래스를 불러와야 하나?
    def __init__(self, position, speed, damage, getGravity=False):
        self.position = vector(*position)
        self.speed = vector(*speed)

        self.sprite_right = draw.sprite(['image/Enemy_D/arrow.png'], True, 1, self.position)
        self.sprite_left = self.sprite_right.flip(True, False)
        if(self.speed.x < 0): #왼쪽으로 날아가고 있을 때
            self.sprite = self.sprite_left
        else:
            self.sprite = self.sprite_right
        self.viewdir = Vright

        self.damage = damage
        self.getGravity = getGravity
        self.hitbox = hitbox(self, *self.position, *self.sprite.get_size(), 'attack')

    def update(self):
        if(self.getGravity):
            self.speed += GRAVITY_CONSTANT
        self.position += self.speed
        self.sprite.move(self.position)

    def image_update(self):
        pass

    def draw(self, surf):
        self.sprite.draw(surf)

    def get_attack(self):
        pass