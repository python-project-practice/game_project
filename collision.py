import pygame

class hitbox(pygame.Rect):
    def __init__(self, parent, x, y, width, height):
        super().__init__(x, y, width, height)
        self.parent = parent

    def get_attack(self, other):
        self.parent.get_attack(other)

def collide_list_to_list(list1, list2):
    for i in list1:
        assert type(i) is hitbox
    for j in list2:
        assert type(j) is hitbox

    for i in list1:
        indices = i.collideRect(list2)
        for j in indices:
            i.get_attack(list2[j])
            list2[j].get_attack(i)
