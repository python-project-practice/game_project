﻿import pygame

class hitbox(pygame.Rect):
    def __init__(self, parent, x, y, width, height, check=True): # 적, 캐릭터의 히트박스/위치/히트박스 넓이,특징
        super().__init__(x, y, width, height) #pygame 메서드 상속
        self.parent = parent # 캐릭터 or 적을 가리킴
        self.check = check

    def move(self, pos):
        self.left = pos[0]
        self.top = pos[1]

    def __repr__(self):
        return '<hitbox(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.width) + ', ' + str(self.height) + ')>'

    def __str__(self):
        return self.__repr__()

    def get_attack(self, other): # 피격 판정
        self.parent.get_attack(other)
        

def collide_list_to_list(list1, list2): #히트박스로 이루어진 리스트
    for i in list1:
        if(i.check):
            indices = i.collidelistall(list2) #list2에 충돌되는 히트박스롤 넣음
            for j in indices:
                if(list2[j].check):
                    print(str(i) + ' collided with ' + str(list2[j])) 
    #               i.get_attack(list2[j]) #상호충돌을 호출
    #               list2[j].get_attack(i) 
