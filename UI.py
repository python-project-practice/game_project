import pygame
from vector import vector
import game_project

RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Character_stat:
    def __init__(self, character, pos=(0,0)):
        self.parent = character
        self.pos = vector(*pos)

    def set_pos(self, pos):
        self.pos = vector(*pos)

    def draw(self, surf):
        if self.parent.hp > 0:
            pygame.draw.rect(surf, RED, [self.pos.x, self.pos.y, self.parent.hp, 30])
        if self.parent.mp > 0:
            pygame.draw.rect(surf, BLUE, [self.pos.x, self.pos.y + 50, self.parent.mp, 30])

    def image_update(self):
        pass

class Enemy_stat:
    def __init__(self, enemy, pos):
        self.parent = enemy
        self.pos = vector(*pos)

    def set_pos(self, pos):
        self.pos = vector(*pos)

    def draw(self, surf):
        if self.parent.hp > 0:
            pygame.draw.rect(surf, BLUE, [self.parent.position.x + self.pos.x,
                                          self.parent.position.y + self.pos.y,
                                          self.parent.hp, 10])
        else:
            pass

    def image_update(self):
        pass

class fps:
    def __init__(self, pos):
        pass
