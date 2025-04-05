# character.py
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
        # Ensure combat strength doesn't exceed a theoretical max if needed,
        # but Hero/Monster setters have their own logic.
        # For simplicity, just assign, letting Hero/Monster manage limits.
        self._combat_strength = value

    @property
    def health_points(self):
        return self._health_points

    @health_points.setter
    def health_points(self, value):
         # Ensure health doesn't go below 0 globally if needed
        self._health_points = max(0, value) # Prevent negative health at base level