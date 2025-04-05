import random
from character import Character

class Hero(Character):
    def __init__(self):
        # Call parent constructor to initialize combat_strength and health_points
        super().__init__()
        # Roll dice for combat strength and health points
        self._combat_strength = random.randint(5, 20)  # Combat strength between 5 and 20
        self._health_points = random.randint(50, 100)  # Health points between 50 and 100
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
        # Destructor
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
