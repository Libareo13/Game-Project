import random
import os

# --- Loot Functions ---
def use_loot(belt, health_points):
    if not belt:
        print("    |    Your belt is empty, cannot use loot.")
        return belt, health_points

    print("    |    !!You see a monster in the distance! So you quickly use your first item:")
    first_item = belt.pop(0)
    print(f"    |    Using: {first_item}")

    if first_item == "Health Potion":
        health_points = min(100, health_points + 10)
        print(f"    |    You used {first_item} to up your health to {health_points}")
    elif first_item == "Leather Boots":
        health_points = min(100, health_points + 5)
        print(f"    |    You equipped {first_item}. Felt slightly healthier: {health_points}")
    elif first_item == "Poison Potion":
        health_points = max(0, health_points - 10)
        print(f"    |    You used {first_item}. Ouch! Health down to {health_points}")
    else:
        print(f"    |    You used {first_item} but it doesn't seem useful right now.")

    return belt, health_points

def collect_loot(loot_options, belt):
    print("    |    !!You find a loot bag!!")
    if not loot_options:
        print("    |    ...but it's empty.")
        return loot_options, belt

    loot_roll = random.randrange(len(loot_options))
    loot = loot_options.pop(loot_roll)
    print(f"    |    You found: {loot}")
    belt.append(loot)
    print("    |    Your belt:", belt)
    return loot_options, belt




# --- Attack Functions ---
def hero_attacks(combat_strength, m_health_points):
    print(f"    |    Player's weapon ({combat_strength}) ---> Monster ({m_health_points})")
    damage = combat_strength
    if damage >= m_health_points:
        m_health_points = 0
        print("    |    You have killed the monster!")
    else:
        m_health_points -= damage
        print(f"    |    You have reduced the monster's health to: {m_health_points}")
    return max(0, m_health_points)

def monster_attacks(m_combat_strength, health_points):
    print(f"    |    Monster's Claw ({m_combat_strength}) ---> Player ({health_points})")
    damage = m_combat_strength
    if damage >= health_points:
        health_points = 0
        print("    |    Player is dead!")
    else:
        health_points -= damage
        print(f"    |    The monster has reduced Player's health to: {health_points}")
    return max(0, health_points)

# --- Save/Load Functions ---
def save_game(winner, hero_name="Hero", num_stars=0, total_kills=0):
    with open("save.txt", "a") as file:
        if winner == "Hero":
            file.write(f"Hero {hero_name} has killed a monster and gained {num_stars} stars.\n")
            file.write(f"Total monsters killed: {total_kills + 1}\n")
        elif winner == "Monster":
            file.write(f"Monster has killed the hero {hero_name}.\n")
            file.write(f"Total monsters killed: {total_kills}\n")
        file.write("-" * 20 + "\n")

def load_game():
    last_game_result = None
    total_kills = 0
    try:
        with open("save.txt", "r") as file:
            print("    |    Loading from save file...")
            lines = [line.strip() for line in file if line.strip()]
            if lines:
                for i in range(len(lines) - 1, -1, -1):
                    if lines[i].startswith("Total monsters killed:"):
                        try:
                            total_kills = int(lines[i].split(":")[1].strip())
                            if i > 0:
                                last_game_result = lines[i - 1]
                            break
                        except (IndexError, ValueError):
                            continue
                return last_game_result, total_kills
            else:
                return None, 0
    except FileNotFoundError:
        print("    |    No save file found. Starting fresh.")
        return None, 0
    except Exception as e:
        print(f"    |    An error occurred loading the game: {e}")
        return None, 0

def adjust_combat_strength(hero_strength, m_combat_strength, last_game_result):
    if last_game_result:
        if "Hero" in last_game_result and "killed a monster" in last_game_result:
            try:
                num_stars = int(last_game_result.split()[-2])
                if num_stars >= 3:
                    print("    |    ... Increasing monster's strength (won easily last time).")
                    m_combat_strength += 1
                else:
                    print("    |    ... Last win was close, no strength adjustment.")
            except (IndexError, ValueError):
                print("    |    ... Increasing monster's strength (Hero won last time).")
                m_combat_strength += 1
        elif "Monster has killed the hero" in last_game_result:
            print("    |    ... Increasing hero's strength (lost last time).")
            hero_strength += 1
    else:
        print("    |    ... No previous game data, starting with base strengths.")
    return hero_strength, m_combat_strength

# --- Treasure Hunt Functions ---
def generate_treasure_map(grid_size=5, num_treasures=3):
    map_grid = [["[ ]" for _ in range(grid_size)] for _ in range(grid_size)]
    treasures = set()
    while len(treasures) < num_treasures:
        pos = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
        if pos not in treasures:
            treasures.add(pos)
            map_grid[pos[0]][pos[1]] = "[T]"
    return map_grid, list(treasures)

def move_hero(hero_location, direction, grid_size):
    row, col = hero_location
    direction = direction.lower()
    if direction == "north" and row > 0:
        row -= 1
    elif direction == "south" and row < grid_size - 1:
        row += 1
    elif direction == "east" and col < grid_size - 1:
        col += 1
    elif direction == "west" and col > 0:
        col -= 1
    else:
        print("    |    Invalid move or boundary reached.")
    print(f"    |    Moved {direction} to ({row}, {col})")
    return row, col

def interact_with_treasure(hero_location, map_grid, inventory):
    row, col = hero_location
    tile = map_grid[row][col]
    if tile == "[T]":
        print("    |    You found a treasure chest!")
        if inventory.get("Keys", 0) > 0:
            print("    |    You used a key to open the chest!")
            inventory["Keys"] -= 1
            inventory["Treasures Collected"] = inventory.get("Treasures Collected", 0) + 1
            map_grid[row][col] = "[X]"
        elif inventory.get("Energy", 0) > 20 and inventory.get("Health", 0) > 50:
            print("    |    No keys... You force the chest open!")
            inventory["Health"] = max(0, inventory["Health"] - 10)
            inventory["Energy"] = max(0, inventory["Energy"] - 10)
            inventory["Treasures Collected"] += 1
            map_grid[row][col] = "[X]"
        else:
            print("    |    You don't have enough resources to open the treasure.")
    elif tile == "[X]":
        print("    |    You already collected the treasure here.")
    else:
        print("    |    This spot seems empty.")
    return inventory, map_grid

# --- Inception Dream Function ---
def inception_dream(num_dream_lvls):
    try:
        num_dream_lvls = int(num_dream_lvls)
        if num_dream_lvls <= 1:
            print("    |    You are in the deepest dream level now")
            print("    |", end="    ")
            input("Start to go back to real life? (Press Enter)")
            print("    |    You start to regress back through your dreams to real life.")
            return 1
        else:
            print(f"    |    Descending to dream level {num_dream_lvls}...")
            deepest_level = inception_dream(num_dream_lvls - 1)
            print(f"    |    Returning from dream level {num_dream_lvls}...")
            return deepest_level
    except ValueError:
        print("    |    Invalid input for dream levels.")
        return 0