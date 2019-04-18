from item import Item

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


class Shopkeeper:
    def __init__(self, **shopkeeper):
        self.name = ""
        self.inventory = []
        self.__dict__.update(shopkeeper)

    def shop(self, player):
        while True:
            print("Welcome to the {}".format(self.name))
            print(
                "You have {0.gold} gold to spend. This is what I'm selling: ".format(
                    player
                )
            )

            for item in self.inventory:
                print(
                    "  * {i.name:<20} for {i.price:<4} gold ({i.effect})".format(i=item)
                )
            print()
            print("Type 'quit' or the name of the item you want to buy.")
            user_input = input("> ")
            if user_input == "quit":
                return
            for item in self.inventory:
                if item.name == user_input:
                    self.purchase(player, item)
                    break
            else:
                print("I do not sell '{}'.".format(user_input))

    def purchase(self, player, item):
        if player.gold >= item.price:
            player.gold -= item.price
            player.addItem(item)
            print("You have chosen {}.".format(item.name))
            print("You have {} gold left.".format(player.gold))
        else:
            print("Not enough gold.")
