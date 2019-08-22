import pygame

class hitbox(pygame.Rect):
    def __init__(self, parent, x, y, width, height, memo = '', check=True): # 적, 캐릭터의 히트박스/위치/히트박스 넓이,특징
        super().__init__(x, y, width, height) #pygame 메서드 상속
        self.parent = parent # 캐릭터 or 적을 가리킴
        self.memo = memo # parent가 여러 종류의 히트 박스를 가질 경우 히트박스끼리 구분하기 위해서
        self.check = check
        
    def move(self, pos):
        self.left = pos[0]
        self.top = pos[1]

    def resize(self, width, height):
        self.width = width
        self.height = height

    def __repr__(self):
        return '<hitbox(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.width) + ', ' + str(self.height) + ')>'
    
    def __str__(self):
        return self.__repr__()


def collide_list_to_list(list1, list2): #히트박스로 이루어진 리스트
    for i in list1:
        if(i.check):
            indices = i.collidelistall(list2) #list2에 충돌되는 히트박스롤 넣음
            for j in indices:
                if(list2[j].check):
                    print('충돌 발생, ' + str(i) + str(list2[j]) + str(i.memo))
                    i.parent.get_attack(list2[j].parent, i.memo) #상호충돌을 호출
                    list2[j].parent.get_attack(i.parent, list2[j].memo)
