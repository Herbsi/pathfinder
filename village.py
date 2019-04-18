import helpers
from gravedigger import Gravedigger
from item import Item
from json_serialization import json_class
from shopkeeper import Shopkeeper, blacksmith_items, druid_items


@json_class
class Village:
    def __init__(self, **village):
        self.player = None
        self.bonus_tasks = False
        self.blacksmith = None
        self.druid = None
        self.gravedigger = None
        self.__dict__.update(village)

    @property
    def village_dict(self):
        return {
            1: self.player.listInventory,
            2: self.merchant,
            3: self.shopAtBlacksmith,
            4: self.shopAtDruid,
            7: self.shopAtGravedigger,
        }

    def merchant(self):
        while True:
            if not self.player.inventory:
                print("Sorry, you have nothing to sell.")
                print("Thanks for visiting!")
                return

            print("Welcome to the merchant!")
            print(
                "You have {0.gold} gold. This is what I would pay for your items: ".format(
                    self.player
                )
            )

            for item in self.player.inventory:
                print("  * {:<20} for {:>4} gold".format(item.name, item.price // 2))
            print()
            print("Type 'quit' or the name of the item you want to sell.")
            user_input = input("> ")
            if user_input == "quit":
                return
            try:
                user_item = self.player.getItemByName(user_input)
                self.player.gold += user_item.price // 2
                self.player.remove(user_item)
                print("You have chosen {item.name}.".format(item=user_item))
                print(
                    "You now have {player.gold} gold left.".format(player=self.player)
                )
                print("Removed item from inventory.")
            except ValueError:
                print("You do not possess a {}.".format(user_input))

    def shopAt(self, shopkeeper):
        shopkeeper.shop(self.player)

    def shopAtBlacksmith(self):
        self.shopAt(self.blacksmith)

    def shopAtDruid(self):
        self.shopAt(self.druid)

    def shopAtGravedigger(self):
        self.gravedigger.shop(self.player)
