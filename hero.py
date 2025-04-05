# hero.py
import random
from character import Character

class Hero(Character):
    def __init__(self, name="Hero"):
        super().__init__()  # Initialize base Character (sets default random stats)
        # Override stats with Hero-specific ranges
        self.name = name
        self.type = "Generic"
        self.level = 1
        self.xp = 0
        self._combat_strength = random.randint(5, 20)  # Hero specific range
        self._health_points = random.randint(50, 100)  # Hero specific range
        print(f"    |    Hero ({self.name}) initial combat strength: {self._combat_strength}")
        print(f"    |    Hero ({self.name}) initial health points: {self._health_points}")

    @property
    def combat_strength(self):
        return self._combat_strength

    @combat_strength.setter
    def combat_strength(self, value):
        # Keep original validation
        if value < 0:
            raise ValueError("Combat strength cannot be negative.")
        # Should there be an upper cap based on level or class? Not implemented yet.
        self._combat_strength = value

    @property
    def health_points(self):
        return self._health_points

    @health_points.setter
    def health_points(self, value):
        # Cap health at a max of 100
        self._health_points = max(0, min(100, value))

    def __del__(self):
        print(f"    |    The Hero object ({self.name}) is being destroyed")

    def hero_attacks(self, monster):
        # Kept for potential specific hero attack logic later
        print(f"    |    Player's weapon ({self.combat_strength}) ---> Monster ({monster.health_points})")
        if self.combat_strength >= monster.health_points:
            monster.health_points = 0
            print("    |    You have killed the monster")
        else:
            monster.health_points -= self.combat_strength
            print(f"    |    You have reduced the monster's health to: {monster.health_points}")

# --- Specific Hero Types ---

class Warrior(Hero):
    def __init__(self, name):
        super().__init__(name)
        self.type = "Warrior"
        # Warrior specific adjustments? e.g., more health/strength
        # self._health_points += 10
        # self._combat_strength += 2
        print(f"    |    {self.name} the Warrior enters the battle!")
        # print(f"    |    Adjusted stats: HP={self.health_points}, Str={self.combat_strength}")

class Mage(Hero):
    def __init__(self, name):
        super().__init__(name)
        self.type = "Mage"
        # Mage specific adjustments? e.g., less health, maybe mana later?
        # self._health_points -= 5
        print(f"    |    {self.name} the Mage prepares their spells!")
        # print(f"    |    Adjusted stats: HP={self.health_points}, Str={self.combat_strength}")

class Archer(Hero):
    def __init__(self, name):
        super().__init__(name)
        self.type = "Archer"
        # Archer specific adjustments?
        print(f"    |    {self.name} the Archer takes aim!")
        # print(f"    |    Adjusted stats: HP={self.health_points}, Str={self.combat_strength}")
