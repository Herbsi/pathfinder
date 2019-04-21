from json_serialization import json_class
from shopkeeper import Shopkeeper


@json_class
class Gravedigger(Shopkeeper):
    def __init__(self, **gravedigger):
        self.name = "gravedigger"
        self.inventory = []
        self.__dict__.update(gravedigger)

    @property
    def selling_price(self):
        return (
            sum([item.price // 2 for item in self.inventory]) if self.inventory else 0
        )

    def shop(self, player):
        if not self.inventory:
            print("I have nothing to sell.")
            print("Goddbye.")
            return

        print("Welcome to the {}".format(self.name))
        print(
            "You have {0.gold} gold to spend. This is what I'm selling: ".format(player)
        )

        for item in self.inventory:
            print("  * {i.name:<20} ({i.effect})".format(i=item, p=item.price // 2))
        print("Total: {}".format(self.selling_price))
        print()
        print("Type 'quit' or 'buy' if you want to buy back your inventory.")
        user_input = input("> ")
        if user_input == "quit":
            return
        elif user_input == "buy":
            self.purchase(player)
        else:
            print("I do not sell '{}'.".format(user_input))

    def purchase(self, player):
        if player.gold >= self.selling_price:
            player.gold -= self.selling_price
            while self.inventory:
                # for loop does not gurantee entire inventory
                item = self.inventory[0]
                player.addItem(item)
                self.inventory.remove(item)
                print("{} added to your inventory.".format(item.name))
            print("You have {} gold left.".format(player.gold))
        else:
            print("Not enough gold")
