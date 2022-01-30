import enum
import random
from player import *
from objects import *
from enemies import *
from rooms import *
from world import *

def initialize(name):
    gameworld = {}
    for room in roomdict:
        gameworld[roomdict[room]["Name"]] = Room(roomdict[room]["Name"], roomdict[room]["desc"], roomdict[room]["objects"],roomdict[room]["adjacency"], roomdict[room]["enemies"], roomdict[room]["characters"])
    for room in lockedroomdict:
        gameworld[lockedroomdict[room]["Name"]] = LockedRoom(lockedroomdict[room]["Name"], lockedroomdict[room]["desc"], lockedroomdict[room]["objects"],lockedroomdict[room]["adjacency"], lockedroomdict[room]["enemies"], lockedroomdict[room]["characters"], lockedroomdict[room]["locked"], lockedroomdict[room]["locks"], lockedroomdict[room]["locked_area"])
    game_data = {"game_over": False, "player":Player(name, gameworld["Path2"], {}, 3),"entering": True, "gameworld": gameworld, "pieces": ["adhesive tape", "sailing rope", "patched fabric", "replacement helm"]}
    print("You are a crewmate on the Teal Maiden, a trading vessel used for transporting goods of all types across the breadth of the Carribean Sea. You and your crew are hirees employed by aristocrats to ensure all products get from one point to the other safe and sound. During a stormy night, your vessel capsized close to an island, and you awake the next morning with no idea of where your crew is, and where you are, for that matter. You must succeed in navigating through the island so that you may find the parts you need to repair your damaged ship, and escape the island.")
    print("HELP: typing 'observe' will let you get more details concerning certain objects in the area, 'fix' will let you fix parts of your ship provided you have the materials needed and are close to the ship, 'inspect' will let you closely examine objects in your inventory, 'attack' will deal damage and impact a enemy/object, 'take' will let you take certain objects lying around the map and 'interact' will let you execute certain actions with specific objects and NPCs, and 'drop' will drop a specified item from your inventory. Type 'help' to get a refresher on these commands and what room you're in.")
    return game_data

#### Game Loop ####
def main():
    name = input("What will your sailor's name be?\n")
    print(name + "'s story begins....")
    game_data = initialize(name)

    while game_data['game_over'] == False:
        render_desc(game_data)
        take_input(game_data)
        update_world(game_data)
    if game_data["player"].health == 0:
        print("Game Over. Try again? (Y/N)")
    else:
        print("You’ve managed to fix enough of your ship to get it back onto open water and sailing (fairly) smoothly. If your crew were present, and under happier circumstances, a song and some rum would be the first thing you’d all think to celebrate with. However, the instinctual survival skills enabled from the start of your adventure have made you weary, and despite your prolonged visit on the island, the rest of your crew is still uncounted for. An eerie silence falls upon the ship, broken up only by the sound of crashing waves, and the island fades out to a blot in your eyes as your ship sails away.")
        print("You won! Great Job! Play again? (Y/N)")
    choice = str(input()).casefold()
    if choice == "y":
        main()
    else:
        exit()
#### Game Loop ####

def render_desc(game_data):
    return render_helper(game_data)
def take_input(game_data):
    return input_helper(game_data)
def update_world(game_data):
    return update_helper(game_data)

####  Game Loop Helpers ####
def render_helper(game_data):
    if game_data["player"].location.name == "DirtyShore"  or game_data["player"].state[0] == "move":
        for level in game_data["gameworld"]:
            if game_data["gameworld"][level].name == game_data["player"].location.name:
                print(game_data["gameworld"][level].desc)
                break
    return game_data
def input_helper(game_data):
    decision = game_data["player"].decision()
    element = ""   
    if decision == "move":
        element = game_data["player"].move(game_data)
    if decision == "observe":
        game_data["player"].observe()
    if decision == "inspect":
        game_data["player"].inspect(game_data)
    if decision == "fix":
        element = game_data["player"].fix(game_data)
    if decision == "attack":
        element = game_data["player"].attack(game_data)
    if decision == "take":
        element = game_data["player"].take(game_data)
    if decision == "interact":
        game_data["player"].interact(game_data)
    if decision == "help":
        game_data["player"].help(game_data)
    if decision == "drop":
        game_data["player"].drop(game_data)

    game_data["player"].state = [decision, element]
    return game_data
def update_helper(game_data):
    if game_data["player"].health == 0 or game_data["player"].fixed_parts[0] == 4:
        game_data["game_over"] = True
    if game_data["player"].state[1] == None:
        return
    if game_data["player"].state[0] == "move":
        game_data["player"].location = game_data["player"].state[1]

    if game_data["player"].state[0] == "fix":
        del game_data["gameworld"]["ShipRemains"].objects["ship_components"][game_data["player"].state[1].name.replace(" ","")]
        del game_data["player"].inventory[game_data["player"].state[1].fix]

    if game_data["player"].state[0] == "attack":
        game_data["player"].state[1][0].damage(game_data, game_data["player"].state[1][1]) 

    if game_data["player"].state[0] == "take":
        game_data["player"].inventory[game_data["player"].state[1].name] = game_data["player"].state[1]
    return game_data
    ###Input Helpers###
#### Main Call ####
if __name__ == "__main__":
    main()