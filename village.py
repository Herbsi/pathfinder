import helpers
from item import Item
from json_serialization import json_class


def village(vill):
    while True:
        user_input = -1

        def pre():
            print("Welcome to Prog0 Village!")
            print("What do you want to do?")
            print()
            print("  1) Inventory")
            print("  2) Merchant")
            print("  3) Blacksmith")
            print("  4) Druid")
            print("  5) Dungeon")
            print("  6) Save game")
            print("  0) Quit game")
            print()

        user_input = helpers.validInput(
            "> ",
            "Invalid choice. Try again.",
            lambda x: x in range(7),
            preamble=pre,
            cast=int)

        if user_input in [0, 5, 6]:
            return user_input

        vill.village_dict[user_input]()


@json_class
class Village:
    def __init__(self, **village):
        self.player = None
        self.savefile = ""
        self.bonus_tasks = False
        self.__dict__.update(village)

    @property
    def village_dict(self):
        return {
            1: self.player.listInventory,
            2: self.merchant,
            3: self.blacksmith,
            4: self.druid,
        }

    def merchant(self):
        while True:
            if not self.player.inventory:
                print("Sorry, you have nothing to sell.")
                print("Thanks for visiting!")
                return

            print("Welcome to the merchant!")
            print(
                "You have {0.gold} gold. This is what I would pay for your items: "
                .format(self.player))

            for item in self.player.inventory:
                print("  * {:<20} for {:>4} gold".format(
                    item.name, item.price // 2))
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
                print("You now have {player.gold} gold left.".format(
                    player=self.player))
                print("Removed item from inventory.")
            except ValueError:
                print("You do not possess a {}.".format(user_input))

    def blacksmith(self):
        blacksmith_items = [
            Item(
                name="Helmet",
                price=3,
                influenced_attribute="defense",
                amount=2,
                passive_effect=True,
            ),
            Item(
                name="Chest plate",
                price=5,
                influenced_attribute="defense",
                amount=4,
                passive_effect=True,
            ),
            Item(
                name="Sword",
                price=10,
                influenced_attribute="attack",
                amount=5,
                passive_effect=True,
            ),
        ]
        self.shop("blacksmith", blacksmith_items)

    def druid(self):
        druid_items = [
            Item(
                name="Potion",
                price=3,
                influenced_attribute="health",
                amount=10,
                passive_effect=False,
            ),
            Item(
                name="Beer",
                price=2,
                influenced_attribute="speed",
                amount=(-2),
                passive_effect=False,
            ),
            Item(
                name="Coffee",
                price=5,
                influenced_attribute="speed",
                amount=2,
                passive_effect=False,
            ),
            Item(
                name="Antidote",
                price=15,
                influenced_attribute="defense",
                amount=6,
                passive_effect=False,
            ),
            Item(
                name="Milk",
                price=15,
                influenced_attribute="attack",
                amount=6,
                passive_effect=False,
            ),
        ]
        self.shop("druid", druid_items)

    def shop(self, shopkeeper, inventory):
        while True:
            print("Welcome to the {}".format(shopkeeper))
            print(
                "You have {player.gold} gold to spend. This is what I'm selling: "
                .format(player=self.player))

            self.pprintInventory(inventory)
            print()
            print("Type 'quit' or the name of the item you want to buy.")
            user_input = input("> ")
            if user_input == "quit":
                return
            for item in inventory:
                if item.name == user_input:
                    self.purchase(item)
                    break
            else:
                print("I do not sell '{}'.".format(user_input))

    def purchase(self, item):
        if self.player.gold >= item.price:
            self.player.gold -= item.price
            self.player.addItem(item)
            print("You have chosen {}.".format(item.name))
            print("You have {} gold left.".format(self.player.gold))
        else:
            print("Not enough gold.")

    def pprintInventory(self, inventory):
        for item in inventory:
            print("  * {i.name:<20} for {i.price:<4} gold ({i.effect})".format(
                i=item))
