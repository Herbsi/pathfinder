from json_serialization import json_class

@json_class
class Player:
    def __init__(self, **player):
        self.name = ""
        self.health = 100
        self.attack = 0
        self.defense = 0
        self.speed = 0
        self.gold = 100
        self.inventory = []
        self.__dict__.update(player)

    def print_stats(self):
        print("Name: {}".format(self.name))
        print("Attributes:")
        print()
        print("  * Attack: {}".format(self.attack))
        print("  * Defense: {}".format(self.defense))
        print("  * Speed: {}".format(self.speed))
        print()
