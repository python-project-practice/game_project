"""draw image or sprite using pygame."""

import pygame
from vector import vector

class image():
    '''
    image(file, alpha=False, pos=(0,0), adjust_pos=(0,0))
        file = filename, image or surface
        alpha = whether to use convert_alpha()
        pos = drawing point(leftup)
        adjust_pos = drawing point(use when you need to adjust start position of image. not_accesible)
            works like sceen.blit(pos + adjust_pos)

        get()-> return surface that image have.
        get_size()->(size x, size y)
        set_size(x,y)-> set size to x, y
        flip(x_bool, y_bool): flip by x axis and(or) y axis
        move(x,y): set pos to x,y
        draw(surf): blit image on surf surface
        update(): do nothing, because image does!

    store image and blit on screen
    '''
    def __init__(self, file, alpha=False, pos=(0,0), adjust_pos=(0,0)): #alpha = 투명도
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

        self.imagesize = self.image.get_size()
        self.pos = vector(*pos)
        self.__adjust = vector(*adjust_pos)

    def get(self):
        return self.image

    def get_size(self):
        return self.imagesize

    def set_size(self, x, y):
        retimg = image(self)
        retimg.image = pygame.transform.scale(self.image, (x, y))
        return retimg

    def flip(self, xbool, ybool): #바꾼 이미지를 변환
        retimg = image(self)
        retimg.image = pygame.transform.flip(self.image, xbool, ybool)
        return retimg

    def move(self, pos):
        # assert pos[0] > 0 and pos[1] > 0
        self.pos = pos

    def draw(self, surf):
        surf.blit(self.image, (self.pos.x + self.__adjust.x, self.pos.y + self.__adjust.y))

    def image_update(self):
        # do absolutely nothing
        pass

class sprite:
    def __init__(self, imagenamelist = [], alpha=False, update_period = 1, pos=(0,0), adjust_pos = []):
        self.imagelist = [image(i, alpha, pos) for i in imagenamelist]
        self.pos = vector(*pos)
        self.__picindex = 0 # 몇 번째 사진을 비출 것인지
        self.update_period = update_period # 몇 프레임마다 사진을 갱신할 것인지
        self.__frame = 0 # 현재 생성 후 몇 프레임이 지났는지
        self.__len = len(self.imagelist)
        self.__adjust = adjust_pos
        if(len(imagenamelist) > len(adjust_pos)):
            t = len(imagenamelist) - len(adjust_pos)
            self.__adjust.extend([vector(0,0)] * t)
            del t
        else:
            self.__adjust = self.__adjust[:len(imagenamelist)]

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
        surf.blit(self.imagelist[self.__picindex].get(),
                  (self.pos.x + self.__adjust[self.__picindex].x, self.pos.y + self.__adjust[self.__picindex].y)
                 )

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
        self.bg = None
        self.__updatelist = []
        
    def append_bg(self, item, alpha=False):
        bg = image(item, alpha)
        bgsize = bg.get_size()
        bg = bg.set_size(bgsize[0] * self.surfsize[1] // bgsize[1], self.surfsize[1])
        self.__updatelist.append(bg)

    def append(self, item):
        assert 'draw' in dir(item)
        self.__updatelist.append(item)

    def draw(self):
        for i in self.__updatelist:
            i.draw(self.surf)

    def image_update(self):
        for i in self.__updatelist:
            i.image_update()
