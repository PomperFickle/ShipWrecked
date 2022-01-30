from objects import *
class Room:

    def __init__(self, name, desc, objects, adj_rooms,enemies, characters):
        self.name = name
        self.desc = desc
        self.objects = objects
        self.adj_rooms = adj_rooms
        self.enemies = enemies
        self.characters = characters
        def __str__(self):
            return self.name + ":" + self.desc
class LockedRoom(Room):
    def __init__(self, name, desc, objects, adj_rooms, enemies, characters, locked, numlocks, locked_area):
        super().__init__(name, desc, objects, adj_rooms, enemies, characters)
        self.locked = locked
        self.numlocks = numlocks
        self.locked_area = locked_area
    def unlock(self, game_data):
        self.numlocks -= 1
        print("There is " + str(self.numlocks) + " remaining.")
        if self.numlocks == 0:
            print("The gate to the next room is unlocked!")
            self.locked = False
            for area in self.locked_area:
                self.adj_rooms[area] = game_data['gameworld']