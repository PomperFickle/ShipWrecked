import random

class Player:
    state = "Move"
    fixed_parts = [0,4]
    def __init__(self, name, loc, inventory, health):
        self.name = name
        self.location = loc
        self.inventory = inventory
        self.health = health
    def decision(self):
        choice_list = {"move","observe","fix", "inspect", "attack", "take", "interact", "drop", "help"}
        print("What will you do?")
        print(choice_list)
        decision = str(input()).replace(" ","").casefold()
        while decision not in choice_list:
            incr_response = ["I don't know what you mean!", "You can't do that right now.", "Choose an appropriate action.", "That makes no sense."]
            print(incr_response[random.randint(0,3)])
            print("What wil you do?")
            print(choice_list)
            decision = str(input()).strip().casefold()
        return decision
    def inspect(self, game_data):
        print("What item in your inventory would you like to inspect?")
        for key in self.inventory.keys():
            print(key)
        element = str(input()).replace(" ","").casefold()
        for item in self.inventory:
            if self.inventory[item].name == element:
                 self.inventory[item].inspect(game_data)
                 return
        print("I don't know what item you want to inspect.")
        return
    def move(self, game_data):
        print("Where would you like to go")
        print(self.location.adj_rooms)
        element = str(input()).replace(" ","").casefold()
        for adjroom in self.location.adj_rooms:
            if adjroom.casefold() == element:
                return game_data["gameworld"][adjroom]
        print("Invalid room.")
        return None
    def observe(self):
        print("What would you like to further observe?")
        element = str(input()).replace(" ","").casefold()
        for item in self.location.objects:
            if self.location.objects[item].name.replace(" ", "").casefold() == element:
                print(self.location.objects[item].desc)
                return
        print("Unable to observe this item.")
        return

    def fix(self,game_data):
        if self.location.name != "ShipRemains":
            print("You can't do that here.")
            return None
        print("What part of your ship would you like to fix?")
        for key in game_data["gameworld"]["ShipRemains"].objects["ship_components"]:
            print("-" + game_data["gameworld"]["ShipRemains"].objects["ship_components"][key].name)
        element = str(input()).replace(" ","").casefold()
        for ship_part in game_data["gameworld"]["ShipRemains"].objects["ship_components"]:
            if ship_part.replace(" ", "").casefold() == element:
                for item in self.inventory:
                    part = game_data["gameworld"]["ShipRemains"].objects["ship_components"][element]
                    if item.replace(" ","") == part.fix.replace(" ", ""):
                        print(part.desc)
                        print("You fixed the " + part.name + ".")
                        print("You've fixed " + str(self.fixed_parts[0]) + " out of " + str(self.fixed_parts[1]) + ".")
                        return game_data["gameworld"]["ShipRemains"].objects["ship_components"][element]
                print("You don't have the part needed to fix this!")
        print("That ship part doesn't exist.")
        return None

    def attack(self,game_data):
        print("What do you want to attack?")
        target = str(input()).replace(" ","").casefold()
        for enemy in self.location.enemies:
            if target == self.location.enemies[enemy]:
                print("What would you like to attack this enemy with?")
                weapon = str(input()).replace(" ", "").casefold()
                for item in self.inventory:
                    if weapon == item:
                        damage = self.location.enemies[enemy].damage(self.inventory[item])
                        return
        for area_obj in self.location.objects:
            if target == self.location.objects[area_obj].name.replace(" ", ""):
                print("What would you like to attack this object with?")
                weapon = str(input()).replace(" ", "").casefold()
                for item in self.inventory:
                    if weapon == item:
                        return [self.location.objects[area_obj], self.inventory[item]]
                print("Can't find that object.")
                return
        print("I don't see what you're trying to attack!")
    def damage(self, dmg):
        self.health -= dmg
        print("You took " + str(dmg) + " damage!")
    def take(self,game_data):
        print("What do you want to take?")
        for item in self.location.objects:
            print("-" + item)
        choice = str(input()).replace(" ","").casefold()
        for item in self.location.objects:
            if choice == item.replace(" ",""):
                if self.location.objects[item].pick_up:
                    print("You add '" + item + "' to your inventory.")
                    obj = self.location.objects[item]
                    del(self.location.objects[item])
                    return obj
                else:
                    print(choice + " cannot be added to your inventory.")
                    return
        print(choice + " cannot be found.")
        return None
    def interact(self,game_data):
        print("What do you wish to interact with?")
        for key in self.location.objects.keys():
            print("-" + key)
        for key in self.location.characters:
            print("-" + key)
        choice = str(input()).casefold().replace(" ", "")
        for key in self.location.objects:
            if choice == key.casefold():
                obj = self.location.objects[key]
                obj.interact(game_data)
                return
        for key in self.location.characters:
            if choice == key.casefold():
                self.location.characters[key].interact(game_data)
                return
        print("I don't know what object you're talking about.")
        return None
    def drop(self, game_data):
        print("What do you want to drop?")
        for item in self.inventory:
            print(item)
        choice = str(input()).replace(" ","")
        for item in self.inventory:
            if self.inventory[item].name == choice:
                self.location.objects[choice] = self.inventory[item]
                del(self.inventory[item])
                print("You dropped the " + choice + ".")
                return
        print("That item is not in your inventory.")
        return

    def help(self, game_data):
        print("HELP: typing 'observe' will let you get more details concerning certain objects in the area, 'fix' will let you fix parts of your ship provided you have the materials needed and are close to the ship, 'inspect' will let you closely examine objects in your inventory, 'throw' will let you throw an object from your inventory, 'take' will let you take certain objects lying around the map and 'interact' will let you execute certain actions with specific objects.")
        print("Location:")
        print(self.location)