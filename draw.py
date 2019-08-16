"""draw image or sprite using pygame."""

import pygame
from vector import vector

class image():
    def __init__(self, file, alpha=False, pos=(0,0)): #alpha = 투명도
        if type(file) is str:
            self.image = pygame.image.load(file)
            self.alpha = False
            if alpha:
                self.image = self.image.convert_alpha()
                self.alpha = True
        elif type(file) is image:
            self.image = file.image
            self.alpha = file.alpha
        elif type(file) is pygame.Surface:
            self.image = file
            self.alpha = alpha

        self.pos = vector(*pos)

    def get(self):
        return self.image

    def get_size(self):
        return self.image.get_size()

    def flip(self, xbool, ybool): #바꾼 이미지를 변환
        retimg = image(self)
        retimg.image = pygame.transform.flip(self.image, xbool, ybool)
        return retimg

    def move(self, pos):
        # assert pos[0] > 0 and pos[1] > 0
        self.pos = pos

    def draw(self, surf):
        surf.blit(self.image, (self.pos.x, self.pos.y))

    def image_update(self):
        # do absolutely nothing
        pass

class sprite:
    def __init__(self, imagenamelist = [], alpha=False, update_period = 1, pos=(0,0)):
        self.imagelist = [image(i, alpha, pos) for i in imagenamelist]
        self.pos = vector(*pos)
        self.__picindex = 0 # 몇 번째 사진을 비출 것인지
        self.update_period = update_period # 몇 프레임마다 사진을 갱신할 것인지
        self.__frame = 0 # 현재 생성 후 몇 프레임이 지났는지
        self.__len = len(self.imagelist)

    def __len__(self):
        return self.__len

    def __getitem__(self, index):
        return self.imagelist[index]

    def get(self):
        return self.imagelist

    def get_size(self):
        return self.imagelist[0].get_size()

    def flip(self, xbool, ybool):
        return sprite([i.flip(xbool, ybool) for i in self], update_period=self.update_period, pos=self.pos)

    def draw(self, surf):
        surf.blit(self.imagelist[self.__picindex].get(), (self.pos.x, self.pos.y))

    def move(self, pos):
        self.pos = vector(*pos)

    def image_update(self):
        self.__frame += 1
        if(self.__frame % self.update_period == 0):
            self.__picindex = (self.__picindex + 1) % len(self)

class painter:
    def __init__(self, surf):
        self.surf = surf
        self.surfsize = surf.get_size()
        self.__updatelist = []
        
    def draw_bg(self, filename, alpha=False):
        bg = image(filename, alpha)
        bgsize = bg.get_size()
        bg = pygame.transform.scale(bg.get(), (bgsize[0] * self.surfsize[1] // bgsize[1], self.surfsize[1]))
        self.surf.blit(bg, (0,0))

    def append(self, item):
        assert 'draw' in dir(item)
        self.__updatelist.append(item)

    def draw(self):
        for i in self.__updatelist:
            i.draw(self.surf)

    def image_update(self):
        for i in self.__updatelist:
            i.image_update()
