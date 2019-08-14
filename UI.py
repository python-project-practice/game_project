import game_project

class Character_UI:

    def draw_hp(self, hp):
        self.hp = hp
        if 

    def update(self):
        

class Enemy_UI:

    def draw_E_hp(self, hp, attack_C):




player = Character()
enemy_1 = Near_Enemy()
enemy_2 = Distance_Enemy()

ch = Character_UI()
en = Enemy_UI()
ch.draw_hp(player.hp, enemy_1.slash, enemy_1.sting, enemy_1.shoot)
en.draw_E_hp()