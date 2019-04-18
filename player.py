import helpers
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

    @property
    def isdead(self):
        return self.health < 1

    @property
    def isalive(self):
        return not self.isdead

    def print_stats(self):
        print("Name: {}".format(self.name))
        print("Attributes:")
        print()
        print("  * Attack: {}".format(self.attack))
        print("  * Defense: {}".format(self.defense))
        print("  * Speed: {}".format(self.speed))
        print()

    def createNewCharacter(self):
        while True:
            print("Welcome to P0 Dungeon Quest character creator!")
            self.name = input("Enter your name: ")
            if self.__assigned_points():
                break

    def __assigned_points(self):
        while True:
            print("You have 100 points to assign to your character.")
            print(
                "Start now to assign those Points to your characters attack, defense and speed."
            )

            for stat in ["Attack", "Defense", "Speed"]:
                new_value = helpers.validInput(
                    "{}: ".format(stat),
                    "Please input a positive integer.",
                    lambda s: s > 0,
                    cast=int,
                )
                setattr(self, stat.lower(), new_value)

            if self.attack + self.defense + self.speed <= 100:
                break

            print(
                "Sorry, it seems like you spent more than 100 ability points on your character... Try that again!"
            )
            print()

        print("Before you store your character please confirm your stats!")
        self.print_stats()
        answer = input("Is this correct? (Y/N) ")
        while answer.lower() not in ["y", "n"]:
            answer = input("Please enter Y/y for yes or N/n for no! ")
        if answer.lower() == "n":
            return False
        return True

    def listInventory(self):
        while True:
            if not self.inventory:
                print("Your inventory is empty.")
                return

            print("Welcome to your inventory {}!".format(self.name))
            print("These are your items:")
            print()
            for item in self.inventory:
                print("  * {0.name:<20} ({0.effect})".format(item))
            print()
            print("Type 'quit' or the name of the item you want to use/drop:")
            user_input = input("> ")
            if user_input == "quit":
                return
            try:
                user_item = self.getItemByName(user_input)
                print(
                    "Do you want to 'use' or 'drop' {}? Else 'quit'.".format(
                        user_item.name
                    )
                )
                user_input = input("> ")
                if user_input == "use":
                    self.use(user_item)
                    return
                elif user_input == "drop":
                    self.drop(user_item)
                    return
                else:
                    print("Nothing done.")
                    return

            except ValueError:
                print("Item does not exist.")

    def use(self, item):
        if item.passive_effect is True:
            print("You cannot use this item.")
        else:
            new_value = getattr(self, item.influenced_attribute) + item.amount
            setattr(self, item.influenced_attribute, new_value)

            self.remove(item)
            print("You used {0.name}.".format(item))
            print(
                "It increased your {0.influenced_attribute} by {0.amount}.".format(item)
            )
            print(
                "You now have {} {}.".format(
                    getattr(self, item.influenced_attribute), item.influenced_attribute
                )
            )

    def drop(self, item):
        print("You dropped {}.".format(item.name))
        self.remove(item)

    def remove(self, item):
        if item.passive_effect:
            new_value = getattr(self, item.influenced_attribute) - item.amount
            setattr(self, item.influenced_attribute, new_value)

        self.inventory.remove(item)

    def addItem(self, item):
        if item.passive_effect:
            new_value = getattr(self, item.influenced_attribute) + item.amount
            setattr(self, item.influenced_attribute, new_value)
        self.inventory.append(item)

    def getItemByName(self, name):
        for item in self.inventory:
            if item.name == name:
                return item
        raise ValueError("Invalid Item!")

    def die(self):
        while self.inventory:
            self.remove(self.inventory[0])

    def revive(self):
        self.health = 100
