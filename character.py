import random

class Character:
    def __init__(self):
        small_dice_options = list(range(1, 7))
        big_dice_options = list(range(1, 21))

        # Initial strength/health set here, potentially overridden by subclasses
        self._combat_strength = random.choice(small_dice_options)
        self._health_points = random.choice(big_dice_options)

    def __del__(self):
        print("    |    Character object is being destroyed.")

    @property
    def combat_strength(self):
        return self._combat_strength

    @combat_strength.setter
    def combat_strength(self, value):
        # Assign directly — Hero/Monster classes handle their own validation
        self._combat_strength = value

    @property
    def health_points(self):
        return self._health_points

    @health_points.setter
    def health_points(self, value):
        # Prevent negative health at base level
        self._health_points = max(0, value)
