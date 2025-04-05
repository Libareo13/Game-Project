# main.py
import random
from hero import Warrior, Mage, Archer
from monster import Monster
import functions
import os
import platform

print(f"Operating System: {os.name}")
print(f"Python Version: {platform.python_version()}")

small_dice_options = list(range(1, 7))
big_dice_options = list(range(1, 21))
weapons = ["Fist", "Knife", "Club", "Gun", "Bomb", "Nuclear Bomb"]
loot_options = ["Health Potion", "Poison Potion", "Secret Note", "Leather Boots", "Flimsy Gloves"]
belt = []
monster_powers = {
    "Fire Magic": 2,
    "Freeze Time": 4,
    "Super Hearing": 6
}

all_powers = [
    {"name": "Warrior's Strike", "type": "Warrior", "level": 1},
    {"name": "Warrior's Rage", "type": "Warrior", "level": 3},
    {"name": "Warrior's Onslaught", "type": "Warrior", "level": 5},
    {"name": "Fireball", "type": "Mage", "level": 1},
    {"name": "Ice Storm", "type": "Mage", "level": 3},
    {"name": "Arcane Blast", "type": "Mage", "level": 5},
    {"name": "Precise Shot", "type": "Archer", "level": 1},
    {"name": "Multi-Shot", "type": "Archer", "level": 3},
    {"name": "Arrow Storm", "type": "Archer", "level": 5}
]

def select_hero():
    print("    |    Choose your hero:")
    print("    |    1. Warrior")
    print("    |    2. Mage")
    print("    |    3. Archer")

    while True:
        choice = input("    |    Enter your choice (1-3): ").strip()
        if choice == "1":
            return Warrior(input("    |    Enter Warrior's name: "))
        elif choice == "2":
            return Mage(input("    |    Enter Mage's name: "))
        elif choice == "3":
            return Archer(input("    |    Enter Archer's name: "))
        else:
            print("    |    Invalid choice. Please enter 1, 2, or 3.")

def get_hero_powers(hero):
    powers = []
    relics = []
    powers_by_type = [power["name"] for power in all_powers if power["type"] == hero.type]
    if hero.xp <= 5:
        if hero.level >= 1:
            powers.append(powers_by_type[0])
        if hero.level >= 3:
            powers.append(powers_by_type[1])
        if hero.level >= 5:
            powers.append(powers_by_type[2])
    elif hero.xp > 5:
        if hero.level >= 1:
            powers.append(powers_by_type[0])
            relics.append('Health Boost')
        if hero.level >= 3:
            powers.append(powers_by_type[1])
            relics.append('Mana Regeneration')
        if hero.level >= 5:
            powers.append(powers_by_type[2])
            relics.append('Critical Hit Chance')
    return powers, relics

def level_up(hero):
    hero.level +=1
    print(f"{hero.name} has reached level {hero.level}!")

def gain_xp(hero, xp):
    hero.xp += xp
    print(f"{hero.name} gained {xp} XP.")
    if hero.xp >= 10:
        level_up(hero)
        hero.xp = 0

last_game_result, monsters_killed_line = functions.load_game()

if monsters_killed_line:
    try:
        monsters_killed = int(monsters_killed_line.split(": ")[1])
        print(f"Total monsters killed: {monsters_killed}")
    except:
        print("Error loading monster kills.")
else:
    print("No monster kill data found.")

hero = select_hero()
monster = Monster()
num_stars = 0

input_invalid = True
i = 0

while input_invalid and i < 5:
    print("    ------------------------------------------------------------------")
    print("    |", end="    ")
    combat_strength = input("Enter your combat Strength (1-6): ").strip()
    print("    |", end="    ")
    m_combat_strength = input("Enter the monster's combat Strength (1-6): ").strip()

    if (not combat_strength.isdigit()) or (not m_combat_strength.isdigit()):
        print("    |    One or more invalid inputs. Player needs to enter integer numbers for Combat Strength    |")
        i += 1
        continue

    combat_strength = int(combat_strength)
    m_combat_strength = int(m_combat_strength)

    if combat_strength not in range(1, 7) or m_combat_strength not in range(1, 7):
        print("    |    Enter a valid integer between 1 and 6 only")
        i += 1
        continue

    input_invalid = False

input("Rolling the dice for your weapon... (Press enter)")
weapon_roll = random.choice(small_dice_options)
combat_strength = min(6, (int(combat_strength) + weapon_roll))
print("    |    The hero\'s weapon is " + str(weapons[weapon_roll - 1]))

hero.combat_strength, monster.combat_strength = functions.adjust_combat_strength(hero.combat_strength, monster.combat_strength)

print(f"Hero health points: {hero.health_points}")
print(f"Monster health points: {monster.health_points}")

for _ in range(2):
    input("Roll for loot (Press enter)")
    loot_options, belt = functions.collect_loot(loot_options, belt)
belt.sort()
print("Your belt contains:", belt)

belt, hero.health_points = functions.use_loot(belt, hero.health_points)

input("Roll for Monster's Magic Power (Press enter)")
power_roll = random.choice(list(monster_powers.keys()))
monster.combat_strength = min(6, monster.combat_strength + monster_powers[power_roll])
print(f"Monster's combat strength is now {monster.combat_strength} using {power_roll}")

print("    ------------------------------------------------------------------")
print("You meet the monster. FIGHT!! FIGHT !!")
while monster.health_points > 0 and hero.health_points > 0:
    input("Roll to see who strikes first (Press Enter)")
    attack_roll = random.choice(small_dice_options)
    match attack_roll % 2:
        case 0:
            input("The Monster strikes (Press enter)")
            hero.health_points = functions.monster_attacks(monster.combat_strength, hero.health_points)
        case _:
            input("You strike (Press enter)")
            monster.health_points = functions.hero_attacks(hero.combat_strength, monster.health_points)

winner = "Hero" if monster.health_points <= 0 else "Monster"

def get_hero_name():
    for _ in range(5):
        hero_name = input("Enter your Hero's name (in two words): ").strip()
        name_p = hero_name.split()
        if len(name_p) == 2 and all(part.isalpha() for part in name_p):
            s_name = name_p[0][:2] + name_p[1][0]
            print(f"I'm going to call you {s_name} for short.")
            return s_name
        else:
            print("Invalid name. Please enter two words (letters only).")
    return "Hero"

short_name = get_hero_name()
functions.save_game(winner, hero_name=short_name, num_stars=3 if winner == "Hero" else 1)
gain_xp(hero, 5)
gain_xp(hero, 5)
powers, relics = get_hero_powers(hero)
print(f"{hero.name}'s powers: {powers}")
print(f"{hero.name}'s relics: {relics}")