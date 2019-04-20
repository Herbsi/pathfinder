from json_serialization import json_class


@json_class
class Inventory_Holder:
    def __init__(self):
        self.inventory = []

    def addItem(self, item):
        self.inventory.append(item)

    def removeItem(self, item):
        self.inventory.remove(item)

    def getItemByName(self, name):
        for item in self.inventory:
            if item.name == name:
                return item
        raise KeyError("Invalid Item!")

    def clear(self):
        while self.inventory:
            self.removeItem(self.inventory[0])

    def display(self):
        for item in self.inventory:
            print("  * {0.name:<20} ({0.effect})".format(item))
            # item.display()
