class enemy():
    def __init__(self, desc, name,location, health, damage, weakness):
        self.name = name
        self.desc = desc
        self.location = location
        self.health = health
        self.damage = damage
        self.weakness = weakness
    def attack(self):
        return damage
    def damage(self, player_att):
        if player_att == self.weakness:
            print("Critical hit!")
class trap(enemy):
    def __init__(self, desc, name, location, health, damage, weakness):
        super().__init__(desc, name, location, health, damage, weakness)

