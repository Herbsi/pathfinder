from inventory_holder import Inventory_Holder
from json_serialization import json_class


@json_class
class Chest(Inventory_Holder):
    # TODO chest is not being saved
    # TODO refactore openChest member
    def __init__(self, **chest):
        super().__init__()
        self.__dict__.update(chest)

    def putIntoChest(self, item):
        self.addItem(item)
        print("You added {0.name} to the chest.".format(item))

    def chooseItem(self, name):
        try:
            return self.getItemByName(name)
        except KeyError:
            print("Invalid Item")
            return None

    def openChest(self, player):
        while True:
            print("Welcome to your chest")
            print("Would you like to take out or deposit an item? ")
            print("Type 'quit', 'take out' or 'deposit'.")
            user_input = input("> ")
            if user_input == "quit":
                return
            elif user_input == "take out":
                if not self.inventory:
                    print("Your chest is empty.")
                    continue

                print("Here are the items in the chest: ")
                self.display()
                print()
                print("Type 'quit' or the name of the item you want to take out:")
                user_input = input("> ")
                if user_input == "quit":
                    continue
                try:
                    user_item = self.getItemByName(user_input)
                    while True:
                        user_input = input(
                            "Take {0.name} out of chest? (Y/N) ".format(user_item)
                        )
                        if user_input.lower() in ["y", "n"]:
                            break
                        print("Error: Invalid input.")

                    if user_input == "y":
                        self.inventory.remove(user_item)
                        player.addItem(user_item)
                        continue

                    elif user_input == "n":
                        print("Nothing done.")
                        continue

                except KeyError:
                    print("Item does not exist.")

            elif user_input == "deposit":
                if not player.inventory:
                    print("You have nothing to deposit")
                    continue
                print("Here are your items:")
                for item in player.inventory:
                    print("  * {0.name}".format(item))

                print()
                print("Type 'quit' or the name of the item you want to deposit:")
                user_input = input("> ")
                if user_input == "quit":
                    continue
                try:
                    user_item = player.getItemByName(user_input)
                    while True:
                        user_input = input(
                            "Deposit {0.name} in chest? (Y/N) ".format(user_item)
                        )
                        if user_input.lower() in ["y", "n"]:
                            break
                        print("Error: Invalid input.")

                    if user_input == "y":
                        player.remove(user_item)
                        self.putIntoChest(user_item)
                        continue

                    elif user_input == "n":
                        print("Nothing done.")
                        continue

                except KeyError:
                    print("Item does not exist.")
            else:
                print("Error: Invalid Choice")
                continue
