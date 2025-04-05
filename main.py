import random
from hero import Hero
from monster import Monster
import functions
import os
import platform
print(f"Operating System: {os.name}")
print(f"Python Version: {platform.python_version()}")

# Dice options
small_dice_options = list(range(1, 7))
big_dice_options = list(range(1, 21))

# Weapons list
weapons = ["Fist", "Knife", "Club", "Gun", "Bomb", "Nuclear Bomb"]

# Loot options
loot_options = ["Health Potion", "Poison Potion", "Secret Note", "Leather Boots", "Flimsy Gloves"]
belt = []

# Monster Powers
monster_powers = {
    "Fire Magic": 2,
    "Freeze Time": 4,
    "Super Hearing": 6
}

# Load old data to display
last_game_result, monsters_killed_line = functions.load_game()

if monsters_killed_line:
    try:
        monsters_killed = int(monsters_killed_line.split(": ")[1])
        print(f"Total monsters killed: {monsters_killed}")
    except:
        print("Error loading monster kills.")
else:
    print("No monster kill data found.")

# Initialize hero and monster objects to Creating instances
hero = Hero()
monster = Monster()
# Define the number of stars to award the player
num_stars = 0

# Loop to get valid input for Hero and Monster's Combat Strength
input_invalid = True
i = 0

while input_invalid and i < 5:
    print("    ------------------------------------------------------------------")
    print("    |", end="    ")
    combat_strength = input("Enter your combat Strength (1-6): ").strip()
    print("    |", end="    ")
    m_combat_strength = input("Enter the monster's combat Strength (1-6): ").strip()

    # Validate if the inputs are numeric and within range
    if (not combat_strength.isdigit()) or (not m_combat_strength.isdigit()):
        print("    |    One or more invalid inputs. Player needs to enter integer numbers for Combat Strength    |")
        i += 1
        continue

    combat_strength = int(combat_strength)  # Convert combat_strength to an integer
    m_combat_strength = int(m_combat_strength)  # Convert monster's combat_strength to an integer

    # Check if the combat strength is within valid range (1 to 6)
    if combat_strength not in range(1, 7) or m_combat_strength not in range(1, 7):
        print("    |    Enter a valid integer between 1 and 6 only")
        i += 1
        continue

    # If inputs are valid, break out of the loop
    input_invalid = False

# Roll the Dice  for hero weapon
input("Rolling the dice for your weapon... (Press enter)")
weapon_roll = random.choice(small_dice_options)

# Limit the combat strength to 6
combat_strength = min(6, (int(combat_strength) + weapon_roll))
print("    |    The hero\'s weapon is " + str(weapons[weapon_roll - 1]))



# Adjust combat strength and initializing it
hero.combat_strength, monster.combat_strength = functions.adjust_combat_strength(hero.combat_strength, monster.combat_strength)

# Roll The Dice  to see health points.  Health points are initialized in the Character class.
print(f"Hero health points: {hero.health_points}")
print(f"Monster health points: {monster.health_points}")

# Collect loot
for _ in range(2):
    input("Roll for loot (Press enter)")
    loot_options, belt = functions.collect_loot(loot_options, belt)
belt.sort()
print("Your belt contains:", belt)

# Use loot
belt, hero.health_points = functions.use_loot(belt, hero.health_points)

# Monster's Magic Power
input("Roll for Monster's Magic Power (Press enter)")
power_roll = random.choice(list(monster_powers.keys()))
monster.combat_strength = min(6, monster.combat_strength + monster_powers[power_roll])
print(f"Monster's combat strength is now {monster.combat_strength} using {power_roll}")

# Fight Sequence
# Loop while the monster and the player are alive. Call fight sequence functions
print("    ------------------------------------------------------------------")
print("You meet the monster. FIGHT!! FIGHT !!")
while monster.health_points > 0 and hero.health_points > 0:
    # Question 5: Determine who attacks first
    input("Roll to see who strikes first (Press Enter)")
    attack_roll = random.choice(small_dice_options)
    match attack_roll % 2: # Use match statement to determine who attacks ( chat gpt assist )
        case 0:
            input("The Monster strikes (Press enter)")
            hero.health_points = functions.monster_attacks(monster.combat_strength, hero.health_points)
        case _: # Default case for odd numbers
            input("You strike (Press enter)")
            monster.health_points = functions.hero_attacks(hero.combat_strength, monster.health_points)

# Determine winner
winner = "Hero" if monster.health_points <= 0 else "Monster"

# Get Hero's Name
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
    return "Hero"  # Default if too many invalid attempts

# Call the function to get the hero's name
short_name = get_hero_name()

# Save game state
functions.save_game(winner, hero_name=short_name, num_stars=3 if winner == "Hero" else 1)
