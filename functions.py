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
                monster_kills_line = lines[-1].strip()
                if "Total monsters killed:" in monster_kills_line:
                    monster_kills = int(monster_kills_line.split(":")[1].strip())
                print(last_line)
                print(f"Total monsters killed: {monster_kills}")
                return last_line, monster_kills
    except FileNotFoundError:
        print("No  games found. Starting again from the start.")
        return None, 0
    except Exception as e:
        print(f"An error occurred: {e}")
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

def generate_treasure_map(grid_size=5, num_treasures=3):
    map_grid = [["Empty" for _ in range(grid_size)] for _ in range(grid_size)]
    treasures = [(random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)) for _ in range(num_treasures)]
    for treasure in treasures:
        map_grid[treasure[0]][treasure[1]] = "Treasure"
    return map_grid, treasures

def move_hero(hero_location, direction, grid_size):
    row, col = hero_location
    if direction == "North" and row > 0:
        return (row - 1, col)
    elif direction == "South" and row < grid_size - 1:
        return (row + 1, col)
    elif direction == "East" and col < grid_size - 1:
        return (row, col + 1)
    elif direction == "West" and col > 0:
        return (row, col - 1)
    else:
        return hero_location

def interact_with_treasure(hero_location, map_grid, inventory):
    tile = map_grid[hero_location[0]][hero_location[1]]
    if tile == "Treasure":
        print("    |    You found a treasure!")
        if inventory["Keys"] > 0:
            print("    |    You used a key to collect the treasure!")
            inventory["Keys"] -= 1
            inventory["Treasures Collected"] += 1
            map_grid[hero_location[0]][hero_location[1]] = "Empty"
        else:
            if inventory["Health"] > 50 and inventory["Energy"] > 20:
                print("    |    You used strong effort to collect the treasure!")
                inventory["Health"] -= 10
                inventory["Energy"] -= 10
                inventory["Treasures Collected"] += 1
                map_grid[hero_location[0]][hero_location[1]] = "Empty"
            elif inventory["Energy"] <= 20:
                print("    |    Not enough energy to collect the treasure.")
            else:
                print("    |    Not enough health to collect the treasure.")
    elif tile == "Empty":
        print("    |    Nothing interesting here.")
    return inventory, map_grid