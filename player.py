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

    def create_new_character(self):
        print("Welcome to P0 Dungeon Quest character creator!")
        self.name = input("Enter your name: ")
        self._assign_points()

    def _assign_points(self):
        print("You have 100 points to assign to you character.")
        print(
            "Start now to assign those Points to your characters attack, defense and speed."
        )
        self.attack = int(input("Attack: "))
        while self.attack <= 0:
            print("Please input a positive integer")
            self.attack = int(input("Attack: "))

        self.defense = int(input("Defense: "))
        while self.defense <= 0:
            print("Please input a positive integer")
            self.defense = int(input("Defense: "))

        self.speed = int(input("Speed: "))
        while self.speed <= 0:
            print("Please input a positive integer")
            self.speed = int(input("Speed: "))

        if self.attack + self.defense + self.speed > 100:
            print(
                "Sorry, it seems like you spent more than 100 ability points on your character... Try that again!"
            )
            print()
            self._assign_points()

        print("Before you store your character please confirm your stats!")
        self.print_stats()

        answer = input("Is this correct? (Y/N) ")
        while answer.lower() not in ["y", "n"]:
            answer = input("Please enter Y/y for yes or N/n for no!")
        if answer.lower() == "n":
            self.create_new_character()

    def list_inventory(self):
        while True:
            print("Welcome to your inventory {}".format(self.name))
            print("These are your items:")
            print()
            for item in self.inventory:
                print("  * {}\t\t{}".format(item.name, item.effect))
            print()
            print("Type 'quit' or the name of the item you want to use/drop:")
            user_input = input("> ")
            try:
                user_item = self.get_item_by_name(user_input)
                user_does = input(
                    "Do you want to 'use' or 'drop' {}? Else 'quit'.".format(user_item.name)
                )
                # TODO mabye change to dictionary
                if user_does == "use":
                    self.use(user_item)
                    print("You used {}".format(user_input))
                elif user_does == "drop":
                    self.drop(user_item)
                    print("You dropped {}".format(user_input))
                elif user_does == "quit":
                    print("Nothing done.")
                else:
                    print("Nothing done.")
                    return
            else:
            except ValueError:
                print("Item does not exist")


    @property
    def item_names(self):
        return [item.name for item in self.inventory]

    @property
    def attributes(self):
        return
    {
        "health"  : self.health,
        "attack"  : self.attack,
        "defense" : self.defense,
        "speed"   : self.speed
    }

    def use(self, item):
        if item.passive_effect == False:
            print("You cannot use this item.")
        else:
            self.attributes[item.influenced_attribute] += item.amount
            self.remove(item)
            print("You used {}".format(item.name))
            print("It increased your {} by {}".format(item.influenced_attribute, item.amount))
            print("You now have {} {}".format(self.attributes[item.influenced_attribute], item.influenced_attribute))

    def drop(self, item):
        print("You dropped {}.".format(item.name))
        self.remove(item)

    def remove(self, item):
        self.inventory.remove(item)

    def get_item_by_name(self, name):
        for item in self.inventory:
            if item.name == name:
                return item
        raise ValueError("Invalid Item!")

    def addItem(self, item):
        self.inventory.append(item)
