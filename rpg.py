import os
import json
import sys
from time import sleep
import random

if not os.path.exists("player"):
    os.makedirs("player")

m_player = None

p_enter = "Press Enter to Continue"

monster = {
    "name": "Goblin",
    "level": 1,
    "current_hp": 10,
    "max_hp": 10,
    "current_mp": 0,
    "max_mp": 0,
    "strength": 10,
    "speed": 8,
    "intellect": 5
}


def gprint(string=""):
    print(">", string)


def ginput(string=""):
    return input("> " + string)

def attack(person1, person2):

    p1_str = person1['strength']

    p1_spd = person1['speed']

    p2_str = person2['strength']

    p2_spd = person2['speed']

    hit_mod = .1

    atk_mod = .1

    p1_hit_chance = random.uniform(0, 1) + (p1_str * hit_mod) + (p1_spd * hit_mod)

    p2_dodge_chance = random.uniform(0, 1) + (p2_str * hit_mod) + (p2_spd * hit_mod)

    if p1_hit_chance < p2_dodge_chance:

        gprint(person1["name"] + " Missed!")

        return 0
    else:
        # TODO: Replace range with weapon power
        p1_atk_val = random.uniform(1, 6) + (p1_str * atk_mod)

        # TODO: Add Armor value to defense
        p2_def_val = p2_str

        damage = 0 if p1_atk_val - p2_def_val < 0 else p1_atk_val - p2_def_val

        gprint(person1["name"] + " hit for " + damage + " damage!")

        return damage





def flee(person1, person2):

    p1_spd = person1['speed']

    p2_spd = person2['speed']

    flee_mod = .1

    p1_flee_chance = random.uniform(0,1) + (p1_spd * flee_mod)

    p2_flee_defence = random.uniform(0,1) + (p2_spd * flee_mod)

    if p1_flee_chance > p2_flee_defence:
        return True
    else:
        return False


def init_combat_loop():
    global m_player
    global monster

    turn_list = []

    # Decide who goes first
    if m_player["speed"] > monster["speed"]:
        turn_list.append(m_player)
        turn_list.append(monster)
    else:
        turn_list.append(monster)
        turn_list.append(m_player)

    turn = 0

    while True:

        next_move = turn_list[turn % len(turn_list)]

        if next_move is m_player:
            gprint("Player Goes!")

            command = ginput("Enter a command, or enter h to list available commands\n")

            if command == "h":
                print("===================")
                print("Combat Commands")
                print("(a)ttack")
                print("(d)efend")
                print("(f)lee")
                print("===================")

            if command == "a":
                attack(m_player, monster)
                if is_dead(monster) is True:
                    break

            if command == "f":
                gprint(m_player["name"] + " attempts to flee!")
                if flee(m_player, monster):
                    gprint(m_player["name"] + " runs away!")
                    break
                else:
                    gprint("Can't run away! Fight to the death!!")

        elif next_move is monster:
            gprint("Monster Goes!")

        ginput(p_enter)
        turn += 1


def is_dead(person):
    is_dead = False

    if person["current_hp"] <= 0:
        is_dead = True

    return is_dead


def init_game_loop():
    global m_player

    init_input = True

    while True:
        os.system("clear")
        print_player_stats()
        if init_input == True:
            command = input("What would you like to do? Type h to list all options\n> ")
            init_input = False
        else:
            command = ginput()

        if command == "h":
            print("===================")
            print("Command List")
            print("(l)ook: observe your immediate surroundings")
            print("(f)ight: go look for some trouble")
            print("===================")
            ginput(p_enter)
        if command == "f":
            gprint(m_player["name"] + " goes looking for some trouble")
            for i in range(3):
                gprint("...")
                sleep(1)
            gprint("He finds it!!!")
            ginput(p_enter)
            init_combat_loop()


def print_player_stats():
    print("===================")
    print("Player Name:", m_player["name"])
    print("Lvl:", m_player["level"])
    print("HP:", m_player["current_hp"], "/", m_player["max_hp"])
    print("MP:", m_player["current_mp"], "/", m_player["max_mp"])
    print("Exp:", m_player["current_exp"], "/", m_player["next_level"])
    print("Strength:", m_player["strength"])
    print("Speed:", m_player["speed"])
    print("Intellect:", m_player["intellect"])
    print("===================")


def new_game(name, pclass):
    global m_player

    print("DEBUG: Creating and saving player:", name)

    player_stats = {
        "max_hp": 20,
        "current_hp": 20,
        "max_mp": 0,
        "current_mp": 0,
        "strength": 10,
        "speed": 10,
        "intellect": 10
    }

    # Warrior Class
    if pclass == 'w':
        player_stats["max_hp"] += 8
        player_stats["current_hp"] += 8
        player_stats["strength"] += 4
        player_stats["intellect"] -= 4
    # Thief Class
    if pclass == 't':
        player_stats["max_hp"] += 4
        player_stats["current_hp"] += 4
        player_stats["speed"] += 2
        player_stats["intellect"] -= 2
        player_stats["strength"] += 2
    # Mage Class
    if pclass == 'm':
        player_stats["max_hp"] += 4
        player_stats["current_hp"] += 4
        player_stats["intellect"] += 4
        player_stats["strength"] -= 4
    # Carl Class
    if pclass == 'c':
        player_stats["max_hp"] += 180
        player_stats["current_hp"] += 180
        player_stats["strength"] += 190
        player_stats["speed"] += 190
        player_stats["intellect"] += 190
    # Shared Stats
    player_stats["current_exp"] = 0
    player_stats["next_level"] = 100
    player_stats["level"] = 1
    player_stats["gold"] = 0
    player_stats["name"] = name

    m_player = player_stats

    with open("player/" + name + ".txt", "w") as file:
        file.write(json.dumps(player_stats))


def load_game(name):
    global m_player

    with open("player/" + name + ".txt", "r") as file:
        m_player = json.loads(file.read())
        print("Player Loaded:", m_player["name"])


if __name__ == "__main__":

    print("Welcome to Corey's RPG!!")
    print("Type '(n)ew' to start a new game")
    print("or '(l)oad' to continue your adventure")
    res = input("> ")

    if res == "new" or res == "n":
        print("Please enter choose a name for your character")
        name = input("> ")
        print("Welcome " + name + "!")
        print("Please select one of the following classes")
        print("-(W)arrior\n-(T)hief\n-(M)age\n-(C)arl")

        valid_class = False

        while not valid_class:
            pclass = input("> ")
            pclass = str(pclass[0]).lower()
            if pclass == 'w' or pclass == 't' or pclass == 'm' or pclass == 'c':
                new_game(name, pclass)
                valid_class = True
            else:
                print("Invalid class selected, please try again")

        print("Character Created Successfully!")
        print_player_stats()

    if res == "load" or res == "l":
        print("Which File would you like to load? Use the file number!!!")
        with os.scandir("player/") as player_files:
            p_count = 0
            pname_list = []
            for player_file in player_files:
                p_count += 1
                name = player_file.name
                name = name[:name.index(".")]
                pname_list.append(name)
                print("(" + str(p_count) + ") " + name)
        name_ind = input("> ")
        name = pname_list[int(name_ind) - 1]
        load_game(name)

    init_game_loop()