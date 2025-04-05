from character import Character
import random

class Monster(Character):
    def __init__(self):
        super().__init__()
        # Monster keeps the base Character's initial random stats
        print(f"    |    Monster's initial combat strength: {self._combat_strength}")
        print(f"    |    Monster's initial health points: {self._health_points}")

    def __del__(self):
        # Note: super().__del__() isn't strictly necessary unless Character.__del__ had critical cleanup
        print("    |    The Monster object is being destroyed by the garbage collector")

    @property
    def combat_strength(self):
        return self._combat_strength

    @combat_strength.setter
    def combat_strength(self, value):
        # Monster specific limits if any (e.g. max 6 from original user input phase?)
        # Let's cap at 6 based on context.
        self._combat_strength = min(6, max(0, value))  # Cap between 0 and 6

    @property
    def health_points(self):
        return self._health_points

    @health_points.setter
    def health_points(self, value):
        # Setting health, ensuring it doesn't go below 0
        self._health_points = max(0, value)

    def monster_attacks(self, hero):
        # Uses the monster_attacks function from functions.py now
        # Kept for potential specific monster attack logic later if needed
        print(f"    |    Monster's Claw ({self.combat_strength}) ---> Player ({hero.health_points})")
        if self.combat_strength >= hero.health_points:
            hero.health_points = 0
            print("    |    Player is dead")
        else:
            hero.health_points -= self.combat_strength
            print(f"    |    The monster has reduced Player's health to: {hero.health_points}")
