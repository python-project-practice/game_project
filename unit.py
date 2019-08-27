import game_project
import pygame
import UI
import draw
from abc import *

units = {'enemy':[], 'projectile':[]}
painter = None

class unitSet(draw.drawable, metaclass=ABCMeta): #지금은 하는 것은 없다. 유닛 하나와 관련된 것을 다루는 클래스임을 명시.
    def draw(self, surf):
        self.character.draw(surf)
        self.UI.draw(surf)

    def image_update(self):
        self.character.image_update()
        self.UI.image_update()


class characterSet(unitSet): #캐릭터와 캐릭터 UI등 하나의 캐릭터와 관련된 모든 것을 포함, 관리하는 클래스.
    def __init__(self, character): #캐릭터와 UI 속성 등을 넣어주면 그걸 토대로 클래스를 초기화한다. UI생성 방법은 모두 동일하니 고정.
        assert isinstance(character, game_project.Character) #character에는 Character 인스턴스만 허용.
        self.character = character
        self.UI = UI.Character_stat(self.character, pos=(5, 5)) #UI는 알아서 생성한다.

    def control(self, keys):
        return self.character.control(keys)

    def update(self):
        return self.character.update()


class nearenemySet(unitSet): #근거리 공격 적과 그 UI등 하나의 근거리 적과 관련된 모든 것을 포함, 관리하는 클래스.
    def __init__(self, enemy): #적과 UI 속성 등을 넣어주면 그걸 토대로 클래스를 초기화한다. UI생성방법은 모두 동일하니 고정.
        assert isinstance(enemy, game_project.Near_Enemy)
        self.character = enemy
        self.UI = UI.Enemy_stat(self.character, pos=(0, 180))
    
    def ai(self, other):
        return self.character.near_ai(other)

    def update(self):
        return self.character.update()

class farenemySet(unitSet):
    def __init__(self, enemy):
        assert isinstance(enemy, game_project.Distance_Enemy)
        self.character = enemy
        self.UI = UI.Enemy_stat(self.character, pos=(0,180))

    def ai(self, other):
        return self.character.distance_ai(other)

    def update(self):
        return self.character.update()

class projectileSet(unitSet):
    def __init__(self, enemy):
        assert isinstance(enemy, game_project.Projectile)
        self.character = enemy
        self.UI = None

    def image_update(self):
        self.character.image_update()

    def draw(self, surf):
        self.character.draw(surf)

    def update(self):
        self.character.update()