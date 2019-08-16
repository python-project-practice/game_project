import vector
import game_project

class Character_stat:
    def __init__(self, character, pos=(0,0)):
        self.parent = character
        self.pos = vector(*pos)

    def set_pos(pos):
        self.pos = vector(*pos)

    def draw(self):
        pass

    def update(self):
        pass

class Enemy_stat:
    def __init__(self, enemy):
        pass

    def draw(self):
        pass

    def update(self):
        pass

class fps:
    def __init__(self):
        pass


player = Character()
enemy_1 = Near_Enemy()
enemy_2 = Distance_Enemy()

ch = Character_UI()
en = Enemy_UI()
ch.draw_hp(player.hp, enemy_1.slash, enemy_1.sting, enemy_1.shoot)
en.draw_E_hp()