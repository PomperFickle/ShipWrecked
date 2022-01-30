
class object:
    def __init__(self, name, desc, pick_up):
        self.name = name
        self.desc = desc
        self.pick_up = pick_up
    def interact(self, game_data):
        print("You cannot interact with this object.")
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def inspect(self, game_data):
        print(self.desc)
class food(object):
    def __init__(self, name, desc, pick_up, hp):
        super().__init__(name, desc, pick_up)
        self.hp = hp
    def inspect(self, game_data):
        super().inspect()
        print("Do you want to eat it?")
        choice = str(input()).replace(" ", "").casefold()
        if choice == "yes":
            game_data['player'].health += self.hp
            print("you ate the " + self.name + ".")
class weapon(object):
    def __init__(self, name, desc, pick_up):
        super().__init__(name, desc, pick_up)
class ship_component(object):
    def __init__(self, name, desc,fix,pick_up=False):
        super().__init__(name, desc, pick_up)
        self.fix = fix
class book(object):
    def __init__(self, name, desc, pick_up):
        super().__init__(name, desc, pick_up)
    def interact(self, game_data):
        print("The first page reads: " + self.desc)
    def inspect(self, game_data):
        print("The title reads '" + self.name + "'")
class container(object):
    def __init__(self, name, desc, contents,pick_up=False):
        super().__init__(name, desc, pick_up)
        self.contents = contents
    def interact(self, game_data):
        print("Which of the items would you like to interact with?")
        choice = str(input()).casefold()
        for item in self.contents:
            if choice == item.name:
                item.interact(game_data)
                return
        print("That item doesn't exist here.")
class fruittree(container):
    def __init__(self, name, desc, fruit, pick_up=False):
        super().__init__(name, desc, fruit, pick_up)
    def interact(self, game_data):
        print("The fruit is way too high to reach.")
    def damage(self, game_data, weapon):
        if weapon.name == "axe":
            print("With a few mighty chops, a " + self.contents.name + " falls to the ground.")
            game_data['player'].location.objects[self.contents.name] = self.contents

class chest(container):
    def __init__(self, name, desc, contents,locked=True):
        super().__init__(name, desc, contents)
        self.locked = locked
    def interact(self, game_data):
        if self.locked == True:
            print("It's locked.")
        else:
            print("The chest is open, in it contains: " + str(self.contents))
class padlock_chest(chest):
    def __init__(self, name, desc, contents,combo,locked=True):
        super().__init__(name, desc, contents, locked=locked)
        self.combo = combo
    def interact(self, game_data):
        super().interact(game_data)
        if self.locked:
            print("Enter the combination: ")
            attempt = str(input()).replace(" ","").casefold()
            if attempt == self.combo:
                print("The combination worked! The lock clicks open.")
                self.locked = False
                for thing in self.contents:
                    game_data['player'].location.objects[thing.name] = thing
                self.desc = "The padlock has opened, unlocking the chest."
            else:
                print("Looks like the combination didn't work.")
class key(object):
    def __init__(self, name, desc, pick_up, gate):
        super().__init__(name, desc, pick_up)
        self.gate = gate
    def interact(self, game_data):
        if game_data['player'].location.name == gate:
            print("You use the " + self.name + " to unlock the gate.")
            game_data['player'].location.unlock(game_data)
        else:
            print("You can't use that here!")

