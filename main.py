# main.py
import random
from hero import Warrior, Mage, Archer # Keep specific classes
from monster import Monster
import functions
import os
import platform

# --- Game Setup ---
print(f"Operating System: {os.name}")
print(f"Python Version: {platform.python_version()}")

small_dice_options = list(range(1, 7))
big_dice_options = list(range(1, 21)) # Used in Character init
weapons = ["Fist", "Knife", "Club", "Gun", "Bomb", "Nuclear Bomb"] # Tied to small dice roll 1-6
loot_options = ["Health Potion", "Poison Potion", "Secret Note", "Leather Boots", "Flimsy Gloves", "Key"] # Added Key for treasure
belt = [] # Hero's inventory belt
monster_powers = {
    "Fire Magic": 2,
    "Freeze Time": 4,
    "Super Hearing": 6
}

# Keep power list for hero classes
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

# --- Hero Selection Function (Keep from original) ---
def select_hero():
    print("    |    Choose your hero:")
    print("    |    1. Warrior")
    print("    |    2. Mage")
    print("    |    3. Archer")

    while True:
        choice = input("    |    Enter your choice (1-3): ").strip()
        name = input("    |    Enter your hero's name: ").strip()
        if not name: name = "Hero" # Default name if empty

        if choice == "1":
            return Warrior(name)
        elif choice == "2":
            return Mage(name)
        elif choice == "3":
            return Archer(name)
        else:
            print("    |    Invalid choice. Please enter 1, 2, or 3.")

# --- Leveling/XP/Powers Functions (Keep from original) ---
def level_up(hero):
    hero.level += 1
    print(f"    |    **** {hero.name} has reached level {hero.level}! ****")
    # Add potential stat increases on level up?
    hero.health_points = min(100, hero.health_points + 10) # Heal a bit on level up
    hero.combat_strength += 1
    print(f"    |    Stats increased! HP: {hero.health_points}, Strength: {hero.combat_strength}")

def gain_xp(hero, xp):
    hero.xp += xp
    print(f"    |    {hero.name} gained {xp} XP. (Total XP: {hero.xp})")
    # Level up threshold (e.g., 10 XP per level)
    xp_needed = 10 # Simple threshold for now
    if hero.xp >= xp_needed:
        level_up(hero)
        hero.xp -= xp_needed # Reset XP for next level (or carry over excess?) Carry over: hero.xp -= xp_needed

def get_hero_powers(hero):
    powers = []
    relics = [] # Relics seem tied to XP threshold? Let's simplify for now.

    # Get powers based on hero type and current level
    available_powers = [p for p in all_powers if p["type"] == hero.type and p["level"] <= hero.level]
    powers = [p["name"] for p in available_powers]

    # Example relic logic (simplified): Gain relics at certain levels
    if hero.level >= 2: relics.append('Minor Health Boost Relic')
    if hero.level >= 4: relics.append('Minor Strength Boost Relic')
    if hero.level >= 6: relics.append('Experience Gain Relic')

    return powers, relics

# --- Load Game ---
last_game_result, total_monsters_killed = functions.load_game() # Load total kills

# --- Initialize Game Objects ---
hero = select_hero()
monster = Monster()
# Keep track of kills for this session, starting from loaded value
session_monsters_killed = total_monsters_killed # Initialize with loaded value

# --- Initial Combat Strength Input (Keep from original, maybe simplify?) ---
# This section sets initial strength based on user input 1-6, overriding hero's class init
# Let's keep it for now, but maybe use hero's base strength later.
input_invalid = True
i = 0
combat_strength_input = 0 # Player input
m_combat_strength_input = 0 # Monster input (doesn't seem used for monster obj?)

while input_invalid and i < 5:
    print("    ------------------------------------------------------------------")
    print("    |    Roll virtual dice for starting combat strength boost!")
    combat_strength_str = input("    |    Enter your roll (1-6): ").strip()
    m_combat_strength_str = input("    |    Enter the monster's roll (1-6): ").strip()

    if (not combat_strength_str.isdigit()) or (not m_combat_strength_str.isdigit()):
        print("    |    Invalid input. Please enter numbers between 1 and 6. |")
        i += 1
        continue

    combat_strength_input = int(combat_strength_str)
    m_combat_strength_input = int(m_combat_strength_str) # Store monster roll

    if combat_strength_input not in range(1, 7) or m_combat_strength_input not in range(1, 7):
        print("    |    Roll must be between 1 and 6.")
        i += 1
        continue

    input_invalid = False

# Adjust hero's strength based on the input roll (add it as a bonus?)
print(f"    |    Applying your roll bonus ({combat_strength_input}) to base strength.")
hero.combat_strength += combat_strength_input

# What to do with monster roll? Maybe adjust monster strength too?
print(f"    |    Monster gets a bonus based on its roll ({m_combat_strength_input}).")
monster.combat_strength += m_combat_strength_input
# Cap monster strength after bonus?
monster.combat_strength = min(6 + 6, max(1, monster.combat_strength)) # Example cap: 12

# --- Weapon Roll (Keep from original) ---
input("    |    Rolling the dice for your weapon... (Press enter)")
weapon_roll = random.choice(small_dice_options) # 1-6
weapon_bonus = weapon_roll # Bonus strength from weapon is the roll value itself?
print(f"    |    You rolled a {weapon_roll}. Your weapon is: {weapons[weapon_roll - 1]}")
print(f"    |    Adding weapon bonus (+{weapon_bonus}) to combat strength.")
hero.combat_strength += weapon_bonus

# --- Adjust Strengths Based on Last Game (Keep from original) ---
# Pass the loaded result to the function
hero.combat_strength, monster.combat_strength = functions.adjust_combat_strength(
    hero.combat_strength, monster.combat_strength, last_game_result
)

print(f"    |    -----------------------------------------------------")
print(f"    |    Hero: {hero.name} ({hero.type} Lvl {hero.level})")
print(f"    |    Current Health: {hero.health_points}")
print(f"    |    Current Combat Strength: {hero.combat_strength}")
print(f"    |    ---------------- VS -------------------------------")
print(f"    |    Monster:")
print(f"    |    Current Health: {monster.health_points}")
print(f"    |    Current Combat Strength: {monster.combat_strength}")
print(f"    |    -----------------------------------------------------")


# --- Loot Collection (Keep from original, modified to call func once per loop) ---
for i in range(2): # Find 2 loot items
    input(f"    |    Searching for loot (Attempt {i+1}/2)... (Press enter)")
    # Make sure loot_options has items before trying to collect
    if loot_options:
        loot_options, belt = functions.collect_loot(loot_options, belt)
    else:
        print("    |    No more loot items available in this area.")
        break # Stop searching if no more loot exists
belt.sort() # Sort belt contents
print("    |    Your belt contains:", belt if belt else "Nothing")

# --- Use Loot (Keep from original) ---
if belt: # Only try to use loot if belt is not empty
    input("    |    Monster approaching! Quickly use an item? (Press enter)")
    belt, hero.health_points = functions.use_loot(belt, hero.health_points)
    # Update hero object health after using loot
    # hero.health_points = current_hp # Already done by passing hero.health_points

# --- Monster Power Roll (Keep from original) ---
input("    |    Roll for Monster's Magic Power (Press enter)")
power_roll = random.choice(list(monster_powers.keys()))
power_bonus = monster_powers[power_roll]
print(f"    |    Monster gains power: {power_roll} (+{power_bonus} strength)")
monster.combat_strength += power_bonus
# Cap monster strength again?
monster.combat_strength = min(18, max(1, monster.combat_strength)) # Higher cap example
print(f"    |    Monster's combat strength is now {monster.combat_strength}")


# --- <<< NEW FEATURE: Random Exploration Event >>> ---
print("    ------------------------------------------------------------------")
print("    |    Exploring the area before the main confrontation...")
# Define possible events and conditions
events = ["artifact", "npc", "bandits"]
eligible_events = ["artifact"] # Artifacts are always possible

# Check conditions for other events
if hero.health_points < 50: # Condition for NPC
    eligible_events.append("npc")
# Condition for Bandits (Using strength threshold from feature code)
# NB: 70 seems very high, maybe adjust based on gameplay?
bandit_strength_threshold = 20 # Lowered threshold for testing
if hero.combat_strength > bandit_strength_threshold:
     eligible_events.append("bandits")
     print(f"    |    (Your high strength [{hero.combat_strength}] might attract bandits...)")
else:
     print(f"    |    (Your strength [{hero.combat_strength}] isn't high enough to trigger bandit encounters.)")


if not eligible_events:
    print("    |    The area seems quiet. Nothing interesting happens.")
else:
    print(f"    |    Possible encounters: {eligible_events}")
    random_event = random.choice(eligible_events)
    print(f"    |    Encountered: {random_event.capitalize()}!")

    if random_event == "artifact":
        print("    |    You found a Strange Artifact!")
        artifact_effect = random.choice(["strength_up", "health_down", "health_up", "strength_down", "xp_boost"])
        if artifact_effect == "strength_up":
            hero.combat_strength += 3
            print("    |    The artifact increased your combat strength!")
        elif artifact_effect == "health_down":
            hero.health_points = max(0, hero.health_points - 10)
            print("    |    The artifact drained some health!")
        elif artifact_effect == "health_up":
            hero.health_points = min(100, hero.health_points + 15)
            print("    |    The artifact restored some health!")
        elif artifact_effect == "strength_down":
            hero.combat_strength = max(1, hero.combat_strength - 2)
            print("    |    The artifact weakened you slightly!")
        elif artifact_effect == "xp_boost":
             gain_xp(hero, 5) # Gain some XP
             print("    |    The artifact grants you some experience!")

    elif random_event == "npc":
        print("    |    You meet a weary traveler (NPC).")
        # Original logic: heal if HP low, otherwise grant power. Keep that.
        if hero.health_points < 50:
            heal_amount = 20
            hero.health_points = min(100, hero.health_points + heal_amount)
            print(f"    |    The traveler shares a potion. You healed +{heal_amount} HP.")
        else:
            strength_boost = 2 # Smaller boost than original feature code
            hero.combat_strength += strength_boost
            print(f"    |    The traveler shares a combat tip. Strength +{strength_boost}.")

    elif random_event == "bandits":
        print("    |    Bandits ambush you!")
        # Use hero vs monster health as condition (as per feature code)
        # But maybe compare hero strength vs fixed bandit strength? Let's use monster health for now.
        bandit_difficulty = monster.health_points # Bandits are as tough as the current monster's health?
        print(f"    |    (Bandit toughness estimated around {bandit_difficulty})")
        if hero.combat_strength > bandit_difficulty:
            print("    |    You fought off the bandits!")
            # Gain loot
            input("    |    Search the bandits' camp? (Press enter)")
            if loot_options:
                 loot_options, belt = functions.collect_loot(loot_options, belt)
                 print("    |    You found some loot on them.")
            else:
                 print("    |    Their camp was already picked clean.")
            # Gain XP for defeating bandits?
            gain_xp(hero, 3)
        else:
            print("    |    The bandits overpower you!")
            loss_penalty = random.choice(["loot", "health"])
            if loss_penalty == "loot" and belt:
                 lost_item = belt.pop(random.randrange(len(belt)))
                 print(f"    |    They stole your {lost_item}!")
            elif loss_penalty == "health":
                 damage_taken = 15
                 hero.health_points = max(0, hero.health_points - damage_taken)
                 print(f"    |    You barely escape, losing {damage_taken} health.")
            else:
                 print("    |    You managed to escape with minor bruises.")

        # Original feature code buffed monster on bandit loss, let's remove that.

    # Display stats after event
    print(f"    |    Current Status - HP: {hero.health_points}, Strength: {hero.combat_strength}, Belt: {belt}")


# --- Treasure Hunt Feature (Keep from original base) ---
print("    ------------------------------------------------------------------")
input("    |    Ready to hunt for treasure? (Press Enter)")
grid_size = 5
map_grid, treasure_locations = functions.generate_treasure_map(grid_size, num_treasures=3)
hero_location = (random.randint(0,grid_size-1), random.randint(0,grid_size-1)) # Start at random spot

# Ensure hero doesn't start on a treasure
while map_grid[hero_location[0]][hero_location[1]] == "[T]":
     hero_location = (random.randint(0,grid_size-1), random.randint(0,grid_size-1))

# Initial inventory for treasure hunt
inventory = {
    "Keys": 1, # Start with one key maybe?
    "Treasures Collected": 0,
    "Health": hero.health_points, # Sync with hero's current health
    "Energy": 50 # Max energy
}

# Treasure Hunt Gameplay Loop
print("    |    --- Treasure Hunt Map ---")
# Mark initial hero location
current_map_display = [row[:] for row in map_grid] # Create a copy for display
current_map_display[hero_location[0]][hero_location[1]] = "[H]" # Mark hero
for row in current_map_display:
    print("    |    " + " ".join(row))
print(f"    |    Inventory: {inventory}")

moves_left = 15 # Limit moves?
while moves_left > 0:
    print(f"    |    Moves left: {moves_left}")
    direction = input("    |    Enter direction (North, South, East, West, exit): ").strip().capitalize()

    if direction == "Exit":
        print("    |    Leaving treasure hunt area...")
        break

    # Store previous location to clear hero marker
    prev_location = hero_location

    # Move hero
    hero_location = functions.move_hero(hero_location, direction, grid_size)

    # Update map display: clear old marker, set new one
    # Check what was at the previous location before overwriting with Hero marker
    if map_grid[prev_location[0]][prev_location[1]] == '[X]':
        current_map_display[prev_location[0]][prev_location[1]] = '[X]' # Keep collected marker
    else:
        current_map_display[prev_location[0]][prev_location[1]] = map_grid[prev_location[0]][prev_location[1]] # Restore original tile (Empty or Treasure)

    # Store symbol at new location before placing Hero marker
    symbol_at_new_location = current_map_display[hero_location[0]][hero_location[1]]

    current_map_display[hero_location[0]][hero_location[1]] = "[H]" # Place hero marker

    # Display updated map
    print("    |    --- Treasure Hunt Map ---")
    for row in current_map_display:
        print("    |    " + " ".join(row))

    # Interact with the location *before* overwriting tile with "[H]" permanently
    # Pass the original map_grid for interaction logic
    inventory, map_grid = functions.interact_with_treasure(hero_location, map_grid, inventory)

    # Update hero's health from inventory changes during interaction
    hero.health_points = inventory["Health"]

    print(f"    |    Inventory: {inventory}")

    # Check if all treasures found
    if inventory["Treasures Collected"] == len(treasure_locations):
        print("    |    **** All treasures collected! ****")
        gain_xp(hero, 10) # Bonus XP for finding all treasures
        break

    moves_left -= 1
    if moves_left == 0:
        print("    |    You ran out of time for the treasure hunt!")

# Update hero health one last time after treasure hunt finishes
hero.health_points = inventory["Health"]
print(f"    |    Finished treasure hunt. Current health: {hero.health_points}")


# --- Final Monster Fight (Keep from original base) ---
print("    ------------------------------------------------------------------")
print("    |    The final confrontation! You meet the monster!")
print("    |    FIGHT!! FIGHT !!")

while monster.health_points > 0 and hero.health_points > 0:
    print("    |    --- Combat Round ---")
    print(f"    |    Hero HP: {hero.health_points} | Monster HP: {monster.health_points}")
    input("    |    Roll to see who strikes first (Press Enter)")
    attack_roll = random.choice(small_dice_options)

    # Determine attacker based on roll (even = monster, odd = hero)
    hero_strikes_first = (attack_roll % 2 != 0)

    if hero_strikes_first:
        print("    |    You act first!")
        input("    |    Attack the monster! (Press enter)")
        # Use the function for consistency
        monster.health_points = functions.hero_attacks(hero.combat_strength, monster.health_points)
        if monster.health_points <= 0: break # Check if monster died

        # Monster retaliates if still alive
        input("    |    The Monster strikes back! (Press enter)")
        hero.health_points = functions.monster_attacks(monster.combat_strength, hero.health_points)

    else: # Monster strikes first
        print("    |    The Monster acts first!")
        input("    |    The Monster attacks! (Press enter)")
        hero.health_points = functions.monster_attacks(monster.combat_strength, hero.health_points)
        if hero.health_points <= 0: break # Check if hero died

        # Hero retaliates if still alive
        input("    |    Retaliate! Attack the monster! (Press enter)")
        monster.health_points = functions.hero_attacks(hero.combat_strength, monster.health_points)

    if hero.health_points <= 0 or monster.health_points <= 0:
        break # End combat if someone died

print("    |    --- Combat Over ---")

# Determine winner
winner = "Hero" if monster.health_points <= 0 else "Monster"

if winner == "Hero":
    print(f"    |    **** VICTORY! {hero.name} defeated the Monster! ****")
    session_monsters_killed += 1 # Increment kill count for this session
    gain_xp(hero, 10) # XP for winning
    num_stars = 3 # Stars for winning
else:
    print(f"    |    ==== DEFEAT! {hero.name} was defeated by the Monster! ====")
    num_stars = 1 # Stars for losing

# --- Hero Naming (Keep from original, maybe redundant if name set at start) ---
# This seems out of place if the hero already has a name. Let's use the existing name.
# def get_hero_name(): ... (Remove this function)
short_name = hero.name # Use the name set during selection

# --- Save Game ---
functions.save_game(winner, hero_name=short_name, num_stars=num_stars, total_kills=session_monsters_killed)
print(f"    |    Game saved. Total monsters killed across all games: {session_monsters_killed}")

# --- Display Final Hero Stats/Powers (Keep from original) ---
# Call gain_xp maybe once more as a bonus? Or remove these extras.
# gain_xp(hero, 5) # Example bonus XP
# gain_xp(hero, 5) # Example bonus XP

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