from json_serialization import json_class

@json_class
class Monster:
    def __init__(self, **data):
        self.health = 0
        self.attack = 0
        self.defense = 0
        self.speed = 0
        self.reward_min = 0
        self.reward_max = 0
        self.__dict__.update(data)
