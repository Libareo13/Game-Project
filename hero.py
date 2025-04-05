# hero.py
import random
from character import Character

class Hero(Character):
    def __init__(self, name="Hero"):
        super().__init__() # Initialize base Character (sets default random stats)
        # Override stats with Hero-specific ranges
        self.name = name
        self.type = "Generic"
        self.level = 1
        self.xp = 0
        self._combat_strength = random.randint(5, 20) # Hero specific range
        self._health_points = random.randint(50, 100) # Hero specific range
        print(f"    |    Hero ({self.name}) initial combat strength: {self._combat_strength}")
        print(f"    |    Hero ({self.name}) initial health points: {self._health_points}")

    @property
    def combat_strength(self):
        return self._combat_strength

    @combat_strength.setter
    def combat_strength(self, value):
        # Keep original validation
        if value < 0:
            # Instead of raising error, maybe cap at 0? Or keep error? Keep error for now.
             raise ValueError("Combat strength cannot be negative.")
        # Should there be an upper cap based on level or class? Not implemented yet.
        self._combat_strength = value

    @property
    def health_points(self):
        return self._health_points

    @health_points.setter
    def health_points(self, value):
        # Keep original validation/logic
        # if value < 0: # Base class setter already handles max(0, value)
        #     raise ValueError("Health points cannot be negative.")
        # Cap health at a max? e.g. 100 or based on level? Let's cap at 100 for now.
        self._health_points = max(0, min(100, value)) # Ensure health is between 0 and 100

    def __del__(self):
        # print("    |    Character object is being destroyed.") # Called by super's del if needed
        print(f"    |    The Hero object ({self.name}) is being destroyed") # Removed "by garbage collector"

    def hero_attacks(self, monster):
         # Uses the hero_attacks function from functions.py now
         # Kept for potential specific hero attack logic later if needed
        print(f"    |    Player's weapon ({self.combat_strength}) ---> Monster ({monster.health_points})")
        if self.combat_strength >= monster.health_points:
            monster.health_points = 0
            print("    |    You have killed the monster")
        else:
            monster.health_points -= self.combat_strength
            print(f"    |    You have reduced the monster's health to: {monster.health_points}")
        # The function version returns the value, this method modifies in place
        # To keep consistency maybe call the function one?
        # For now, keep original method logic.
        # return monster.health_points # Original didn't return here


# --- Keep the specific Hero classes ---
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