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
from pygame.locals import *
import draw
from vector import vector

#++ 히트박스 클래스 고려하여 프로그래밍 ㄱㄱ

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

        self.position = vector(0, 0)  #위치
        self.speed = vector(0, 0) #속도, 매 프레임마다 위치+= 속도
        self.motion = 0  #모션
        self.viewdir = Vright #오른쪽
        self.onGround = True #캐릭터가 땅 위에 존재

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
    def stop(self): #멈춤/땅 위에 존재
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

    def __init__(self):
        super().__init__(hp = 100, mp = 0, atk = 30, arm = 10, cri = 0.1) #상속

        self.sprite = None
        self.position = vector(60, GROUND_HEIGHT)
        self.static_sprite = draw.sprite(['image/char/static.png'], True, 2, self.position)
        self.walk_sprite = draw.sprite(['image/char/walk-' + str(i) + '.png' for i in range(1,4)],True, 12, self.position)

        self.stop()
        
    def control(self, keys): #기본적인 조작법
        if keys[K_RIGHT]:
            self.right()
            self.walk()

        elif keys[K_LEFT]:
            self.left()
            self.walk()

        else:
            self.stop()


        if keys[K_UP] and self.onGround:
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

    def left(self): #좌측 보기?
    	self.viewdir = Vleft

    def right(self): #우측 보기?
    	self.viewdir = Vright

    def walk(self): #보고 있는 방향으로 이동?
    	if(self.viewdir == Vleft):
    		self.speed.x = -MOVE_SPEED
    	elif(self.viewdir == Vright):
    		self.speed.x = MOVE_SPEED
    	self.sprite = self.walk_sprite

    def stop(self):
        self.speed.x = 0
        self.sprite = self.static_sprite
    
    def rigidity(self):
    	pass

    def dead(self):
    	pass

    def get_attack(self): #피격 판정
        pass

    def rigidity(self): #경직
        pass

    def dead(self): #사망
        pass

    def slash(self):
        pass

    def sting(self):
        pass

    def update(self):
        self.sprite.move(self.position)
        self.sprite.update()
        self.position += self.speed
        if not self.onGround:
            self.speed += GRAVITY_CONSTANT
        if(self.position.y > GROUND_HEIGHT):
            self.onGround = True
            self.position.y = GROUND_HEIGHT
            self.speed = vector(0, 0)
        
    def draw(self, surf):
        self.sprite.draw(surf)

class Near_Enemy(Human): #근거리

    def __init__(self):
        Human.__init__(hp = 800, mp = 0, atk = 15, arm = 10, cri = 0)

    def sting(self, other):
        return other.hp - (other.arm - self.atk)

    def slash(self, other):
        return other.hp - (other.arm - self.atk)

    def get_attack(self, other):
        if other.slash() or other.sting():
            return #피격 상태 이미지로 출력 -> 추후에 경직 시간(후딜레이) 고려해야 함!

    def rigidity(self, other):
        if other.slash() or other.sting():
            self.get_attack()

    def near_ai(self, other): #이동 메서드 추가
        dist()
        if (dist() < 100):
            self.slash() or self.sting()
        else:
            pass
            #dist() -= 10 #거리가 가까워짐

    def dead(self):
        pass

class Distance_Enemy(Human): #원거리

    def __init__(self):
       Human.__init__(hp = 250, mp = 0, atk = 20, arm = 5, cri = 0)
    
    def sting(self ,other): #활쏘기로 오버라이딩
        return other.hp - (other.arm - self.atk)

    def get_attack(self, other):
        if other.slash() or other.sting():
            return #피격 상태 이미지 출력 -> 추후에 경직 시간(후딜레이)도 고려해야 함

    def rigidity(self, other):
        if other.slash() or other.sting():
            self.get_attack()

    def distance_ai(self, other): #모션은 기존의 찌르기/베기 모션을 오버라이딩함.
        dist()
        if (dist() < 200):
            dist += 20
        else:
            self.sting()

    def dead(self):
        pass

class Boss(Near_Enemy, Distance_Enemy): #다중상속 -> 근/원거리 공격 포함

    def __init__(self):
        Human.__init__(hp = 2000, mp = 0, atk = 25, arm = 10, cri = 0) #상속 코드 질문 다시 하기!!

    def slash(self, other):
        return other.hp - (other.arm - self.atk)

    def sting(self, other):
        return other.hp -(other.arm - self.atk)

    def get_attack(self, other):
        if other.slash or other.sting:
            return

    def rigidity(self):
        if other.slash or other.sting:
            self.get_attack()

    def boss_ai(self): #복잡해지면 근/원거리 ai로 나눌거다.
        dist()
        if dist() < 100:
            self.slash #필수인 공격주기는 나중에 짜기로!
        elif dist() > 100:
            self.sting #원거리 공격
        else:
            self.stop

    def dead(self):
        pass
