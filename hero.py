# hero.py
import random
from character import Character

class Hero(Character):
    def __init__(self, name="Hero"):
        super().__init__()
        self.name = name
        self.type = "Generic"
        self.level = 1
        self.xp = 0
        self._combat_strength = random.randint(5, 20)
        self._health_points = random.randint(50, 100)
        print(f"    |    Hero's initial combat strength: {self._combat_strength}")
        print(f"    |    Hero's initial health points: {self._health_points}")

    @property
    def combat_strength(self):
        return self._combat_strength

    @combat_strength.setter
    def combat_strength(self, value):
        if value < 0:
            raise ValueError("Combat strength cannot be negative.")
        self._combat_strength = value

    @property
    def health_points(self):
        return self._health_points

    @health_points.setter
    def health_points(self, value):
        if value < 0:
            raise ValueError("Health points cannot be negative.")
        self._health_points = value

    def __del__(self):
        print("    |    The Hero object is being destroyed by the garbage collector")

    def hero_attacks(self, monster):
        print(f"    |    Player's weapon ({self._combat_strength}) ---> Monster ({monster.health_points})")
        if self._combat_strength >= monster.health_points:
            monster.health_points = 0
            print("    |    You have killed the monster")
        else:
            monster.health_points -= self._combat_strength
            print(f"    |    You have reduced the monster's health to: {monster.health_points}")
        return monster.health_points

class Warrior(Hero):
    def __init__(self, name):
        super().__init__(name)
        self.type = "Warrior"
        print(f"    |    {self.name} the Warrior enters the battle!")

class Mage(Hero):
    def __init__(self, name):
        super().__init__(name)
        self.type = "Mage"
        print(f"    |    {self.name} the Mage prepares their spells!")

class Archer(Hero):
    def __init__(self, name):
        super().__init__(name)
        self.type = "Archer"
        print(f"    |    {self.name} the Archer takes aim!")