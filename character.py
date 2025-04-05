import random

class Character:
    def __init__(self):
        small_dice_options = list(range(1, 7))
        big_dice_options = list(range(1, 21))

        self._combat_strength = random.choice(small_dice_options)
        self._health_points = random.choice(big_dice_options)

    def __del__(self):
        print("    |    Character object is being destroyed.")

    @property
    def combat_strength(self):
        return self._combat_strength

    @combat_strength.setter
    def combat_strength(self, value):
        self._combat_strength = min(6, value)

    @property
    def health_points(self):
        return self._health_points

    @health_points.setter
    def health_points(self, value):
        self._health_points = value

# functions.py
import random
import os

def use_loot(belt, health_points):
    good_loot_options = ["Health Potion", "Leather Boots"]
    bad_loot_options = ["Poison Potion"]

    print("    |    !!You see a monster in the distance! So you quickly use your first item:")
    first_item = belt.pop(0)
    if first_item in good_loot_options:
        health_points = min(20, (health_points + 2))
        print("    |    You used " + first_item + " to up your health to " + str(health_points))
    elif first_item in bad_loot_options:
        health_points = max(0, (health_points - 2))
        print("    |    You used " + first_item + " to hurt your health to " + str(health_points))
    else:
        print("    |    You used " + first_item + " but it's not helpful")
    return belt, health_points

def collect_loot(loot_options, belt):
    print("    |    !!You find a loot bag!! You look inside to find 2 items:")
    loot_roll = random.choice(range(1, len(loot_options) + 1))
    loot = loot_options.pop(loot_roll - 1)
    belt.append(loot)
    print("    |    Your belt: ", belt)
    return loot_options, belt

def hero_attacks(combat_strength, m_health_points):
    print("    |    Player's weapon (" + str(combat_strength) + ") ---> Monster (" + str(m_health_points) + ")")
    if combat_strength >= m_health_points:
        m_health_points = 0
        print("    |    You have killed the monster")
    else:
        m_health_points -= combat_strength
        print("    |    You have reduced the monster's health to: " + str(m_health_points))
    return m_health_points

def monster_attacks(m_combat_strength, health_points):
    print("    |    Monster's Claw (" + str(m_combat_strength) + ") ---> Player (" + str(health_points) + ")")
    if m_combat_strength >= health_points:
        health_points = 0
        print("    |    Player is dead")
    else:
        health_points -= m_combat_strength
        print("    |    The monster has reduced Player's health to: " + str(health_points))
    return health_points

def inception_dream(num_dream_lvls):
    num_dream_lvls = int(num_dream_lvls)
    if num_dream_lvls == 1:
        print("    |    You are in the deepest dream level now")
        print("    |", end="    ")
        input("Start to go back to real life? (Press Enter)")
        print("    |    You start to regress back through your dreams to real life.")
        return 2
    else:
        return 1 + int(inception_dream(num_dream_lvls - 1))

def save_game(winner, hero_name="", num_stars=0):
    monster_kills = 0
    try:
        with open("save.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                if "Total monsters killed:" in line:
                    monster_kills = int(line.split(":")[1].strip())
    except FileNotFoundError:
        pass

    with open("save.txt", "a") as file:
        if winner == "Hero":
            file.write(f"Hero {hero_name} has killed a monster and gained {num_stars} stars.\n")
            file.write(f"Total monsters killed: {monster_kills + 1}\n")
        elif winner == "Monster":
            file.write("Monster has killed the hero previously\n")
            file.write(f"Total monsters killed: {monster_kills}\n")

def load_game():
    monster_kills = 0
    try:
        with open("save.txt", "r") as file:
            print("    |    Loading from saved file ...")
            lines = file.readlines()
            if lines:
                last_line = lines[-2].strip()
                for line in lines:
                    if "Total monsters killed:" in line:
                        monster_kills = int(line.split(":")[1].strip())
                print(last_line)
                print(f"Total monsters killed: {monster_kills}")
                return last_line, monster_kills
    except FileNotFoundError:
        print("No  games found. Starting again from the start.")
        return None, 0

def adjust_combat_strength(combat_strength, m_combat_strength):
    last_game, total_kills = load_game()
    if last_game:
        if "Hero" in last_game and "gained" in last_game:
            num_stars = int(last_game.split()[-2])
            if num_stars > 3:
                print("    |    ... Increasing the monster's combat strength since you won so easily last time")
                m_combat_strength += 1
        elif "Monster has killed the hero" in last_game:
            combat_strength += 1
            print("    |    ... Increasing the hero's combat strength since you lost last time")
        else:
            print("    |    ... Based on your previous game, neither the hero nor the monster's combat strength will be increased")
    return combat_strength, m_combat_strength

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

# monster.py
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