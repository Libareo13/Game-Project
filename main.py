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
# Weapons list
weapons = ["Fist", "Knife", "Club", "Gun", "Bomb", "Nuclear Bomb", "Bat", "Machete", "Sword", "Bow", "Axe"]
# Loot options
loot_options = ["Health Potion", "Poison Potion", "Secret Note", "Leather Boots", "Flimsy Gloves", "Golden Coin"]
belt = []
#armor options
armor = ["Helmet", "Chestplate", "Shield"]


# Filtering by Good and Bad
good_loot = [item for item in loot_options if item == "Health Potion"]
bad_loot = [item for item in loot_options if item == "Poison Potion"]
good_weapons = [item for item in weapons if (item in ["Fist", "Knife", "Sword", "Axe"]) and item != "Nuclear Bomb"]
bad_weapons = [item for item in weapons if item == "Bomb" or item == "Nuclear Bomb"]
good_armor = [item for item in armor if (item == "Helmet" or item == "Chestplate") and item != "Shield"]
bad_armor = [item for item in armor if item == "Shield"]

# Filtering by Usefulness
useful_loot = [item for item in loot_options if item in ["Health Potion", "Leather Boots", "Flimsy Gloves"]]
not_useful_loot = [item for item in loot_options if item == "Secret Note"]
useful_weapons = [item for item in weapons if (item in ["Fist", "Knife", "Sword", "Axe"]) and item != "Gun"]
not_useful_weapons = [item for item in weapons if item == "Bomb" or item == "Nuclear Bomb"]
useful_armor = [item for item in armor if item in ["Helmet", "Chestplate"]]
not_useful_armor = [item for item in armor if item == "Shield"]

# Filtering by Rarity
rare_loot = [item for item in loot_options if item == "Golden Coin"]
common_loot = [item for item in loot_options if item not in rare_loot]
rare_weapons = [item for item in weapons if item in ["Sword", "Axe"]]
common_weapons = [item for item in weapons if item not in rare_weapons]
rare_armor = [item for item in armor if item == "Chestplate"]
common_armor = [item for item in armor if item not in rare_armor]

# Displaying the filtered results
print("Welcome to your Inventory Filter")
print("\nFiltered by Effect:")
print("Good Loot:", good_loot)
print("Bad Loot:", bad_loot)
print("Good Weapons:", good_weapons)
print("Bad Weapons:", bad_weapons)
print("Good Armor:", good_armor)
print("Bad Armor:", bad_armor)

print("\nFiltered by Usefulness:")
print("Useful Loot:", useful_loot)
print("Not Useful Loot:", not_useful_loot)
print("Useful Weapons:", useful_weapons)
print("Not Useful Weapons:", not_useful_weapons)
print("Useful Armor:", useful_armor)
print("Not Useful Armor:", not_useful_armor)

print("\nFiltered by Rarity:")
print("Rare Loot:", rare_loot)
print("Common Loot:", common_loot)
print("Rare Weapons:", rare_weapons)
print("Common Weapons:", common_weapons)
print("Rare Armor:", rare_armor)
print("Common Armor:", common_armor)



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
        name = input("    |    Enter your hero's name: ").strip()
        if not name:
            name = "Hero"

        if choice == "1":
            return Warrior(name)
        elif choice == "2":
            return Mage(name)
        elif choice == "3":
            return Archer(name)
        else:
            print("    |    Invalid choice. Please enter 1, 2, or 3.")

def level_up(hero):
    hero.level += 1
    print(f"    |    **** {hero.name} has reached level {hero.level}! ****")
    hero.health_points = min(100, hero.health_points + 10)
    hero.combat_strength += 1
    print(f"    |    Stats increased! HP: {hero.health_points}, Strength: {hero.combat_strength}")

def gain_xp(hero, xp):
    hero.xp += xp
    print(f"    |    {hero.name} gained {xp} XP. (Total XP: {hero.xp})")
    xp_needed = 10
    if hero.xp >= xp_needed:
        level_up(hero)
        hero.xp -= xp_needed

def get_hero_powers(hero):
    powers = []
    relics = []
    available_powers = [p for p in all_powers if p["type"] == hero.type and p["level"] <= hero.level]
    powers = [p["name"] for p in available_powers]

    if hero.level >= 2:
        relics.append('Minor Health Boost Relic')
    if hero.level >= 4:
        relics.append('Minor Strength Boost Relic')
    if hero.level >= 6:
        relics.append('Experience Gain Relic')

    return powers, relics

last_game_result, total_monsters_killed = functions.load_game()
hero = select_hero()
monster = Monster()
session_monsters_killed = total_monsters_killed

# Initial combat strength input
input_invalid = True
i = 0
combat_strength_input = 0
m_combat_strength_input = 0

while input_invalid and i < 5:
    print("    ------------------------------------------------------------------")
    print("    |    Roll virtual dice for starting combat strength boost!")
    combat_strength_str = input("    |    Enter your roll (1-6): ").strip()
    m_combat_strength_str = input("    |    Enter the monster's roll (1-6): ").strip()

    if not (combat_strength_str.isdigit() and m_combat_strength_str.isdigit()):
        print("    |    Invalid input. Please enter numbers between 1 and 6. |")
        i += 1
        continue

    combat_strength_input = int(combat_strength_str)
    m_combat_strength_input = int(m_combat_strength_str)

    if combat_strength_input not in range(1, 7) or m_combat_strength_input not in range(1, 7):
        print("    |    Roll must be between 1 and 6.")
        i += 1
        continue

    input_invalid = False

# Apply combat strength bonuses
hero.combat_strength += combat_strength_input
monster.combat_strength += m_combat_strength_input
monster.combat_strength = min(12, max(1, monster.combat_strength))

# Weapon roll
input("    |    Rolling the dice for your weapon... (Press enter)")
weapon_roll = random.choice(small_dice_options)
weapon_bonus = weapon_roll
print(f"    |    You rolled a {weapon_roll}. Your weapon is: {weapons[weapon_roll - 1]}")
print(f"    |    Adding weapon bonus (+{weapon_bonus}) to combat strength.")
hero.combat_strength += weapon_bonus

# Adjust strength based on previous game result
hero.combat_strength, monster.combat_strength = functions.adjust_combat_strength(
    hero.combat_strength, monster.combat_strength, last_game_result
)

# Display current status
print(f"    |    Hero: {hero.name} ({hero.type}) | HP: {hero.health_points} | Strength: {hero.combat_strength}")
print(f"    |    Monster | HP: {monster.health_points} | Strength: {monster.combat_strength}")

# Loot collection
for i in range(2):
    input(f"    |    Searching for loot (Attempt {i+1}/2)... (Press enter)")
    if loot_options:
        loot_options, belt = functions.collect_loot(loot_options, belt)
    else:
        print("    |    No more loot items available.")
        break
belt.sort()
print("    |    Your belt contains:", belt if belt else "Nothing")

# Use loot
if belt:
    input("    |    Monster approaching! Quickly use an item? (Press enter)")
    belt, hero.health_points = functions.use_loot(belt, hero.health_points)

# Monster power roll
input("    |    Roll for Monster's Magic Power (Press enter)")
power_roll = random.choice(list(monster_powers.keys()))
power_bonus = monster_powers[power_roll]
print(f"    |    Monster gains power: {power_roll} (+{power_bonus} strength)")
monster.combat_strength += power_bonus
monster.combat_strength = min(18, max(1, monster.combat_strength))
print(f"    |    Monster's combat strength is now {monster.combat_strength}")

# Final Monster Fight
print("    ------------------------------------------------------------------")
print("    |    The final confrontation! You meet the monster!")
print("    |    FIGHT!! FIGHT !!")

while monster.health_points > 0 and hero.health_points > 0:
    print("    |    --- Combat Round ---")
    print(f"    |    Hero HP: {hero.health_points} | Monster HP: {monster.health_points}")
    input("    |    Roll to see who strikes first (Press Enter)")
    attack_roll = random.choice(small_dice_options)

    hero_strikes_first = (attack_roll % 2 != 0)

    if hero_strikes_first:
        print("    |    You act first!")
        input("    |    Attack the monster! (Press enter)")
        monster.health_points = functions.hero_attacks(hero.combat_strength, monster.health_points)
        if monster.health_points <= 0: break
        input("    |    The Monster strikes back! (Press enter)")
        hero.health_points = functions.monster_attacks(monster.combat_strength, hero.health_points)
    else:
        print("    |    The Monster acts first!")
        input("    |    The Monster attacks! (Press enter)")
        hero.health_points = functions.monster_attacks(monster.combat_strength, hero.health_points)
        if hero.health_points <= 0: break
        input("    |    Retaliate! Attack the monster! (Press enter)")
        monster.health_points = functions.hero_attacks(hero.combat_strength, monster.health_points)

print("    |    --- Combat Over ---")
winner = "Hero" if monster.health_points <= 0 else "Monster"

if winner == "Hero":
    print(f"    |    **** VICTORY! {hero.name} defeated the Monster! ****")
    session_monsters_killed += 1
    gain_xp(hero, 10)
    num_stars = 3
else:
    print(f"    |    ==== DEFEAT! {hero.name} was defeated by the Monster! ====")
    num_stars = 1

functions.save_game(winner, hero_name=hero.name, num_stars=num_stars, total_kills=session_monsters_killed)
print(f"    |    Game saved. Total monsters killed: {session_monsters_killed}")

powers, relics = get_hero_powers(hero)
print(f"    |    --- Final Hero Status ---")
print(f"    |    Name: {hero.name}")
print(f"    |    Class: {hero.type}")
print(f"    |    Level: {hero.level}")
print(f"    |    XP: {hero.xp}")
print(f"    |    Health: {hero.health_points}")
print(f"    |    Strength: {hero.combat_strength}")
print(f"    |    Powers: {powers if powers else 'None'}")
print(f"    |    Relics: {relics if relics else 'None'}")
print(f"    |    Belt: {belt if belt else 'Empty'}")
print("    ------------------------------------------------------------------")
print("    |    Game Over.")
