class animal():
    def __init__(self, name, dialogue):
        self.name = name
        self.dialogue = dialogue
    def interact(self, game_data):
        print("- - -" + self.name + "- - -")

class koala(animal):
    def __init__(self, name, dialogue,fruit, part):
        super().__init__(name, dialogue)
        self.fruit = fruit
        self.part = part
    def interact(self, game_data):
        super().interact(game_data)
        print(self.dialogue)
        if self.part != None:
            for thing in game_data['player'].location.objects:
                if thing == self.fruit:
                    print("The koala promptly flings itself down from its nest and snatches the " + thing + ". In return, it drops a " + self.part.name + ".")
                    game_data['player'].location.objects[self.part.name] = self.part
                    del(game_data['player'].location.objects[self.fruit])
                    self.dialogue = "The koala doesn't look like it wants to waste anymore time on you. It's too preoccupied with eating its " + self.fruit + "."
                    return

class deity():
    def __init__(self, riddle, answer, reward, beaten):
        self.riddle = riddle
        self.answer = answer
        self.reward = reward
        self.beaten = beaten
    def interact(self, game_data):
        if self.beaten == False:
            print("The mysterious entity asks you in a booming voice: " + self.riddle)
            print("How do you answer?")
            response = str(input()).replace(" ","").casefold()
            if response == self.answer:
                print("The entity responds: 'CORRECT.'. A key suddenly materializes in the middle of the room.")
                self.beaten = True
                game_data['player'].location.objects[self.reward.name] = self.reward
            else:
                print("The entity responds: 'INCORRECT'. Suddenly, you feel a excrutiatingly pain which shoots up from your chest to your head.")
                game_data['player'].damage(1)
        else:
            print("The entity has nothing to say to you.")