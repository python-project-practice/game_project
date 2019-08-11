"""draw image or sprite using pygame."""

import pygame
from vector import vector
import random

class image:
    def __init__(self, filename, alpha=False, pos=(0,0)):
        self.image = pygame.image.load(filename)
        if alpha:
            self.image = self.image.convert_alpha()
        self.pos = vector(*pos)

    def get(self):
        return self.image

    def get_size(self):
        return self.image.get_size()

    def move(self, pos):
        # assert pos[0] > 0 and pos[1] > 0
        self.pos = pos

    def draw(self, surf):
        surf.blit(self.image, (self.pos.x, self.pos.y))

class sprite:
    def __init__(self, imagenamelist = [], alpha=False, update_period = 1, pos=(0,0)):
        if alpha is True:
            self.imagelist = [pygame.image.load(i).convert_alpha() for i in imagenamelist]
        else:
            self.imagelist = [pygame.image.load(i) for i in imagenamelist]
        self.pos = vector(*pos)
        self._picindex = 0 # 몇 번째 사진을 비출 것인지
        self.update_period = update_period # 몇 프레임마다 사진을 갱신할 것인지
        self._frame = 0 # 현재 생성 후 몇 프레임이 지났는지
        self._len = len(self.imagelist)

    def __len__(self):
        return self._len

    def get(self):
        return self.imagelist

    def get_size(self):
        return self.imagelist[0].get_size()

    def draw(self, surf):
        surf.blit(self.imagelist[self._picindex], (self.pos.x, self.pos.y))

    def move(self, pos):
        self.pos = vector(*pos)

    def update(self):
        self._frame += 1
        if(self._frame % self.update_period == 0):
            self._picindex = (self._picindex + 1) % len(self)

class painter:
    def __init__(self, surf, weather=None):
        self.surf = surf
        self.surfsize = surf.get_size()
        self._updatelist = []
        
    def draw_bg(self, filename, alpha=False):
        bg = image(filename, alpha)
        bgsize = bg.get_size()
        bg = pygame.transform.scale(bg.get(), (bgsize[0] * self.surfsize[1] // bgsize[1], self.surfsize[1]))
        self.surf.blit(bg, (0,0))

    def append(self, item):
        assert 'draw' in dir(item)
        self._updatelist.append(item)

    def draw(self):
        for i in self._updatelist:
            i.draw(self.surf)

    def update(self):
        for i in self._updatelist:
            i.update()
