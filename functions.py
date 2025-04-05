# functions.py
import random
import os

# --- Loot Functions (from original base) ---
def use_loot(belt, health_points):
    good_loot_options = ["Health Potion", "Leather Boots"]
    bad_loot_options = ["Poison Potion"]

    if not belt:
        print("    |    Your belt is empty, cannot use loot.")
        return belt, health_points

    print("    |    !!You see a monster in the distance! So you quickly use your first item:")
    first_item = belt.pop(0) # Use and remove the first item
    print(f"    |    Using: {first_item}")

    if first_item == "Health Potion":
        health_points = min(100, (health_points + 10)) # Increase HP, cap at 100
        print(f"    |    You used {first_item} to up your health to {health_points}")
    elif first_item == "Leather Boots":
        # What should boots do? Maybe increase temp speed or defense? For now, small HP boost.
        health_points = min(100, (health_points + 5))
        print(f"    |    You equipped {first_item}. Felt slightly healthier: {health_points}")
    elif first_item == "Poison Potion":
        health_points = max(0, (health_points - 10)) # Decrease HP, floor at 0
        print(f"    |    You used {first_item}. Ouch! Health down to {health_points}")
    else:
        print(f"    |    You used {first_item} but it doesn't seem useful right now.")

    return belt, health_points

def collect_loot(loot_options, belt):
    print("    |    !!You find a loot bag!!")
    if not loot_options:
        print("    |    ...but it's empty.")
        return loot_options, belt

    print("    |    You look inside:")
    # Collect one item per call for simplicity? Original collected 2 implicitly via loop in main.
    # Let's make it collect one item.
    loot_roll = random.randrange(len(loot_options)) # Use randrange
    loot = loot_options.pop(loot_roll) # Remove from available options
    print(f"    |    You found: {loot}")
    belt.append(loot)
    print("    |    Your belt:", belt)
    return loot_options, belt

# --- Attack Functions (from original base) ---
def hero_attacks(combat_strength, m_health_points):
    print(f"    |    Player's weapon ({combat_strength}) ---> Monster ({m_health_points})")
    damage = combat_strength # Simple damage model
    if damage >= m_health_points:
        m_health_points = 0
        print("    |    You have killed the monster!")
    else:
        m_health_points -= damage
        print(f"    |    You have reduced the monster's health to: {m_health_points}")
    return max(0, m_health_points) # Ensure health doesn't go below 0

def monster_attacks(m_combat_strength, health_points):
    print(f"    |    Monster's Claw ({m_combat_strength}) ---> Player ({health_points})")
    damage = m_combat_strength # Simple damage model
    if damage >= health_points:
        health_points = 0
        print("    |    Player is dead!")
    else:
        health_points -= damage
        print(f"    |    The monster has reduced Player's health to: {health_points}")
    return max(0, health_points) # Ensure health doesn't go below 0

# --- Save/Load Functions (Using improved load_game logic) ---
def save_game(winner, hero_name="Hero", num_stars=0, total_kills=0):
    # Pass total_kills to save it correctly
    with open("save.txt", "a") as file:
        if winner == "Hero":
            file.write(f"Hero {hero_name} has killed a monster and gained {num_stars} stars.\n")
            # Save the new total kills count
            file.write(f"Total monsters killed: {total_kills + 1}\n")
        elif winner == "Monster":
            file.write(f"Monster has killed the hero {hero_name}.\n")
            # Save the existing total kills count (no increment)
            file.write(f"Total monsters killed: {total_kills}\n")
        file.write("-" * 20 + "\n") # Add separator for clarity

def load_game():
    last_game_result = None
    total_kills = 0
    try:
        with open("save.txt", "r") as file:
            print("    |    Loading from save file...")
            lines = [line.strip() for line in file if line.strip()] # Read non-empty lines
            if lines:
                # Find the last "Total monsters killed:" line
                for i in range(len(lines) - 1, -1, -1):
                    if lines[i].startswith("Total monsters killed:"):
                        try:
                            total_kills = int(lines[i].split(":")[1].strip())
                            # The result line should be the one before the kills line
                            if i > 0:
                                last_game_result = lines[i-1]
                            break # Found the latest kill count
                        except (IndexError, ValueError):
                            print(f"    |    Warning: Could not parse kill count line: {lines[i]}")
                            continue # Try finding an earlier one if format is broken

                if last_game_result:
                    print(f"    |    Last result found: {last_game_result}")
                else:
                     # Fallback: try finding the last line that isn't a separator or kill count
                     for i in range(len(lines) - 1, -1, -1):
                         if not lines[i].startswith("Total monsters killed:") and not lines[i].startswith("----"):
                             last_game_result = lines[i]
                             print(f"    |    Last result (fallback): {last_game_result}")
                             break
                     if not last_game_result:
                          print("    |    Could not determine last game result from save file.")


                print(f"    |    Total monsters killed loaded: {total_kills}")
                return last_game_result, total_kills
            else:
                print("    |    Save file is empty.")
                return None, 0
    except FileNotFoundError:
        print("    |    No save file found. Starting fresh.")
        return None, 0
    except Exception as e:
        print(f"    |    An error occurred loading the game: {e}")
        return None, 0

def adjust_combat_strength(hero_strength, m_combat_strength, last_game_result):
    # Pass last_game_result explicitly
    if last_game_result:
        if "Hero" in last_game_result and "killed a monster" in last_game_result:
             # Check if stars were mentioned and parse them
             try:
                 num_stars = int(last_game_result.split()[-2])
                 if num_stars >= 3: # Adjust threshold if needed
                     print("    |    ... Increasing monster's strength (won easily last time).")
                     m_combat_strength += 1
                 else:
                     print("    |    ... Last win was close, no strength adjustment.")
             except (IndexError, ValueError):
                 # If stars parsing fails, maybe default to increasing monster strength on any win?
                 print("    |    ... Increasing monster's strength (Hero won last time).")
                 m_combat_strength += 1
        elif "Monster has killed the hero" in last_game_result:
            print("    |    ... Increasing hero's strength (lost last time).")
            hero_strength += 1
        else:
            print("    |    ... Previous game result unclear, no automatic strength adjustment.")
    else:
        print("    |    ... No previous game data, starting with base strengths.")

    # Apply caps if necessary (e.g., monster max strength 6?)
    # hero_strength = max(1, hero_strength) # Ensure hero strength > 0
    # m_combat_strength = min(6, max(1, m_combat_strength)) # Monster str 1-6

    return hero_strength, m_combat_strength


# --- Treasure Hunt Functions (from original base) ---
def generate_treasure_map(grid_size=5, num_treasures=3):
    map_grid = [["[ ]" for _ in range(grid_size)] for _ in range(grid_size)] # Use brackets for empty
    treasures = set() # Use a set to avoid placing multiple treasures in the same spot easily
    while len(treasures) < num_treasures:
        pos = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
        if pos not in treasures: # Ensure unique locations
             treasures.add(pos)
             map_grid[pos[0]][pos[1]] = "[T]" # Mark treasure

    return map_grid, list(treasures) # Return treasures as a list if needed elsewhere

def move_hero(hero_location, direction, grid_size):
    row, col = hero_location
    new_row, new_col = row, col
    direction = direction.lower() # Make case-insensitive

    if direction == "north" and row > 0:
        new_row -= 1
    elif direction == "south" and row < grid_size - 1:
        new_row += 1
    elif direction == "east" and col < grid_size - 1:
        new_col += 1
    elif direction == "west" and col > 0:
        new_col -= 1
    else:
        print("    |    Invalid move or boundary reached.")
        return hero_location # Return original location if move is invalid

    print(f"    |    Moved {direction} to ({new_row}, {new_col})")
    return (new_row, new_col)

def interact_with_treasure(hero_location, map_grid, inventory):
    row, col = hero_location
    tile_symbol = map_grid[row][col] # Get the symbol currently on the map tile

    # This function needs to know what symbols represent what.
    # Let's assume "[T]" is treasure, "[H]" is hero, "[ ]" is empty, "[X]" is collected treasure
    if tile_symbol == "[T]":
        print("    |    You found a treasure chest!")
        # Check conditions based on inventory dict provided by main.py
        if inventory.get("Keys", 0) > 0:
            print("    |    You used a key to open the chest!")
            inventory["Keys"] -= 1
            inventory["Treasures Collected"] = inventory.get("Treasures Collected", 0) + 1
            map_grid[row][col] = "[X]" # Mark as collected
            print("    |    Treasure collected!")
        elif inventory.get("Energy", 0) > 20 and inventory.get("Health", 0) > 50 :
             # Use health/energy only if no keys
            print("    |    No keys... You force the chest open!")
            inventory["Health"] = max(0, inventory.get("Health", 0) - 10)
            inventory["Energy"] = max(0, inventory.get("Energy", 0) - 10)
            inventory["Treasures Collected"] = inventory.get("Treasures Collected", 0) + 1
            map_grid[row][col] = "[X]" # Mark as collected
            print(f"    |    Treasure collected! Health: {inventory['Health']}, Energy: {inventory['Energy']}")
        else:
            # Check which resource is lacking
            if inventory.get("Keys", 0) <= 0:
                 print("    |    You need a key to open this.")
            if inventory.get("Energy", 0) <= 20:
                print("    |    Not enough energy to force it open.")
            if inventory.get("Health", 0) <= 50:
                 print("    |    Too wounded to risk forcing it open.")

    elif tile_symbol == "[X]":
        print("    |    You already collected the treasure here.")
    elif tile_symbol == "[ ]" or tile_symbol == "[H]": # Allow interaction check even if Hero is marked
        print("    |    This spot seems empty.")
    else:
        print(f"    |    You see: {tile_symbol}. Nothing to interact with.") # Handle unexpected symbols

    # Return updated inventory and map
    return inventory, map_grid

# --- Inception Dream Function (from original base - unused by main?) ---
def inception_dream(num_dream_lvls):
    try:
        num_dream_lvls = int(num_dream_lvls)
        if num_dream_lvls <= 1:
            print("    |    You are in the deepest dream level now")
            print("    |", end="    ")
            input("Start to go back to real life? (Press Enter)")
            print("    |    You start to regress back through your dreams to real life.")
            return 1 # Return depth 1 reached
        else:
            print(f"    |    Descending to dream level {num_dream_lvls}...")
            # Recursive call, result is the deepest level reached
            deepest_level = inception_dream(num_dream_lvls - 1)
            print(f"    |    Returning from dream level {num_dream_lvls}...")
            return deepest_level # Pass the deepest level back up
    except ValueError:
        print("    |    Invalid input for dream levels.")
        return 0 # Indicate error or invalid state