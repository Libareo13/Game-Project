from character import Character
import random


class Monster(Character):
    def __init__(self):
        super().__init__()
        print(f"    |    Monster's initial combat strength: {self._combat_strength}")
        print(f"    |    Monster's initial health points: {self._health_points}")

    def __del__(self):
        super().__del__()
        print("    |    The Monster object is being destroyed by the garbage collector")

    def monster_attacks(self, hero):
        print(f"    |    Monster's Claw ({self._combat_strength}) ---> Player ({hero.health_points})")
        if self._combat_strength >= hero.health_points:
            hero.health_points = 0
            print("    |    Player is dead")
        else:
            hero.health_points -= self._combat_strength
            print(f"    |    The monster has reduced Player's health to: " + str(hero.health_points))
        return hero.health_points
