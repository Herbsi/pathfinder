import helpers
from inventory_holder import Inventory_Holder
from json_serialization import json_class


@json_class
class Chest(Inventory_Holder):
    # TODO chest is not being saved
    # TODO refactore openChest member
    def __init__(self, **chest):
        super().__init__()
        self.__dict__.update(chest)

    @property
    def chest_dict(self):
        return {1: self.deposit, 2: self.takeOut}

    def putIntoChest(self, item):
        self.addItem(item)
        print("You added {0.name} to the chest.".format(item))

    def chooseItem(self, name):
        try:
            return self.getItemByName(name)
        except KeyError:
            print("Invalid Item")
            return None

    def deposit(self, player):
        if not player.inventory:
            print("You have nothing to deposit")
            return

        print("Here are your items:")
        for item in player.inventory:
            print("  * {0.name}".format(item))

        print()
        print("Type 'quit' or the name of the item you want to deposit,")
        user_input = input("> ")
        if user_input == "quit":
            return
        try:
            user_item = player.getItemByName(user_input)
            user_input = helpers.validInput(
                "Deposit {0.name} in chest? (Y/N) ".format(user_item),
                "Error: Invalid input.",
                lambda c: c.lower() in ["y", "n"],
            )

            if user_input == "y":
                player.remove(user_item)
                self.putIntoChest(user_item)

            elif user_input == "n":
                print("Nothing done.")

        except KeyError:
            print("Item does not exist.")

    def takeOut(self, player):
        if not self.inventory:
            print("Your chest is empty.")
            return

        print("Here are the items in the chest: ")
        self.display()
        print()
        print("Type 'quit' or the name of the item you want to take out.")
        user_input = input("> ")
        if user_input == "quit":
            return
        try:
            user_item = self.getItemByName(user_input)
            user_input = helpers.validInput(
                "Take {0.name} out of chest? (Y/N) ".format(user_item),
                "Error: Invalid input.",
                lambda c: c.lower() in ["y", "n"],
            )

            if user_input == "y":
                self.inventory.remove(user_item)
                player.addItem(user_item)

            elif user_input == "n":
                print("Nothing done.")

        except KeyError:
            print("Item does not exist.")

    def openChest(self, player):
        option_count = 3

        def pre():
            print("Welcome to your chest!")
            print("What do you want to do?")
            print("  1) Deposit item")
            print("  2) Take out item")
            print("  0) Quit")
            print()

        while True:
            user_input = helpers.validInput(
                "> ",
                "Invalid choice. Try again.",
                lambda x: x in range(option_count),
                preamble=pre,
                cast=int,
            )

            if user_input == 0:
                return
            elif user_input == 1:
                self.deposit(player)
            elif user_input == 2:
                self.takeOut(player)
