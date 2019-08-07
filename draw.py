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
        assert len(pos) == 2
        # assert pos[0] > 0 and pos[1] > 0
        self.pos = pos

    def draw(self, surf):
        surf.blit(self.image, (self.pos.x, self.pos.y))

class sprite:
    def __init__(self, imagenamelist = [], alpha=False, pos=(0,0)):
        if alpha is True:
            self.imagelist = [pygame.image.load(i).convert_alpha() for i in imagenamelist]
        else:
            self.imagelist = [pygame.image.load(i) for i in imagenamelist]
        print(self.imagelist)
        self.pos = vector(*pos)
        self._frame = 0
        self._len = len(self.imagelist)

    def __len__(self):
        return self._len

    def get(self):
        return self.imagelist

    def get_size(self):
        return self.imagelist[0].get_size()

    def draw(self, surf):
        surf.blit(self.imagelist[self._frame], (self.pos.x, self.pos.y))

    def move(self, pos):
        assert len(pos) == 2
        self.pos = vector(*pos)

    def update(self):
        self._frame = (self._frame + 1) % len(self)

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