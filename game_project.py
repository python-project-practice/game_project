from abc import *
import random

class Human(metaclass=ABCMeta):  #추상 클래스 -> Boss, Character, Enemy 클래스를 모두 아우름
    
    @abstractmethod
    def stat(self):

    @abstractmethod
    def motion(self):

class Character(Human):

    def __init__(self, ):       #캐릭터 스텟, 조작법, 모션등을 정의

    def stat(self):

    def motion(self):

    def menual(self):

class Enemy(Human):

class Boss(Enemy):


class Inventory(Character):                 #인벤토리 클래스 -> 캐릭터 클래스에 상속하여~~
    
    def item(self):
