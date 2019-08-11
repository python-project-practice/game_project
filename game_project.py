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

맵 / 규칙 설계
벨트 스크롤 형식이 아닌 스테이지 형식(적이 모두 죽으면 다음 스테이지로 넘어감)
적들을 죽이면 점수를 쌓도록 만듦(이거는 희망사항인데, 일정시간 내에 타격을 많이 하면 점수를 쌓도록 설계(콤보 시스템))
만약 적의 hp가 0이 될 경우, 타격 판정(경직)이 사라짐.

'''
from abc import *
import random
from pygame.locals import *
import draw
from vector import vector



Stop = 'stop'
Walk = 'walk'
Jump = 'jump'

Vleft = 'view_left'
Vright = 'view_right'

GROUND_HEIGHT = 350
GRAVITY_CONSTANT = vector(0, 4.0) # gain speed (rightward , downward) px per frame
MOVE_SPEED = 6
JUMP_SPEED = -40

# human 클래스에 character, enemy가 공유함
class Human(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, hp = 100, mp = 0, atk = 0, arm = 0, cri = 0.1): #기본 스텟/몹, 캐릭터의 위치 설계
        self.hp = hp
        self.mp = mp
        self.atk = atk
        self.arm = arm
        self.cri = cri

        self.position = 0  #위치
        self.motion = 0  #모션
        self.viewdir = Vright #오른쪽
        self.onGround = True #캐릭터가 땅 위에 존재

    @abstractmethod 
    def jump(self): #점프
        pass

    @abstractmethod
    def left(self): #좌측 이동
        pass

    @abstractmethod
    def right(self): #우측 이동
        pass

    @abstractmethod
    def stop(self):
        pass
    
    @abstractmethod
    def sting(self): #찌르기
        pass

    @abstractmethod
    def slash(self): # 베기
        pass

    @abstractmethod
    def get_attack(self): #피격 판정
        pass

    @abstractmethod
    def rigidity(self): #경직
        pass

    @abstractmethod
    def dead(self): #사망
        pass

class Character(Human):
    def __init__(self, hp = 100, mp = 0, atk = 0, arm = 0, cri = 0.1): #기본 스텟/몹, 캐릭터의 위치 설계
        self.hp = hp
        self.mp = mp
        self.atk = atk
        self.arm = arm
        self.cri = cri

        self.pos = vector(60, GROUND_HEIGHT)  #위치
        self.speed = vector(0, 0) #속도. 매 프레임마다 위치+= 속도
        self.motion = 0  #모션
        self.viewdir = Vright #오른쪽
        self.onGround = True #캐릭터가 땅 위에 존재

        self.sprite = None
        self.static_sprite = draw.sprite(['image/char/static.png'], True, 2, self.pos)
        self.walk_sprite = draw.sprite(['image/char/walk-' + str(i) + '.png' for i in range(1,4)],True, 5, self.pos)

        self.stop()
        
    def control(self, keys): #기본적인 조작법
        if keys[K_RIGHT]:
            self.right()

        elif keys[K_LEFT]:
            self.left()

        else:
            self.stop()


        if keys[K_UP]:
            self.jump()

        if keys[K_x]:
            self.sting()
        
        elif keys[K_z]:
            self.slash()
        
        else:
            pass

    def jump(self): #점프
        if self.onGround:
            self.onGround = False
            self.speed.y = JUMP_SPEED
            self.sprite = self.static_sprite

    def left(self): #좌측 이동
        self.speed.x = -MOVE_SPEED
        self.sprite = self.walk_sprite

    def right(self): #우측 이동
        self.speed.x = +MOVE_SPEED
        self.sprite = self.walk_sprite

    def stop(self):
        self.speed.x = 0
        self.sprite = self.static_sprite
    
    def sting(self): #찌르기
        pass

    def slash(self): # 베기
        pass

    def get_attack(self): #피격 판정
        pass

    def rigidity(self): #경직
        pass

    def dead(self): #사망
        pass

    def update(self):
        self.sprite.move(self.pos)
        self.sprite.update()
        self.pos += self.speed
        if not self.onGround:
            self.speed += GRAVITY_CONSTANT
        if(self.pos.y > GROUND_HEIGHT):
            self.onGround = True
            self.pos.y = GROUND_HEIGHT
            self.speed = vector(0, 0)
        
    def draw(self, surf):
        self.sprite.draw(surf)

class Near_Enemy(Human): #근거리

    def __init__(self):
        super().__init__(hp = 1500, mp = 0, atk = 15, arm = 10, cri = 0)

    def sting(self):
        while (self.hp == 0):
            Character().hp - (Character().arm - Near_Enemy().atk)

    def slash(self):
        while (self.hp == 0):
            Character().hp - (Character().arm - Near_Enemy().atk)

    def get_attack(self):
        if (True):
            pass

    def near_ai(self): #이동 메서드 추가
        distance = ((Character().position.x - Near_Enemy().position.x) ** 2 + (Character().position.y - Near_Enemy().position.y) ** 2) ** 0.5 
        if (distance < 100):
            Near_Enemy().slash() or Near_Enemy().sting()
        else:
            distance -= 10 #거리가 가까워짐


class Distance_Enemy(Human): #원거리

    def __init__(self):
        super().__init__(hp = 750, mp = 0, atk = 20, arm = 5, cri = 0)
    
    def sting(self): #활쏘기로 오버라이딩
        while (self.hp == 0):
            Character().hp - (Character().arm - Distance_Enemy().atk)


    def distance_ai(self): #모션은 기존의 찌르기/베기 모션을 오버라이딩함.
        distance = ((Character().position.x - Near_Enemy().position.x) ** 2 + (Character().position.y - Near_Enemy().position.y) ** 2) ** 0.5
        if (distance < 200):
            distance += 20
        else:
            self.sting()

class Boss(Near_Enemy, Distance_Enemy): #다중상속 -> 근/원거리 공격 포함

    def __init__(self):
        super().__init__()

    def slash(self):
        while True:
            pass
