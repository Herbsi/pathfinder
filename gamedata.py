from json_serialization import json_class


@json_class
class GameData:
    def __init__(self, **gamedata):
        self.player = None
        self.dungeon_room = None
        self.savefile = ""
        self.bonus_tasks = False
        self.__dict__.update(gamedata)
